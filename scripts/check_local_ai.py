#!/usr/bin/env python3
"""Read-only Linux setup checks; not yet run on a fresh Ollama 0.31.2 install.

Run from the guide checkout: python3 scripts/check_local_ai.py boot|answer|report
The answer check sends one fixed, nonprivate task to native loopback Ollama.
Report only reads metadata; it never loads a model or sends an inference request.
Report exits: 0 = known allocation (GPU, CPU or mixed), 2 = unknown/incomplete,
1 = stopped/error. None establishes execution, speed or broad model quality.
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
REPORT_TIMEOUT = 10  # Per GET; at most two GETs, no retries.
GUIDE_URL = "https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/LOCAL_CHAT_START.md"
# Report prose is kept here and in render_report for editorial review.
REPORT_NEXT = {
    "GPU": "Free next step: check the visible answer separately in the guide's Step 5.",
    "CPU": "Free next step: follow the guide's CPU fallback troubleshooting before checking speed.",
    "mixed": "Free next step: review model/context memory needs and CPU fallback troubleshooting.",
    "unknown": "Free next step: review the guide's Step 6 and failure table; no model was loaded by this report.",
    "STOP": "Free next step: review the guide's listener/service failure steps; do not open the service to the network.",
}
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
        raise CheckFailed("Choose exactly one check: boot, answer or report (use --help for usage).")


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


def check_listeners(tables=None, *, quiet=False):
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
    if not quiet:
        print("OK listener: 127.0.0.1:11434 only")


@contextmanager
def request_deadline(seconds=TOTAL_TIMEOUT):
    # A socket inactivity timeout alone cannot bound slowly arriving headers or
    # body bytes. Linux SIGALRM also bounds the entire request, including those.
    def expired(_signum, _frame):
        raise TimeoutError("total request deadline")

    previous_handler = signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)


def fetch_json(path, payload=None, *, timeout=TOTAL_TIMEOUT, strict=False):
    # http.client connects directly: no proxy environment, OLLAMA_HOST, DNS
    # target override, redirect following, cloud fallback or retry loop.
    connection = http.client.HTTPConnection(HOST, PORT, timeout=CONNECT_TIMEOUT)
    try:
        with request_deadline(timeout):
            connection.connect()
            connection.auto_open = 0
            connection.sock.settimeout(timeout)
            if payload is None:
                connection.request("GET", path)
            else:
                connection.request("POST", path, json.dumps(payload).encode("utf-8"),
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
        return json.loads(body, object_pairs_hook=unique_json_object,
                          parse_constant=invalid_json_constant) if strict else json.loads(body)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise CheckFailed("Ollama returned invalid JSON.") from exc


def unique_json_object(pairs):
    """Do not silently choose one of conflicting JSON fields in a report."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result


def invalid_json_constant(_value):
    raise ValueError("non-finite JSON number")


def fetch_answer():
    return fetch_json("/api/chat", PAYLOAD)


def fetch_metadata(path):
    if path not in ("/api/version", "/api/ps"):
        raise CheckFailed("Unsupported metadata endpoint.")
    return fetch_json(path, timeout=REPORT_TIMEOUT, strict=True)


def read_metadata_file(path):
    """Bound proc reads and never return raw contents to report output."""
    try:
        with path.open(encoding="ascii") as source:
            text = source.read(MAX_RESPONSE_BYTES + 1)
        return text if len(text) <= MAX_RESPONSE_BYTES else None
    except (OSError, UnicodeError):
        return None


def system_metadata():
    memory = None
    text = read_metadata_file(Path("/proc/meminfo"))
    if text is not None:
        rows = [line for line in text.splitlines() if line.startswith("MemTotal:")]
        match = re.fullmatch(r"MemTotal:\s+([0-9]{1,16})\s+kB\s*", rows[0]) if len(rows) == 1 else None
        if match and 0 < int(match[1]) <= (2**63 - 1) // 1024:
            memory = int(match[1]) * 1024  # Linux meminfo kB is KiB.
    kernel = "unknown"
    try:
        # Custom kernel suffixes can contain private names. Only numeric release.
        match = re.match(r"([0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,6})(?:$|[-+])", os.uname().release)
        if match:
            kernel = match[1]
    except OSError:
        pass
    text = read_metadata_file(Path("/proc/cmdline"))
    boot = {}
    for expected in BOOT_PARAMETERS:
        key = expected.split("=", 1)[0]
        values = [] if text is None else [token for token in text.split() if token.split("=", 1)[0] == key]
        boot[key] = ("unknown" if text is None else "absent" if not values
                     else "conflicting" if len(values) > 1 else "match" if values == [expected]
                     else "different")
    groups = {name: "unknown" for name in ("render", "video")}
    try:
        active = set(os.getgroups()) | {os.getegid()}
        for name in groups:
            try:
                groups[name] = "active" if grp.getgrnam(name).gr_gid in active else "inactive"
            except KeyError:
                groups[name] = "absent"
            except OSError:
                pass
    except OSError:
        pass
    return {"memory_bytes": memory, "kernel": kernel, "boot": boot, "groups": groups}


