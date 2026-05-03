# 2026-05-03 Filled-KV Decode Benchmark

Purpose: measure generation speed after a long prompt has already filled a 32K or 64K KV cache. This answers a different question than `llama-bench` prompt-processing rows.

## Preflight

| Item | Value |
|------|-------|
| System | Beelink GTR9 Pro |
| CPU/GPU | AMD Ryzen AI MAX+ 395 / Radeon 8060S |
| Kernel | 6.19.4-061904-generic |
| Vulkan driver | Mesa RADV 26.0.6, kisak-mesa PPA |
| llama.cpp | b9010 / `d05fe1d7d` |
| Backend | Vulkan RADV |
| Server | `llama-server` |
| Prompt cache | disabled per request; server cache RAM set to 0 |
| tuned profile | `accelerator-performance` |
| GPU clock | 2900 MHz selected |

## Method

Each scenario started a fresh `llama-server` with one slot and continuous batching enabled. The request used a synthetic long prompt, `n_predict=128`, `temperature=0`, `top_k=1`, and `ignore_eos=true`. The API response was restricted to token counters so the long prompt was not written to result JSON.

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
~/llama-cpp-latest/build-vulkan/bin/llama-server \
  -m <model.gguf> \
  -fa on -ngl 999 --no-mmap \
  -c <prompt_tokens + 1152> -np 1 -cb \
  -b 2048 -ub 512 \
  -ctk <cache_k> -ctv <cache_v> \
  --no-cache-prompt --cache-ram 0 \
  --host 127.0.0.1 --port <port> --metrics --slots
```

Important caveat: prompt content was synthetic and repetitive. The most defensible comparisons are within this table, especially f16 vs q8_0/q4_0 under identical prompt construction.

## Results

| Model | Prompt | KV | Prompt Eval | Decode After Fill | Wall Time |
|-------|--------|----|-------------|-------------------|-----------|
| Qwen3.6 35B-A3B | 32K | f16 | 1216.64 t/s | 51.00 t/s | 29.50 s |
| Qwen3.6 35B-A3B | 32K | q8_0 | 1023.43 t/s | 54.59 t/s | 34.46 s |
| Qwen3.6 35B-A3B | 32K | q4_0 | 1048.70 t/s | 56.03 t/s | 33.58 s |
| Qwen3.6 35B-A3B | 64K | f16 | 931.89 t/s | 41.44 t/s | 73.52 s |
| Qwen3.6 35B-A3B | 64K | q8_0 | 731.22 t/s | 49.13 t/s | 92.33 s |
| Qwen3.6 35B-A3B | 64K | q4_0 | 750.04 t/s | 51.33 t/s | 89.97 s |
| Qwen3-Next 80B-A3B | 32K | f16 | 972.57 t/s | 46.17 t/s | 36.51 s |
| Qwen3-Next 80B-A3B | 64K | f16 | 753.26 t/s | 38.18 t/s | 90.45 s |

## Verdict

For Qwen3.6, q8_0 and q4_0 KV cache improve decode speed after the context is filled, but they slow prompt ingestion enough that full request wall time is worse than f16 in this benchmark. At 64K, q4_0 improves decode from 41.44 t/s to 51.33 t/s, but wall time rises from 73.52 s to 89.97 s.

Use f16 KV for first-turn long-prompt throughput. Consider q4_0/q8_0 KV only when memory pressure or long continued generation matters more than prompt-ingest speed.

Raw files:

- `filled-kv-decode-summary.csv`
- `filled-kv-decode-detail.csv`
- `*.log`
