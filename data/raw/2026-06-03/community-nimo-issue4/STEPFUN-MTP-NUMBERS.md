# StepFun MTP Numbers

This file captures the measured numbers for the StepFun Step-3.7-Flash run with the Q8_0 MTP draft model so they can live alongside the Strix Halo benchmark export as a separate reference sheet.

## Model And Run Context

| Field | Value |
|---|---|
| Model | StepFun Step-3.7-Flash `UD-IQ4_XS` + `Step-3.7-Flash-MTP-Q8_0.gguf` |
| Architecture | `step35` |
| Backend | b9360 Vulkan server (Step-3.7-Flash MTP patched) |
| Serve port | `:8101` |
| GTT ceiling | 112 GiB |
| Gate context | 12,288 |
| Coding-eval context | 12,288 |
| Source log | `projects/stepfun-3.7-flash-mtp/devlog.md` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash-mtp/devlog.md`) |

## Measured Numbers

| Metric | MTP Value | Baseline (Non-MTP) | Speedup / Improvement | Source |
|---|---|---|---|---|
| Load to listening | ~31 s | ~31 s | 0% startup penalty | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash-mtp/devlog.md`) |
| Prefill throughput | **211.2 tok/s** | 212.0 tok/s | Parity | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash-mtp/devlog.md`) |
| Decode throughput | **26.0 tok/s** | 20.4 tok/s | **+27.5%** | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash-mtp/devlog.md`) |
| Wall time std (1150-in/2000-out) | **82.4 s** | 103.4 s | **20.8% faster** | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash-mtp/devlog.md`) |
| Two-slot sustained decode | **19.7 / 19.6 tok/s**, ~35.7 tok/s aggregate | 17.14 tok/s, ~34 tok/s aggregate | **+15.0% per-slot, +5.0% agg** | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash-mtp/devlog.md`) |
| Nonce gate | **3/3 PASS** | 3/3 PASS | Parity | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash-mtp/devlog.md`) |
| Coding eval E2E | **PASS (5/5 E2E)** | 4/5 (80%) | **+20.0% Correctness Win** | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash-mtp/devlog.md`) |
| Substantive step-files correct | **20/20** | 20/20 | Parity | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash-mtp/devlog.md`) |
| MTP draft acceptance | **84.7%** (standard decode run) | N/A | High-acceptance verification | `raw timing JSON` (`/home/keith/Desktop/github/tesla/evals/bench/results/stepfun-mtp-vulkan/tg_probe.json`) |

## Thermal And Power

| Metric | MTP Value | Baseline (Non-MTP) | Source |
|---|---|---|---|
| Socket power (PPT) | ~101 W prefill peak, ~73 W decode | ~93 W prefill peak, ~85 W decode | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash-mtp/devlog.md`) |
| Power Efficiency | ~14% less average power on decode | Baseline | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash-mtp/devlog.md`) |
| Thermal verdict | No thermal throttle; power-limited instead | No thermal throttle; power-limited instead | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash-mtp/devlog.md`) |

## Per-Step Coding-Eval Decode Samples

Timings recorded during the E2E orchestrated coding execution:

| Step | Generation Speed (Decode) | Draft Acceptance Rate |
|---|---|---|
| Step 1 | **29.8 – 31.9 tok/s** | **93.9%** (140/149) |
| Step 2 | **27.2 – 28.8 tok/s** | **88.1%** (664/753) |
| Step 3 | **31.4 tok/s** | **97.0%** (33/34) |
| Step 4 | **28.9 – 29.5 tok/s** | **93.3%** (70/75) |

## Repro Notes

- The serve configuration requires rebuilding `llama.cpp` using the Step-3.7 MTP patch: `llama.cpp-step37-mtp.patch` found in `notSnix/Step-3.7-Flash-Q4_K_M-MTP-GGUF`.
- The main model and draft model are served using `scripts/serve/stepfun_mtp_vulkan_serve.sh` on `:8101`.
- **Note on MTP draft acceptance**: The summary `bench.json` outputs `"mtp.acceptance_pct": null` because of log-parsing format variations for this run. The **84.7%** acceptance figure was calculated directly from the raw token count values (`draft_n_accepted` / `draft_n`) recorded in the raw `tg_probe.json` timing logs.

## Raw Source Files

- `projects/stepfun-3.7-flash-mtp/devlog.md` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash-mtp/devlog.md`)
- `evals/bench/results/stepfun-mtp-vulkan/bench.json` (`/home/keith/Desktop/github/tesla/evals/bench/results/stepfun-mtp-vulkan/bench.json`)
- `evals/bench/results/stepfun-mtp-vulkan/tg_probe.json` (`/home/keith/Desktop/github/tesla/evals/bench/results/stepfun-mtp-vulkan/tg_probe.json`)
