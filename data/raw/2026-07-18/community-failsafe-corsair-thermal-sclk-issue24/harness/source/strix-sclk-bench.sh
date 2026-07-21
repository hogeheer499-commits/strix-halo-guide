#!/usr/bin/env bash
# Sweep Strix Halo SCLK targets with raw llama-bench and telemetry artifacts.
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./strix-bench-lib.sh
source "$SCRIPT_DIR/strix-bench-lib.sh"

GPU_PCI="${GPU_PCI:-}"
CAPS="${CAPS:-2200 2400 2500 2600}"
read -r -a CAP_LIST <<< "$CAPS"
SCLK_FLOOR="${SCLK_FLOOR:-600}"
STOCK_EXPECTED_MIN_MHZ="${STOCK_EXPECTED_MIN_MHZ:-2800}"
MAX_SAFE_TEMP="${MAX_SAFE_TEMP:-98}"
SAMPLE_INT="${SAMPLE_INT:-1}"
SETTLE_SECS="${SETTLE_SECS:-20}"
COOLDOWN_DELTA_C="${COOLDOWN_DELTA_C:-5}"
COOLDOWN_TIMEOUT="${COOLDOWN_TIMEOUT:-600}"
TIMER_UNIT="${TIMER_UNIT:-strix-sclk-cap.timer}"
CONTAINER_NAME="${STRIX_BENCH_CONTAINER_NAME:-strix-bench}"

LLAMA_BENCH="${LLAMA_BENCH:-$HOME/bin/llama-bench-box}"
MODEL="${MODEL:-/data/models/UD-IQ2_M/MiMo-V2.5-UD-IQ2_M-00001-of-00003.gguf}"
PP="${PP:-512}"
TG="${TG:-128}"
NGL="${NGL:-99}"
REPETITIONS="${REPETITIONS:-10}"
BACKGROUND_CONDITION="${BACKGROUND_CONDITION:-unspecified}"
EXTRA_ARGS="${EXTRA_ARGS:--fa on -mmp 0 -ctk q8_0 -ctv q8_0 -b 4096 -ub 256}"
read -r -a EXTRA_ARGV <<< "$EXTRA_ARGS"

CAMPAIGN_ID="${CAMPAIGN_ID:-strix-halo-thermal}"
NODE_LABEL="${NODE_LABEL:-node-unknown}"
RUN_ID="${RUN_ID:-$(date -u +%Y%m%dT%H%M%SZ)}"
OUT_DIR="${OUT_DIR:-$HOME/strix-halo-evidence/$CAMPAIGN_ID/$NODE_LABEL/$RUN_ID/sweep}"
METADATA="$OUT_DIR/metadata.txt"
SUMMARY_CSV="$OUT_DIR/summary.csv"

MONITOR_PID=""
BENCH_PID=""
STRIX_STATE_CAPTURED=0
TIMER_WAS_ACTIVE=0
BASELINE_TEMP_MILLIC=0

