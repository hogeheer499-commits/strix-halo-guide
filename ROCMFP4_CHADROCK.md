# ROCmFP4 / CHADROCK Advanced Lane

This page tracks the experimental ROCmFP4 / CHADROCK route for AMD Strix Halo / Ryzen AI MAX+ 395 systems.

It is not the default setup path. New users should start with [`setup.sh`](setup.sh), Ollama, and Vulkan/RADV as described in the [`README.md`](README.md). ROCmFP4 is an advanced route for people who want to test tuned GGUFs, MTP/speculative decoding, ROCm/HIP behavior, NPU-aware stacks, and quality/speed tradeoffs.

## What It Is

[`charlie12345/rocmfp4-llama`](https://github.com/charlie12345/rocmfp4-llama) is an experimental `llama.cpp` branch focused on AMD Strix Halo / `gfx1151`.

The branch documents:

- custom ROCmFP4 GGUF tensor formats
- Strix Halo / `gfx1151` build scripts
- ROCm/HIP and Vulkan integration work
- MTP/speculative decoding guard tests
- reproducibility notes for Strix Halo runs

Treat it as a separate runtime lane. Do not mix its results with stock upstream `llama.cpp` Vulkan/RADV direct `llama-bench` headline rows.

## Why It Matters

The guide already has a community evidence package from ciru-ai's GMKtec EVO-X2 / NixOS / IOMMU-on stack that includes ROCmFP4, Chadrock/Qwopus, Gemma QAT/MTP, CrownV7, quality metrics, and NPU sidecar data:

- [`COMMUNITY_RESULTS.md#gmktec-evo-x2-nixos--npu--rocmfp4-evidence-package`](COMMUNITY_RESULTS.md#gmktec-evo-x2-nixos--npu--rocmfp4-evidence-package)
- [`data/community_ciru_evox2_metrics.csv`](data/community_ciru_evox2_metrics.csv)
- [`ciru-ai/strix-halo-evo-x2-evidence`](https://github.com/ciru-ai/strix-halo-evo-x2-evidence)

That makes ROCmFP4 valuable for the guide because it answers different buyer and vendor questions than the default path:

- Can tuned Strix Halo GGUFs improve practical quality/speed tradeoffs?
- Can an IOMMU-on setup keep NPU workflows usable while the iGPU handles the main model?
- Which routes are promising enough to reproduce on a second system?
- Which runtime/model combinations are too experimental for beginner guidance?

## Current Public Artifacts To Watch

These are artifact scans, not first-party Beelink benchmark claims.

| Artifact | Size observed | Why it is interesting |
| --- | ---: | --- |
| [`jcbtc/qwopus3.6-27b-v2-chadrock-rocmfp4-mtp`](https://huggingface.co/jcbtc/qwopus3.6-27b-v2-chadrock-rocmfp4-mtp) | 13.8 GiB | Practical 27B tuned ROCmFP4/MTP candidate with existing ciru quality context. |
| [`jcbtc/chadrock3.6-27b-pi-agent-rocmfp4-mtp`](https://huggingface.co/jcbtc/chadrock3.6-27b-pi-agent-rocmfp4-mtp) | 13.8 GiB | Small enough for a clean local smoke/repro attempt; useful for agent-profile testing. |
| [`jcbtc/chadrock-35b-ace-saber-rocmfp4-mtp`](https://huggingface.co/jcbtc/chadrock-35b-ace-saber-rocmfp4-mtp) | 17.7 GiB | 35B-class tuned ROCmFP4/MTP route; useful because ciru's evidence includes quality-plus-speed signals. |
| [`jcbtc/CHADROCK3.6-35B-UNCENSORED-MTP-STRIX-LEAN`](https://huggingface.co/jcbtc/CHADROCK3.6-35B-UNCENSORED-MTP-STRIX-LEAN) | 17.7 GiB | Earlier 35B STRIX_LEAN candidate; useful for format/runtime checks. |
| [`jcbtc/qwen3.6-35b-a3b-crown-halo-mtp-dynamic`](https://huggingface.co/jcbtc/qwen3.6-35b-a3b-crown-halo-mtp-dynamic) | 21.0 GiB | CrownV7-style dynamic route; useful for tool/function-calling and long-context behavior if reproduced cleanly. |

## First Repro Plan

The first local Beelink test should be a smoke/repro route, not a broad benchmark campaign.

Record:

- `rocmfp4-llama` commit
- exact model repository, filename, size, and hash
- ROCm, kernel, Mesa, and firmware context
- exact command
- no-spec baseline when possible
- MTP/speculative route when possible
- acceptance rate or available speculative metrics
- short decode and sustained decode separately
- whether the route loads cleanly without breaking the default Vulkan/RADV setup

The first useful result can be negative. A clean "does not build", "loads but crashes", "runs but slower than Vulkan", or "needs IOMMU-on/ROCm tuning" result still removes setup friction.

## How To Use This In The Guide

Use ROCmFP4 / CHADROCK as:

- an advanced Strix Halo runtime lane
- community tuned-route evidence
- a possible bridge between raw benchmark rows and "best known settings per model"
- a source of vendor/reviewer questions about ROCm, NPU, IOMMU, and tuned GGUF support

Do not use it as:

- the beginner setup path
- a replacement for direct `llama-bench` Vulkan/RADV headline claims
- official AMD, OEM, or upstream `llama.cpp` performance evidence
- a universal recommendation before local reproduction

## Status

Status as of 2026-06-21: promising and test-worthy, but not yet first-party reproduced on the guide's Beelink GTR9 Pro.
