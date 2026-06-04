# StepFun Numbers

This file captures the measured numbers for the StepFun Step-3.7-Flash run
so they can live alongside the Strix Halo benchmark export as a separate
reference sheet.

## Model And Run Context

| Field | Value |
|---|---|
| Model | StepFun Step-3.7-Flash `UD-IQ4_XS` |
| Architecture | `step35` |
| Backend | b9360 Vulkan server |
| Serve port | `:8101` |
| GTT ceiling | 112 GiB |
| Gate context | 16,384 |
| Coding-eval context | 32,768 |
| Source log | `projects/stepfun-3.7-flash/devlog.md` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/devlog.md`) |

## Measured Numbers

| Metric | Value | Source |
|---|---|---|
| Load to listening | ~31 s | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/devlog.md`) |
| Prefill throughput | 43.13 tok/s | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/devlog.md`) |
| Decode throughput | 22.28 tok/s | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/devlog.md`) |
| Two-slot sustained decode | 17.14 tok/s per slot, ~34 tok/s aggregate | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/devlog.md`) |
| Nonce gate | 3/3 | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/devlog.md`) |
| Coding eval E2E | 4/5 | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/devlog.md`) |
| Substantive step-files correct | 20/20 | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/devlog.md`) |
| Quality set generation | 6/6 finished `stop` | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/devlog.md`) |
| Pairwise vs gpt-oss-120b-soulfix | 6/0 | `pairwise scorecard` (`/home/keith/Desktop/github/tesla/evals/quality/comparison/round-robin/m1-stepfun-vs-gptoss120-soulfix.md`) |
| Pairwise vs 122b | 4/0/2 | `pairwise scorecard` (`/home/keith/Desktop/github/tesla/evals/quality/comparison/round-robin/m2-stepfun-vs-122b.md`) |
| Calibration anchor | 122b 3-2 over gpt-oss-soulfix | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/devlog.md`) |

## Thermal And Power

| Metric | Value | Source |
|---|---|---|
| Edge temperature | 45 °C rising to a 58 °C plateau | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/devlog.md`) |
| Socket power (PPT) | brief 92-93 W, then flat 84-85 W | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/devlog.md`) |
| Thermal verdict | No thermal throttle; power-limited instead | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/devlog.md`) |
| GPU busy | 96-97% sustained | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/devlog.md`) |
| Per-slot decode under load | 17.14 tok/s each, ~34 tok/s aggregate | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/devlog.md`) |
| Core clock sample | not captured (`rocm-smi` parse miss) | `devlog` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/devlog.md`) |

## Per-Prompt Decode Samples

The quality battery decode rates recorded in the stepfun prompt outputs were:

| Prompt | Decode |
|---|---|
| 01 | 19.6 tok/s |
| 02 | 21.0 tok/s |
| 03 | 20.4 tok/s |
| 04 | 20.4 tok/s |
| 05 | 20.3 tok/s |

## Repro Notes

- The serve path and gate path are documented in
  `projects/stepfun-3.7-flash/plan.md` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/plan.md`).
- The thermal session showed the box was power-limited rather than
  thermally throttled.
- The stepfun quality battery was run with `SOUL.md`, seed=42, temp=0, and
  `MAX_TOKENS=8000`.

## Raw Source Files

- `projects/stepfun-3.7-flash/devlog.md` (`/home/keith/Desktop/github/tesla/projects/stepfun-3.7-flash/devlog.md`)
- `evals/quality/comparison/round-robin/m1-stepfun-vs-gptoss120-soulfix.md` (`/home/keith/Desktop/github/tesla/evals/quality/comparison/round-robin/m1-stepfun-vs-gptoss120-soulfix.md`)
- `evals/quality/comparison/round-robin/m2-stepfun-vs-122b.md` (`/home/keith/Desktop/github/tesla/evals/quality/comparison/round-robin/m2-stepfun-vs-122b.md`)
