#!/usr/bin/env python3
import base64
import csv
import json
import os
import pathlib
import signal
import statistics
import subprocess
import threading
import time
import urllib.error
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parent
PORT = 11435
BASE_URL = f"http://127.0.0.1:{PORT}"
MODEL = "qwen3.6:35b-a3b"
VISION_MODEL = "qwen2.5vl:7b"
VISION_IMAGE = pathlib.Path(__file__).resolve().parents[4] / "docs/assets/social-preview.png"
VERSIONS = {
    "0.31.1": pathlib.Path("/home/hoge-heer/benchmark-tools/ollama-0.31.1/bin/ollama"),
    "0.31.2": pathlib.Path("/usr/local/bin/ollama"),
    "0.32.0": pathlib.Path("/home/hoge-heer/benchmark-tools/ollama-0.32.0/bin/ollama"),
}
PROMPT = (
    "Write a concise explanation of why reproducible local AI benchmarks "
    "matter for buyers."
)


def api(path, payload=None, timeout=900):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(BASE_URL + path, data=data, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def locate_telemetry():
    for hwmon in pathlib.Path("/sys/class/drm").glob("card*/device/hwmon/hwmon*"):
        if (hwmon / "temp1_input").exists() and (hwmon / "power1_average").exists():
            busy = hwmon.parents[1] / "gpu_busy_percent"
            return hwmon, busy
    return None, None


def read_number(path):
    try:
        return path.read_text(encoding="ascii").strip()
    except OSError:
        return "n/a"


def wait_for_cooldown(hwmon, threshold=50000, timeout=600):
    if hwmon is None:
        return
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        value = int(read_number(hwmon / "temp1_input"))
        if value < threshold:
            return
        time.sleep(2)
    raise RuntimeError("cooldown timeout")


def telemetry_loop(path, stop_event, hwmon, busy):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["unix_s", "temp_edge_mC", "ppt_uW", "sclk_Hz", "gpu_busy_pct"])
        while not stop_event.is_set():
            if hwmon is not None:
                writer.writerow(
                    [
                        time.time(),
                        read_number(hwmon / "temp1_input"),
                        read_number(hwmon / "power1_average"),
                        read_number(hwmon / "freq1_input"),
                        read_number(busy),
                    ]
                )
                handle.flush()
            stop_event.wait(1)


def start_server(label, binary, hwmon, busy):
    wait_for_cooldown(hwmon)
    env = os.environ.copy()
    env.update(
        {
            "OLLAMA_HOST": f"127.0.0.1:{PORT}",
            "OLLAMA_MODELS": "/usr/share/ollama/.ollama/models",
            "OLLAMA_VULKAN": "1",
            "OLLAMA_IGPU_ENABLE": "1",
            "HIP_VISIBLE_DEVICES": "-1",
            "OLLAMA_FLASH_ATTENTION": "1",
            "OLLAMA_CONTEXT_LENGTH": "65536",
            "AMD_VULKAN_ICD": "RADV",
            "VK_ICD_FILENAMES": "/usr/share/vulkan/icd.d/radeon_icd.json",
            "OLLAMA_NUM_BATCH": "512",
            "OLLAMA_NUM_PARALLEL": "1",
            "OLLAMA_MAX_LOADED_MODELS": "2",
        }
    )
    log_handle = (ROOT / f"{label}-server.log").open("w", encoding="utf-8")
    process = subprocess.Popen(
        [str(binary), "serve"],
        env=env,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        start_new_session=True,
        text=True,
    )
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        if process.poll() is not None:
            log_handle.close()
            raise RuntimeError(f"{label} server exited with {process.returncode}")
        try:
            version = api("/api/version", timeout=2)
            break
        except (OSError, urllib.error.URLError):
            time.sleep(0.5)
    else:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=10)
        log_handle.close()
        raise RuntimeError(f"{label} server startup timeout")

    stop_event = threading.Event()
    thread = threading.Thread(
        target=telemetry_loop,
        args=(ROOT / f"{label}-telemetry.csv", stop_event, hwmon, busy),
        daemon=True,
    )
    thread.start()
    return process, log_handle, version, stop_event, thread


def stop_server(process, log_handle, stop_event, thread):
    stop_event.set()
    thread.join(timeout=5)
    if process.poll() is None:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=30)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=10)
    log_handle.close()
    time.sleep(3)


