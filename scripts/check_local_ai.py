#!/usr/bin/env python3
"""Read-only Linux setup checks; not yet run on a fresh Ollama 0.31.2 install.

Run from the guide checkout: python3 scripts/check_local_ai.py boot|answer
The answer check sends one fixed, nonprivate task to native loopback Ollama.
Neither check establishes GPU placement, speed or broad model quality.
"""

import argparse
from contextlib import contextmanager
import grp
import http.client
import json
import os
from pathlib import Path
import re
import signal
import socket
import sys


BOOT_PARAMETERS = (
    "amdgpu.gttsize=131072",
    "ttm.pages_limit=31457280",
    "amdgpu.cwsr_enable=0",
)
MODEL = "qwen3.6:35b-a3b"
HOST, PORT = "127.0.0.1", 11434
CONNECT_TIMEOUT, TOTAL_TIMEOUT = 5, 180
MAX_RESPONSE_BYTES = 64 * 1024
EXPECTED_ANSWER = "STRIX_CHECK=391"
PAYLOAD = {
    "model": MODEL,
    "messages": [{"role": "user", "content":
                  "Compute 17 * 23. Reply with exactly this format and no other text: STRIX_CHECK=<integer>"}],
    "think": False,
    "stream": False,
    "options": {"num_ctx": 8192, "temperature": 0, "seed": 42, "num_predict": 96},
}


class CheckFailed(Exception):
    """An expected setup failure, reported without a traceback."""


class CheckParser(argparse.ArgumentParser):
    def error(self, message):
        raise CheckFailed("Choose exactly one check: boot or answer (use --help for usage).")


def check_boot(cmdline_path=Path("/proc/cmdline")):
    try:
        tokens = cmdline_path.read_text(encoding="ascii").split()
        session_groups = set(os.getgroups()) | {os.getegid()}
    except (OSError, UnicodeError) as exc:
        raise CheckFailed("Cannot read boot settings or current session groups.") from exc

    good = True
    for expected in BOOT_PARAMETERS:
        key = expected.split("=", 1)[0]
        actual = [token for token in tokens if token.split("=", 1)[0] == key]
        matches = actual == [expected]
        print(("OK " if matches else "MISSING ") + expected)
        good = good and matches
    for name in ("render", "video"):
        try:
            present = grp.getgrnam(name).gr_gid in session_groups
        except KeyError:
            present = False
        except OSError as exc:
            raise CheckFailed("Cannot read the system group database.") from exc
        print(("OK " if present else "MISSING ") + name + " in current session")
        good = good and present
    if not good:
        raise CheckFailed("Boot parameters or session groups are missing/conflicting; review the boot and GPU access steps.")


def listener_addresses(text, ipv6=False):
    """Parse kernel TCP rows, failing closed on incomplete/unknown table data."""
    lines = text.splitlines()
    if not lines or lines[0].split()[:4] not in (
        ["sl", "local_address", "rem_address", "st"],
        ["sl", "local_address", "remote_address", "st"],
    ):
        raise CheckFailed("Cannot interpret TCP listener data; no request was sent.")
    width = 32 if ipv6 else 8
    endpoint = re.compile(rf"[0-9A-Fa-f]{{{width}}}:[0-9A-Fa-f]{{4}}")
    addresses = []
    for line in lines[1:]:
        if not line.strip():
            continue
        fields = line.split()
        if (len(fields) < 10 or not re.fullmatch(r"[0-9]+:", fields[0])
                or not endpoint.fullmatch(fields[1])
                or not endpoint.fullmatch(fields[2])
                or not re.fullmatch(r"[0-9A-Fa-f]{2}", fields[3])
                or int(fields[3], 16) not in range(1, 14)):
            raise CheckFailed("Cannot interpret TCP listener data; no request was sent.")
        address, port = fields[1].split(":")
        if int(port, 16) != PORT or int(fields[3], 16) != 0x0A:
            continue
        if ipv6:
            # Even ::1 or IPv4-mapped IPv6 is outside this exact IPv4 profile.
            addresses.append("IPv6")
        else:
            packed = int(address, 16).to_bytes(4, sys.byteorder)
            addresses.append(socket.inet_ntop(socket.AF_INET, packed))
    return addresses


