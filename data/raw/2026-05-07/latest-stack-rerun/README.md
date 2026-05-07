# 2026-05-07 Latest Stack Rerun

Purpose: check whether current upstream llama.cpp changes after b9010 materially change the short-context Vulkan/RADV headline path on the primary Beelink GTR9 Pro.

This is smoke/spot-check evidence, not a replacement for the public headline rows. The run used one `-r 20` pass per model per build. T3 and Hermes were left running. High-noise `ffmpeg`, Zoom, and RustDesk user processes were paused with `SIGSTOP` during the measurements.

## Builds

| Build | Commit | Path | Notes |
|-------|--------|------|-------|
| b9010 | `d05fe1d7d` | `/home/hoge-heer/llama-cpp-latest/build-vulkan/bin/llama-bench` | Current published llama.cpp build |
| b9049 | `2496f9c14` | `/home/hoge-heer/llama-cpp-upstream-2026-05-07/build-vulkan/bin/llama-bench` | Separate upstream worktree, built for this spot check |

## Results

All runs used:

```bash
AMD_VULKAN_ICD=RADV
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json
-fa 1 -ngl 999 -mmp 0 -p 512 -n 128 -r 20 -o csv
```

| Build | Model | Quant | pp512 | tg128 | Interpretation |
|-------|-------|-------|-------|-------|----------------|
| b9010 | Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 1376.68 | 94.12 | Baseline repeat before upstream worktree test |
| b9049 | Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 1381.55 | 95.04 | No meaningful tg change versus b9010 |
| b9010 | Qwen3.6 35B-A3B | UD-Q4_K_M | 1093.07 | 61.82 | Baseline repeat before upstream worktree test |
| b9049 | Qwen3.6 35B-A3B | UD-Q4_K_M | 1094.19 | 61.65 | No meaningful tg change versus b9010 |

## Takeaway

llama.cpp b9049 does not change the short-context Vulkan/RADV conclusion for these two Qwen MoE models. The guide should not claim a new speedup from this update. The next higher-value work is the HIP vs Vulkan long-prompt crossover and vLLM AWQ/DFlash reproduction.

