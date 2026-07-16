#!/usr/bin/env bash
set -euo pipefail

OUT_DIR=${OUT_DIR:-$(cd "$(dirname "$0")" && pwd)}
MODEL=${MODEL:-/home/hoge-heer/benchmark-models/2026-07-16/agentworld/Qwen-AgentWorld-35B-A3B-UD-IQ4_XS.gguf}
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

system='You are a language world model simulating a Linux terminal environment. Given the user command, predict the terminal output.'
action=$'Action: execute_bash\nCommand: echo agentworld-ok'
prompt="<|im_start|>system
${system}<|im_end|>
<|im_start|>user
${action}<|im_end|>
<|im_start|>assistant
<think>
"

common=(
    -m "$MODEL"
    -ngl 999
    -fa on
    --no-mmap
    --single-turn
    --simple-io
    --no-display-prompt
    --temp 0.6
    --top-p 0.95
    --top-k 20
    -p "$prompt"
)

printf '%q ' "$BIN_DIR/llama-cli" "${common[@]}" -c 4096 -n 512 \
    > "$OUT_DIR/terminal-smoke-command.txt"
printf '\n' >> "$OUT_DIR/terminal-smoke-command.txt"
"$BIN_DIR/llama-cli" "${common[@]}" -c 4096 -n 512 \
    > "$OUT_DIR/terminal-smoke-output.txt" 2> "$OUT_DIR/terminal-smoke-stderr.txt"

printf '%q ' /usr/bin/time -v "$BIN_DIR/llama-cli" "${common[@]}" -c 131072 -ctk q8_0 -ctv q8_0 -n 64 \
    > "$OUT_DIR/context-128k-command.txt"
printf '\n' >> "$OUT_DIR/context-128k-command.txt"
/usr/bin/time -v "$BIN_DIR/llama-cli" "${common[@]}" -c 131072 -ctk q8_0 -ctv q8_0 -n 64 \
    > "$OUT_DIR/context-128k-output.txt" 2> "$OUT_DIR/context-128k-stderr.txt"
