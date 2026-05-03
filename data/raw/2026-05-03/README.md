# 2026-05-03 Controlled Benchmark Reruns

Purpose: verify whether the 95 t/s Qwen3-Coder smoke-test result was publishable headline data, then recheck the Qwen3.6 allrounder and Ollama easy path.

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

## Qwen3-Coder 30B Direct

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

Verdict: the 95 t/s smoke-test signal was real and slightly conservative. The current publishable headline for Qwen3-Coder 30B-A3B UD-Q4_K_XL on this b9010 Vulkan RADV stack is **97 t/s**.

## Qwen3.6 35B Direct

The direct-compatible local file available for this rerun was `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`.

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
~/llama-cpp-latest/build-vulkan/bin/llama-bench \
  -m ~/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf \
  -fa 1 -ngl 999 -mmp 0 -p 512 -n 128 -r 20 -o csv
```

| File | pp512 | pp stddev | tg128 | tg stddev |
|------|-------|-----------|-------|-----------|
| `qwen3.6-35b-a3b-ud-q4-k-m-b9010-r20.csv` | 1110.72 | 9.12 | 63.05 | 0.19 |
| `qwen3.6-35b-a3b-ud-q4-k-m-b9010-r20-run2.csv` | 1107.14 | 24.46 | 63.06 | 0.10 |
| **Average** | **1108.93** | - | **63.06** | - |

Verdict: the current UD-Q4_K_M result effectively matches the older plain Q4_K_M 64 t/s allrounder claim. The old "UD costs 13%" warning was not reproduced on this b9010 RADV stack.

### Plain Q4_K_M Direct Attempt

The Ollama `qwen3.6:35b-a3b` model blob has a GGUF header, but upstream `llama-bench` b9010 failed to load it:

```text
qwen35moe.rope.dimension_sections has wrong array length; expected 4, got 3
```

The failed attempt is kept as `qwen3.6-35b-a3b-q4-k-m-ollama-blob-b9010-r20.stderr`. A same-build direct plain Q4_K_M rerun still needs a direct-compatible GGUF.

## Ollama Qwen3.6 API

Ollama 0.21.2 was tested through `POST /api/generate` using `qwen3.6:35b-a3b`, `num_predict=128`, `temperature=0`, and `top_k=1`. The first run was cold after unload; the next 10 runs were warm.

| Phase | Runs | Prompt eval | Generation | Notes |
|-------|------|-------------|------------|-------|
| cold | 1 | 152.79 t/s | 50.90 t/s | 6.89 s load duration |
| warm | 10 | 157.90 t/s avg | 50.51 t/s avg | 50.23-50.75 t/s range, 0.15 t/s stddev |

Verdict: the old 45-46 t/s easy-path claim is superseded. Current Ollama Qwen3.6 generation is **50.5 t/s** warm, about 20-21% below direct llama-bench on this short-context workload.

## Qwen3.6 Multi-User llama-server

The same b9010 RADV stack was also tested with `llama-server`, continuous batching, and `-np 1/2/4/8/16`. Detailed raw output is under `multi-user/`.

| `-np` | Concurrent Requests | Aggregate tg | Avg per Request | Mean TTFT | Mean ITL |
|-------|---------------------|--------------|-----------------|-----------|----------|
| 1 | 1 | 59.21 t/s | 59.21 t/s | 0.117 s | 16.1 ms |
| 2 | 2 | 92.21 t/s | 46.11 t/s | 0.198 s | 20.3 ms |
| 4 | 4 | 130.81 t/s | 32.71 t/s | 0.237 s | 29.0 ms |
| 8 | 8 | 161.98 t/s | 20.25 t/s | 0.307 s | 47.4 ms |
| 16 | 16 | 165.98 t/s | 10.38 t/s | 0.547 s | 92.9 ms |

Verdict: the practical sweet spot for this Qwen3.6 local API workload is `-np 8`: about **162 t/s aggregate** with ~0.31 s TTFT. `-np 16` confirms the server can keep 16 simultaneous streams alive, but aggregate throughput plateaus while per-user speed drops sharply.

## Qwen3-Coder Multi-User llama-server

The same serving harness was repeated with Qwen3-Coder 30B-A3B UD-Q4_K_XL. Detailed raw output is under `multi-user-coder/`.

| `-np` | Concurrent Requests | Aggregate tg | Avg per Request | Mean TTFT | Mean ITL |
|-------|---------------------|--------------|-----------------|-----------|----------|
| 1 | 1 | 90.20 t/s | 90.20 t/s | 0.079 s | 10.6 ms |
| 2 | 2 | 121.65 t/s | 60.83 t/s | 0.133 s | 15.5 ms |
| 4 | 4 | 157.41 t/s | 39.36 t/s | 0.207 s | 24.0 ms |
| 8 | 8 | 173.16 t/s | 21.65 t/s | 0.382 s | 43.5 ms |
| 16 | 16 | 129.56 t/s | 8.10 t/s | 0.571 s | 119.9 ms |

Verdict: `-np 8` is the best measured setting for Qwen3-Coder serving. `-np 16` regresses and should not be used for throughput-focused coding workloads.

## Long-Context Prompt Scaling

Detailed raw output is under `long-context/`.

| Model | 4K pp | 8K pp | 16K pp | 32K pp | 64K pp | tg128 row |
|-------|-------|-------|--------|--------|--------|-----------|
| Qwen3.6 35B-A3B UD-Q4_K_M | 1081.93 | 1089.48 | 1024.58 | 908.61 | 740.25 | 57.84 |
| Qwen3-Next 80B-A3B UD-Q4_K_XL | 741.68 | 735.50 | 700.49 | 644.82 | 543.89 | 55.58 |

Verdict: both MoE models keep strong prompt-ingestion speed through 64K. This is prompt-processing data, not decode speed after a filled KV cache.

## Filled-KV Decode

Detailed raw output is under `filled-kv-decode/`.

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

Verdict: KV quantization helps Qwen3.6 decode speed after the cache is filled, but slows prompt ingestion enough that total request wall time is worse in this first-turn long-prompt benchmark. Use f16 for first-turn speed; consider q4_0/q8_0 only when memory pressure or long continued generation dominates.

### 128K f16 Follow-Up

Detailed raw output is under `filled-kv-decode-128k/`.

| Model | Prompt | KV | Prompt Eval | Decode After Fill | Wall Time | Truncated |
|-------|--------|----|-------------|-------------------|-----------|-----------|
| Qwen3.6 35B-A3B | 128K | f16 | 616.77 t/s | 32.23 t/s | 216.69 s | no |
| Qwen3-Next 80B-A3B | 128K | f16 | 497.79 t/s | 29.12 t/s | 268.54 s | no |

Verdict: both tested MoE models complete a 128K prompt plus 128 generated tokens without truncation on the current Vulkan RADV stack.
