# Qwen3.8 27B Ollama 0.32.13 Vulkan/RADV Evidence

Status: first-party measured local buyer-route evidence.

This run qualifies the official dense Qwen3.8 27B Ollama artifact as a practical chat, image, tool-call, thinking, and medium-context route on one 128GB Strix Halo system. It is not a direct `llama-bench` result or a broad model-quality benchmark.

## Tested Stack

- System: Beelink GTR9 Pro
- Processor/GPU: AMD Ryzen AI MAX+ 395 / Radeon 8060S (`gfx1151`)
- Memory: 128GB unified LPDDR5X-8000
- Kernel: `7.0.0-28-generic`
- Graphics stack: Mesa `26.1.6` from kisak-mesa, Vulkan/RADV
- Runtime: Ollama `0.32.13` system service
- Model: official `qwen3.8:27b`
- Architecture: `qwen35`, 27.3B dense parameters
- Quantization: `Q4_K_M`
- Artifact size: 17,741,872,154 bytes (17.7 GB decimal / about 16.5 GiB)
- Reported model context limit: 262,144 tokens
- Verified exact retrieval: through 50,059 prompt tokens with a 65,536-token runtime allocation

The host service retained `OLLAMA_IGPU_ENABLE=1` and `OLLAMA_VULKAN=1`. `ollama ps` reported the loaded model as `100% GPU`.

## Text Benchmark Method

The script called Ollama's non-streaming `/api/generate` endpoint with:

- `think=false`
- `temperature=0`
- `seed=42`
- `num_predict=128`
- `num_ctx=4096`
- one 45-token technical prompt
- one cold load followed by nine warm repeats

The exact prompt, options, extraction logic, and raw responses are preserved in [`benchmark.sh`](benchmark.sh), [`cold.json`](cold.json), and `warm_*.json`.

| Measurement | Prompt processing | Generation | Load time |
| --- | ---: | ---: | ---: |
| Cold load | 103.90 t/s | 21.02 t/s | 6.38 s |
| Nine-repeat warm mean | 292.49 t/s | 20.42 t/s | cached |
| Warm range | 290.46-295.36 t/s | 19.85-20.79 t/s | cached |

Every warm repeat evaluated 45 prompt tokens and generated 128 output tokens. The aggregate calculation is in [`warm_results.json`](warm_results.json), and the compact row set is in [`results.csv`](results.csv).

## Vision Smoke

The official artifact exposes vision capability. A deterministic `/api/chat` request asked the model to read the main title and largest benchmark number in [`vision-input-social-preview.png`](vision-input-social-preview.png). It answered:

> The main title is "AMD Strix Halo Local LLM Guide," and the largest benchmark number is 140.4 t/s.

That matches the supplied image. The raw request/response is preserved in [`vision_smoke.json`](vision_smoke.json). This is one functional image-text check, not a broad vision benchmark.

## Tools And Thinking

The `/api/chat` tool-call test asked the model to multiply 37 by 19 through a declared `multiply` function. The model selected the right function and arguments, and its follow-up answer returned `703`. A separate thinking request exposed a non-empty reasoning field and answered the held-out probability question with the exact simplified result `3/10`.

These are functional protocol checks, not agent or reasoning benchmarks. The exact requests, responses, and summaries are under [`qualification/`](qualification/).

## Context Qualification

The context harness placed a unique retrieval code before deterministic filler and asked the model to return only that code. Successful rows used the non-streaming `/api/chat` endpoint except for the separately noted `/api/generate` compatibility check.

| Runtime allocation | Evaluated prompt | Result | Prompt processing | Generation |
| ---: | ---: | --- | ---: | ---: |
| 16,384 | 14,055 tokens | exact retrieval pass | 259.97 t/s | 30.54 t/s |
| 32,768 | 28,056 tokens | exact retrieval pass | 190.53 t/s | 30.34 t/s |
| 65,536 | 28,059 tokens | exact retrieval pass | 180.05 t/s | 37.03 t/s |
| 65,536 | 42,059 tokens | exact retrieval pass | 132.16 t/s | 34.58 t/s |
| 65,536 | 50,059 tokens | exact retrieval pass | 113.56 t/s | 32.88 t/s |
| 65,536 | 56,051 tokens last logged | **failed: Vulkan device lost** | n/a | n/a |

The 56K attempt ended after 538.12 seconds with RADV reporting a cancelled command stream and `ggml_vulkan` reporting `ErrorDeviceLost`. Ollama returned `done=false`. Unloading and reloading the model restored a normal short chat response, recorded in [`post_device_loss_smoke.json`](qualification/post_device_loss_smoke.json).

This establishes a measured boundary for this exact Ollama 0.32.13 / Mesa 26.1.6 / Vulkan-RADV / Beelink stack. It is not evidence that 56K is a universal Qwen3.8, Ollama, or Strix Halo limit. The artifact advertises 262K context, but this run does not validate that claim locally.

One 28K `/api/generate` request produced the correct retrieval text and complete timing data, but its very large returned context-token array left malformed JSON in the captured body. The equivalent `/api/chat` row was valid. Use `/api/chat` for the published long-context path.

## Scope And Caveats

- This is an Ollama API/server result, not direct `llama-bench` evidence.
- Exact retrieval passed through 50,059 prompt tokens; a 56,051-token attempt caused a recoverable Vulkan device-loss on this stack.
- The advertised 262K context was not qualified.
- Tool use and thinking protocol behavior passed one deterministic smoke each; agent quality and broad reasoning quality were not benchmarked.
- Broad text quality, coding quality, and visual reasoning were not benchmarked.
- The separate official `Qwen3.8-2.4T-A95B` is a much larger frontier model and remains outside a one-box 128GB route.
- Ollama was upgraded because this artifact requires version `0.32.12` or newer. The previous `0.31.2` binary and library directory were retained locally as rollback artifacts.

## Evidence Map

- [`host_snapshot.txt`](host_snapshot.txt): measured host/runtime summary
- [`ollama-show.txt`](ollama-show.txt): model metadata and capabilities
- [`ollama-tag-qwen38-27b.json`](ollama-tag-qwen38-27b.json): local tag metadata
- [`ollama-ps.txt`](ollama-ps.txt): loaded-model GPU placement
- [`ollama-version.txt`](ollama-version.txt): runtime version
- [`ollama-service-unit.txt`](ollama-service-unit.txt): system service definition
- [`ollama-service-properties.txt`](ollama-service-properties.txt): relevant service properties
- [`benchmark.sh`](benchmark.sh): exact benchmark procedure
- [`results.csv`](results.csv): cold and warm rows
- [`warm_results.json`](warm_results.json): calculated warm summary
- [`vision_smoke.json`](vision_smoke.json): image-text request and response
- [`qualification.sh`](qualification.sh): exact tool, thinking, and context harness
- [`qualification/context_results.csv`](qualification/context_results.csv): context qualification summary
- [`qualification/tool_summary.json`](qualification/tool_summary.json): tool-call and follow-up result
- [`qualification/thinking_summary.json`](qualification/thinking_summary.json): thinking-field and answer result
- [`qualification/context_64k_ollama_journal.log`](qualification/context_64k_ollama_journal.log): device-loss service log
- [`qualification/post_device_loss_smoke.json`](qualification/post_device_loss_smoke.json): successful runner-recovery check
