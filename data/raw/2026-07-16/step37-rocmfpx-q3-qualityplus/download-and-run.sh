#!/usr/bin/env bash
set -euo pipefail

OUT_DIR=$(cd "$(dirname "$0")" && pwd)
MODEL_ROOT=/home/hoge-heer/benchmark-models/2026-07-16/step37
TARGET_REPO=jcbtc/Step-3.7-Flash-ROCmFPX-Q3-QualityPlus
TARGET_REV=fa311ca5a82bf82a2338151c4790e3f659abd88d
DRAFT_REPO=notSnix/Step-3.7-Flash-MTP-Draft-GGUF
DRAFT_REV=c7bc8526b2b7004ce045112edebdf13a9eceb7eb

if [[ -n ${WAIT_PID:-} ]]; then
    while kill -0 "$WAIT_PID" 2>/dev/null; do
        sleep 30
    done
fi

mkdir -p "$MODEL_ROOT/target" "$MODEL_ROOT/draft"

hf download "$TARGET_REPO" \
    --revision "$TARGET_REV" \
    --include 'Step-3.7-Flash-ROCmFPX-Q3-QualityPlus-*.gguf' \
    --include 'step37-native-tool-response-template.jinja' \
    --include 'README.md' \
    --local-dir "$MODEL_ROOT/target" \
    > "$OUT_DIR/target-download.txt"

hf download "$DRAFT_REPO" \
    --revision "$DRAFT_REV" \
    --include 'Step-3.7-Flash-MTP-Q8_0.gguf' \
    --include 'README.md' \
    --local-dir "$MODEL_ROOT/draft" \
    > "$OUT_DIR/draft-download.txt"

{
    printf 'target_repo=%s\n' "$TARGET_REPO"
    printf 'target_revision=%s\n' "$TARGET_REV"
    printf 'draft_repo=%s\n' "$DRAFT_REPO"
    printf 'draft_revision=%s\n' "$DRAFT_REV"
    git -C /home/hoge-heer/ROCmFPX-ciru rev-parse HEAD
} > "$OUT_DIR/source-revisions.txt"

sha256sum "$MODEL_ROOT"/target/*.gguf > "$OUT_DIR/target-shards.sha256"
sha256sum "$MODEL_ROOT"/draft/*.gguf > "$OUT_DIR/draft.sha256"
sha256sum "$MODEL_ROOT/target/step37-native-tool-response-template.jinja" \
    > "$OUT_DIR/template.sha256"

{
    date -Is
    uname -a
    lscpu | sed -n '1,30p'
    free -h
    df -h /home/hoge-heer
    vulkaninfo --summary 2>/dev/null | sed -n '1,100p' || true
    distrobox enter vllm-gfx1151 -- /opt/rocm/bin/hipcc --version 2>/dev/null || true
} > "$OUT_DIR/host-snapshot.txt"

distrobox enter vllm-gfx1151 -- bash -lc \
    '/home/hoge-heer/ROCmFPX-ciru/build-strix-rocmfp4/bin/llama-server --version' \
    > "$OUT_DIR/llama-server-version.txt" 2>&1

python3 "$OUT_DIR/run-repro.py" > "$OUT_DIR/run-repro.stdout.txt" 2>&1
