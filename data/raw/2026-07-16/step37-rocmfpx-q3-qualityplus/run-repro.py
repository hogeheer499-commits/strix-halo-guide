#!/usr/bin/env python3
"""Reproduce the Step 3.7 ROCmFPX Q3 QualityPlus Strix Halo profile."""

import json
import pathlib
import shlex
import statistics
import subprocess
import time
import urllib.error
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parent
MODEL_ROOT = pathlib.Path("/home/hoge-heer/benchmark-models/2026-07-16/step37")
TARGET = MODEL_ROOT / "target/Step-3.7-Flash-ROCmFPX-Q3-QualityPlus-00001-of-00009.gguf"
DRAFT = MODEL_ROOT / "draft/Step-3.7-Flash-MTP-Q8_0.gguf"
TEMPLATE = MODEL_ROOT / "target/step37-native-tool-response-template.jinja"
SERVER = pathlib.Path("/home/hoge-heer/ROCmFPX-ciru/build-strix-rocmfp4/bin/llama-server")
PORT = 18037
BASE_URL = f"http://127.0.0.1:{PORT}"


def request_json(path, payload=None, timeout=900):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        BASE_URL + path,
        data=data,
        headers={"Content-Type": "application/json"},
    )
    started = time.monotonic()
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response), time.monotonic() - started


def wait_for_server(process, timeout=1800):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"server exited with code {process.returncode}")
        try:
            health, _ = request_json("/health", timeout=5)
            if health.get("status") == "ok":
                return
        except (OSError, urllib.error.URLError, json.JSONDecodeError):
            pass
        time.sleep(5)
    raise TimeoutError("server did not become ready")


def server_alias(label):
    return f"step-3.7-flash-rocmfpx-q3-qualityplus-{label}"


