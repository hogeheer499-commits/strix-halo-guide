#!/usr/bin/env bash
# Supplementary smoke: Laguna XS 2.1 code prompt hit the 1024-token cap while
# still reasoning in run-routine.sh; repeat twice with -n 4096. Same conditions.
set -u
OUT="$HOME/strix-halo-guide-audit/data/raw/2026-09-26/64gb-tier-30b-candidates-b11146"
cd "$OUT"
LOG="$OUT/run-order.log"
BIN="$HOME/llama-cpp-b11146/llama-b11146"
F="$HOME/models/2026-09-26/Laguna-XS-2.1-Q4_K_M.gguf"
export AMD_VULKAN_ICD=RADV VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json
HOST=$(hostname)
red(){ sed -e "s#$HOME#~#g" -e "s#$HOST#<host>#g"; }
log(){ echo "$(date -Iseconds) $*" | tee -a "$LOG"; }
P2="Write a Python function is_prime(n) that returns True if n is a prime number and False otherwise. Reply with only the code."
for r in 1 2; do
  tag="laguna-xs21-q4km-smoke-code-n4096-run$r"
  log "START $tag"
  echo "$BIN/llama-completion -m $F -ngl 999 -fa 1 -c 8192 -n 4096 --temp 0 --top-k 1 --seed 42 --jinja -st -p \"$P2\"" | red > "$OUT/$tag.command.txt"
  timeout 900 "$BIN/llama-completion" -m "$F" -ngl 999 -fa 1 -c 8192 -n 4096 --temp 0 --top-k 1 --seed 42 --jinja -st -p "$P2" \
     < /dev/null 2> >(red > "$OUT/$tag.stderr.log") | red > "$OUT/$tag.out.txt"
  log "END $tag rc=${PIPESTATUS[0]}"
  sleep 5
done
