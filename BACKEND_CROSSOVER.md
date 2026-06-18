# HIP vs Vulkan Backend Crossover

Status: active evidence track, started 2026-05-07.

This page answers a narrower question than the main guide:

> Should Strix Halo users always pick Vulkan/RADV, or does ROCm/HIP win some workloads?

Current answer: there is no single backend winner. Vulkan/RADV is still the best measured local path for short-context generation, chat, and coding-agent loops. ROCm/HIP can be better for prompt-processing-heavy work such as long prompts, RAG ingestion, summarization, and some batch/server shapes.

## Same-Source b9049 Matrix

Canonical 2026-05-07 data: [`data/max_performance_campaign.csv`](data/max_performance_campaign.csv) and [`data/raw/2026-05-07/max-performance-campaign/benchmarks/same-build-hip-vulkan-b9049/`](data/raw/2026-05-07/max-performance-campaign/benchmarks/same-build-hip-vulkan-b9049/).

Important caveat: Vulkan and HIP were built from the same b9049 source checkout, but the HIP binary reports `build_commit=unknown` because the container did not trust the git directory. Treat this as a same-source matrix, not a perfectly embedded-build-id matrix.

| Model | Vulkan pp16384 | HIP pp16384 | Prompt winner | Vulkan tg128 | HIP tg128 | Generation winner |
|-------|---------------:|------------:|---------------|-------------:|----------:|-------------------|
| Qwen3.6 35B-A3B Q4_0 | 1088.91 | **1331.28** | HIP +22.3% | **79.54** | 62.16 | Vulkan +28.0% |
| Qwen3.6 35B-A3B UD-Q4_K_M | 1037.43 | **1302.76** | HIP +25.6% | **60.03** | 53.30 | Vulkan +12.6% |
| Qwen3-Coder 30B-A3B UD-Q4_K_XL | 564.47 | **747.00** | HIP +32.3% | **85.20** | 68.33 | Vulkan +24.7% |

Takeaway: the beginner rule is still simple: use RADV/Vulkan first. The advanced rule is also clearer now: if your workload spends most of its time ingesting long prompts, RAG chunks, or documents, test HIP instead of assuming Vulkan wins that shape too.

## Local Spot Check

Canonical local data: [`data/backend_crossover.csv`](data/backend_crossover.csv).

This older local existing-build spot check is kept as supporting history. Vulkan rows use llama.cpp b9010; HIP rows use the available local HIP b8460 build and Ollama-bundled ROCm 7.2 libraries. The value is directional: it checks whether our machine shows the same workload split that newer external Strix Halo HIP/Vulkan work reports.

| Model | Vulkan pp16384 | HIP pp16384 | Prompt winner | Vulkan tg128 | HIP tg128 | Generation winner |
|-------|---------------:|------------:|---------------|-------------:|----------:|-------------------|
| Qwen3.6 35B-A3B UD-Q4_K_M | 1038.14 | **1295.38** | HIP +24.8% | **62.24** | 52.72 | Vulkan +18.1% |
| Qwen3-Coder 30B-A3B UD-Q4_K_XL | 564.68 | **756.16** | HIP +33.9% | **93.67** | 72.19 | Vulkan +29.8% |

Charts:

- [`charts/backend_crossover_prefill.svg`](charts/backend_crossover_prefill.svg)
- [`charts/backend_crossover_generation.svg`](charts/backend_crossover_generation.svg)

Raw logs:

- [`data/raw/2026-05-07/hip-vs-vulkan-crossover/`](data/raw/2026-05-07/hip-vs-vulkan-crossover/)

## Qwen3-Next 80B 2026-05-16 Spot Check

Canonical local data: [`data/backend_crossover.csv`](data/backend_crossover.csv), [`data/raw/2026-05-16/latest-stack-b9172/`](data/raw/2026-05-16/latest-stack-b9172/), and [`data/raw/2026-05-16/lemonade-rocm-b1259-spotcheck/`](data/raw/2026-05-16/lemonade-rocm-b1259-spotcheck/).

This is not a final same-build backend shootout: Vulkan uses llama.cpp b9172, while HIP uses the existing Lemonade `llamacpp-rocm` b1259/gfx1151 bundle. It is still valuable because it repeats the same practical split on the largest current Qwen-family model in the guide.

| Model | Vulkan pp512 | HIP pp512 | Prompt winner | Vulkan tg128 | HIP tg128 | Generation winner |
|-------|-------------:|----------:|---------------|-------------:|----------:|-------------------|
| Qwen3-Next 80B-A3B UD-Q4_K_XL | 751.70 | **800.38** | HIP +6.5% | **59.06** | 49.57 | Vulkan +19.1% |

Takeaway: Qwen3-Next strengthens the same rule rather than replacing it. Vulkan/RADV stays the practical default for generation-heavy chat/coding on GGUF models, while HIP remains worth testing for prompt-processing-heavy work.

## Community Beelink CachyOS ROCm/ZenDNN Crossover

