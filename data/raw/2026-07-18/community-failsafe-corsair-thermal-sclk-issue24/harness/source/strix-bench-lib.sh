#!/usr/bin/env bash
# Shared safety and state-management helpers for the Strix Halo benchmark tools.

strix_die() {
  echo "ERROR: $*" >&2
  exit 1
}

strix_control() {
  sudo -n "${BENCH_CONTROL:-/usr/local/sbin/strix-bench-control}" "$@"
}

strix_check_control() {
  strix_control check \
    || strix_die "passwordless benchmark control is unavailable"
}

strix_read_od_min() {
  awk '/^0:/{gsub(/[^0-9]/,"",$2); print $2; exit}' "$OD_FILE"
}

strix_read_od_max() {
  awk '/^1:/{gsub(/[^0-9]/,"",$2); print $2; exit}' "$OD_FILE"
}

strix_find_gpu() {
  local d dev
  if [[ -n "${GPU_PCI:-}" ]]; then
    GPU="/sys/bus/pci/devices/${GPU_PCI}"
    [[ -e "$GPU/pp_od_clk_voltage" ]] \
      || strix_die "no overdrive node at $GPU"
    [[ "$(cat "$GPU/vendor" 2>/dev/null)" == "0x1002" ]] \
      || strix_die "$GPU is not an AMD GPU"
  else
    GPU=""
    for d in /sys/bus/pci/devices/*/pp_od_clk_voltage; do
      [[ -e "$d" ]] || continue
      dev="${d%/pp_od_clk_voltage}"
      [[ "$(cat "$dev/vendor" 2>/dev/null)" == "0x1002" ]] || continue
      GPU="$dev"
      GPU_PCI="$(basename "$dev")"
      break
    done
    [[ -n "$GPU" ]] \
      || strix_die "no AMD overdrive node found; verify amdgpu.ppfeaturemask=0xffffffff"
  fi

  OD_FILE="$GPU/pp_od_clk_voltage"
  PERF_FILE="$GPU/power_dpm_force_performance_level"
  SCLK_FILE="$GPU/pp_dpm_sclk"
}

strix_find_hwmon() {
  local h label_file input_file
  TEMP_FILE=""
  POWER_FILE=""

  for h in "$GPU"/hwmon/hwmon*; do
    [[ -d "$h" ]] || continue
    for label_file in "$h"/temp*_label; do
      [[ -e "$label_file" ]] || continue
      if [[ "$(tr '[:upper:]' '[:lower:]' < "$label_file")" == "edge" ]]; then
        input_file="${label_file%_label}_input"
        [[ -e "$input_file" ]] && TEMP_FILE="$input_file"
      fi
    done
    [[ -n "$TEMP_FILE" ]] || [[ ! -e "$h/temp1_input" ]] || TEMP_FILE="$h/temp1_input"

    if [[ -e "$h/power1_average" ]]; then
      POWER_FILE="$h/power1_average"
    elif [[ -e "$h/power1_input" ]]; then
      POWER_FILE="$h/power1_input"
    fi
  done

  [[ -n "$TEMP_FILE" && -n "$POWER_FILE" ]] \
    || strix_die "could not find edge temperature and power telemetry under $GPU/hwmon"
}

strix_capture_initial_state() {
  INITIAL_MODE="$(cat "$PERF_FILE")"
  INITIAL_OD_MIN="$(strix_read_od_min)"
  INITIAL_OD_MAX="$(strix_read_od_max)"
  [[ -n "$INITIAL_MODE" && -n "$INITIAL_OD_MIN" && -n "$INITIAL_OD_MAX" ]] \
    || strix_die "could not capture the initial GPU overdrive state"
  STRIX_STATE_CAPTURED=1
}

strix_pause_timer() {
  TIMER_WAS_ACTIVE=0
  [[ -n "${TIMER_UNIT:-}" ]] || return 0
  if systemctl is-active --quiet "$TIMER_UNIT" 2>/dev/null; then
    strix_control timer-stop
    TIMER_WAS_ACTIVE=1
    echo "Paused $TIMER_UNIT."
  fi
}

strix_set_cap() {
  local cap="$1" floor="${2:-$SCLK_FLOOR}"
  [[ "$floor" =~ ^[0-9]+$ && "$cap" =~ ^[0-9]+$ ]] \
    || strix_die "SCLK floor and ceiling must be integer MHz values"
  (( floor >= 100 && cap >= floor && cap <= 3000 )) \
    || strix_die "refusing invalid SCLK range ${floor}-${cap} MHz"
  strix_control set-cap "$floor" "$cap"

  [[ "$(cat "$PERF_FILE")" == "manual" ]] \
    || strix_die "GPU performance level did not enter manual mode"
  [[ "$(strix_read_od_min)" == "$floor" && "$(strix_read_od_max)" == "$cap" ]] \
    || strix_die "GPU overdrive readback did not match ${floor}-${cap} MHz"
}

strix_set_stock() {
  local max
  strix_control set-stock
  sleep 1

  max="$(strix_read_od_max)"
  [[ "$(cat "$PERF_FILE")" == "auto" ]] \
    || strix_die "GPU performance level did not return to auto"
  [[ "$max" =~ ^[0-9]+$ && "$max" -ge "${STOCK_EXPECTED_MIN_MHZ:-2800}" ]] \
    || strix_die "OD reset readback was ${max:-unknown} MHz, not an expected stock ceiling"
}

strix_restore_initial_state() {
  local rc=0
  [[ "${STRIX_STATE_CAPTURED:-0}" == "1" ]] || return 0

  strix_control restore "$INITIAL_OD_MIN" "$INITIAL_OD_MAX" "$INITIAL_MODE" || rc=1

  if [[ "$rc" == "0" ]]; then
    echo "Restored initial GPU state: mode=$INITIAL_MODE, SCLK=${INITIAL_OD_MIN}-${INITIAL_OD_MAX} MHz."
  else
    echo "WARNING: failed to restore the complete initial GPU state" >&2
  fi

  if [[ "${TIMER_WAS_ACTIVE:-0}" == "1" ]]; then
    strix_control timer-start \
      && echo "Re-started $TIMER_UNIT." \
      || echo "WARNING: failed to restart $TIMER_UNIT" >&2
  fi
  STRIX_STATE_CAPTURED=0
  return "$rc"
}

strix_assert_gpu_idle() {
  local holders
  [[ "${ALLOW_GPU_BUSY:-0}" == "1" ]] && return 0
  holders="$(fuser /dev/kfd /dev/dri/renderD* 2>/dev/null || true)"
  [[ -z "$holders" ]] \
    || strix_die "GPU device files are still held by process IDs:${holders}; stop competing workloads or set ALLOW_GPU_BUSY=1"
}

strix_reap_container() {
  podman rm -f "${CONTAINER_NAME:-strix-bench}" >/dev/null 2>&1 || true
}

strix_current_sclk() {
  awk '/\*/{for(i=1;i<=NF;i++) if($i ~ /Mhz/){gsub(/[^0-9]/,"",$i); print $i; exit}}' \
    "$SCLK_FILE" 2>/dev/null || true
}
