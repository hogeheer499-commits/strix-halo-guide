#!/usr/bin/env bash
set -euo pipefail

BIN=${BIN:-/home/hoge-heer/benchmark-tools/llama-b10034/llama-b10034/llama-batched-bench}
OUT_DIR=${OUT_DIR:-$(cd "$(dirname "$0")" && pwd)}
QWEN30=${QWEN30:-/home/hoge-heer/models/Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf}
QWEN80=${QWEN80:-/home/hoge-heer/models/Qwen3-Next-80B-A3B-Instruct-UD-Q4_K_XL.gguf}

hwmon=$(find /sys/class/drm/card*/device/hwmon -mindepth 1 -maxdepth 1 -type l -o -type d 2>/dev/null | while read -r path; do
    [[ -e "$path/temp1_input" && -e "$path/power1_average" ]] && printf '%s\n' "$path"
done | head -n 1)
busy=/sys/class/drm/card1/device/gpu_busy_percent

if [[ -z "$hwmon" ]]; then
    echo "could not locate AMD hwmon telemetry" >&2
    exit 2
fi

mkdir -p "$OUT_DIR"

run_one() {
    local label=$1
    local model=$2
    local telemetry="$OUT_DIR/${label}.telemetry.csv"
    local stdout="$OUT_DIR/${label}.jsonl"
    local stderr="$OUT_DIR/${label}.stderr.txt"

    for _ in $(seq 1 240); do
        temp=$(cat "$hwmon/temp1_input")
        (( temp < 50000 )) && break
        sleep 2
    done

    printf 'unix_s,temp_edge_mC,ppt_uW,sclk_Hz,gpu_busy_pct\n' > "$telemetry"

    LD_LIBRARY_PATH="$(dirname "$BIN")" \
        "$BIN" \
        -m "$model" \
        -c 65536 -ngl 999 -fa on \
        -ctk q4_0 -ctv q4_0 --no-mmap \
        -npp 512 -ntg 128 -npl 8,9 \
        --output-format jsonl \
        > "$stdout" 2> "$stderr" &
    bench_pid=$!

    while kill -0 "$bench_pid" 2>/dev/null; do
        temp=$(cat "$hwmon/temp1_input")
        power=$(cat "$hwmon/power1_average")
        sclk=$(cat "$hwmon/freq1_input")
        util=$(cat "$busy" 2>/dev/null || printf 'n/a')
        printf '%s,%s,%s,%s,%s\n' "$(date +%s)" "$temp" "$power" "$sclk" "$util" >> "$telemetry"
        if (( temp >= 95000 )); then
            printf 'thermal abort at %s mC\n' "$temp" >> "$stderr"
            kill -TERM "$bench_pid" 2>/dev/null || true
            wait "$bench_pid" || true
            return 95
        fi
        sleep 1
    done

    wait "$bench_pid"
}

for repeat in 1 2 3; do
    run_one "qwen30-stock-r${repeat}" "$QWEN30"
done

for repeat in 1 2 3; do
    run_one "qwen80-stock-r${repeat}" "$QWEN80"
done
