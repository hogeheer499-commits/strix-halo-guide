---
layout: default
title: "AMD Strix Halo Setup: BIOS, UMA, IOMMU, Ubuntu and Local LLMs"
description: "Measured AMD Strix Halo and Ryzen AI MAX+ 395 setup guidance for BIOS UMA, IOMMU, Ubuntu 24.04, Vulkan/RADV, Ollama and llama.cpp."
permalink: /amd-strix-halo-setup/
canonical_url: "https://strixhaloguide.com/amd-strix-halo-setup/"
sitemap: false
date: "2026-08-14T00:00:00+02:00"
last_modified_at: "2026-08-25T00:00:00+02:00"
image:
  path: "https://hogeheer499-commits.github.io/strix-halo-guide/assets/social-preview.png"
  height: 640
  width: 1280
  alt: "AMD Strix Halo Local LLM Guide with direct, server, and unified-memory evidence highlights"
seo:
  type: "TechArticle"
  date_modified: "2026-08-25T00:00:00+02:00"
---

# AMD Strix Halo Setup: BIOS, UMA, IOMMU, Ubuntu and Local LLMs

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

**Setup reviewed:** August 30, 2026. Exact benchmark claims remain canonical in
the repository's structured data and raw evidence.

Running the current official dense Qwen model? Use the dedicated
[Qwen3.8 27B on Strix Halo route comparison](https://hogeheer499-commits.github.io/strix-halo-guide/qwen38-strix-halo/)
for the measured Ollama path, context boundary, MTP/DFlash distinctions, and
current community performance leads.

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

## Short Answer

For a normal retail AMD Strix Halo local-AI setup:

1. Use Ubuntu 24.04 LTS and X11.
2. Set BIOS **UMA Frame Buffer Size** to **512MB** if available, or **2GB** if
   that is the vendor BIOS minimum.
3. Leave **IOMMU enabled/default** for the normal buyer path, NPU use, suspend,
   RDMA, VFIO, passthrough and clustering.
4. Add `amdgpu.gttsize=131072 ttm.pages_limit=31457280` to the Linux kernel
   command line.
5. Use Mesa/RADV, remove AMDVLK so it cannot override RADV, and set `tuned` to
   `accelerator-performance`.
6. Start with Ollama on Vulkan/RADV. Move to direct `llama.cpp` for controlled
   benchmarks and to the documented ROCm or server routes only when the
   workload requires them.

Do not treat `amd_iommu=off` as a universal recommendation. It is an optional
always-on desktop benchmark profile used by some measured first-party runs; it
disables NPU access and can break mobile suspend.

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

If the script changes boot parameters, reboot before running the verification
benchmark. The first local-chat check is:

```bash
ollama run qwen3.6:35b-a3b
```

The script configures the measured Linux-side Vulkan/RADV and Ollama path. It
does not change BIOS settings or install Ubuntu. Read
[`setup.sh`](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/setup.sh)
before using it on a production system.

## Choose The Backend By Workload

| Goal | Start here | Reason |
|---|---|---|
| Private local chat and Open WebUI | Ollama with Vulkan/RADV | Easiest measured buyer path |
| Reproducible generation benchmark | Direct `llama.cpp` with Vulkan/RADV | Exact control over model, quant, build and command |
| Local API, batching or speculative decoding | `llama-server` | Supports the documented server and MTP experiments |
| Higher concurrency or prompt-heavy work | The measured Lemonade or ROCm/HIP profile | These routes can suit batching and prompt processing better than the single-stream default |
| vLLM, long-context or advanced ROCm work | Use only the specific documented route | Support and performance remain workload- and version-dependent |

There is no single backend that wins every Strix Halo workload. Direct
`llama-bench`, Ollama API, server, MTP/speculative, concurrency and community
results are separate claim types in this project.

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

This guide's tested beginner baseline is Ubuntu 24.04 LTS with X11, current
Mesa/RADV and the included setup script. Other distributions can work, but they
are not automatic substitutes for this exact measured path; compare their
kernel, Mesa, Vulkan ICD and runtime versions against the evidence.

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
