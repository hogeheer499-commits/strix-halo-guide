#!/usr/bin/env python3
"""Compare Qwen3-Next baseline and MTP policies on llama.cpp b10330 Vulkan."""

import csv
import hashlib
import json
import pathlib
import shlex
import statistics
import subprocess
import time
import urllib.error
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parent
SERVER = pathlib.Path(
    "/home/hoge-heer/local-scratch/llama.cpp-b10330/build-vulkan/bin/llama-server"
)
MODEL = pathlib.Path(
    "/home/hoge-heer/models/Qwen3-Next-80B-A3B-Instruct-UD-Q4_K_XL.gguf"
)
DRAFT = pathlib.Path(
    "/home/hoge-heer/local-scratch/models/qwen3-next-mtp/"
    "Qwen3-Next-80B-A3B-Instruct-MTP-ONLY-Q4_K_M.gguf"
)
PORT = 18103
BASE_URL = f"http://127.0.0.1:{PORT}"
PROFILES = (
    {"name": "baseline", "mtp": False},
    {"name": "mtp-n2-p060", "mtp": True, "n_max": 2, "p_min": 0.60},
    {"name": "mtp-n4-p000", "mtp": True, "n_max": 4, "p_min": 0.00},
)


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


def wait_for_server(process, timeout=900):
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
        time.sleep(2)
    raise TimeoutError("server did not become ready")


def stop_server(process, log_handle):
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=60)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=30)
    log_handle.close()
    time.sleep(5)


def server_command(profile):
    command = [
        str(SERVER),
        "-m", str(MODEL),
        "--alias", profile["name"],
        "--host", "127.0.0.1",
        "--port", str(PORT),
        "--no-ui",
        "--metrics",
        "--no-cache-prompt",
        "--parallel", "1",
        "-c", "8192",
        "-b", "2048",
        "-ub", "512",
        "-dev", "Vulkan0",
        "-ngl", "999",
    ]
    if profile["mtp"]:
        command.extend(
            [
                "--spec-draft-model", str(DRAFT),
                "--spec-draft-device", "Vulkan0",
                "--spec-draft-ngl", "999",
                "--spec-type", "draft-mtp",
                "--spec-draft-n-max", str(profile["n_max"]),
                "--spec-draft-p-min", str(profile["p_min"]),
            ]
        )
    return command


def start_server(profile):
    command = server_command(profile)
    (ROOT / f"{profile['name']}.command.txt").write_text(
        shlex.join(command) + "\n", encoding="utf-8"
    )
    log_handle = (ROOT / f"{profile['name']}.server.log").open(
        "w", encoding="utf-8"
    )
    process = subprocess.Popen(
        command,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        wait_for_server(process)
        models, _ = request_json("/v1/models")
        (ROOT / f"{profile['name']}.models.json").write_text(
            json.dumps(models, indent=2), encoding="utf-8"
        )
        return process, log_handle
    except Exception:
        stop_server(process, log_handle)
        raise


def prompt_for_tokens(target_tokens):
    prefix = (
        "Read this synthetic backend log, preserve all stated constraints, and "
        "finish with a concise five-item validation checklist.\n\n"
    )
    unit = " event=healthy backend=Vulkan0 model=qwen3next status=ok"
    repeats = max(1, target_tokens)
    observed = 0
    for _ in range(8):
        prompt = prefix + unit * repeats
        tokenized, _ = request_json("/tokenize", {"content": prompt})
        observed = len(tokenized["tokens"])
        if abs(observed - target_tokens) <= max(8, target_tokens // 100):
            return prompt, observed
        repeats = max(1, round(repeats * target_tokens / observed))
    return prompt, observed


def completion_row(profile, prompt_name, prompt, repeat):
    payload = {
        "prompt": prompt,
        "n_predict": 128,
        "temperature": 0,
        "top_p": 1.0,
        "min_p": 0.0,
        "repeat_penalty": 1.0,
        "ignore_eos": True,
        "cache_prompt": False,
        "seed": 42,
    }
    stem = f"{profile['name']}-{prompt_name}-r{repeat}"
    (ROOT / f"{stem}.request.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    response, wall_seconds = request_json("/completion", payload, timeout=1800)
    (ROOT / f"{stem}.response.json").write_text(
        json.dumps(response, indent=2), encoding="utf-8"
    )
    timings = response["timings"]
    content = response.get("content", "")
    draft_n = timings.get("draft_n", 0)
    accepted = timings.get("draft_n_accepted", 0)
    return {
        "profile": profile["name"],
        "prompt": prompt_name,
        "repeat": repeat,
        "prompt_tokens": timings["prompt_n"],
        "generated_tokens": timings["predicted_n"],
        "prompt_tps": timings["prompt_per_second"],
        "decode_tps": timings["predicted_per_second"],
        "draft_generated": draft_n,
        "draft_accepted": accepted,
        "draft_acceptance": accepted / draft_n if draft_n else "",
        "wall_seconds": wall_seconds,
        "content_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "content_preview": content.replace("\n", " ")[:160],
    }


def write_outputs(rows):
    fieldnames = list(rows[0])
    with (ROOT / "rows.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    summaries = []
    for profile in sorted({row["profile"] for row in rows}):
        for prompt in sorted({row["prompt"] for row in rows}):
            selected = [
                row for row in rows
                if row["profile"] == profile and row["prompt"] == prompt
            ]
            acceptance = [
                float(row["draft_acceptance"])
                for row in selected if row["draft_acceptance"] != ""
            ]
            summaries.append(
                {
                    "profile": profile,
                    "prompt": prompt,
                    "prompt_tokens": selected[0]["prompt_tokens"],
                    "repeats": len(selected),
                    "decode_tps_mean": statistics.mean(
                        float(row["decode_tps"]) for row in selected
                    ),
                    "decode_tps_min": min(
                        float(row["decode_tps"]) for row in selected
                    ),
                    "decode_tps_max": max(
                        float(row["decode_tps"]) for row in selected
                    ),
                    "prompt_tps_mean": statistics.mean(
                        float(row["prompt_tps"]) for row in selected
                    ),
                    "draft_acceptance_mean": (
                        statistics.mean(acceptance) if acceptance else None
                    ),
                    "unique_content_hashes": len(
                        {row["content_sha256"] for row in selected}
                    ),
                }
            )
    (ROOT / "summary.json").write_text(
        json.dumps(summaries, indent=2), encoding="utf-8"
    )


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    for required in (SERVER, MODEL, DRAFT):
        if not required.exists():
            raise FileNotFoundError(required)
    rows = []
    targets = {"short": 64, "3k": 3072}
    observed_targets = {}
    for profile in PROFILES:
        process, log_handle = start_server(profile)
        try:
            prompts = {}
            for name, target in targets.items():
                prompts[name], observed_targets[f"{profile['name']}-{name}"] = (
                    prompt_for_tokens(target)
                )
            for prompt_name, prompt in prompts.items():
                for repeat in range(1, 4):
                    rows.append(
                        completion_row(profile, prompt_name, prompt, repeat)
                    )
        finally:
            stop_server(process, log_handle)
    (ROOT / "prompt-token-targets.json").write_text(
        json.dumps(observed_targets, indent=2), encoding="utf-8"
    )
    write_outputs(rows)


if __name__ == "__main__":
    main()