def allocation_metadata(reply):
    """Classify only the exact guide model's loaded row; never choose a fallback.

    Ollama v0.31.2 server/routes.go PsHandler exposes runtime totalSize/MemorySize
    and vramSize as size and size_vram (bytes), not /api/tags download size.
    cmd/cmd.go ListRunningHandler and https://docs.ollama.com/faq describe the
    allocation labels. We require positive size and valid int64 fields before
    classifying, including CPU: zero/zero is unknown, not a loaded-model proof.
    """
    if not isinstance(reply, dict) or "error" in reply or not isinstance(reply.get("models"), list):
        return "unknown", "invalid model metadata", None
    selected = []
    for row in reply["models"]:
        if not isinstance(row, dict):
            return "unknown", "invalid model row", None
        # Both are supplied by upstream. Reject conflicting identities rather
        # than treating a missing/malformed identifier as a different model.
        name, model = row.get("name"), row.get("model")
        if not isinstance(name, str) or not name or model != name:
            return "unknown", "invalid model identity", None
        if name == MODEL:
            selected.append(row)
    if len(selected) != 1:
        return "unknown", "selected model not loaded" if not selected else "ambiguous selected model", None
    row = selected[0]
    size, vram = row.get("size"), row.get("size_vram")
    if (type(size) is not int or type(vram) is not int
            or not 0 < size <= 2**63 - 1 or not 0 <= vram <= size):
        return "unknown", "invalid allocation fields", None
    state = "CPU" if vram == 0 else "GPU" if vram == size else "mixed"
    return state, "Ollama allocation metadata", (size, vram)


def runtime_version(reply):
    version = reply.get("version") if isinstance(reply, dict) and "error" not in reply else None
    # No arbitrary local build labels, paths, identifiers or API error text.
    return version if isinstance(version, str) and re.fullmatch(
        r"[0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}(?:-rc[0-9]{1,4})?", version) else "unknown"


def render_report(system, version, allocation, *, stopped=False):
    """Only allowlisted fields reach this renderer; no API/host blobs or errors."""
    state, reason, sizes = allocation
    print("Local AI report (metadata only)")
    memory = system["memory_bytes"]
    if memory is None:
        print("Memory: unknown")
    else:
        gib = memory / 2**30
        near = next((n for n in (32, 64, 96, 128, 192) if abs(gib - n) <= 8), None)
        band = f"near {near} GiB" if near is not None else "unclassified"
        print(f"Memory: {gib:.2f} GiB MemTotal; {band} (approximate visible-memory class, not installed RAM/SKU)")
    print(f"Kernel: {system['kernel']} (numeric release only)")
    print("Boot parameters (128GB reference only): " + "; ".join(f"{k}={v}" for k, v in system["boot"].items()))
    print("Session GPU groups: " + "; ".join(f"{k}={v}" for k, v in system["groups"].items()))
    print("Profile: metadata cannot confirm installed capacity; use the matching manual route, never copy the 128GB boot values to another size.")
    print(f"Ollama version: {version}")
    print(f"Selected model: {MODEL} (exact tag only)")
    print(f"Allocation: {state} ({reason})")
    if sizes is not None:
        print(f"Reported bytes: size={sizes[0]}, size_vram={sizes[1]}")
    print("Scope: allocation is not proof of GPU execution, correct answers or speed; boot/answer checks were not run.")
    print(REPORT_NEXT["STOP" if stopped else state])
    print(f"Guide: {GUIDE_URL}#if-a-step-fails")


def check_report():
    """0 known allocation; 2 unknown/incomplete metadata; 1 refused/failed read.

    Exit 0 includes CPU/mixed and is not a setup/GPU/boot acceptance result.
    Known boot mismatches are observations, never recommendations or fixes.
    """
    system = system_metadata()
    version = "unknown"
    allocation = ("unknown", "not read", None)
    stopped = None
    try:
        try:
            check_listeners(quiet=True)
        except CheckFailed:
            # Existing listener messages contain the fixed endpoint; a shareable
            # report prints neither addresses nor untrusted exception contents.
            stopped = "Listener contract not met or unreadable; no HTTP request was sent."
        if stopped is None:
            version = runtime_version(fetch_metadata("/api/version"))
            allocation = allocation_metadata(fetch_metadata("/api/ps"))
    except TimeoutError:
        stopped = "Metadata request timed out (5s connect, 10s total per GET); no retry."
    except CheckFailed:
        stopped = "Listener or metadata check failed; no further request was sent."
    except (OSError, http.client.HTTPException):
        stopped = "Cannot read local runtime metadata; no retry."
    except KeyboardInterrupt:
        stopped = "Report cancelled."
    render_report(system, version, allocation, stopped=stopped is not None)
    if stopped:
        print(f"STOP: {stopped}")
        return 1
    incomplete = (allocation[0] == "unknown" or version == "unknown"
                  or system["memory_bytes"] is None or system["kernel"] == "unknown"
                  or "unknown" in system["boot"].values() or "unknown" in system["groups"].values())
    print("REPORT: incomplete/unknown" if incomplete else "REPORT: complete (allocation only)")
    return 2 if incomplete else 0


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
    parser.add_argument("check", choices=("boot", "answer", "report"))
    try:
        args = parser.parse_args(argv)
        if args.check == "boot":
            check_boot()
        elif args.check == "report":
            return check_report()
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
