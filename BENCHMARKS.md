# Benchmark Results - Current Snapshot

This file is the compact benchmark source-of-truth for numbers already published in the README. It reconciles historical and current measurements so old ROCm, driver, serving, and long-context notes do not contradict the current guide.

## Current System Snapshot

Live audit on 2026-05-07:

| Component | Current State |
|-----------|---------------|
| System | Beelink GTR9 Pro |
| CPU | AMD Ryzen AI MAX+ 395, 16C/32T |
| GPU | Radeon 8060S, gfx1151, RADV STRIX_HALO |
| RAM | 124GiB OS-visible unified memory |
| Kernel | 6.19.4-061904-generic |
| Mesa RADV | 26.0.6, kisak-mesa PPA |
| Ollama | 0.23.1 |
| AMDVLK | Removed |
| linux-firmware | 20240318.git3b128b60-0ubuntu2.27 |
| GPU clock | 2900 MHz selected |
| tuned | `accelerator-performance` active |

Historical benchmark runs below were measured on 2026-03-20, 2026-03-21, and 2026-04-26 with `tuned accelerator-performance` active. The 2026-05-07 latest-stack rerun confirms `tuned accelerator-performance` active, Mesa RADV 26.0.6, AMDVLK absent, linux-firmware safe, GPU clock at 2900 MHz, llama.cpp b9049, and Ollama 0.23.1.

## Top-Line Model Results

| Model | Backend / Build | Quant | pp512 | tg128 | Notes |
|-------|-----------------|-------|-------|-------|-------|
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9049 | UD-Q4_K_XL | 1321 | **96.76** | Max-performance guide-flags r20 confirmation |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9010 | UD-Q4_K_XL | 1346 | **97.24** | Previous May peak |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b8460 | UD-Q4_K_XL | 1342 | **87.11** | Previous coding MoE headline |
| Qwen3.6 35B-A3B | Vulkan RADV, llama.cpp b9049 | Q4_0 | 1244 | **81.30** | Fastest measured speed-first quant; lower-quality tradeoff |
| Qwen3.6 35B-A3B | Vulkan RADV, llama.cpp b9049 | Q4_K_M | 1106 | **76.94** | Fast balanced Strix quant candidate |
| Qwen3.6 35B-A3B | Vulkan RADV, llama.cpp b9049 | UD-Q4_K_M | 1059 | **62.56** | Clean latest-stack rerun |
| Qwen3.6 35B-A3B | Vulkan RADV, llama.cpp b9010 | UD-Q4_K_M | 1109 | **63.06** | Previous May UD rerun |
| Qwen3.6 35B-A3B | Vulkan RADV, llama.cpp b8460 | Q4_K_M | 1064 | **63.76** | Recommended all-rounder |
| Qwen3.5 35B-A3B | Vulkan RADV, llama.cpp b8460 | Q4_K_M | 1080 | **64.85** | Used for backend/build comparison |
| gpt-oss-120b | Vulkan RADV, llama.cpp b9049 | MXFP4 MoE | 727 | **55.57** | 117B-parameter open-weight MoE loaded from split GGUF |
| Qwen3-Next 80B-A3B | Vulkan RADV, llama.cpp b8933 | UD-Q4_K_XL | 657 | **54.92** | 80B MoE, 256K context capable |
| Gemma 4 26B-A4B | Vulkan RADV, llama.cpp b8933 | UD-Q4_K_M | 1142 | **48.46** | Slower than Qwen MoE at similar active params |
| Llama 4 Scout 109B | Vulkan RADV, llama.cpp b8933 | Q4_K_M | 331 | **18.32** | 109B params on one mini PC |
| Llama 3.1 70B | Ollama Vulkan RADV | Q4_K_M | 22-80 | **4.7-4.9** | Dense 70B, bandwidth-bound |
| Qwen3 0.6B | Vulkan RADV, llama.cpp | Q8_0 | 13112 | **266** | Small-model speed ceiling |

## Qwen3.6 Quant Sweep

