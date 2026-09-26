#!/usr/bin/env bash
# Routine 64GB-tier 30B-class candidate campaign on llama.cpp v0.5.0 (b11146):
# direct llama-bench plus a deterministic correctness smoke per model.
# Routine conditions: the VM and background workloads are NOT paused and the
# power profile is left as found. No speculative/MTP/DFlash/vision in this lane.
set -u
OUT="$HOME/strix-halo-guide-audit/data/raw/2026-09-26/64gb-tier-30b-candidates-b11146"
mkdir -p "$OUT"; cd "$OUT"
LOG="$OUT/run-order.log"
BIN="$HOME/llama-cpp-b11146/llama-b11146"
M="$HOME/models/2026-09-26"
export AMD_VULKAN_ICD=RADV VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json
HOST=$(hostname)
red(){ sed -e "s#$HOME#~#g" -e "s#$HOST#<host>#g"; }
log(){ echo "$(date -Iseconds) $*" | tee -a "$LOG"; }

snapshot(){
  f="$OUT/host-snapshot-$1.txt"
  {
    echo "timestamp: $(date -Iseconds)"
    echo "kernel: $(uname -srm)"
    echo "power_profile: $(powerprofilesctl get 2>&1)"
    echo "amdgpu_dpm_level: $(cat /sys/class/drm/card*/device/power_dpm_force_performance_level 2>/dev/null | head -1)"
    echo "gpu_busy_percent: $(cat /sys/class/drm/card*/device/gpu_busy_percent 2>/dev/null | head -1)"
    echo "loadavg: $(cat /proc/loadavg)"
    echo "--- vulkaninfo --summary (GPU0)"
    vulkaninfo --summary 2>/dev/null | grep -E "apiVersion|driverVersion|driverName|deviceName" | head -4
    echo "--- packages"
    dpkg-query -W -f='${Package} ${Version}\n' mesa-vulkan-drivers linux-firmware 2>/dev/null
    echo "--- memory"
    free -g
    grep -E "MemAvailable|SwapFree" /proc/meminfo
    echo "--- disk (home filesystem: size used avail use%)"
    df -h "$HOME" | awk '{print $2, $3, $4, $5}'
    echo "--- ollama ps"
    ollama ps 2>&1
    echo "--- libvirt domains (not paused: routine run)"
    virsh -c qemu:///system list --all 2>&1
    echo "--- GPU render node holders (runtime names only)"
    for p in $(fuser /dev/dri/renderD128 2>/dev/null); do cat /proc/$p/comm 2>/dev/null; done | sort | uniq -c
    echo "--- top -bn1 (by CPU; %CPU %MEM COMMAND name only)"
    top -bn1 -o %CPU -w 200 | sed -n '8,30p' | awk '{print $9, $10, $12}'
  } 2>&1 | red > "$f"
}

bench(){ # name args...
  name=$1; shift
  log "START $name"
  echo "$BIN/llama-bench $* -o csv" | red > "$OUT/$name.command.txt"
  "$BIN/llama-bench" "$@" -o csv > "$OUT/$name.csv" 2> >(red > "$OUT/$name.stderr.log")
  rc=$?
  log "END $name rc=$rc"
  sleep 10
}

P1="What is 17 multiplied by 23? Answer with the number only."
P2="Write a Python function is_prime(n) that returns True if n is a prime number and False otherwise. Reply with only the code."
smoke(){ # short model promptid prompt run
  s=$1; model=$2; pid=$3; prompt=$4; run=$5
  tag="$s-smoke-$pid-run$run"
  log "START $tag"
  echo "$BIN/llama-completion -m $model -ngl 999 -fa 1 -c 4096 -n 1024 --temp 0 --top-k 1 --seed 42 --jinja -st -p \"$prompt\"" | red > "$OUT/$tag.command.txt"
  timeout 600 "$BIN/llama-completion" -m "$model" -ngl 999 -fa 1 -c 4096 -n 1024 --temp 0 --top-k 1 --seed 42 --jinja -st -p "$prompt" \
     < /dev/null 2> >(red > "$OUT/$tag.stderr.log") | red > "$OUT/$tag.out.txt"
  rc=${PIPESTATUS[0]}
  log "END $tag rc=$rc"
  sleep 5
}

model_block(){ # short file
  s=$1; f=$M/$2
  bench "$s-b11146-p512-n128-r10" -m "$f" -fa 1 -ngl 999 -p 512 -n 128 -r 10
  bench "$s-b11146-pp8192-r3" -m "$f" -fa 1 -ngl 999 -p 8192 -n 0 -r 3
  bench "$s-b11146-tg128-d8192-r3" -m "$f" -fa 1 -ngl 999 -p 0 -n 128 -d 8192 -r 3
  for r in 1 2; do
    smoke "$s" "$f" arith "$P1" "$r"
    smoke "$s" "$f" code "$P2" "$r"
  done
}

log "BEGIN (routine: VM and background workloads not paused)"
for m in $(ollama ps 2>/dev/null | awk 'NR>1{print $1}'); do ollama stop "$m" >>"$LOG" 2>&1; log "ollama stop $m"; done
"$BIN/llama-bench" --version 2>&1 | red | tail -2 > "$OUT/build-version.txt"
snapshot before
model_block nemotron35-lightning-q4_0 NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q4_0.gguf
snapshot mid-1
model_block laguna-xs21-q4km Laguna-XS-2.1-Q4_K_M.gguf
snapshot mid-2
model_block muse-glimmer-30b-q4km Muse-Glimmer-30B-KQuant-17GB-Q4_K_M.gguf
for m in $(ollama ps 2>/dev/null | awk 'NR>1{print $1}'); do ollama stop "$m" >>"$LOG" 2>&1; log "ollama stop $m"; done
sleep 10
snapshot after
log "DONE"
