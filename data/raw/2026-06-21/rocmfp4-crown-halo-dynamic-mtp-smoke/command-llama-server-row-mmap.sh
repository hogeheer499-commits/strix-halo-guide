#!/usr/bin/env bash
set -euo pipefail
MODEL=/home/hoge-heer/benchmark-models/rocmfp4-chadrock/qwen36-35b-crown-halo-dyn/Qwen3.6-35B-A3B-HaloStrix-Dyn-MTP-v7.gguf
BIN=/home/hoge-heer/rocmfp4-llama/build-strix-rocmfp4-hiponly/bin/llama-server
export HSA_OVERRIDE_GFX_VERSION=11.5.1
exec "$BIN" \
  -m "$MODEL" \
  --alias crown-dynamic-mtp-beelink-row-mmap \
  --host 127.0.0.1 \
  --port 18182 \
  --jinja \
  -c 16384 \
  --reasoning off \
  --reasoning-format none \
  --reasoning-budget -1 \
  --no-context-shift \
  -sm row \
  -dev ROCm0 \
  --spec-draft-device ROCm0 \
  -ngl 999 \
  -fa on \
  -b 2048 \
  -ub 512 \
  -t 16 \
  -tb 32 \
  -ctk f16 \
  -ctv f16 \
  -ctkd f16 \
  -ctvd f16 \
  --parallel 1 \
  --metrics \
  --spec-type draft-mtp \
  --spec-draft-ngl all \
  --spec-draft-n-max 4 \
  --spec-draft-n-min 0 \
  --spec-draft-p-min 0.0 \
  --spec-draft-p-split 0.10 \
  --poll 100 \
  --poll-batch 1 \
  --spec-draft-poll 1 \
  --spec-draft-poll-batch 1 \
  --temp 0.6 \
  --min-p 0.0 \
  --top-p 0.95 \
  --top-k 20 \
  --repeat-penalty 1.0