Measured 2026-05-07 with llama.cpp b9049 Vulkan/RADV on the Beelink GTR9 Pro. Raw data: [`data/raw/2026-05-07/max-performance-campaign/benchmarks/qwen36-top-confirm-r20/`](data/raw/2026-05-07/max-performance-campaign/benchmarks/qwen36-top-confirm-r20/).

| Quant | pp512 | tg128 | Use |
|-------|------:|------:|-----|
| Q4_0 | 1243.51 | **81.30** | Fastest measured Qwen3.6 row; speed-first, lower-quality tradeoff. |
| Q4_0 with q8 KV | 1229.97 | 79.90 | Slightly slower decode; q8 KV may be useful for some context/memory tradeoffs. |
| IQ4_NL | 1199.41 | 77.29 | Fast candidate; quality sanity needed before recommending broadly. |
| Q4_K_M | 1105.78 | 76.94 | Balanced Strix quant candidate; likely more practical than Q4_0 if quality matters. |
| UD-Q4_K_M | 1059.45 | 62.56 | Older default headline row from the clean latest-stack rerun. |

Takeaway: Qwen3.6 can be pushed well past the old 63 t/s row, but the guide should not hide the quant tradeoff. For beginners, keep "use Qwen3.6 Q4_K_M/UD-Q4_K_M as the all-rounder" and add "use Q4_0 when you want maximum speed and have accepted the quality tradeoff."

## gpt-oss-120b Local Check

Measured 2026-05-07 with llama.cpp b9049 Vulkan/RADV and the `ggml-org/gpt-oss-120b-GGUF` MXFP4 split GGUF. This is a performance/loadability check, not a quality evaluation.

Raw data:

