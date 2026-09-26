---
layout: default
title: "AMD Strix Halo Models: Measured Results, New GGUFs, and 128GB Fit"
description: "Evidence-backed AMD Strix Halo model hub separating guide-measured local LLM routes from published 2026 model artifacts and published 128GB GGUF fit tiers."
permalink: /strix-halo-models/
canonical_url: "https://strixhaloguide.com/strix-halo-models/"
sitemap: false
date: "2026-08-30T00:00:00+02:00"
last_modified_at: "2026-09-19T00:00:00+02:00"
image:
  path: "https://hogeheer499-commits.github.io/strix-halo-guide/assets/social-preview.png"
  height: 640
  width: 1280
  alt: "AMD Strix Halo model hub with measured evidence and published GGUF fit tiers"
seo:
  type: "TechArticle"
  date_modified: "2026-09-19T00:00:00+02:00"
---

# AMD Strix Halo Model Hub

**September 19 functional update:** the [scoped runtime qualification](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/RUNTIME_QUALIFICATION_2026-09-19.md)
records text (Qwen3.6), image (Qwen2.5-VL), executed tools (Devstral) and pinned
Open WebUI on the existing 0.32.15 service after restart. Isolated 0.34.2 is
useful but not default; official Qwen3.8 and full-reboot candidate acceptance
remain open. The tested host's Ollama listener was LAN-reachable, not local-only.
Released llama.cpp v0.4.1 passed bounded direct/server/HIP controls; this does
not qualify every model, long-context shape or maximum-memory allocation.

