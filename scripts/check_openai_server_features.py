#!/usr/bin/env python3
"""Probe OpenAI-compatible local server features.

This is a compatibility probe, not a quality benchmark. It records whether a
local server exposes common OpenAI-style endpoints used by chat apps, coding
tools, agents, and the benchmark harness.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class Probe:
    name: str
    ok: bool
    status: int
    elapsed_s: float
    detail: str
    transport_accepted: bool = False
    client_verified: bool = False


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
        return {"error": f"bad json: {data[:160]}"}


def build_headers(api_key: str | None = None) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def request_json(
    base_url: str,
    path: str,
    method: str,
    payload: dict[str, Any] | None,
    timeout: float,
    api_key: str | None,
) -> tuple[bool, int, float, Any]:
    url = base_url.rstrip("/") + path
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=build_headers(api_key), method=method)
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
            elapsed = time.perf_counter() - start
            try:
                return True, response.status, elapsed, json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                return True, response.status, elapsed, raw[:400]
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return False, exc.code, time.perf_counter() - start, detail[:400]
    except Exception as exc:
        return False, 0, time.perf_counter() - start, f"{type(exc).__name__}: {exc}"


def request_streaming_chat(
    base_url: str,
    model: str,
    timeout: float,
    api_key: str | None,
) -> tuple[bool, int, float, str]:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Reply with exactly five words."}],
        "max_tokens": 16,
        "temperature": 0,
        "stream": True,
    }
    req = urllib.request.Request(
        base_url.rstrip("/") + "/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers=build_headers(api_key),
        method="POST",
    )
    start = time.perf_counter()
    chunks = 0
    done = False
    finish = False
    first_chunk_s: float | None = None
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
                    return False, response.status, time.perf_counter() - start, str(parsed["error"])
                choices = parsed.get("choices") or []
                for choice in choices:
                    content = (choice.get("delta") or {}).get("content")
                    if isinstance(content, str) and content.strip():
                        chunks += 1
                        if first_chunk_s is None:
                            first_chunk_s = time.perf_counter() - start
                    if choice.get("finish_reason") in ("stop", "length"):
                        finish = True
        elapsed = time.perf_counter() - start
        if chunks and done and finish:
            return True, response.status, elapsed, f"{chunks} SSE chunks; first chunk {first_chunk_s:.3f}s"
        return False, response.status, elapsed, "missing visible SSE content or terminal completion"
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return False, exc.code, time.perf_counter() - start, detail[:400]
    except Exception as exc:
        return False, 0, time.perf_counter() - start, f"{type(exc).__name__}: {exc}"


def summarize_models(payload: Any) -> str:
    if not isinstance(payload, dict):
        return str(payload)[:160]
    data = payload.get("data")
    if isinstance(data, list):
        ids = [str(item.get("id", "")) for item in data if isinstance(item, dict)]
        return f"{len(ids)} models: {', '.join(ids[:5])}"
    return "models response without data list"


def completion_probe(payload: Any) -> str:
    if not isinstance(payload, dict):
        return str(payload)[:160]
    choices = payload.get("choices") or []
    if not choices:
        return "no choices"
    text = choices[0].get("text") if isinstance(choices[0], dict) else ""
    return f"text chars={len(text or '')}"


def chat_probe(payload: Any) -> str:
    if not isinstance(payload, dict):
        return str(payload)[:160]
    choices = payload.get("choices") or []
    if not choices or not isinstance(choices[0], dict):
        return "no choices"
    message = choices[0].get("message") or {}
    content = message.get("content") if isinstance(message, dict) else ""
    reasoning = ""
    if isinstance(message, dict):
        reasoning = message.get("reasoning_content") or message.get("reasoning") or ""
    return f"content chars={len(content or '')}; reasoning chars={len(reasoning or '')}"


def tool_probe(payload: Any) -> str:
    if not isinstance(payload, dict):
        return str(payload)[:160]
    choices = payload.get("choices") or []
    if not choices or not isinstance(choices[0], dict):
        return "no choices"
    message = choices[0].get("message") or {}
    tool_calls = message.get("tool_calls") if isinstance(message, dict) else None
    if tool_calls:
        return f"tool_calls={len(tool_calls)}"
    content = message.get("content") if isinstance(message, dict) else ""
    reasoning = ""
    if isinstance(message, dict):
        reasoning = message.get("reasoning_content") or message.get("reasoning") or ""
    return f"no tool_calls; content chars={len(content or '')}; reasoning chars={len(reasoning or '')}"


def semantic_success(kind: str, payload: Any, model: str) -> bool:
    """Validate bounded response shape/content; never claim a client task ran."""
    if not isinstance(payload, dict) or payload.get("error"):
        return False
    if kind == "models":
        data = payload.get("data")
        return isinstance(data, list) and any(isinstance(item, dict) and item.get("id") == model for item in data)
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices or not isinstance(choices[0], dict):
        return False
    choice = choices[0]
    if kind == "completion":
        return isinstance(choice.get("text"), str) and bool(choice["text"].strip()) and choice.get("finish_reason") in ("stop", "length")
    message = choice.get("message")
    if not isinstance(message, dict):
        return False
    if kind == "chat":
        return isinstance(message.get("content"), str) and bool(message["content"].strip()) and choice.get("finish_reason") in ("stop", "length")
    calls = message.get("tool_calls")
    if not isinstance(calls, list) or not calls or choice.get("finish_reason") != "tool_calls":
        return False
    for call in calls:
        if not isinstance(call, dict) or call.get("type") != "function" or not isinstance(call.get("id"), str) or not call["id"]:
            return False
        function = call.get("function")
        if not isinstance(function, dict) or function.get("name") != "get_weather":
            return False
        try:
            arguments = json.loads(function.get("arguments", ""))
        except (ValueError, TypeError):
            return False
        if not isinstance(arguments, dict) or not isinstance(arguments.get("city"), str) or arguments["city"].strip().casefold() != "paris":
            return False
    return True


def response_probe(name: str, kind: str, accepted: bool, status: int, elapsed: float, payload: Any, model: str) -> Probe:
    success = accepted and semantic_success(kind, payload, model)
    return Probe(name, success, status, elapsed,
                 "validated response content/shape" if success else "response did not satisfy content/shape contract",
                 transport_accepted=accepted)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Base URL, for example http://127.0.0.1:8080")
    parser.add_argument("--model", required=True)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    probes: list[Probe] = []

    ok, status, elapsed, payload = request_json(args.url, "/v1/models", "GET", None, args.timeout, args.api_key)
    probes.append(response_probe("/v1/models", "models", ok, status, elapsed, payload, args.model))

    completion_payload = {
        "model": args.model,
        "prompt": "Reply with exactly five words.",
        "max_tokens": 16,
        "temperature": 0,
        "stream": False,
    }
    ok, status, elapsed, payload = request_json(
        args.url, "/v1/completions", "POST", completion_payload, args.timeout, args.api_key
    )
    probes.append(response_probe("/v1/completions", "completion", ok, status, elapsed, payload, args.model))

    chat_payload = {
        "model": args.model,
        "messages": [{"role": "user", "content": "Reply with exactly five words."}],
        "max_tokens": 16,
        "temperature": 0,
        "stream": False,
    }
    ok, status, elapsed, payload = request_json(
        args.url, "/v1/chat/completions", "POST", chat_payload, args.timeout, args.api_key
    )
    probes.append(response_probe("/v1/chat/completions", "chat", ok, status, elapsed, payload, args.model))

    ok, status, elapsed, detail = request_streaming_chat(args.url, args.model, args.timeout, args.api_key)
    probes.append(Probe("/v1/chat/completions stream", ok, status, elapsed, detail, 200 <= status < 300))

    tool_payload = {
        "model": args.model,
        "messages": [
            {
                "role": "user",
                "content": "Use the get_weather tool to check the weather in Paris. Do not answer from memory.",
            }
        ],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get current weather for a city.",
                    "parameters": {
                        "type": "object",
                        "properties": {"city": {"type": "string"}},
                        "required": ["city"],
                    },
                },
            }
        ],
        "tool_choice": "auto",
        "max_tokens": 64,
        "temperature": 0,
        "stream": False,
    }
    ok, status, elapsed, payload = request_json(
        args.url, "/v1/chat/completions", "POST", tool_payload, args.timeout, args.api_key
    )
    probes.append(response_probe("/v1/chat/completions tools auto", "tools", ok, status, elapsed, payload, args.model))
    tool_payload["tool_choice"] = {"type": "function", "function": {"name": "get_weather"}}
    ok, status, elapsed, payload = request_json(
        args.url, "/v1/chat/completions", "POST", tool_payload, args.timeout, args.api_key
    )
    probes.append(response_probe("/v1/chat/completions tools forced", "tools", ok, status, elapsed, payload, args.model))

    result = {
        "url": args.url,
        "model": args.model,
        "probes": [asdict(probe) for probe in probes],
    }

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    for probe in probes:
        marker = "ok" if probe.ok else "FAIL"
        print(f"{marker:4} {probe.name:32} status={probe.status} elapsed={probe.elapsed_s:.3f}s {probe.detail}")

    core_ok = all(probe.ok for probe in probes if probe.name in {"/v1/models", "/v1/chat/completions", "/v1/chat/completions stream"})
    sys.exit(0 if core_ok else 2)


if __name__ == "__main__":
    main()
