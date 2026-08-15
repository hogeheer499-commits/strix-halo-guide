#!/usr/bin/env bash
set -euo pipefail

MODEL="qwen3.8:27b"
OUT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT='Write a detailed technical explanation of how unified memory helps a local AI workstation run models larger than a conventional discrete GPU can hold. Continue until the output limit is reached.'

run_once() {
    local label="$1"
    curl --fail --silent --show-error http://127.0.0.1:11434/api/generate \
        -H 'Content-Type: application/json' \
        -d "$(jq -n \
            --arg model "$MODEL" \
            --arg prompt "$PROMPT" \
            '{model:$model,prompt:$prompt,stream:false,think:false,options:{temperature:0,seed:42,num_predict:128,num_ctx:4096}}')" \
        > "$OUT_DIR/${label}.json"
}

ollama stop "$MODEL" >/dev/null 2>&1 || true
sleep 3
run_once cold
for repeat in $(seq -w 1 9); do
    sleep 2
    run_once "warm_${repeat}"
done

printf '%s\n' 'run,prompt_tokens,prompt_seconds,prompt_tps,generated_tokens,generation_seconds,generation_tps,load_seconds,total_seconds' > "$OUT_DIR/results.csv"
for result in "$OUT_DIR"/cold.json "$OUT_DIR"/warm_[0-9].json; do
    run="$(basename "$result" .json)"
    jq -r --arg run "$run" '
        [$run,
         .prompt_eval_count,
         (.prompt_eval_duration / 1e9),
         (.prompt_eval_count / (.prompt_eval_duration / 1e9)),
         .eval_count,
         (.eval_duration / 1e9),
         (.eval_count / (.eval_duration / 1e9)),
         (.load_duration / 1e9),
         (.total_duration / 1e9)]
        | @csv
    ' "$result" >> "$OUT_DIR/results.csv"
done

jq -s '
    map({
        prompt_tokens: .prompt_eval_count,
        prompt_tps: (.prompt_eval_count / (.prompt_eval_duration / 1e9)),
        generated_tokens: .eval_count,
        generation_tps: (.eval_count / (.eval_duration / 1e9))
    })
' "$OUT_DIR"/warm_[0-9].json > "$OUT_DIR/warm_results.json"
