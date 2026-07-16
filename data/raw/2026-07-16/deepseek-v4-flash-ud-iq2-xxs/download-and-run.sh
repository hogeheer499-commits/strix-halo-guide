#!/usr/bin/env bash
set -euo pipefail

REPO=${REPO:-unsloth/DeepSeek-V4-Flash-GGUF}
REVISION=${REVISION:-e3aa0d6a5fa4f820d9e132ac1fd1d01e1b2b49e0}
MODEL_DIR=${MODEL_DIR:-/home/hoge-heer/benchmark-models/2026-07-16/deepseek-v4-flash}
OUT_DIR=${OUT_DIR:-$(cd "$(dirname "$0")" && pwd)}
export HF_XET_HIGH_PERFORMANCE=${HF_XET_HIGH_PERFORMANCE:-1}

mkdir -p "$MODEL_DIR" "$OUT_DIR"

printf 'repo=%s\nrevision=%s\n' "$REPO" "$REVISION" \
    > "$OUT_DIR/source-revision.txt"

hf download "$REPO" \
    --revision "$REVISION" \
    --include 'UD-IQ2_XXS/*.gguf' \
    --local-dir "$MODEL_DIR" \
    2>&1 | tee "$OUT_DIR/download.txt"

MODEL="$MODEL_DIR/UD-IQ2_XXS/DeepSeek-V4-Flash-UD-IQ2_XXS-00001-of-00003.gguf" \
    OUT_DIR="$OUT_DIR" \
    "$OUT_DIR/run-scout.sh"
