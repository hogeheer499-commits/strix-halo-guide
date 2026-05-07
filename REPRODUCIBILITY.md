# Reproducibility

This file is the checklist for copying, rerunning, or challenging benchmark claims from the guide. The README is the human-facing entry point; structured CSVs and raw logs are the source of truth.

## Scope

Current headline numbers were measured on one primary Strix Halo machine unless a row says otherwise. Treat them as local measurements, not universal hardware guarantees.

The public claim index is [`data/headline_claims.csv`](data/headline_claims.csv). Each row maps a README headline claim to structured data, raw evidence, chart path, and notes.

## Primary Machine

| Component | Measured state |
|-----------|----------------|
| System | Beelink GTR9 Pro |
| CPU | AMD Ryzen AI MAX+ 395, 16 cores / 32 threads |
| GPU | Radeon 8060S, `gfx1151`, RADV STRIX_HALO |
| Memory | 128GB LPDDR5X-8000 unified memory; about 124GiB OS-visible |
| OS | Ubuntu 24.04 |
| Kernel | `6.19.4-061904-generic` |
| Mesa/RADV | Mesa 26.0.6 from kisak-mesa PPA |
| llama.cpp | b9049 `2496f9c14` for the current direct Vulkan/RADV headline rerun; b9010 `d05fe1d7d` kept as previous peak evidence |
| Ollama | 0.23.1 for the current Ollama API baseline |
| BIOS UMA | 512MB for the measured local setup |
| IOMMU | Disabled for the measured local setup |
| AMDVLK | Removed; RADV should be the selected Vulkan ICD |
| Power profile | `tuned` profile `accelerator-performance` active |
| GPU clock | 2900 MHz selected during current readiness checks |
| Firmware | `linux-firmware` 20240318.git3b128b60-0ubuntu2.27 |

## Before Running

Record the host state before every publishable run:

```bash
date -Is
uname -a
tuned-adm active
free -h
vulkaninfo --summary | sed -n '/Devices:/,$p' | sed -n '1,40p'
cat /sys/class/drm/card*/device/pp_dpm_sclk
dpkg -l | grep -E 'amdvlk|mesa-vulkan-drivers|linux-firmware|rocm|hip' || true
```

Then run the local hygiene check:

```bash
scripts/check_benchmark_cleanliness.sh
```

The hygiene script is read-only. On the maintainer workstation it also checks local workflow dependencies. If you are reproducing on another machine, record equivalent background load, remote desktop state, VMs, local AI servers, power profile, GPU clock, and selected Vulkan ICD.

## Benchmark Commands

Direct Vulkan/RADV `llama-bench` shape used for the short-context headline rows:

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
~/llama-cpp-upstream-2026-05-07/build-vulkan/bin/llama-bench \
  -m ~/models/Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf \
  -fa 1 -ngl 999 -mmp 0 -p 0 -n 128 -r 20 -o csv
```

OpenAI-compatible server feature probe:

```bash
python3 scripts/check_openai_server_features.py \
  --url http://127.0.0.1:8080 \
  --model MODEL_NAME \
  --output data/raw/YYYY-MM-DD/server/features.json
```

OpenAI-compatible streaming throughput harness:

```bash
python3 scripts/benchmark_openai_server.py \
  --url http://127.0.0.1:8080 \
  --model MODEL_NAME \
  --np 8 \
  --tokens 128 \
  --reps 3 \
  --detail data/raw/YYYY-MM-DD/server/detail-np8.csv \
  --summary data/raw/YYYY-MM-DD/server/summary-np8.csv
