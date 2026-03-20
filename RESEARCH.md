# Research Findings — March 2026

## Source 1: kyuz0/amd-strix-halo-toolboxes

**Stable Configuration:**
- OS: Fedora 42/43
- Kernel: 6.18.6-200+ (minimum 6.18.4)
- Firmware: 20260110
- Kernel params: `iommu=pt amdgpu.gttsize=126976 ttm.pages_limit=32505856`

**CRITICAL WARNING:** linux-firmware-20251125 breaks ROCm on Strix Halo.

**LLVM Workaround:** `-mllvm --amdgpu-unroll-threshold-local=600` for ROCm 7.11. NOT needed for nightly builds.

**Container Tags:** vulkan-amdvlk, vulkan-radv, rocm-6.4.4, rocm-7.2, rocm7-nightlies

**rocWMMA:** Performance degrades at long context. Library rewrite pending. lhl has tuned branch.

**Mandatory flags:** `-fa 1` and `--no-mmap` always on Strix Halo.

## Source 2: lhl/strix-halo-testing

**IOMMU:**
- `amd_iommu=off`: ~6% faster memory reads (234 vs 221 GB/s)
- `iommu=pt`: NO speed benefit over default
- CONFLICT: kyuz0 recommends `iommu=pt`, lhl shows `off` is faster

**Vulkan vs ROCm at Long Context (gpt-oss-120b tg32):**
- @2K: Vulkan AMDVLK 50.05, ROCm 46.56
- @8K: Vulkan 43.15, ROCm 32.65
- @16K: Vulkan 38.46, ROCm 25.50
- @32K: Vulkan 31.54, ROCm 17.82 (Vulkan 1.8X faster)
- lhl's tuned rocWMMA @32K: 36.43 (2X standard ROCm!)

**Best Backend Per Model:**
- Best pp and best tg often use DIFFERENT backends for the same model
- AMDVLK generally better pp, RADV sometimes better tg
- ROCm best for very small and very large dense models pp
- Vulkan AMDVLK best for mid-size models pp

**Optimal ubatch sizes:**
- AMDVLK: `-ub 512`
- RADV: `-ub 1024`
- ROCm: `-ub 2048`

## Source 3: kyuz0/amd-strix-halo-vllm-toolboxes

**vLLM works on gfx1151** with patches:
1. MIOpen Encoder hang fix (disable encoder profiling for vision models)
2. Qwen3.5 block_size validation fix (remove BlockSize whitelist)

**RDMA Clustering:**
- 2x Framework Desktop + Intel E810 100GbE = 256GB unified
- ~50 Gbps, ~5 us latency
- Needs `pci=realloc` kernel param, MTU 9000

## Source 4: ROCm/ROCm#6027 (Qwen3.5 Hang Bug)

**Status:** OPEN (as of 2026-03-18)
- Qwen3.5 hangs during load_tensors on gfx1151
- AMD successfully ran with TheRock 7.13.0a20260316+ nightlies
- Workaround: `--batch-size 128 --ubatch-size 32 --flash-attn off --n-gpu-layers 1`

## Source 5: Web Search — Recent Developments (Jan-Mar 2026)

**ROCm 7.2 Regression (Feb 28, 2026):**
- 73% performance loss with GGML_HIP_ROCWMMA_FATTN=ON
- Do NOT use rocWMMA FA on upstream llama.cpp
- lhl's custom branch is the exception

**Lemonade 10.0 (March 11, 2026):**
- First Linux NPU support via FastFlowLM 0.9.35
- Up to 256k context, ONNX format required
- Limited to ~8B models

**DGX Spark vs Strix Halo:**
- tg32 @120B model: DGX 56 t/s vs Strix Halo 47-53 t/s
- Price: DGX $3,999 vs Strix Halo ~$2,199
- Strix Halo has 2X better CPU performance

**Upcoming Hardware:**
- Gorgon Halo (Ryzen AI Max 400): Q4 2026, same arch, higher clocks
- Medusa Halo (Max 500): LPDDR6, ~80% more memory bandwidth

**AMD Trillion-Parameter LLM:**
- 4-node Framework Desktop cluster running Kimi K2.5 (1T params)
- Distributed llama.cpp inference

**Strix Halo Wiki Deep Context Benchmarks (Qwen3-30B-A3B, 130k tokens):**
- Vulkan RADV: pp512 17 t/s, tg128 13 t/s
- ROCm: pp512 41 t/s, tg128 5 t/s
- ROCm rocm-wmma-tune: pp512 51 t/s, tg128 13 t/s

## Our Own Findings

**Kernel 6.19.4 breaks ALL ROCm containers:**
- GPU detected as gfx1100 instead of gfx1151
- Segfault on all builds (kyuz0, self-compiled, optimized)
- Stay on 6.18.x for ROCm

**Vulkan performance improved ~4-5%:**
- Mesa 26.0.1 → 26.0.2 + tuned profile
- qwen3.5:35b-a3b tg: 45.8 → 48.0 t/s
- qwen3-coder-next tg: 38 → 39.1 t/s
