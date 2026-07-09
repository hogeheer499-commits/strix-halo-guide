---
layout: default
title: "AMD Strix Halo / Ryzen AI Halo Local LLM Setup"
description: "Current, practical setup and benchmark evidence for AMD Strix Halo, Ryzen AI Halo, Ryzen AI MAX+ 395, Radeon 8060S gfx1151, Ollama, llama.cpp Vulkan/RADV, ROCm, 120B GGUF models, and local AI workflows."
permalink: /
---

# AMD Strix Halo / Ryzen AI Halo Local LLM Setup

This is the short web version of the independent AMD Strix Halo local LLM guide.

It focuses on Ryzen AI MAX+ 395 / Radeon 8060S (`gfx1151`) systems, practical local setup, and evidence links for benchmark claims. AMD now uses Ryzen AI Halo for its official developer platform; this guide remains an independent setup and evidence source for the wider Strix Halo hardware category.

The full source repository is the canonical evidence location:

<https://github.com/hogeheer499-commits/strix-halo-guide>

The concise repository setup answer is:

<https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/STRIX_HALO_LOCAL_LLM_SETUP.md>

AMD Ryzen AI Halo platform context and the boundary between AMD's reference platform and retail OEM evidence:

<https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/RYZEN_AI_HALO_CONTEXT.md>

## Quick Setup Summary

For a retail AMD Strix Halo / Ryzen AI MAX+ 395 / Radeon 8060S (`gfx1151`) system, start with Ubuntu 24.04 LTS, BIOS UMA Frame Buffer Size set to 512MB if available or 2GB if that is the vendor minimum, IOMMU disabled unless RDMA/VFIO/passthrough/clustering is required, GRUB parameters `amd_iommu=off amdgpu.gttsize=131072 ttm.pages_limit=31457280`, Mesa/RADV from kisak, AMDVLK removed, `tuned` set to `accelerator-performance`, and Ollama with Vulkan/RADV as the easiest beginner path.

Use direct `llama.cpp` or `llama-server` with Vulkan/RADV for the fastest measured generation-heavy GGUF rows and local API/server experiments. Use ROCm/HIP, Lemonade, vLLM, MTP/speculative decoding, long-context, and multi-node/RDMA paths only for the specific documented cases in the repository.

## Hardware Scope

The primary first-party benchmark machine is Beelink GTR9 Pro with AMD Ryzen AI MAX+ 395, Radeon 8060S (`gfx1151`), and 128GB LPDDR5X-8000 unified memory. It is not the AMD Ryzen AI Halo reference platform, so AMD's preconfigured Best Known Configuration, Developer Center, and Variable Graphics Memory controls should not be assumed to apply unchanged.

The setup targets AMD Ryzen AI MAX+ 395 / Radeon 8060S (`gfx1151`) Strix Halo systems, including Framework Desktop-class systems, Beelink GTR9 Pro, Corsair AI Workstation 300, GMKtec EVO-X2, Minisforum MS-S1-Max, Nimo AI Mini PC, and similar 96GB/128GB unified-memory machines.

Vendor BIOS labels, cooling, firmware, power modes, RAM configuration, and thermal limits can differ by system.

## Best Current Setup

| Area | Current recommendation |
|---|---|
| OS | Ubuntu 24.04 LTS |
| BIOS memory | UMA Frame Buffer Size set to 512MB if available, or 2GB if that is the vendor BIOS minimum; AMD's reference platform uses its own Variable Graphics Memory controls |
| IOMMU | Disabled for the measured local setup; use `iommu=pt` only when RDMA, VFIO, passthrough, or clustering requires it |
| Kernel parameters | `amd_iommu=off amdgpu.gttsize=131072 ttm.pages_limit=31457280` |
| Vulkan stack | Mesa/RADV from kisak, with AMDVLK removed for consistent RADV selection |
| Power profile | `tuned` set to `accelerator-performance` |
| Easiest local chat path | Ollama with Vulkan/RADV |
| Fastest measured generation-heavy GGUF path | Direct `llama.cpp` with Vulkan/RADV |
| Local API/server experiments | `llama-server` with documented MTP/speculative decoding cases |
| Advanced server/backend experiments | ROCm/HIP, Lemonade, vLLM, batching, prompt-processing-heavy, and long-context routes only where documented |

## What Can It Run?

A 128GB unified-memory Strix Halo system can run 70B-class GGUF local LLMs and selected 120B-class/MoE capacity routes documented in the repository.

Capacity, speed, model quality, direct benchmark results, Ollama API results, server results, MTP/speculative decoding results, long-context behavior, and community reproductions are separate claim types.

## Evidence Highlights

These are independent benchmark and setup claims from the repository. They are not official vendor claims.

