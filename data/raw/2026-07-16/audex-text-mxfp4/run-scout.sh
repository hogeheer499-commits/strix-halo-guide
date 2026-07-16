#!/usr/bin/env bash
set -euo pipefail

OUT_DIR=${OUT_DIR:-$(cd "$(dirname "$0")" && pwd)}
MODEL=${MODEL:-/home/hoge-heer/benchmark-models/2026-07-16/audex/quants/audex-30b-a3b-textonly-MXFP4_MOE.gguf}
BIN_DIR=${BIN_DIR:-/home/hoge-heer/benchmark-tools/llama-b10034/llama-b10034}

sha256sum "$MODEL" > "$OUT_DIR/model.sha256"
"$BIN_DIR/llama-bench" --list-devices > "$OUT_DIR/llama-version.txt" 2>&1

{
    date -Is
    uname -a
    lscpu | sed -n '1,30p'
    free -h
    df -h /home/hoge-heer
    vulkaninfo --summary 2>/dev/null | sed -n '1,100p' || true
} > "$OUT_DIR/host-snapshot.txt"

printf '%q ' "$BIN_DIR/llama-bench" -m "$MODEL" -ngl 999 -fa on -mmp 0 \
    -p 512 -n 128 -r 3 -o csv > "$OUT_DIR/bench-command.txt"
printf '\n' >> "$OUT_DIR/bench-command.txt"
"$BIN_DIR/llama-bench" -m "$MODEL" -ngl 999 -fa on -mmp 0 \
    -p 512 -n 128 -r 3 -o csv \
    > "$OUT_DIR/llama-bench.csv" 2> "$OUT_DIR/llama-bench.stderr.txt"

printf '%q ' "$BIN_DIR/llama-cli" -m "$MODEL" -ngl 999 -fa on \
    -c 4096 -n 192 --temp 0 --single-turn --simple-io \
    -p 'A farmer has 12 sheep. All but 9 run away. Reply with only the number of sheep remaining.' \
    > "$OUT_DIR/text-smoke-command.txt"
printf '\n' >> "$OUT_DIR/text-smoke-command.txt"
"$BIN_DIR/llama-cli" -m "$MODEL" -ngl 999 -fa on \
    -c 4096 -n 192 --temp 0 --single-turn --simple-io \
    -p 'A farmer has 12 sheep. All but 9 run away. Reply with only the number of sheep remaining.' \
    > "$OUT_DIR/text-smoke-output.txt" 2> "$OUT_DIR/text-smoke-stderr.txt"
