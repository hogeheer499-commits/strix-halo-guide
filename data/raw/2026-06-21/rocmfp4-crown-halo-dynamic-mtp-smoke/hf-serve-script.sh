#!/usr/bin/env bash
set -euo pipefail

model_dir="/srv/llm/models/Qwen3.6-35B-A3B-HaloStrix-Dyn-MTP-v7-GGUF"
llama_root="${LLAMA_ROOT:-/home/crown/tmp/llama-cpp-qwen-mtp-pr22673}"
server="${llama_root}/build-vulkan/bin/llama-server"
model="${MODEL:-${model_dir}/Qwen3.6-35B-A3B-HaloStrix-Dyn-MTP-v7.gguf}"
mmproj="${MMPROJ:-${model_dir}/mmproj-F16.mmproj}"
port="${PORT:-18181}"
ctx="${CTX:-131072}"

exec "${server}" \
  -m "${model}" \
  --alias crown-dynamic-mtp \
  --host 127.0.0.1 \
  --port "${port}" \
  --jinja \
  -c "${ctx}" \
  --reasoning off \
  --reasoning-format none \
  --reasoning-budget -1 \
  --no-context-shift \
  -sm row \
  -ngl 999 \
  -fa on \
  -b 2048 \
  -ub 512 \
  -t 16 \
  -ctk f16 \
  -ctv f16 \
  -ctkd f16 \
  -ctvd f16 \
  --parallel 1 \
  --metrics \
  --mmproj "${mmproj}" \
  --spec-type mtp \
  --spec-draft-n-max 4 \
  --poll 100 \
  --poll-batch 1 \
  --spec-draft-poll 1 \
  --spec-draft-poll-batch 1 \
  --temp 0.6 \
  --min-p 0.0 \
  --top-p 0.95 \
  --top-k 20 \
  --repeat-penalty 1.0