def kill_server_on_port():
    subprocess.run(
        [
            "distrobox", "enter", "vllm-gfx1151", "--", "bash", "-lc",
            f"pkill -TERM -f '[l]lama-server.*--port {PORT}' || true",
        ],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        try:
            request_json("/health", timeout=2)
        except (OSError, urllib.error.URLError, json.JSONDecodeError):
            return
        time.sleep(1)
    raise RuntimeError(f"server on port {PORT} did not stop")


def server_command(label, ctx_size, with_mtp):
    command = [
        str(SERVER),
        "-m", str(TARGET),
        "--alias", server_alias(label),
        "--host", "127.0.0.1",
        "--port", str(PORT),
        "--jinja",
        "-c", str(ctx_size),
        "--reasoning", "on",
        "--reasoning-format", "deepseek",
        "--reasoning-budget", "-1",
        "--no-context-shift",
        "-dev", "Vulkan0",
        "-ngl", "999",
        "-fa", "on",
        "-b", "8192",
        "-ub", "2048",
        "--parallel", "1",
        "--no-mmap",
        "--cache-ram", "0",
        "-ctk", "q8_0",
        "-ctv", "q8_0",
        "--chat-template-file", str(TEMPLATE),
        "--metrics",
        "--no-webui",
        "--no-cache-prompt",
    ]
    if with_mtp:
        command.extend(
            [
                "--spec-draft-model", str(DRAFT),
                "--spec-draft-device", "Vulkan0",
                "--spec-type", "draft-mtp",
                "--spec-draft-ngl", "all",
                "--spec-draft-type-k", "q8_0",
                "--spec-draft-type-v", "q8_0",
                "--spec-draft-n-max", "2",
                "--spec-draft-n-min", "0",
                "--spec-draft-p-min", "0.75",
                "--spec-draft-p-split", "0.10",
            ]
        )
    return command


def start_server(label, ctx_size, with_mtp):
    kill_server_on_port()
    command = server_command(label, ctx_size, with_mtp)
    (ROOT / f"{label}.command.txt").write_text(
        shlex.join(command) + "\n", encoding="utf-8"
    )
    wrapped = [
        "distrobox", "enter", "vllm-gfx1151", "--", "bash", "-lc",
        "exec " + shlex.join(command),
    ]
    log_handle = (ROOT / f"{label}.server.log").open("w", encoding="utf-8")
    process = subprocess.Popen(
        wrapped,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        wait_for_server(process)
        models, _ = request_json("/v1/models")
        observed_id = models["data"][0]["id"]
        if observed_id != server_alias(label):
            raise RuntimeError(
                f"stale server detected: expected {server_alias(label)!r}, "
                f"observed {observed_id!r}"
            )
        (ROOT / f"{label}.models.json").write_text(
            json.dumps(models, indent=2), encoding="utf-8"
        )
        return process, log_handle
    except Exception:
        kill_server_on_port()
        process.terminate()
        try:
            process.wait(timeout=30)
        except subprocess.TimeoutExpired:
            process.kill()
        log_handle.close()
        raise


def stop_server(process, log_handle):
    kill_server_on_port()
    try:
        process.wait(timeout=60)
    except subprocess.TimeoutExpired:
        process.terminate()
        try:
            process.wait(timeout=30)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=30)
    log_handle.close()
    time.sleep(10)


def prompt_for_tokens(target_tokens):
    prefix = (
        "Study the following synthetic service log. Preserve every detail, then "
        "finish with a concise operational summary.\n\n"
    )
    unit = " event=healthy backend=Vulkan0 route=step37 status=ok"
    repeats = max(1, target_tokens)
    for _ in range(8):
        prompt = prefix + unit * repeats
        tokenized, _ = request_json("/tokenize", {"content": prompt})
        observed = len(tokenized["tokens"])
        if abs(observed - target_tokens) <= max(8, target_tokens // 100):
            return prompt, observed
        repeats = max(1, round(repeats * target_tokens / observed))
    return prompt, observed


def completion_row(label, prompt, repeat, with_mtp, n_predict=128):
    payload = {
        "prompt": prompt,
        "n_predict": n_predict,
        "temperature": 0,
        "top_p": 1.0,
        "min_p": 0.0,
        "repeat_penalty": 1.0,
        "ignore_eos": True,
        "cache_prompt": False,
    }
    if with_mtp:
        payload.update(
            {
                "speculative.n_max": 2,
                "speculative.n_min": 0,
                "speculative.p_min": 0.75,
            }
        )
    stem = f"{label}-r{repeat}"
    (ROOT / f"{stem}.request.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    response, wall_seconds = request_json("/completion", payload, timeout=1800)
    (ROOT / f"{stem}.response.json").write_text(
        json.dumps(response, indent=2), encoding="utf-8"
    )
    timings = response["timings"]
    draft_n = timings.get("draft_n", 0)
    accepted = timings.get("draft_n_accepted", 0)
    return {
        "profile": label,
        "repeat": repeat,
        "prompt_tokens": timings["prompt_n"],
        "generated_tokens": timings["predicted_n"],
        "prompt_tps": timings["prompt_per_second"],
        "decode_tps": timings["predicted_per_second"],
        "draft_generated": draft_n,
        "draft_accepted": accepted,
        "draft_acceptance": accepted / draft_n if draft_n else None,
        "wall_seconds": wall_seconds,
    }


def write_summary(rows):
    summaries = []
    for profile in sorted({row["profile"] for row in rows}):
        selected = [row for row in rows if row["profile"] == profile]
        acceptance = [
            row["draft_acceptance"]
            for row in selected
            if row["draft_acceptance"] is not None
        ]
        summaries.append(
            {
                "profile": profile,
                "prompt_tokens": selected[0]["prompt_tokens"],
                "repeats": len(selected),
                "decode_tps_mean": statistics.mean(
                    row["decode_tps"] for row in selected
                ),
                "decode_tps_min": min(row["decode_tps"] for row in selected),
                "decode_tps_max": max(row["decode_tps"] for row in selected),
                "prompt_tps_mean": statistics.mean(
                    row["prompt_tps"] for row in selected
                ),
                "draft_acceptance_mean": (
                    statistics.mean(acceptance) if acceptance else None
                ),
            }
        )
    (ROOT / "summary.json").write_text(
        json.dumps(summaries, indent=2), encoding="utf-8"
    )


def main():
    for required in (TARGET, DRAFT, TEMPLATE, SERVER):
        if not required.exists():
            raise FileNotFoundError(required)

    rows = []
    baseline, baseline_log = start_server("baseline-64k", 65536, False)
    try:
        prompt4k, _ = prompt_for_tokens(4096)
        for repeat in range(1, 4):
            rows.append(completion_row("baseline-4k", prompt4k, repeat, False))
    finally:
        stop_server(baseline, baseline_log)

    mtp, mtp_log = start_server("mtp-64k", 65536, True)
    try:
        prompt4k, tokens4k = prompt_for_tokens(4096)
        prompt16k, tokens16k = prompt_for_tokens(16384)
        (ROOT / "prompt-token-targets.json").write_text(
            json.dumps(
                {"4k_observed": tokens4k, "16k_observed": tokens16k}, indent=2
            ),
            encoding="utf-8",
        )
        for repeat in range(1, 4):
            rows.append(completion_row("mtp-4k", prompt4k, repeat, True))
            rows.append(completion_row("mtp-16k", prompt16k, repeat, True))

        prompt48k, tokens48k = prompt_for_tokens(49152)
        (ROOT / "prompt-token-targets.json").write_text(
            json.dumps(
                {
                    "4k_observed": tokens4k,
                    "16k_observed": tokens16k,
                    "48k_observed": tokens48k,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        rows.append(completion_row("mtp-48k", prompt48k, 1, True, n_predict=64))

        tool_payload = {
            "model": server_alias("mtp-64k"),
            "messages": [
                {
                    "role": "user",
                    "content": "Call the terminal tool with the exact command: printf step37-ok",
                }
            ],
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "terminal",
                        "description": "Run one shell command.",
                        "parameters": {
                            "type": "object",
                            "properties": {"command": {"type": "string"}},
                            "required": ["command"],
                        },
                    },
                }
            ],
            "tool_choice": "required",
            "temperature": 0,
            "max_tokens": 256,
        }
        (ROOT / "tool-smoke.request.json").write_text(
            json.dumps(tool_payload, indent=2), encoding="utf-8"
        )
        tool_response, _ = request_json(
            "/v1/chat/completions", tool_payload, timeout=1800
        )
        (ROOT / "tool-smoke.response.json").write_text(
            json.dumps(tool_response, indent=2), encoding="utf-8"
        )
    finally:
        stop_server(mtp, mtp_log)

    write_summary(rows)
    (ROOT / "rows.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

    allocation, allocation_log = start_server("mtp-256k-allocation", 262144, True)
    try:
        models, _ = request_json("/v1/models")
        (ROOT / "mtp-256k-allocation-proof.json").write_text(
            json.dumps(models, indent=2), encoding="utf-8"
        )
    finally:
        stop_server(allocation, allocation_log)


if __name__ == "__main__":
    main()
