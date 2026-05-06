# Maintainer Notes

These notes are for the local Hoge Heer workstation workflow. They are intentionally separate from the public README because they are not required to reproduce Strix Halo performance on another machine.

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

## Scratch Data

The directory below contains incomplete vLLM startup artifacts and is not a publishable result:

```text
data/raw/2026-05-05/server-shootout/kyuz0-vllm-awq-qwen36-t3-baseline/
```

Keep it untracked until the vLLM AWQ run is either completed and documented or deliberately discarded.
