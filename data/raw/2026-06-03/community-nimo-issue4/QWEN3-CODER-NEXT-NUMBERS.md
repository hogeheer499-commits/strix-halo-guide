# Qwen3-Coder-Next Numbers

This file captures the measured numbers for the Qwen3-Coder-Next UD-Q4_K_XL run on Vulkan vs ROCm backends, verifying the performance improvements of the Vulkan b9360 server.

## Model And Run Context

| Field | Value |
|---|---|
| Model | Qwen3-Coder-Next `UD-Q4_K_XL` (49.6 GB) |
| Architecture | `qwen2` |
| GTT ceiling | 112 GiB |
| Gate context | 32,768 |
| Coding-eval context | 32,768 |
| Vulkan Backend | b9360 Vulkan server (b9360 build, `/home/keith/ai-tools/llama.cpp-b9360/build-vulkan-b9360/bin/llama-server`) |
| ROCm Backend | Lemonade llama.cpp ROCm server (stable release, `/home/keith/.cache/lemonade/bin/llamacpp/rocm-stable/llama-server`) |
| Serve port | `:8097` |
| Source log | `projects/qwen3-coder-next-speed/devlog.md` (`/home/keith/Desktop/github/tesla/projects/qwen3-coder-next-speed/devlog.md`) |

## Measured Numbers (Vulkan vs ROCm)

| Metric | Vulkan Backend | ROCm Backend (Baseline) | Speedup / Improvement |
|---|---|---|---|
| Load to listening | ~20 s | ~24 s | -16.7% time |
| **Prefill throughput** | **723.2 tok/s** | **663.4 tok/s** | **+9.0%** |
| **Decode throughput (single-stream)** | **44.4 tok/s** | **38.5 tok/s** | **+15.3%** |
| **Wall time std (1150-in/2000-out)** | **46.6 s** | **53.7 s** | **13.2% faster** |
| **Concurrency aggregate @ 2 slots** | **66.7 tok/s** | **55.6 tok/s** | **+19.9%** |
| Per-slot sustained decode | slot1: 34.5 tok/s, slot2: 34.8 tok/s | slot1: 29.4 tok/s, slot2: 29.2 tok/s | +17.3% to +19.2% |
| Nonce gate | 3/3 PASS recorded | 3/3 PASS recorded | Recorded parity; no saved nonce transcript was found in the repo |
| Coding eval | One orchestrated 4-step run: all grader checks PASS | Not regraded in this run | Vulkan gate verified from saved artifacts |

## Thermal And Power

| Metric | Vulkan Backend | ROCm Backend (Baseline) | Improvement |
|---|---|---|---|
| Socket power (PPT) | ~85 W prefill peak, ~70 W decode | ~96 W prefill peak, ~82 W decode | ~14.6% power reduction |
| Thermal verdict | No thermal throttle (power-limited) | No thermal throttle | Lower temperatures under Vulkan |

## Repro Notes

- The serve path and gate path are documented in `projects/qwen3-coder-next-speed/plan-v1.md` (`/home/keith/Desktop/github/tesla/projects/qwen3-coder-next-speed/plan-v1.md`).
- The benchmarks were captured using `scripts/eval/full_bench.sh` against `:8097` servers.
- The saved Vulkan coding artifact grades cleanly with `python3 scripts/eval/coding_eval_grade.py qwen3-coder-next-vulkan`.
- Do not describe the coding result as five independent E2E runs. It was one orchestrated 4-step task where all grader checks passed.
- The nonce result is recorded in the project docs, but no preserved nonce transcript/log was found during the handoff audit.

## Raw Source Files

- `projects/qwen3-coder-next-speed/devlog.md` (`/home/keith/Desktop/github/tesla/projects/qwen3-coder-next-speed/devlog.md`)
- `evals/bench/results/qwen3-coder-next-vulkan/bench.json` (`/home/keith/Desktop/github/tesla/evals/bench/results/qwen3-coder-next-vulkan/bench.json`)
- `evals/bench/results/qwen3-coder-next-rocm/bench.json` (`/home/keith/Desktop/github/tesla/evals/bench/results/qwen3-coder-next-rocm/bench.json`)
