---
layout: default
title: "AMD Strix Halo Models: Measured Results, New GGUFs, and 128GB Fit"
description: "Evidence-backed AMD Strix Halo model hub separating guide-measured local LLM routes from published 2026 model artifacts and published 128GB GGUF fit tiers."
permalink: /strix-halo-models/
date: "2026-08-30T00:00:00+02:00"
last_modified_at: "2026-09-05T00:00:00+02:00"
image:
  path: "https://hogeheer499-commits.github.io/strix-halo-guide/assets/social-preview.png"
  height: 640
  width: 1280
  alt: "AMD Strix Halo model hub with measured evidence and published GGUF fit tiers"
seo:
  type: "TechArticle"
  date_modified: "2026-09-05T00:00:00+02:00"
---

# AMD Strix Halo Model Hub

**Evidence reviewed:** August 30, 2026.

This page keeps two claim classes separate: models measured by this guide on its
primary Strix Halo machine, and publisher-listed artifacts whose remaining
quants, features or context limits still need qualification. The canonical sources for the first section are the
[headline claim index](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv)
and [best-known profiles](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BEST_KNOWN_PROFILES.md).

## Measured On This Machine

These are first-party guide measurements. Direct `llama-bench`, Ollama API,
server/speculative, and capacity results remain different claim types. An em
dash in the artifact-size column means neither `data/headline_claims.csv` nor
`BEST_KNOWN_PROFILES.md` states a size for that row; no size is inferred.

