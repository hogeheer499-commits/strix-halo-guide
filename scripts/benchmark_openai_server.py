#!/usr/bin/env python3
"""Benchmark an OpenAI-compatible streaming completion endpoint.

The script is intentionally dependency-free. It is used for vLLM, but can also
target other OpenAI-compatible local servers.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
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
    prompt_tokens: int | None
    tokens: int | None
    ttft_s: float
    wall_s: float
    mean_decode_interval_s: float | None
    request_wall_tps: float | None
    stop: bool
    error: str
    chunks: int
    finish_reason: str | None
    count_source: str
    completion_mode: str


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
        value = json.loads(data)
        return value if isinstance(value, dict) else {"error": "SSE payload is not an object"}
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
    completion_mode: str = "fixed",
) -> RequestResult:
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": 0,
        "stream": True,
        "stream_options": {"include_usage": True},
        "ignore_eos": completion_mode == "fixed",
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
    prompt_tokens = None
    completion_tokens = None
    chunks = 0
    stop = False
    error = ""
    finish_reason = None
    done = False

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            for raw_line in response:
                parsed = parse_sse_line(raw_line)
                if not parsed:
                    continue
                if parsed.get("done"):
                    done = True
                    break
                if parsed.get("error"):
                    error = str(parsed["error"])
                    break
                usage = parsed.get("usage")
                if usage is not None:
                    if not isinstance(usage, dict):
                        raise ValueError("usage is not an object")
                    for key in ("prompt_tokens", "completion_tokens"):
                        value = usage.get(key)
                        if type(value) is not int or value < 0:
                            raise ValueError(f"invalid usage.{key}")
                    prompt_tokens = usage["prompt_tokens"]
                    completion_tokens = usage["completion_tokens"]
                choices = parsed.get("choices") or []
                for choice in choices:
                    text = choice.get("text") or ""
                    if not isinstance(text, str):
                        raise ValueError("completion text is not a string")
                    if text:
                        chunks += 1
                        if first_token is None:
                            first_token = time.perf_counter()
                    if choice.get("finish_reason"):
                        if not isinstance(choice["finish_reason"], str):
                            raise ValueError("finish_reason is not a string")
                        finish_reason = choice["finish_reason"]
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8", errors="replace")
        except Exception:
            detail = str(exc)
        error = f"HTTP {exc.code}: {detail[:240]}"
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"

    end = time.perf_counter()
    stop = done and finish_reason in {"stop", "length"}
    if not error:
        if not stop:
            error = "incomplete stream or unsupported finish reason"
        elif not chunks:
            error = "no visible completion content"
        elif completion_tokens is None or completion_tokens <= 0:
            error = "trusted completion token usage unavailable"
        elif completion_mode == "fixed" and completion_tokens != max_tokens:
            error = "fixed-length token budget not met"
    wall_s = end - start
    ttft_s = (first_token - start) if first_token is not None else wall_s
    gen_s = max(end - (first_token if first_token is not None else start), 1e-9)
    # End includes the protocol/usage tail. This is NOT token-gap telemetry.
    interval = gen_s / (completion_tokens - 1) if not error and completion_tokens > 1 else None
    # Request throughput includes prefill and the protocol tail consistently.
    request_tps = completion_tokens / wall_s if not error and wall_s > 0 else None
    return RequestResult(
        np=np_value,
        rep=rep,
        request=request_index,
        phase=phase,
        prompt_tokens=prompt_tokens,
        tokens=completion_tokens,
        ttft_s=ttft_s,
        wall_s=wall_s,
        mean_decode_interval_s=interval,
        request_wall_tps=request_tps,
        stop=stop,
        error=error,
        chunks=chunks,
        finish_reason=finish_reason,
        count_source="server_usage" if completion_tokens is not None else "unknown",
        completion_mode=completion_mode,
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
    completion_mode: str = "fixed",
) -> tuple[list[RequestResult], dict[str, Any]]:
    batch_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=np_value) as pool:
        futures = [
            pool.submit(run_one, url, model, np_value, rep, idx, phase, max_tokens, timeout, prompt, completion_mode)
            for idx in range(np_value)
        ]
        results = [future.result() for future in as_completed(futures)]
    batch_wall = time.perf_counter() - batch_start
    results.sort(key=lambda item: item.request)
    valid = [item for item in results if not item.error]
    total_tokens = sum(item.tokens for item in valid)
    errors = sum(1 for item in results if item.error)
    ttfts = [item.ttft_s for item in valid]
    itls = [item.mean_decode_interval_s for item in valid if item.mean_decode_interval_s is not None]
    request_tps = [item.request_wall_tps for item in valid]
    summary = {
        "np": np_value,
        "rep": rep,
        "phase": phase,
        "requests": np_value,
        "valid_requests": len(valid),
        "completion_mode": completion_mode,
        "total_tokens": total_tokens,
        "batch_wall_s": batch_wall,
        "aggregate_tps": total_tokens / batch_wall if not errors and batch_wall > 0 else None,
        "mean_request_wall_tps": statistics.fmean(request_tps) if request_tps and not errors else None,
        "mean_ttft_s": statistics.fmean(ttfts) if ttfts and not errors else None,
        "p95_ttft_s": percentile(ttfts, 0.95) if ttfts and not errors else None,
        "mean_request_mean_decode_interval_s": statistics.fmean(itls) if itls and not errors else None,
        "p95_request_mean_decode_interval_s": percentile(itls, 0.95) if itls and not errors else None,
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
    parser.add_argument("--completion-mode", choices=("fixed", "natural"), default="fixed")
    parser.add_argument("--cache-policy", default="unknown", help="Recorded server/prompt cache policy; this flag does not configure the server")
    parser.add_argument("--detail", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    if min(args.np_value, args.tokens, args.reps, args.timeout) <= 0:
        parser.error("np, tokens, reps and timeout must be positive")
    metadata = {"cache_policy": args.cache_policy,
                "prompt_sha256": hashlib.sha256(args.prompt.encode()).hexdigest(),
                "prompt_characters": len(args.prompt),
                "requested_output_tokens": args.tokens,
                "warmup_batches": 1, "warmup_requests": args.np_value}

    all_results: list[RequestResult] = []
    summaries: list[dict[str, Any]] = []

    warm_results, warm_summary = run_batch(
        args.url, args.model, args.np_value, -1, "warmup", args.tokens, args.timeout, args.prompt, args.completion_mode
    )
    all_results.extend(warm_results)
    warm_summary.update(metadata)
    print(json.dumps(warm_summary), flush=True)

    for rep in range(args.reps):
        results, summary = run_batch(
            args.url, args.model, args.np_value, rep, "measure", args.tokens, args.timeout, args.prompt, args.completion_mode
        )
        all_results.extend(results)
        summary.update(metadata)
        summaries.append(summary)
        print(json.dumps(summary), flush=True)

    detail_rows = [result.__dict__ for result in all_results]
    write_rows(args.detail, detail_rows)
    write_rows(args.summary, summaries)

    if warm_summary["errors"] or any(row["errors"] for row in summaries):
        sys.exit(2)


if __name__ == "__main__":
    main()
