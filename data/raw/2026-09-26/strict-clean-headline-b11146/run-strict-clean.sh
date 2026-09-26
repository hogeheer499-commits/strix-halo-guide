#!/usr/bin/env bash
# Strict-clean re-check of direct llama-bench headline rows on llama.cpp b11146.
set -u
OUT="$HOME/strix-halo-guide-audit/data/raw/2026-09-26/strict-clean-headline-b11146"
mkdir -p "$OUT"
cd "$OUT"
DOM=ubuntu-zoom
V="virsh -c qemu:///system"
LOG="$OUT/run-order.log"
NEW="$HOME/llama-cpp-b11146/llama-b11146/llama-bench"
B10687="$HOME/benchmark-tools/llama-b10687-src/build/bin/llama-bench"
B9172="$HOME/llama-cpp-upstream-2026-05-16/build-vulkan/bin/llama-bench"
B9049="$HOME/llama-cpp-upstream-2026-05-07/build-vulkan/bin/llama-bench"
M=$HOME/models
export AMD_VULKAN_ICD=RADV VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json
SUSPENDED=0

log(){ echo "$(date -Iseconds) $*" | tee -a "$LOG"; }

cleanup(){
  if [ "$SUSPENDED" = 1 ]; then
    $V resume $DOM >>"$LOG" 2>&1 && log "VM resumed" || log "VM RESUME FAILED"
  fi
  $HOME/.local/bin/adaptive-power-guard --clear-boost >>"$LOG" 2>&1 || true
  sleep 20
  snapshot after
  $V list --all > "$OUT/vm-state-after.txt" 2>&1
  log "DONE"
}
trap cleanup EXIT
trap 'log "signal received"; exit 1' INT TERM HUP

snapshot(){
  f="$OUT/host-snapshot-$1.txt"
  {
    echo "timestamp: $(date -Iseconds)"
    echo "kernel: $(uname -srvm)"
    echo "power_profile: $(powerprofilesctl get 2>&1)"
    echo "amdgpu_dpm_level: $(cat /sys/class/drm/card*/device/power_dpm_force_performance_level 2>/dev/null | head -1)"
    echo "gpu_busy_percent: $(cat /sys/class/drm/card*/device/gpu_busy_percent 2>/dev/null | head -1)"
    echo "adaptive_power_guard: $(systemctl --user is-active adaptive-power-guard 2>&1)"
    echo "--- vulkaninfo --summary (GPU0)"
    vulkaninfo --summary 2>/dev/null | grep -E "apiVersion|driverVersion|driverName|deviceName" | head -4
    echo "--- packages"
    dpkg-query -W -f='${Package} ${Version}\n' mesa-vulkan-drivers linux-firmware 2>/dev/null
    echo "--- memory"
    free -g
    grep -E "MemAvailable|SwapFree" /proc/meminfo
    echo "--- ollama ps"
    ollama ps 2>&1
    echo "--- libvirt domains"
    $V list --all 2>&1
    echo "--- GPU render node holders (runtime names only)"
    for p in $(fuser /dev/dri/renderD128 2>/dev/null); do cat /proc/$p/comm 2>/dev/null; done | sort | uniq -c
    echo "--- top -bn1 (by CPU; %CPU %MEM COMMAND name only)"
    top -bn1 -o %CPU -w 200 | sed -n '8,30p' | awk '{print $9, $10, $12}'
  } > "$f" 2>&1
}

bench(){ # name bin args...
  name=$1; bin=$2; shift 2
  log "START $name"
  echo "$bin $*" | sed "s#$HOME#~#g" > "$OUT/$name.command.txt"
  "$bin" "$@" -o csv > "$OUT/$name.csv" 2> "$OUT/$name.stderr.log"
  rc=$?
  log "END $name rc=$rc"
  sleep 10
}

log "BEGIN"
snapshot pre-cleanup
# 1. Ollama: stop any loaded models
for m in $(ollama ps 2>/dev/null | awk 'NR>1{print $1}'); do ollama stop "$m" >>"$LOG" 2>&1; log "ollama stop $m"; done
# 2. Suspend VM
if $V suspend $DOM >>"$LOG" 2>&1; then SUSPENDED=1; log "VM $DOM suspended"; else log "VM suspend FAILED (recorded as remaining load)"; fi
# 3. Performance via the machine's own guard boost (self-expiring)
$HOME/.local/bin/adaptive-power-guard --boost 120 >>"$LOG" 2>&1
sleep 30
snapshot before

