---
layout: default
title: "AMD Strix Halo Troubleshooting: Ollama, Vulkan, ROCm, and Unified Memory"
description: "Symptom-first troubleshooting for AMD Strix Halo local LLM setup: Ollama CPU fallback, llama.cpp batch clamps, RADV selection, firmware, GTT, ROCm overrides, and HIP correctness."
permalink: /troubleshooting/
canonical_url: "https://strixhaloguide.com/troubleshooting/"
sitemap: false
date: "2026-08-30T00:00:00+02:00"
last_modified_at: "2026-10-01T00:00:00+02:00"
image:
  path: "https://hogeheer499-commits.github.io/strix-halo-guide/assets/social-preview.png"
  height: 640
  width: 1280
  alt: "AMD Strix Halo local LLM troubleshooting for Ollama, Vulkan, ROCm, and unified memory"
seo:
  type: "TechArticle"
  date_modified: "2026-10-01T00:00:00+02:00"
---

# AMD Strix Halo Local LLM Troubleshooting

**September 19 functional update:** the [scoped runtime qualification](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/RUNTIME_QUALIFICATION_2026-09-19.md)
records text (Qwen3.6), image (Qwen2.5-VL), executed tools (Devstral) and pinned
Open WebUI on the existing 0.32.15 service after restart. Isolated 0.34.2 is
useful but not default; official Qwen3.8 and full-reboot candidate acceptance
remain open. The tested host's Ollama listener was LAN-reachable, not local-only.
Released llama.cpp v0.4.1 passed bounded direct/server/HIP controls; this does
not qualify every model, long-context shape or maximum-memory allocation.

**Evidence reviewed:** October 1, 2026.

