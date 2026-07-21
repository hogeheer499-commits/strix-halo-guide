#!/usr/bin/env bash
# Sustained Strix Halo thermal soak with raw telemetry and exact state restore.
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./strix-bench-lib.sh
source "$SCRIPT_DIR/strix-bench-lib.sh"

GPU_PCI="${GPU_PCI:-}"
CAP="${CAP:-2400}"                       # MHz, or "stock" for a separately approved control
SCLK_FLOOR="${SCLK_FLOOR:-600}"
STOCK_EXPECTED_MIN_MHZ="${STOCK_EXPECTED_MIN_MHZ:-2800}"
DURATION="${DURATION:-1800}"             # seconds under sustained compute, excluding model load
MAX_SAFE_TEMP="${MAX_SAFE_TEMP:-98}"     # hard thermal abort
SAMPLE_INT="${SAMPLE_INT:-2}"
PRINT_INT="${PRINT_INT:-30}"
LOAD_POWER_THRESHOLD_W="${LOAD_POWER_THRESHOLD_W:-40}"
LOAD_TIMEOUT="${LOAD_TIMEOUT:-600}"
BACKGROUND_CONDITION="${BACKGROUND_CONDITION:-unspecified}"
TIMER_UNIT="${TIMER_UNIT:-strix-sclk-cap.timer}"
CONTAINER_NAME="${STRIX_BENCH_CONTAINER_NAME:-strix-bench}"

LLAMA_BENCH="${LLAMA_BENCH:-$HOME/bin/llama-bench-box}"
MODEL="${MODEL:-/data/models/UD-IQ2_M/MiMo-V2.5-UD-IQ2_M-00001-of-00003.gguf}"
NGL="${NGL:-99}"
PP="${PP:-512}"
TG="${TG:-512}"
EXTRA_ARGS="${EXTRA_ARGS:--fa on -mmp 0 -ctk q8_0 -ctv q8_0 -b 4096 -ub 256}"
read -r -a EXTRA_ARGV <<< "$EXTRA_ARGS"

CAMPAIGN_ID="${CAMPAIGN_ID:-strix-halo-thermal}"
NODE_LABEL="${NODE_LABEL:-node-unknown}"
RUN_ID="${RUN_ID:-$(date -u +%Y%m%dT%H%M%SZ)}"
TARGET_LABEL="${CAP}MHz"
[[ "$CAP" == "stock" ]] && TARGET_LABEL="stock"
OUT_DIR="${OUT_DIR:-$HOME/strix-halo-evidence/$CAMPAIGN_ID/$NODE_LABEL/$RUN_ID/soak-$TARGET_LABEL}"
TELEMETRY="$OUT_DIR/telemetry.tsv"
BENCH_LOG="$OUT_DIR/llama-bench.log"
METADATA="$OUT_DIR/metadata.txt"
SUMMARY="$OUT_DIR/summary.txt"
ABORT_FLAG="$OUT_DIR/thermal-abort.flag"

BENCH_PID=""
SAMPLER_PID=""
STRIX_STATE_CAPTURED=0
TIMER_WAS_ACTIVE=0
EXIT_REASON="not-started"

