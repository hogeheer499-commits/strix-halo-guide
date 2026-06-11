# Gemma 4 QAT Q4_0 Numbers

This file captures the full measured numbers for the Gemma 4 QAT Q4_0 runs across three model sizes (12B, 26B-A4B, 31B) on the Strix Halo APU, including plain Vulkan baselines, non-QAT MTP heads, and matched QAT MTP heads.

Later status note: Atomic PR #26 has since merged a Gemma 4 MTP `PARALLEL=2` fix. These numbers predate that merge. Treat the `PARALLEL=2` crash notes below as historical caveats until fresh post-merge 1-slot and 2-slot measurements are available.

## Model And Run Context

| Field | Value |
|---|---|
| Models tested | Gemma 4 12B QAT Q4_0, Gemma 4 26B-A4B QAT Q4_0, Gemma 4 31B QAT Q4_0 |
| Architecture | `gemma4` (MoE for 26B-A4B, dense for 12B and 31B) |
| Backend | llama.cpp b9360 Vulkan/RADV (`build-vulkan-b9360`) |
| Runtime for MTP rows | Atomic llama.cpp TurboQuant fork (assistant-head `gemma4_assistant` MTP path) |
| Serve port (plain) | `:8113` (12B), `:8127` (26B-A4B), `:8133` (31B) |
| Serve port (MTP block3 non-QAT) | `:8135` (12B), `:8130` (26B-A4B), `:8134` (31B) |
| Serve port (MTP qathead) | `:8139` (12B), `:8140` (26B-A4B), `:8137` (31B) |
| GTT ceiling | 96 GiB |
| Gate context | 12,288 (MTP rows); 32,768 (plain rows) |
| Bench date | 2026-06-06 |
| Source logs | `evals/bench/results/` — one subdirectory per run |

## Model Sizes On Disk

| Model | File | Disk size |
|---|---|---:|
| Gemma 4 12B QAT Q4_0 | `gemma-4-12b-it-qat-q4_0.gguf` | 6,975,877,728 bytes / **6.50 GiB** |
| Gemma 4 26B-A4B QAT Q4_0 | `gemma-4-26B_q4_0-it.gguf` | 14,439,361,440 bytes / **13.45 GiB** |
| Gemma 4 31B QAT Q4_0 | `gemma-4-31B_q4_0-it.gguf` | 17,650,999,456 bytes / **16.44 GiB** |

## MTP Assistant Heads Used

| Main model | Head type | Head file | Approx size |
|---|---|---|---:|
| Gemma 4 12B QAT | Non-QAT (block3 row) | `gemma-4-12B-it-assistant-MTP-Q4_K_M.gguf` | ~313 MiB |
| Gemma 4 12B QAT | Matched QAT head | `gemma-4-12B-it-qat-assistant-MTP-Q8_0.gguf` | ~313 MiB |
| Gemma 4 26B-A4B QAT | Non-QAT (block3 row) | `gemma-4-26B-A4B-it-assistant.Q4_K_M.gguf` | ~310 MiB |
| Gemma 4 26B-A4B QAT | Matched QAT head | `gemma-4-26B-A4B-it-qat-assistant-MTP-Q8_0.gguf` | ~310 MiB |
| Gemma 4 31B QAT | Non-QAT (block3 row) | `gemma-4-31B-it-assistant.Q4_K_M.gguf` | ~337 MiB |
| Gemma 4 31B QAT | Matched QAT head | `gemma-4-31B-it-qat-assistant-MTP-Q8_0.gguf` | ~337 MiB |

QAT head source repos: `google/gemma-4-{12B,26B-A4B,31B}-it-qat-q4_0-unquantized-assistant` — converted to Atomic `gemma4_assistant` GGUF `Q8_0`.

## Measured Numbers — Gemma 4 12B QAT Q4_0

| Metric | Plain F16 KV | MTP block3 Q8KV (non-QAT head) | MTP qathead Q8 Q8KV | Source |
|---|---:|---:|---:|---|
| Time-to-listening | ~4 s | ~6 s | ~10 s | bench.md |
| Prefill (cache-busted) | **666.5 tok/s** | 555.8 tok/s | 539.9 tok/s | bench.md |
| Decode (single-stream) | 25.7 tok/s | 44.6 tok/s | **45.6 tok/s** | bench.md |
| Wall time std (1150-in/2000-out) | 79.5 s | 46.9 s | **46.0 s** | bench.md |
| 2-slot aggregate | **47.6 tok/s** | 41.7 tok/s | 43.5 tok/s | bench.md |
| MTP acceptance | N/A | 71.3% | **78.4%** | bench.md / tg_probe.json |
| MTP effective decode | N/A | 43.5 tok/s | **43.9 tok/s** | bench.md |

Single-stream speedup (plain → qathead MTP): **+77.4%** decode, wall time **42.1% faster**.

