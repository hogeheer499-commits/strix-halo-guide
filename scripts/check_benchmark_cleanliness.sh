#!/usr/bin/env bash
# Read-only benchmark hygiene check. This script does not stop services.
#
# T3 Code is a hard workflow dependency for this workstation. Strix Halo work is
# operated from T3, so T3 must remain running and reachable during all routine
# benchmark work. This script never stops services; it only reports readiness.

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
  body="$(curl -fsS --max-time 5 "$url" 2>/dev/null || true)"
  if printf '%s\n' "$body" | grep -q '"ok"[[:space:]]*:[[:space:]]*true'; then
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
if pgrep -i 'zoom|ZoomClips' >/dev/null; then
  pgrep -i 'zoom|ZoomClips' | xargs -r ps -o pid,pcpu,pmem,comm --no-headers -p
  blocker "Zoom is running"
fi
if command -v virsh >/dev/null 2>&1 && virsh list --state-running --name 2>/dev/null | grep -q .; then
  virsh list --state-running
  blocker "one or more libvirt VMs are running"
fi

section "T3 Workstation Dependency"
T3_LOCAL_BASE="${T3_LOCAL_BASE:-http://127.0.0.1}"
T3_LAN_BASE="${T3_LAN_BASE:-http://192.168.2.13}"
if pgrep -f -i 't3code' >/dev/null; then
  pgrep -f -i 't3code' | xargs -r ps -o pid,pcpu,pmem,comm --no-headers -p
  info "T3 Code process is running and protected"
else
  blocker "T3 Code process is not running"
fi
if pgrep -f -i 't3_react185_semantic_proxy|t3-react185-semantic-proxy' >/dev/null; then
  pgrep -f -i 't3_react185_semantic_proxy|t3-react185-semantic-proxy' | xargs -r ps -o pid,pcpu,pmem,comm --no-headers -p
  info "T3 semantic proxy is running and protected"
else
  blocker "T3 semantic proxy is not running"
fi
check_http "T3 local backend" "${T3_LOCAL_BASE}:3773/"
check_http "T3 LAN backend" "${T3_LAN_BASE}:3773/"
check_json_ok "T3 local semantic proxy" "${T3_LOCAL_BASE}:3777/__t3react185/health"
check_http "T3 LAN semantic proxy" "${T3_LAN_BASE}:3777/"

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
  printf 'NOT CLEAN ENOUGH for publishable benchmarks.\n'
  exit 2
fi
if [ "$warnings" -gt 0 ]; then
  printf 'USABLE FOR SMOKE TESTS, but review warnings before publishing numbers.\n'
  exit 1
fi
printf 'CLEAN ENOUGH for benchmark runs.\n'
