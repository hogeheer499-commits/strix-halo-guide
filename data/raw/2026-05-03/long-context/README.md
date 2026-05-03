# 2026-05-03 Long-Context Prompt Scaling

Purpose: measure local long-prompt ingestion on the current b9010 Vulkan RADV stack. This complements the existing external long-context decode references from lhl.

## Preflight

| Item | Value |
|------|-------|
| System | Beelink GTR9 Pro |
| CPU/GPU | AMD Ryzen AI MAX+ 395 / Radeon 8060S |
| Kernel | 6.19.4-061904-generic |
| Vulkan driver | Mesa RADV 26.0.6, kisak-mesa PPA |
| llama.cpp | b9010 / `d05fe1d7d` |
| Backend | Vulkan RADV |
| KV cache | f16 |
| tuned profile | `accelerator-performance` |
| GPU clock | 2900 MHz selected |

## Method

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
~/llama-cpp-latest/build-vulkan/bin/llama-bench \
  -m <model.gguf> \
  -fa 1 -ngl 999 -mmp 0 \
  -p 4096,8192,16384,32768,65536 \
  -n 128 -r <3 or 5> -o csv
```

Important caveat: the `pp` rows measure prompt processing at the listed prompt lengths. The `tg128` row is a separate `n_prompt=0` generation row from the same run. These results do **not** measure generation speed after a fully occupied 32K/64K KV cache.

## Results

### Qwen3.6-35B-A3B UD-Q4_K_M

| Prompt Tokens | pp | Retained vs 4K |
|---------------|----|----------------|
| 4K | 1081.93 t/s | 100% |
| 8K | 1089.48 t/s | 101% |
| 16K | 1024.58 t/s | 95% |
| 32K | 908.61 t/s | 84% |
| 64K | 740.25 t/s | 68% |

Separate tg128 row from the same run: **57.84 t/s**.

### Qwen3-Next-80B-A3B UD-Q4_K_XL

| Prompt Tokens | pp | Retained vs 4K |
|---------------|----|----------------|
| 4K | 741.68 t/s | 100% |
| 8K | 735.50 t/s | 99% |
| 16K | 700.49 t/s | 94% |
| 32K | 644.82 t/s | 87% |
| 64K | 543.89 t/s | 73% |

Separate tg128 row from the same run: **55.58 t/s**.

## Verdict

Prompt ingestion remains strong through 64K on both tested MoE models. Qwen3.6 drops from 1082 t/s at 4K to 740 t/s at 64K. Qwen3-Next 80B drops from 742 t/s at 4K to 544 t/s at 64K, which is especially useful because it shows the 80B/256K model remains practical for large prompt ingestion on one 128GB Strix Halo box.

Open follow-up: measure decode speed after a filled 32K/64K KV cache and compare f16 KV against q8_0/q4_0 KV cache.