## Measured Numbers — Gemma 4 26B-A4B QAT Q4_0

| Metric | Plain F16 KV | MTP block3 Q8KV (non-QAT head) | MTP qathead Q8 Q8KV | Source |
|---|---:|---:|---:|---|
| Time-to-listening | ~4 s | ~18 s | ~18 s | bench.md |
| Prefill (cache-busted) | **1194.4 tok/s** | 714.4 tok/s | 729.3 tok/s | bench.md |
| Decode (single-stream) | 59.4 tok/s | 71.0 tok/s | **71.4 tok/s** | bench.md |
| Wall time std (1150-in/2000-out) | 34.6 s | 29.8 s | **29.6 s** | bench.md |
| 2-slot aggregate | **90.9 tok/s** | 55.6 tok/s | 62.5 tok/s | bench.md |
| MTP acceptance | N/A | 56.9% | **91.8%** | bench.md / tg_probe.json |
| MTP effective decode | N/A | 56.8 tok/s | **71.4 tok/s** | bench.md |

Single-stream speedup (plain → qathead MTP): **+20.2%** decode, wall time **14.5% faster**. The QAT head raises acceptance from 56.9% → 91.8% — the head mismatch was the entire acceptance gap.

## Measured Numbers — Gemma 4 31B QAT Q4_0

| Metric | Plain Q8 KV | MTP block3 F16KV (non-QAT head) | MTP qathead Q8 F16KV | Source |
|---|---:|---:|---:|---|
| Time-to-listening | ~8 s | ~10 s | ~20 s | bench.md |
| Prefill (cache-busted) | **204.2 tok/s** | 118.0 tok/s | 203.6 tok/s | bench.md |
| Decode (single-stream) | 11.0 tok/s | 15.4 tok/s | **19.1 tok/s** | bench.md |
| Wall time std (1150-in/2000-out) | 187.4 s | 139.6 s | **110.4 s** | bench.md |
| 2-slot aggregate | 20.0 tok/s | 15.9 tok/s | **18.9 tok/s** | bench.md |
| MTP acceptance | N/A | 42.5% | **60.4%** | bench.md / tg_probe.json |
| MTP effective decode | N/A | 16.2 tok/s | 19.0 tok/s | bench.md |

Single-stream speedup (plain → qathead MTP): **+73.6%** decode, wall time **41.1% faster**. 31B is dense-architecture bandwidth-limited at ~11 tok/s plain; MTP recovers significant ground.

## Cross-Model Summary (Best Row Per Model)

| Model | Best lane | Decode | Wall std | 2-slot agg | MTP acc |
|---|---|---:|---:|---:|---:|
| Gemma 4 12B QAT | MTP qathead Q8 Q8KV | **45.6 tok/s** | 46.0 s | 43.5 tok/s | 78.4% |
| Gemma 4 26B-A4B QAT | MTP qathead Q8 Q8KV | **71.4 tok/s** | 29.6 s | 62.5 tok/s | **91.8%** |
| Gemma 4 31B QAT | MTP qathead Q8 F16KV | **19.1 tok/s** | 110.4 s | 18.9 tok/s | 60.4% |
| Gemma 4 26B-A4B QAT | Plain F16 KV (best concurrency) | 59.4 tok/s | 34.6 s | **90.9 tok/s** | N/A |

The 26B-A4B plain row wins the submitted 2-slot aggregate (90.9 tok/s) because PARALLEL=2 was stable for the plain server in this bundle. The submitted MTP rows were capped at PARALLEL=1 by an Atomic crash on Gemma 4 MTP graph init with two slots. Atomic PR #26 later merged a fix, so fresh post-merge aggregate numbers are pending.

## DRAFT_BLOCK_SIZE Sweep (Short Probe, Non-QAT Heads)

These are shorter probe runs from `gemma-qat-mtp-qathead-block-sweep.jsonl`, not full canonical benches. Useful for tuning block size, not directly wall-comparable to the bench.md rows.

| Model | block | Decode (probe) | Acceptance |
|---|---:|---:|---:|
| Gemma 4 12B QAT | 2 | 41.15 tok/s | 96.5% |
| Gemma 4 12B QAT | 3 | 50.39 tok/s | 93.4% |
| Gemma 4 26B-A4B QAT | 2 | 62.19 tok/s | 71.7% |
| Gemma 4 26B-A4B QAT | 3 | 79.62 tok/s | 97.6% |

`DRAFT_BLOCK_SIZE=3` is the chosen default. Both models show higher throughput at block=3 despite slightly lower acceptance for the 12B row; the extra drafted token more than pays for its acceptance cost at these speeds.

## Thermal And Power

