#!/usr/bin/env bash
set -euo pipefail

MODEL="qwen3.8:27b"
API="http://127.0.0.1:11434"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="$ROOT_DIR/qualification"
mkdir -p "$OUT_DIR"

api_chat() {
    local request="$1"
    local response="$2"

    timeout 900 curl --fail --silent --show-error \
        "$API/api/chat" \
        -H 'Content-Type: application/json' \
        --data-binary "@$request" \
        > "$response"
}

run_tools() {
    local request="$OUT_DIR/tool_request.json"
    local response="$OUT_DIR/tool_response.json"
    local followup_request="$OUT_DIR/tool_followup_request.json"
    local followup_response="$OUT_DIR/tool_followup_response.json"

    jq -n '
        {
            model: "qwen3.8:27b",
            stream: false,
            think: false,
            messages: [{
                role: "user",
                content: "Use the multiply tool to calculate 37 times 19. Do not calculate it yourself."
            }],
            tools: [{
                type: "function",
                function: {
                    name: "multiply",
                    description: "Multiply two integers",
                    parameters: {
                        type: "object",
                        required: ["a", "b"],
                        properties: {
                            a: {type: "integer"},
                            b: {type: "integer"}
                        }
                    }
                }
            }],
            options: {
                temperature: 0,
                seed: 42,
                num_ctx: 4096,
                num_predict: 128
            }
        }
    ' > "$request"
    api_chat "$request" "$response"

    jq -n --slurpfile first "$response" '
        {
            model: "qwen3.8:27b",
            stream: false,
            think: false,
            messages: [
                {
                    role: "user",
                    content: "Use the multiply tool to calculate 37 times 19. Do not calculate it yourself."
                },
                $first[0].message,
                {
                    role: "tool",
                    tool_name: "multiply",
                    content: "703"
                }
            ],
            tools: [{
                type: "function",
                function: {
                    name: "multiply",
                    description: "Multiply two integers",
                    parameters: {
                        type: "object",
                        required: ["a", "b"],
                        properties: {
                            a: {type: "integer"},
                            b: {type: "integer"}
                        }
                    }
                }
            }],
            options: {
                temperature: 0,
                seed: 42,
                num_ctx: 4096,
                num_predict: 128
            }
        }
    ' > "$followup_request"
    api_chat "$followup_request" "$followup_response"

    jq -n --slurpfile first "$response" --slurpfile second "$followup_response" '
        {
            tool_call_pass: (
                $first[0].message.tool_calls[0].function.name == "multiply" and
                $first[0].message.tool_calls[0].function.arguments.a == 37 and
                $first[0].message.tool_calls[0].function.arguments.b == 19
            ),
            followup_pass: ($second[0].message.content | contains("703")),
            called_function: $first[0].message.tool_calls[0].function.name,
            arguments: $first[0].message.tool_calls[0].function.arguments,
            final_content: $second[0].message.content
        }
    ' > "$OUT_DIR/tool_summary.json"
}