- first load/speed check: [`data/raw/2026-05-07/gpt-oss-120b-local-attempt/`](data/raw/2026-05-07/gpt-oss-120b-local-attempt/)
- clean paused-system long-context rerun: [`data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/)

| Workload | Result | Raw CSV |
|----------|-------:|---------|
| pp512 | 726.99 t/s | [`long-context rerun`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-prefill-512-32768-r3.csv) |
| pp2048 | 728.60 t/s | [`long-context rerun`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-prefill-512-32768-r3.csv) |
| pp8192 | 678.59 t/s | [`long-context rerun`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-prefill-512-32768-r3.csv) |
| pp16384 | 605.21 t/s | [`long-context rerun`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-prefill-512-32768-r3.csv) |
| pp32768 | 478.25 t/s | [`long-context rerun`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-prefill-512-32768-r3.csv) |
| pp65536 | 293.73 t/s | [`pp65536 r1`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-pp65536-r1.csv) |
| tg128 | 55.57 t/s | [`tg128 r20`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-tg128-r20.csv) |

Takeaway: the 128GB Strix Halo setup can load and run a 117B-parameter open-weight MoE locally at about 55-56 t/s generation on the measured direct Vulkan path. The first tg32 attempt was correctly aborted by the benchmark guard when swap-free dropped under 2 GiB; after clearing swap with ample free RAM, tg32 and tg128 completed. The later paused-system rerun also proves prompt processing through 65K tokens, but the 65K row is one repeat.

## Ollama Vulkan

### Qwen3.6-35B-A3B, Ollama 0.23.1, Vulkan RADV

| Prompt Tokens | Prompt Eval | Generation | Notes |
|---------------|-------------|------------|-------|
| 19 | 158 t/s | **50.5 t/s** | Controlled 2026-05-07 API warm average across 10 runs; matches 0.21.2 |
| 20 | 163 t/s | 45.6 t/s | Older result, superseded by controlled API run |
| 22 | 174 t/s | 45.4 t/s | Older result, superseded by controlled API run |

### Historical March Ollama Results

These remain useful as historical data, but they are not the current headline numbers.

| Model | Prompt Tokens | pp (t/s) | tg (t/s) | Notes |
|-------|---------------|----------|----------|-------|
| Qwen3.5 35B-A3B, Ollama 0.20.4 | 14 | 121.3 | **48.0** | Mesa 26.0.2 era |
| Qwen3.5 35B-A3B, Ollama 0.20.4 | 23 | 182.3 | **47.5** | Mesa 26.0.2 era |
| Qwen3.5 35B-A3B, Ollama 0.20.4 | 122 | 456.7 | **47.4** | Mesa 26.0.2 era |
| Qwen3-Coder 30B-A3B Q8_0 | 12 | 118.3 | **51.4** | Ollama path |
| Qwen3-Coder-Next | 120 | 301.2 | **37.9** | Dense 51GB model |
| Qwen2.5-VL 7B | 23 | 81.7 | **21.4** | Vision-language model |

## Multi-User llama-server

### Qwen3.6-35B-A3B UD-Q4_K_M, llama.cpp b9010, Vulkan RADV

This is a serving benchmark, not a single-user `llama-bench` headline. Each row is the average of 3 measured repetitions with streaming `/completion`, 128 generated tokens per request, prompt cache disabled, continuous batching enabled, and about 4096 context tokens per slot.

| `-np` | Concurrent Requests | Aggregate tg | Avg per Request | Mean TTFT | Mean ITL | Notes |
|-------|---------------------|--------------|-----------------|-----------|----------|-------|
| 1 | 1 | 59.21 t/s | 59.21 t/s | 0.117 s | 16.1 ms | Server/API path baseline |
| 2 | 2 | 92.21 t/s | 46.11 t/s | 0.198 s | 20.3 ms | Good scaling |
| 4 | 4 | 130.81 t/s | 32.71 t/s | 0.237 s | 29.0 ms | Strong batching gain |
| 8 | 8 | **161.98 t/s** | 20.25 t/s | 0.307 s | 47.4 ms | Practical sweet spot |
| 16 | 16 | 165.98 t/s | 10.38 t/s | 0.547 s | 92.9 ms | Throughput plateau |

Takeaway: continuous batching makes Strix Halo much more useful as a local API box than single-user numbers imply. `-np 8` gives about 2.7x the `-np 1` aggregate throughput while keeping TTFT near 0.3 seconds. `-np 16` is viable for many low-rate clients, but not faster overall.

### Qwen3-Coder 30B-A3B UD-Q4_K_XL, llama.cpp b9010, Vulkan RADV

| `-np` | Concurrent Requests | Aggregate tg | Avg per Request | Mean TTFT | Mean ITL | Notes |
|-------|---------------------|--------------|-----------------|-----------|----------|-------|
| 1 | 1 | 90.20 t/s | 90.20 t/s | 0.079 s | 10.6 ms | Server/API path baseline |
| 2 | 2 | 121.65 t/s | 60.83 t/s | 0.133 s | 15.5 ms | Good scaling |
| 4 | 4 | 157.41 t/s | 39.36 t/s | 0.207 s | 24.0 ms | Strong batching gain |
| 8 | 8 | **173.16 t/s** | 21.65 t/s | 0.382 s | 43.5 ms | Practical sweet spot |
| 16 | 16 | 129.56 t/s | 8.10 t/s | 0.571 s | 119.9 ms | Regression |

Takeaway: `-np 8` is the best measured setting for Qwen3-Coder serving. `-np 16` regresses, so avoid it for throughput-focused coding workloads.

## Long-Context Prompt Scaling

These rows measure prompt processing at the listed prompt lengths. They do not measure decode speed after a fully occupied KV cache.

| Model | Quant | 4K pp | 8K pp | 16K pp | 32K pp | 64K pp | tg128 row |
|-------|-------|-------|-------|--------|--------|--------|-----------|
| Qwen3.6 35B-A3B | UD-Q4_K_M | 1081.93 | 1089.48 | 1024.58 | 908.61 | 740.25 | 57.84 |
| Qwen3-Next 80B-A3B | UD-Q4_K_XL | 741.68 | 735.50 | 700.49 | 644.82 | 543.89 | 55.58 |

Takeaway: Qwen3.6 retains 68% of its 4K prompt-processing speed at 64K. Qwen3-Next 80B retains 73%, which is a strong result for a 46GB-on-disk 80B MoE model.

## Filled-KV Decode

These rows measure a full `llama-server` request: long prompt ingestion plus 128 generated tokens after the KV cache is filled. Prompt cache was disabled. Prompt content was synthetic and repetitive, so compare within this table rather than against arbitrary real-world documents.

| Model | Prompt | KV | Prompt Eval | Decode After Fill | Wall Time |
|-------|--------|----|-------------|-------------------|-----------|
| Qwen3.6 35B-A3B | 32K | f16 | 1216.64 t/s | 51.00 t/s | 29.50 s |
| Qwen3.6 35B-A3B | 32K | q8_0 | 1023.43 t/s | 54.59 t/s | 34.46 s |
| Qwen3.6 35B-A3B | 32K | q4_0 | 1048.70 t/s | 56.03 t/s | 33.58 s |
| Qwen3.6 35B-A3B | 64K | f16 | 931.89 t/s | 41.44 t/s | 73.52 s |
| Qwen3.6 35B-A3B | 64K | q8_0 | 731.22 t/s | 49.13 t/s | 92.33 s |
| Qwen3.6 35B-A3B | 64K | q4_0 | 750.04 t/s | 51.33 t/s | 89.97 s |
| Qwen3.6 35B-A3B | 128K | f16 | 616.77 t/s | 32.23 t/s | 216.69 s |
| Qwen3-Next 80B-A3B | 32K | f16 | 972.57 t/s | 46.17 t/s | 36.51 s |
| Qwen3-Next 80B-A3B | 64K | f16 | 753.26 t/s | 38.18 t/s | 90.45 s |
| Qwen3-Next 80B-A3B | 128K | f16 | 497.79 t/s | 29.12 t/s | 268.54 s |

Takeaway: q4_0/q8_0 KV cache improves Qwen3.6 decode speed after a filled context, but slows prompt ingestion enough that full first-turn wall time is worse than f16. Use f16 for first-turn long prompts; use q4_0/q8_0 only when memory pressure or long continued generation matters more than ingest speed. The 128K f16 rows completed without truncation.

### Real-Corpus 64K Check

| Model | Prompt Type | Tokens | Prompt Eval | Decode After Fill | Wall Time |
|-------|-------------|--------|-------------|-------------------|-----------|
| Qwen3.6 35B-A3B | synthetic repeated token | 65,533 | 931.89 t/s | 41.44 t/s | 73.52 s |
| Qwen3.6 35B-A3B | real guide corpus | 65,120 | 706.21 t/s | 40.84 t/s | 95.41 s |
| Qwen3-Next 80B-A3B | synthetic repeated token | 65,532 | 753.26 t/s | 38.18 t/s | 90.45 s |
| Qwen3-Next 80B-A3B | real guide corpus | 63,507 | 504.53 t/s | 37.75 t/s | 129.40 s |

Takeaway: synthetic repeated-token prompts are optimistic for prompt-ingest speed. Real guide/documentation text slowed prompt eval by 24-33%, while decode-after-fill barely changed.

## Backend and Build Comparison

### Qwen3.5-35B-A3B Q4_K_M

| Backend / Build | pp512 | tg128 | Takeaway |
|-----------------|-------|-------|----------|
| Ollama Vulkan RADV, bundled older llama.cpp | ~457 | 47.4 | Easy, but slower |
| Vulkan RADV, b8298 | 868 | 52.06 | Baseline kyuz0-era direct path |
| Vulkan RADV, b8460 | **1080** | **64.85** | Best short-context result |
| ROCm HIP, b8301, HSA fix | 1059 | 47.87 | Old self-compiled ROCm build |
| ROCm HIP, b8460, HSA fix | 1047 | 54.67 | ROCm improved, still slower tg than RADV |

### AMDVLK Correction

AMDVLK is not recommended. It was installed during earlier testing and its ICD file silently overrode RADV for some direct `llama-bench` commands. That caused false "RADV regression" conclusions. Corrected current state:

- RADV wins on pp and tg with latest tested llama.cpp.
- AMDVLK should be uninstalled, not just ignored.
- Verify RADV in output: `(RADV STRIX_HALO) (radv)` and `shared memory: 65536`.
- AMDVLK output shows `(AMD open-source driver)` and `shared memory: 32768`.

## ROCm Status

ROCm is no longer "all broken" on kernel 6.19.x. It works when both environment variables are set before running ROCm/HIP binaries:

```bash
export HSA_OVERRIDE_GFX_VERSION=11.5.1
export HSA_ENABLE_SDMA=0
```

| Build | Kernel | pp128 | pp512 | tg128 | Notes |
|-------|--------|-------|-------|-------|-------|
| b8460 | 6.19.4 | **547** | **1047** | **54.67** | Current fair ROCm comparison |
| b8301 | 6.19.4 | 542 | 1059 | 47.87 | Old build, HSA fix |
| b8301 | 6.18.14 | 488 | 996 | 48.80 | Previous reference |

ROCm remains relevant for batch processing, hipBLASLt, vLLM experiments, and long-context/rocWMMA work. For current short-context MoE inference, Vulkan RADV is faster on the measured data.

### 2026-05-03 ROCm HIP Spot Check

| Model | Quant | ROCm pp512 | ROCm tg128 | Vulkan Reference |
|-------|-------|------------|------------|------------------|
| Qwen3.6 35B-A3B | UD-Q4_K_M | 1186.19 | 52.69 | Vulkan b9010: 1108.93 pp, 63.06 tg |
| Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 1285.32 | 73.69 | Vulkan b9010: 1346.27 pp, 97.24 tg |

The local HIP build is b8460 and requires `LD_LIBRARY_PATH=/usr/local/lib/ollama/rocm` plus the HSA override. It emitted a missing `TensileLibrary_lazy_gfx1151.dat` warning, so treat this as a ROCm HIP baseline, not a tuned rocBLASLt/rocWMMA result.

### 2026-05-07 HIP vs Vulkan Crossover Spot Check

The new local spot check separates prompt processing from token generation. It is not a perfect same-build fairness claim: Vulkan rows use b9010, while HIP rows use the available local b8460 HIP build. The result is still useful because it matches the direction of the independent same-build Strix Halo study in [`nabe2030/hip-vs-vulkan-evo-x2`](https://github.com/nabe2030/hip-vs-vulkan-evo-x2).

Structured data: [`data/backend_crossover.csv`](data/backend_crossover.csv). Full notes: [`BACKEND_CROSSOVER.md`](BACKEND_CROSSOVER.md).

| Model | Vulkan pp16384 | HIP pp16384 | Prompt-processing read | Vulkan tg128 | HIP tg128 | Generation read |
|-------|---------------:|------------:|------------------------|-------------:|----------:|-----------------|
| Qwen3.6 35B-A3B UD-Q4_K_M | 1038.14 | **1295.38** | HIP +24.8% | **62.24** | 52.72 | Vulkan +18.1% |
| Qwen3-Coder 30B-A3B UD-Q4_K_XL | 564.68 | **756.16** | HIP +33.9% | **93.67** | 72.19 | Vulkan +29.8% |

Takeaway: keep Vulkan/RADV as the default for generation-heavy chat/coding and low-concurrency API use, but keep ROCm/HIP available for prompt-heavy experiments such as RAG ingestion, long prompts, summarization, and future vLLM/AWQ/DFlash work.

Gemma 4 26B-A4B is a negative result on the local HIP path: Vulkan loaded and ran, but HIP b8460 failed to load the local GGUF. No local Gemma 4 HIP speed claim is made.

## Current Takeaways

1. Direct llama.cpp with Vulkan RADV is the fastest measured short-context path for Qwen MoE models.
2. Updating llama.cpp from b8298 to b8460 produced the largest improvement: +24% pp and +25% tg on Qwen3.5-35B-A3B.
3. AMDVLK caused false regression reports through ICD hijacking; keep it removed.
4. ROCm works on kernel 6.19.4 with HSA overrides. The latest measured generation rows are still behind Vulkan RADV, but HIP can win prompt processing.
5. Before any new benchmark campaign, keep `tuned accelerator-performance` active and log raw commands/results into a single dataset.
