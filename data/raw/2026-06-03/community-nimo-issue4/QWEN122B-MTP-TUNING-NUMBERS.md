# Qwen 122B-A10B MTP Tuning Numbers

This file documents the results of the parameter sweep grid over speculative decoding configurations (`DRAFT_N` and `PMIN`) for the Qwen 3.5 122B-A10B MTP (`MXFP4_MOE`) model on Vulkan, executed on 2026-06-03.

## Model And Run Context

| Field | Value |
|---|---|
| Model | Qwen 3.5 122B-A10B MTP `MXFP4_MOE` |
| Architecture | `qwen2` |
| Backend | b9360 Vulkan server (Step-3.7-Flash MTP patched) |
| Serve port | `:8098` |
| GTT ceiling | 112 GiB |
| Gate context | 12,288 |
| Coding-eval context | 12,288 |
| Project Home | `projects/qwen122b-mtp-tuning/brief-v1.md` (`/home/keith/Desktop/github/tesla/projects/qwen122b-mtp-tuning/brief-v1.md`) |
| Source log | `projects/qwen122b-mtp-tuning/devlog.md` (`/home/keith/Desktop/github/tesla/projects/qwen122b-mtp-tuning/devlog.md`) |

## Sweep Grid Results (15 Cells)

The parameters `DRAFT_N` (draft budget) and `PMIN` (draft token probability threshold) were swept. All other settings were held fixed.
Acceptance percentages in this table are the dedicated MTP-probe acceptance values written to `bench.json` from `mtp_probe.json` (`draft_n_accepted / draft_n`).

| Run Label | DRAFT_N | PMIN | Decode Throughput | Draft Acceptance | Wall Time (Std) | Concurrency (Agg) | Finish Reason |
|---|---|---|---|---|---|---|---|
| `n1-pmin-none` | **1** | **unset** | **28.3 tok/s** | **81.8%** | **74.2 s** | **26.3 tok/s** | `length` |
| `n1-pmin-0.50` | 1 | 0.50 | 26.1 tok/s | 89.9% | 80.2 s | 25.6 tok/s | `length` |
| `n1-pmin-0.60` | 1 | 0.60 | 24.6 tok/s | 92.9% | 84.8 s | 25.0 tok/s | `length` |
| `n1-pmin-0.70` | 1 | 0.70 | 24.4 tok/s | 95.7% | 85.5 s | 24.4 tok/s | `length` |
| `n1-pmin-0.80` | 1 | 0.80 | 23.6 tok/s | 98.3% | 88.3 s | 23.8 tok/s | `length` |
| `n2-pmin-none` | 2 | unset | 27.8 tok/s | 68.6% | 75.4 s | 27.0 tok/s | `length` |
| `n2-pmin-0.50` | 2 | 0.50 | 26.0 tok/s | 86.1% | 80.5 s | 26.3 tok/s | `length` |
| `n2-pmin-0.60` | 2 | 0.60 | 25.1 tok/s | 91.6% | 83.2 s | 25.6 tok/s | `length` |
| `n2-pmin-0.70` | 2 | 0.70 | 24.4 tok/s | 94.2% | 85.5 s | 25.6 tok/s | `length` |
| `n2-pmin-0.80` | 2 | 0.80 | 23.2 tok/s | 95.4% | 89.7 s | 24.4 tok/s | `length` |
| `n3-pmin-none` | 3 | unset | 26.5 tok/s | 55.0% | 79.0 s | 25.6 tok/s | `length` |
| `n3-pmin-0.50` | 3 | 0.50 | 25.5 tok/s | 81.9% | 82.0 s | 26.3 tok/s | `length` |
| `n3-pmin-0.60` | 3 | 0.60 | 25.0 tok/s | 88.8% | 83.5 s | 26.3 tok/s | `length` |
| `n3-pmin-0.70` | 3 | 0.70 | 23.8 tok/s | 94.6% | 87.6 s | 24.4 tok/s | `length` |
| `n3-pmin-0.80` | 3 | 0.80 | 22.4 tok/s | 95.0% | 92.9 s | 23.8 tok/s | `length` |

## Key Findings

1. **PMIN Pruning Trade-off:** While increasing `PMIN` leads to extremely high token validation efficiency (reaching **98.3%** at `PMIN=0.80`), it causes a monotonic decrease in single-stream generation speed (tok/s) across all draft budgets. Pruning draft tokens forces the system to execute slow autoregressive validation fallbacks too frequently, offsetting the benefit. Greedy speculative validation (keeping `PMIN` unset) yields the best single-stream throughput.
2. **Optimal Single-Stream Configuration:** **`DRAFT_N=1` with `PMIN=unset`** is the clear winner for single-stream decode and normalized wall time, achieving **28.3 tok/s** decode speed (+6.0% improvement over the previous `DRAFT_N=2` baseline, and +45.9% faster than the non-speculative 19.4 tok/s baseline). It also records a very healthy **81.8%** MTP-probe draft acceptance rate.
3. **Concurrency Trade-off:** **`DRAFT_N=2` with `PMIN=unset`** remains slightly better on two-slot aggregate throughput (**27.0 tok/s** vs **26.3 tok/s**) and the dedicated MTP probe's effective throughput field (**28.7 tok/s** vs **28.5 tok/s**). The default was still moved to `DRAFT_N=1` because the primary serving target is single-stream/wall-time responsiveness.

## Gating Verification (Best Cell: DRAFT_N=1, PMIN unset)

- **Nonce Gate:** **3/3 PASS** using the `qwen122plan` profile.
- **Orchestrated Coding Gate:** **PASS (E2E 5/5)** (All steps 1-4 and summary fidelity graded cleanly).
- **Blinded Pairwise Quality Comparison:** **3-3 Tie** vs. the previous `DRAFT_N=2` run, supporting quality parity in this six-prompt sample.

## Repro Notes

- The serve script `scripts/qwen122b_mtp_vulkan_serve.sh` has been updated to use `DRAFT_N=1` as the default.
- Results are saved under `evals/bench/results/qwen122b-mtp-n1-pmin-none/`.
- For the winning cell, `bench.json` reports `mtp.acceptance_pct = 81.8` from the dedicated `mtp_probe.json` sample (**224 accepted / 274 drafted**). The standard decode run's `tg_probe.json` reports **893 accepted / 1105 drafted = 80.8%**.
