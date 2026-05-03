# 2026-05-03 ROCm HIP Spot Check

Purpose: verify the current local ROCm/HIP path against the same May benchmark state without changing the system globally.

## Preflight

| Item | Value |
|------|-------|
| System | Beelink GTR9 Pro |
| CPU/GPU | AMD Ryzen AI MAX+ 395 / Radeon 8060S |
| Kernel | 6.19.4-061904-generic |
| llama.cpp HIP build | b8460 / `b1c70e2e5` |
| Runtime library path | `/usr/local/lib/ollama/rocm` |
| ROCm device | Radeon 8060S Graphics, gfx1151 |
| Required env | `HSA_OVERRIDE_GFX_VERSION=11.5.1`, `HSA_ENABLE_SDMA=0` |

## Method

```bash
LD_LIBRARY_PATH=/usr/local/lib/ollama/rocm \
HSA_OVERRIDE_GFX_VERSION=11.5.1 \
HSA_ENABLE_SDMA=0 \
ROCBLAS_USE_HIPBLASLT=1 \
/home/hoge-heer/llama-cpp-latest/build-hip/bin/llama-bench \
  -m <model.gguf> \
  -fa 1 -ngl 999 -mmp 0 -p 512 -n 128 -r 10 -o csv
```

Important caveat: the run emitted:

```text
rocblaslt error: Cannot read "TensileLibrary_lazy_gfx1151.dat": No such file or directory
```

Treat this as a current ROCm HIP baseline, not a tuned rocBLASLt/rocWMMA result.

## Results

| Model | Quant | pp512 | tg128 | Vulkan Reference |
|-------|-------|-------|-------|------------------|
| Qwen3.6 35B-A3B | UD-Q4_K_M | 1186.19 | 52.69 | Vulkan b9010: 1108.93 pp, 63.06 tg |
| Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 1285.32 | 73.69 | Vulkan b9010: 1346.27 pp, 97.24 tg |

## Verdict

ROCm HIP is usable with the HSA override and local ROCm runtime path, but it is not the best short-context generation path for these MoE models. Qwen3.6 ROCm improves pp versus the Vulkan b9010 UD rerun, but tg is about 16% lower. Qwen3-Coder ROCm is much slower on tg than Vulkan b9010.

Use Vulkan RADV for current short-context generation speed. Keep ROCm for vLLM, HIP-specific serving, and future long-context/rocWMMA experiments.
