# Maintainer Notes

These notes are for the local Hoge Heer workstation workflow. They are intentionally separate from the public README because they are not required to reproduce Strix Halo performance on another machine.

## Current Handoff

Current as of 2026-05-07. For the latest pushed commit, run `git log -1 --oneline`.

For a new Strix Halo chat, start by reading:

1. `README.md`
2. `BENCHMARKS.md`
3. `MAX_PERFORMANCE_PLAN.md`
4. `BACKEND_CROSSOVER.md`
5. `ROCM_VLLM_BUGWATCH.md`
6. `SERVER_SHOOTOUT.md`
7. `REPRODUCIBILITY.md`
8. this file

The guide is share-ready. The latest completed work:

- 2026-05-07 max-performance campaign added:
  - Qwen3.6 Q4_0 reached 81.30 t/s as a speed-first row
  - Qwen3-Coder b9049 guide-flags confirmation reached 96.76 t/s, no stable 100 t/s result
  - gpt-oss-120b clean rerun reached 55.57 t/s and prompt processing through 65K tokens
  - same-source b9049 HIP/Vulkan matrix confirmed HIP wins prompt processing and Vulkan wins generation
  - vLLM AWQ without DFlash worked as a smoke test but only reached about 25 t/s
  - lhl rocWMMA branch built but failed to load current Qwen3.6 GGUFs
- latest-stack rerun with llama.cpp b9049 and Ollama 0.23.1
- first local gpt-oss-120b MXFP4 check: 50.59 t/s tg128, 725.03 t/s pp512, 707.29 t/s pp2048; superseded by the 55.57 t/s paused-system rerun above
- HIP/Vulkan crossover evidence: Vulkan wins measured generation; HIP can win prompt processing
- hec-ovi vLLM AWQ/DFlash tracked as an important candidate, not a local claim
- ROCm/vLLM bugwatch added
- README, SHARE, social preview, CSVs, raw logs, and charts updated
- `MAX_PERFORMANCE_PLAN.md` added as the focused "can we push the Beelink further?" roadmap
- `MAX_PERFORMANCE_RESULTS_2026-05-07.md` and `data/max_performance_campaign.csv` hold the latest campaign summary

Current local-only handoff details live in `CONTEXT.md`. That file is intentionally ignored by git and should be used for local continuity, not public claims.

Known local untracked scratch directory:

```text
data/raw/2026-05-05/server-shootout/kyuz0-vllm-awq-qwen36-t3-baseline/
```

Keep it untracked until the vLLM AWQ run is either completed and documented or deliberately discarded.

## Keep Public Docs Separate

The README should answer, within one screen:

- what was tested
- which hardware was used
- best current backend per use case
- where raw data and charts live
- where reproducibility and security context live

Keep local workflow details here unless they directly affect public reproducibility.

## T3 Is Required Locally

Strix Halo work on this machine is operated from T3. Routine benchmark work must keep the T3 backend on `3773` and the semantic proxy on `3777` alive.

If the browser shows:

```text
Upstream request failed: connect ECONNREFUSED 127.0.0.1:3773
```

the proxy is reachable but the real T3 backend is down. Stop Strix testing and restore T3 before doing anything else.

Read-only readiness check:

```bash
scripts/check_benchmark_cleanliness.sh
```

For long or memory-risky benchmark commands, use the T3 guard:

```bash
scripts/run_with_t3_guard.py \
  --cleanup-cmd "podman stop vllm-gfx1151" \
  -- <benchmark command>
```

For heavy vLLM experiments, set stricter headroom explicitly:

```bash
scripts/run_with_t3_guard.py \
  --min-mem-available-gib 24 \
  --min-swap-free-gib 4 \
  --cleanup-cmd "podman stop vllm-gfx1151" \
  -- <benchmark command>
```

Cleanup commands are for benchmark targets only. The guard refuses cleanup commands that reference T3, `3773`, `3777`, broad Node kills, Hermes, or destructive Docker-wide actions.

## Hermes Is Out Of Scope

Do not stop, restart, remove, or otherwise manage `hermes-*` Docker containers from Strix Halo guide work. Docker may be inspected read-only for noise/status, but Hermes recovery belongs in its own chat/workspace.

## Remote Desktop And Other Noise

RustDesk, Zoom, unrelated VMs, Open WebUI, ComfyUI, and unrelated local AI servers can affect publishable numbers. Prefer pausing them for benchmark campaigns, but do not manage them from this project unless explicitly requested for that run. Record the state in raw notes.

Default restore rule for future Strix Halo benchmark chats: when the user asks to pause benchmark noise, automatically restore everything that was paused before ending the task. The user should not need to repeat this. T3 must stay on the whole time, Hermes stays out of scope, and restore should cover the paused local services such as DocFlock, RustDesk, Ollama, Zoom, and suspended benchmark-noise VMs.

## Scratch Data

The directory below contains incomplete vLLM startup artifacts and is not a publishable result:

```text
data/raw/2026-05-05/server-shootout/kyuz0-vllm-awq-qwen36-t3-baseline/
```

Keep it untracked until the vLLM AWQ run is either completed and documented or deliberately discarded.
