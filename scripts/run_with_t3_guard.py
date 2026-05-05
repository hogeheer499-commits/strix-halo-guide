#!/usr/bin/env python3
"""Run a command while keeping the T3 workstation path alive.

Strix Halo work on this machine is operated from T3. This wrapper starts a
benchmark command only after T3 is reachable, then monitors T3, memory, and swap
while the command runs. If T3 becomes unhealthy or memory headroom gets too low,
the benchmark command is terminated and optional cleanup commands are run.
"""

from __future__ import annotations

import argparse
import os
import re
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request


DEFAULT_URLS = [
    "http://127.0.0.1:3773/",
    "http://192.168.2.13:3773/",
    "http://127.0.0.1:3777/__t3react185/health",
    "http://192.168.2.13:3777/",
]

PROTECTED_CLEANUP_PATTERN = re.compile(
    r"("
    r"t3code|t3-react185|t3_react185|:3773\b|:3777\b|pkill\s+.*node|killall\s+node|"
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
            return 200 <= response.status < 400
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def validate_cleanup(commands: list[str]) -> None:
    for command in commands:
        if PROTECTED_CLEANUP_PATTERN.search(command):
            raise SystemExit(f"refusing cleanup command that could affect protected workflow services: {command}")


def run_cleanup(commands: list[str]) -> None:
    for command in commands:
        subprocess.run(command, shell=True, check=False)


def terminate_process(process: subprocess.Popen[object], grace_seconds: float) -> None:
    if process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=grace_seconds)
        return
    except subprocess.TimeoutExpired:
        pass
    except ProcessLookupError:
        return
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


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
            return f"T3 health check failed {failures[url]} times: {url}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", action="append", default=[], help="T3 URL to guard; defaults cover 3773 and 3777")
    parser.add_argument("--interval", type=float, default=5.0)
    parser.add_argument("--timeout", type=float, default=3.0)
    parser.add_argument("--max-failures", type=int, default=2)
    parser.add_argument("--min-mem-available-gib", type=float, default=16.0)
    parser.add_argument("--min-swap-free-gib", type=float, default=2.0)
    parser.add_argument("--cleanup-cmd", action="append", default=[], help="Cleanup command for the benchmark only")
    parser.add_argument("--grace-seconds", type=float, default=15.0)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()

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

    process = subprocess.Popen(command, preexec_fn=os.setsid)
    try:
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
                terminate_process(process, args.grace_seconds)
                run_cleanup(args.cleanup_cmd)
                return 99
            time.sleep(args.interval)
    except KeyboardInterrupt:
        terminate_process(process, args.grace_seconds)
        run_cleanup(args.cleanup_cmd)
        raise

    return process.returncode or 0


if __name__ == "__main__":
    raise SystemExit(main())
