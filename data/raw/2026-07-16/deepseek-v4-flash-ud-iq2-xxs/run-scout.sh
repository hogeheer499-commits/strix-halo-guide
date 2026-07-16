#!/usr/bin/env bash
set -euo pipefail

OUT_DIR=${OUT_DIR:-$(cd "$(dirname "$0")" && pwd)}
MODEL=${MODEL:-/home/hoge-heer/benchmark-models/2026-07-16/deepseek-v4-flash/UD-IQ2_XXS/DeepSeek-V4-Flash-UD-IQ2_XXS-00001-of-00003.gguf}
BIN_DIR=${BIN_DIR:-/home/hoge-heer/benchmark-tools/llama-b10034/llama-b10034}

mkdir -p "$OUT_DIR"

sha256sum "$(dirname "$MODEL")"/*.gguf > "$OUT_DIR/model-shards.sha256"
"$BIN_DIR/llama-cli" --version > "$OUT_DIR/llama-version.txt" 2>&1
"$BIN_DIR/llama-bench" --list-devices > "$OUT_DIR/llama-devices.txt" 2>&1

{
    date -Is
    uname -a
    lscpu | sed -n '1,30p'
    free -h
    df -h /home/hoge-heer
    vulkaninfo --summary 2>/dev/null | sed -n '1,100p' || true
} > "$OUT_DIR/host-snapshot.txt"

printf '%q ' "$BIN_DIR/llama-bench" -m "$MODEL" -ngl 999 -fa on -mmp 0 -p 512 -n 128 -r 3 -o csv \
    > "$OUT_DIR/bench-command.txt"
printf '\n' >> "$OUT_DIR/bench-command.txt"

"$BIN_DIR/llama-bench" -m "$MODEL" -ngl 999 -fa on -mmp 0 -p 512 -n 128 -r 3 -o csv \
    > "$OUT_DIR/llama-bench.csv" 2> "$OUT_DIR/llama-bench.stderr.txt"

prompt='Answer with only the number: if a machine has 12 drives and 3 fail, how many remain?'
common=(
    -m "$MODEL"
    -ngl 999
    -fa on
    --no-mmap
    --single-turn
    --simple-io
    --no-display-prompt
    -c 4096
    -n 256
    --temp 0
    --top-p 1
    --top-k 0
    -p "$prompt"
)

printf '%q ' "$BIN_DIR/llama-cli" "${common[@]}" > "$OUT_DIR/smoke-command.txt"
printf '\n' >> "$OUT_DIR/smoke-command.txt"
"$BIN_DIR/llama-cli" "${common[@]}" \
    > "$OUT_DIR/smoke-output.txt" 2> "$OUT_DIR/smoke-stderr.txt"
