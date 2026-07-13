#!/usr/bin/env bash
set -u

repo=/home/hoge-heer/strix-halo-guide
runner=$repo/local-scratch/run_density_bench.sh
out=/home/hoge-heer/benchmark-tools/density-results-20260713
vk=/home/hoge-heer/benchmark-tools/llama-b9979-density-build/bin/llama-batched-bench
rocm=/home/hoge-heer/strix-halo-bench-tools/lemonade-llamacpp-rocm-b1259-gfx1151/extracted/llama-batched-bench
model30=/home/hoge-heer/models/Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf
model80=/home/hoge-heer/models/Qwen3-Next-80B-A3B-Instruct-UD-Q4_K_XL.gguf
dpm=/sys/class/drm/card1/device/power_dpm_force_performance_level
temp_file=/sys/class/drm/card1/device/hwmon/hwmon6/temp1_input

mkdir -p "$out"
trap 'echo auto > "$dpm"' EXIT INT TERM

cool_run() {
    local label=$1
    local group=$2
    local model=$3
    shift 3

    echo auto > "$dpm"
    for _ in $(seq 1 180); do
        temp=$(cat "$temp_file")
        (( temp < 50000 )) && break
        sleep 2
    done
    echo high > "$dpm"
    sleep 2

    echo "[$(date -Is)] start $label at $(cat "$temp_file") mC" | tee -a "$out/campaign.log"
    if runuser -u hoge-heer -- env HOME=/home/hoge-heer "$runner" "$label" "$out/$group" "$model" "$@"; then
        echo "[$(date -Is)] pass $label" | tee -a "$out/campaign.log"
    else
        echo "[$(date -Is)] fail $label status=$?" | tee -a "$out/campaign.log"
    fi
    echo auto > "$dpm"
}

vk_run() {
    local label=$1 group=$2 model=$3 mode=$4 npl=$5
    local -a env_args=()
    case "$mode" in
        stock) ;;
        gate) env_args=(env GGML_VK_DENSITY_GATE=1) ;;
        dense16) env_args=(env GGML_VK_DENSITY_GATE=1 GGML_VK_MMV_MAX_COLS=16) ;;
        *) echo "unknown mode: $mode" >&2; return 2 ;;
    esac
    cool_run "$label" "$group" "$model" "${env_args[@]}" "$vk" \
        -c 65536 -ngl 999 -fa on -ctk q4_0 -ctv q4_0 --no-mmap \
        -npp 512 -ntg 128 -npl "$npl" --output-format jsonl
}

rocm_run() {
    local label=$1 group=$2 model=$3 npl=$4
    cool_run "$label" "$group" "$model" "$rocm" \
        -c 65536 -ngl 999 -fa 1 -ctk q4_0 -ctv q4_0 --no-mmap \
        -npp 512 -ntg 128 -npl "$npl"
}

phase=${1:-discovery}

if [[ $phase == discovery ]]; then
    # 30B stock already completed as one clean b9979 sweep. Complete the two
    # experimental modes in thermally isolated blocks.
    for mode in gate dense16; do
        vk_run "30b-${mode}-low" discovery "$model30" "$mode" 1,2,4,8,9,12,16
        vk_run "30b-${mode}-mid" discovery "$model30" "$mode" 24,32
        vk_run "30b-${mode}-48" discovery "$model30" "$mode" 48
        vk_run "30b-${mode}-64" discovery "$model30" "$mode" 64
    done

    for mode in stock gate dense16; do
        vk_run "80b-${mode}-low" discovery "$model80" "$mode" 1,2,4,8,9,12,16
        vk_run "80b-${mode}-mid" discovery "$model80" "$mode" 24,32
        vk_run "80b-${mode}-48" discovery "$model80" "$mode" 48
        vk_run "80b-${mode}-64" discovery "$model80" "$mode" 64
    done

    rocm_run 30b-rocm-low discovery "$model30" 1,2,4,8,9,12,16
    rocm_run 30b-rocm-mid discovery "$model30" 24,32
    rocm_run 30b-rocm-48 discovery "$model30" 48
    rocm_run 30b-rocm-64 discovery "$model30" 64
    rocm_run 80b-rocm-low discovery "$model80" 1,2,4,8,9,12,16
    rocm_run 80b-rocm-mid discovery "$model80" 24,32
    rocm_run 80b-rocm-48 discovery "$model80" 48
    rocm_run 80b-rocm-64 discovery "$model80" 64
fi

if [[ $phase == repeats30 ]]; then
    for rep in 1 2 3 4 5; do
        for mode in stock gate dense16; do
            vk_run "30b-${mode}-critical-r${rep}" repeats30 "$model30" "$mode" 8,9,12,16
        done
    done
    for rep in 1 2 3; do
        rocm_run "30b-rocm-critical-r${rep}" repeats30 "$model30" 8,9,12,16
    done
fi

if [[ $phase == repeats80 ]]; then
    for rep in 1 2 3; do
        for mode in stock gate dense16; do
            vk_run "80b-${mode}-critical-r${rep}" repeats80 "$model80" "$mode" 8,9,12,16
        done
        rocm_run "80b-rocm-critical-r${rep}" repeats80 "$model80" 8,9,12,16
    done
fi

