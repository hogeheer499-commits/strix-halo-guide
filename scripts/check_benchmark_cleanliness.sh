#!/usr/bin/env bash
# Read-only benchmark hygiene check. This script does not stop services.
#
# Set BENCHMARK_POWER_POLICY=tuned only for a tuned reproduction. Optional
# BENCHMARK_HEALTH_URLS lists JSON health endpoints. This inventory cannot prove
# GPU inactivity or strict-clean conditions from process names alone. It does not
# record process names, listening ports, or container names: note any known
# background workload in your own run notes.

set -u

blockers=0
warnings=0

section() {
  printf '\n== %s ==\n' "$1"
}

blocker() {
  blockers=$((blockers + 1))
  printf 'BLOCKER: %s\n' "$1"
}

warn() {
  warnings=$((warnings + 1))
  printf 'WARN: %s\n' "$1"
}

info() {
  printf 'INFO: %s\n' "$1"
}

check_http() {
  label="$1"
  url="$2"
  if curl -fsSIL --max-time 5 "$url" >/dev/null 2>&1; then
    info "$label is reachable: $url"
  else
    blocker "$label is not reachable: $url"
  fi
}

check_json_ok() {
  label="$1"
  url="$2"
  if ! body="$(curl -fsS --max-time 5 "$url" 2>/dev/null)"; then
    blocker "$label HTTP request failed: $url"
    return
  fi
  if printf '%s\n' "$body" | python3 -c 'import json,sys; d=json.load(sys.stdin); sys.exit(0 if isinstance(d,dict) and d.get("ok") is True else 1)' 2>/dev/null; then
    info "$label is healthy: $url"
  else
    blocker "$label is not healthy: $url"
  fi
}

section "Host Load"
date -Is
uptime
free -h

section "Platform"
for file in /sys/class/dmi/id/bios_version /sys/class/dmi/id/bios_date; do
  if [ -r "$file" ]; then
    printf '%s: %s\n' "$(basename "$file")" "$(cat "$file")"
  else
    info "$(basename "$file") is not readable on this system"
  fi
done
if [ -r /sys/firmware/acpi/platform_profile ]; then
  printf 'platform_profile: %s\n' "$(cat /sys/firmware/acpi/platform_profile)"
else
  info "platform_profile is not exposed on this system; record the power profile another way"
fi

section "tuned"
BENCHMARK_POWER_POLICY="${BENCHMARK_POWER_POLICY:-recorded}"
if [ "$BENCHMARK_POWER_POLICY" != recorded ] && [ "$BENCHMARK_POWER_POLICY" != tuned ]; then
  blocker "BENCHMARK_POWER_POLICY must be recorded or tuned"
fi
if command -v tuned-adm >/dev/null 2>&1; then
  tuned_output="$(tuned-adm active 2>&1 || true)"
  printf '%s\n' "$tuned_output"
  if [ "$BENCHMARK_POWER_POLICY" = tuned ] && ! printf '%s\n' "$tuned_output" | grep -qi '^Current active profile: accelerator-performance$'; then
    blocker "tuned accelerator-performance is not active"
  fi
else
  if [ "$BENCHMARK_POWER_POLICY" = tuned ]; then blocker "selected tuned policy is not installed"; else info "tuned not installed; match recorded alternate policy"; fi
fi
if systemctl is-active --quiet power-profiles-daemon 2>/dev/null; then
  if [ "$BENCHMARK_POWER_POLICY" = tuned ]; then blocker "active power-profiles-daemon conflicts with selected tuned policy"; else info "power-profiles-daemon active; record its profile"; fi
  if command -v powerprofilesctl >/dev/null 2>&1; then
    printf 'powerprofilesctl: %s\n' "$(powerprofilesctl get 2>&1)"
  fi
else
  info "power-profiles-daemon is inactive"
fi
gov_summary="$(for file in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do [ -e "$file" ] && cat "$file"; done | sort | uniq -c)"
printf '%s\n' "$gov_summary"
if printf '%s\n' "$gov_summary" | grep -vq 'performance'; then
  warn "not all CPU governors report performance"
fi

section "GPU Clock"
for file in /sys/class/drm/card*/device/pp_dpm_sclk; do
  [ -e "$file" ] || continue
  printf '%s\n' "$file"
  cat "$file"
  info "Compare clocks under workload with the selected profile; idle clocks are not a readiness verdict"
done

section "Vulkan Device"
if command -v vulkaninfo >/dev/null 2>&1; then
  vulkaninfo --summary 2>/dev/null | sed -n '/Devices:/,$p' | sed -n '1,40p'
  if ! vulkaninfo --summary 2>/dev/null | grep -q 'RADV STRIX_HALO'; then
    blocker "RADV STRIX_HALO was not detected by vulkaninfo"
  fi
else
  warn "vulkaninfo is not installed"
fi

section "Background Load"
# Uses the load average, the GPU busy counter, and a VM count; no names are recorded.
load1="$(cut -d' ' -f1 /proc/loadavg 2>/dev/null || echo 0)"
if awk -v l1="$load1" 'BEGIN { exit !(l1 >= 1.0) }'; then
  warn "1-minute load average is $load1; record the background load and measure its CPU, GPU, and I/O activity before classifying conditions"
else
  info "1-minute load average is $load1"
fi
for file in /sys/class/drm/card*/device/gpu_busy_percent; do
  [ -e "$file" ] || continue
  gpu_busy="$(cat "$file" 2>/dev/null || echo 0)"
  info "GPU busy: ${gpu_busy}%"
  if [ "$gpu_busy" -gt 5 ] 2>/dev/null; then
    warn "GPU is busy (${gpu_busy}%) before the run; find out which workload holds it"
  fi
done
if command -v virsh >/dev/null 2>&1; then
  vm_count="$(virsh list --state-running --name 2>/dev/null | grep -c . || true)"
  if [ "${vm_count:-0}" -gt 0 ]; then
    warn "$vm_count VM(s) running; record their actual load and control them for strict comparisons"
  fi
fi

section "Optional Health Dependencies"
# Space-separated URLs must each return JSON {"ok": true}. No private defaults.
for health_url in ${BENCHMARK_HEALTH_URLS:-}; do
  check_json_ok "Configured dependency" "$health_url"
done

section "Local AI and Containers"
ai_pids="$(
  {
    pgrep -x ollama 2>/dev/null || true
    pgrep -x llama-server 2>/dev/null || true
    pgrep -f -i 'vllm' 2>/dev/null || true
  } | sort -nu
)"
if [ -n "$ai_pids" ]; then
  ai_count="$(printf '%s\n' "$ai_pids" | grep -c .)"
  warn "$ai_count local AI service process(es) already running; confirm they are part of the test (names and PIDs are not recorded)"
fi
for engine in docker podman; do
  if command -v "$engine" >/dev/null 2>&1; then
    running="$("$engine" ps -q 2>/dev/null | grep -c . || true)"
    if [ "${running:-0}" -gt 0 ]; then
      info "$engine reports $running running container(s); names and ports are not recorded"
    fi
  fi
done

section "Verdict"
printf 'Blockers: %s\n' "$blockers"
printf 'Warnings: %s\n' "$warnings"
if [ "$blockers" -gt 0 ]; then
  printf 'Selected prerequisites failed; investigate before the run.\n'
  exit 2
fi
if [ "$warnings" -gt 0 ]; then
  printf 'Review observations and workload activity against the selected claim class.\n'
  exit 1
fi
printf 'Inventory complete; this does not certify strict-clean conditions or GPU inactivity.\n'
