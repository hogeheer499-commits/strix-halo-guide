# Qwen 122B-A10B MTP Numbers

This file captures the measured numbers for the Qwen 3.5 122B-A10B MTP (MXFP4_MOE) run so they can live alongside the Strix Halo benchmark export as a separate reference sheet.

## Model And Run Context

| Field | Value |
|---|---|
| Model | Qwen 3.5 122B-A10B MTP `MXFP4_MOE` |
| Architecture | `qwen2` |
| Backend | b9360 Vulkan server |
| Serve port | `:8098` |
| GTT ceiling | 112 GiB |
| Gate context | 12,288 |
| Coding-eval context | 12,288 |
| Source log | `projects/qwen122b-mtp/devlog.md` (`/home/keith/Desktop/github/tesla/projects/qwen122b-mtp/devlog.md`) |

## Measured Numbers

| Metric | Value | Source |
|---|---|---|
| Load to listening | ~24 s | `devlog` (`/home/keith/Desktop/github/tesla/projects/qwen122b-mtp/devlog.md`) |
| Prefill throughput | 332.1 tok/s | `devlog` (`/home/keith/Desktop/github/tesla/projects/qwen122b-mtp/devlog.md`) |
| Decode throughput | 26.7 tok/s | `devlog` (`/home/keith/Desktop/github/tesla/projects/qwen122b-mtp/devlog.md`) |
| Two-slot sustained decode | 13.6 tok/s per slot, ~25.6 tok/s aggregate | `devlog` (`/home/keith/Desktop/github/tesla/projects/qwen122b-mtp/devlog.md`) |
| Nonce gate | 3/3 | `devlog` (`/home/keith/Desktop/github/tesla/projects/qwen122b-mtp/devlog.md`) |
| Coding eval E2E | PASS (5/5 E2E) | `devlog` (`/home/keith/Desktop/github/tesla/projects/qwen122b-mtp/devlog.md`) |
| Substantive step-files correct | 20/20 | `devlog` (`/home/keith/Desktop/github/tesla/projects/qwen122b-mtp/devlog.md`) |
| Quality set generation | 6/6 finished `stop` | `devlog` (`/home/keith/Desktop/github/tesla/projects/qwen122b-mtp/devlog.md`) |
| Pairwise vs non-MTP baseline | 3-3 Tie | `pairwise scorecard` (`/home/keith/Desktop/github/tesla/evals/quality/comparison/pairwise-mtp/pairwise-qwen122b-mtp-vs-baseline.md`) |
| MTP draft acceptance | ~63-65% of drafted tokens (`draft_n_accepted / draft_n`) | `raw timing JSON` (`/home/keith/Desktop/github/tesla/evals/bench/results/qwen122b-mtp-vulkan/tg_probe.json`) |

## Thermal And Power

| Metric | Value | Source |
|---|---|---|
| Edge temperature | 48 °C idle / 52 °C load | `devlog` (`/home/keith/Desktop/github/tesla/projects/qwen122b-mtp/devlog.md`) |
| Socket power (PPT) | ~98 W prefill peak, ~72-73 W decode | `devlog` (`/home/keith/Desktop/github/tesla/projects/qwen122b-mtp/devlog.md`) |
| Thermal verdict | No thermal throttle; power-limited instead | `devlog` (`/home/keith/Desktop/github/tesla/projects/qwen122b-mtp/devlog.md`) |

## Per-Prompt Decode Samples

The quality battery decode rates recorded in the prompt outputs:

| Prompt | Decode |
|---|---|
| Run 1 | 29.6 tok/s |
| Run 2 | 28.3 tok/s |
| Run 3 | 31.7 tok/s |

## MTP Acceptance Interpretation

The preserved raw timing JSON does **not** support the older `~80.4%`
acceptance note. The preserved samples show:

| Source | Drafted | Accepted | Accepted / drafted | Accepted / predicted |
|---|---:|---:|---:|---:|
| `tg_probe.json` | 1756 | 1121 | 63.8% | 56.1% |
| `mtp_probe.json` | 436 | 280 | 64.2% | 56.0% |
| `concurrency/slot1.json` | 441 | 278 | 63.0% | 55.6% |
| `concurrency/slot2.json` | 433 | 281 | 64.9% | 56.2% |

Operational read: acceptance is lower than the previous note, but the lane is
still a net speed win because single-stream decode measured **26.7 tok/s** versus
the non-MTP 122B baseline of roughly **19.4 tok/s**. Rejected draft tokens do not
change model quality; they reduce speculative-decoding efficiency because the
target model verifies and discards them.

Tuning implication: `DRAFT_N`, `PMIN`, and prompt class could change the
acceptance/speed tradeoff. The current setting (`DRAFT_N=2`, no `PMIN`) is good
enough to keep, but it is not obviously optimal.

## Repro Notes

- The serve path and gate path are documented in `projects/qwen122b-mtp/plan-v1.md` (`/home/keith/Desktop/github/tesla/projects/qwen122b-mtp/plan-v1.md`).
- The Qwen 122B MTP quality battery was run with `SOUL.md`, seed=42, temp=0, and `MAX_TOKENS=8000`.

## Raw Source Files

- `projects/qwen122b-mtp/devlog.md` (`/home/keith/Desktop/github/tesla/projects/qwen122b-mtp/devlog.md`)
- `evals/bench/results/qwen122b-mtp-vulkan/tg_probe.json` (`/home/keith/Desktop/github/tesla/evals/bench/results/qwen122b-mtp-vulkan/tg_probe.json`)
- `evals/bench/results/qwen122b-mtp-vulkan/mtp_probe.json` (`/home/keith/Desktop/github/tesla/evals/bench/results/qwen122b-mtp-vulkan/mtp_probe.json`)
- `evals/quality/comparison/pairwise-mtp/pairwise-qwen122b-mtp-vs-baseline.md` (`/home/keith/Desktop/github/tesla/evals/quality/comparison/pairwise-mtp/pairwise-qwen122b-mtp-vs-baseline.md`)
