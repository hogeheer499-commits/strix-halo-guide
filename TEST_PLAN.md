# Benchmark Roadmap and Test Plan

This guide should spread because it contains useful, reproducible data that other Strix Halo owners can use immediately. The goal is not to make louder claims. The goal is to keep the guide current, measured, practical, and hard to replace.

## Principles

1. **Data first.** Every performance claim should map back to a command, version, model, quant, backend, and date.
2. **One variable at a time.** Do not mix a software update with a new benchmark category unless the goal is explicitly before/after testing.
3. **Current state is not assumed.** Before each benchmark campaign, record kernel, Mesa, Ollama, llama.cpp commit, model file, AMDVLK state, GPU clock, and `tuned` profile.
4. **Failure cases are content.** "This did not help" and "this broke silently" are often more useful than another speed row.
5. **Practicality beats peak numbers.** The guide should answer what to run, how to set it up, how fast it feels, what fails, and when another platform is a better choice.

## Current Locked Baseline

As of the 2026-05-01 reconciliation:

- GitHub `main` is aligned with the local tracked repo.
- CPU spec is corrected to Ryzen AI MAX+ 395, 16 cores / 32 threads.
- Beelink GTR9 Pro pricing is date-bound at $4,399 official for the 128GB+2TB variant on May 1, 2026.
- AMDVLK is documented as removed and not recommended.
- ROCm is no longer described as globally broken on kernel 6.19.x; it works with the HSA overrides documented in the guide.
- Mesa RADV 26.0.6, Ollama 0.21.2, kernel 6.19.4, safe linux-firmware, 2900 MHz GPU clock, and `tuned accelerator-performance` are the current verified system state.

## Benchmark Workflow

### Phase 0: Documentation Gate

Status: done.

The README, `BENCHMARKS.md`, `SYSTEM_AUDIT.md`, and `RESEARCH.md` must not contain stale claims that contradict the current system state. This gate is complete for the May 2026 baseline.

### Phase 1: Data Foundation

Status: initial CSV and chart layer complete.

Create structured data files under `data/` before adding more benchmark rows. The README can stay human-readable, but charts, comparisons, and future posts should come from structured data.

Required files:

- `data/README.md`: schema and workflow.
- `data/benchmarks.csv`: existing measured benchmark rows.
- `data/long_context.csv`: long-context reference rows.
- `data/smoke_tests.csv`: short validation runs before bigger benchmark campaigns.
- `charts/*.svg`: generated summaries from the CSV corpus.
- `scripts/generate_charts.py`: dependency-free chart generator.

### Phase 2: Smoke Test

Status: first run completed, clean rerun required.

A smoke test is a short sanity check that proves the current stack is still healthy before a larger benchmark run. It is not a new benchmark campaign.

Minimum checks:

- `tuned-adm active` shows `accelerator-performance`.
- `vulkaninfo --summary` shows `RADV STRIX_HALO` and Mesa RADV.
- AMDVLK is absent.
- GPU clock has the asterisk on 2900 MHz.
- One direct Vulkan `llama-bench` result is within expected range.
- One Ollama result is within expected range.

Why this matters: if `tuned` is inactive, AMDVLK hijacks Vulkan, a model file changes, or a nightly build regresses, a full benchmark campaign can produce polluted data. Smoke tests catch that cheaply.

The 2026-05-02 smoke test confirmed the stack is functional, but also found heavy background load. Those numbers are recorded in `SMOKE_TESTS.md` and `data/smoke_tests.csv` as non-publishable smoke-test data.

### Phase 3: Update Gate

Do this before unique benchmark campaigns, but do not blindly update everything.

Recommended order:

1. Record the current baseline.
2. Check upstream versions and known issues.
3. Decide whether the update is worth testing.
4. If updating, change one major component at a time.
5. Run the smoke test before and after the update.
6. Only then run the larger benchmark campaign.

This means: **check for updates before new unique benchmarks, but benchmark against a known baseline first.** Updating first without a baseline makes regressions hard to explain.

