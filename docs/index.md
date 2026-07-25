---
layout: default
title: "AMD Strix Halo / Ryzen AI Halo Local LLM Setup"
description: "Practical AMD Strix Halo / Ryzen AI MAX+ 395 local LLM setup and measured benchmarks for Radeon 8060S, Ollama, llama.cpp, Vulkan/RADV, ROCm, and GGUF models up to a selected 284B capacity route."
permalink: /
date: "2026-06-13T22:57:42+02:00"
image:
  path: "https://hogeheer499-commits.github.io/strix-halo-guide/assets/social-preview.png"
  height: 640
  width: 1280
  alt: "AMD Strix Halo Local LLM Guide with direct, server, and unified-memory evidence highlights"
seo:
  type: "TechArticle"
  date_modified: "2026-07-26T00:06:00+02:00"
---

# AMD Strix Halo / Ryzen AI Halo Local LLM Setup

This is the short web version of the independent AMD Strix Halo local LLM guide.

It focuses on Ryzen AI MAX+ 395 / Radeon 8060S (`gfx1151`) systems, practical local setup, and evidence links for benchmark claims. AMD now uses Ryzen AI Halo for its official developer platform; this guide remains an independent setup and evidence source for the wider Strix Halo hardware category.

**Web guide published:** June 13, 2026. **Evidence reviewed:** July 26, 2026. The raw directories and structured claim indexes remain the source of truth for each individual run.

