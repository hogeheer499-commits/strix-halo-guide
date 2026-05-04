#!/usr/bin/env python3
"""Benchmark an OpenAI-compatible streaming completion endpoint.

The script is intentionally dependency-free. It is used for vLLM, but can also
target other OpenAI-compatible local servers.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROMPT = (
    "Write a dense technical note about local LLM inference performance on "
    "unified-memory systems. Continue until the token budget is exhausted."
)


@dataclass
class RequestResult:
    np: int
    rep: int
    request: int
    phase: str
    prompt_tokens: int
    tokens: int
    ttft_s: float
    wall_s: float
    itl_s: float
    request_tps: float
    stop: bool
    error: str


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    rank = (len(ordered) - 1) * pct
    lo = int(rank)
    hi = min(lo + 1, len(ordered) - 1)
    frac = rank - lo
    return ordered[lo] * (1 - frac) + ordered[hi] * frac


def parse_sse_line(line: bytes) -> dict[str, Any] | None:
    text = line.decode("utf-8", errors="replace").strip()
    if not text or not text.startswith("data:"):
        return None
    data = text[5:].strip()
    if data == "[DONE]":
        return {"done": True}
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return {"error": f"bad json: {data[:120]}"}


def run_one(
    url: str,
    model: str,
    np_value: int,
    rep: int,
    request_index: int,
    phase: str,
    max_tokens: int,
    timeout: float,
    prompt: str,
) -> RequestResult:
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": 0,
        "stream": True,
        "stream_options": {"include_usage": True},
        "ignore_eos": True,
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url.rstrip("/") + "/v1/completions",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    start = time.perf_counter()
    first_token: float | None = None
    prompt_tokens = 0
    completion_tokens = 0
    chunks = 0
    stop = False
    error = ""

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            for raw_line in response:
                parsed = parse_sse_line(raw_line)
                if not parsed:
                    continue
                if parsed.get("done"):
                    stop = True
                    break
                if parsed.get("error"):
                    error = str(parsed["error"])
                    continue
                usage = parsed.get("usage")
                if usage:
                    prompt_tokens = int(usage.get("prompt_tokens") or prompt_tokens or 0)
                    completion_tokens = int(usage.get("completion_tokens") or completion_tokens or 0)
                choices = parsed.get("choices") or []
                for choice in choices:
                    text = choice.get("text") or ""
                    if text:
                        chunks += 1
                        if first_token is None:
                            first_token = time.perf_counter()
                    if choice.get("finish_reason"):
                        stop = True
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8", errors="replace")
        except Exception:
            detail = str(exc)
        error = f"HTTP {exc.code}: {detail[:240]}"
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"

    end = time.perf_counter()
    if completion_tokens <= 0:
        completion_tokens = chunks if chunks else 0
    wall_s = end - start
    ttft_s = (first_token - start) if first_token is not None else wall_s
    gen_s = max(end - (first_token if first_token is not None else start), 1e-9)
    itl_s = gen_s / max(completion_tokens - 1, 1)
    request_tps = completion_tokens / gen_s if completion_tokens else 0.0
    return RequestResult(
        np=np_value,
        rep=rep,
        request=request_index,
        phase=phase,
        prompt_tokens=prompt_tokens,
        tokens=completion_tokens,
        ttft_s=ttft_s,
        wall_s=wall_s,
        itl_s=itl_s,
        request_tps=request_tps,
        stop=stop,
        error=error,
    )


def run_batch(
    url: str,
    model: str,
    np_value: int,
    rep: int,
    phase: str,
    max_tokens: int,
    timeout: float,
    prompt: str,
) -> tuple[list[RequestResult], dict[str, Any]]:
    batch_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=np_value) as pool:
        futures = [
            pool.submit(run_one, url, model, np_value, rep, idx, phase, max_tokens, timeout, prompt)
            for idx in range(np_value)
        ]
        results = [future.result() for future in as_completed(futures)]
    batch_wall = time.perf_counter() - batch_start
    results.sort(key=lambda item: item.request)
    total_tokens = sum(item.tokens for item in results)
    errors = sum(1 for item in results if item.error)
    ttfts = [item.ttft_s for item in results]
    itls = [item.itl_s for item in results]
    request_tps = [item.request_tps for item in results]
    summary = {
        "np": np_value,
        "rep": rep,
        "phase": phase,
        "requests": np_value,
        "total_tokens": total_tokens,
        "batch_wall_s": batch_wall,
        "aggregate_tps": total_tokens / batch_wall if batch_wall > 0 else 0.0,
        "mean_request_tps": statistics.fmean(request_tps) if request_tps else 0.0,
        "mean_ttft_s": statistics.fmean(ttfts) if ttfts else 0.0,
        "p95_ttft_s": percentile(ttfts, 0.95),
        "mean_itl_s": statistics.fmean(itls) if itls else 0.0,
        "p95_itl_s": percentile(itls, 0.95),
        "errors": errors,
    }
    return results, summary


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--np", dest="np_value", type=int, required=True)
    parser.add_argument("--tokens", type=int, default=128)
    parser.add_argument("--reps", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=600)
    parser.add_argument("--prompt", default=PROMPT)
    parser.add_argument("--detail", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    all_results: list[RequestResult] = []
    summaries: list[dict[str, Any]] = []

    warm_results, warm_summary = run_batch(
        args.url, args.model, args.np_value, -1, "warmup", args.tokens, args.timeout, args.prompt
    )
    all_results.extend(warm_results)
    print(json.dumps(warm_summary), flush=True)

    for rep in range(args.reps):
        results, summary = run_batch(
            args.url, args.model, args.np_value, rep, "measure", args.tokens, args.timeout, args.prompt
        )
        all_results.extend(results)
        summaries.append(summary)
        print(json.dumps(summary), flush=True)

    detail_rows = [result.__dict__ for result in all_results]
    write_rows(args.detail, detail_rows)
    write_rows(args.summary, summaries)

    if any(row["errors"] for row in summaries):
        sys.exit(2)


if __name__ == "__main__":
    main()
