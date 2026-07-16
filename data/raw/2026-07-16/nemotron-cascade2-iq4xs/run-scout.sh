#!/usr/bin/env bash
set -euo pipefail

OUT_DIR=${OUT_DIR:-$(cd "$(dirname "$0")" && pwd)}
MODEL=${MODEL:-/home/hoge-heer/benchmark-models/2026-07-16/cascade2/nvidia_Nemotron-Cascade-2-30B-A3B-IQ4_XS.gguf}
BIN_DIR=${BIN_DIR:-/home/hoge-heer/benchmark-tools/llama-b10034/llama-b10034}

mkdir -p "$OUT_DIR"

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

printf '%q ' "$BIN_DIR/llama-bench" -m "$MODEL" -ngl 999 -fa on -mmp 0 -p 512 -n 128 -r 3 -o csv \
    > "$OUT_DIR/bench-command.txt"
printf '\n' >> "$OUT_DIR/bench-command.txt"

"$BIN_DIR/llama-bench" -m "$MODEL" -ngl 999 -fa on -mmp 0 -p 512 -n 128 -r 3 -o csv \
    > "$OUT_DIR/llama-bench.csv" 2> "$OUT_DIR/llama-bench.stderr.txt"

system=$'You are a helpful and harmless assistant.\n\nYou are not allowed to use any tools'
question='A farmer has 17 sheep. All but 9 run away. How many sheep remain? Give the final answer clearly.'
thinking_prompt="<|im_start|>system
${system}<|im_end|>
<|im_start|>user
${question}<|im_end|>
<|im_start|>assistant
<think>
"
instruct_prompt="<|im_start|>system
${system}<|im_end|>
<|im_start|>user
${question}<|im_end|>
<|im_start|>assistant
<think></think>"

printf '%q ' "$BIN_DIR/llama-cli" -m "$MODEL" -ngl 999 -fa on --no-mmap -c 4096 -n 512 --temp 0 --single-turn --simple-io --no-display-prompt -p "$thinking_prompt" \
    > "$OUT_DIR/thinking-command.txt"
printf '\n' >> "$OUT_DIR/thinking-command.txt"
"$BIN_DIR/llama-cli" -m "$MODEL" -ngl 999 -fa on --no-mmap -c 4096 -n 512 --temp 0 --single-turn --simple-io --no-display-prompt -p "$thinking_prompt" \
    > "$OUT_DIR/thinking-output.txt" 2> "$OUT_DIR/thinking-stderr.txt"

printf '%q ' "$BIN_DIR/llama-cli" -m "$MODEL" -ngl 999 -fa on --no-mmap -c 4096 -n 128 --temp 0 --single-turn --simple-io --no-display-prompt -p "$instruct_prompt" \
    > "$OUT_DIR/instruct-command.txt"
printf '\n' >> "$OUT_DIR/instruct-command.txt"
"$BIN_DIR/llama-cli" -m "$MODEL" -ngl 999 -fa on --no-mmap -c 4096 -n 128 --temp 0 --single-turn --simple-io --no-display-prompt -p "$instruct_prompt" \
    > "$OUT_DIR/instruct-output.txt" 2> "$OUT_DIR/instruct-stderr.txt"
