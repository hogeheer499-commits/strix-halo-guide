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
