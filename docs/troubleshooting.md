---
layout: default
title: "AMD Strix Halo Troubleshooting: Ollama, Vulkan, ROCm, and Unified Memory"
description: "Symptom-first troubleshooting for AMD Strix Halo local LLM setup: Ollama CPU fallback, llama.cpp batch clamps, RADV selection, firmware, GTT, ROCm overrides, and HIP correctness."
permalink: /troubleshooting/
date: "2026-08-30T00:00:00+02:00"
last_modified_at: "2026-08-30T00:00:00+02:00"
image:
  path: "https://hogeheer499-commits.github.io/strix-halo-guide/assets/social-preview.png"
  height: 640
  width: 1280
  alt: "AMD Strix Halo local LLM troubleshooting for Ollama, Vulkan, ROCm, and unified memory"
seo:
  type: "TechArticle"
  date_modified: "2026-08-30T00:00:00+02:00"
---

# AMD Strix Halo Local LLM Troubleshooting

**Evidence reviewed:** August 30, 2026.

This page extracts the most useful checks from the canonical
[README troubleshooting](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#troubleshooting),
[known-issues section](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#known-issues),
and [concise setup guide](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/STRIX_HALO_LOCAL_LLM_SETUP.md).
Those files remain the source of truth for full commands, dated evidence, and
caveats.

## Ollama Runs, But Falls Back To CPU

**Symptom:** generation completes but is far slower than the guide's measured
GPU routes. The measured Ollama 0.31.x builds could detect Radeon 8060S and then
drop the integrated-GPU path when `OLLAMA_IGPU_ENABLE=1` was missing.

**Check:** run `ollama ps`, then inspect `journalctl -u ollama` for Vulkan,
iGPU, and GPU messages.

**Fix:** make sure the service has `OLLAMA_VULKAN=1`,
`OLLAMA_IGPU_ENABLE=1`, and `HIP_VISIBLE_DEVICES=-1`; reload systemd and restart
Ollama. Follow the full
[README troubleshooting entry](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#troubleshooting).

## Prompt Processing Is Slow Because `-ub` Exceeds `-b`

**Symptom:** prompt processing is below the relevant guide row while generation
looks normal.

**Check:** compare the `-b` and `-ub` values in the exact command. `llama.cpp`
silently clamps `-ub` to `min(n_batch, n_ubatch)` when `-ub` is larger.

**Fix:** use a micro-batch no larger than the batch and rerun the same command
before changing the model or backend. See the
[canonical batch-clamp troubleshooting note](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#troubleshooting).

## AMDVLK Silently Wins ICD Selection Instead Of RADV

**Symptom:** Vulkan inference works, but prompt processing is unexpectedly slow
or output identifies the AMD open-source driver instead of RADV STRIX_HALO.

**Check:** inspect `vulkaninfo --summary` and the device/driver lines printed by
`llama-bench`.

**Fix:** remove AMDVLK so its ICD file cannot override RADV. An explicit RADV
ICD selection can be used as a diagnostic, but the guide's normal path keeps
AMDVLK uninstalled. Read the full
[Vulkan driver correction](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#vulkan-driver-comparison).

## `linux-firmware-20251125` Breaks The ROCm Path

**Symptom:** instability, crashes, or ROCm containers failing to start after a
firmware-package change.

**Check:** inspect the installed `linux-firmware` package version.

**Fix:** do not use `linux-firmware-20251125` on the documented Strix Halo ROCm
path; follow the pinned downgrade/upgrade commands and safe-version guidance in
[Step 4.4 of the README](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#step-44-linux-firmware).

## Large Models Cannot See The Expected GTT Pool

**Symptom:** the OS or runtime exposes too little GPU-accessible shared memory,
or a model that should fit fails during allocation.

**Check:** inspect `/sys/module/amdgpu/parameters/gttsize`,
`/sys/module/ttm/parameters/pages_limit`, the active kernel command line, and
`free -h`.

**Fix:** apply the guide's documented
`amdgpu.gttsize=131072 ttm.pages_limit=31457280` boot parameters, update GRUB,
reboot, and verify the active values before retrying. Use the complete
[kernel-parameter procedure](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#step-32-configure-grub-boot-parameters).

## A Stale ROCm Override Reports `gfx1100` Or Segfaults

**Symptom:** a current container reports `gfx1100` instead of native `gfx1151`,
or crashes during model load.

**Check:** run `printenv HSA_OVERRIDE_GFX_VERSION` and compare device detection
with the variable unset.

**Fix:** remove a stale global `HSA_OVERRIDE_GFX_VERSION` from host shell or
service startup files and retry. Keep the older `11.5.1` value only in commands
that deliberately reproduce the dated b8460/kernel 6.19.4 evidence. See the
[current ROCm migration check](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#current-rocm-migration-check-july-2026).

## HIP Loads, But Correctness Is Not Yet Qualified

**Symptom:** long-context, vision, or multi-slot HIP output repeats or becomes
garbled on the integrated-host compute path described by upstream reports.

**Check:** compare exact outputs on a stock build and the fix candidate, while
recording the model, prompt, context, backend commit, and buffer path.
[`llama.cpp` issue #26209](https://github.com/ggml-org/llama.cpp/issues/26209)
and [PR #25863](https://github.com/ggml-org/llama.cpp/pull/25863) were both still
open when rechecked 2026-08-30.

**Fix:** pin a known-good or patched HIP build and run exact-output controls
before making a practical-model recommendation; use the documented Vulkan route
as a comparator when appropriate. The guide's b10046 result is only a small-model
allocation/setup smoke, not long-context, multimodal, or multi-slot correctness.
Read the scoped
[upstream compatibility alert](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#current-upstream-compatibility-alerts).

## Independence And Affiliate Disclosure

This guide contains no affiliate links as of August 30, 2026. Future affiliate,
loaned, gifted, sponsored, or early-access relationships must be disclosed near
the relevant links or results and do not buy positive conclusions.
