# 2026-05-03 Controlled Qwen3-Coder 30B Rerun

Purpose: verify whether the 95 t/s smoke-test result was publishable headline data.

## Preflight

| Item | Value |
|------|-------|
| System | Beelink GTR9 Pro |
| CPU/GPU | AMD Ryzen AI MAX+ 395 / Radeon 8060S |
| Kernel | 6.19.4-061904-generic |
| Vulkan driver | Mesa RADV 26.0.6, kisak-mesa PPA |
| llama.cpp | b9010 / `d05fe1d7d` |
| tuned profile | `accelerator-performance` |
| GPU clock | 2900 MHz selected |
| Model | `Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf` |
| Model size | 17.7 GB file / 16.5 GiB |

## Command

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
~/llama-cpp-latest/build-vulkan/bin/llama-bench \
  -m ~/models/Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf \
  -fa 1 -ngl 999 -mmp 0 -p 512 -n 128 -r 20 -o csv
```

## Results

| File | pp512 | pp stddev | tg128 | tg stddev |
|------|-------|-----------|-------|-----------|
| `qwen3-coder-30b-a3b-ud-q4-k-xl-b9010-r20.csv` | 1350.68 | 84.82 | 97.34 | 0.27 |
| `qwen3-coder-30b-a3b-ud-q4-k-xl-b9010-r20-run2.csv` | 1341.87 | 86.73 | 97.15 | 0.65 |
| **Average** | **1346.27** | - | **97.24** | - |

## Verdict

The 95 t/s smoke-test signal was real and slightly conservative. The current publishable headline for Qwen3-Coder 30B-A3B UD-Q4_K_XL on this b9010 Vulkan RADV stack is **97 t/s**.
