#!/usr/bin/env bash
# Read-only benchmark hygiene check. This script does not stop services.
#
# Set BENCHMARK_POWER_POLICY=tuned only for a tuned reproduction. Optional
# BENCHMARK_HEALTH_URLS lists JSON health endpoints. This inventory cannot prove
# GPU inactivity or strict-clean conditions from process names alone.

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

section "Known Benchmark Noise"
if pgrep -i rustdesk >/dev/null; then
  pgrep -i rustdesk | xargs -r ps -o pid,pcpu,pmem,comm --no-headers -p
  warn "RustDesk process present; measure actual CPU/GPU/I/O activity before classifying conditions"
fi
if pgrep -i 'zoom|ZoomClips' >/dev/null; then
  pgrep -i 'zoom|ZoomClips' | xargs -r ps -o pid,pcpu,pmem,comm --no-headers -p
  warn "Zoom process present; measure actual CPU/GPU/I/O activity before classifying conditions"
fi
if command -v virsh >/dev/null 2>&1 && virsh list --state-running --name 2>/dev/null | grep -q .; then
  virsh list --state-running
  warn "VMs are present; record their actual load and control them for strict comparisons"
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
    pgrep -f -i 'vllm|open_webui|comfy|webui' 2>/dev/null || true
  } | sort -nu
)"
if [ -n "$ai_pids" ]; then
  printf '%s\n' "$ai_pids" | xargs -r ps -o pid,pcpu,pmem,comm --no-headers -p
  warn "local AI services are already running; confirm they are part of the test"
fi
if command -v docker >/dev/null 2>&1; then
  docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}' 2>/dev/null || true
fi
if command -v podman >/dev/null 2>&1; then
  podman ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}' 2>/dev/null || true
fi

section "Listening Ports"
ss -tulpn | grep -E '(:11434|:8080|:18001|:3000|:3773|:3774|:3776|:3777|:22|ollama|llama|vllm|node|rustdesk|python)' || true

section "Top CPU Processes"
ps -eo pid,ppid,stat,pcpu,pmem,comm --sort=-pcpu | head -20

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
