#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="${BIN:-/home/hoge-heer/benchmark-tools/llama-b10066-vulkan/llama-b10066}"
MODEL_DIR="${MODEL_DIR:-/home/hoge-heer/benchmark-models/gemma-4-31b-qat-dflash}"
MODEL="$MODEL_DIR/gemma-4-31B-it-Q4_0.gguf"
DRAFT="$MODEL_DIR/dflash-gemma-4-31B-it-Q8_0.gguf"
MMPROJ="$MODEL_DIR/mmproj-gemma-4-31B-it-Q8_0.gguf"
IMAGE="$ROOT/vision-test.png"
PORT="${PORT:-18131}"

rm -f \
  "$ROOT"/host-snapshot.txt \
  "$ROOT"/*.sha256 \
  "$ROOT"/llama-bench.csv \
  "$ROOT"/llama-bench.stderr.txt \
  "$ROOT"/text-smoke.txt \
  "$ROOT"/text-smoke.stderr.txt \
  "$ROOT"/vision-output.txt \
  "$ROOT"/vision-stderr.txt \
  "$ROOT"/*.exit-code.txt \
  "$ROOT"/*.jsonl \
  "$ROOT"/*.tool-smoke.json \
  "$ROOT"/*.server.log

for path in "$BIN/llama-bench" "$BIN/llama-cli" "$BIN/llama-mtmd-cli" \
  "$BIN/llama-server" "$MODEL" "$DRAFT" "$MMPROJ" "$IMAGE"; do
  [[ -e "$path" ]] || { echo "missing required path: $path" >&2; exit 1; }
done

capture_host() {
  {
    date --iso-8601=seconds
    uname -a
    cat /proc/cmdline
    free -h
    "$BIN/llama-cli" --version
    vulkaninfo --summary 2>/dev/null || true
    glxinfo -B 2>/dev/null || true
  } > "$ROOT/host-snapshot.txt"

  sha256sum "$MODEL" > "$ROOT/model.sha256"
  sha256sum "$DRAFT" > "$ROOT/dflash.sha256"
  sha256sum "$MMPROJ" > "$ROOT/mmproj.sha256"
}

run_direct() {
  "$BIN/llama-bench" -m "$MODEL" -ngl 999 -fa on -mmp 0 \
    -p 512 -n 128 -r 3 -o csv \
    > "$ROOT/llama-bench.csv" 2> "$ROOT/llama-bench.stderr.txt"

  set +e
  "$BIN/llama-cli" -m "$MODEL" -ngl 999 -fa on -n 128 --temp 0 \
    --jinja --reasoning off \
    --chat-template-kwargs '{"enable_thinking":false}' \
    --no-display-prompt --simple-io --single-turn \
    -p 'Return exactly three concise bullet points explaining why unified memory helps a local AI PC.' \
    > "$ROOT/text-smoke.txt" 2> "$ROOT/text-smoke.stderr.txt"
  printf '%s\n' "$?" > "$ROOT/text-smoke.exit-code.txt"

  "$BIN/llama-mtmd-cli" -m "$MODEL" --mmproj "$MMPROJ" --image "$IMAGE" \
    -ngl 999 -fa on --jinja -n 512 --temp 0 \
    -p 'Read the large text in this image. Return only the text.' \
    > "$ROOT/vision-output.txt" 2> "$ROOT/vision-stderr.txt"
  printf '%s\n' "$?" > "$ROOT/vision.exit-code.txt"
  set -e
}

stop_server() {
  if [[ -n "${SERVER_PID:-}" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
}

start_server() {
  local server_profile="$1"
  shift
  stop_server
  "$BIN/llama-server" -m "$MODEL" -ngl 999 -fa on --jinja --reasoning off \
    -c 32768 -np 1 \
    --host 127.0.0.1 --port "$PORT" --metrics \
    --alias "gemma4-31b-$server_profile" \
    "$@" > "$ROOT/$server_profile.server.log" 2>&1 &
  SERVER_PID=$!
  for _ in $(seq 1 180); do
    curl -fsS "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 && return 0
    kill -0 "$SERVER_PID" 2>/dev/null || {
      tail -100 "$ROOT/$server_profile.server.log" >&2
      return 1
    }
    sleep 1
  done
  echo "server did not become healthy: $server_profile" >&2
  return 1
}

run_server_profile() {
  local run_profile="$1"
  shift
  if ! start_server "$run_profile" "$@"; then
    printf '%s\n' "1" > "$ROOT/$run_profile.start.exit-code.txt"
    stop_server
    return 0
  fi
  printf '%s\n' "0" > "$ROOT/$run_profile.start.exit-code.txt"
  set +e
  python3 "$ROOT/run-server-tests.py" \
    --base-url "http://127.0.0.1:$PORT" \
    --model "gemma4-31b-$run_profile" \
    --profile "$run_profile" \
    --out "$ROOT"
  printf '%s\n' "$?" > "$ROOT/$run_profile.tests.exit-code.txt"
  set -e
  stop_server
}

trap stop_server EXIT
capture_host
run_direct
run_server_profile nospec
run_server_profile dflash \
  --spec-draft-model "$DRAFT" \
  --spec-type draft-dflash \
  --spec-draft-n-max 8 \
  --spec-draft-n-min 0 \
  --spec-draft-p-min 0

echo "Gemma 4 31B QAT/DFlash scout completed: $ROOT"
