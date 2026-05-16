# Qwen3-Coder 30B Break-100 Sweep - 2026-05-16

Purpose: test whether current llama.cpp master plus smaller Qwen3-Coder 30B quants can reliably break the existing 96-97 t/s Strix Halo generation ceiling.

Host: Beelink GTR9 Pro, Ryzen AI MAX+ 395, Radeon 8060S, 128GB unified memory, Mesa RADV.

Build:

- llama.cpp commit: `b81c2cdd748dc2704d5989cf03936325554c12d3`
- llama-bench build number reported by CSV: `9179`
- Vulkan ICD: RADV via `/usr/share/vulkan/icd.d/radeon_icd.json`

Benchmark command shape:

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
llama-bench \
  -m <model.gguf> \
  -fa 1 -ngl 999 -mmp 0 \
  -p 512 -n 128 -r 20 -o csv
```

## Main r20 Results

| Quant | Raw CSV | pp512 | tg128 | Read |
|-------|---------|------:|------:|------|
| UD-Q4_K_XL | [`guide-r20/ud-q4-k-xl.csv`](guide-r20/ud-q4-k-xl.csv) | 1373.35 | 95.21 | Current master did not beat b9049/b9010 for the existing headline quant. |
| Q4_0 | [`guide-r20/q4-0.csv`](guide-r20/q4-0.csv) | 1497.65 | 96.65 | Faster prompt processing, but not a new generation headline. |
| Q4_K_S | [`guide-r20/q4-k-s.csv`](guide-r20/q4-k-s.csv) | 1387.22 | 97.22 | Fastest confirmed row in this sweep; effectively matches the old 97 t/s ceiling but does not prove stable 100 t/s. |
| IQ4_NL | [`guide-r20/iq4-nl.csv`](guide-r20/iq4-nl.csv) | 1367.49 | 93.49 | Slower decode here. |
| Q4_K_M | [`guide-r20/q4-k-m.csv`](guide-r20/q4-k-m.csv) | 1326.60 | 93.30 | Slower decode here. |

## Follow-Up Flag Checks

Best r5 rows reached 97.7 t/s, but the r20 confirmations fell back to 96.9-97.2 t/s:

| Setting | Raw CSV | pp512 | tg128 | Read |
|---------|---------|------:|------:|------|
| Q4_K_S, `--no-host 1` | [`q4-k-s-confirm-r20/nohost.csv`](q4-k-s-confirm-r20/nohost.csv) | 1385.89 | 97.16 | r5 improvement did not hold at r20. |
| Q4_K_S, `--no-host 1 --poll 0` | [`q4-k-s-confirm-r20/nohost-poll0.csv`](q4-k-s-confirm-r20/nohost-poll0.csv) | 1377.82 | 96.93 | r5 improvement did not hold at r20. |
| Q4_K_S, `-b 4096 -ub 2048` | [`q4-k-s-confirm-r20/b4096-ub2048.csv`](q4-k-s-confirm-r20/b4096-ub2048.csv) | 1360.52 | 97.20 | No stable improvement over guide flags. |
| Q4_K_S, `-b 4096 -ub 512` | [`q4-k-s-confirm-r20/b4096-ub512.csv`](q4-k-s-confirm-r20/b4096-ub512.csv) | 1385.86 | 96.70 | No stable improvement over guide flags. |

## Takeaway

This sweep did not find a reliable 100 t/s local Qwen3-Coder path on the measured Beelink. Q4_K_S on current master is the fastest confirmed new quant row at 97.22 t/s, but it is a speed-first/lower-quality quant candidate and should not replace the UD-Q4_K_XL recommendation for coding quality without a separate quality check.