# Invoked through the EXIT trap.
# shellcheck disable=SC2329
cleanup() {
  local rc=$?
  trap - EXIT INT TERM
  [[ -z "$MONITOR_PID" ]] || kill "$MONITOR_PID" 2>/dev/null || true
  [[ -z "$BENCH_PID" ]] || kill "$BENCH_PID" 2>/dev/null || true
  strix_reap_container
  if ! strix_restore_initial_state; then
    [[ "$rc" == "0" ]] && rc=1
  fi
  exit "$rc"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

monitor() {
  local bench_pid="$1" telemetry="$2" abort_flag="$3"
  local start now temp_millic power_microw sclk od_max mode
  start="$(date +%s)"
  printf '# elapsed_s\tutc\tedge_mC\tpower_uW\tsclk_MHz\tod_max_MHz\tperf_level\n' > "$telemetry"
  while kill -0 "$bench_pid" 2>/dev/null; do
    now="$(date +%s)"
    temp_millic="$(cat "$TEMP_FILE" 2>/dev/null || printf '0')"
    power_microw="$(cat "$POWER_FILE" 2>/dev/null || printf '0')"
    sclk="$(strix_current_sclk)"
    od_max="$(strix_read_od_max)"
    mode="$(cat "$PERF_FILE" 2>/dev/null || printf 'unknown')"
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
      "$(( now - start ))" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$temp_millic" "$power_microw" \
      "${sclk:-0}" "${od_max:-0}" "$mode" >> "$telemetry"
    if (( temp_millic >= MAX_SAFE_TEMP * 1000 )); then
      printf 'edge reached %s C\n' "$MAX_SAFE_TEMP" > "$abort_flag"
      kill -TERM "$bench_pid" 2>/dev/null || true
      break
    fi
    sleep "$SAMPLE_INT"
  done
}

cooldown() {
  local target_millic start current
  target_millic=$(( BASELINE_TEMP_MILLIC + COOLDOWN_DELTA_C * 1000 ))
  start="$(date +%s)"
  while :; do
    current="$(cat "$TEMP_FILE" 2>/dev/null || printf '0')"
    if (( current <= target_millic )); then
      return 0
    fi
    if (( $(date +%s) - start >= COOLDOWN_TIMEOUT )); then
      echo "WARNING: cooldown timed out at $(( current / 1000 )) C; continuing after recorded timeout" >&2
      return 0
    fi
    printf '  cooling: edge=%d C, target<=%d C\r' "$(( current / 1000 ))" "$(( target_millic / 1000 ))"
    sleep 10
  done
}

(( ${#CAP_LIST[@]} > 0 )) || strix_die "CAPS must contain at least one target"
for cap in "${CAP_LIST[@]}"; do
  [[ "$cap" == "stock" || "$cap" =~ ^[0-9]+$ ]] \
    || strix_die "invalid CAPS target: $cap"
done
[[ "$SAMPLE_INT" =~ ^[0-9]+$ && "$SAMPLE_INT" -gt 0 ]] || strix_die "SAMPLE_INT must be a positive integer"
[[ "$SETTLE_SECS" =~ ^[0-9]+$ ]] || strix_die "SETTLE_SECS must be a non-negative integer"
[[ "$REPETITIONS" =~ ^[0-9]+$ && "$REPETITIONS" -gt 0 ]] || strix_die "REPETITIONS must be a positive integer"
[[ "$MAX_SAFE_TEMP" =~ ^[0-9]+$ && "$MAX_SAFE_TEMP" -ge 50 && "$MAX_SAFE_TEMP" -le 100 ]] \
  || strix_die "MAX_SAFE_TEMP must be an integer from 50 through 100 C"
[[ -f "$MODEL" ]] || strix_die "model not found: $MODEL"
[[ -x "$LLAMA_BENCH" ]] || strix_die "llama-bench wrapper is not executable: $LLAMA_BENCH"
strix_check_control

strix_find_gpu
strix_find_hwmon
strix_assert_gpu_idle
strix_capture_initial_state
BASELINE_TEMP_MILLIC="$(cat "$TEMP_FILE")"

if [[ -e "$OUT_DIR" ]]; then
  strix_die "output directory already exists: $OUT_DIR"
fi
mkdir -p "$OUT_DIR"

NODE_LABEL="$NODE_LABEL" CAMPAIGN_ID="$CAMPAIGN_ID" MODEL="$MODEL" HASH_MODE=none \
  BACKGROUND_CONDITION="$BACKGROUND_CONDITION" \
  "$SCRIPT_DIR/strix-collect-metadata.sh" "$METADATA"

cat > "$OUT_DIR/run-config.txt" <<EOF
run_id=$RUN_ID
node_label=$NODE_LABEL
caps=$CAPS
max_safe_temp_c=$MAX_SAFE_TEMP
sample_interval_s=$SAMPLE_INT
settle_seconds=$SETTLE_SECS
cooldown_delta_c=$COOLDOWN_DELTA_C
background_condition=$BACKGROUND_CONDITION
model=$(basename "$MODEL")
pp=$PP
tg=$TG
repetitions=$REPETITIONS
ngl=$NGL
extra_args=$EXTRA_ARGS
EOF

printf 'target,pp_avg_ts,pp_stddev_ts,tg_avg_ts,tg_stddev_ts,max_edge_c,avg_power_w,max_power_w,status\n' \
  > "$SUMMARY_CSV"

strix_pause_timer
echo "Sweep node=$NODE_LABEL GPU=$GPU_PCI targets=${CAP_LIST[*]} artifacts=$OUT_DIR"

overall_rc=0
for cap in "${CAP_LIST[@]}"; do
  label="${cap}MHz"
  [[ "$cap" == "stock" ]] && label="stock"
  cap_dir="$OUT_DIR/$label"
  mkdir -p "$cap_dir"
  raw_json="$cap_dir/llama-bench.json"
  stderr_log="$cap_dir/llama-bench.stderr.log"
  telemetry="$cap_dir/telemetry.tsv"
  abort_flag="$cap_dir/thermal-abort.flag"

  cooldown
  if [[ "$cap" == "stock" ]]; then
    strix_set_stock
  else
    strix_set_cap "$cap" "$SCLK_FLOOR"
  fi
  sleep "$SETTLE_SECS"

  echo "Running target=$label repetitions=$REPETITIONS"
  strix_reap_container
  set +e
  "$LLAMA_BENCH" -m "$MODEL" -p "$PP" -n "$TG" -r "$REPETITIONS" -ngl "$NGL" \
    "${EXTRA_ARGV[@]}" -o json > "$raw_json" 2> "$stderr_log" &
  BENCH_PID=$!
  set -e
  monitor "$BENCH_PID" "$telemetry" "$abort_flag" &
  MONITOR_PID=$!

  bench_rc=0
  wait "$BENCH_PID" || bench_rc=$?
  BENCH_PID=""
  kill "$MONITOR_PID" 2>/dev/null || true
  wait "$MONITOR_PID" 2>/dev/null || true
  MONITOR_PID=""
  strix_reap_container

  status="ok"
  [[ "$bench_rc" == "0" ]] || status="benchmark-exit-$bench_rc"
  [[ ! -e "$abort_flag" ]] || status="thermal-abort"

  python3 - "$label" "$raw_json" "$telemetry" "$status" <<'PY' >> "$SUMMARY_CSV"
import csv
import json
import statistics
import sys

target, result_path, telemetry_path, status = sys.argv[1:]
pp_avg = pp_sd = tg_avg = tg_sd = ""
try:
    with open(result_path, encoding="utf-8") as handle:
        results = json.load(handle)
    for row in results:
        if int(row.get("n_gen", 0) or 0) > 0:
            tg_avg = row.get("avg_ts", "")
            tg_sd = row.get("stddev_ts", "")
        elif int(row.get("n_prompt", 0) or 0) > 0:
            pp_avg = row.get("avg_ts", "")
            pp_sd = row.get("stddev_ts", "")
except (OSError, ValueError, TypeError):
    if status == "ok":
        status = "invalid-json"

temps = []
powers = []
try:
    with open(telemetry_path, encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            fields = line.rstrip().split("\t")
            temps.append(int(fields[2]) / 1000)
            powers.append(int(fields[3]) / 1_000_000)
except (OSError, ValueError, IndexError):
    pass

writer = csv.writer(sys.stdout, lineterminator="\n")
writer.writerow([
    target, pp_avg, pp_sd, tg_avg, tg_sd,
    f"{max(temps):.3f}" if temps else "",
    f"{statistics.fmean(powers):.3f}" if powers else "",
    f"{max(powers):.3f}" if powers else "",
    status,
])
PY

  sha256sum "$raw_json" "$stderr_log" "$telemetry" > "$cap_dir/SHA256SUMS"
  if [[ "$status" != "ok" ]]; then
    overall_rc=1
    echo "Target $label ended with status=$status; stopping the sweep." >&2
    break
  fi
done

sha256sum "$METADATA" "$SUMMARY_CSV" "$OUT_DIR/run-config.txt" > "$OUT_DIR/SHA256SUMS"
exit "$overall_rc"
