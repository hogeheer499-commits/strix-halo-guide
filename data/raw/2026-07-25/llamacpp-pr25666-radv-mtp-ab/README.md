# llama.cpp PR #25666 AMD/RADV MTP A/B

Independent Strix Halo reproduction of
[`ggml-org/llama.cpp` PR #25666](https://github.com/ggml-org/llama.cpp/pull/25666),
which disables MMVQ for speculative-decode steps on AMD Vulkan.

## Exact comparison

- Hardware: Beelink GTR9 Pro, Ryzen AI MAX+ 395, Radeon 8060S, 128GB unified memory.
- Backend: Vulkan/RADV.
- Stock base: `7f575c39d6a29a40c0ef22278eca6bd4a573c8a6` (`llama.cpp` b10005).
- PR head: `e0649d3e02c0a2540a4a1d2b80f308083779e273` (`llama.cpp` b10007).
- Build flags: `Release`, `GGML_NATIVE=ON`, `GGML_VULKAN=ON`, `LLAMA_CURL=OFF`.
- Model: `Qwen3.6-35B-A3B-MTP-IQ4_XS-Q8nextn.gguf`.
- Model SHA-256: `4d2349305663bc59bacab26d8eba8ed1218de84b8d1f0456208037e13efa9a98`.
- Server shape: context 32768, parallel 1, batch 2048, ubatch 512, 16 CPU threads.
- Speculation: MTP, draft maximum 2.
- Workload: six deterministic prompts, 512 generated tokens per prompt, EOS ignored.
- Order: stock/PR for three pairs, then PR/stock for the fourth pair to check warm-up bias.

## Result

The first cold pair favored the PR by 2.69%, but that difference disappeared as
the system warmed. Across warm repeats 2-4:

| Build | Mean weighted decode |
| --- | ---: |
| Stock | 104.04 t/s |
| PR #25666 | 104.61 t/s |

The warm-repeat difference was **+0.55%**, which is too small to treat as a
meaningful performance win on this workload.

Correctness remained stable:

- every run produced the same six per-prompt output hashes;
- the combined output SHA-256 was identical across all eight runs;
- draft acceptance was identical at 80.187%;
- no load failure or server error occurred.

The useful conclusion is therefore **no measured regression and matching
output on this Strix Halo MTP route**, not a speed headline. The PR may matter
more for other model, quant, or speculative-decode shapes.

See [`comparison.csv`](comparison.csv) for the compact result and each run
directory for JSONL responses, server logs, summaries, and sysfs telemetry.
