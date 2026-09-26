#!/usr/bin/env bash
# Second pass: pp512/tg128 r10 with -o json, because the b11146 CSV output has no
# per-repeat samples. Same routine conditions as run-routine.sh (nothing paused).
set -u
OUT="$HOME/strix-halo-guide-audit/data/raw/2026-09-26/64gb-tier-30b-candidates-b11146"
cd "$OUT"
LOG="$OUT/run-order.log"
BIN="$HOME/llama-cpp-b11146/llama-b11146"
M="$HOME/models/2026-09-26"
export AMD_VULKAN_ICD=RADV VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json
HOST=$(hostname)
red(){ sed -e "s#$HOME#~#g" -e "s#$HOST#<host>#g"; }
log(){ echo "$(date -Iseconds) $*" | tee -a "$LOG"; }

jbench(){ # name file
  name=$1; f=$M/$2
  log "START $name"
  echo "$BIN/llama-bench -m $f -fa 1 -ngl 999 -p 512 -n 128 -r 10 -o json" | red > "$OUT/$name.command.txt"
  "$BIN/llama-bench" -m "$f" -fa 1 -ngl 999 -p 512 -n 128 -r 10 -o json 2> >(red > "$OUT/$name.stderr.log") | red > "$OUT/$name.json"
  rc=${PIPESTATUS[0]}
  log "END $name rc=$rc"
  sleep 10
}

log "BEGIN samples pass (routine: nothing paused)"
jbench nemotron35-lightning-q4_0-b11146-p512-n128-r10-pass2 NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q4_0.gguf
jbench laguna-xs21-q4km-b11146-p512-n128-r10-pass2 Laguna-XS-2.1-Q4_K_M.gguf
jbench muse-glimmer-30b-q4km-b11146-p512-n128-r10-pass2 Muse-Glimmer-30B-KQuant-17GB-Q4_K_M.gguf
{ echo "timestamp: $(date -Iseconds)"; echo "--- ollama ps"; ollama ps 2>&1; echo "--- memory"; free -g; echo "--- libvirt domains"; virsh -c qemu:///system list --all 2>&1; echo "gpu_busy_percent: $(cat /sys/class/drm/card*/device/gpu_busy_percent 2>/dev/null | head -1)"; } 2>&1 | red > "$OUT/host-snapshot-after-pass2.txt"
log "DONE samples pass"