# Invoked through the EXIT trap.
# shellcheck disable=SC2329
cleanup() {
  local rc=$?
  trap - EXIT INT TERM
  [[ -z "$SAMPLER_PID" ]] || kill "$SAMPLER_PID" 2>/dev/null || true
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

sampler() {
  local bench_pid="$1" start now elapsed temp_millic power_microw sclk od_max mode
  local i=0 every
  every=$(( PRINT_INT / SAMPLE_INT ))
  (( every >= 1 )) || every=1
  start="$(date +%s)"
  printf '# elapsed_s\tutc\tedge_mC\tpower_uW\tsclk_MHz\tod_max_MHz\tperf_level\n' > "$TELEMETRY"

  while kill -0 "$bench_pid" 2>/dev/null; do
    now="$(date +%s)"
    elapsed=$(( now - start ))
    temp_millic="$(cat "$TEMP_FILE" 2>/dev/null || printf '0')"
    power_microw="$(cat "$POWER_FILE" 2>/dev/null || printf '0')"
    sclk="$(strix_current_sclk)"
    od_max="$(strix_read_od_max)"
    mode="$(cat "$PERF_FILE" 2>/dev/null || printf 'unknown')"
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
      "$elapsed" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$temp_millic" "$power_microw" \
      "${sclk:-0}" "${od_max:-0}" "$mode" >> "$TELEMETRY"

    if (( temp_millic >= MAX_SAFE_TEMP * 1000 )); then
      printf 'edge reached %s C at elapsed=%ss\n' "$MAX_SAFE_TEMP" "$elapsed" > "$ABORT_FLAG"
      kill -TERM "$bench_pid" 2>/dev/null || true
      break
    fi
    if (( i % every == 0 )); then
      printf '  t=%5ss  edge=%3d C  PPT=%3d W  SCLK=%4s MHz\n' \
        "$elapsed" "$(( temp_millic / 1000 ))" "$(( power_microw / 1000000 ))" "${sclk:-0}"
    fi
    i=$(( i + 1 ))
    sleep "$SAMPLE_INT"
  done
}

[[ "$CAP" == "stock" || "$CAP" =~ ^[0-9]+$ ]] \
  || strix_die "CAP must be an integer MHz value or 'stock'"
[[ "$SAMPLE_INT" =~ ^[0-9]+$ && "$SAMPLE_INT" -gt 0 ]] || strix_die "SAMPLE_INT must be a positive integer"
[[ "$PRINT_INT" =~ ^[0-9]+$ && "$PRINT_INT" -gt 0 ]] || strix_die "PRINT_INT must be a positive integer"
[[ "$DURATION" =~ ^[0-9]+$ && "$DURATION" -gt 0 ]] || strix_die "DURATION must be a positive integer"
[[ "$MAX_SAFE_TEMP" =~ ^[0-9]+$ && "$MAX_SAFE_TEMP" -ge 50 && "$MAX_SAFE_TEMP" -le 100 ]] \
  || strix_die "MAX_SAFE_TEMP must be an integer from 50 through 100 C"
[[ "$LOAD_POWER_THRESHOLD_W" =~ ^[0-9]+$ && "$LOAD_POWER_THRESHOLD_W" -gt 0 ]] \
  || strix_die "LOAD_POWER_THRESHOLD_W must be a positive integer"
[[ -f "$MODEL" ]] || strix_die "model not found: $MODEL"
[[ -x "$LLAMA_BENCH" ]] || strix_die "llama-bench wrapper is not executable: $LLAMA_BENCH"
strix_check_control

strix_find_gpu
strix_find_hwmon
strix_assert_gpu_idle
strix_capture_initial_state

if [[ -e "$OUT_DIR" ]]; then
  strix_die "output directory already exists: $OUT_DIR"
fi
mkdir -p "$OUT_DIR"

NODE_LABEL="$NODE_LABEL" CAMPAIGN_ID="$CAMPAIGN_ID" MODEL="$MODEL" HASH_MODE=none \
  BACKGROUND_CONDITION="$BACKGROUND_CONDITION" \
  "$SCRIPT_DIR/strix-collect-metadata.sh" "$METADATA"

strix_pause_timer
if [[ "$CAP" == "stock" ]]; then
  strix_set_stock
else
  strix_set_cap "$CAP" "$SCLK_FLOOR"
fi

cat > "$OUT_DIR/run-config.txt" <<EOF
run_id=$RUN_ID
node_label=$NODE_LABEL
target=$TARGET_LABEL
duration_under_load_s=$DURATION
max_safe_temp_c=$MAX_SAFE_TEMP
sample_interval_s=$SAMPLE_INT
load_power_threshold_w=$LOAD_POWER_THRESHOLD_W
background_condition=$BACKGROUND_CONDITION
model=$(basename "$MODEL")
pp=$PP
tg=$TG
ngl=$NGL
extra_args=$EXTRA_ARGS
EOF

echo "Soak target=$TARGET_LABEL node=$NODE_LABEL duration=${DURATION}s-under-load GPU=$GPU_PCI"
echo "Artifacts: $OUT_DIR"

strix_reap_container
"$LLAMA_BENCH" -m "$MODEL" -ngl "$NGL" -p "$PP" -n "$TG" -r 999 \
  "${EXTRA_ARGV[@]}" > "$BENCH_LOG" 2>&1 &
BENCH_PID=$!
sampler "$BENCH_PID" &
SAMPLER_PID=$!
EXIT_REASON="waiting-for-load"

launch_start="$(date +%s)"
load_start=""
while [[ -z "$load_start" ]]; do
  sleep "$SAMPLE_INT"
  [[ ! -e "$ABORT_FLAG" ]] || { EXIT_REASON="thermal-abort"; break; }
  kill -0 "$BENCH_PID" 2>/dev/null || { EXIT_REASON="benchmark-exited-before-load"; break; }
  power_microw="$(cat "$POWER_FILE" 2>/dev/null || printf '0')"
  if (( power_microw >= LOAD_POWER_THRESHOLD_W * 1000000 )); then
    load_start="$(date +%s)"
    EXIT_REASON="running"
    echo "Sustained load detected; starting the ${DURATION}s soak clock."
  elif (( $(date +%s) - launch_start >= LOAD_TIMEOUT )); then
    EXIT_REASON="load-timeout"
    break
  fi
done

while [[ "$EXIT_REASON" == "running" ]]; do
  sleep "$SAMPLE_INT"
  [[ ! -e "$ABORT_FLAG" ]] || { EXIT_REASON="thermal-abort"; break; }
  kill -0 "$BENCH_PID" 2>/dev/null || { EXIT_REASON="benchmark-exited-early"; break; }
  if (( $(date +%s) - load_start >= DURATION )); then
    EXIT_REASON="completed"
    break
  fi
done

kill "$BENCH_PID" 2>/dev/null || true
strix_reap_container
wait "$BENCH_PID" 2>/dev/null || true
BENCH_PID=""
kill "$SAMPLER_PID" 2>/dev/null || true
wait "$SAMPLER_PID" 2>/dev/null || true
SAMPLER_PID=""

python3 - "$TELEMETRY" "$LOAD_POWER_THRESHOLD_W" "$EXIT_REASON" <<'PY' | tee "$SUMMARY"
import statistics
import sys

path, threshold_w, reason = sys.argv[1], float(sys.argv[2]), sys.argv[3]
rows = []
with open(path, encoding="utf-8") as handle:
    for line in handle:
        if line.startswith("#"):
            continue
        fields = line.rstrip().split("\t")
        if len(fields) < 7:
            continue
        try:
            rows.append((int(fields[0]), int(fields[2]) / 1000, int(fields[3]) / 1_000_000, int(fields[4])))
        except ValueError:
            pass

loaded = [row for row in rows if row[2] >= threshold_w]
print(f"exit_reason={reason}")
print(f"samples_total={len(rows)}")
print(f"samples_under_load={len(loaded)}")
if len(loaded) < 6:
    print("verdict=insufficient-loaded-samples")
    raise SystemExit

third = max(1, len(loaded) // 3)
first = loaded[:third]
last = loaded[-third:]
first_edge = statistics.fmean(row[1] for row in first)
last_edge = statistics.fmean(row[1] for row in last)

xs = [row[0] / 60 for row in last]
ys = [row[1] for row in last]
x_bar = statistics.fmean(xs)
y_bar = statistics.fmean(ys)
denominator = sum((x - x_bar) ** 2 for x in xs)
slope_per_min = sum((x - x_bar) * (y - y_bar) for x, y in zip(xs, ys)) / denominator if denominator else 0
slope_10m = slope_per_min * 10

print(f"loaded_duration_s={loaded[-1][0] - loaded[0][0]}")
print(f"edge_max_c={max(row[1] for row in loaded):.3f}")
print(f"edge_final_c={loaded[-1][1]:.3f}")
print(f"edge_first_third_avg_c={first_edge:.3f}")
print(f"edge_last_third_avg_c={last_edge:.3f}")
print(f"edge_first_to_last_delta_c={last_edge - first_edge:+.3f}")
print(f"edge_late_slope_c_per_10m={slope_10m:+.3f}")
print(f"power_avg_w={statistics.fmean(row[2] for row in loaded):.3f}")
print(f"power_max_w={max(row[2] for row in loaded):.3f}")
print(f"sclk_avg_mhz={statistics.fmean(row[3] for row in loaded):.1f}")

if reason == "thermal-abort":
    verdict = "thermal-abort"
elif reason != "completed":
    verdict = "incomplete"
elif slope_10m <= 1.0 and last_edge - first_edge <= 1.5:
    verdict = "stabilized"
else:
    verdict = "still-creeping"
print(f"verdict={verdict}")
PY

sha256sum "$TELEMETRY" "$BENCH_LOG" "$METADATA" "$SUMMARY" "$OUT_DIR/run-config.txt" \
  > "$OUT_DIR/SHA256SUMS"

case "$EXIT_REASON" in
  completed) exit 0 ;;
  thermal-abort) exit 2 ;;
  *) exit 1 ;;
esac
