#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(cd "$ROOT/../../../.." && pwd)
IMAGE="docker.io/rocm/vllm@sha256:5b0389109bb2db9346d3f0f971c4c99eba7e5e72cfa57e9a2a9b4ac67477771d"
IMAGE_TAG="rocm7.14.0_rdna_ubuntu24.04_py3.14_pytorch_2.11.0_vllm_0.23.0"
MODEL_REPO="/home/hoge-heer/distrobox/vllm-gfx1151/.cache/huggingface/hub/models--Qwen--Qwen3-0.6B"
SNAPSHOT="c1899de289a04d12100db370d81485cdf75e47ca"
MODEL_HOST="$MODEL_REPO/snapshots/$SNAPSHOT"
MODEL_CONTAINER="/models/qwen/snapshots/$SNAPSHOT"
SERVED_MODEL="qwen3-0.6b-fp16"
PORT=18014
CONCURRENCY=(1 4 8 9 16)

require() {
    command -v "$1" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$1" >&2
        exit 1
    }
}

find_hwmon() {
    local path
    for path in /sys/class/drm/card*/device/hwmon/hwmon*; do
        [[ -e "$path/temp1_input" && -e "$path/power1_average" ]] && {
            printf '%s\n' "$path"
            return 0
        }
    done
    return 1
}

wait_for_health() {
    local name=$1
    local deadline=$((SECONDS + 300))
    while (( SECONDS < deadline )); do
        if curl -fsS "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
            return 0
        fi
        if ! podman container exists "$name" || [[ "$(podman inspect -f '{{.State.Running}}' "$name" 2>/dev/null || true)" != true ]]; then
            return 1
        fi
        sleep 2
    done
    return 1
}

sample_telemetry() {
    local output=$1
    local stop_file=$2
    local hwmon=$3
    local busy_file
    busy_file=$(realpath "$hwmon/../../gpu_busy_percent" 2>/dev/null || true)
    printf 'unix_s,temp_edge_mC,ppt_uW,sclk_Hz,gpu_busy_pct\n' > "$output"
    while [[ ! -e "$stop_file" ]]; do
        printf '%s,%s,%s,%s,%s\n' \
            "$(date +%s.%N)" \
            "$(cat "$hwmon/temp1_input" 2>/dev/null || printf 'n/a')" \
            "$(cat "$hwmon/power1_average" 2>/dev/null || printf 'n/a')" \
            "$(cat "$hwmon/freq1_input" 2>/dev/null || printf 'n/a')" \
            "$(cat "$busy_file" 2>/dev/null || printf 'n/a')" >> "$output"
        sleep 1
    done
}

stop_container() {
    local name=$1
    podman rm -f "$name" >/dev/null 2>&1 || true
}

