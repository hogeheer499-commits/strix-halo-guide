# Gemma 4 31B QAT And DFlash Scout

First-party Beelink GTR9 Pro scout of the official Gemma 4 31B QAT Q4_0 GGUF, matched Q8_0 multimodal projector, and matched Q8_0 DFlash sidecar on `llama.cpp` b10066 (`86a9c79f8`) with Vulkan/RADV.

This was a practical workstation-state scout, not a strict-clean headline run. A known low-load CPU-only media workload remained active and did not open the GPU render device. Use the direct and server rows as current-model compatibility and route-selection evidence, not as power, thermal, or strict-clean performance claims.

## Artifacts

- Target: `ggml-org/gemma-4-31B-it-GGUF`, `gemma-4-31B-it-Q4_0.gguf`, 16.76 GiB.
- DFlash sidecar: `dflash-gemma-4-31B-it-Q8_0.gguf`, 1.53 GiB.
- Vision projector: `mmproj-gemma-4-31B-it-Q8_0.gguf`, 0.75 GiB.
- Exact SHA-256 files are stored beside this note.

## Direct And Capability Results

- Direct `llama-bench` r3: **308.28 pp512 / 11.38 tg128**.
- Text smoke: passed with exactly three requested bullets after reasoning was disabled.
- Vision smoke: passed; the model read `STRIX 395` from the generated test image.
- Native OpenAI-compatible tool call: passed in both the no-spec and DFlash server profiles with the correct `calculator(a=395, b=128)` arguments.

These are narrow function checks, not broad text, vision, reasoning, or tool-use quality evaluations.

## Matched Server Comparison

Both profiles used one slot, a 32K server context, greedy generation, uncached synthetic prompts, three repeats per shape, and up to 256 generated tokens. The response records contain the authoritative token counts: the nominal 4K and 16K inputs tokenized to 5,471 and 21,855 prompt tokens.

| Profile | Prompt tokens | PP mean | TG mean | TG range | Draft acceptance | Read |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| No speculative decoding | 5,471 | 275.51 | 10.30 | 10.26-10.35 | n/a | Baseline |
| DFlash, `n_max=8` | 5,471 | 263.17 | 9.73 | 9.12-10.22 | 14.12% | 5.54% slower than baseline |
| No speculative decoding | 21,855 | 209.83 | 9.40 | 9.33-9.46 | n/a | Baseline |
| DFlash, `n_max=8` | 21,855 | 201.52 | 7.48 | 7.40-7.58 | 10.91% | 20.42% slower than baseline |

The sidecar loads and produces correct tool calls, but it is not a useful speed recommendation for these synthetic long-prompt shapes. The upstream DFlash card reports task-dependent acceptance lengths on a single NVIDIA B300 with vLLM; those results do not imply a Vulkan/RADV speedup on this workload. A future comparison should use representative chat, coding, and reasoning prompts plus source-recommended parameters rather than treating speculative decoding as automatically faster.

## Evidence Map

- `llama-bench.csv`: direct r3 row.
- `nospec.jsonl`, `dflash.jsonl`: full requests, responses, and wall times.
- `nospec.server.log`, `dflash.server.log`: server timing and DFlash acceptance records.
- `server-summary.csv`: compact matched comparison.
- `nospec.tool-smoke.json`, `dflash.tool-smoke.json`: native tool-call checks.
- `text-smoke.txt`, `vision-output.txt`: narrow function outputs.
- `host-snapshot.txt`: kernel, boot profile, memory, build, and RADV metadata.
- `run-scout.sh`, `run-dflash-only.sh`, `run-server-tests.py`: reproducer scripts.

## Sources

- <https://huggingface.co/ggml-org/gemma-4-31B-it-GGUF>
- <https://huggingface.co/z-lab/gemma-4-31B-it-DFlash>
