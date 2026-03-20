# Benchmark Results — 2026-03-20

## System Configuration
- Kernel: 6.19.4-061904-generic
- Mesa RADV: 26.0.2 (kisak-mesa PPA)
- Ollama: 0.18.2
- tuned: accelerator-performance (active)
- GPU clock: 2900 MHz (stable, no clock bug)
- Backend: Vulkan (RADV) via Ollama

## Ollama Vulkan (RADV Mesa 26.0.2)

### qwen3.5:35b-a3b (~23GB, MoE)

| Prompt | Tokens | pp (t/s) | tg (t/s) | Gen Tokens | Prev pp | Prev tg | Delta tg |
|--------|--------|----------|----------|------------|---------|---------|----------|
| "hello how are you" | 14 | 121.3 | 48.0 | 390 | ~267 @56t | 45.8 | **+4.8%** |
| "explain backpropagation..." | 23 | 182.3 | 47.5 | 1963 | - | 45.5 | **+4.4%** |
| Long arch review prompt | 122 | 456.7 | 47.4 | 2498 | 467 @201t | 45.5 | **+4.2%** |

**Analysis:** Token generation improved ~4-5% across all prompt lengths. Likely from Mesa 26.0.1→26.0.2 + tuned being active. Prompt processing scales linearly with token count as expected.

### qwen3-coder-next (~51GB, dense)

| Prompt | Tokens | pp (t/s) | tg (t/s) | Gen Tokens | Prev pp | Prev tg | Delta tg |
|--------|--------|----------|----------|------------|---------|---------|----------|
| "hello how are you" | 12 | 90.7 | 39.1 | 60 | 96 @12t | 38 | **+2.9%** |
| "explain backpropagation..." | 21 | 129.5 | 38.4 | 631 | 136 @54t | 37 | **+3.8%** |
| Long arch review prompt | 120 | 301.2 | 37.9 | 3549 | - | - | NEW |

**Analysis:** pp slightly lower (-5%), tg slightly higher (+3%). The pp drop may be measurement variance due to different prompt tokenization.

### qwen3-coder:30b-a3b-q8_0 (~32GB, MoE, Q8_0)

| Prompt | Tokens | pp (t/s) | tg (t/s) | Gen Tokens |
|--------|--------|----------|----------|------------|
| "hello how are you" | 12 | 118.3 | **51.4** | 38 |
| "explain backpropagation..." | 21 | 205.2 | **51.3** | 344 |

**Analysis:** NEW model, not previously tested. Fastest generation speed at 51.3-51.4 t/s. The Q8_0 quantization trades size (32GB vs 23GB) for higher quality while maintaining excellent speed.

### llama2:latest (~3.8GB, dense 7B)

| Prompt | Tokens | pp (t/s) | tg (t/s) | Gen Tokens |
|--------|--------|----------|----------|------------|
| "hello how are you" | 24 | 384.6 | **52.0** | 66 |

### qwen3.5-nothinker (~23GB, MoE, no-think variant)

| Prompt | Tokens | pp (t/s) | tg (t/s) | Gen Tokens |
|--------|--------|----------|----------|------------|
| "hello how are you" | 14 | 127.1 | 47.4 | 1110 |

**Analysis:** Same speed as thinking variant — expected since it's the same model architecture.

### qwen2.5vl:7b (~6GB, vision model)

| Prompt | Tokens | pp (t/s) | tg (t/s) | Gen Tokens |
|--------|--------|----------|----------|------------|
| "hello how are you" | 23 | 81.7 | 21.4 | 26 |

**Analysis:** Vision models have additional overhead from image encoder components, even on text-only prompts.

## ROCm HIP (llama.cpp via Distrobox)

### Status: ALL BROKEN on Kernel 6.19.4

Every ROCm container segfaults immediately:
- kyuz0 pre-built (rocm-7.2): Segfault
- kyuz0 pre-built (rocm-6.4.4): ROCm error in ggml_cuda_mul_mat_q
- Self-compiled (b8301): Segfault
- Build-opt: Segfault

**Root cause:** GPU detected as "gfx1100 (0x1100)" instead of "gfx1151". Kernel 6.19.4 appears to have changed GPU identification, breaking ROCm compatibility.

**Previous results (kernel 6.18.14, for reference):**

| Build | Model | pp128 | pp512 | tg128 |
|-------|-------|-------|-------|-------|
| Self-compiled b8301 FA on | Qwen3.5-35B-A3B Q4_K_M | 488 | 996 | 48.8 |
| kyuz0 b8298 FA on | Qwen3.5-35B-A3B Q4_K_M | 306 | 520 | 55.3 |
| kyuz0 b8298 FA off | Qwen3.5-35B-A3B Q4_K_M | 352 | 524 | 53.8 |
| kyuz0 b8189 FA+hipBLASLt | Llama 2 7B Q4_K_M | 1163 | 1261 | 45.07 |

## Summary of Changes vs Previous

| Metric | Previous | Current | Change |
|--------|----------|---------|--------|
| Vulkan tg (qwen3.5:35b-a3b) | 45.5-45.8 | 47.4-48.0 | **+4-5%** |
| Vulkan tg (qwen3-coder-next) | 37-38 | 37.9-39.1 | **+3%** |
| Mesa version | 26.0.1 | 26.0.2 | Updated |
| Kernel | 6.18.14 | 6.19.4 | **Breaks ROCm** |
| ROCm HIP | Working | **BROKEN** | Regression |
| tuned | Not running | Active | Fixed |
| GPU clock bug | Intermittent | Not present | Fixed/stable |

## Key Takeaways
1. Vulkan performance improved ~4% (Mesa update + tuned)
2. Kernel 6.19.4 breaks ALL ROCm containers — stay on 6.18.x for ROCm
3. qwen3-coder:30b-a3b-q8_0 is the fastest model at 51+ t/s
4. GPU clock is stable at 2900 MHz (no more stuck at 900 MHz bug)