run_thinking() {
    local request="$OUT_DIR/thinking_request.json"
    local response="$OUT_DIR/thinking_response.json"

    jq -n '
        {
            model: "qwen3.8:27b",
            stream: false,
            think: true,
            messages: [{
                role: "user",
                content: "A box contains 3 red balls and 2 blue balls. Two balls are drawn without replacement. What is the probability both are red? Give the final answer as a simplified fraction."
            }],
            options: {
                temperature: 0,
                seed: 42,
                num_ctx: 4096,
                num_predict: 512
            }
        }
    ' > "$request"
    api_chat "$request" "$response"

    jq '
        {
            thinking_present: ((.message.thinking // "") | length > 0),
            answer_pass: (
                (.message.content | contains("3/10")) or
                (.message.content | contains("\\frac{3}{10}"))
            ),
            thinking: .message.thinking,
            final_content: .message.content,
            prompt_eval_count,
            eval_count,
            prompt_tps: (.prompt_eval_count / (.prompt_eval_duration / 1e9)),
            generation_tps: (.eval_count / (.eval_duration / 1e9))
        }
    ' "$response" > "$OUT_DIR/thinking_summary.json"
}

generate_context_prompt() {
    local filler_tokens="$1"
    local code="$2"

    python3 - "$filler_tokens" "$code" <<'PY'
import sys

filler_tokens = int(sys.argv[1])
code = sys.argv[2]
before = filler_tokens * 2 // 3
after = filler_tokens - before

print("Read the complete document and remember the one access code.\n")
print(" alpha" * before)
print(f"\nACCESS_CODE={code}\n")
print(" beta" * after)
print("\nWhat is the access code? Return the code exactly and nothing else.")
PY
}

run_context() {
    local label="$1"
    local num_ctx="$2"
    local filler_tokens="$3"
    local code="QWEN38-${label}-PASS"
    local prompt_file="/tmp/qwen38-${label}-prompt.txt"
    local request_file="/tmp/qwen38-${label}-request.json"
    local raw_response="/tmp/qwen38-${label}-raw-response.json"
    local response="$OUT_DIR/context_${label}.json"

    generate_context_prompt "$filler_tokens" "$code" > "$prompt_file"
    jq -n \
        --arg model "$MODEL" \
        --rawfile prompt "$prompt_file" \
        --argjson num_ctx "$num_ctx" \
        '{
            model: $model,
            messages: [{role: "user", content: $prompt}],
            stream: false,
            think: false,
            keep_alive: "15m",
            options: {
                temperature: 0,
                seed: 42,
                num_ctx: $num_ctx,
                num_predict: 32
            }
        }' > "$request_file"

    free -b > "$OUT_DIR/context_${label}_memory_before.txt"
    ollama ps > "$OUT_DIR/context_${label}_ollama_before.txt"
    /usr/bin/time -v -o "$OUT_DIR/context_${label}_client_time.txt" \
        timeout 2400 curl --fail --silent --show-error \
            "$API/api/chat" \
            -H 'Content-Type: application/json' \
            --data-binary "@$request_file" \
            > "$raw_response"
    jq 'del(.context)' "$raw_response" > "$response"
    free -b > "$OUT_DIR/context_${label}_memory_after.txt"
    ollama ps > "$OUT_DIR/context_${label}_ollama_after.txt"

    jq -n \
        --arg label "$label" \
        --arg code "$code" \
        --argjson num_ctx "$num_ctx" \
        --argjson filler_tokens "$filler_tokens" \
        --slurpfile result "$response" \
        '{
            label: $label,
            configured_context: $num_ctx,
            generated_filler_tokens: $filler_tokens,
            run_complete: ($result[0].done == true and $result[0].prompt_eval_count != null),
            prompt_eval_count: $result[0].prompt_eval_count,
            eval_count: $result[0].eval_count,
            retrieval_pass: (
                $result[0].done == true and
                (($result[0].message.content // "") | contains($code))
            ),
            expected_code: $code,
            response: ($result[0].message.content // ""),
            api_error: ($result[0].error // null),
            load_seconds: (
                if $result[0].load_duration != null then $result[0].load_duration / 1e9 else null end
            ),
            prompt_seconds: (
                if $result[0].prompt_eval_duration != null then $result[0].prompt_eval_duration / 1e9 else null end
            ),
            prompt_tps: (
                if $result[0].prompt_eval_count != null and $result[0].prompt_eval_duration > 0
                then $result[0].prompt_eval_count / ($result[0].prompt_eval_duration / 1e9)
                else null end
            ),
            generation_seconds: (
                if $result[0].eval_duration != null then $result[0].eval_duration / 1e9 else null end
            ),
            generation_tps: (
                if $result[0].eval_count != null and $result[0].eval_duration > 0
                then $result[0].eval_count / ($result[0].eval_duration / 1e9)
                else null end
            ),
            total_seconds: (
                if $result[0].total_duration != null then $result[0].total_duration / 1e9 else null end
            )
        }
    ' > "$OUT_DIR/context_${label}_summary.json"
}

summarize_contexts() {
    printf '%s\n' 'label,configured_context,run_complete,prompt_tokens,retrieval_pass,prompt_tps,generation_tps,load_seconds,total_seconds' \
        > "$OUT_DIR/context_results.csv"
    for summary in "$OUT_DIR"/context_*_summary.json; do
        jq -r '
            [
                .label,
                .configured_context,
                .run_complete,
                .prompt_eval_count,
                .retrieval_pass,
                .prompt_tps,
                .generation_tps,
                .load_seconds,
                .total_seconds
            ] | @csv
        ' "$summary" >> "$OUT_DIR/context_results.csv"
    done
}

case "${1:-all}" in
    tools)
        run_tools
        ;;
    thinking)
        run_thinking
        ;;
    context)
        run_context "$2" "$3" "$4"
        summarize_contexts
        ;;
    summarize)
        summarize_contexts
        ;;
    all)
        run_tools
        run_thinking
        run_context 16k 16384 14000
        summarize_contexts
        ;;
    *)
        printf 'Usage: %s [all|tools|thinking|context LABEL NUM_CTX FILLER_TOKENS|summarize]\n' "$0" >&2
        exit 2
        ;;
esac