Canonical community source: [discussion #2](https://github.com/hogeheer499-commits/strix-halo-guide/discussions/2#discussioncomment-17276639) and [`data/raw/2026-06-12/community-devoidfury-cachyos-rocm-zendnn/`](data/raw/2026-06-12/community-devoidfury-cachyos-rocm-zendnn/).

devoidfury contributed a second Beelink GTR9 Pro owner stack using CachyOS, `linux-cachyos-server` 7.0.11-1, ROCm 7.2.4-1, local ZenDNN, `amd_iommu=on`, and llama.cpp commit `1593d5684d077c07fc788e9527ec1bd52287de7f` with small local MMQ/ZenDNN build tweaks.

Model and command shape:

- `unsloth/Qwen3.6-27B-MTP-GGUF`
- `UD-Q6_K_XL`
- `llama-bench --n-gpu-layers 999 --flash-attn on -b 1024 -ub 512 -p 5000 -n 512`

| Backend | Prompt workload | Prompt t/s | Decode workload | Decode t/s | Interpretation |
|---------|-----------------|-----------:|-----------------|-----------:|----------------|
| Vulkan/RADV + ZenDNN | pp5000 | 155.89 | tg512 | 8.09 | Baseline for this patched CachyOS/ZenDNN row. |
| ROCm/HIP + ZenDNN | pp5000 | 303.20 | tg512 | 8.38 | ROCm prompt processing was about 1.95x Vulkan on this workload; decode stayed in the same class. |
| ROCm/HIP + ZenDNN | pp40000 | 227.44 | tg1024 | 8.39 | Long-prompt bonus row; supports the "test ROCm for prompt-heavy work" rule. |

This is useful backend-crossover evidence, not a stock same-build shootout and not a decode-speed headline. The local patches and ZenDNN build mean the raw provenance matters. The negative notes matter too: VMM built but crashed on model load, and `GGML_HIP_ROCWMMA_FATTN` was reported as a prompt-processing regression on this stack.

## Community GMKtec EVO-X2 NixOS / ROCmFP4 Context

Canonical community source: [`ciru-ai/strix-halo-evo-x2-evidence`](https://github.com/ciru-ai/strix-halo-evo-x2-evidence), guide provenance note [`data/raw/2026-06-14/community-ciru-evox2-nixos-npu-rocmfp4/`](data/raw/2026-06-14/community-ciru-evox2-nixos-npu-rocmfp4/), and compact metric subset [`data/community_ciru_evox2_metrics.csv`](data/community_ciru_evox2_metrics.csv).

ciru-ai's artifact is not a stock HIP-versus-Vulkan shootout. It is still important for the backend story because it adds an advanced GMKtec EVO-X2 owner stack with NixOS 26.05 pre-release, Linux 7.0.1, Mesa 26.0.5, IOMMU enabled, the NPU exposed through `/dev/accel/accel0`, and tuned ROCmFP4/Chadrock/Gemma/CrownV7 routes.

Selected backend-relevant rows:

| Track | Representative result | Backend interpretation |
|-------|-----------------------|------------------------|
| NPU sidecar | +3.29% main 64k iGPU workload latency with concurrent NPU load versus +68.96% with a comparable iGPU auxiliary load | Keep the NPU discussion separate from main iGPU decode speed. The NPU may be useful as an auxiliary lane when IOMMU/NPU access matters. |
| ROCmFP4 tuned 27B | Qwopus3.6 27B Chadrock reached 0.9451 HumanEval+ in the public artifact | Useful tuned-route quality evidence, not a stock ROCm/HIP backend recommendation. |
| ROCmFP4 tuned 35B | Ace Saber 35B ROCmFP4 MTP reached 0.9024 HumanEval+ with 104.35 peak predicted tok/s | Interesting for advanced model-route testing; keep separate from direct `llama-bench` headlines. |
| Gemma QAT/MTP | Gemma 4 26B-A4B QAT/MTP row reports 122.8 decode tok/s after TTFP on a 512-token API row | Served/API and speculative route evidence, not a direct backend replacement row. |

Practical read: this package strengthens the advanced-research lane. It does not change the beginner recommendation: use Ubuntu + Vulkan/RADV + Ollama first, then test direct `llama.cpp`, `llama-server`, ROCm/HIP, NPU sidecar work, or ROCmFP4 tuned routes when the workload justifies the complexity.

## Negative Result

Gemma 4 26B-A4B loaded and ran on Vulkan/RADV, but the local HIP b8460 path failed to load the GGUF:

```text
main: error: failed to load model '/home/hoge-heer/models/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf'
```

That means this guide should not publish a Gemma 4 HIP speed claim from the local machine yet.

## External Context

The local result matches the direction of [`nabe2030/hip-vs-vulkan-evo-x2`](https://github.com/nabe2030/hip-vs-vulkan-evo-x2), which reports a cleaner same-build Strix Halo comparison on llama.cpp b8966 with ROCm 7.2.2. Their main conclusion is also workload-dependent: HIP wins prompt-processing-dominated workloads, while Vulkan wins generation-dominated workloads.

This does not replace local measurements because their system differs: EVO-X2, Ubuntu 26.04, 96GB VGM, ROCm 7.2.2, and b8966. It is still useful as an independent cross-check.

## Practical Recommendation

Use this split until a newer polished same-build local comparison replaces it:

| Workload | Start with | Why |
|----------|------------|-----|
| Easy chat and model pulling | Ollama Vulkan/RADV | lowest setup friction and measured 50.51 t/s warm Qwen3.6 API average |
| Coding, scripts, short responses | llama.cpp or `llama-server` Vulkan/RADV | fastest measured local generation path |
| RAG ingestion, long prompts, summarization | keep a ROCm/HIP path available | local and external data both show HIP can win prompt processing |
| Many local clients hitting one API | compare Vulkan/RADV and Lemonade ROCm at target concurrency | existing server sweep shows Lemonade ROCm wins aggregate throughput at 8-16 parallel requests |
| vLLM/AWQ/DFlash experiments | container only, not host Python | promising but not yet reproduced locally in this guide |

## Next Clean Test

The next publishable upgrade is not another broad argument; it is a more polished repeat of the same-source result:

1. Build current llama.cpp with both Vulkan and HIP from the same commit.
2. Use the same model files, flags, batch sizes, KV types, and repetition counts.
3. Ensure both binaries embed the correct build id.
4. Test pp512, pp2048, pp8192, pp16384, tg128, and at least one real long-prompt request.
5. Keep Gemma 4 as a load/support check, not a speed claim unless HIP loads cleanly.
