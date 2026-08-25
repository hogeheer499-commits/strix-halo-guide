# Best Known Strix Halo Local-AI Profiles

This is a compact recommendation index, not another benchmark leaderboard. It turns existing evidence into a practical first choice for common workloads. The machine-readable source is [`data/best_known_profiles.csv`](data/best_known_profiles.csv); detailed caveats remain in the linked evidence pages.

## Start Here

| You want | Start with | Measured signal | Important caveat |
| --- | --- | --- | --- |
| Private chat, vision, and Open WebUI | Ollama 0.31.2 system service with Vulkan/RADV, Qwen3.6 35B-A3B Q4_K_M | 60.57 t/s warm API mean; iGPU, vision, restart, and reboot passed | Set `OLLAMA_IGPU_ENABLE=1`. Qwen3.8 27B is measured separately on 0.32.13; 0.31.2 stays the reboot-qualified default until current 0.32.15 passes the normal service-upgrade, Qwen3.8 thinking compatibility, and full-reboot path. |
| Current official dense multimodal chat | Ollama 0.32.13 system service with Vulkan/RADV, Qwen3.8 27B Q4_K_M | 292.49 prompt t/s and 20.42 generation t/s warm API mean over nine repeats; image, tool-call, thinking, and exact retrieval passed through 50,059 prompt tokens | Use `/api/chat` for the qualified long-context path. A 56,051-token attempt caused a recoverable Vulkan device-loss on this exact stack; the advertised 262K and broad quality remain unqualified. Not a direct speed headline. |
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
| Fine-tune, export, and reload a small local model | Pinned Unsloth ROCm 7.2 container plus bundled ROCm `llama.cpp` | Radeon GPU gate, one SFT step, checkpoint inference, `Q4_K_M` export, local GGUF inference, and post-restart load all passed | Functional Qwen3 0.6B plumbing smoke. It does not prove useful fine-tuning quality, large-model training, or headline speed. Follow [`UNSLOTH_STRIX_HALO.md`](UNSLOTH_STRIX_HALO.md). |
| Lightweight local image understanding | Official LFM2.5-VL 1.6B Q4_0 plus Q8_0 projector on b10107 Vulkan/RADV | Correctly read the guide image and produced an exact fresh-process repeat; cached process took 1.89 seconds | One-image function/restart smoke, not broad vision quality. Follow the exact [`raw route`](data/raw/2026-07-25/lfm25-vl-16b-official-gguf/). |
| Short offline speech transcription | Official Qwen3-ASR 0.6B Q8_0 plus Q8_0 projector on b10107 Vulkan/RADV | Transcribed `Front, center.` exactly across fresh processes; cached process took 1.13 seconds | Short clean English smoke only. No Dutch, streaming, long-audio, WER, or production claim; `llama.cpp` audio is experimental. Follow the exact [`raw route`](data/raw/2026-07-25/qwen3-asr-06b-official-gguf/). |
| Qwen3-Next 80B speculative serving | b10330 ROCm/HIP with the matched MTP-only Q4_K_M sidecar | 83.52 t/s short and 83.60 t/s at 3K; 62.7-66.5% over matched HIP direct with exact observed output hashes | Backend-specific real-workstation qualification, not a strict-clean headline. The same sidecar was a severe regression on Vulkan despite high acceptance. Follow the [`backend A/B`](data/raw/2026-08-09/qwen3-next-80b-mtp-b10330/). |
| Short offline speech synthesis | Official Qwen3-TTS 1.7B Q4_K_M plus Q8_0 projector on b10330 Vulkan/RADV | 4.16 seconds of audio in 1.27 seconds reported model processing (`3.27x` real time); ASR preserved the intended sentence | Experimental audio route with unsupported-operation and possible reduced-quality warnings. No voice-quality, multilingual, deterministic-audio, or production claim. Follow the [`raw route`](data/raw/2026-08-09/qwen3-tts-17b-b10330-vulkan/). |
| Local document embeddings | NVIDIA Llama Nemotron Embed 1B v2 through Sentence Transformers on CPU | Relevant cosine 0.41061 versus unrelated 0.03095; 2048 dimensions and exact offline repeat | Tiny retrieval sanity check, not a corpus, multilingual, long-document, ROCm, or quality benchmark. Follow the exact [`raw route`](data/raw/2026-07-25/nemotron-embed-1b-v2-official/). |

Qwen3.8 needs an extra route decision because current public values are not
measured under one protocol. The guide's official Ollama result, the external
262K-class GMKtec validation, stock community MTP, tuned ROCm/DFlash reports,
and the unpublished-sidecar lead are separated in
[`QWEN38_STRIX_HALO.md`](QWEN38_STRIX_HALO.md) and
[`data/qwen38_route_matrix.csv`](data/qwen38_route_matrix.csv).

## Rules

- A profile is included only when it points to measured local or clearly labeled community evidence.
- Direct, API/server, MTP, concurrency, capacity, and NPU results remain separate.
- Experimental profiles do not replace the setup-script default.
- The exact model, quant, runtime, concurrency, context, and host state still matter.
- For the b9979 multi-user decision, use [`MOE_CONCURRENCY.md`](MOE_CONCURRENCY.md) rather than copying one aggregate number into a single-user comparison.

For a new installation, begin with the [README setup script](README.md#setup-script). Move to these profiles only after the basic Ollama/Vulkan path works.