def run_speed(label):
    rows = []
    for repeat in range(1, 11):
        payload = {
            "model": MODEL,
            "prompt": PROMPT,
            "stream": False,
            "keep_alive": "15m",
            "options": {
                "num_predict": 128,
                "temperature": 0,
                "num_ctx": 2048,
            },
        }
        response = api("/api/generate", payload)
        (ROOT / f"{label}-qwen-r{repeat}.json").write_text(
            json.dumps(response, indent=2), encoding="utf-8"
        )
        row = {
            "version_label": label,
            "repeat": repeat,
            "phase": "cold" if repeat == 1 else "warm",
            "prompt_eval_count": response.get("prompt_eval_count", 0),
            "prompt_eval_duration_ns": response.get("prompt_eval_duration", 0),
            "prompt_tps": (
                response.get("prompt_eval_count", 0) * 1e9
                / response.get("prompt_eval_duration", 1)
            ),
            "eval_count": response.get("eval_count", 0),
            "eval_duration_ns": response.get("eval_duration", 0),
            "generation_tps": (
                response.get("eval_count", 0) * 1e9 / response.get("eval_duration", 1)
            ),
            "total_duration_ns": response.get("total_duration", 0),
            "load_duration_ns": response.get("load_duration", 0),
        }
        rows.append(row)
        print(json.dumps(row), flush=True)
        time.sleep(2)
    with (ROOT / f"{label}-qwen-api-r10.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def run_vision(label, suffix):
    image = base64.b64encode(VISION_IMAGE.read_bytes()).decode("ascii")
    payload = {
        "model": VISION_MODEL,
        "prompt": (
            "Read the main title and the largest benchmark number in this image. "
            "Answer in one sentence."
        ),
        "images": [image],
        "stream": False,
        "keep_alive": "5m",
        "options": {"temperature": 0, "num_predict": 64, "num_ctx": 2048},
    }
    response = api("/api/generate", payload)
    (ROOT / f"{label}-vision-{suffix}.json").write_text(
        json.dumps(response, indent=2), encoding="utf-8"
    )
    return response


def summarize(all_rows, versions):
    summary = []
    for label, rows in all_rows.items():
        warm = rows[1:]
        values = [row["generation_tps"] for row in warm]
        summary.append(
            {
                "requested_version": label,
                "reported_server_version": versions[label]["version"],
                "cold_generation_tps": rows[0]["generation_tps"],
                "warm_repeats": len(warm),
                "warm_generation_tps_mean": statistics.mean(values),
                "warm_generation_tps_min": min(values),
                "warm_generation_tps_max": max(values),
                "warm_generation_tps_sd": statistics.stdev(values),
                "warm_prompt_tps_mean": statistics.mean(row["prompt_tps"] for row in warm),
            }
        )
    (ROOT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({"summary": summary}, indent=2), flush=True)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    hwmon, busy = locate_telemetry()
    all_rows = {}
    versions = {}

    for label, binary in VERSIONS.items():
        process, log_handle, version, stop_event, thread = start_server(label, binary, hwmon, busy)
        try:
            versions[label] = version
            (ROOT / f"{label}-api-version.json").write_text(
                json.dumps(version, indent=2), encoding="utf-8"
            )
            all_rows[label] = run_speed(label)
            (ROOT / f"{label}-ps.json").write_text(
                json.dumps(api("/api/ps"), indent=2), encoding="utf-8"
            )
            if label == "0.32.0":
                run_vision(label, "before-restart")
        finally:
            stop_server(process, log_handle, stop_event, thread)

    label = "0.32.0"
    binary = VERSIONS[label]
    process, log_handle, version, stop_event, thread = start_server(
        f"{label}-restart", binary, hwmon, busy
    )
    try:
        restart_qwen = api(
            "/api/generate",
            {
                "model": MODEL,
                "prompt": "Reply with exactly: restart pass",
                "stream": False,
                "options": {"temperature": 0, "num_predict": 16, "num_ctx": 2048},
            },
        )
        (ROOT / f"{label}-qwen-after-restart.json").write_text(
            json.dumps(restart_qwen, indent=2), encoding="utf-8"
        )
        run_vision(label, "after-restart")
        (ROOT / f"{label}-ps-after-restart.json").write_text(
            json.dumps(api("/api/ps"), indent=2), encoding="utf-8"
        )
    finally:
        stop_server(process, log_handle, stop_event, thread)

    summarize(all_rows, versions)


if __name__ == "__main__":
    main()