| Model and route | Quant | Measured result | Artifact size | Measurement date and raw evidence |
| --- | --- | --- | ---: | --- |
| Qwen3.8 27B, Ollama API/Vulkan | `Q4_K_M` | 292.49 prompt t/s; 20.42 generation t/s; exact retrieval through 50,059 prompt tokens | — | [2026-08-15 raw route](https://github.com/hogeheer499-commits/strix-halo-guide/tree/main/data/raw/2026-08-15/qwen38-27b-ollama-03213-vulkan-radv) |
| Qwen3-Coder 30B-A3B, direct Vulkan speed-first | `Q4_K_S` | 100.99 tg128; 1423.05 pp512 | — | [2026-06-30 raw r50](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/raw/2026-06-30/latest-llamacpp-b9851-vulkan-sentinel/qwen3-coder-q4ks-b9851-p512-n128-r50.csv) |
| Qwen3-Coder 30B-A3B, direct Vulkan balanced | `UD-Q4_K_XL` | 96.76 tg128; 1320.52 pp512 | — | [2026-05-07 raw r20](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/raw/2026-05-07/max-performance-campaign/benchmarks/qwen3-coder-top-confirm-r20/guide.csv) |
| Qwen3-30B-A3B-Instruct-2507, direct Vulkan | `IQ4_XS` | 100.04 tg128; 1416.03 pp512; r20 was 100.58 tg128 | — | [2026-06-02 raw r50](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/qwen3-30b-2507-iq4xs-b9467-r50.csv) |
| LFM2.5 8B-A1B, direct Vulkan | `Q4_K_M` | 168.96 tg128; 3414.61 pp512; generation-only 170.02 tg128 | — | [2026-06-05 raw row](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/raw/2026-06-05/latest-llamacpp-intdot-regression/lfm25-8b-a1b-q4km-b2016bf2-r5.csv) |
| Qwen3.6 35B-A3B, direct Vulkan balanced | `UD-Q4_K_M` | 62.56 tg128; 1059.45 pp512 | — | [2026-05-07 raw r20](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/raw/2026-05-07/latest-stack-rerun/clean-b9049-rerun/qwen36-35b-b9049-clean-r20.csv) |
| Qwen3-Next 80B-A3B, direct Vulkan | `UD-Q4_K_XL` | 59.06 tg128; 751.70 pp512 | — | [2026-05-16 raw r20](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/raw/2026-05-16/latest-stack-b9172/qwen3-next-confirm-r20/qwen3-next-80b-b9172-ub1024-r20.csv) |
| gpt-oss-120b, direct Vulkan | `MXFP4 MoE` | 55.57 tg128; 726.99 pp512; 293.73 pp65536 r1 | — | [2026-05-07 raw campaign](https://github.com/hogeheer499-commits/strix-halo-guide/tree/main/data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan) |
| Nemotron 3 Super 120B-A12B, direct Vulkan capacity | `UD-IQ4_XS` | 18.43 tg128; 294.99 pp512 | — | [2026-06-05 raw row](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/raw/2026-06-05/latest-llamacpp-intdot-regression/nemotron-3-super-120b-a12b-udiq4xs-b2016bf2-r3.csv) |
| DeepSeek V4 Flash 284B, direct Vulkan capacity | `UD-IQ2_XXS` | 155.64 pp512; 13.27 tg128; correctness answer `9` | 90.86GB | [2026-07-16 raw route](https://github.com/hogeheer499-commits/strix-halo-guide/tree/main/data/raw/2026-07-16/deepseek-v4-flash-ud-iq2-xxs) |
| Gemma 4 26B-A4B IT QAT, Vulkan server/MTP | `UD-Q4_K_XL` plus `Q4_0` MTP head | 102.69 t/s cold; 107.42 t/s T3-only; 110.00 t/s best repeat; 73.96 t/s no-spec baseline | — | [2026-06-12 raw repeat](https://github.com/hogeheer499-commits/strix-halo-guide/tree/main/data/raw/2026-06-12/gemma4-26b-qat-mtp-cold-repeat-ac4cddeb) |
| Step 3.7 Flash 198B-A11B, ROCmFPX server/MTP | ROCmFPX `Q3 QualityPlus` plus `Q8_0` MTP draft | 34.50 t/s at 4K; 33.83 t/s at 16K; native tool call and 256K allocation passed | — | [2026-07-16 raw route](https://github.com/hogeheer499-commits/strix-halo-guide/tree/main/data/raw/2026-07-16/step37-rocmfpx-q3-qualityplus) |

## August 30 Direct Sentinel And Flash-Next Scout

These additional first-party rows used b10687 (`c841aee`), kernel 7.0.0-30,
Mesa/RADV 26.1.7, desktop performance, DPM auto and recorded CPU-only background
load. They do not replace strict-clean headlines or establish an A/B improvement.

| Model / quant | pp512 t/s | tg128 t/s | Repeats and scope |
| --- | ---: | ---: | --- |
| Qwen3-Coder 30B-A3B UD-Q4_K_XL | 1264.16 | 94.64 | 20; direct sentinel |
| Qwen3-Next 80B-A3B UD-Q4_K_XL | 675.76 | 62.09 | 20; direct sentinel |
| Qwen3.8-Flash-Next UD-IQ4_XS (~93.7GB) | 394.73 | 27.16 | 10; single-artifact scout |

[Read the methods and raw evidence](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BENCHMARKS.md#2026-08-30-vulkan-sentinel-and-flash-next-scout).
Flash-Next passed only a separate arithmetic smoke; vision, tools, long context,
server behavior and broad quality remain unqualified. Its **qwen-community-1.0**
license differs from Apache 2.0; inspect the terms for commercial use.

## Published Artifacts And Remaining Qualification (2026-08-29 Check)

These publisher listings include model families with measured routes above.
A measured artifact does not qualify every quant, revision, context length or
feature in its family. Dates, architectures, contexts, licenses and sizes below
are from the linked primary repositories checked on 2026-08-29; they are not
new measurements on this machine.

| Model | Primary model repository | Released | Architecture | Published GGUF repository and size | License |
| --- | --- | --- | --- | --- | --- |
| Qwen3.8-Flash-Next | [Qwen/Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) | ~2026-08-26 | 125B / 6B active MoE plus 51B n-gram embeddings and 4B MTP; advertised 262K context (1M via YaRN), multimodal | [unsloth/Qwen3.8-Flash-Next-GGUF](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF): UD-Q2_K_XL 78.9GB, UD-Q3_K_XL 90GB, UD-IQ4_XS 93.7GB, UD-Q4_K_XL 111GB | qwen-community-1.0; **not Apache 2.0**—check terms for commercial use |
| Nemotron 3.5 Lightning 30B-A3B | [nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16) | 2026-08-11 | 30B total / 3B active, Mamba-2 + MoE hybrid, up to 1M context | [ggml-org/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF](https://huggingface.co/ggml-org/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF); size not verified here | OpenMDW-1.1 |
| Mistral Medium 3.5 | [mistralai/Mistral-Medium-3.5-128B](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B) | announced 2026-05-22 | dense 128B, 256K context, multimodal | [unsloth/Mistral-Medium-3.5-128B-GGUF](https://huggingface.co/unsloth/Mistral-Medium-3.5-128B-GGUF): Q4_K_M 74.9GB, UD-Q4_K_XL 75.7GB, Q5_K_M 88.3GB, Q6_K 103GB | “Modified MIT” with a large-revenue carve-out |
| Qwen3-Coder-Next | [Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) | 2026-02-03 | 80B total / 3B active MoE, 256K context | [unsloth/Qwen3-Coder-Next-GGUF](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF): Q4_K_M 48.5GB, Q6_K 65.6GB, Q8_0 84.8GB | Apache 2.0 |
| DeepSeek V4-Flash | [deepseek-ai/DeepSeek-V4-Flash-0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) | GA 2026-07-31 | 284B total / 13B active MoE, 1M context | [unsloth/DeepSeek-V4-Flash-GGUF](https://huggingface.co/unsloth/DeepSeek-V4-Flash-GGUF): UD-IQ3_XXS 103GB, UD-IQ3_S 117GB, 2-bit 90.9-96.8GB | MIT |
| Step 3.7 Flash | [stepfun-ai/Step-3.7-Flash](https://huggingface.co/stepfun-ai/Step-3.7-Flash) | 2026-05-29 | 198B MoE, ~11B active, 256K context, vision | [stepfun-ai/Step-3.7-Flash-GGUF](https://huggingface.co/stepfun-ai/Step-3.7-Flash-GGUF): Q4_K_S 111.5GB in 3 shards | Apache 2.0 |
| Gemma 4 31B / 26B-A4B | [google/gemma-4-31B](https://huggingface.co/google/gemma-4-31B), [google/gemma-4-26B-A4B](https://huggingface.co/google/gemma-4-26B-A4B) | 2026-07-02 | dense 31B / 26B-A4B MoE, 256K context, multimodal | [ggml-org/gemma-4-31B-it-GGUF](https://huggingface.co/ggml-org/gemma-4-31B-it-GGUF): Q4_0 18GB | Apache 2.0 |
| GLM-5.3-Flash | [zai-org/GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash) | 2026-02-17 | 320B total / 18B active MoE, 300K context | [unsloth/GLM-5.3-Flash-GGUF](https://huggingface.co/unsloth/GLM-5.3-Flash-GGUF); sizes **not verified** | MIT |

### Important Compatibility And Lineage Notes

- [Step 3.7 Flash's own documentation](https://huggingface.co/stepfun-ai/Step-3.7-Flash)
  requires StepFun's `llama.cpp` fork on branch `step3.7`, not mainline, and
  states a 120GB unified-memory minimum. Its published 111.5GB Q4_K_S artifact
  is therefore very tight on a 128GB machine. This is fit guidance, not a guide
  benchmark.
- [gpt-oss-120b commit history](https://huggingface.co/openai/gpt-oss-120b/commits/main)
  showed no weight revisions after its 2025-08-26 release when checked
  2026-08-29; later changes were README, chat-template, or configuration changes.
  Claims of 2026 weight “patches” on SEO blogs are unsubstantiated here.
- [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B), released 2026-08-14
  under Apache 2.0, remained the newest Qwen dense model in its class at the
  2026-08-29 check. [Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)
  is a different 125B MoE class; Qwen's model card reports stronger coding and
  agentic results, but its qwen-community-1.0 license is more restrictive.
- Qwen3.6-35B-A3B had no same-class successor in the Qwen3.8 open lineup at the
  [2026-08-29 Qwen organization check](https://huggingface.co/Qwen). The nearest
  modern alternative identified here is
  [Nemotron 3.5 Lightning 30B-A3B](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16).

## 128GB Fit Tiers

These are published artifact-size tiers from the 2026-08-29 check, not local
memory-use measurements. Runtime buffers, KV cache, the operating system, and
other workloads still need room; a file fitting on paper is not a usability or
correctness result.

| Tier | Published-size examples |
| --- | --- |
| Comfortable: under 70GB | [gpt-oss-120b GGUF](https://huggingface.co/ggml-org/gpt-oss-120b-GGUF) at about 63GB; [Qwen3-Coder-Next](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF) Q6 at about 66GB; and the measured 35B-and-smaller routes listed above |
| Workable: 70-100GB | [Mistral Medium 3.5](https://huggingface.co/unsloth/Mistral-Medium-3.5-128B-GGUF) Q4/Q5; [Nemotron 3 Super](https://huggingface.co/unsloth/NVIDIA-Nemotron-3-Super-120B-A12B-GGUF) Q4/Q5; [Qwen3.8-Flash-Next](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF) through IQ4_XS at about 94GB |
| Tight: over 100GB | [DeepSeek V4-Flash](https://huggingface.co/unsloth/DeepSeek-V4-Flash-GGUF) IQ3_XXS at 103GB; [Step 3.7 Flash](https://huggingface.co/stepfun-ai/Step-3.7-Flash-GGUF) Q4_K_S at 111.5GB; [Qwen3.8-Flash-Next](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF) Q4_K_XL at 111GB |

## What We Want Measured Next

The live [current test queue](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/current_test_queue.csv)
records model, backend, artifact, status, workload, and the buyer question each
test should answer. A model in that queue or in the publisher table above does
not become a recommendation until a dated row links to raw evidence and keeps
direct, API/server, speculative, capacity, and community results separate.

## Independence And Affiliate Disclosure

This guide contains no affiliate links as of August 30, 2026. Future affiliate,
loaned, gifted, sponsored, or early-access relationships must be disclosed near
the relevant links or results and do not buy positive conclusions.
