# 2026-05-16 latest-stack b9172 check

Purpose: test whether llama.cpp b9172 improved the current public headline rows on the Beelink GTR9 Pro while leaving the normal workspace session active.

Host state:

- Kernel: `6.19.4-061904-generic`
- Mesa/RADV: `26.0.6`
- llama.cpp: `b9172`, commit `1348f67c5`
- Normal workspace connectivity stayed up during the run
- Non-essential GUI/noise processes were paused during the run

Main results:

| Model | Quant | pp512 | tg128 | Read |
|-------|-------|------:|------:|------|
| Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 1371.69 | 94.43 | No new headline; b9049/b9010 remain faster. |
| Qwen3.6 35B-A3B | UD-Q4_K_M | 1094.52 | 61.52 | No new headline; b9049/b9010 remain faster. |
| Qwen3.6 35B-A3B | Q4_0 | 1242.63 | 79.14 | No new headline; b9049 remains faster. |
| Qwen3-Next 80B-A3B | UD-Q4_K_XL | 751.70 | 59.06 | New best 80B Qwen-family row after r20 confirmation. |
| gpt-oss-120b | MXFP4 | 718.61 | 54.69 | No new headline; b9049 remains slightly faster. |

The Qwen3-Next flag sweep found `-b 2048 -ub 1024` slightly best in the short r5 sweep; the final r20 confirmation used that setting.
