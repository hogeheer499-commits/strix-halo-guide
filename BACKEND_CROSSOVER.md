# HIP vs Vulkan Backend Crossover

Status: active evidence track, started 2026-05-07.

This page answers a narrower question than the main guide:

> Should Strix Halo users always pick Vulkan/RADV, or does ROCm/HIP win some workloads?

Current answer: there is no single backend winner. Vulkan/RADV is still the best measured local path for short-context generation, chat, and coding-agent loops. ROCm/HIP can be better for prompt-processing-heavy work such as long prompts, RAG ingestion, summarization, and some batch/server shapes.

## Local Spot Check

Canonical local data: [`data/backend_crossover.csv`](data/backend_crossover.csv).

Important caveat: this is a local existing-build spot check, not a perfect same-build fairness claim. Vulkan rows use llama.cpp b9010; HIP rows use the available local HIP b8460 build and Ollama-bundled ROCm 7.2 libraries. The value is directional: it checks whether our machine shows the same workload split that newer external Strix Halo HIP/Vulkan work reports.

| Model | Vulkan pp16384 | HIP pp16384 | Prompt winner | Vulkan tg128 | HIP tg128 | Generation winner |
|-------|---------------:|------------:|---------------|-------------:|----------:|-------------------|
| Qwen3.6 35B-A3B UD-Q4_K_M | 1038.14 | **1295.38** | HIP +24.8% | **62.24** | 52.72 | Vulkan +18.1% |
| Qwen3-Coder 30B-A3B UD-Q4_K_XL | 564.68 | **756.16** | HIP +33.9% | **93.67** | 72.19 | Vulkan +29.8% |

Charts:

- [`charts/backend_crossover_prefill.svg`](charts/backend_crossover_prefill.svg)
- [`charts/backend_crossover_generation.svg`](charts/backend_crossover_generation.svg)

Raw logs:

- [`data/raw/2026-05-07/hip-vs-vulkan-crossover/`](data/raw/2026-05-07/hip-vs-vulkan-crossover/)

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

Use this split until a newer same-build local comparison replaces it:

| Workload | Start with | Why |
|----------|------------|-----|
| Easy chat and model pulling | Ollama Vulkan/RADV | lowest setup friction and measured 50.51 t/s warm Qwen3.6 API average |
| Coding, scripts, short responses | llama.cpp or `llama-server` Vulkan/RADV | fastest measured local generation path |
| RAG ingestion, long prompts, summarization | keep a ROCm/HIP path available | local and external data both show HIP can win prompt processing |
| Many local clients hitting one API | compare Vulkan/RADV and Lemonade ROCm at target concurrency | existing server sweep shows Lemonade ROCm wins aggregate throughput at 8-16 parallel requests |
| vLLM/AWQ/DFlash experiments | container only, not host Python | promising but not yet reproduced locally in this guide |

## Next Clean Test

The next publishable upgrade is a true same-build comparison:

1. Build current llama.cpp with both Vulkan and HIP from the same commit.
2. Use the same model files, flags, batch sizes, KV types, and repetition counts.
3. Test pp512, pp2048, pp8192, pp16384, tg128, and at least one real long-prompt request.
4. Keep Gemma 4 as a load/support check, not a speed claim unless HIP loads cleanly.