**Evidence reviewed:** September 26, 2026.

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
| Qwen3.8 27B, Ollama API/Vulkan with Ollama-default MTP drafting (`draft_num_predict 4`; not a no-draft result; requires Ollama 0.32.12+) | `Q4_K_M` | 292.49 prompt t/s; 20.42 generation t/s; exact retrieval through 50,059 prompt tokens | — | [2026-08-15 raw route](https://github.com/hogeheer499-commits/strix-halo-guide/tree/main/data/raw/2026-08-15/qwen38-27b-ollama-03213-vulkan-radv) |
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

**Newer coding candidates (not measured here; checked 2026-09-25):** the
measured Qwen3-Coder 30B-A3B rows above are speed evidence for that exact model,
not a claim that it is the newest or best coding model. Newer 30B-class
artifacts with coding relevance include Laguna XS 2.1 (`Q4_K_M` 19.56GB),
Nemotron 3.5 Lightning 30B-A3B (`Q4_0` 18.90GB) and Muse Glimmer 30B (`Q4_K_M`
16.76GB); sizes are publisher-listed, not measured here, and none has a guide
speed or quality result. They are queued for a matched coding campaign in the
[current test queue](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/current_test_queue.csv).

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
server behavior and broad quality remain unqualified. The b10687 scout predates
the Qwen4-experimental graph and Vulkan sparse-attention operations that first
shipped in llama.cpp v0.5.0 (b11146, 2026-09-23); a v0.5.0 Vulkan re-scout is
needed before any new Flash-Next speed statement. Its **qwen-community-1.0**
license differs from Apache 2.0; inspect the terms for commercial use.

## Published Artifacts And Remaining Qualification (2026-08-29 Check)

These publisher listings include model families with measured routes above.
A measured artifact does not qualify every quant, revision, context length or
feature in its family. Dates, architectures, contexts, licenses and sizes below
are from the linked primary repositories checked on 2026-08-29; they are not
new measurements on this machine.

**2026-09-25 recheck:** rows marked *(checked 2026-09-25)* were rechecked or
added on that date. In the Released column, the date type is named: a vendor
announcement, a model-card release date, or the Hugging Face repository
creation date. Paper (arXiv) dates are not used as release dates. Published
sizes are publisher-listed decimal gigabytes, not measured here.

| Model | Primary model repository | Released | Architecture | Published GGUF repository and size | License |
| --- | --- | --- | --- | --- | --- |
| Qwen3.8-Flash-Next | [Qwen/Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) | ~2026-08-26 | 125B / 6B active MoE plus 51B n-gram embeddings and 4B MTP; advertised 262K context (1M via YaRN), multimodal | [unsloth/Qwen3.8-Flash-Next-GGUF](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF): UD-Q2_K_XL 78.9GB, UD-Q3_K_XL 90GB, UD-IQ4_XS 93.7GB, UD-Q4_K_XL 111GB; smaller UD-IQ1_S 72.55GB, UD-IQ1_M 74.54GB and UD-IQ3_XXS 81.96GB also listed *(checked 2026-09-25)*; [ggml-org](https://huggingface.co/ggml-org/Qwen3.8-Flash-Next-GGUF) publishes only Q8_0 at 162.6GB | qwen-community-1.0; **not Apache 2.0**—check terms for commercial use |
| Nemotron 3.5 Lightning 30B-A3B | [nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16) | 2026-08-11 (model card) | 30B total / 3B active (card; 31.58B in GGUF metadata), Mamba-2 + MoE hybrid, up to 1M context; the card's language list does not include Dutch | [ggml-org/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF](https://huggingface.co/ggml-org/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF): Q4_0 18.90GB plus MTP Q4_0 sidecar 1.16GB; Ollama `nemotron-3.5-lightning:30b` 25.43GB *(checked 2026-09-25)* | OpenMDW-1.1 |
| Laguna XS 2.1 | [poolside/Laguna-XS-2.1](https://huggingface.co/poolside/Laguna-XS-2.1) | not recorded here | 33B total / 3B active MoE (card; 33.44B in GGUF metadata) | [ggml-org/Laguna-XS-2.1-GGUF](https://huggingface.co/ggml-org/Laguna-XS-2.1-GGUF): Q4_K_M 19.56GB; Ollama `laguna-xs-2.1` about 20GB *(checked 2026-09-25)* | OpenMDW-1.1 |
| Muse Glimmer 30B | published by the verified `meta-models` organization | not recorded here; mainline `llama.cpp` support since b10353 (#26841, 2026-08-10) | dense 29.6B including the vision encoder, multimodal; DFlash drafter published | [meta-models/Muse-Glimmer-30B-GGUF](https://huggingface.co/meta-models/Muse-Glimmer-30B-GGUF): Q4_K_M 16.76GB, mmproj 1.40GB, DFlash drafter 1.63GB *(checked 2026-09-25)* | Apache 2.0 |
| Granite 4.2 30B | [ibm-granite/granite-4.2-30b](https://huggingface.co/ibm-granite/granite-4.2-30b) | 2026-08-25 (model card) | dense 30B; Dutch is among the card's tested languages | [ibm-granite/granite-4.2-30b-GGUF](https://huggingface.co/ibm-granite/granite-4.2-30b-GGUF): Q4_K_M 17.72GB *(checked 2026-09-25)* | Apache 2.0 |
| Mistral Medium 3.5 | [mistralai/Mistral-Medium-3.5-128B](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B) | announced 2026-05-22 | dense 128B, 256K context, multimodal | [unsloth/Mistral-Medium-3.5-128B-GGUF](https://huggingface.co/unsloth/Mistral-Medium-3.5-128B-GGUF): Q4_K_M 74.9GB, UD-Q4_K_XL 75.7GB, Q5_K_M 88.3GB, Q6_K 103GB | “Modified MIT” with a large-revenue carve-out |
| Qwen3-Coder-Next | [Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) | 2026-02-03 | 80B total / 3B active MoE, 256K context | [unsloth/Qwen3-Coder-Next-GGUF](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF): Q4_K_M 48.5GB, Q6_K 65.6GB, Q8_0 84.8GB | Apache 2.0 |
| DeepSeek V4-Flash | [deepseek-ai/DeepSeek-V4-Flash-0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) | GA 2026-07-31 | 284B total / 13B active MoE, 1M context | [unsloth/DeepSeek-V4-Flash-GGUF](https://huggingface.co/unsloth/DeepSeek-V4-Flash-GGUF): UD-IQ3_XXS 103GB, UD-IQ3_S 117GB, 2-bit 90.9-96.8GB | MIT |
| DeepSeek V4-Flash-Vision-Exp | [deepseek-ai/DeepSeek-V4-Flash-Vision-Exp](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp) | 2026-08-31 (HF repository creation) | 284.33B total (GGUF metadata), vision; mainline `llama.cpp` vision support since b10762 (#28133, #28154, 2026-09-02) | [ggml-org/DeepSeek-V4-Flash-Vision-Exp-GGUF](https://huggingface.co/ggml-org/DeepSeek-V4-Flash-Vision-Exp-GGUF): Q2_K_S 98.59GB in 2 shards plus mmproj Q8_0 0.50GB; the same storage block as the queued 0731 Q2_K_S *(checked 2026-09-25)* | MIT |
| Step 3.7 Flash | [stepfun-ai/Step-3.7-Flash](https://huggingface.co/stepfun-ai/Step-3.7-Flash) | 2026-05-29 | 198B MoE, ~11B active, 256K context, vision | [stepfun-ai/Step-3.7-Flash-GGUF](https://huggingface.co/stepfun-ai/Step-3.7-Flash-GGUF): Q4_K_S 111.5GB in 3 shards; also IQ3_XXS 75.76GB, Q3_K_M 93.80GB, Q3_K_L 102.5GB, IQ4_XS 104.99GB, MTP Q8_0 3.71GB and mmproj 3.97GB *(checked 2026-09-25)* | Apache 2.0 |
| Gemma 4 31B / 26B-A4B | [google/gemma-4-31B](https://huggingface.co/google/gemma-4-31B), [google/gemma-4-26B-A4B](https://huggingface.co/google/gemma-4-26B-A4B) | 2026-04-02 ([Google announcement](https://opensource.googleblog.com/2026/03/gemma-4-expanding-the-gemmaverse-with-apache-20.html); corrected *2026-09-25*) | dense 31B / 26B-A4B MoE, 256K context, multimodal | [ggml-org/gemma-4-31B-it-GGUF](https://huggingface.co/ggml-org/gemma-4-31B-it-GGUF): Q4_0 18GB | Apache 2.0 |
| GLM-5.3-Flash | [zai-org/GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash) | 2026-08-25 (HF repository creation; corrected *2026-09-25*) | 320B total / 18B active MoE (card), natively multimodal; the card's 300K figure is an evaluation setting, not a stated context limit. **No mainline `llama.cpp` support as of 2026-09-25:** PRs [#27752](https://github.com/ggml-org/llama.cpp/pull/27752) (draft), [#27754](https://github.com/ggml-org/llama.cpp/pull/27754) and [#27773](https://github.com/ggml-org/llama.cpp/pull/27773) were open | [unsloth/GLM-5.3-Flash-GGUF](https://huggingface.co/unsloth/GLM-5.3-Flash-GGUF) (requires Unsloth's unmerged PR): UD-IQ1_S 93.09GB, UD-IQ1_M 97.58GB, UD-IQ2_XXS 101.84GB, UD-Q2_K_XL 108.72GB, plus mmproj about 1.1GB *(checked 2026-09-25)* | MIT |

### Important Compatibility And Lineage Notes

- [Step 3.7 Flash's own documentation](https://huggingface.co/stepfun-ai/Step-3.7-Flash)
  still points to StepFun's `llama.cpp` fork on branch `step3.7` and states a
  120GB unified-memory minimum. Mainline `llama.cpp` has, however, supported
  Step 3.7 text through the existing `step35` architecture since b9473
  (#23845, 2026-06-02), with MTP3 speculative support since b9745 (#24340);
  mainline Step 3.7 vision is not verified here, and no local mainline load has
  been run. The published 111.5GB Q4_K_S artifact is very tight on a 128GB
  machine; smaller official quants from IQ3_XXS 75.76GB upward are listed
  above as published sizes, not fit results. The measured ROCmFPX route stays
  separate fork evidence.
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
  At the 2026-09-25 check, Laguna XS 2.1, Muse Glimmer 30B and Granite 4.2 30B
  were also published in this size class. None of these four is measured here,
  so none is a recommendation. The measured Nemotron 3 Nano 30B-A3B rows remain
  dated 2026-06 evidence for that model; they do not make it the current NVIDIA
  pick.
- Qwen3.8-Flash-Next through Ollama *(checked 2026-09-25)*: the only non-MLX
  tag under 128GB is `qwen3.8-flash-next:125b-a6b-q4_K_M` at 120.06GB
  (111.8GiB). On paper that sits under the guide's 120GiB `ttm.pages_limit`
  but leaves little room for KV cache and runtime buffers, so it is tight and
  unqualified. The about-105GB tags are MLX format for Apple Silicon, not a
  Linux Vulkan or ROCm GGUF route, and the library has no `:latest` tag.
- GLM-5.3-Flash's smallest listed GGUF (UD-IQ1_S, 93.09GB) is already
  capacity-tight on 128GB, and it cannot be loaded with mainline `llama.cpp`
  until one of the open PRs above merges. This is fit guidance, not a benchmark.
- DeepSeek V4.1-Flash (HF repository created 2026-09-10; 552B backbone plus
  196B Engram) has no mainline `llama.cpp` support as of 2026-09-25 and is a
  multi-node or external-storage watchlist item. The open
  [ds4 PR #1036](https://github.com/antirez/ds4/pull/1036) is an external
  report from two Strix Halo systems linked over the network; its numbers are
  not guide evidence and are not one-box results.

## 64GB Published-Size Tier

The guide has not measured a 64GB system. These are artifact-size estimates
from publisher listings checked on 2026-09-25, not fit results: how much of a
64GB machine the GPU can address depends on firmware and driver settings, and
KV cache, projectors, drafters and the operating system still need room.

| Published file size | Examples (weights only unless noted) |
| --- | --- |
| Under about 20GB | [Qwen3.8 27B](https://huggingface.co/ggml-org/Qwen3.8-27B-GGUF) Q4_K_M 18.97GB; [Nemotron 3.5 Lightning](https://huggingface.co/ggml-org/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF) Q4_0 18.90GB; [Laguna XS 2.1](https://huggingface.co/ggml-org/Laguna-XS-2.1-GGUF) Q4_K_M 19.56GB; [Granite 4.2 30B](https://huggingface.co/ibm-granite/granite-4.2-30b-GGUF) Q4_K_M 17.72GB; [Muse Glimmer 30B](https://huggingface.co/meta-models/Muse-Glimmer-30B-GGUF) Q4_K_M 16.76GB plus 1.40GB mmproj |
| About 40-50GB | [Qwen3-Coder-Next](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF) Q4_K_M 48.5GB (2026-08-29 listing); leaves much less headroom on 64GB once context is added |

## 128GB Fit Tiers

These are published artifact-size tiers from the 2026-08-29 check, not local
memory-use measurements. Runtime buffers, KV cache, the operating system, and
other workloads still need room; a file fitting on paper is not a usability or
correctness result.

| Tier | Published-size examples |
| --- | --- |
| Comfortable: under 70GB | [gpt-oss-120b GGUF](https://huggingface.co/ggml-org/gpt-oss-120b-GGUF) at about 63GB; [Qwen3-Coder-Next](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF) Q6 at about 66GB; and the measured 35B-and-smaller routes listed above |
| Workable: 70-100GB | [Mistral Medium 3.5](https://huggingface.co/unsloth/Mistral-Medium-3.5-128B-GGUF) Q4/Q5; [Nemotron 3 Super](https://huggingface.co/unsloth/NVIDIA-Nemotron-3-Super-120B-A12B-GGUF) Q4/Q5; [Qwen3.8-Flash-Next](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF) through IQ4_XS at about 94GB; [Step 3.7 Flash](https://huggingface.co/stepfun-ai/Step-3.7-Flash-GGUF) IQ3_XXS 75.76GB and Q3_K_M 93.80GB; [DeepSeek V4-Flash-Vision-Exp](https://huggingface.co/ggml-org/DeepSeek-V4-Flash-Vision-Exp-GGUF) Q2_K_S 98.59GB (2026-09-25 listings) |
| Tight: over 100GB | [DeepSeek V4-Flash](https://huggingface.co/unsloth/DeepSeek-V4-Flash-GGUF) IQ3_XXS at 103GB; [Step 3.7 Flash](https://huggingface.co/stepfun-ai/Step-3.7-Flash-GGUF) Q4_K_S at 111.5GB; [Qwen3.8-Flash-Next](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF) Q4_K_XL at 111GB; Ollama `qwen3.8-flash-next:125b-a6b-q4_K_M` at 120.06GB (2026-09-25 listing) |

## What We Want Measured Next

The live [current test queue](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/current_test_queue.csv)
records model, backend, artifact, status, workload, and the buyer question each
test should answer. A model in that queue or in the publisher table above does
not become a recommendation until a dated row links to raw evidence and keeps
direct, API/server, speculative, capacity, and community results separate.

## Independence And Affiliate Disclosure

This guide contains no affiliate links as of September 19, 2026. Future affiliate,
loaned, gifted, sponsored, or early-access relationships must be disclosed near
the relevant links or results and do not buy positive conclusions.
