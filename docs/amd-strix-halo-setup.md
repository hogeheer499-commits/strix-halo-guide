---
layout: default
title: "AMD Strix Halo Setup: BIOS, UMA, IOMMU, Ubuntu and Local LLMs"
description: "Measured AMD Strix Halo and Ryzen AI MAX+ 395 setup guidance for BIOS UMA, IOMMU, Ubuntu 24.04, Vulkan/RADV, Ollama and llama.cpp."
permalink: /amd-strix-halo-setup/
canonical_url: "https://strixhaloguide.com/amd-strix-halo-setup/"
sitemap: false
date: "2026-08-14T00:00:00+02:00"
last_modified_at: "2026-10-03T00:00:00+02:00"
image:
  path: "https://hogeheer499-commits.github.io/strix-halo-guide/assets/social-preview.png"
  height: 640
  width: 1280
  alt: "AMD Strix Halo Local LLM Guide with direct, server, and unified-memory evidence highlights"
seo:
  type: "TechArticle"
  date_modified: "2026-10-03T00:00:00+02:00"
---

# AMD Strix Halo Setup: BIOS, UMA, IOMMU, Ubuntu and Local LLMs

**September 19 functional update:** the [scoped runtime qualification](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/RUNTIME_QUALIFICATION_2026-09-19.md)
records text (Qwen3.6), image (Qwen2.5-VL), executed tools (Devstral) and pinned
Open WebUI on the existing 0.32.15 service after restart. Isolated 0.34.2 is
useful but not default; official Qwen3.8 and full-reboot candidate acceptance
remain open. The tested host's Ollama listener was LAN-reachable, not local-only.
Released llama.cpp v0.4.1 passed bounded direct/server/HIP controls; this does
not qualify every model, long-context shape or maximum-memory allocation.