| Model / lane | Pre-decode (W) | Post-decode (W) | Source |
|---|---:|---:|---|
| Gemma 4 12B plain F16KV | 101 W | 76 W | bench.log |
| Gemma 4 12B MTP qathead Q8KV | 106 W | 76 W | bench.log |
| Gemma 4 26B-A4B plain F16KV | 87 W | 76 W | bench.log |
| Gemma 4 26B-A4B MTP qathead Q8KV | 105 W | 78 W | bench.log |
| Gemma 4 31B plain Q8KV | 80 W | 77 W | bench.log |
| Gemma 4 31B MTP qathead F16KV | 79 W | 75 W | bench.log |

No thermal throttle observed on any run. Pre-decode is peak prefill load; post-decode reflects decode steady-state power.

## Repro Notes

- All runs use `llama.cpp-b9360` Vulkan build (`build-vulkan-b9360/bin/llama-server`)
- MTP rows require the **Atomic llama.cpp TurboQuant fork**, which has the `gemma4_assistant` architecture wired up. Stock llama.cpp b9360 does not load MTP heads for Gemma 4.
- `ik_llama` QAT assistant heads (from `ji-farthing/gemma-4-qat-q4_0-MTP-assistants-ik-llama-GGUF`) use architecture `gemma4_mtp` — this Atomic build rejects them with `unknown model architecture: 'gemma4_mtp'`. These rows use the Atomic-compatible heads converted from Google's unquantized QAT assistant repos.
- **PARALLEL=2 crashed in this submitted Atomic build** on Gemma 4 MTP graph init even with F16 KV and async overlap disabled. MTP rows in this bundle are PARALLEL=1 only. Atomic PR #26 later merged a fix, so post-merge 2-slot results should be measured before reusing the old concurrency conclusion.
- Plain serve scripts: `scripts/serve/gemma26_mtp_vulkan_serve.sh` (26B/12B) and `scripts/serve/gemma31_mtp_vulkan_serve.sh` (31B) with env overrides for plain vs MTP configurations.

## Context Against Previous Non-QAT Gemma Rows

| Model / lane | Quant | Prefill | Decode |
|---|---|---:|---:|
| Gemma 4 26B-A4B non-QAT | UD-Q6_K_XL, plain Vulkan | 1002.8 tok/s | 44.8 tok/s |
| Gemma 4 26B-A4B QAT | Q4_0, plain Vulkan | **1194.4 tok/s** | **59.4 tok/s** |
| Gemma 4 26B-A4B QAT | Q4_0 + MTP qathead | 729.3 tok/s | **71.4 tok/s** |
| Gemma 4 31B non-QAT | Q6, plain Vulkan | 151.3 tok/s | ~8.1 tok/s |
| Gemma 4 31B QAT | Q4_0, plain Vulkan | **204.2 tok/s** | **11.0 tok/s** |
| Gemma 4 31B QAT | Q4_0 + MTP qathead | 203.6 tok/s | **19.1 tok/s** |

QAT Q4_0 consistently beats non-QAT Q6 on speed at this quant level — the smaller model footprint wins on bandwidth even against the higher-precision variant.

## Raw Source Files

| Run | Directory |
|---|---|
| Gemma 4 12B plain F16KV | `evals/bench/results/gemma12-qat-q4_0-vulkan-b9360-f16kv/` |
| Gemma 4 12B MTP block3 Q8KV (non-QAT head) | `evals/bench/results/gemma12-qat-q4_0-mtp-block3-q8kv/` |
| Gemma 4 12B MTP qathead Q8 Q8KV | `evals/bench/results/gemma12-qat-q4_0-mtp-qathead-q8-q8kv/` |
| Gemma 4 12B MTP parallel2 repro (crash) | `evals/bench/results/gemma12-qat-q4_0-mtp-parallel2-repro/` |
| Gemma 4 26B-A4B plain F16KV | `evals/bench/results/gemma26-a4b-qat-q4_0-vulkan-b9360-f16kv/` |
| Gemma 4 26B-A4B MTP block3 Q8KV (non-QAT head) | `evals/bench/results/gemma26-a4b-qat-q4_0-mtp-block3-q8kv/` |
| Gemma 4 26B-A4B MTP qathead Q8 Q8KV | `evals/bench/results/gemma26-a4b-qat-q4_0-mtp-qathead-q8-q8kv/` |
| Gemma 4 31B plain Q8KV | `evals/bench/results/gemma31-qat-q4_0-vulkan-b9360-q8kv/` |
| Gemma 4 31B MTP block3 F16KV (non-QAT head) | `evals/bench/results/gemma31-qat-q4_0-mtp-block3-f16kv/` |
| Gemma 4 31B MTP qathead Q8 F16KV | `evals/bench/results/gemma31-qat-q4_0-mtp-qathead-q8-f16kv/` |
| Block sweep JSONL (short probe) | `evals/bench/results/gemma-qat-mtp-qathead-block-sweep.jsonl` |
