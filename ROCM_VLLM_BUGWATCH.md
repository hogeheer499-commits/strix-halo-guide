# ROCm and vLLM Bugwatch

Status: current as of 2026-05-23.

This file tracks fast-moving upstream items that affect Strix Halo local AI work. It is intentionally separate from the README so the public guide stays stable even when upstream ROCm/vLLM issues move.

## Current Upstream Snapshot

| Area | Current status | Why it matters |
|------|----------------|----------------|
| ROCm production release | [`ROCm 7.2.3`](https://github.com/ROCm/ROCm/releases/tag/rocm-7.2.3) remains the latest production ROCm release checked here, published 2026-05-04. | Production documentation still points to 7.2.3 for normal use. This guide did not install it host-wide. |
| ROCm preview release | [`ROCm 7.13.0 Preview`](https://rocm.docs.amd.com/en/7.13.0-preview/about/release-notes.html) is the latest preview stream checked here, published 2026-05-15. | It adds official gfx1151/vLLM image coverage and RCCL multi-node optimization for AMD Ryzen AI Max 300 series, but it is a preview stream and should stay isolated from the host. |
| vLLM release | [`vLLM 0.21.0`](https://docs.vllm.ai/en/v0.21.0/getting_started/installation/gpu/) is the latest normal upstream vLLM release checked here. ROCm 7.13.0 Preview also documents vLLM 0.19.1 images for gfx1151/gfx1150/gfx1152. | Useful signal for future containers; do not pip-install into the host Python environment for this guide. |
| Strix Halo unified memory reporting | [`ROCm/hip#3892`](https://github.com/ROCm/hip/issues/3892) remains open. | Some HIP APIs can report VRAM aperture instead of unified memory, which can confuse schedulers and capacity checks. |
| Older 15.5GB VRAM aperture issue | [`ROCm/ROCm#5444`](https://github.com/ROCm/ROCm/issues/5444) is closed. | Keep as troubleshooting context; not a current headline blocker. |
| MES memory-access fault report | [`ROCm/ROCm#5724`](https://github.com/ROCm/ROCm/issues/5724) is closed. | Still relevant when diagnosing firmware/kernel regressions. |
| Qwen ROCm load/hang report | [`ROCm/ROCm#6027`](https://github.com/ROCm/ROCm/issues/6027) is closed. | Historical context for why the guide keeps ROCm notes conservative. |
| vLLM ROCm non-causal attention | [`vllm-project/vllm#40176`](https://github.com/vllm-project/vllm/pull/40176) is merged. | Relevant to ROCm attention support and newer vLLM container paths. |
| vLLM DFlash SWA support | [`vllm-project/vllm#40898`](https://github.com/vllm-project/vllm/pull/40898) remains open. | Relevant to Qwen3.6 DFlash speculative decoding repos; not a local guide claim yet. |

## Local ROCm State

This guide machine does not currently have a host-wide `/opt/rocm` install, `rocminfo`, or `hipcc` on `PATH`.

Available ROCm paths:

| Path | Status |
|------|--------|
| `/usr/local/lib/ollama/rocm` | Ollama-bundled ROCm runtime libraries; includes HIP/rocBLAS/hipBLAS 7.2-series libraries used by local HIP spot checks. |
| `rocm/dev-ubuntu-24.04:7.2-complete` | Docker image is present locally. Useful for isolated experiments, not used as a host install. |
| Lemonade `llamacpp-rocm` b1259 bundle | Measured server path with ROCm 7.13-era bundled libraries; strongest measured aggregate throughput at 8-16 parallel Qwen3.6 requests. |

Do not install ROCm, PyTorch, TheRock, or vLLM directly into the host Python environment for this guide. Prefer containers or self-contained extracted bundles so failed experiments do not corrupt the workstation setup.

## 2026-05-16 Local Refresh

Raw refresh:

- [`data/raw/2026-05-16/vllm-preflight-refresh/`](data/raw/2026-05-16/vllm-preflight-refresh/)
- [`data/raw/2026-05-16/lucebox-dflash-preflight/`](data/raw/2026-05-16/lucebox-dflash-preflight/)

Local container status:

- `vllm-gfx1151` still starts.
- ROCm SMI inside the container sees Radeon 8060S / `gfx1151`.
- Container versions:
  - vLLM `0.19.2rc1.dev113+g6aa057c9d.d20260422.rocm713`
  - PyTorch `2.13.0a0+rocm7.13.0a20260422`
  - Triton `3.7.0+git6aa07328.rocm7.13.0a20260422`
- Existing local AWQ smoke remains about 25 t/s at `np=1`, so plain AWQ is not a default-speed win.

Lucebox DFlash/PFlash status:

- Lucebox is a high-upside experimental lead for Qwen3.5/Qwen3.6 27B DFlash/PFlash on Strix Halo.
- Local clone succeeded, but HIP CMake preflight failed because this host has no ROCm root / `hipcc`.
- Next safe path is an isolated ROCm/HIP developer container or toolbox with hipcc and rocWMMA, not a host-wide ROCm dev install.

## 2026-05-23 Upstream Watch Refresh

ROCm 7.13.0 Preview is the new high-signal watch item for this guide, but not a reason to mutate the host install.

Relevant upstream signals:

- ROCm 7.13.0 Preview documents vLLM Docker images and pip packages with architecture-specific images including AMD Ryzen AI APUs `gfx1150`, `gfx1151`, and `gfx1152`.
- The same preview documents RCCL multi-node optimization for AMD Ryzen AI Max 300 systems over Ethernet, targeting distributed inference workloads with tensor parallelism and expert parallelism across up to four nodes.
- ROCm Compute Profiler now calls out RDNA 3.5 support for AMD Ryzen AI Max 300 series profiling and analysis.

Practical guide interpretation:

- Keep the public default unchanged: Vulkan/RADV remains the measured beginner path for normal GGUF chat/coding generation.
- Treat ROCm 7.13 Preview as the next isolated vLLM/RCCL/container lane, not a host-wide upgrade.
- If tested, capture container image digest, ROCm component versions, `rocminfo`, model source/hash, startup logs, TTFT, throughput, and failure modes before adding claims.

## vLLM AWQ/DFlash Lead

[`hec-ovi/vllm-awq4-qwen`](https://github.com/hec-ovi/vllm-awq4-qwen) is now an important Strix Halo lead:

- Qwen3.6-27B AWQ-INT4.
- DFlash speculative decoding.
- OpenAI-compatible API, vision, tools, and 256K context claims.
- Docker-first setup.
- Reported single-stream and 3-stream throughput, plus custom HIP prefill kernel work.

Local status in this guide: not reproduced yet. The repo requires a heavier Docker build, model downloads, and at least one gated drafter-model acceptance path. Until reproduced locally, it belongs in the candidate/experimental bucket, not in headline measured numbers.

## Practical Impact On The Guide

The README recommendation should stay conservative:

- Vulkan/RADV remains the default for easiest chat and fastest measured generation.
- ROCm/HIP is no longer treated as broken; it is relevant for prompt-heavy workloads, high-concurrency server paths, vLLM, AWQ/DFlash, and future tuned rocWMMA work.
- vLLM is promising but still experimental in this guide until a comparable 27B/35B throughput run is reproduced locally.
- Host-wide ROCm upgrades should be avoided during benchmark campaigns unless the whole run is dedicated to testing that stack.

## Next Watch Items

1. Recheck `ROCm/hip#3892` before any vLLM capacity/autoscheduling claim.
2. Recheck `vllm-project/vllm#40898` before trying to reproduce DFlash/SWA behavior.
3. Test ROCm 7.13 Preview vLLM images only through a container or isolated environment.
4. Recheck ROCm 7.13 Preview RCCL notes before any future multi-node Strix Halo claim.
5. If installing ROCm 7.2.3 or preview ROCm host-wide becomes necessary, treat it as a dedicated maintenance window and record a new system snapshot before publishing numbers.
