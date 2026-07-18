#!/usr/bin/env python3
import argparse
import json
import time
import urllib.request
from pathlib import Path


def post_json(url: str, payload: dict) -> tuple[dict, float]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.monotonic()
    with urllib.request.urlopen(request, timeout=900) as response:
        body = json.load(response)
    return body, time.monotonic() - started


def make_prompt(target_tokens: int) -> str:
    sentence = (
        "A local AI workstation must balance memory capacity, decode speed, "
        "software compatibility, energy use, reproducibility, and data privacy. "
    )
    # The server response records the authoritative tokenizer count. This only
    # creates stable short and long prompt shapes without private source text.
    words = sentence.split()
    repeated = (words * ((target_tokens // len(words)) + 1))[:target_tokens]
    return " ".join(repeated) + "\nSummarize the tradeoffs in five concise bullets."


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    for shape, target_tokens in (("4k", 4096), ("16k", 16384)):
        for repeat in range(1, 4):
            payload = {
                "model": args.model,
                "prompt": make_prompt(target_tokens),
                "max_tokens": 256,
                "temperature": 0,
                "top_k": 1,
                "seed": 42,
                "cache_prompt": False,
                "stream": False,
            }
            response, wall_s = post_json(
                f"{args.base_url}/v1/completions", payload
            )
            record = {
                "profile": args.profile,
                "shape": shape,
                "repeat": repeat,
                "wall_s": wall_s,
                "request": payload,
                "response": response,
            }
            rows.append(record)
            with (args.out / f"{args.profile}.jsonl").open("a") as handle:
                handle.write(json.dumps(record) + "\n")

    tool_payload = {
        "model": args.model,
        "messages": [
            {
                "role": "user",
                "content": "Use the calculator tool to add 395 and 128.",
            }
        ],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "calculator",
                    "description": "Add two integers.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "integer"},
                            "b": {"type": "integer"},
                        },
                        "required": ["a", "b"],
                    },
                },
            }
        ],
        "tool_choice": "auto",
        "temperature": 0,
        "max_tokens": 128,
    }
    tool_response, wall_s = post_json(
        f"{args.base_url}/v1/chat/completions", tool_payload
    )
    (args.out / f"{args.profile}.tool-smoke.json").write_text(
        json.dumps(
            {"wall_s": wall_s, "request": tool_payload, "response": tool_response},
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
