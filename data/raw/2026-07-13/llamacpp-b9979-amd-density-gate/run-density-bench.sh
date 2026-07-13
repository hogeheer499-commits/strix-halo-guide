#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 4 ]]; then
    echo "usage: $0 LABEL OUT_DIR MODEL COMMAND..." >&2
    exit 2
fi

label=$1
out_dir=$2
model=$3
shift 3

hwmon=/sys/class/drm/card1/device/hwmon/hwmon6
busy=/sys/class/drm/card1/device/gpu_busy_percent
mkdir -p "$out_dir"

# Start each run below 50 C so repeat order does not dominate the comparison.
for _ in $(seq 1 180); do
    temp=$(cat "$hwmon/temp1_input")
    (( temp < 50000 )) && break
    sleep 2
done

telemetry="$out_dir/${label}.telemetry.csv"
stdout="$out_dir/${label}.stdout.log"
stderr="$out_dir/${label}.stderr.log"
printf 'unix_s,temp_edge_mC,ppt_uW,sclk_Hz,gpu_busy_pct\n' > "$telemetry"

start=$(date +%s)
"$@" -m "$model" > "$stdout" 2> "$stderr" &
bench_pid=$!

(
    while kill -0 "$bench_pid" 2>/dev/null; do
        now=$(date +%s)
        temp=$(cat "$hwmon/temp1_input")
        power=$(cat "$hwmon/power1_average")
        sclk=$(cat "$hwmon/freq1_input")
        util=$(cat "$busy")
        printf '%s,%s,%s,%s,%s\n' "$now" "$temp" "$power" "$sclk" "$util" >> "$telemetry"
        if (( temp >= 95000 )); then
            printf 'thermal abort at %s mC\n' "$temp" >> "$stderr"
            kill -TERM "$bench_pid" 2>/dev/null || true
            exit 95
        fi
        sleep 1
    done
) &
monitor_pid=$!

set +e
wait "$bench_pid"
status=$?
wait "$monitor_pid"
monitor_status=$?
set -e

end=$(date +%s)
awk -F, -v label="$label" -v start="$start" -v end="$end" -v status="$status" -v monitor="$monitor_status" '
    NR == 2 { min_t=$2; max_t=$2; min_p=$3; max_p=$3; sum_t=0; sum_p=0; n=0 }
    NR > 1 {
        if ($2 < min_t) min_t=$2; if ($2 > max_t) max_t=$2;
        if ($3 < min_p) min_p=$3; if ($3 > max_p) max_p=$3;
        sum_t += $2; sum_p += $3; n++
    }
    END {
        printf "label,status,monitor_status,elapsed_s,samples,min_temp_mC,max_temp_mC,avg_temp_mC,min_ppt_uW,max_ppt_uW,avg_ppt_uW\n";
        printf "%s,%d,%d,%d,%d,%d,%d,%.0f,%d,%d,%.0f\n", label,status,monitor,end-start,n,min_t,max_t,sum_t/n,min_p,max_p,sum_p/n
    }
' "$telemetry" > "$out_dir/${label}.summary.csv"

if (( status != 0 || monitor_status == 95 )); then
    exit "${status:-95}"
fi