High-impact update checks:

- llama.cpp commit and recent Vulkan/ROCm changes.
- Ollama version and bundled llama.cpp changes.
- Mesa/RADV version.
- Kernel and linux-firmware changes.
- ROCm container tags from kyuz0.
- Model releases and GGUF/quant updates.

## Benchmark Campaign Priority

### P0: Existing Data Structure

Purpose: make current results reusable for charts, dashboards, README tables, and external comparisons.

Deliverables:

- CSV rows for current headline benchmarks.
- CSV rows for Ollama, direct llama.cpp, ROCm, and historical backend comparisons.
- Clear status labels: `measured-local`, `historical-local`, `external-reference`, `smoke-test`.

### P1: Current Stack Smoke Test

Purpose: prove the May 2026 system still matches the guide's assumptions before adding new rows.

Initial targets:

- Direct Vulkan RADV `llama-bench` on a local GGUF model.
- Ollama Qwen3.6 35B easy-path generation.
- Preflight log of driver, firmware, clock, and `tuned`.

### P2: Multi-User Serving

Purpose: answer the practical question: "Can this box serve more than one user or tool at once?"

Status: initial `llama-server` baseline completed on 2026-05-03. Qwen3.6 35B-A3B UD-Q4_K_M reached 162 t/s aggregate at `-np 8` and plateaued at 166 t/s at `-np 16`. Qwen3-Coder 30B-A3B reached 173 t/s aggregate at `-np 8`; `-np 16` regressed. Power draw and vLLM are still open.

This track is now expanded into the [Server Shootout](SERVER_SHOOTOUT.md): a practical local-AI-PC comparison of Ollama, `llama-server`, ROCm/Lemonade builds, and vLLM containers.

Targets:

- `llama-server` with `--parallel` / slot tests where applicable.
- vLLM where practical.
- Lemonade `llamacpp-rocm` and `vllm-rocm` gfx1151 builds where practical.
- Concurrency levels: 1, 2, 4, 8, 16.
- Metrics: total throughput, per-user throughput, TTFT, ITL, p50/p95 latency, API compatibility, tool-call behavior, setup friction, memory use, power if available.

This is likely the highest-value missing benchmark category because most public Strix Halo data is single-user tg/pp.

### P3: Long Context

Purpose: show where backend choice changes at 32K, 64K, and 128K context.

Status: initial local RADV prompt-processing baseline completed on 2026-05-03 for Qwen3.6 35B and Qwen3-Next 80B through 64K. Filled-KV decode at 32K/64K/128K is also complete for f16, with Qwen3.6 q8_0/q4_0 KV-cache comparisons at 32K/64K. A 64K real-corpus prompt using the guide documentation is complete. ROCm HIP spot-checking exists, but no tuned local rocWMMA build is available yet. Broader real-corpus prompts remain open.

ROCm/rocWMMA gate: do not publish upstream rocWMMA numbers unless the build is explicitly the tuned branch or container being tested. Upstream `GGML_HIP_ROCWMMA_FATTN=ON` has known regression risk, and the current local HIP build caches all have `GGML_HIP_ROCWMMA_FATTN=OFF`. The next ROCm long-context campaign needs its own build log, ROCm version, llama.cpp commit/branch, compiler flags, `rocblaslt` warning state, and raw output directory.

Targets:

- RADV Vulkan direct.
- ROCm HIP.
- rocWMMA/tuned paths where practical.
- KV cache settings, including TurboQuant if stable.
- Models: Qwen3.6 35B, Qwen3-Next 80B, gpt-oss-120b if available.

Metrics:

- pp, tg, TTFT, memory use, and failure mode.

### P4: Easy Path vs Fast Path

Purpose: quantify the tradeoff users actually care about.

Targets:

- Ollama.
- latest direct `llama-server`.
- Open WebUI against Ollama and `llama-server`.

Metrics:

- Throughput, latency, setup friction, model management, stability.