**Canonical readable setup:**
[strixhaloguide.com/amd-strix-halo-setup/](https://strixhaloguide.com/amd-strix-halo-setup/).
This GitHub Pages page is the technical mirror; exact evidence remains in the
repository.

This is the practical starting configuration measured by the independent
[AMD Strix Halo Local LLM Guide](https://github.com/hogeheer499-commits/strix-halo-guide).
It targets Ryzen AI MAX+ 395 / Radeon 8060S (`gfx1151`) systems with 96GB or
128GB unified memory. The primary first-party machine is a 128GB Beelink GTR9
Pro; BIOS labels, firmware, cooling and power modes can differ on other OEM
systems.

**Setup reviewed:** October 1, 2026. Exact benchmark claims remain canonical in
the repository's structured data and raw evidence.

The setup script preserves administrator Ollama drop-ins and stops on unresolved
environment conflicts or legacy custom GPU rules. Existing installations may
therefore need manual review; writing configuration does not qualify an upgrade
or prove GPU offload. See [the manual configuration and access checks](../README.md#step-34-verify-gpu-access).

Running the current official dense Qwen model? Use the dedicated
[Qwen3.8 27B on Strix Halo route comparison](https://strixhaloguide.com/qwen38-strix-halo/)
for the measured Ollama path, context boundary, MTP/DFlash distinctions, and
current community performance leads.

If setup is already failing, use the symptom-first
[Strix Halo troubleshooting page](https://strixhaloguide.com/troubleshooting/).
To choose between measured routes and newer unmeasured artifacts, use the
[Strix Halo model hub](https://strixhaloguide.com/strix-halo-models/).

## What Is AMD Strix Halo?

AMD Strix Halo is the hardware family behind Ryzen AI MAX systems. The Ryzen AI
MAX+ 395 combines 16 Zen 5 CPU cores with Radeon 8060S integrated graphics
(40 RDNA 3.5 compute units) and configurations with up to 128GB of LPDDR5x
unified memory. AMD's Ryzen AI Halo developer platform uses this processor with
128GB of memory; retail systems from different OEMs can expose different BIOS,
power, cooling and firmware behavior. See AMD's
[official Ryzen AI Halo specifications](https://www.amd.com/en/products/processors/desktops/ryzen/ryzen-ai-halo/ryzen-ai-max-plus-395.html).

Unified memory does not mean that applications should reserve all physical RAM
as fixed VRAM. Linux, the model runtime and other processes still need memory.
On the measured Vulkan/RADV path, a small fixed UMA reserve leaves memory visible
to Linux while the integrated GPU accesses a much larger GTT-backed shared pool.

## Start With One Local Chat Path

Read the [short local-chat path and acceptance checks](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/LOCAL_CHAT_START.md) before installing. It puts runtime qualification, a patched WebUI candidate, loopback binding and the matching SSH tunnel together. The revised installer and UI candidate remain unqualified for a fresh installation; do not transfer the historical LAN-reachable client result to a new local-only setup.

## Short Answer

For a normal retail AMD Strix Halo local-AI setup:

1. Use the measured Ubuntu 24.04 LTS route; select X11 only if a desktop tool needs it.
2. Set BIOS **UMA Frame Buffer Size** to **512MB** if available, or **2GB** if
   that is the vendor BIOS minimum.
3. Leave **IOMMU enabled/default** for the normal buyer path, NPU use, suspend,
   RDMA, VFIO, passthrough and clustering.
4. The recorded 128GB Beelink profile uses
   `amdgpu.gttsize=131072 ttm.pages_limit=31457280 amdgpu.cwsr_enable=0`.
   `cwsr_enable=0` disables compute wave save/restore (mid-wave compute
   preemption); it is the gfx1151 workaround
   from [ROCm/ROCm#5590](https://github.com/ROCm/ROCm/issues/5590). The
   GTT/TTM values are limits, not allocated VRAM; do not apply them as a 96GB
   preset. 192GB-class systems (for example Ryzen AI Max+ PRO 495) are not
   qualified; do not reuse the 128GB values there.
   Preserve unrelated boot parameters and verify live values after reboot.
5. Use Mesa/RADV and verify the selected ICD. Record a power policy per campaign;
   `tuned accelerator-performance` is one historical reproduction profile,
   not a requirement for every routine check.
6. Start with Ollama on Vulkan/RADV. Move to direct `llama.cpp` for controlled
   benchmarks and to the documented ROCm or server routes only when the
   workload requires them.

**192GB-class and PRO 495 systems (checked 2026-09-30).** `setup.sh` stops above
about 136GiB of visible RAM, and no 192GB-class profile is qualified here. Vendors
advertise up to 160GB of dedicated VRAM through the BIOS for their 192GB systems
(for example the
[HP ZBook Ultra G3a page](https://www.hp.com/us-en/workstations/mobile-workstation-pc/zbook-ultra-g3.html)
and the [Minisforum MS-S1 MAX page](https://minisforumpc.eu/products/minisforum-ms-s1-max-p495));
this guide's route uses a small fixed UMA reserve plus GTT. Neither approach has
been tested on 192GB here. On Linux the NPU of the Ryzen AI Max+ PRO 495 is
expected only with kernel 7.4 unless a patch is backported (Phoronix,
2026-09-30: the XDNA driver patch targets 7.4, with its merge window in late
October and a stable kernel around the end of 2026; a backport is possible but
uncertain). No 495 system has been tested here.

Do not treat `amd_iommu=off` as a universal recommendation. It is an optional
always-on desktop benchmark profile used by some measured first-party runs; it
disables NPU access and can break mobile suspend.

**IOMMU notes (checked 2026-09-30).** Phoronix (2026-09-29) tested AMD's PerfOpt,
an IOMMU bypass for iGPU memory access that is on by default in Linux 7.4 and can
be turned off with `amdgpu.iommu_perfopt=0`. On a Framework Desktop (Ryzen AI
MAX+ 395, 64GB) with Lemonade it measured 2 to 4%; the 18 to 23% in its headline
applies to smaller iGPUs and should not be carried over to Strix Halo. The patch
was queued but not yet merged. Whether PerfOpt removes the roughly 6% memory-read
gain recorded here for `amd_iommu=off` in one desktop test is not measured.
Separately, `amd_iommu=off` also turns off the IOMMU that the kernel's USB4 and
Thunderbolt documentation names as the protection against DMA by connected
devices ([kernel docs](https://docs.kernel.org/admin-guide/thunderbolt.html)).

**Kernel (checked 2026-09-30).** Ubuntu's 7.0.0-28 HWE kernel (the updates kernel
from 2026-07-16 to 2026-08-17) carries an amdgpu memory-management regression from
upstream 7.0.12 that was fixed in 7.0.13; Ubuntu has the fix from 7.0.0-29
([Launchpad #2158267](https://launchpad.net/bugs/2158267) reports a roughly 42x
ComfyUI SDXL slowdown; 7.0.0-34 was in noble-updates on 2026-09-22). The reporter
of [ROCm#6508](https://github.com/ROCm/ROCm/issues/6508) (open) attributes a KFD
hang on 7.0.0-28 to that kernel and saw none on 7.0.0-34. Use the current HWE
kernel. Any ROCm/HIP result in this guide that was measured on 7.0.0-28 may be
affected; the effect on those numbers is unknown.

## Which Configuration Should I Use?

| Your use case | UMA setting | IOMMU policy | Starting runtime |
|---|---|---|---|
| Normal local-AI buyer path | 512MB if available, otherwise the vendor minimum such as 2GB | Enabled/default | Ollama with Vulkan/RADV |
| Laptop, suspend or NPU use | Vendor-supported minimum | Enabled/default | Ollama or the documented NPU route |
| RDMA, VFIO, passthrough or clustering | Vendor-supported minimum | Enabled, with `iommu=pt` only when the workflow needs pass-through behavior | The documented workload-specific route |
| Strict reproduction of the measured always-on desktop benchmark profile | 512MB on the primary Beelink system | Optional `amd_iommu=off`, with the NPU and suspend caveats understood | Direct `llama.cpp` with Vulkan/RADV |

## Why The UMA Setting Is Small

The fixed UMA frame buffer is not the total memory available to the integrated
GPU on the measured Linux path. Vulkan/RADV can use GPU-accessible unified
system memory through GTT. On the primary 128GB Beelink system, using the small
fixed UMA reserve left almost the full memory pool visible to Linux while the
iGPU could still access the large GTT-backed pool.

Some vendor BIOSes expose 2GB rather than 512MB as the minimum. Use the lowest
supported vendor setting that still exposes the expected shared-memory pool;
do not assume every OEM uses the same label or range.

## Install The Working Buyer Path

After configuring BIOS and installing Ubuntu 24.04 LTS:

```bash
git clone https://github.com/hogeheer499-commits/strix-halo-guide
cd strix-halo-guide
less setup.sh
bash setup.sh
```

This clones the unpinned `main` branch, which has not been fresh-install
qualified on hardware. For a reproducible run, review the script and pin it with
`git checkout <tag-or-commit>` before `bash setup.sh`. The script stops on
anything other than Ubuntu 24.04 unless `STRIX_HALO_ALLOW_UNQUALIFIED_OS=1` is
set, and above about 136GiB visible RAM (no 192GB-class profile is qualified). It
does not read the CPU model: any AMD system that shows 120 to 136GiB of visible
RAM passes its hardware checks, including SKUs this guide has not measured (for example a 128GB Ryzen
AI Max+ PRO 495).

If the script changes boot parameters, reboot before running the verification
benchmark. The first local-chat check is:

```bash
ollama run qwen3.6:35b-a3b
```

The script configures the measured Linux-side Vulkan/RADV and Ollama path. It
does not change BIOS settings or install Ubuntu. Read
[`setup.sh`](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/setup.sh)
before using it on a production system.

**Security (checked 2026-09-30; Open WebUI count 2026-10-02):** a fresh `setup.sh` run
installs Ollama 0.31.2, a version inside the range listed for CVE-2026-85180 (no fixed
release is named), and the README's Open WebUI command pins an image (0.10.2) that 47
published advisories list as affected (count of published advisories whose affected
range includes 0.10.2, Open WebUI's GitHub security advisories, checked 2026-10-02). Read
[Security status of pinned components](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/SECURITY.md#security-status-of-pinned-components)
and the [local AI security checklist](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/SECURE_LOCAL_AI.md)
before exposing anything beyond loopback.

## Choose The Backend By Workload

| Goal | Start here | Reason |
|---|---|---|
| Local chat and Open WebUI | Ollama with Vulkan/RADV | Easiest measured buyer path |
| Reproducible generation benchmark | Direct `llama.cpp` with Vulkan/RADV | Exact control over model, quant, build and command |
| Local API, batching or speculative decoding | `llama-server` | Supports the documented server and MTP experiments |
| Higher concurrency or prompt-heavy work | The measured Lemonade or ROCm/HIP profile | These routes can suit batching and prompt processing better than the single-stream default |
| vLLM, long-context or advanced ROCm work | Use only the specific documented route | Support and performance remain workload- and version-dependent |

There is no single backend that wins every Strix Halo workload. Direct
`llama-bench`, Ollama API, server, MTP/speculative, concurrency and community
results are separate claim types in this project.

**Open WebUI (checked 2026-10-02):** 47 published advisories include the pinned
0.10.2 image. The batch of 19 published on 2026-09-27 and 2026-09-28 (13 of them
include 0.10.2) lists 0.11.4 as the patched version, and one of them (GHSA-vpq8-f445-hcq7)
applies while community sharing is enabled, which is the default. The digest-pinned 0.10.2 image is the only Open WebUI
version this guide has qualified; a patched release is not qualified here.
See [Open WebUI in SECURITY.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/SECURITY.md#open-webui).

## Frequently Asked Setup Questions

### What BIOS UMA setting should I use on Strix Halo?

Use 512MB when the BIOS offers it, or the lowest vendor-supported setting such
as 2GB. Then verify that Linux still sees the expected system-memory pool. A
large fixed UMA reservation is not required for the measured Vulkan/RADV path.

### Should I disable IOMMU on Strix Halo?

Not for the normal buyer setup. Leave IOMMU enabled or at the firmware default
for NPU use, suspend, RDMA, VFIO, passthrough and clustering. `amd_iommu=off` is
only an optional reproduction profile for an always-on desktop benchmark box.

### Which Linux distribution should I use for a Strix Halo local LLM?

This guide's measured beginner runtime uses Ubuntu 24.04 LTS and Mesa/RADV;
X11 is conditional on desktop-tool needs. The revised script's configuration
checks do not replace fresh-install/upgrade hardware qualification. Other distributions can work, but they
are not automatic substitutes for this exact measured path; compare their
kernel, Mesa, Vulkan ICD and runtime versions against the evidence.
**Ubuntu 26.04 is not qualified** by this guide (checked 2026-09-25; the
26.04.1 point release shipped 2026-08-27). Community 26.04 reports stay
separate from first-party results.

## What This Setup Does Not Guarantee

- It does not guarantee identical performance across Beelink, Framework,
  Corsair, GMKtec, Minisforum, Nimo or other Strix Halo systems.
- It does not turn a low-bit capacity pass into a model-quality recommendation.
- It does not make experimental ROCm, MTP, vLLM or NPU paths beginner defaults.
- It is not official AMD or OEM documentation or endorsement.

For cross-OEM differences, use the
[system evidence matrix](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/SYSTEM_EVIDENCE_MATRIX.md).

## Evidence And Source Of Truth

- [Complete guide and setup script](https://github.com/hogeheer499-commits/strix-halo-guide)
- [Concise canonical setup with detailed caveats](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/STRIX_HALO_LOCAL_LLM_SETUP.md)
- [Workload-specific best-known profiles](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BEST_KNOWN_PROFILES.md)
- [Retail buyer-path validation](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BUYER_PATH_VALIDATION.md)
- [Cross-OEM system evidence matrix](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/SYSTEM_EVIDENCE_MATRIX.md)
- [Structured headline claim index](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv)
- [Raw evidence](https://github.com/hogeheer499-commits/strix-halo-guide/tree/main/data/raw)

If a number appears in a post or AI answer but not in the linked structured data
or raw evidence, treat it as unverified.
