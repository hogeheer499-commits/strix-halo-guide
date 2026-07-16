#!/usr/bin/env bash
set -euo pipefail

OUT_DIR=${OUT_DIR:-$(cd "$(dirname "$0")" && pwd)}
MODEL=${MODEL:-/home/hoge-heer/benchmark-models/2026-07-16/omni-nvfp4/nemotron-3-30b-NVFP4.gguf}
MMPROJ=${MMPROJ:-/home/hoge-heer/benchmark-models/2026-07-16/omni-nvfp4/mmproj-nemotron-3-30b-f16.gguf}
BIN_DIR=${BIN_DIR:-/home/hoge-heer/benchmark-tools/llama-b10034/llama-b10034}
IMAGE=${IMAGE:-$OUT_DIR/vision-test.png}

mkdir -p "$OUT_DIR"

sha256sum "$MODEL" > "$OUT_DIR/model.sha256"
sha256sum "$MMPROJ" > "$OUT_DIR/mmproj.sha256"
"$BIN_DIR/llama-bench" --list-devices > "$OUT_DIR/llama-version.txt" 2>&1

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

printf '%q ' "$BIN_DIR/llama-mtmd-cli" -m "$MODEL" -mm "$MMPROJ" --image "$IMAGE" \
    -p 'Read the large black text in this image. Reply with only that text.' \
    -ngl 999 --mmproj-offload -c 4096 -n 128 --temp 0 \
    > "$OUT_DIR/vision-command.txt"
printf '\n' >> "$OUT_DIR/vision-command.txt"
"$BIN_DIR/llama-mtmd-cli" -m "$MODEL" -mm "$MMPROJ" --image "$IMAGE" \
    -p 'Read the large black text in this image. Reply with only that text.' \
    -ngl 999 --mmproj-offload -c 4096 -n 128 --temp 0 \
    > "$OUT_DIR/vision-output.txt" 2> "$OUT_DIR/vision-stderr.txt"