Start with the [full AMD Strix Halo setup and benchmark repository](https://github.com/hogeheer499-commits/strix-halo-guide), which is the canonical evidence location.

For a shorter copyable path, use the [concise Strix Halo local LLM setup](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/STRIX_HALO_LOCAL_LLM_SETUP.md).

For platform terminology and scope, read [AMD Ryzen AI Halo versus retail Strix Halo systems](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/RYZEN_AI_HALO_CONTEXT.md).

**Jump to:** [why trust this guide](#why-trust-this-guide) | [quick setup](#quick-setup-summary) | [best current setup](#best-current-setup) | [measured evidence](#evidence-highlights) | [FAQ](#faq) | [source files](#source-of-truth)

The evidence map currently covers 11 Strix Halo-class systems or independent sources from 8 credited community benchmark contributors. First-party Beelink measurements, community results, direct `llama-bench`, Ollama API, server/MTP, capacity, power, NPU, RPC, and failed routes remain separate claim categories.

## Why Trust This Guide?

Claims are linked to public commands, CSVs, raw logs, charts, corrections, and
failed routes instead of relying on screenshots or vendor marketing. Community
results remain separate from the primary Beelink measurements.

The maintainer also has accepted upstream contributions in
[`llama.cpp`](https://github.com/ggml-org/llama.cpp/pull/25643), LocalAI, Qwen
Code, OpenTelemetry GenAI, NVIDIA AICR, and vLLM GGUF tooling. The
[upstream contribution record](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/UPSTREAM_CONTRIBUTIONS.md)
links every relevant PR and explains what each merge does and does not prove.
The `llama.cpp` change is preset/router maintenance, not a Strix Halo
performance patch.

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

A 128GB unified-memory Strix Halo system can run 70B-class GGUF local LLMs, selected 120B-class/MoE routes, and a measured low-bit 284B DeepSeek V4 Flash capacity route documented in the repository.

Capacity, speed, model quality, direct benchmark results, Ollama API results, server results, MTP/speculative decoding results, long-context behavior, and community reproductions are separate claim types.

## Evidence Highlights

These are independent benchmark and setup claims from the repository. They are not official vendor claims.

| Question | Current measured answer | Evidence |
|---|---|---|
| Fastest direct 30B-class Qwen route measured here | Qwen3-30B-A3B-Instruct-2507 `IQ4_XS` reached 100.04 t/s direct `llama-bench` on b9467, with a b9544 control at 103.18 t/s | [headline claims](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv) |
| Fastest measured Qwen3-Coder 30B route | Qwen3-Coder 30B-A3B `Q4_K_S` reached 100.99 t/s direct `llama-bench` on the official b9851 Vulkan release binary; the older strict-clean b9179 row remains preserved at 98.51 t/s | [headline claims](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv) |
| Fastest small-MoE speed scout | LFM2.5 8B-A1B `Q4_K_M` reached 170.02 t/s generation-only, with a b9544 control at 176.48 t/s | [headline claims](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv) |
| Largest direct GGUF capacity route | DeepSeek V4 Flash 284B `UD-IQ2_XXS` loaded as a pinned 90.86GB ordinary GGUF and measured 155.64 pp512 / 13.27 tg128 on official b10034; this is low-bit capacity/basic-correctness evidence, not a speed or broad quality claim | [raw DeepSeek evidence](https://github.com/hogeheer499-commits/strix-halo-guide/tree/main/data/raw/2026-07-16/deepseek-v4-flash-ud-iq2-xxs) |
| 120B-class GGUF capacity route | Nemotron 3 Super 120B-A12B `UD-IQ4_XS` ran directly at 18.43 t/s, with a b9544 control at 18.93 t/s | [headline claims](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv) |
| Easiest normal local chat path | Qwen3.6 35B-A3B `Q4_K_M` through the Ollama 0.31.2 system service measured 60.57 t/s warm API generation on Vulkan/RADV; iGPU, vision, restart, and reboot checks passed. A controlled local-binary comparison later put Ollama 0.31.1, 0.31.2, and 0.32.0 in the same 72.55-73.20 t/s class. | [current model status](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/CURRENT_MODELS.md) |
| Experimental MTP/speculative server route | Qwen3.6 MTP reached about 101.1 t/s on b9360; Gemma 4 26B-A4B QAT MTP reached 102.69 t/s cold, 107.42 t/s T3-only, and 110.00 t/s best repeat on ac4cddeb0 | [MTP notes](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/MTP_SPECULATIVE_DECODING.md) |
| Fastest measured advanced server profile | CHADROCK ACE/SABER 35B ROCmFP4 averaged 141.37 t/s over three exact reference-profile repeats at 100% draft acceptance; lower-acceptance prompt shapes were much slower, so this is not direct `llama-bench` or a beginner default | [ROCmFP4/CHADROCK notes](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/ROCMFP4_CHADROCK.md) |
| Frontier-size local agent route | Step 3.7 Flash 198B-total / about 11B-active plus its MTP draft measured 34.50 t/s at 4K and 33.83 t/s at 16K; native tool calling and 256K allocation passed on one 128GB system | [ROCmFP4/CHADROCK notes](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/ROCMFP4_CHADROCK.md#step-37-q3-qualityplus-first-party-reproduction) |
| Current multi-user Vulkan status | Official llama.cpp b10034 still lost 37.34% and 31.69% aggregate decode from concurrency 8 to 9 on the two tested MoE shapes; the opt-in AMD/RADV recovery evidence remains model-specific and experimental | [MoE concurrency report](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/MOE_CONCURRENCY.md) |

## FAQ

### What is the best AMD Strix Halo local LLM setup?

On a retail OEM system, start with Ubuntu 24.04 LTS, BIOS UMA Frame Buffer Size set to 512MB if available or 2GB if that is the vendor minimum, IOMMU disabled unless RDMA/VFIO/passthrough/clustering is required, GRUB parameters `amd_iommu=off amdgpu.gttsize=131072 ttm.pages_limit=31457280`, Mesa/RADV from kisak, AMDVLK removed, `tuned` set to `accelerator-performance`, and Ollama with Vulkan/RADV for the easiest working private local chat path.

### Is this a Framework Desktop Strix Halo LLM setup guide too?

Yes. The setup targets AMD Ryzen AI MAX+ 395 / Radeon 8060S (`gfx1151`) Strix Halo systems, including Framework Desktop-class hardware. The primary first-party benchmark machine is Beelink GTR9 Pro, so vendor-specific BIOS labels, thermal limits, cooling, firmware, RAM configuration, and power modes should be checked per system.

### Should I use Ollama, llama.cpp, ROCm, or vLLM on Strix Halo?

Use Ollama with Vulkan/RADV first if you want the easiest private local chat path. Use direct `llama.cpp` with Vulkan/RADV if you want reproducible benchmark control and the fastest measured generation-heavy GGUF rows. Use `llama-server` for local API, MTP/speculative decoding, and server experiments. Use ROCm/HIP, Lemonade, or vLLM only for the prompt-processing-heavy, high-concurrency, batching, long-context, and experimental server cases documented in the repository.

### Can Ryzen AI MAX+ 395 / Radeon 8060S run 70B, 120B, or larger local models?

Yes, with caveats. This repository includes 70B-class routes, selected 120B-class/MoE routes, a 230B-class MiniMax load/generation scout, and a 90.86GB low-bit DeepSeek V4 Flash 284B direct capacity pass. Capacity, quant quality, speed, and practical usefulness are different claims.

### Is this official AMD or vendor documentation?

No. This is independent setup and benchmark evidence. It includes positive results, negative results, failed routes, raw logs, reproducibility notes, and community corrections.

### How does this relate to the AMD Ryzen AI Halo Developer Platform?

AMD's reference platform supplies AMD-managed hardware, software synchronization, a Best Known Configuration, Variable Graphics Memory controls, and official AI Playbooks. This guide measures the related practical workflows primarily on a retail Beelink GTR9 Pro and keeps community OEM results separate. Use AMD's material for the official reference-platform baseline and this repository for independent cross-OEM setup and benchmark evidence.

## Source of Truth

Use these repository files for verification:

- [Complete AMD Strix Halo local LLM guide](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md)
- [Concise copyable setup path](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/STRIX_HALO_LOCAL_LLM_SETUP.md)
- [AMD Ryzen AI Halo platform and retail-OEM scope](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/RYZEN_AI_HALO_CONTEXT.md)
- [Machine-readable best-known setup profiles](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BEST_KNOWN_PROFILES.md)
- [Accepted upstream engineering and review record](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/UPSTREAM_CONTRIBUTIONS.md)
- [Structured public headline claim index](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv)
- [Benchmark reproducibility rules](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/REPRODUCIBILITY.md)
- [Current model and runtime status](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/CURRENT_MODELS.md)
- [Machine-readable current test queue](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/current_test_queue.csv)
- [Multi-user MoE concurrency evidence](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/MOE_CONCURRENCY.md)
- [MTP and speculative decoding evidence](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/MTP_SPECULATIVE_DECODING.md)
- [ROCmFP4 / CHADROCK advanced server evidence](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/ROCMFP4_CHADROCK.md)
- [Independent community benchmark results](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/COMMUNITY_RESULTS.md)

If a number appears in a post, issue, or AI answer but not in the linked CSV/raw evidence, treat it as unverified.