```

Generate charts from structured CSVs:

```bash
python3 scripts/generate_charts.py
```

## Raw Data Map

| Claim family | Structured data | Raw logs | Charts / notes |
|--------------|-----------------|----------|----------------|
| Public headline claim index | [`data/headline_claims.csv`](data/headline_claims.csv) | Row-specific raw paths | Row-specific chart paths or `n/a` |
| Short-context Vulkan/RADV and Ollama headline rows | [`data/benchmarks.csv`](data/benchmarks.csv) | [`data/raw/2026-05-07/latest-stack-rerun/clean-b9049-rerun/`](data/raw/2026-05-07/latest-stack-rerun/clean-b9049-rerun/), [`data/raw/2026-05-03/`](data/raw/2026-05-03/) | [`BENCHMARKS.md`](BENCHMARKS.md), [`charts/backend_spot_check.svg`](charts/backend_spot_check.svg) |
| gpt-oss-120b local load and speed check | [`data/benchmarks.csv`](data/benchmarks.csv) | [`data/raw/2026-05-07/gpt-oss-120b-local-attempt/`](data/raw/2026-05-07/gpt-oss-120b-local-attempt/) | [`BENCHMARKS.md`](BENCHMARKS.md) |
| HIP/Vulkan workload split spot check | [`data/backend_crossover.csv`](data/backend_crossover.csv) | [`data/raw/2026-05-07/hip-vs-vulkan-crossover/`](data/raw/2026-05-07/hip-vs-vulkan-crossover/) | [`BACKEND_CROSSOVER.md`](BACKEND_CROSSOVER.md), [`charts/backend_crossover_prefill.svg`](charts/backend_crossover_prefill.svg), [`charts/backend_crossover_generation.svg`](charts/backend_crossover_generation.svg) |
| Server shootout and concurrency sweeps | [`data/server_shootout.csv`](data/server_shootout.csv) | [`data/raw/2026-05-05/server-shootout/full-sweep-qwen36-workstation-baseline/`](data/raw/2026-05-05/server-shootout/full-sweep-qwen36-workstation-baseline/) | [`SERVER_SHOOTOUT.md`](SERVER_SHOOTOUT.md) |
| `llama-server` multi-user behavior | [`data/multi_user.csv`](data/multi_user.csv) | [`data/raw/2026-05-03/multi-user/`](data/raw/2026-05-03/multi-user/), [`data/raw/2026-05-03/multi-user-coder/`](data/raw/2026-05-03/multi-user-coder/) | [`charts/multi_user_aggregate.svg`](charts/multi_user_aggregate.svg) |
| Long-context prompt scaling | [`data/long_context.csv`](data/long_context.csv) | [`data/raw/2026-05-03/long-context/`](data/raw/2026-05-03/long-context/) | [`charts/long_context_prompt.svg`](charts/long_context_prompt.svg) |
| Filled-KV decode and KV-cache tradeoffs | [`data/filled_kv_decode.csv`](data/filled_kv_decode.csv) | [`data/raw/2026-05-03/filled-kv-decode/`](data/raw/2026-05-03/filled-kv-decode/), [`data/raw/2026-05-03/filled-kv-decode-128k/`](data/raw/2026-05-03/filled-kv-decode-128k/), [`data/raw/2026-05-03/filled-kv-decode-real-corpus/`](data/raw/2026-05-03/filled-kv-decode-real-corpus/) | [`charts/filled_kv_decode.svg`](charts/filled_kv_decode.svg), [`charts/kv_cache_tradeoff.svg`](charts/kv_cache_tradeoff.svg), [`charts/real_vs_synthetic.svg`](charts/real_vs_synthetic.svg) |
| Smoke-test evidence | [`data/smoke_tests.csv`](data/smoke_tests.csv) | Run-specific notes linked from the CSV | [`SMOKE_TESTS.md`](SMOKE_TESTS.md) |

## Claim Hygiene

Do not copy these claims without matching setup. Performance depends on exact hardware SKU, RAM configuration, BIOS UMA, IOMMU, firmware, kernel, Mesa/RADV, ROCm, Vulkan ICD selection, power profile, GPU clocks, thermal state, backend commit/build flags/container image, model file, quant type, model hash/path, context length, prompt length, generated token count, batch size, parallel slots, request concurrency, API endpoint, environment variables, and background system load.

If your setup differs, rerun the benchmark scripts and cite the date, command, CSV, raw log, chart, model file, and backend version with any copied claim.
