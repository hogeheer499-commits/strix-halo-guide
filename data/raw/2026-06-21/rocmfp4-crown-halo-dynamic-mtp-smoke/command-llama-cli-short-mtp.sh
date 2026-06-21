#!/usr/bin/env bash
set -euo pipefail
MODEL=/home/hoge-heer/benchmark-models/rocmfp4-chadrock/qwen36-35b-crown-halo-dyn/Qwen3.6-35B-A3B-HaloStrix-Dyn-MTP-v7.gguf
BIN=/home/hoge-heer/rocmfp4-llama/build-strix-rocmfp4-hiponly/bin/llama-cli
export HSA_OVERRIDE_GFX_VERSION=11.5.1
"$BIN" \
  -m "$MODEL" \
  -dev ROCm0 \
  --spec-draft-device ROCm0 \
  -sm none \
  -ngl 999 \
  -fa on \
  --no-mmap \
  -t 16 \
  -tb 32 \
  -ctk f16 \
  -ctv f16 \
  -ctkd f16 \
  -ctvd f16 \
  -c 4096 \
  -b 2048 \
  -ub 512 \
  --temp 0.6 \
  --min-p 0.0 \
  --top-p 0.95 \
  --top-k 20 \
  --repeat-penalty 1.0 \
  --seed 123 \
  --no-display-prompt \
  --simple-io \
  --no-warmup \
  -st \
  -cnv \
  --jinja \
  --reasoning off \
  --reasoning-format none \
  --reasoning-budget -1 \
  --no-context-shift \
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
  -n 128 \
  -p 'Write a compact JSON object with eight short keys describing why reproducible local AI benchmarks matter for AMD Strix Halo buyers.'