# Qwen3-Coder 30B UD-Q4_K_XL
C=$M/Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf
bench coder-udq4kxl-b11146-p512-n128-r20       $NEW    -m $C -fa 1 -ngl 999 -p 512 -n 128 -r 20
bench coder-udq4kxl-b10687-p512-n128-r20       $B10687 -m $C -fa 1 -ngl 999 -p 512 -n 128 -r 20
bench coder-udq4kxl-b11146-lmnone-guide-r20    $NEW    -m $C -fa 1 -ngl 999 -lm none -b 2048 -ub 512 -p 512 -n 128 -r 20
bench coder-udq4kxl-b9049-mmp0-guide-r20       $B9049  -m $C -fa 1 -ngl 999 -mmp 0 -b 2048 -ub 512 -p 512 -n 128 -r 20

# Qwen3-Next 80B UD-Q4_K_XL
N=$M/Qwen3-Next-80B-A3B-Instruct-UD-Q4_K_XL.gguf
bench next80b-udq4kxl-b11146-p512-n128-r20     $NEW    -m $N -fa 1 -ngl 999 -p 512 -n 128 -r 20
bench next80b-udq4kxl-b10687-p512-n128-r20     $B10687 -m $N -fa 1 -ngl 999 -p 512 -n 128 -r 20
bench next80b-udq4kxl-b11146-lmnone-ub1024-pp-r20 $NEW   -m $N -fa 1 -ngl 999 -lm none -b 2048 -ub 1024 -p 512 -n 0 -r 20
bench next80b-udq4kxl-b11146-lmnone-ub1024-tg-r20 $NEW   -m $N -fa 1 -ngl 999 -lm none -b 2048 -ub 1024 -p 0 -n 128 -r 20
bench next80b-udq4kxl-b9172-mmp0-ub1024-pp-r20 $B9172  -m $N -fa 1 -ngl 999 -mmp 0 -b 2048 -ub 1024 -p 512 -n 0 -r 20
bench next80b-udq4kxl-b9172-mmp0-ub1024-tg-r20 $B9172  -m $N -fa 1 -ngl 999 -mmp 0 -b 2048 -ub 1024 -p 0 -n 128 -r 20

# gpt-oss-120b MXFP4
G=$M/gpt-oss-120b-GGUF/gpt-oss-120b-mxfp4-00001-of-00003.gguf
bench gptoss120b-b11146-lmnone-pp512-r3        $NEW    -m $G -fa 1 -ngl 999 -lm none -b 2048 -ub 512 -p 512 -n 0 -r 3
bench gptoss120b-b11146-lmnone-tg128-r20       $NEW    -m $G -fa 1 -ngl 999 -lm none -b 2048 -ub 512 -p 0 -n 128 -r 20
bench gptoss120b-b9049-mmp0-pp512-r3           $B9049  -m $G -fa 1 -ngl 999 -mmp 0 -b 2048 -ub 512 -p 512 -n 0 -r 3
bench gptoss120b-b9049-mmp0-tg128-r20          $B9049  -m $G -fa 1 -ngl 999 -mmp 0 -b 2048 -ub 512 -p 0 -n 128 -r 20
bench gptoss120b-b11146-lmnone-pp65536-r1      $NEW    -m $G -fa 1 -ngl 999 -lm none -b 2048 -ub 512 -p 65536 -n 0 -r 1

# Qwen3.8-Flash-Next UD-IQ4_XS (~93.7 GB): memory-gated
avail=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
log "MemAvailable before flash-next: ${avail} kB"
if [ "$avail" -ge 100000000 ]; then
  F=$M/qwen38-flash-next-ud-iq4xs/Qwen3.8-Flash-Next-UD-IQ4_XS-00001-of-00003.gguf
  bench flashnext-udiq4xs-b11146-p512-n128-r10 $NEW    -m $F -fa 1 -ngl 999 -p 512 -n 128 -r 10
  bench flashnext-udiq4xs-b10687-p512-n128-r10 $B10687 -m $F -fa 1 -ngl 999 -p 512 -n 128 -r 10
else
  log "SKIP flash-next: MemAvailable below 100000000 kB gate"
fi
snapshot end-of-runs