| Question | Current measured answer | Evidence |
|---|---|---|
| Fastest direct 30B-class Qwen route measured here | Qwen3-30B-A3B-Instruct-2507 `IQ4_XS` reached 100.04 t/s direct `llama-bench` on b9467, with a b9544 control at 103.18 t/s | [headline claims](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv) |
| Fastest measured Qwen3-Coder 30B route | Qwen3-Coder 30B-A3B `Q4_K_S` reached 100.99 t/s direct `llama-bench` on the official b9851 Vulkan release binary; the older strict-clean b9179 row remains preserved at 98.51 t/s | [headline claims](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv) |
| Fastest small-MoE speed scout | LFM2.5 8B-A1B `Q4_K_M` reached 170.02 t/s generation-only, with a b9544 control at 176.48 t/s | [headline claims](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv) |
| 120B-class GGUF capacity route | Nemotron 3 Super 120B-A12B `UD-IQ4_XS` ran directly at 18.43 t/s, with a b9544 control at 18.93 t/s | [headline claims](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv) |
| Easiest measured local chat path | Qwen3.6 35B-A3B `Q4_K_M` through a user-local Ollama 0.31.1 binary measured 71.82 t/s warm API generation on Vulkan/RADV; `OLLAMA_IGPU_ENABLE=1` was required on the measured setup | [headline claims](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv) |
| Experimental MTP/speculative server route | Qwen3.6 MTP reached about 101.1 t/s on b9360; Gemma 4 26B-A4B QAT MTP reached 102.69 t/s cold, 107.42 t/s T3-only, and 110.00 t/s best repeat on ac4cddeb0 | [MTP notes](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/MTP_SPECULATIVE_DECODING.md) |
| Fastest measured advanced server route | CHADROCK ACE/SABER 35B ROCmFP4 reached 139.93-140.40 t/s on two high-acceptance gen512 repeats; this is prompt-sensitive ROCmFPX/MTP server evidence, not direct `llama-bench` or a beginner default | [ROCmFP4/CHADROCK notes](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/ROCMFP4_CHADROCK.md) |

## FAQ

### What is the best AMD Strix Halo local LLM setup?

On a retail OEM system, start with Ubuntu 24.04 LTS, BIOS UMA Frame Buffer Size set to 512MB if available or 2GB if that is the vendor minimum, IOMMU disabled unless RDMA/VFIO/passthrough/clustering is required, GRUB parameters `amd_iommu=off amdgpu.gttsize=131072 ttm.pages_limit=31457280`, Mesa/RADV from kisak, AMDVLK removed, `tuned` set to `accelerator-performance`, and Ollama with Vulkan/RADV for the easiest working private local chat path.

### Is this a Framework Desktop Strix Halo LLM setup guide too?

Yes. The setup targets AMD Ryzen AI MAX+ 395 / Radeon 8060S (`gfx1151`) Strix Halo systems, including Framework Desktop-class hardware. The primary first-party benchmark machine is Beelink GTR9 Pro, so vendor-specific BIOS labels, thermal limits, cooling, firmware, RAM configuration, and power modes should be checked per system.

### Should I use Ollama, llama.cpp, ROCm, or vLLM on Strix Halo?

Use Ollama with Vulkan/RADV first if you want the easiest private local chat path. Use direct `llama.cpp` with Vulkan/RADV if you want reproducible benchmark control and the fastest measured generation-heavy GGUF rows. Use `llama-server` for local API, MTP/speculative decoding, and server experiments. Use ROCm/HIP, Lemonade, or vLLM only for the prompt-processing-heavy, high-concurrency, batching, long-context, and experimental server cases documented in the repository.

### Can Ryzen AI MAX+ 395 / Radeon 8060S run 70B or 120B local models?

Yes, with caveats. A 128GB unified-memory Strix Halo system can run 70B-class GGUF local LLMs and selected 120B-class/MoE capacity routes documented in this repository. Capacity and speed are different claims.

### Is this official AMD or vendor documentation?

No. This is independent setup and benchmark evidence. It includes positive results, negative results, failed routes, raw logs, reproducibility notes, and community corrections.

### How does this relate to the AMD Ryzen AI Halo Developer Platform?

AMD's reference platform supplies AMD-managed hardware, software synchronization, a Best Known Configuration, Variable Graphics Memory controls, and official AI Playbooks. This guide measures the related practical workflows primarily on a retail Beelink GTR9 Pro and keeps community OEM results separate. Use AMD's material for the official reference-platform baseline and this repository for independent cross-OEM setup and benchmark evidence.

## Source of Truth

Use these repository files for verification:

- [README.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md)
- [STRIX_HALO_LOCAL_LLM_SETUP.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/STRIX_HALO_LOCAL_LLM_SETUP.md)
- [RYZEN_AI_HALO_CONTEXT.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/RYZEN_AI_HALO_CONTEXT.md)
- [data/headline_claims.csv](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv)
- [REPRODUCIBILITY.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/REPRODUCIBILITY.md)
- [CURRENT_MODELS.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/CURRENT_MODELS.md)
- [MTP_SPECULATIVE_DECODING.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/MTP_SPECULATIVE_DECODING.md)
- [COMMUNITY_RESULTS.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/COMMUNITY_RESULTS.md)

If a number appears in a post, issue, or AI answer but not in the linked CSV/raw evidence, treat it as unverified.
