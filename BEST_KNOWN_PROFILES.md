# Best Known Strix Halo Local-AI Profiles

This is a compact recommendation index, not another benchmark leaderboard. It turns existing evidence into a practical first choice for common workloads. The machine-readable source is [`data/best_known_profiles.csv`](data/best_known_profiles.csv); detailed caveats remain in the linked evidence pages.

## Start Here

| You want | Start with | Measured signal | Important caveat |
| --- | --- | --- | --- |
| Private chat, vision, and Open WebUI | Ollama 0.31.2 system service with Vulkan/RADV, Qwen3.6 35B-A3B Q4_K_M | 60.57 t/s warm API mean; iGPU, vision, restart, and reboot passed | Set `OLLAMA_IGPU_ENABLE=1`. Controlled local binaries later put 0.31.1, 0.31.2, and 0.32.0 in the same 72.55-73.20 t/s class; 0.31.2 stays the default because it is the fully qualified normal service path. |
| Fastest measured direct coding route | llama.cpp Vulkan/RADV, Qwen3-Coder 30B-A3B Q4_K_S | 100.99 tg128 r50 | Speed-first quant, not the balanced quality default. |
| Balanced direct coding | llama.cpp Vulkan/RADV, Qwen3-Coder 30B-A3B UD-Q4_K_XL | 96.76 tg128 r20 | Use this when the quant tradeoff matters more than the last few t/s. |
| Current Google-model MTP server | Gemma 4 26B-A4B QAT plus matched MTP head | 102.69 cold / 107.42 T3-only / 110.00 best repeat t/s | Advanced server/speculative route, not direct `llama-bench`. |
| 30B service around 16 parallel sequences | Lemonade ROCm b1259 | 287.64 aggregate decode t/s mean | At np9-12, experimental density+dense16 Vulkan was stronger; benchmark the actual concurrency. |
| 80B service around 16 parallel sequences | b9979 Vulkan with opt-in AMD/RADV density gate | 150.82 aggregate decode t/s mean | Experimental patch while upstream issue #25356 remains open. |
| A direct 120B-class GGUF on one box | Nemotron 3 Super 120B-A12B UD-IQ4_XS | 18.43 tg128 | Capacity proof, not a speed result. |
| Maximum measured direct ordinary-GGUF capacity | DeepSeek V4 Flash 284B UD-IQ2_XXS | 155.64 pp512 / 13.27 tg128; deterministic smoke answered `9` | 90.86GB low-bit artifact. Use as a capacity/current-model scout, not as a speed or broad quality recommendation. |
| A frontier-size local agent with tools and long context | Step 3.7 Flash ROCmFPX Q3 QualityPlus plus Q8 MTP draft | 34.50 t/s at 4K; 33.83 t/s at 16K; native tool call and 256K allocation passed | 198B-total / about 11B-active advanced server route. Pinned ROCmFPX runtime; not direct `llama-bench`, and the 256K result is allocation rather than a filled-context quality test. |
| FP16 vLLM at 8-16 concurrent requests | ROCm 7.14 official RDNA image with `TORCH_BLAS_PREFER_HIPBLASLT=1` | +40.50% / +38.96% / +41.54% aggregate throughput at concurrency 8/9/16 | Measured with Qwen3-0.6B FP16 and PyTorch 2.11. Small-model server profile, not proof for quantized or practical 27B/35B models; concurrency 4 was slightly slower. |
| NPU work beside an iGPU LLM | Treat the NPU as a sidecar | Community artifact measured +3.29% main-workload latency with NPU load | Community/NixOS/IOMMU-on evidence; not the beginner path. |
| A tuned high-acceptance MTP reference profile | ROCmFPX CHADROCK ACE/SABER 35B | 141.37 t/s mean across three exact 3946-token-profile repeats | Advanced and prompt-shape-specific. The 1K and 8K profiles fell to 78.00 and 83.85 t/s as draft acceptance dropped; measure real workloads. |
| Current 30B-class image understanding | Nemotron 3 Nano Omni NVFP4 plus F16 projector | 53.21 tg128 language row; `STRIX 395` image OCR smoke passed | Experimental multimodal CLI and one small image check only; no broad vision, audio, video, or production claim. |

## Rules

- A profile is included only when it points to measured local or clearly labeled community evidence.
- Direct, API/server, MTP, concurrency, capacity, and NPU results remain separate.
- Experimental profiles do not replace the setup-script default.
- The exact model, quant, runtime, concurrency, context, and host state still matter.
- For the b9979 multi-user decision, use [`MOE_CONCURRENCY.md`](MOE_CONCURRENCY.md) rather than copying one aggregate number into a single-user comparison.

For a new installation, begin with the [README setup script](README.md#setup-script). Move to these profiles only after the basic Ollama/Vulkan path works.