def check_listeners(tables=None):
    if tables is None:
        tables = (Path("/proc/net/tcp"), Path("/proc/net/tcp6"))
    if len(tables) != 2:
        raise CheckFailed("Both TCP listener tables are required; no request was sent.")
    addresses = []
    for path, ipv6 in zip(tables, (False, True)):
        try:
            text = path.read_text(encoding="ascii")
        except (OSError, UnicodeError) as exc:
            raise CheckFailed("Cannot read both TCP listener tables; no request was sent.") from exc
        addresses.extend(listener_addresses(text, ipv6))
    if not addresses:
        raise CheckFailed("Service not ready: no listener on port 11434; no request was sent.")
    if any(address != HOST for address in addresses):
        raise CheckFailed("Port 11434 has a non-profile listener; require only 127.0.0.1, with no IPv6 or broader listener. No request was sent.")
    print("OK listener: 127.0.0.1:11434 only")


@contextmanager
def request_deadline():
    # A socket inactivity timeout alone cannot bound slowly arriving headers or
    # body bytes. Linux SIGALRM also bounds the entire request, including those.
    def expired(_signum, _frame):
        raise TimeoutError("total request deadline")

    previous_handler = signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, TOTAL_TIMEOUT)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)


def fetch_answer():
    # http.client connects directly: no proxy environment, OLLAMA_HOST, DNS
    # target override, redirect following, cloud fallback or retry loop.
    connection = http.client.HTTPConnection(HOST, PORT, timeout=CONNECT_TIMEOUT)
    try:
        with request_deadline():
            connection.connect()
            connection.auto_open = 0
            connection.sock.settimeout(TOTAL_TIMEOUT)
            connection.request("POST", "/api/chat", json.dumps(PAYLOAD).encode("utf-8"),
                               {"Content-Type": "application/json"})
            response = connection.getresponse()
            if response.status != 200:
                raise CheckFailed(f"Ollama returned HTTP {response.status}; no redirect was followed.")
            length = response.getheader("Content-Length")
            if length is not None and (not re.fullmatch(r"[0-9]{1,10}", length)
                                       or int(length) > MAX_RESPONSE_BYTES):
                raise CheckFailed("Ollama response size is invalid or exceeds the 64KiB limit.")
            body = response.read(MAX_RESPONSE_BYTES + 1)
            if len(body) > MAX_RESPONSE_BYTES:
                raise CheckFailed("Ollama response exceeds the 64KiB limit.")
    finally:
        connection.close()
    try:
        return json.loads(body)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise CheckFailed("Ollama returned invalid JSON.") from exc


def check_answer():
    check_listeners()
    reply = fetch_answer()
    if not isinstance(reply, dict):
        raise CheckFailed("Ollama reply is not a JSON object.")
    if "error" in reply:
        raise CheckFailed("Ollama returned an error; inspect its redacted service log.")
    message = reply.get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), str):
        raise CheckFailed("Ollama reply has no visible answer text.")
    answer = message["content"].strip()
    # Bound terminal output too; render control characters instead of executing
    # terminal escapes from a malformed model response.
    visible = "".join(char if char.isprintable() else repr(char)[1:-1]
                      for char in answer[:240])
    print("Answer:", visible + (" [truncated]" if len(answer) > 240 else ""))
    done, reason = reply.get("done"), reply.get("done_reason")
    print("Completion:", done if type(done) is bool else "missing/invalid",
          reason if reason in ("stop", "length") else "missing/invalid")
    if not answer:
        raise CheckFailed("Ollama returned an empty answer.")
    if done is not True or reason != "stop":
        raise CheckFailed("The request did not complete normally (need done=true and done_reason=stop).")
    if answer.count(EXPECTED_ANSWER) > 1:
        raise CheckFailed("The answer repeated instead of completing the known task.")
    if answer != EXPECTED_ANSWER:
        raise CheckFailed("The known-answer task failed: expected STRIX_CHECK=391.")


def main(argv=None):
    parser = CheckParser(description=__doc__)
    parser.add_argument("check", choices=("boot", "answer"))
    try:
        args = parser.parse_args(argv)
        if args.check == "boot":
            check_boot()
        else:
            check_answer()
    except CheckFailed as exc:
        print(f'STOP: {exc} → see "If A Step Fails"')
        return 1
    except TimeoutError:
        print('STOP: Request timed out (5s connect, 180s total) → see "If A Step Fails"')
        return 1
    except (OSError, http.client.HTTPException) as exc:
        print(f'STOP: Cannot complete the check ({type(exc).__name__}); check the service and retry deliberately → see "If A Step Fails"')
        return 1
    except KeyboardInterrupt:
        print('STOP: Check cancelled → see "If A Step Fails"')
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