**Security status (checked 2026-09-30):** published advisories cover the pinned
Open WebUI 0.10.2 image and the Ollama 0.31.2 version that `setup.sh` installs;
see [Security status of pinned components](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/SECURITY.md#security-status-of-pinned-components)
and the [local AI security checklist](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/SECURE_LOCAL_AI.md).

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

Why the guide keeps the Vulkan route and hides HIP devices: upstream
[ollama#17895](https://github.com/ollama/ollama/issues/17895) (open, checked
2026-09-25) reports that Ollama's bundled ROCm backend returns wrong output for
prompts above about 4K tokens on gfx1151, while Vulkan and CPU are correct on
the same machine. It was reported on Ollama 0.32.5 through 0.32.14 and has not
been tested here on 0.33 or 0.34. `OLLAMA_VULKAN=1` plus
`HIP_VISIBLE_DEVICES=-1` keeps the service off that ROCm path.

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

**Check:** inspect the installed firmware packages with
`dpkg-query -W 'linux-firmware*'` and
`apt-cache policy linux-firmware-amd-graphics`. `20251125` is an upstream tag
reported in Fedora packaging; Ubuntu version strings never contain it. On
Ubuntu 24.04, `linux-firmware` has been a metapackage since 2026-09-03 and the
AMD GPU blobs ship in `linux-firmware-amd-graphics` (checked 2026-09-25).

**Fix:** do not use `linux-firmware-20251125` on the documented Strix Halo ROCm
path; inspect available distro packages, restore an unaffected version, reboot and
repeat the GPU/model checks. On Ubuntu 24.04, restore or hold
`linux-firmware-amd-graphics`; a hold on the `linux-firmware` metapackage does
not stop amdgpu firmware updates. No known-good version is qualified by the
guide. Holding a package does not downgrade it. See
[Step 4.4 of the README](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#step-44-linux-firmware).

## Large Models Cannot See The Expected GTT Pool

**Symptom:** the OS or runtime exposes too little GPU-accessible shared memory,
or a model that should fit fails during allocation.

**Check:** inspect `/sys/module/amdgpu/parameters/gttsize`,
`/sys/module/ttm/parameters/pages_limit`, the active kernel command line, and
`free -h`.

**Fix:** compare the selected RAM/kernel profile with actual allocation needs.
The guide's recorded 128GB Beelink profile is
`amdgpu.gttsize=131072 ttm.pages_limit=31457280 amdgpu.cwsr_enable=0`
(`cwsr_enable=0` disables compute wave save/restore, i.e. mid-wave compute preemption; ROCm/ROCm#5590 workaround). It is
not a 96GB or 192GB preset or a universal OOM fix. Upstream kernel master
(checked 2026-09-25) logs `gttsize`
as deprecated in favour of `ttm.pages_limit`. Preserve
unrelated settings, resolve conflicts, and verify live values after any reboot.
Use the complete
[kernel-parameter procedure](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#step-32-configure-grub-boot-parameters).

## A Stale ROCm Override Reports `gfx1100` Or Segfaults

**Symptom:** a current container reports `gfx1100` instead of native `gfx1151`,
or crashes during model load.

**Check:** run `printenv HSA_OVERRIDE_GFX_VERSION` and compare device detection
with the variable unset.

**Fix:** remove a stale global `HSA_OVERRIDE_GFX_VERSION` from host shell or
service startup files and retry. Keep the older `11.5.1` value only in commands
that deliberately reproduce the dated b8460/kernel 6.19.4 evidence. See the
[current ROCm migration check](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#rocm-migration-check-july-2026).

## HIP Loads, But Does The Exact Workload Remain Correct?

**Symptom:** long-context, vision, or multi-slot HIP output repeats or becomes
garbled on the integrated-host compute path described by upstream reports.

**Check (September 19 status):** compare exact outputs on historical stock
b10687 and released v0.4.1, recording the model, prompt, context, backend commit,
usable memory and buffer path. [Issue #26209](https://github.com/ggml-org/llama.cpp/issues/26209)
remains open. [PR #25863](https://github.com/ggml-org/llama.cpp/pull/25863) closed
unmerged; [#28604](https://github.com/ggml-org/llama.cpp/pull/28604) shipped the
revert mitigation. Broader scheduler PR #27311 remains open. The September 19
Coder controls passed on the release at 4,579 and 14,029 prompt tokens and with
two concurrent distinct markers; historical b10687 failed retrieval and both
slots. Both builds passed the Gemma image fixture. These are scoped controls,
not general Qwen3.8, maximum-memory or all-model HIP qualification.

**Fix:** pin a known-good or patched HIP build and run exact-output controls
before making a practical-model recommendation; use the documented Vulkan route
as a comparator when appropriate. The guide's b10046 result is only a small-model
allocation/setup smoke, not long-context, multimodal, or multi-slot correctness.
Read the scoped
[upstream compatibility alert](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#current-upstream-compatibility-alerts).

## Text From Another Conversation Appears In An Answer

**Symptom:** a reply answers a different, earlier conversation, or repeats text
that your prompt never contained. Nothing in the response marks it; for
`llama-server` the `cached_tokens` counter showed 0 in the reports.

**Reported causes (checked 2026-09-30; none reproduced here):**

- `llama-server`: [llama.cpp#27148](https://github.com/ggml-org/llama.cpp/issues/27148)
  (open) reports that the default `--cache-ram` and `--cache-idle-slots` can
  restore an unrelated, finished conversation into a slot for a new request. The
  reporters ran Strix Halo with ROCm, one of them in router mode with a single
  user. Whether Vulkan builds are affected is not established.
- Ollama's bundled ROCm server: [ollama#18528](https://github.com/ollama/ollama/issues/18528)
  and [llama.cpp#29092](https://github.com/ggml-org/llama.cpp/issues/29092) (both
  open) report earlier prompts' text in later responses with Ollama 0.32.14 and
  0.34.1 on Qwen3.6-35B-A3B and Qwen3.8-27B. The reports concern the ROCm backend;
  this guide's Ollama setup runs Vulkan with HIP devices hidden, and this guide has
  not reproduced the leak on either backend.

**Check:** note the server and version, whether it uses the ROCm or Vulkan
backend, and whether more than one conversation or client shares the process.

**Mitigation reported by others, not tested here:** start `llama-server` with
`--cache-ram 0 --no-cache-idle-slots` (the reporters say both are needed with
several parallel slots). Until this is resolved, do not share one server between
people or agents of different trust; see
[shared servers](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/SECURE_LOCAL_AI.md#shared-servers).

## Out Of Memory After A Very Long Context

**Symptom:** the process is killed by the out-of-memory handler after a long
agent session or a very large context, although the model loaded fine.

**Reported cause (checked 2026-09-30; not measured here):** a large `-ub`
reserves a compute buffer when the model loads. A third-party fork's
[issue #6](https://github.com/pwilkin/strix-halo/issues/6) (open, 2026-09-22)
reports that its default `-b 16384 -ub 16384` on 128GB with a 262K context
reserved about 16GB at load and was killed near 178K tokens; in an 11-run sweep
`-ub 8192` left about 8GB more free for about 5% less prefill. That was the
fork's own default, not a route from this guide, whose commands use `-ub` up to
2048. Treat it as a warning for anyone running forks or high `-ub` profiles.

**Check:** read `-b` and `-ub` in the exact command and compare `free -h` before
and after loading.

**Fix:** lower `-ub` and measure again. Keep `-ub` no larger than `-b` (see the
batch-clamp entry above).

## Qwen3.8-Flash-Next Q4 Runs Out Of Memory On ROCm/HIP

**Symptom:** loading a Q4_K_M-class quant of Qwen3.8-Flash-Next (about 111GB)
on the ROCm/HIP backend swaps or is killed, while the IQ4_XS route measured here
loads.

**Reports of others (to verify, checked 2026-09-30):** a Level1Techs forum
[thread](https://forum.level1techs.com/t/franken-strix-halo-2x-r9700s-128gb-strix-halo-unified-memory/254736)
(2026-09-03) says mainline `llama.cpp` on HIP puts a roughly 33GiB n-gram
embedding table into GTT, which makes Q4_K_M not viable on the iGPU alone, and
describes a community fork as a workaround. A Framework forum
[thread](https://community.frame.work/t/qwen3-8-please-share-your-t-s-any-quant/84405)
reports that the largest quant that fit on a 128GiB system alone was IQ4_XS and
that larger sizes were killed by the out-of-memory handler; it does not state the
backend. This guide measured IQ4_XS on Vulkan/RADV (see the
[model hub](https://strixhaloguide.com/strix-halo-models/)) and has not tested
Q4_K_M on HIP.

**Fix:** use the measured IQ4_XS Vulkan/RADV route; if you try HIP with a larger
quant, watch `free -h` and expect memory pressure before downloading 111GB.

## Prompts Appear In LM Studio Logs

**Symptom:** prompt text is readable in LM Studio's log files after a session.

**Report (checked 2026-09-30; preprint, not tested here):**
[arXiv 2609.18526](https://arxiv.org/abs/2609.18526) (2026-09-16, not peer
reviewed, tested on an NVIDIA GPU with LM Studio 0.4.21) found that the default
configuration had a setting named `logSensitiveData` enabled and that test prompts
were recoverable from plain-text logs days later. With the setting disabled, the
authors found no such traces. This guide has not tested LM Studio's logging.

**Fix:** turn `logSensitiveData` off if your LM Studio version exposes it (to
verify in your version), and delete old logs if the prompts were sensitive.

## Independence And Affiliate Disclosure

This guide contains no affiliate links as of September 19, 2026. Future affiliate,
loaned, gifted, sponsored, or early-access relationships must be disclosed near
the relevant links or results and do not buy positive conclusions.
