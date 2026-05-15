# 2026-05-16 Lemonade ROCm b1259 Qwen3-Next spot check

Purpose: test whether the existing Lemonade `llamacpp-rocm` b1259/gfx1151 bundle changes the backend recommendation for Qwen3-Next 80B.

Environment:

- Tool bundle: `lemonade-llamacpp-rocm-b1259-gfx1151`
- `HSA_OVERRIDE_GFX_VERSION=11.5.1`
- `HSA_ENABLE_SDMA=0`
- `ROCBLAS_USE_HIPBLASLT=1`

Result:

| Backend | pp512 | tg128 | Read |
|---------|------:|------:|------|
| Vulkan/RADV llama.cpp b9172 | 751.70 | 59.06 | Best generation/decode path. |
| Lemonade ROCm b1259 | 800.38 | 49.57 | Better prompt processing, slower generation. |

Takeaway: keep Vulkan/RADV as the beginner/default path for chat, coding, and generation-heavy GGUF inference. Keep ROCm/HIP available for prompt-heavy experiments, server/batch work, and future vLLM/AWQ/DFlash paths.
