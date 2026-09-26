---
layout: default
title: "Qwen3.8 27B on AMD Strix Halo: Setup, Speed Routes, and Context Evidence"
description: "Run Qwen3.8 27B on Ryzen AI MAX+ 395 / Radeon 8060S: official Ollama setup, measured 20.42 t/s Ollama-default-MTP route, 50K local retrieval, external 262K evidence, MTP, DFlash, and current 52-65 t/s claims explained."
permalink: /qwen38-strix-halo/
canonical_url: "https://strixhaloguide.com/qwen38-strix-halo/"
sitemap: false
date: "2026-08-25T00:00:00+02:00"
last_modified_at: "2026-09-19T00:00:00+02:00"
image:
  path: "https://hogeheer499-commits.github.io/strix-halo-guide/assets/qwen38-route-preview.png"
  height: 640
  width: 1280
  alt: "Qwen3.8 27B routes on AMD Strix Halo with measured official and external context evidence"
seo:
  type: "TechArticle"
  date_modified: "2026-09-19T00:00:00+02:00"
---

# Qwen3.8 27B on AMD Strix Halo

**September 19 functional update:** the [scoped runtime qualification](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/RUNTIME_QUALIFICATION_2026-09-19.md)
records text (Qwen3.6), image (Qwen2.5-VL), executed tools (Devstral) and pinned
Open WebUI on the existing 0.32.15 service after restart. Isolated 0.34.2 is
useful but not default; official Qwen3.8 and full-reboot candidate acceptance
remain open. The tested host's Ollama listener was LAN-reachable, not local-only.
Released llama.cpp v0.4.1 passed bounded direct/server/HIP controls; this does
not qualify every model, long-context shape or maximum-memory allocation.

Qwen3.8 27B runs locally on AMD Ryzen AI MAX+ 395 / Radeon 8060S Strix Halo
systems. The useful question is no longer only “does it run?” It is which
official, stock, MTP, DFlash, ROCmFP4, or performance-fork route fits the
workload—and which published numbers are actually comparable.

**Evidence reviewed:** September 26, 2026.

Project home: [Strix Halo Guide](https://strixhaloguide.com/). The [canonical Qwen3.8 evidence page](https://strixhaloguide.com/qwen38-strix-halo/) is on the project domain; this page remains a technical mirror.

## Fast Answer

| Question | Current answer |
| --- | --- |
| Easiest measured official route | `qwen3.8:27b` through Ollama 0.32.13 and Vulkan/RADV |
| Guide-measured warm result | 292.49 prompt t/s and 20.42 generation t/s over nine repeats, measured as Ollama API with Ollama-default MTP drafting (`draft_num_predict 4`; `draft-mtp` logged in the same-service 64K run; per-run log for the 4K warm runs not captured); not a no-draft result, and a matched no-draft control is queued |
| Guide-measured capabilities | Image, tool-call, thinking, and exact retrieval through 50,059 prompt tokens passed |
| Long-context boundary | A 56,051-token attempt caused a recoverable device loss on that exact stack; separate corrected GMKtec evidence reached 261,130 evaluated tokens |
| 52-65 t/s posts | Advanced fork/quant/speculation leads that require their exact artifacts, prompts, context behavior, and independent reproduction |

For commands, the complete matrix, caveats, upstream alerts, and raw evidence,
read the canonical
[Qwen3.8 Strix Halo decision page](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/QWEN38_STRIX_HALO.md).

## Start With Ollama

The measured official route used the 17.7GB-decimal `Q4_K_M` artifact:

```bash
# Requires Ollama 0.32.12 or later; measured on 0.32.13
ollama run qwen3.8:27b
```

The Strix Halo service still needs the guide's Vulkan/iGPU environment,
including `OLLAMA_VULKAN=1` and `OLLAMA_IGPU_ENABLE=1`. Ollama 0.34.2 was the
current checked package on September 19 (0.34.4 was available on September 25,
unqualified). Neither has inherited the measured 0.32.13 result or the full
normal-service/reboot qualification.

## Why The Speed Claims Differ

Official Ollama (which enables its default MTP drafting for `qwen3.8:27b`), stock `llama.cpp`, custom quants, ROCmFP4, native MTP,
DFlash2, and adaptive speculation are different routes. Code versus prose,
cold versus cached context, context depth, generated-token count, and draft
acceptance can change the result again. A useful comparison therefore records
the entire profile, not only a tokens-per-second screenshot.

The guide keeps:

- [first-party raw Ollama evidence](https://github.com/hogeheer499-commits/strix-halo-guide/tree/main/data/raw/2026-08-15/qwen38-27b-ollama-03213-vulkan-radv),
- [community/runtime provenance](https://github.com/hogeheer499-commits/strix-halo-guide/tree/main/data/raw/2026-08-25/qwen38-community-runtime-update), and
- the [machine-readable route matrix](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/qwen38_route_matrix.csv)

separate so readers can decide which result applies to them.

## What Should Be Tested Next?

The missing proof is a matched same-host ladder: stock b10687 Vulkan without
speculation, native MTP, corrected HIP correctness, a published ROCmFP4 route,
and a fully published DFlash/adaptive route. It must cover code and prose,
4K/16K/50K context, exact outputs, vision/tools, acceptance, memory, hashes,
and raw logs.

See the live [test queue](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/current_test_queue.csv)
or submit a [benchmark report](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=benchmark-report.md).

## Independence And Affiliate Disclosure

This guide contains no affiliate links as of September 19, 2026. Future affiliate,
loaned, gifted, sponsored, or early-access relationships must be disclosed near
the relevant links/results and do not buy positive conclusions. Community
results remain separate from first-party measurements. The public
[affiliate link registry](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/affiliate_link_registry.csv)
remains the audit source if that status changes.
