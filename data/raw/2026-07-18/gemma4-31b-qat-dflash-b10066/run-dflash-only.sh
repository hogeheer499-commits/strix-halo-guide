#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="${BIN:-/home/hoge-heer/benchmark-tools/llama-b10066-vulkan/llama-b10066}"
MODEL_DIR="${MODEL_DIR:-/home/hoge-heer/benchmark-models/gemma-4-31b-qat-dflash}"
MODEL="$MODEL_DIR/gemma-4-31B-it-Q4_0.gguf"
DRAFT="$MODEL_DIR/dflash-gemma-4-31B-it-Q8_0.gguf"
PORT="${PORT:-18131}"

for path in "$BIN/llama-server" "$MODEL" "$DRAFT"; do
  [[ -e "$path" ]] || { echo "missing required path: $path" >&2; exit 1; }
done

rm -f \
  "$ROOT/dflash.jsonl" \
  "$ROOT/dflash.tool-smoke.json" \
  "$ROOT/dflash.server.log" \
  "$ROOT/dflash.start.exit-code.txt" \
  "$ROOT/dflash.tests.exit-code.txt"

stop_server() {
  if [[ -n "${SERVER_PID:-}" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
}
trap stop_server EXIT

"$BIN/llama-server" -m "$MODEL" -ngl 999 -fa on --jinja --reasoning off \
  -c 32768 -np 1 --host 127.0.0.1 --port "$PORT" --metrics \
  --alias gemma4-31b-dflash \
  --spec-draft-model "$DRAFT" \
  --spec-type draft-dflash \
  --spec-draft-n-max 8 \
  --spec-draft-n-min 0 \
  --spec-draft-p-min 0 \
  > "$ROOT/dflash.server.log" 2>&1 &
SERVER_PID=$!

for _ in $(seq 1 180); do
  if curl -fsS "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
    printf '0\n' > "$ROOT/dflash.start.exit-code.txt"
    break
  fi
  if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    printf '1\n' > "$ROOT/dflash.start.exit-code.txt"
    tail -100 "$ROOT/dflash.server.log" >&2
    exit 1
  fi
  sleep 1
done

[[ -e "$ROOT/dflash.start.exit-code.txt" ]] || {
  printf '1\n' > "$ROOT/dflash.start.exit-code.txt"
  echo "DFlash server did not become healthy" >&2
  exit 1
}

set +e
python3 "$ROOT/run-server-tests.py" \
  --base-url "http://127.0.0.1:$PORT" \
  --model gemma4-31b-dflash \
  --profile dflash \
  --out "$ROOT"
printf '%s\n' "$?" > "$ROOT/dflash.tests.exit-code.txt"
set -e

stop_server
echo "Gemma 4 31B DFlash-only rerun completed: $ROOT"
