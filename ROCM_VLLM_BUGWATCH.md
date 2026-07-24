# ROCm and vLLM Bugwatch

Status: current as of 2026-07-24 for locally measured runtime paths and upstream release triage. External release rows retain their own checked dates.

This file tracks fast-moving upstream items that affect Strix Halo local AI work. It is intentionally separate from the README so the public guide stays stable even when upstream ROCm/vLLM issues move.

## Current Upstream Snapshot

| Area | Current status | Why it matters |
|------|----------------|----------------|
| `llama.cpp` release | [`llama.cpp` b10098](https://github.com/ggml-org/llama.cpp/releases/tag/b10098) is the latest upstream release audited here. | It includes Vulkan queue work, server validation fixes, speculative-draft sidecar/type handling, Qwen3-VL vision fixes, and DeepSeek4 fixes. None of those changes replaces a measured guide result until the relevant route is rerun. |
| Ollama release | [`Ollama 0.32.3`](https://github.com/ollama/ollama/releases/tag/v0.32.3) is the latest stable release audited here; 0.32.2 was withdrawn. | It includes a model-download stall fix and lower memory use on Linux CUDA/ROCm iGPUs. The installed, fully qualified beginner route remains 0.31.2 until 0.32.3 passes the same iGPU, vision, restart, and full-reboot checks. |
| ROCm production release | [`ROCm 7.14.0`](https://github.com/ROCm/ROCm/releases/tag/rocm-7.14.0) is the latest production ROCm release checked here, published 2026-07-16. | It focuses on AI inference across Instinct, Radeon, and Ryzen AI and moves the earlier 7.13 preview lane into a production release. This guide has not installed it host-wide. |
| ROCm Ryzen AI inference note | ROCm 7.14.0 documents lower-than-expected LLM inference on Ryzen AI MAX / MAX+ with PyTorch earlier than 2.14 in some FP16 vLLM workloads at batch 8+, with `TORCH_BLAS_PREFER_HIPBLASLT=1` as the workaround. | The isolated local A/B reproduced the expected threshold: +40.50%, +38.96%, and +41.54% aggregate throughput at concurrency 8, 9, and 16, with no material gain at 1 and a -0.77% result at 4. This remains an FP16 vLLM rule, not universal llama.cpp or Vulkan tuning. |
| vLLM release | [`vLLM 0.25.1`](https://github.com/vllm-project/vllm/releases/tag/v0.25.1) is the latest normal upstream release checked here, published 2026-07-14. ROCm 7.14.0 validates vLLM 0.23.0, which is not the same as claiming that upstream 0.25.1 is validated on this machine. | Use a pinned ROCm image or isolated environment and record both ROCm and vLLM versions. Do not pip-install into the host Python environment. |
| SGLang release | [`SGLang 0.5.15.post1`](https://github.com/sgl-project/sglang/releases/tag/v0.5.15.post1) is the latest upstream release checked here, published 2026-07-14. ROCm 7.14.0 validates SGLang 0.5.13. | Useful serving watch signal; no local Strix Halo performance claim is made from version availability alone. |
| Strix Halo unified memory reporting | [`ROCm/hip#3892`](https://github.com/ROCm/hip/issues/3892) is now closed as of 2026-05-29. | Still verify inside any ROCm/vLLM container before making a capacity/autoscheduling claim; closed upstream does not prove every local bundle has the fix. |
| Older 15.5GB VRAM aperture issue | [`ROCm/ROCm#5444`](https://github.com/ROCm/ROCm/issues/5444) is closed. | Keep as troubleshooting context; not a current headline blocker. |
| MES memory-access fault report | [`ROCm/ROCm#5724`](https://github.com/ROCm/ROCm/issues/5724) is closed. | Still relevant when diagnosing firmware/kernel regressions. |
| Qwen ROCm load/hang report | [`ROCm/ROCm#6027`](https://github.com/ROCm/ROCm/issues/6027) is closed. | Historical context for why the guide keeps ROCm notes conservative. |
| vLLM ROCm non-causal attention | [`vllm-project/vllm#40176`](https://github.com/vllm-project/vllm/pull/40176) is merged. | Relevant to ROCm attention support and newer vLLM container paths. |
| vLLM DFlash SWA support | [`vllm-project/vllm#40898`](https://github.com/vllm-project/vllm/pull/40898) remains open. | Relevant to Qwen3.6 DFlash speculative decoding repos; not a local guide claim yet. |

## Current Strix Halo Compatibility Alerts

These are narrowly scoped upstream reports, not blanket claims about Strix Halo, Linux, ROCm, or the named runtimes. Check the exact operating system, kernel, deployment type, backend, and environment-variable behavior before applying a workaround.

| Scope | Upstream status | Practical reading |
| --- | --- | --- |
| Kernel 7.0.0-28 + ComfyUI + PyTorch/ROCm unified-memory FLUX loading | [`ROCm/ROCm#6508`](https://github.com/ROCm/ROCm/issues/6508) is open. The report reproduces a silent KFD work-queue deadlock on kernel 7.0.0-28 while kernel 6.17.0-35 works on the same 128GB Strix Halo system. Smaller PyTorch tests and a 23GB ROCm `llama.cpp` load still worked. | Do not generalize this to every kernel-7.0 or ROCm workload. If a FLUX workflow stalls at VAE load after a kernel update, preserve the working kernel as a boot option and compare there before changing the model or reinstalling the full stack. |
| ROCm/HIP `mmap` above 64GB on Ubuntu 26.04 | [`ROCm/ROCm#6501`](https://github.com/ROCm/ROCm/issues/6501) is open. One `gfx1151` report says Vulkan works, ROCm works with `--no-mmap`, and an HRX HIP binding also allows the allocation. | For a large ROCm GGUF that stalls during mapping, try the exact same artifact with `--no-mmap` before concluding that it does not fit. Keep this separate from Vulkan guidance and from the guide's older prompt-processing `--no-mmap` measurements. |
| Ollama 0.30+ ROCm container memory detection | [`ollama/ollama#16462`](https://github.com/ollama/ollama/issues/16462) remains open and is explicitly about Docker/Podman deployments that expose roughly 2GB instead of the full unified-memory pool. Community workarounds include Vulkan or unified-memory environment settings. | This is not evidence that the guide's native Ollama system-service path is broken. Container users should verify the startup memory report and actual offload before pulling a large model. |
| Unsloth Windows ROCm prebuilt b10079 | [`unslothai/unsloth#7371`](https://github.com/unslothai/unsloth/issues/7371) reports roughly 11 tok/s on b10079 versus 39 tok/s on b10069 for two Qwen3.6 MTP routes. | Treat this as a Windows/prebuilt regression report, not a Linux or generic Unsloth result. Pin a known-good prebuilt when comparing speeds and record the exact bundled `llama.cpp` build. |
| DeepSeek V4 through ROCm/HIP `llama.cpp` | [`ggml-org/llama.cpp#25436`](https://github.com/ggml-org/llama.cpp/issues/25436) reports garbled output on Strix Halo. A key follow-up notes that defining `GGML_CUDA_ENABLE_UNIFIED_MEMORY=0` can still enable the code path because the implementation checks whether the variable exists. | If output is corrupted, remove the variable completely for the control run; do not assume assigning `0` disables it. Vulkan working on the same model is a useful comparator, not proof that every ROCm build is broken. |
| AMD Unsloth playbook NaN loss on `gfx1151` | [`amd/playbooks#611`](https://github.com/amd/playbooks/issues/611) reports NaNs with an older ROCm 7.2 environment. AMD replied that the current playbook uses ROCm 7.14 and passes on Strix Halo in its CI. | Match the playbook's pinned wheel versions before adding compiler workarounds. The guide's measured pinned workflow remains a functional smoke, not proof that every Unsloth/ROCm combination is safe. |

## 2026-07-13 Local Runtime Recheck

- The normal Ollama system service was upgraded and measured on 0.31.2. Qwen3.6 reached 60.57 t/s warm API generation with full iGPU offload; Qwen2.5-VL 7B vision, service restart, and full-host-reboot persistence passed. A separate user-local 0.31.1 run reached 71.82 t/s, but the controlled comparison below shows that this was not a version-wide 0.31.2 regression.
- Official `llama.cpp` b9979 was measured in the multi-user MoE campaign. The resulting Vulkan dispatch cliff and opt-in AMD/RADV recovery evidence are documented in [`MOE_CONCURRENCY.md`](MOE_CONCURRENCY.md).
- These measured updates supersede the easy-path/runtime statements in the dated 2026-07-06 section below; that section remains as a historical watch snapshot.

## 2026-07-16 Release And Runtime Recheck

- ROCm 7.14.0 is now the current production release. The release adds newer AI framework coverage and publishes a specific Ryzen AI MAX / MAX+ performance note for some FP16 vLLM workloads at batch 8 or greater.
- The official workaround is `TORCH_BLAS_PREFER_HIPBLASLT=1` when using PyTorch versions earlier than 2.14. An isolated official ROCm 7.14 / PyTorch 2.11 / vLLM A/B on this `gfx1151` system measured 480.98 versus 675.79 aggregate t/s at concurrency 8, 540.67 versus 751.33 at 9, and 896.83 versus 1269.40 at 16. At concurrency 1 the change was +0.10%; at 4 it was -0.77%.
- This is a successful reproduction of the release-note workaround for the pinned FP16 Qwen3-0.6B server workload. It is not interchangeable with the older llama.cpp `ROCBLAS_USE_HIPBLASLT=1` evidence and is not a universal recommendation for quantized models or low concurrency. Raw evidence is under [`data/raw/2026-07-16/rocm-714-vllm-hipblaslt-ab/`](data/raw/2026-07-16/rocm-714-vllm-hipblaslt-ab/); the compact A/B is [`data/rocm_714_hipblaslt_ab.csv`](data/rocm_714_hipblaslt_ab.csv).
- vLLM 0.25.1 and SGLang 0.5.15.post1 are newer upstream than the versions validated in ROCm 7.14.0. Record that distinction instead of presenting the newest package combination as supported by default.
- ROCm 7.14 lists significantly longer LLM warmup times on some Radeon GPUs with vLLM 0.21.0 through 0.25.0; AMD's published workaround is to use a release before 0.21.0 or 0.26.0 and later. The latest upstream version checked here is still 0.25.1, so cache/warmup timing must remain part of every local vLLM report.
- ROCm 7.14 also marks Radeon SGLang support as initial. For the validated image family, AMD advises `SGLANG_USE_AITER=false` and `SGLANG_ROCM_FUSED_DECODE_MLA=false`; some MoE and Qwen3-ASR routes still need newer upstream fixes. Treat these as official setup caveats, not local performance claims.
- A controlled same-cache Ollama comparison measured 0.31.1, 0.31.2, and 0.32.0 at 72.55, 73.19, and 73.20 t/s respectively over nine warm requests. The earlier 60.57-versus-71.82 observation was not a version-wide regression.
- Official llama.cpp b10046 is the latest release checked. It includes merged PR #24233, which restores the integrated-device property for HIP builds. The official b10046 ROCm binary locally detected 120,124 MiB free UMA and used `ROCm_Host` model, output, and compute buffers on `gfx1151` without `HSA_OVERRIDE_GFX_VERSION`. The release binary needed the existing Ollama ROCm library path on this host; this is a compatibility/setup result, not a replacement Vulkan speed run.

## 2026-07-06 Watch Recheck

No benchmark recommendation changed in this recheck:

- ROCm production remains 7.2.4 in this guide's checked production lane.
- vLLM moved to 0.24.0 upstream. Treat this as a container/watchlist update only; it does not make vLLM/DFlash a guide recommendation without a clean local Strix Halo reproduction.
- `llama.cpp` latest official release moved to b9888 and was measured as a Vulkan/RADV sentinel. It reproduced the Qwen3-Coder 98 t/s class, but did not replace the stronger b9851 100.99 t/s direct speed-first headline.
- Ollama latest remains 0.31.1 in the checked easy-path lane; the measured local buyer-path claim is still the 2026-07-02 user-local 0.31.1 run with `OLLAMA_IGPU_ENABLE=1`.

## 2026-06-12 Watch Recheck

No benchmark recommendation changed in this recheck:

- ROCm production remains 7.2.4.
- vLLM remains 0.22.1 as the latest normal upstream vLLM release checked here.
- `llama.cpp` latest release moved beyond the earlier b9544 checkpoint to b9601. This is an update-watch signal only; the guide's measured local controls remain tied to their exact commits and raw evidence.
- Ollama latest release moved to 0.30.7, while the installed local guide path remains Ollama 0.23.1 until an isolated update check proves that changing it helps the easy buyer path.
- Keep host-wide ROCm/Ollama/llama.cpp updates out of benchmark campaigns unless the whole campaign is explicitly about testing that update.

## Local ROCm State

This guide machine does not currently have a host-wide `/opt/rocm` install, `rocminfo`, or `hipcc` on `PATH`.

Available ROCm paths:

| Path | Status |
|------|--------|
| `/usr/local/lib/ollama/rocm` | Ollama-bundled ROCm runtime libraries; includes HIP/rocBLAS/hipBLAS 7.2-series libraries used by local HIP spot checks. |
| `rocm/dev-ubuntu-24.04:7.2-complete` | Docker image is present locally. Useful for isolated experiments, not used as a host install. |
| Lemonade `llamacpp-rocm` b1259 bundle | Measured server path with ROCm 7.13-era bundled libraries; strongest measured aggregate throughput at 8-16 parallel Qwen3.6 requests. |
| Official ROCm 7.14 RDNA vLLM image | Isolated image digest `sha256:5b0389109bb2db9346d3f0f971c4c99eba7e5e72cfa57e9a2a9b4ac67477771d` initialized on `gfx1151`; PyTorch 2.11 / HIP 7.14 / vLLM 0.23.1.dev1 FP16 A/B completed without request errors. The host ROCm stack was not changed. |
| Official llama.cpp b10046 ROCm binary | Merged HIP integrated-device support reproduced on `gfx1151`: full UMA discovery plus real `ROCm_Host` model/output/compute allocations without a gfx override. Required `LD_LIBRARY_PATH=/usr/local/lib/ollama/rocm_v7_2` on this host. |

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

## 2026-05-31 Upstream Watch Refresh

Latest watch changes:

- ROCm production moved to 7.2.4 on 2026-05-29.
- vLLM moved to 0.22.0 on 2026-05-29.
- `ROCm/hip#3892` is closed, but any local ROCm/vLLM path should still record memory reporting from inside the actual container or bundle before claiming full unified-memory scheduler behavior.
- `vllm-project/vllm#40898` remains open, so DFlash/SWA support is still a watch item rather than a reproduced guide claim.
- Latest local `llama.cpp` b9442 direct Qwen3-Coder check did not improve the Qwen3-Coder direct row; that remains b9179 Q4_K_S at 98.51 t/s. A later b9467 scout added a separate Qwen3-30B-A3B-Instruct-2507 IQ4_XS direct 100.04 t/s row, and the experimental MTP server route remains b9360 at about 101.1 t/s.

## 2026-06-01 Watch Recheck

No new public guide claim changed in the 2026-06-01 recheck:

- ROCm production remained 7.2.4 as the latest checked production release.
- vLLM remained 0.22.0 as the latest checked normal upstream release.
- Local installed Ollama remained 0.23.1; the previous isolated Ollama 0.24.0 API check already found no speedup versus the same-prompt 0.23.1 control.
- Local `llama.cpp` latest-stack evidence moved to `de6f727aa` on 2026-06-01. The direct Qwen3-Coder Q4_K_S check measured 95.55 t/s tg128 with `mmap=0`, so it is useful negative evidence, not a new headline.
- Keep ROCm/vLLM/DFlash work in isolated containers or extracted bundles until a reproducible 27B/35B serving row beats or complements the existing `llama-server` and Ollama paths.

## 2026-06-07 Watch Recheck

No benchmark recommendation changed in this recheck:

- `llama.cpp` latest release was b9544 at this checkpoint, while the local source checkout used for recent experiments was behind that release. This made a latest-release regression run useful before telling users to update.
- Ollama latest release was 0.30.6 at this checkpoint, while the installed local Ollama remained 0.23.1. This was a buyer-facing update candidate because Ollama is the easiest setup path.
- ROCm production remains 7.2.4.
- vLLM moved to 0.22.1. Treat this as a watch/update signal only; it does not make vLLM/DFlash a guide recommendation without a clean local reproduction.
- Atomic TurboQuant PR #26 for Gemma 4 MTP `PARALLEL=2` has merged. The Nimo Gemma 4 QAT/MTP route remains an advanced path until fresh post-merge 1-slot and 2-slot numbers are measured with exact Atomic commit, command, acceptance rate, single-stream decode, and aggregate throughput.

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
- vLLM is now locally reproduced for an isolated Qwen3-0.6B FP16 hipBLASLt A/B, but it remains experimental for the guide's practical 27B/35B model class until a comparable larger-model serving run is measured.
- Host-wide ROCm upgrades should be avoided during benchmark campaigns unless the whole run is dedicated to testing that stack.

## Next Watch Items

1. Qualify Ollama 0.32.3 through the normal system-service path, including model pulling, iGPU detection, vision, service restart, and a full host reboot.
2. Recheck a relevant Vulkan/server route on `llama.cpp` b10098 without replacing the b10034 concurrency or b10066 DFlash sentinels prematurely.
3. Repeat the measured ROCm 7.14 hipBLASLt A/B on a practical 27B/35B FP16 or supported low-precision model before promoting it from a small-model server proof to a normal operator profile.
4. Repeat the b10046 HIP host-buffer path with a practical 27B/35B GGUF and record whether a self-contained package can avoid the manual Ollama library path.
5. Recheck vLLM 0.26.0-or-later availability and warmup behavior before treating 0.25.x as the current Radeon default.
6. Recheck `vllm-project/vllm#40898` before trying to reproduce DFlash/SWA behavior.
7. Use the ROCm 7.14 Radeon SGLang environment overrides for the next isolated smoke and keep affected MoE/ASR routes labeled experimental.
8. Verify local memory reporting inside the exact ROCm 7.14.0, TheRock, vLLM, or Ollama container before making a capacity or autoscheduling claim.
9. Preserve a known-working kernel as a boot option during ComfyUI/FLUX kernel qualification, and compare there before rebuilding the whole stack.
10. For DeepSeek ROCm controls, remove `GGML_CUDA_ENABLE_UNIFIED_MEMORY` from the environment instead of setting it to `0`.
11. Recheck ROCm 7.14.0 RCCL notes before any future multi-node Strix Halo claim.
12. If installing ROCm 7.14.0 host-wide becomes necessary, treat it as a dedicated maintenance window and record a new system snapshot before publishing numbers.
