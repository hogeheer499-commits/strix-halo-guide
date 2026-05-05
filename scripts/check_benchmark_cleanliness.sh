#!/usr/bin/env bash
# Read-only benchmark hygiene check. This script does not stop services.
#
# Optional:
#   STRICT_T3=1 scripts/check_benchmark_cleanliness.sh
#
# T3 Code is a protected workflow dependency for this workstation. It stays on
# by default and is reported as informational background state, not benchmark
# noise. Use STRICT_T3=1 only after an explicit request for a no-T3 A/B run.

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

section "Host Load"
date -Is
uptime
free -h

section "tuned"
if command -v tuned-adm >/dev/null 2>&1; then
  tuned_output="$(tuned-adm active 2>&1 || true)"
  printf '%s\n' "$tuned_output"
  if ! printf '%s\n' "$tuned_output" | grep -qi '^Current active profile: accelerator-performance$'; then
    blocker "tuned accelerator-performance is not active"
  fi
else
  blocker "tuned-adm is not installed"
fi

section "GPU Clock"
for file in /sys/class/drm/card*/device/pp_dpm_sclk; do
  [ -e "$file" ] || continue
  printf '%s\n' "$file"
  cat "$file"
  if ! grep -q '2900Mhz \*' "$file"; then
    warn "GPU clock does not show 2900Mhz as the active state"
  fi
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
  blocker "RustDesk is running"
fi
if pgrep -f -i 't3code|t3_react185' >/dev/null; then
  pgrep -f -i 't3code|t3_react185' | xargs -r ps -o pid,pcpu,pmem,comm --no-headers -p
  if [ "${STRICT_T3:-0}" = "1" ]; then
    blocker "T3 Code or T3 proxy is running and STRICT_T3=1 was requested"
  else
    info "T3 Code or T3 proxy is running; protected and allowed by default"
  fi
fi
if pgrep -i 'zoom|ZoomClips' >/dev/null; then
  pgrep -i 'zoom|ZoomClips' | xargs -r ps -o pid,pcpu,pmem,comm --no-headers -p
  blocker "Zoom is running"
fi
if command -v virsh >/dev/null 2>&1 && virsh list --state-running --name 2>/dev/null | grep -q .; then
  virsh list --state-running
  blocker "one or more libvirt VMs are running"
fi

section "Local AI and Containers"
if pgrep -f -i 'ollama|llama-server|vllm|open_webui|comfy|webui' >/dev/null; then
  pgrep -f -i 'ollama|llama-server|vllm|open_webui|comfy|webui' | xargs -r ps -o pid,pcpu,pmem,comm --no-headers -p
  warn "local AI services are already running; confirm they are part of the test"
fi
if command -v docker >/dev/null 2>&1; then
  docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}' 2>/dev/null || true
fi
if command -v podman >/dev/null 2>&1; then
  podman ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}' 2>/dev/null || true
fi

section "Listening Ports"
ss -tulpn | grep -E '(:11434|:8080|:18001|:3000|:3773|:3774|:3776|:22|ollama|llama|vllm|node|rustdesk|python)' || true

section "Top CPU Processes"
ps -eo pid,ppid,stat,pcpu,pmem,comm --sort=-pcpu | head -20

section "Verdict"
printf 'Blockers: %s\n' "$blockers"
printf 'Warnings: %s\n' "$warnings"
if [ "$blockers" -gt 0 ]; then
  printf 'NOT CLEAN ENOUGH for publishable benchmarks.\n'
  exit 2
fi
if [ "$warnings" -gt 0 ]; then
  printf 'USABLE FOR SMOKE TESTS, but review warnings before publishing numbers.\n'
  exit 1
fi
printf 'CLEAN ENOUGH for benchmark runs.\n'