### P5: Power Efficiency

Purpose: add ownership-cost and always-on self-hosting data.

Status: blocked from public tokens-per-watt claims until power telemetry is validated. `powercap` is empty, but `amdgpu` exposes `power1_average` / `power1_input` with label `PPT`; treat this as candidate GPU/APU telemetry, not wall power. See `POWER_BASELINE.md`.

Metrics:

- Idle watts.
- Load watts.
- tokens per watt.
- cost per million local tokens under realistic power prices.

Acceptable measurement sources:

- wall meter or smart plug with timestamped export;
- validated AMD telemetry that reports package/APU power during the exact run;
- repeatable idle/load protocol with at least 3 runs and the same benchmark command.

Record power in a separate dataset, not in the existing throughput CSVs, until the source is validated.

### P6: vLLM and ROCm Serving

Purpose: test whether Strix Halo can be a real local API appliance, not just a chat box.

Status: clean vLLM container preflight completed on 2026-05-03. The `vllm-gfx1151` Distrobox uses `docker.io/kyuz0/vllm-therock-gfx1151:stable`, exposes gfx1151 through `rocm-smi`, and passed a small `Qwen/Qwen3-0.6B` OpenAI-compatible smoke test. This is not yet a throughput benchmark.

Targets:

- kyuz0 vLLM toolbox.
- OpenAI-compatible serving.
- Batch/concurrency comparison against llama.cpp server.

Clean setup rule: vLLM must run in a dedicated Distrobox/Toolbx/Podman container. Do not install vLLM, PyTorch, ROCm, or TheRock packages into the host Python environment.

Recommended first pass:

1. Create `vllm-gfx1151` from `docker.io/kyuz0/vllm-therock-gfx1151:stable`.
2. Verify GPU access with `rocm-smi` inside the container.
3. Start one known-supported model with `start-vllm`.
4. Run the same concurrency levels as `llama-server`: 1, 2, 4, 8, 16.
5. Store image tag, model, quant, context, TTFT, p50/p95 latency, aggregate throughput, memory use, and warmup/compile notes.

Only test `:latest` after `:stable` has a clean baseline, because latest images may include upstream regressions.

### P7: Cross-Platform Comparisons

Purpose: only compare when model, quant, prompt length, context, and backend are close enough to be defensible.

Targets:

- Mac Studio / MLX on the exact same model family and quant where possible.
- DGX Spark public numbers with exact workload notes.
- RTX 4090 / 3090 for capacity-bound versus speed-bound workload segmentation.

## What Makes the Guide Unique

The strongest differentiator is a combination of:

- Current Strix Halo setup knowledge.
- Reproducible commands and raw data.
- Driver and backend failure cases.
- Practical model recommendations.
- Multi-user, long-context, and easy-path-vs-fast-path measurements that are still thinly documented elsewhere.

The guide should not be positioned as "buy this box." It should be positioned as: "Here is what Strix Halo can actually do, how to reproduce it, where it wins, where it loses, and how to avoid wasting days on bad assumptions."

## Benchmark Cleanliness

Before any publishable benchmark run, run the read-only cleanliness check:

```bash
scripts/check_benchmark_cleanliness.sh
```

The goal is "clean enough", not "everything disabled forever." Daily-use services can run outside benchmark windows, but publishable numbers should not be collected while remote desktop sessions, video conferencing, VMs, unrelated containers, or inactive `tuned` profiles are adding measurement noise.

T3 is not optional noise for this workstation. The Strix Halo workflow is operated from T3, so the `3773` backend and `3777` semantic proxy must remain reachable before and during tests. If T3 is broken, pause Strix testing and restore T3 first.

For long or memory-risky runs:

```bash
scripts/run_with_t3_guard.py --cleanup-cmd "podman stop vllm-gfx1151" -- <benchmark command>
```

The guard is allowed to stop only the benchmark command and explicit benchmark cleanup targets. It must not stop T3, `3773`, or `3777`.