run_mode() {
    local mode=$1
    local prefer=$2
    local name="rocm714-vllm-${mode}"
    local mode_dir="$ROOT/$mode"
    local stop_file="$mode_dir/telemetry.stop"
    local hwmon=$3
    local telemetry_pid=""

    mkdir -p "$mode_dir"
    rm -f "$stop_file"
    stop_container "$name"

    if [[ -n "$hwmon" ]]; then
        sample_telemetry "$mode_dir/telemetry.csv" "$stop_file" "$hwmon" &
        telemetry_pid=$!
    fi

    podman run -d --name "$name" \
        --network host \
        --ipc host \
        --device /dev/kfd \
        --device /dev/dri \
        --group-add keep-groups \
        --security-opt label=disable \
        -v "$MODEL_REPO:/models/qwen:ro" \
        -e HSA_OVERRIDE_GFX_VERSION=11.0.0 \
        -e TORCH_BLAS_PREFER_HIPBLASLT="$prefer" \
        --entrypoint /bin/bash \
        "$IMAGE" -lc \
        "python -m vllm.entrypoints.openai.api_server \
          --model '$MODEL_CONTAINER' \
          --served-model-name '$SERVED_MODEL' \
          --host 127.0.0.1 --port '$PORT' \
          --dtype float16 \
          --max-model-len 2048 \
          --max-num-seqs 32 \
          --gpu-memory-utilization 0.35 \
          --enforce-eager" > "$mode_dir/container-id.txt"

    if ! wait_for_health "$name"; then
        podman logs "$name" > "$mode_dir/server.log" 2>&1 || true
        touch "$stop_file"
        [[ -n "$telemetry_pid" ]] && wait "$telemetry_pid" || true
        podman inspect "$name" > "$mode_dir/container-inspect.json" 2>/dev/null || true
        stop_container "$name"
        printf '%s failed to reach health; see %s\n' "$mode" "$mode_dir/server.log" >&2
        return 1
    fi

    podman exec "$name" bash -lc \
        "python - <<'PY'
import json
import torch
import vllm
print(json.dumps({
    'torch': torch.__version__,
    'torch_hip': torch.version.hip,
    'vllm': vllm.__version__,
}, sort_keys=True))
PY" > "$mode_dir/container-versions.json"

    curl -fsS "http://127.0.0.1:$PORT/v1/models" > "$mode_dir/models.json"
    for np in "${CONCURRENCY[@]}"; do
        python3 "$REPO/scripts/benchmark_openai_server.py" \
            --url "http://127.0.0.1:$PORT" \
            --model "$SERVED_MODEL" \
            --np "$np" \
            --tokens 256 \
            --reps 3 \
            --timeout 900 \
            --detail "$mode_dir/np${np}-detail.csv" \
            --summary "$mode_dir/np${np}-summary.csv" \
            | tee "$mode_dir/np${np}-stdout.jsonl"
    done

    podman logs "$name" > "$mode_dir/server.log" 2>&1 || true
    podman inspect "$name" > "$mode_dir/container-inspect.json"
    touch "$stop_file"
    [[ -n "$telemetry_pid" ]] && wait "$telemetry_pid" || true
    stop_container "$name"
}

require podman
require curl
require python3
[[ -r /dev/kfd ]] || { printf '/dev/kfd is not readable\n' >&2; exit 1; }
[[ -d "$MODEL_HOST" ]] || { printf 'missing model snapshot: %s\n' "$MODEL_HOST" >&2; exit 1; }

mkdir -p "$ROOT"
{
    printf 'prepared_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'image=%s\n' "$IMAGE"
    printf 'image_tag_context=%s\n' "$IMAGE_TAG"
    printf 'model_snapshot=%s\n' "$MODEL_HOST"
    printf 'kernel=%s\n' "$(uname -r)"
    printf 'cmdline=%s\n' "$(cat /proc/cmdline)"
} > "$ROOT/run-context.txt"
find -L "$MODEL_HOST" -maxdepth 1 -type f -print0 \
    | sort -z \
    | xargs -0 sha256sum > "$ROOT/model-sha256.txt"

podman pull "$IMAGE" | tee "$ROOT/image-pull.log"
podman image inspect "$IMAGE" > "$ROOT/image-inspect.json"

hwmon=$(find_hwmon || true)
result=0
run_mode hipblaslt-off 0 "$hwmon" || result=1
run_mode hipblaslt-on 1 "$hwmon" || result=1

python3 - "$ROOT" <<'PY'
import csv
import json
import pathlib
import statistics
import sys

root = pathlib.Path(sys.argv[1])
rows = []
for mode in ("hipblaslt-off", "hipblaslt-on"):
    for path in sorted((root / mode).glob("np*-summary.csv")):
        with path.open(newline="", encoding="utf-8") as handle:
            data = list(csv.DictReader(handle))
        if not data:
            continue
        rows.append({
            "mode": mode,
            "np": int(data[0]["np"]),
            "repeats": len(data),
            "aggregate_tps_mean": statistics.fmean(float(row["aggregate_tps"]) for row in data),
            "aggregate_tps_stdev": statistics.stdev(float(row["aggregate_tps"]) for row in data) if len(data) > 1 else 0.0,
            "ttft_mean_s": statistics.fmean(float(row["mean_ttft_s"]) for row in data),
            "ttft_p95_mean_s": statistics.fmean(float(row["p95_ttft_s"]) for row in data),
            "itl_mean_s": statistics.fmean(float(row["mean_itl_s"]) for row in data),
            "errors": sum(int(row["errors"]) for row in data),
        })

if rows:
    with (root / "summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (root / "summary.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
PY

exit "$result"
