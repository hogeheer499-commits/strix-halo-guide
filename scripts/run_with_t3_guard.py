#!/usr/bin/env python3
"""Run a benchmark with explicit optional health and memory guards.

The historical filename is retained for compatibility. No private workstation
service is required by default. Health URLs must return a JSON object with ok=true.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request


DEFAULT_URLS: list[str] = []

PROTECTED_CLEANUP_PATTERN = re.compile(
    r"("
    r"t3code|t3-react185|t3_react185|:3773\b|:3774\b|:3777\b|pkill\s+.*node|killall\s+node|"
    r"hermes|docker\s+(stop|restart|kill|rm)|docker\s+compose\s+down"
    r")",
    re.IGNORECASE,
)


def read_meminfo() -> dict[str, int]:
    values: dict[str, int] = {}
    with open("/proc/meminfo", "r", encoding="utf-8") as handle:
        for line in handle:
            key, raw_value = line.split(":", 1)
            parts = raw_value.strip().split()
            if parts:
                values[key] = int(parts[0]) * 1024
    return values


def gib(value: int) -> float:
    return value / 1024 / 1024 / 1024


def url_ok(url: str, timeout: float) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            if response.status != 200:
                return False
            payload = json.loads(response.read(65537))
            return isinstance(payload, dict) and payload.get("ok") is True
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        return False


def validate_cleanup(commands: list[str]) -> None:
    for command in commands:
        if PROTECTED_CLEANUP_PATTERN.search(command):
            raise SystemExit(f"refusing cleanup command that could affect protected workflow services: {command}")


def run_cleanup(commands: list[str]) -> None:
    for command in commands:
        subprocess.run(command, shell=True, check=False)


def terminate_process(process: subprocess.Popen[object], grace_seconds: float) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    # The leader may exit while descendants remain. Check the owned process
    # group rather than treating leader exit as proof of complete cleanup.
    deadline = time.monotonic() + grace_seconds
    while time.monotonic() < deadline:
        process.poll()  # reap the leader when possible
        try:
            os.killpg(process.pid, 0)
        except ProcessLookupError:
            return
        time.sleep(min(0.05, max(0, deadline - time.monotonic())))
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()


def guard_reason(
    urls: list[str],
    timeout: float,
    failures: dict[str, int],
    max_failures: int,
    min_mem_available_gib: float,
    min_swap_free_gib: float,
) -> str | None:
    meminfo = read_meminfo()
    mem_available = gib(meminfo.get("MemAvailable", 0))
    swap_free = gib(meminfo.get("SwapFree", 0))

    if mem_available < min_mem_available_gib:
        return f"MemAvailable below threshold: {mem_available:.1f} GiB < {min_mem_available_gib:.1f} GiB"
    if swap_free < min_swap_free_gib:
        return f"SwapFree below threshold: {swap_free:.1f} GiB < {min_swap_free_gib:.1f} GiB"

    for url in urls:
        if url_ok(url, timeout):
            failures[url] = 0
            continue
        failures[url] += 1
        if failures[url] >= max_failures:
            return f"configured health check failed {failures[url]} times: {url}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", action="append", default=[], help="Optional health URL returning JSON {ok:true}; no URL defaults")
    parser.add_argument("--interval", type=float, default=5.0)
    parser.add_argument("--timeout", type=float, default=3.0)
    parser.add_argument("--max-failures", type=int, default=2)
    parser.add_argument("--min-mem-available-gib", type=float, default=16.0)
    parser.add_argument("--min-swap-free-gib", type=float, default=0.0)
    parser.add_argument("--cleanup-cmd", action="append", default=[], help="Cleanup command for the benchmark only")
    parser.add_argument("--grace-seconds", type=float, default=15.0)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.interval <= 0 or args.timeout <= 0 or args.max_failures < 1 or min(args.grace_seconds, args.min_mem_available_gib, args.min_swap_free_gib) < 0:
        parser.error("interval/timeout/failure count must be positive; thresholds/grace must be nonnegative")

    urls = args.url or DEFAULT_URLS
    failures = {url: 0 for url in urls}
    validate_cleanup(args.cleanup_cmd)

    reason = guard_reason(
        urls,
        args.timeout,
        failures,
        1,
        args.min_mem_available_gib,
        args.min_swap_free_gib,
    )
    if reason:
        print(f"[t3-guard] preflight failed: {reason}", file=sys.stderr)
        return 98
    if args.preflight_only:
        print("[t3-guard] preflight passed")
        return 0

    command = args.command[1:] if args.command and args.command[0] == "--" else args.command
    if not command:
        parser.error("missing command after --")

    process = None
    try:
        process = subprocess.Popen(command, start_new_session=True)
        while process.poll() is None:
            reason = guard_reason(
                urls,
                args.timeout,
                failures,
                args.max_failures,
                args.min_mem_available_gib,
                args.min_swap_free_gib,
            )
            if reason:
                print(f"[t3-guard] aborting benchmark: {reason}", file=sys.stderr)
                return 99
            time.sleep(args.interval)
        return process.returncode or 0
    finally:
        try:
            if process is not None:
                terminate_process(process, args.grace_seconds)
        finally:
            run_cleanup(args.cleanup_cmd)


if __name__ == "__main__":
    raise SystemExit(main())
