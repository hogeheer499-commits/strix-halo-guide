---
layout: default
title: "AMD Strix Halo Models: Measured Results, New GGUFs, and 128GB Fit"
description: "Evidence-backed AMD Strix Halo model hub separating guide-measured local LLM routes from published 2026 model artifacts, third-party public capability scores and published 128GB GGUF fit tiers."
permalink: /strix-halo-models/
canonical_url: "https://strixhaloguide.com/strix-halo-models/"
sitemap: false
date: "2026-08-30T00:00:00+02:00"
last_modified_at: "2026-10-01T00:00:00+02:00"
image:
  path: "https://hogeheer499-commits.github.io/strix-halo-guide/assets/social-preview.png"
  height: 640
  width: 1280
  alt: "AMD Strix Halo model hub with measured evidence and published GGUF fit tiers"
seo:
  type: "TechArticle"
  date_modified: "2026-10-01T00:00:00+02:00"
---

# AMD Strix Halo Model Hub

**September 19 functional update:** the [scoped runtime qualification](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/RUNTIME_QUALIFICATION_2026-09-19.md)
records text (Qwen3.6), image (Qwen2.5-VL), executed tools (Devstral) and pinned
Open WebUI on the existing 0.32.15 service after restart. Isolated 0.34.2 is
useful but not default; official Qwen3.8 and full-reboot candidate acceptance
remain open. The tested host's Ollama listener was LAN-reachable, not local-only.
Released llama.cpp v0.4.1 passed bounded direct/server/HIP controls; this does
not qualify every model, long-context shape or maximum-memory allocation.

**Evidence reviewed:** October 1, 2026.

**Model watchlist update (public sources checked 2026-09-30; merge states re-read
2026-10-01):** adds a table of third-party public capability scores next to fit on
one box, the MiMo-V2.6 and K2 Horizon releases, the mainline status of
GLM-5.3-Flash, a checklist for fork-only quants and a section on other workloads.
Nothing in the new sections is a measurement by this guide unless a Measured
column says so; the review date above is not a new measurement date.
Related pages: [inference engines](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/ENGINES.md), [starting on Windows](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/WINDOWS_START.md)
and [laptops, homelab, clusters and extra GPUs](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/LAPTOPS_AND_HOMELAB.md).

This page keeps three claim classes separate: models measured by this guide on its
primary Strix Halo machine, publisher-listed artifacts whose remaining quants,
features or context limits still need qualification, and third-party public
capability scores, which are neither measured nor qualified here. The canonical sources for the first section are the
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

**Newer coding candidates (routine direct scout, 2026-09-26):** the measured
Qwen3-Coder 30B-A3B rows above are speed evidence for that exact model (the
`Q4_K_S` row is the fastest measured coding speed in this guide), not a quality
ranking and not a claim that the model is the newest or best coding model. Three newer 30B-class artifacts with coding relevance were run on
the official llama.cpp v0.5.0 Vulkan build (b11146) under **routine** host
conditions (nothing paused); see the 64GB tier below for the numbers. They are
direct `llama-bench` and two-prompt smoke results only, not a coding-quality
ranking or a recommendation; IBM Granite 4.2 30B and a matched Qwen3.8 27B control
remain open in the
[current test queue](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/current_test_queue.csv).

### Coding Quality: Third-Party Signals (checked 2026-09-30)

This guide measures coding speed, not coding quality. Two third-party signals
exist; neither was reproduced here.

- **Public index scores** (Artificial Analysis Intelligence Index v4.3.2, read
  2026-09-30; full precision via API): Qwen3-Coder 30B A3B about 9.6 (an estimated
  score on a deprecated entry), Qwen3.6 35B A3B 18.2 and Qwen3.8 27B at `xhigh`
  reasoning effort 33.7. See the capability table below for the caveats.
