# Benchmark Results - Current Snapshot

This file is the compact benchmark source-of-truth for numbers already published in the README. It does not add new tests; it reconciles the March and April measurements so old ROCm and driver notes do not contradict the current guide.

## Current System Snapshot

Live audit on 2026-05-01:

| Component | Current State |
|-----------|---------------|
| System | Beelink GTR9 Pro |
| CPU | AMD Ryzen AI MAX+ 395, 16C/32T |
| GPU | Radeon 8060S, gfx1151, RADV STRIX_HALO |
| RAM | 124GiB OS-visible unified memory |
| Kernel | 6.19.4-061904-generic |
| Mesa RADV | 26.0.6, kisak-mesa PPA |
| Ollama | 0.21.2 |
| AMDVLK | Removed |
| linux-firmware | 20240318.git3b128b60-0ubuntu2.27 |
| GPU clock | 2900 MHz selected |
| tuned | `accelerator-performance` active |

Historical benchmark runs below were measured on 2026-03-20, 2026-03-21, and 2026-04-26 with `tuned accelerator-performance` active. The 2026-05-01 readiness check now also confirms `tuned accelerator-performance` active, Mesa RADV 26.0.6, AMDVLK absent, linux-firmware safe, and GPU clock at 2900 MHz.

## Top-Line Model Results

| Model | Backend / Build | Quant | pp512 | tg128 | Notes |
|-------|-----------------|-------|-------|-------|-------|
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9010 | UD-Q4_K_XL | 1346 | **97.24** | Controlled May headline rerun |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b8460 | UD-Q4_K_XL | 1342 | **87.11** | Previous coding MoE headline |
| Qwen3.6 35B-A3B | Vulkan RADV, llama.cpp b9010 | UD-Q4_K_M | 1109 | **63.06** | Controlled May UD rerun |
| Qwen3.6 35B-A3B | Vulkan RADV, llama.cpp b8460 | Q4_K_M | 1064 | **63.76** | Recommended all-rounder |
| Qwen3.5 35B-A3B | Vulkan RADV, llama.cpp b8460 | Q4_K_M | 1080 | **64.85** | Used for backend/build comparison |
| Qwen3-Next 80B-A3B | Vulkan RADV, llama.cpp b8933 | UD-Q4_K_XL | 657 | **54.92** | 80B MoE, 256K context capable |
| Gemma 4 26B-A4B | Vulkan RADV, llama.cpp b8933 | UD-Q4_K_M | 1142 | **48.46** | Slower than Qwen MoE at similar active params |
| Llama 4 Scout 109B | Vulkan RADV, llama.cpp b8933 | Q4_K_M | 331 | **18.32** | 109B params on one mini PC |
| Llama 3.1 70B | Ollama Vulkan RADV | Q4_K_M | 22-80 | **4.7-4.9** | Dense 70B, bandwidth-bound |
| Qwen3 0.6B | Vulkan RADV, llama.cpp | Q8_0 | 13112 | **266** | Small-model speed ceiling |

## Ollama Vulkan

### Qwen3.6-35B-A3B, Ollama 0.21.2, Vulkan RADV

| Prompt Tokens | Prompt Eval | Generation | Notes |
|---------------|-------------|------------|-------|
| 19 | 158 t/s | **50.5 t/s** | Controlled 2026-05-03 API warm average across 10 runs |
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

## Current Takeaways

1. Direct llama.cpp with Vulkan RADV is the fastest measured short-context path for Qwen MoE models.
2. Updating llama.cpp from b8298 to b8460 produced the largest improvement: +24% pp and +25% tg on Qwen3.5-35B-A3B.
3. AMDVLK caused false regression reports through ICD hijacking; keep it removed.
4. ROCm works on kernel 6.19.4 with HSA overrides, but the latest measured short-context tg is still behind Vulkan RADV.
5. Before any new benchmark campaign, keep `tuned accelerator-performance` active and log raw commands/results into a single dataset.
