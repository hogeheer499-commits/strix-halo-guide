# Qwen3.8 27B Ollama 0.32.13 Vulkan/RADV Evidence

Status: first-party measured local buyer-route evidence.

This run qualifies the official dense Qwen3.8 27B Ollama artifact as a practical text-and-image route on one 128GB Strix Halo system. It is not a direct `llama-bench` result and is not a broad model-quality or long-context qualification.

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
- Tested context: 4,096 tokens

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

## Scope And Caveats

- This is an Ollama API/server result, not direct `llama-bench` evidence.
- The advertised 262K context was not filled or quality-tested.
- Tool use and thinking behavior were not qualified.
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
