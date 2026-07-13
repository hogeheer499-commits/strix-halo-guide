# Best Known Strix Halo Local-AI Profiles

This is a compact recommendation index, not another benchmark leaderboard. It turns existing evidence into a practical first choice for common workloads. The machine-readable source is [`data/best_known_profiles.csv`](data/best_known_profiles.csv); detailed caveats remain in the linked evidence pages.

## Start Here

| You want | Start with | Measured signal | Important caveat |
| --- | --- | --- | --- |
| Private chat and Open WebUI | Ollama Vulkan/RADV, Qwen3.6 35B-A3B Q4_K_M | 71.82 t/s warm API mean on Ollama 0.31.1 | Set `OLLAMA_IGPU_ENABLE=1`; the installed 0.31.2 service was compatible but slower in its check. |
| Fastest measured direct coding route | llama.cpp Vulkan/RADV, Qwen3-Coder 30B-A3B Q4_K_S | 100.99 tg128 r50 | Speed-first quant, not the balanced quality default. |
| Balanced direct coding | llama.cpp Vulkan/RADV, Qwen3-Coder 30B-A3B UD-Q4_K_XL | 96.76 tg128 r20 | Use this when the quant tradeoff matters more than the last few t/s. |
| Current Google-model MTP server | Gemma 4 26B-A4B QAT plus matched MTP head | 102.69 cold / 107.42 T3-only / 110.00 best repeat t/s | Advanced server/speculative route, not direct `llama-bench`. |
| 30B service around 16 parallel sequences | Lemonade ROCm b1259 | 287.64 aggregate decode t/s mean | At np9-12, experimental density+dense16 Vulkan was stronger; benchmark the actual concurrency. |
| 80B service around 16 parallel sequences | b9979 Vulkan with opt-in AMD/RADV density gate | 150.82 aggregate decode t/s mean | Experimental patch while upstream issue #25356 remains open. |
| A direct 120B-class GGUF on one box | Nemotron 3 Super 120B-A12B UD-IQ4_XS | 18.43 tg128 | Capacity proof, not a speed result. |
| NPU work beside an iGPU LLM | Treat the NPU as a sidecar | Community artifact measured +3.29% main-workload latency with NPU load | Community/NixOS/IOMMU-on evidence; not the beginner path. |

## Rules

- A profile is included only when it points to measured local or clearly labeled community evidence.
- Direct, API/server, MTP, concurrency, capacity, and NPU results remain separate.
- Experimental profiles do not replace the setup-script default.
- The exact model, quant, runtime, concurrency, context, and host state still matter.
- For the b9979 multi-user decision, use [`MOE_CONCURRENCY.md`](MOE_CONCURRENCY.md) rather than copying one aggregate number into a single-user comparison.

For a new installation, begin with the [README setup script](README.md#setup-script). Move to these profiles only after the basic Ollama/Vulkan path works.