- **An external coding test on a 128GB Strix Halo-class machine** (GMKtec EVO-X3),
  [published 2026-08-14](https://www.soothill.io/blog/2026/08/14/coding-model-benchmark-strix-halo/):
  23 deployments, 230 executable tasks, 10 tasks per deployment, pass@1, thinking
  off. As published: Qwen3-Coder 30B-A3B `Q4_K_S` 5/10; Qwen3.8 27B `Q6_K` with MTP
  8/10 and `Q4_K_M` with MTP 7/10; AgentWorld 35B-A3B `Q6_K` 8/10; Qwen3.6
  35B-A3B `UD-Q6_K` with MTP 6/10; gpt-oss-120b `MXFP4` 9/10. With 10 tasks per
  deployment, differences such as 5 against 7 or 8 are a signal, not a ranking.

A local coding-quality measurement with the same harness and one quant per model
is not part of this page. Keep any such result separate from the speed rows above.

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
shipped in llama.cpp v0.5.0 (b11146, 2026-09-23). A direct re-check of the same
`UD-IQ4_XS` artifact on b11146 on 2026-09-26 measured 508.29 pp512 and 28.61 tg128
(10 repeats; same-night b10687 control 396.56 / 27.83). It is a controlled
re-check on a host that was not fully idle, not a new headline: Flash-Next ran
last and filled swap, and no correctness smoke was repeated on b11146. See
[BENCHMARKS.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BENCHMARKS.md)
and the [raw bundle](https://github.com/hogeheer499-commits/strix-halo-guide/tree/main/data/raw/2026-09-26/strict-clean-headline-b11146).
Its **qwen-community-1.0** license differs from Apache 2.0; inspect the terms for
commercial use.

## Public Capability Scores Versus Fit On One Box (third-party, checked 2026-09-30)

This table puts publicly reported capability next to what fits on a Strix Halo
box. **These are third-party scores, full precision via API, not measured locally;
quantisation loss is unknown.** A 2-bit or 4-bit local file can score lower than
the number shown, and by how much has not been measured here.

- **Artificial Analysis Intelligence Index v4.3.2** ([leaderboard](https://artificialanalysis.ai/leaderboards/models),
  read 2026-09-30; the version string is on the site's methodology page, the
  leaderboard page itself shows v4.3). The index composition changes between
  versions, so do not compare these scores with scores from another version.
  Reasoning effort differs per entry: maximum for the Claude, GLM-5.3, Kimi K3 and
  DeepSeek entries, `xhigh` for Qwen3.8 27B.
- **LMArena text leaderboard**, snapshot 2026-09-25
  ([leaderboard](https://lmarena.ai/leaderboard/text), which redirects to arena.ai).
  A different scale from the index; compare only within a column. Entries not
  recorded in the snapshot read are marked "not recorded".
- **Valid until 2026-10-21** (this guide's 21-day freshness window); treat the
  table as stale after that date until it is read again.
- **Fit is on paper:** a publisher-listed file size against 64, 128 or 192GB, as in
  the fit tiers below. It is not a measured fit and not a usability result.

| Model (weights licence) | Index v4.3.2 | LMArena text | Parameters | Smallest listed quant | Fits one box (on paper) | Mainline `llama.cpp` and Ollama | Measured here |
| --- | ---: | ---: | --- | --- | --- | --- | --- |
| Claude Opus 5.5, max effort (hosted only) | 57.6 | not recorded | not applicable | not applicable | not applicable | not applicable | no |
| Claude Opus 4.8, max effort (hosted only) | 41.8 | 1480 (`claude-opus-4-8-high`) | not applicable | not applicable | not applicable | not applicable | no |
| MiMo-V2.6-Pro (MIT) | 46.3 | 1480 | 1.024T | none recorded here | multiple boxes | not checked | no |
| GLM-5.3 (licence "other" in the HF API) | 44.8 | 1480 (`glm-5.3-max`) | 753.3B | none recorded here | multiple boxes | not checked; Ollama: `:cloud` tag only | no |
| Kimi K3 (licence "other" in the HF API) | 43.6 | 1488 (`kimi-k3-max`) | 2.780T | none recorded here | multiple boxes | not checked; Ollama: `:cloud` tag only | no |
| GLM-5.3-Flash (MIT) | 41.8 | 1474 | 321.3B | `UD-IQ1_S` 93.09GB | 128GB: tight, 1 to 2 bit; 192GB: yes; 64GB: no | PR #27773 merged 2026-09-30, after v0.5.0; Ollama: `:cloud` tag only | no |
| Qwen3.8-Flash-Next (qwen-community-1.0) | 39.8 | not recorded | 125B total, 6B active, plus n-gram embeddings | `UD-IQ1_S` 72.55GB; `UD-IQ4_XS` 93.7GB | 128GB: yes (workable tier); 64GB: no | yes; Ollama local tag `125b-a6b-q4_K_M`, 120.06GB | **yes**: `UD-IQ4_XS` 28.61 tg128 / 508.29 pp512 (b11146 re-check, 2026-09-26); 27.16 / 394.73 (b10687, 2026-08-30) |
| DeepSeek V4.1 Flash (MIT) | 39.5 | not recorded | 763.2B | Q2 about 163GB (vendor's tier table, below) | multiple boxes or SSD streaming (not checked); 192GB: vendor claim, below | none as of 2026-09-25 (not rechecked); Ollama: `:cloud` tag only | no |
| MiMo-V2.6-Flash (MIT) | 37.9 | not recorded | 310.8B total, about 15B active | community quants 77.40 to 96.74GB; ggml-org `Q2_K` 126.21GB | 128GB: community quants on paper, unqualified | convert support merged 2026-09-22 (in v0.5.0), DFlash support merged 2026-09-30; Ollama: not checked | no |
| Qwen3.8 27B, dense (Apache 2.0) | 33.7 | not recorded | 27B | `Q4_K_M` 18.97GB | 64GB: yes | yes; Ollama local tag | **yes**, via the Ollama API: 12.89 t/s without draft, 22.71 t/s with MTP (2026-09-26) |
| K2 Horizon MoVA 36B-A4B (Apache 2.0) | 25.3 | not recorded | 37.44B total, about 4B active | `Q4_K_M` 22.37GB | 64GB: yes, on paper | needs open PR #29535 (not merged when re-read 2026-10-01); Ollama: not checked | no |

Notes on the table:

- On this index Qwen3.8-Flash-Next scores 39.8 against 41.8 for Opus 4.8. Both are
  full-precision API scores; the local quantised model was not scored.
- Agentic coding differs by memory class on the same source: Artificial Analysis
  lists Terminal-Bench 4.0 at 5.6% for Qwen3.8 27B and 25.3% for
  Qwen3.8-Flash-Next (2026-09-30).
- **Ollama and cloud tags (read 2026-09-30, re-read 2026-10-01).** On ollama.com,
  `glm-5.3-flash`, `glm-5.3`, `kimi-k3` and `deepseek-v4.1-flash` each list only a
  `:cloud` tag ([example](https://ollama.com/library/glm-5.3-flash/tags)). A
  `:cloud` tag is a cloud-hosted model ([Ollama cloud documentation](https://docs.ollama.com/cloud)), so prompts leave your machine; the page for
  `glm-5.3-flash` describes it as approaching Claude Opus 4.8 on coding and agentic
  benchmarks (the publisher's own description). Ollama documents a local-only mode
  (`OLLAMA_NO_CLOUD=1`) that turns cloud models and web search off
  ([FAQ](https://github.com/ollama/ollama/blob/v0.34.4/docs/faq.mdx)); this guide
  has not tested it. Check the tag before you run `ollama run`.
  `qwen3.8-flash-next` has local tags.
- **GLM-5.3-Flash on 128GB (third party, to verify).** A
  [video review](https://www.youtube.com/watch?v=HbiNTcaUDto) (2026-09-08) reports
  that every Unsloth quant that fits (93 to 120GB) loaded on a 128GB Strix Halo
  using a branch of llama.cpp PR #27754, at 8 to 10 tok/s regardless of file size.
  With reasoning set to low only the smallest file completed all four of the
  reviewer's tests; on high 1 of 20 completed and on max 0 of 8, with the
  reasoning degenerating into a repeated word after about 20K tokens (as
  reported). The vendor blog below calls two GLM-5.3 Flash configurations slow for
  interactive coding on 192GB. Usability on 128GB is therefore to verify; this
  guide has not measured it.

### Vendor-Published 192GB Claims And Per-Tier Recommendations (checked 2026-09-30)

These are claims of a third party, published by the vendor. They were not
reproduced here, and this guide has not tested a 192GB system. The vendor blog
([What 192GB changes for local AI on the Framework Desktop](https://frame.work/nl/en/blog/what-192gb-changes-for-local-ai-on-the-framework-desktop),
2026-09-30) is published by the vendor. Treat the figures as vendor-published,
not independent.

- About 6.7% higher theoretical memory bandwidth than the 128GB machines, with the
  same CPU and GPU architecture.
- DeepSeek V4.1 Flash at Q2 runs on one 192GB machine with the main weights in
  memory and the Engram tables on disk: about 14 tok/s without speculation and 16
  to 20% faster with DSpark. This guide's own measured DeepSeek V4 Flash row (284B,
  `UD-IQ2_XXS`, 13.27 tg128 on 128GB, 2026-07-16) is a different model version and
  route.
- MiMo V2.6 Flash: about 18 tok/s at empty context and about 16 tok/s at 64K.
- GLM-5.3 Flash: two configurations described as slow for interactive coding.
- Keeping two models loaded at once is named as a use of the extra memory; the blog
  notes that switching in the middle of a long session is slow because the context
  has to be processed again.

For one 192GB box against two 128GB boxes, see
[LAPTOPS_AND_HOMELAB.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/LAPTOPS_AND_HOMELAB.md).

**The vendor's per-tier table.** The Framework Desktop product page (NL storefront,
read 2026-09-30) lists a "recommended model (as of Sept 2026)" per memory tier,
described as measured on the vendor's reference configuration; the page says the
methodology is on the vendor's blog, GitHub and YouTube. Vendor-measured, not
reproduced here:

| Memory tier | Model the vendor lists | Listed size |
| --- | --- | ---: |
| 32GB | Qwen3.8-27B `UD-Q4_K_XL` | 17.6GB |
| 64GB | Qwen3.5-122B-A10B `Q3_K_S` | 52.5GB |
| 128GB | DeepSeek V4 Flash 0731 `UD-IQ2_XXS` | 90.9GB |
| 192GB | DeepSeek V4.1 Flash Q2 | 163GB |

The 64GB entry differs from this guide's 64GB tier below, which lists 17 to 20GB
30B-class files and a 48.5GB 80B coder and has no measured 64GB system. The 128GB
entry has a similar size and the same quant name as this guide's measured DeepSeek
V4 Flash row (90.86GB).

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
| Laguna XS 2.1 | [poolside/Laguna-XS-2.1](https://huggingface.co/poolside/Laguna-XS-2.1) | 2026-06-20 (HF repository creation, checked 2026-09-30) | 33B total / 3B active MoE (card; 33.44B in GGUF metadata) | [ggml-org/Laguna-XS-2.1-GGUF](https://huggingface.co/ggml-org/Laguna-XS-2.1-GGUF): Q4_K_M 19.56GB; Ollama `laguna-xs-2.1` about 20GB *(checked 2026-09-25)* | OpenMDW-1.1 |
| Muse Glimmer 30B | published by the verified `meta-models` organization | 2026-08-09 (HF repository creation, checked 2026-09-30); mainline `llama.cpp` support since b10353 (#26841, 2026-08-10) | dense 29.6B including the vision encoder, multimodal; DFlash drafter published | [meta-models/Muse-Glimmer-30B-GGUF](https://huggingface.co/meta-models/Muse-Glimmer-30B-GGUF): Q4_K_M 16.76GB, mmproj 1.40GB, DFlash drafter 1.63GB *(checked 2026-09-25)* | Apache 2.0 |
| Granite 4.2 30B | [ibm-granite/granite-4.2-30b](https://huggingface.co/ibm-granite/granite-4.2-30b) | 2026-08-25 (model card) | dense 30B; Dutch is among the card's tested languages | [ibm-granite/granite-4.2-30b-GGUF](https://huggingface.co/ibm-granite/granite-4.2-30b-GGUF): Q4_K_M 17.72GB *(checked 2026-09-25)* | Apache 2.0 |
| Mistral Medium 3.5 | [mistralai/Mistral-Medium-3.5-128B](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B) | announced 2026-05-22 | dense 128B, 256K context, multimodal | [unsloth/Mistral-Medium-3.5-128B-GGUF](https://huggingface.co/unsloth/Mistral-Medium-3.5-128B-GGUF): Q4_K_M 74.9GB, UD-Q4_K_XL 75.7GB, Q5_K_M 88.3GB, Q6_K 103GB | “Modified MIT” with a large-revenue carve-out |
| Qwen3-Coder-Next | [Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next) | 2026-02-03 | 80B total / 3B active MoE, 256K context | [unsloth/Qwen3-Coder-Next-GGUF](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF): Q4_K_M 48.5GB, Q6_K 65.6GB, Q8_0 84.8GB | Apache 2.0 |
| DeepSeek V4-Flash | [deepseek-ai/DeepSeek-V4-Flash-0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) | GA 2026-07-31 | 284B total / 13B active MoE, 1M context | [unsloth/DeepSeek-V4-Flash-GGUF](https://huggingface.co/unsloth/DeepSeek-V4-Flash-GGUF): UD-IQ3_XXS 103GB, UD-IQ3_S 117GB, 2-bit 90.9-96.8GB | MIT |
| DeepSeek V4-Flash-Vision-Exp | [deepseek-ai/DeepSeek-V4-Flash-Vision-Exp](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp) | 2026-08-31 (HF repository creation) | 284.33B total (GGUF metadata), vision; mainline `llama.cpp` vision support since b10762 (#28133, #28154, 2026-09-02) | [ggml-org/DeepSeek-V4-Flash-Vision-Exp-GGUF](https://huggingface.co/ggml-org/DeepSeek-V4-Flash-Vision-Exp-GGUF): Q2_K_S 98.59GB in 2 shards plus mmproj Q8_0 0.50GB; the same storage block as the queued 0731 Q2_K_S *(checked 2026-09-25)* | MIT |
| Step 3.7 Flash | [stepfun-ai/Step-3.7-Flash](https://huggingface.co/stepfun-ai/Step-3.7-Flash) | 2026-05-29 | 198B MoE, ~11B active, 256K context, vision | [stepfun-ai/Step-3.7-Flash-GGUF](https://huggingface.co/stepfun-ai/Step-3.7-Flash-GGUF): Q4_K_S 111.5GB in 3 shards; also IQ3_XXS 75.76GB, Q3_K_M 93.80GB, Q3_K_L 102.5GB, IQ4_XS 104.99GB, MTP Q8_0 3.71GB and mmproj 3.97GB *(checked 2026-09-25)* | Apache 2.0 |
| Gemma 4 31B / 26B-A4B | [google/gemma-4-31B](https://huggingface.co/google/gemma-4-31B), [google/gemma-4-26B-A4B](https://huggingface.co/google/gemma-4-26B-A4B) | 2026-04-02 ([Google announcement](https://opensource.googleblog.com/2026/03/gemma-4-expanding-the-gemmaverse-with-apache-20.html); corrected *2026-09-25*) | dense 31B / 26B-A4B MoE, 256K context, multimodal | [ggml-org/gemma-4-31B-it-GGUF](https://huggingface.co/ggml-org/gemma-4-31B-it-GGUF): Q4_0 18GB | Apache 2.0 |
| GLM-5.3-Flash | [zai-org/GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash) | 2026-08-25 (HF repository creation; corrected *2026-09-25*) | 320B total / 18B active MoE (card), natively multimodal; the card's 300K figure is an evaluation setting, not a stated context limit. **No mainline `llama.cpp` support as of 2026-09-25:** PRs [#27752](https://github.com/ggml-org/llama.cpp/pull/27752), [#27754](https://github.com/ggml-org/llama.cpp/pull/27754) and [#27773](https://github.com/ggml-org/llama.cpp/pull/27773) were open. **Rechecked 2026-10-01:** #27773 was merged on 2026-09-30; #27752 and #27754 are closed without merging. The named release v0.5.0 (b11146) predates the merge; a build tagged b11295 contains it and b11275 does not, and the first build containing it was not determined | [unsloth/GLM-5.3-Flash-GGUF](https://huggingface.co/unsloth/GLM-5.3-Flash-GGUF) (its card, read 2026-10-01, still points to PR #27754, now closed, or to Unsloth Desktop; whether these quants load on a mainline build with #27773 was not tested here): UD-IQ1_S 93.09GB, UD-IQ1_M 97.58GB, UD-IQ2_XXS 101.84GB, UD-Q2_K_XL 108.72GB, plus mmproj about 1.1GB *(checked 2026-09-25)* | MIT |
| MiMo-V2.6-Flash-MOPD | [XiaomiMiMo/MiMo-V2.6-Flash-MOPD](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Flash-MOPD) | 2026-09-27 (HF repository creation) *(checked 2026-09-30)* | 310.76B total / about 15B active MoE (HF API total; card), multimodal; mainline convert support [#29257](https://github.com/ggml-org/llama.cpp/pull/29257) merged 2026-09-22 (in v0.5.0), DFlash support [#29650](https://github.com/ggml-org/llama.cpp/pull/29650) merged 2026-09-30 | [ggml-org/MiMo-V2.6-Flash-MOPD-GGUF](https://huggingface.co/ggml-org/MiMo-V2.6-Flash-MOPD-GGUF) (created 2026-09-28): Q2_K 126.21GB, MXFP4 167.37GB plus MTP, DFlash and mmproj sidecars; community quants [BPW2.0 77.40GB and BPW2.5 96.74GB](https://huggingface.co/AesSedai/MiMo-V2.6-Flash-MOPD-GGUF) and an [IQ2_XXS of 81.75GB](https://huggingface.co/fresherbz/MiMo-V2.6-Flash-MOPD-IQ2_XXS-GGUF) *(checked 2026-09-30; publisher-listed sizes, not loaded here)* | MIT |
| MiMo-V2.6-Pro-MOPD | [XiaomiMiMo/MiMo-V2.6-Pro-MOPD](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-MOPD) | 2026-09-27 (HF repository creation; RL variants 2026-09-21) *(checked 2026-09-30)* | 1.024T total MoE (HF API); multiple-box class | No single-box GGUF checked here | MIT |
| K2 Horizon MoVA 36B-A4B | [IFM/K2-Horizon-MoVA-36B-A4B](https://huggingface.co/IFM/K2-Horizon-MoVA-36B-A4B) | 2026-09-01 (HF repository creation) *(checked 2026-09-30)* | 37.44B total / about 4B active MoE (HF API; model name) | [IFM/K2-Horizon-MoVA-36B-A4B-GGUF](https://huggingface.co/IFM/K2-Horizon-MoVA-36B-A4B-GGUF): Q4_K_M 22.37GB. Requires [llama.cpp PR #29535](https://github.com/ggml-org/llama.cpp/pull/29535), open when re-read on 2026-10-01; the GGUF card says llama.cpp support is in progress | Apache 2.0 |

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
  were also published in this size class. Three of these four (Nemotron 3.5
  Lightning, Laguna XS 2.1 and Muse Glimmer 30B) have a routine direct scout
  dated 2026-09-26 on b11146, listed in the 64GB tier below: speed and load
  evidence only, with no coding-quality or Dutch-quality result. Granite 4.2 30B
  is not measured yet. None of the four is a recommendation. The measured
  Nemotron 3 Nano 30B-A3B rows remain dated 2026-06 evidence for that model; they
  do not make it the current NVIDIA pick.
- Qwen3.8-Flash-Next through Ollama *(checked 2026-09-25)*: the only non-MLX
  tag under 128GB is `qwen3.8-flash-next:125b-a6b-q4_K_M` at 120.06GB
  (111.8GiB). On paper that sits under the guide's 120GiB `ttm.pages_limit`
  but leaves little room for KV cache and runtime buffers, so it is tight and
  unqualified. The about-105GB tags are MLX format for Apple Silicon, not a
  Linux Vulkan or ROCm GGUF route, and the library has no `:latest` tag.
- GLM-5.3-Flash's smallest listed GGUF (UD-IQ1_S, 93.09GB) is already
  capacity-tight on 128GB. Mainline `llama.cpp` support (PR #27773) was merged on
  2026-09-30, after the v0.5.0 release; whether the published quants load on a
  build that contains it was not tested here. A third-party video reports that it
  loads on 128GB but is slow (see the capability table notes above). This is fit
  guidance, not a benchmark.
- DeepSeek V4.1-Flash (HF repository created 2026-09-10; 552B backbone plus
  196B Engram) had no mainline `llama.cpp` support as of 2026-09-25 (not
  rechecked). Community threads describe it as needing more than one 128GB box or
  external storage; one Framework community thread from 2026-09-23 reports SSD
  streaming on a single 128GB box (not checked here). On 2026-09-30 the vendor
  published a claim that the Q2 build runs on one 192GB machine (see the
  vendor-published claims above). The open
  [ds4 PR #1036](https://github.com/antirez/ds4/pull/1036) is an external report
  from two Strix Halo systems linked over the network; its numbers are not guide
  evidence and are not one-box results.
- MiMo-V2.6-Flash class (checked 2026-09-30): this guide's own community rows
  already include a MiMo-V2.5 310B-A15B `UD-IQ2_M` (96.55GB) that loaded on one
  128GB box, as a prompt-processing capacity row only (`n_gen=0`, not a
  generation-speed claim; see
  [COMMUNITY_RESULTS.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/COMMUNITY_RESULTS.md#corsair-ai-workstation-300-mimo-v25-capacity-row)).
  The MiMo-V2.6-Flash-MOPD community quants (77.40 to 96.74GB, about 2 to 2.5 bits
  per weight) are in the same size class, so "external storage or multi-node" does
  not describe them; they stay unqualified because loading, correctness and speed
  on mainline Vulkan were not tested here. Sources disagree: the vendor's 192GB
  blog counts MiMo V2.6 Flash among the models that do not fit on 128GB.
  MiMo-V2.6-Pro (1.024T) is a multiple-box model.

## Fork-Only Quants: A One-Screen Checklist (checked 2026-09-30)

Several widely downloaded Strix-specific Hugging Face repositories need a fork
or a custom runtime. Their community tabs (read 2026-09-30) show real failure
modes. This guide has not tested these repositories; the fork route it does record
is in
[ROCMFP4_CHADROCK.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/ROCMFP4_CHADROCK.md).

1. **Pin the version and the hash.** Record the exact revision of the weights and
   the version and hash of the fork or runtime.
2. **Read the community tab first.** Failure modes reported on the community tabs
   of such repositories (reports by users and makers, read 2026-09-30, not verified
   here; individual reports are not linked):
   - A fallback attention path in two versions of one quant caused loops and errors
     from about 32K context; the maker confirmed it and reported a fix in a later
     version (2026-09-16).
   - On a GTR9 Pro, the same machine model as this guide's primary system, a fork
     bug produced a GPU hang ("SDMA wedge") that needed a hard power cycle
     (2026-09-03); the maker acknowledged it and published a patch with a checksum.
   - A DeepSeek-V4-Flash quant gives garbage output in mainline `llama.cpp`, LM
     Studio and Ollama because of its custom tensor types.
   - With the default configuration one quant dropped to 5 to 7 t/s at 200K context
     through swap thrashing, according to a reporter. A reduced prompt-cache and
     batch configuration avoided it for that reporter, and the maker could not name
     the cause. The reporter later moved to v5.0.1 and closed the report; there is
     no statement that v5.0.1 fixes it.
3. **Check output at depth, not only speed.** Run the same prompt at 8K and 32K
   and read the answer. A `llama.cpp` discussion describes an earlier MTP port
   that produced fast tokens but noise above about 1K prompt tokens
   ([discussion](https://github.com/ggml-org/llama.cpp/discussions/27950)).
4. **Do not load a fork-only GGUF in mainline `llama.cpp`, Ollama or LM Studio**
   unless its card says it works there.
5. **Assume a GPU hang is possible.** Save `dmesg` before rebooting and do not run
   it on a machine with unsaved work or a service you need.
6. **Run it contained and pinned.** See the questions to ask before running a
   community engine in [ENGINES.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/ENGINES.md).

## 64GB Published-Size Tier

The guide has not measured a 64GB system. These are artifact-size estimates
from publisher listings checked on 2026-09-25, not fit results: how much of a
64GB machine the GPU can address depends on firmware and driver settings, and
KV cache, projectors, drafters and the operating system still need room.

| Published file size | Examples (weights only unless noted) |
| --- | --- |
| Under about 20GB | [Qwen3.8 27B](https://huggingface.co/ggml-org/Qwen3.8-27B-GGUF) Q4_K_M 18.97GB; [Nemotron 3.5 Lightning](https://huggingface.co/ggml-org/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF) Q4_0 18.90GB; [Laguna XS 2.1](https://huggingface.co/ggml-org/Laguna-XS-2.1-GGUF) Q4_K_M 19.56GB; [Granite 4.2 30B](https://huggingface.co/ibm-granite/granite-4.2-30b-GGUF) Q4_K_M 17.72GB; [Muse Glimmer 30B](https://huggingface.co/meta-models/Muse-Glimmer-30B-GGUF) Q4_K_M 16.76GB plus 1.40GB mmproj; [MiMo-V2.6-Distill-Qwen-9B](https://huggingface.co/ggml-org/MiMo-V2.6-Distill-Qwen-9B-GGUF) Q8_0 9.53GB (2026-09-21, MIT; 2026-09-30 listing) |
| About 20-30GB | [K2 Horizon MoVA 36B-A4B](https://huggingface.co/IFM/K2-Horizon-MoVA-36B-A4B-GGUF) Q4_K_M 22.37GB (2026-09-30 listing); requires the open llama.cpp PR #29535 |
| About 40-50GB | [Qwen3-Coder-Next](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF) Q4_K_M 48.5GB (2026-08-29 listing); leaves much less headroom on 64GB once context is added |

**Routine direct scout of three under-20GB candidates (2026-09-26):** measured
on this 128GB machine, so this is speed and load evidence, not a 64GB fit or
memory-use result. Official llama.cpp v0.5.0 Vulkan build (b11146), `-fa 1
-ngl 999`, llama-bench defaults, routine background load (VM and desktop not
paused, `balanced` power profile). Direct `llama-bench` rows only; server, MTP,
DFlash and vision were not tested. Mean t/s; ranges and a second pass are in
the [raw bundle](https://github.com/hogeheer499-commits/strix-halo-guide/tree/main/data/raw/2026-09-26/64gb-tier-30b-candidates-b11146).

| Model / quant (file size) | pp512 (r10) | tg128 (r10) | pp8192 (r3) | tg128 at depth 8192 (r3) | Smoke (arithmetic and `is_prime`, 2 greedy runs each) |
| --- | ---: | ---: | ---: | ---: | --- |
| Nemotron 3.5 Lightning 30B-A3B Q4_0 (18.90GB) | 1450.33 | 66.80 | 1409.10 | 65.99 | pass; identical across runs |
| Laguna XS 2.1 Q4_K_M (19.56GB) | 1399.02 | 80.45 | 1026.84 | 70.05 | pass; the code prompt needed more than 1024 tokens of reasoning (no answer at `-n 1024`, pass at `-n 4096`); identical across runs |
| Muse Glimmer 30B Q4_K_M, text only (16.76GB) | 370.89 | 13.24 | 346.52 | 13.01 | pass; identical across runs |

All three loaded without an unsupported-architecture error. Muse Glimmer is a
dense model and decodes in the dense-30B speed class, not the 3B-active MoE
class. Two prompts are a smoke test, not a coding or Dutch-quality result.

**Public scores and the dense/MoE split (checked 2026-09-30).** Qwen3.8 27B is a
dense model, not one of the 3B-active MoE files in this tier; its measured Ollama
rates (12.89 t/s without draft and 22.71 t/s with MTP, 2026-09-26) are in the dense
class, below the MoE rows above. On the Artificial Analysis Intelligence Index
v4.3.2 (third-party scores, full precision via API, not measured locally;
quantisation loss unknown; caveats in the capability table above) the models of this
size class score as follows:

| Model | Index v4.3.2 | Note |
| --- | ---: | --- |
| Qwen3.8 27B (`xhigh` reasoning effort) | 33.7 | `Q4_K_M` 18.97GB; measured here through the Ollama API |
| K2 Horizon MoVA 36B-A4B | 25.3 | Needs the open llama.cpp PR #29535 |
| Gemma 4 31B | 14.7 (Reasoning entry, not estimated; read 2026-10-01). Read as 19.0, estimated, on 2026-09-30 | Not measured here |
| Qwen3.6 35B-A3B | 18.2 | Measured here (direct Vulkan, `UD-Q4_K_M`, 62.56 tg128) |
| Muse Glimmer 30B | 17.5 | Scouted 2026-09-26 |
| Granite 4.2 30B | 14.8 (estimated) | Not measured here |
| Nemotron 3.5 Lightning 30B-A3B | 12.9 | Scouted 2026-09-26 |

The vendor's own per-tier table lists a 122B-parameter MoE at Q3 (52.5GB) for 64GB,
not a 30B-class file; see the vendor-published section above. This guide has not
measured a 64GB system and has not reproduced the vendor's figures.

## 128GB Fit Tiers

These are published artifact-size tiers from the 2026-08-29 check, not local
memory-use measurements. Runtime buffers, KV cache, the operating system, and
other workloads still need room; a file fitting on paper is not a usability or
correctness result.

| Tier | Published-size examples |
| --- | --- |
| Comfortable: under 70GB | [gpt-oss-120b GGUF](https://huggingface.co/ggml-org/gpt-oss-120b-GGUF) at about 63GB; [Qwen3-Coder-Next](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF) Q6 at about 66GB; and the measured 35B-and-smaller routes listed above |
| Workable: 70-100GB | [Mistral Medium 3.5](https://huggingface.co/unsloth/Mistral-Medium-3.5-128B-GGUF) Q4/Q5; [Nemotron 3 Super](https://huggingface.co/unsloth/NVIDIA-Nemotron-3-Super-120B-A12B-GGUF) Q4/Q5; [Qwen3.8-Flash-Next](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF) through IQ4_XS at about 94GB; [Step 3.7 Flash](https://huggingface.co/stepfun-ai/Step-3.7-Flash-GGUF) IQ3_XXS 75.76GB and Q3_K_M 93.80GB; [DeepSeek V4-Flash-Vision-Exp](https://huggingface.co/ggml-org/DeepSeek-V4-Flash-Vision-Exp-GGUF) Q2_K_S 98.59GB (2026-09-25 listings); [MiMo-V2.6-Flash-MOPD](https://huggingface.co/AesSedai/MiMo-V2.6-Flash-MOPD-GGUF) community quants at 77.40GB, 81.75GB and 96.74GB (2026-09-30 listings; about 2 to 2.5 bits per weight; unqualified) |
| Tight: over 100GB | [DeepSeek V4-Flash](https://huggingface.co/unsloth/DeepSeek-V4-Flash-GGUF) IQ3_XXS at 103GB; [Step 3.7 Flash](https://huggingface.co/stepfun-ai/Step-3.7-Flash-GGUF) Q4_K_S at 111.5GB; [Qwen3.8-Flash-Next](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF) Q4_K_XL at 111GB; Ollama `qwen3.8-flash-next:125b-a6b-q4_K_M` at 120.06GB (2026-09-25 listing) |

## Other Workloads (third-party routes, not measured here, checked 2026-09-30)

This guide measures LLM text routes. For other workloads this section lists what
third parties publish. None of it was run here, and every rate is a claim of a
third party.

### Image And Video

- **Route.** The community [ComfyUI toolbox for Strix Halo](https://github.com/kyuz0/amd-strix-halo-comfyui-toolboxes)
  (last commit 2026-09-02) bundles workflows for HunyuanVideo 1.5, LTX-2.3,
  MiniMax-H3 (video with audio), Qwen Image 2512, Qwen Image Edit 2511 and Wan 2.2
  14B. Flux is no longer in its bundled workflow list.
- **`--disable-mmap`.** The toolbox starts with `--disable-mmap`. Its README calls
  this critical on Strix Halo because mmap above 64GB is very slow, owing to a ROCm
  issue. The guide tracks that upstream problem (ROCm#6501) and non-deterministic
  ComfyUI/LTX-2.3 hangs (ROCm#6530) in
  [ROCM_VLLM_BUGWATCH.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/ROCM_VLLM_BUGWATCH.md).
- **How long it takes.** The toolbox's benchmark page is undated (its docs were last
  updated 2026-02-13) and its figures are claims of a third party: about 75 s for a
  Qwen Image 2512 4-step image, about 615 s for LTX-2 at 720p with 121 frames, about
  930 to 950 s for HunyuanVideo 1.5 at 720p with 61 frames, and about 2,000 s for
  Wan 2.2 14B at 720p with 41 frames. A short clip therefore takes minutes to over
  half an hour.
- **Comparison.** A [Tweakers review of the ASUS GX10 and the DGX Spark](https://tweakers.net/reviews/14328/nvidia-dgx-spark-asus-ascent-gx10-je-eigen-ai-supercomputer-op-je-bureau.html)
  (2026-03-12; claim of a third party) reports FLUX.2 at about 10 minutes per image
  on the Framework Desktop against about 2 minutes on the DGX Spark, and an AMD
  driver crash without a fixed VRAM allocation.
- **Other routes.** Unsloth Studio reports failures for image, video and audio
  generation on a Radeon 8060S
  ([unslothai/unsloth#9897](https://github.com/unslothai/unsloth/issues/9897), open
  when read; Strix Halo report of 2026-09-23). On Windows, ComfyUI Desktop has had
  official ROCm support since v0.7.0 (2026-01-06); see
  [WINDOWS_START.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/WINDOWS_START.md).

### Speech

- **This guide.** Qwen3-ASR 0.6B and Qwen3-TTS 1.7B English smoke tests only. Dutch
  speech output needs a separate Dutch-capable TTS candidate
  ([CURRENT_MODELS.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/CURRENT_MODELS.md)).
- **faster-whisper.** CTranslate2 4.7.1 ships an official ROCm wheel that includes
  gfx1151. A [recipe](https://github.com/nabe2030/faster-whisper-rocm-strix-halo)
  (EVO-X2, Ubuntu 26.04, ROCm 7.2.2, 2026-04-29) claims Whisper large-v3 at about
  11.5 times realtime on English, and 30 minutes of Japanese in 4 minutes 41
  seconds, without memory faults.
- **Home Assistant voice containers.** [ha-voice-rocm](https://github.com/ndom91/ha-voice-rocm)
  (updated 2026-09-13) provides Wyoming containers for gfx1151 with Whisper,
  Parakeet, Granite and Moonshine for speech to text and Qwen3-TTS, Chatterbox,
  Kokoro and Pocket for text to speech. Its README names Parakeet v3 and Kokoro as
  its daily use.
- **Lemonade** bundles whisper.cpp (Vulkan or ROCm), Kokoro (CPU) and
  stable-diffusion.cpp behind one OpenAI-style API
  ([README](https://github.com/lemonade-sdk/lemonade)).
- **Gufo** lists Qwen3-ASR 1.7B at 15.27 times realtime and Qwen3-TTS 1.7B at up to
  2.54 times realtime with 201 ms to first audio (the makers' numbers; audio
  excludes loading; [README](https://github.com/gufo-org/gufo)).
- **Dutch.** The [Parakeet TDT 0.6B v3 model card](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3)
  lists Dutch among its languages (speech to text). No Dutch text-to-speech route
  was found in the sources read; the Kokoro documentation checked does not list
  Dutch.
- **Windows.** LM Studio's voice mode does not work on AMD under Windows because
  only a CUDA speech-recognition engine exists
  ([#2341](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/2341), open
  when read).

### Fine-Tuning And Quantising

- **4-bit training.** Unsloth's [AMD documentation](https://unsloth.ai/docs/get-started/install/amd)
  (read 2026-09-30) says all ROCm systems need a pre-release `bitsandbytes` build,
  because versions up to 0.49.2 have a 4-bit decode NaN bug on every AMD GPU. This
  guide's one-step smoke recorded `bitsandbytes` 0.50.0.dev0
  ([versions](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/raw/2026-07-21/unsloth-rocm72-train-export-smoke/versions.txt)).
  Check the version if you follow another install path; not tested here.
- **Other tooling.** The community fine-tuning toolbox's last commit is 2026-03-08.
  No gfx1151-specific evidence was found for Axolotl or LLaMA-Factory.
- **Quantising on the box.** AMD's [ROCm blog of 2026-09-25](https://rocm.blogs.amd.com/artificial-intelligence/quark-strix-halo/README.html)
  describes quantising Qwen3.6-35B-A3B from BF16 to W4A16 with AMD Quark on one
  Strix Halo machine (ROG Flow Z13, 128GB, Ubuntu 24.04, ROCm 7.2.0, amd-quark
  0.12.post1) and exporting to GGUF `Q4_0`/`Q4_1` for `llama.cpp` and Lemonade or
  to safetensors for vLLM. AMD reports a peak GTT of 95GB on the GGUF path or 73GB,
  an export time of about 18 to 23 minutes and an accuracy table against BF16. The
  vLLM evaluation ran on a datacenter GPU, not on Strix Halo. All figures are AMD's
  claims, and a 35B model needed the 128GB machine.

### Switching Between Models

- Ollama loads and unloads models on demand by itself; this was not measured here.
- **llama-swap** (MIT; [repository](https://github.com/mostlygeek/llama-swap)) is a
  proxy that starts and stops a server for the requested model. Version v260 was
  released on 2026-09-26, the fifth release in 10 days (read 2026-09-30).
- **`llama-server` router mode** (`--models-dir`, `--models-preset`) loads and
  unloads models dynamically. By default `--models-max` is 4 and autoload is on
  ([server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md),
  read 2026-09-30). With unified memory on a 64GB or 128GB machine, four large
  models can exhaust memory (an inference, not tested here). Until it is measured,
  `--models-max 1` is a cautious setting.
- A reproduction on Strix Halo in
  [llama.cpp issue #27148](https://github.com/ggml-org/llama.cpp/issues/27148)
  (text from another conversation restored into a new answer) used router mode, so
  a model switcher in front of `llama-server` inherits that risk. The reporters'
  mitigation is `--cache-ram 0 --no-cache-idle-slots`; it was not tested here. See
  [SECURE_LOCAL_AI.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/SECURE_LOCAL_AI.md).
- A third-party Windows benchmark repository
  ([strix-halo-windows-llm-bench](https://github.com/ihanesman/strix-halo-windows-llm-bench),
  ROG Flow Z13 128GB, 2026-09-25) runs four models behind llama-swap with a
  different backend each. Its claims: the best `-ub` differs per backend (256 on
  ROCm and 512 on Vulkan for a dense 27B); an `IQ4_XS` model decodes at 7.7 t/s on
  ROCm against 25.2 t/s on Vulkan; and `-np 2` avoids cache thrashing with agent
  clients.

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
