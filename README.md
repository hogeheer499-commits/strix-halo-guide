![AMD](https://img.shields.io/badge/AMD-Ryzen_AI_MAX+_395-ED1C24?style=for-the-badge&logo=amd&logoColor=white)
![Speed](https://img.shields.io/badge/direct_30B_Qwen-100.0_t/s-brightgreen?style=for-the-badge)
![Small MoE](https://img.shields.io/badge/small_MoE-170.0_t/s-brightgreen?style=for-the-badge)
![284B](https://img.shields.io/badge/direct_284B_GGUF-13.3_t/s-0ea5e9?style=for-the-badge)
![MTP](https://img.shields.io/badge/MTP_server-101--140_t/s_experimental-7c3aed?style=for-the-badge)
[![Community](https://img.shields.io/badge/community-8_benchmark_contributors_11_systems%2Fsources-success?style=for-the-badge)](COMMUNITY_RESULTS.md)
![RAM](https://img.shields.io/badge/128GB_unified-blue?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/hogeheer499-commits/strix-halo-guide?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
[![Validate](https://img.shields.io/github/actions/workflow/status/hogeheer499-commits/strix-halo-guide/validate.yml?branch=main&label=validate&style=for-the-badge)](https://github.com/hogeheer499-commits/strix-halo-guide/actions/workflows/validate.yml)

# AMD Strix Halo Local LLM Guide for Ryzen AI MAX+ 395 / Radeon 8060S (gfx1151)

A complete, practical guide to running large language models locally on AMD Strix Halo / Ryzen AI MAX+ 395 systems with Radeon 8060S (`gfx1151`) and 96GB/128GB unified memory.

Covers BIOS config, Ubuntu 24.04/kernel setup, Ollama, `llama.cpp` Vulkan/RADV, ROCm/HIP experiments, vLLM notes, 70B/120B and selected 284B GGUF capacity evidence, benchmarks, raw logs, and reproducibility checks.

AMD now publicly frames Ryzen AI Halo-class systems as a local-AI and developer-platform direction. This repository is the independent practical layer: copyable setup, measured rows, raw evidence, failures, and community reproductions. It is not official AMD or OEM endorsement. See [`RYZEN_AI_HALO_CONTEXT.md`](RYZEN_AI_HALO_CONTEXT.md).

Project website: <https://strixhaloguide.com/>. This GitHub repository remains the source of truth for setup commands, benchmark claims, and raw evidence.

Maintainer credibility is also public and reviewable: accepted upstream contributions include code and validation in [`llama.cpp`](https://github.com/ggml-org/llama.cpp/pull/25643), LocalAI, Qwen Code, OpenTelemetry GenAI, and NVIDIA AICR, plus tested-coverage documentation in the vLLM GGUF plugin. See [`UPSTREAM_CONTRIBUTIONS.md`](UPSTREAM_CONTRIBUTIONS.md) for exact PR links, scope, and honest boundaries. Upstream acceptance strengthens confidence in the engineering process; it does not replace the raw evidence required for each benchmark claim.

What you get:

- Copyable Ubuntu + Vulkan/RADV setup for Ollama and `llama.cpp`.
- Practical model/backend choices for a local AI PC.
- Direct local results: Qwen3-Coder 30B at 101.0 t/s on the official `llama.cpp` b9851 Vulkan release binary, Qwen3-30B-A3B-Instruct-2507 IQ4_XS at 100.0 t/s with a b9544 control at 103.2 t/s, LFM2.5 8B-A1B at 170.0 t/s with a b9544 control at 176.5 t/s, Nemotron 3 Super 120B-A12B at 18.4-18.9 t/s, and a 90.86GB DeepSeek V4 Flash 284B `UD-IQ2_XXS` capacity scout at 13.27 t/s direct on Vulkan/RADV.
- Experimental server routes: Qwen3.6 MTP at 101.1 t/s, Gemma 4 26B-A4B QAT MTP up to 110.0 t/s best-repeat, and CHADROCK ACE/SABER 35B ROCmFP4 at 141.37 t/s across three repeats on one exact high-acceptance reference profile with `llama-server` speculative decoding. The CHADROCK number is prompt-shape-specific, not a universal server speed.
- Multi-user evidence: b9979 stock, opt-in AMD/RADV density, dense16, and Lemonade ROCm concurrency matrices for 30B 128-expert/top-8 and 80B 512-expert/top-10 MoE models.
- Raw CSVs, logs, charts, and reproducibility notes for headline claims.
- Community validation from Beelink, Corsair, GMKtec, MS-S1-Max, Nimo, NixOS, NPU, ROCmFP4, and other Strix Halo owner stacks.

> Measured primarily on one Beelink GTR9 Pro. Community results are kept separate from local headline claims. This repository ships docs, scripts, data, and charts only; no `.exe`, binary `.zip`, browser extensions, or model weights. Raw evidence, commands, caveats, and corrections are linked so results can be checked instead of taken on trust.

[Quick Start](#quick-start-6-steps) | [Setup Script](#setup-script) | [Short Setup Answer](STRIX_HALO_LOCAL_LLM_SETUP.md) | [AI Halo Context](RYZEN_AI_HALO_CONTEXT.md) | [What Runs](#what-you-can-run-quick-snapshot) | [Profiles](BEST_KNOWN_PROFILES.md) | [Current Models](CURRENT_MODELS.md) | [Fine-Tune](UNSLOTH_STRIX_HALO.md) | [Use Cases](#use-this-if-you-want) | [Rules](#community-tested-rules-of-thumb) | [Best Setup](#best-current-setup-tested-here) | [Evidence](#headline-evidence) | [Upstream Work](UPSTREAM_CONTRIBUTIONS.md) | [Concurrency](MOE_CONCURRENCY.md) | [MTP](MTP_SPECULATIVE_DECODING.md) | [Community](COMMUNITY_RESULTS.md) | [Feedback](COMMUNITY_FEEDBACK.md) | [RPC](COMMUNITY_RPC.md) | [USB4](USB4_CLUSTER_TUNING.md) | [Reproduce](#reproduce-one-headline-result) | [Security](SECURITY.md)

---

## Use This Guide If

- You have, ordered, or are evaluating a Strix Halo / Ryzen AI MAX+ 395 system for local AI.
- You want a copyable Ubuntu local-LLM setup instead of piecing together scattered posts.
- You need practical model/backend choices for Ollama, llama.cpp Vulkan/RADV, ROCm, server use, and long context.
- You want benchmark claims that point to CSVs, raw logs, charts, and reproducibility notes.

## What This Gives You

| If you want to... | Start here |
|-------------------|------------|
| Apply the setup without reading everything | [Quick Start](#quick-start-6-steps), then [Setup Script](#setup-script). |
| Need the short current setup answer | [`STRIX_HALO_LOCAL_LLM_SETUP.md`](STRIX_HALO_LOCAL_LLM_SETUP.md): concise Strix Halo / Ryzen AI MAX+ 395 local LLM setup, benchmark highlights, and source-of-truth links. |
| Understand why this guide matters now | [`RYZEN_AI_HALO_CONTEXT.md`](RYZEN_AI_HALO_CONTEXT.md): how AMD's public Ryzen AI Halo / Developer Platform direction maps to this guide's independent setup and benchmark evidence. |
| Decide what to run on your Strix Halo machine | [What You Can Run: Quick Snapshot](#what-you-can-run-quick-snapshot), then [Use This If You Want](#use-this-if-you-want): practical model and backend choices for a local AI PC. |
| Need a machine-readable known-good route | [`BEST_KNOWN_PROFILES.md`](BEST_KNOWN_PROFILES.md) and [`data/best_known_profiles.csv`](data/best_known_profiles.csv): compact workload-to-runtime recommendations that link back to the full evidence. |
| See what should be tested next | [`CURRENT_MODELS.md`](CURRENT_MODELS.md) and [`data/current_test_queue.csv`](data/current_test_queue.csv): current candidates, practical artifact sizes, blockers, and the buyer question each test should answer. |
| Fine-tune and export a model locally | [`UNSLOTH_STRIX_HALO.md`](UNSLOTH_STRIX_HALO.md): measured ROCm GPU gate, one-step Unsloth training smoke, GGUF export, local ROCm inference, persistence, and the two setup failures found along the way. |
| Skip the community-data deep dive | [Community-Tested Rules Of Thumb](#community-tested-rules-of-thumb): practical decisions extracted from the Beelink data plus Corsair, GMKtec, MS-S1-Max, Nimo, NixOS/NPU, and ROCmFP4 community reports. |
| See what work was actually done | [Headline Evidence](#headline-evidence): dated claims with backend, model, result, CSV, raw logs, charts, and notes. |
| Check whether the numbers are real | [Reproduce One Headline Result](#reproduce-one-headline-result), [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md), and [`data/headline_claims.csv`](data/headline_claims.csv). |
| Verify the maintainer's upstream engineering work | [`UPSTREAM_CONTRIBUTIONS.md`](UPSTREAM_CONTRIBUTIONS.md): accepted changes in `llama.cpp` and other AI infrastructure, with direct PR links, validation scope, and explicit limits on what those merges prove. |
| Compare against other Strix Halo systems | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md): independent benchmark reports kept separate from headline claims, including native Linux, WSL2/HIP, Windows LM Studio, power, tuned thermal/power-policy rows, and Nimo large-model serving evidence. [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md): multi-node USB4 RPC results. [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md): cluster latency tuning. |
| Diagnose sustained thermal or custom fan-control trouble | [`THERMAL_STABILITY.md`](THERMAL_STABILITY.md): scoped Corsair/Sixunited three-system evidence, post-kernel-update checks, cap tradeoffs, stock controls, and the upstream fan-reset patch. |
| Check current ROCm, kernel, container, or runtime compatibility alerts | [`ROCM_VLLM_BUGWATCH.md`](ROCM_VLLM_BUGWATCH.md#current-strix-halo-compatibility-alerts): narrowly scoped upstream reports with safe troubleshooting boundaries. |
| See how public corrections change the guide | [`COMMUNITY_FEEDBACK.md`](COMMUNITY_FEEDBACK.md): trust/framing lessons, corrected routes, and examples of community pushback turning into better evidence. |

## 20-Second Summary

| Question | Current answer |
|----------|----------------|
| What was tested? | Local LLM inference and local API serving on Strix Halo, mainly Vulkan/RADV llama.cpp, Ollama, ROCm/HIP, Lemonade `llamacpp-rocm`, and early vLLM smoke tests. |
| Primary hardware | Beelink GTR9 Pro, Ryzen AI MAX+ 395, Radeon 8060S `gfx1151`, 128GB LPDDR5X-8000 unified memory. |
| Best easy path | The normal Ollama 0.31.2 system service with Vulkan/RADV for chat, model pulling, vision, and Open WebUI. It measured 60.57 t/s warm Qwen3.6 API generation and survived service restart plus a full host reboot. An isolated 0.32.3 check later measured 73.13 t/s versus 73.20 on 0.31.2, preserved exact text outputs, and passed iGPU vision plus process restart. Keep 0.31.2 as the default only until 0.32.3 completes the same normal package-upgrade and full-reboot path. |
| Local training/export path | A pinned ROCm 7.2 Unsloth container detected the Radeon 8060S, completed a one-step Qwen3 0.6B SFT smoke, loaded the checkpoint, exported `Q4_K_M` GGUF, loaded it through ROCm `llama.cpp`, and loaded the host-persisted artifact again after restart. This proves the workflow, not useful fine-tuning quality or large-model training speed. |
| Fastest measured short-context path | Direct llama.cpp / `llama-server` with Vulkan/RADV. Current Qwen3-Coder Q4_K_S speed-first row reached 100.99 t/s r50 on the official b9851 Vulkan release binary. The older strict-clean b9179 Qwen3-Coder row remains in the evidence at 98.51 t/s r50, and a separate Qwen3-30B-A3B-Instruct-2507 IQ4_XS row reached 100.04 t/s r50 on b9467 with a b9544 control at 103.18 tg128 r10. |
| Fastest current small-MoE scout | LFM2.5 8B-A1B Q4_K_M reached 168.96 tg128 in a pp512/tg128 run and 170.02 t/s generation-only on the 2026-06-05 latest/int-dot check; the 2026-06-07 b9544 control measured 176.48 tg128 r10. This is a small active-parameter MoE speed result, not a 30B-class capability replacement. |
| Largest current direct GGUF capacity route | DeepSeek V4 Flash 284B `UD-IQ2_XXS` loaded as a pinned 90.86GB ordinary GGUF and measured 155.64 pp512 / 13.27 tg128 on official b10034. It answered a deterministic smoke correctly, but the low-bit quant and visible thinking block make this capacity/current-model evidence rather than a speed or broad quality recommendation. |
| Current 120B-class direct GGUF route | Nemotron 3 Super 120B-A12B `UD-IQ4_XS` ran directly at 18.43 tg128, with a b9544 control at 18.93 tg128. It remains a useful more-balanced 120B-class capacity route. |
| Experimental speculative server path | MTP works on current `llama.cpp`/ROCmFPX routes. The best local Qwen3.6 MTP server route uses IQ4_XS-Q8nextn and reached about 101.1 t/s across six prompts on b9360; Gemma 4 26B-A4B QAT reached up to 110.0 t/s best-repeat; the exact CHADROCK ACE/SABER reference profile averaged 141.37 t/s over three repeats at 100% draft acceptance. These are server/speculative results, not direct `llama-bench` headlines. CHADROCK's separate 1K and 8K profiles were much slower, so operators must profile real prompts. |
| Frontier-size local agent path | Step 3.7 Flash ROCmFPX Q3 QualityPlus runs as a 198B-total / about 11B-active target plus separate Q8 MTP draft: 34.50 t/s at 4K, 33.83 t/s at 16K, native tool-call pass, and full 256K allocation. This is advanced server/capacity evidence, not direct `llama-bench`; the 256K result is allocation, not a filled-context quality test. |
| Current runtime status | The normal Ollama 0.31.2 service path remains the fully reboot-qualified default. Isolated Ollama 0.32.3 preserved Qwen3.6 text speed/output and passed iGPU vision plus process restart, so only the normal service-upgrade/full-reboot step remains. Official `llama.cpp` b10107 is locally qualified for the pinned LFM2.5-VL image and Qwen3-ASR audio smokes, but those narrow checks do not replace the b10034 Vulkan concurrency sentinel. A stock-versus-PR #25666 MTP A/B preserved exact outputs and acceptance with only +0.55% warm speed, making it no-regression evidence rather than a new performance recommendation. See [`CURRENT_MODELS.md`](CURRENT_MODELS.md), [`MOE_CONCURRENCY.md`](MOE_CONCURRENCY.md), and the current [`compatibility alerts`](ROCM_VLLM_BUGWATCH.md#current-strix-halo-compatibility-alerts). |
| Current HIP/UMA compatibility status | Official `llama.cpp` b10046 locally detected 120,124 MiB free UMA and used real `ROCm_Host` model, output, and compute buffers on `gfx1151` without a gfx-version override. The release binary needed the existing Ollama ROCm library path on this host. This validates merged HIP integrated-device support; it does not replace Vulkan/RADV as the beginner path. |
| Large local model checks | gpt-oss-120b MXFP4 loaded at 55.57 tg128; Nemotron 3 Super 120B-A12B at 18.43 tg128; MiniMax M2.7 230B-class MoE loaded and generated; and DeepSeek V4 Flash 284B `UD-IQ2_XXS` loaded directly at 13.27 tg128. These are different capacity/quality tradeoffs, not interchangeable speed claims. |
| Best measured Qwen3.6 server path | Vulkan/RADV wins at 1-4 parallel requests; Lemonade `llamacpp-rocm` b1259 wins aggregate throughput at 8-16. |
| Latest multi-user MoE finding | Official b10034 confirms that the concurrency-8-to-9 cliff persists: -37.34% aggregate decode on Qwen3-Coder 30B-A3B and -31.69% on Qwen3-Next 80B-A3B. The separate b9979 campaign shows an opt-in AMD/RADV density gate recovering 42.7% at 30B np9 and 25.3% at 80B np9; dense16 is not a universal default. See [`MOE_CONCURRENCY.md`](MOE_CONCURRENCY.md). |
| Current community thermal/stability finding | On Fail-Safe's three matched Corsair systems, 2400 MHz was the best measured conservative SCLK tradeoff: generation stayed within about 1% of higher caps and retained runs stayed at or below 75 C. This is fleet-specific, not a universal cap. Bounded stock controls saw 0/3 locks, while historical logs exposed a missing custom EC/fan module after kernel updates as a plausible major confounder. See [`THERMAL_STABILITY.md`](THERMAL_STABILITY.md). |
| Backend split | Vulkan/RADV wins measured generation on the current single-box Qwen rows; ROCm/HIP can win prompt-processing-heavy work, and ROCm RPC is required for the tested MiniMax capacity case. See [`BACKEND_CROSSOVER.md`](BACKEND_CROSSOVER.md) and [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md). |
| Community validation | The evidence map covers 11 systems or independent sources from 8 credited community benchmark contributors, with first-party and community claims kept separate. It includes same-SKU variance, cross-OEM Linux and Windows routes, wall power, USB4 RPC, NPU sidecars, ROCmFP4, large-model capacity, thermals, and failed paths. See the counted [`Evidence Coverage`](#evidence-coverage-11-systems-or-independent-sources) table and [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md). |
| Claim index | [`data/headline_claims.csv`](data/headline_claims.csv) maps each public headline to CSV, raw evidence, chart, and notes. |
| Raw evidence | Structured CSVs in [`data/`](data/README.md), raw logs in [`data/raw/`](data/raw/), generated charts in [`charts/`](charts/README.md). |

## Quick Start (6 Steps)

For those who want to get running as fast as possible:

1. **BIOS:** Set UMA Frame Buffer to 512MB if available; if your BIOS minimum is 2GB, leave it at 2GB. Keep IOMMU enabled/default for laptops, suspend, and NPU use. Disabling it is an optional desktop benchmark profile.
2. **Install Ubuntu 24.04 LTS**, switch to X11.
3. **Kernel params:** Add `amdgpu.gttsize=131072 ttm.pages_limit=31457280` to GRUB. Add `amd_iommu=off` only for the optional desktop benchmark profile after reading [Choose the IOMMU policy](#step-12-choose-the-iommu-policy).
4. **Performance:** Install tuned, set `accelerator-performance` profile, upgrade Mesa via kisak PPA.
5. **Ollama:** Install, configure Vulkan backend with `OLLAMA_VULKAN=1` and `HIP_VISIBLE_DEVICES=-1`.
6. **Test:** `ollama run qwen3.6:35b-a3b` -- the measured Ollama 0.31.2 system-service path reached about 60 t/s generation. Exact speed depends on runtime, model, power state, and background load.

Use the setup script below for the automated path. The phases later in this README are the manual reference and fallback path if you want to inspect or reproduce each change yourself.

## Setup Script

If you've already set your BIOS (UMA = 512MB if available, or 2GB if that is your vendor minimum; leave IOMMU enabled/default unless you deliberately choose the desktop benchmark profile) and installed Ubuntu 24.04:

```bash
git clone https://github.com/hogeheer499-commits/strix-halo-guide
cd strix-halo-guide
bash setup.sh
```

Optional: inspect the script first with `less setup.sh` before running it on a production system.

For unattended copy/paste installs, the same script can also be run as:

```bash
curl -fsSL https://raw.githubusercontent.com/hogeheer499-commits/strix-halo-guide/main/setup.sh | bash
```

This installs the Linux-side Vulkan/RADV + Ollama path, configures Ollama for Vulkan, pulls a model, and prepares a verification benchmark. If the script changes boot parameters, reboot first and then run `bash ~/bench-ollama.sh`.

## What You Can Run: Quick Snapshot

This is the quick "what can I actually run on my AI PC?" view. It is not the full benchmark list; see [What You Can Run](#what-you-can-run) for more models and [Headline Evidence](#headline-evidence) for the audit trail.

| What you want to do | Measured local result | Practical takeaway | Evidence |
|---------------------|-----------------------|--------------------|----------|
| Fastest direct 30B-class Qwen MoE row | Qwen3-30B-A3B-Instruct-2507 IQ4_XS: 100.04 t/s direct llama.cpp Vulkan/RADV on b9467; b9544 control measured 103.18 tg128 r10 | First local direct `llama-bench` row above 100 t/s. Treat it as a separate general-instruct Qwen route, not as a Qwen3-Coder replacement or balanced-default claim. | [`headline claims`](data/headline_claims.csv), [`raw r50`](data/raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/qwen3-30b-2507-iq4xs-b9467-r50.csv), [`b9544 control`](data/raw/2026-06-07/latest-llamacpp-b9544-regression/) |
| Fastest current small-MoE scout | LFM2.5 8B-A1B Q4_K_M: 168.96 tg128 in pp512/tg128, 170.02 t/s generation-only, b9544 control at 176.48 tg128 r10 | Shows how fast newer small active-parameter MoE routes can be on Strix Halo. Do not compare it as a 30B-class coding/reasoning replacement. | [`headline claims`](data/headline_claims.csv), [`raw latest/int-dot`](data/raw/2026-06-05/latest-llamacpp-intdot-regression/), [`b9544 control`](data/raw/2026-06-07/latest-llamacpp-b9544-regression/) |
| Fastest local coding speed | Qwen3-Coder 30B-A3B Q4_K_S: 100.99 t/s direct llama.cpp Vulkan/RADV on the official b9851 release binary; older strict-clean b9179 row measured 98.51 t/s | Speed-first quant candidate. Use it when raw t/s matters and you accept the quality tradeoff. This is direct `llama-bench`, not MTP/server speculation. | [`headline claims`](data/headline_claims.csv), [`b9851 raw r50`](data/raw/2026-06-30/latest-llamacpp-b9851-vulkan-sentinel/qwen3-coder-q4ks-b9851-p512-n128-r50.csv), [`older strict-clean raw r50`](data/raw/2026-05-16/break-97-24-strict-noise-settings/b9179-q4-k-s-r50.csv) |
| Fast balanced local coding model | Qwen3-Coder 30B-A3B UD-Q4_K_XL: 96.76 t/s direct llama.cpp Vulkan/RADV on current b9049 | Strong first model for coding scripts, editors, and agent loops. | [`headline claims`](data/headline_claims.csv), [`raw run`](data/raw/2026-05-07/max-performance-campaign/benchmarks/qwen3-coder-top-confirm-r20/guide.csv) |
| Newer Qwen coding model | Qwen3-Coder-Next 80B-A3B IQ4_XS: 61.91 t/s direct llama.cpp Vulkan/RADV on b9467 | Modern coding-model row for people who want current Qwen Coder-Next rather than the older 30B speed headline. Use it for capability/currentness, not maximum raw t/s. | [`benchmarks CSV`](data/benchmarks.csv), [`raw run`](data/raw/2026-06-02/modern-model-clean-followup/) |
| Easy private chat setup | Qwen3.6 35B-A3B Q4_K_M: 60.57 t/s warm API generation through the normal Ollama 0.31.2 system service with `OLLAMA_IGPU_ENABLE=1`; vision, service restart, and full-host reboot persistence passed | This is the copyable default for model pulling, Open WebUI, vision, and simple local chat. A later controlled local-binary comparison measured 0.31.1/0.31.2/0.32.0 at 72.55/73.19/73.20 t/s, so do not treat the earlier 60.57-versus-71.82 gap as a version-wide regression. | [`headline claims`](data/headline_claims.csv), [`raw service run`](data/raw/2026-07-10/ollama-0312-buyer-path/), [`raw controlled comparison`](data/raw/2026-07-16/ollama-0311-0312-0320-controlled/) |
| Fine-tune, export, and reload a local model | Pinned ROCm 7.2 Unsloth route: Radeon GPU gate, one SFT step, checkpoint inference, `Q4_K_M` GGUF export, ROCm `llama.cpp` inference, and post-restart artifact load all passed | End-to-end developer workflow evidence on a retail box. The Qwen3 0.6B one-step run is a plumbing smoke, not a quality or performance headline. | [`Unsloth guide`](UNSLOTH_STRIX_HALO.md), [`raw evidence`](data/raw/2026-07-21/unsloth-rocm72-train-export-smoke/) |
| Fast all-rounder direct path | Qwen3.6 35B-A3B UD-Q4_K_M: 62.56 t/s direct llama.cpp Vulkan/RADV on current b9049 | Use this when you care more about speed and control than the easiest UI. | [`headline claims`](data/headline_claims.csv), [`raw run`](data/raw/2026-05-07/latest-stack-rerun/clean-b9049-rerun/qwen36-35b-b9049-clean-r20.csv) |
| Fastest Qwen3.6 direct path | Qwen3.6 35B-A3B Q4_0: 81.30 t/s direct llama.cpp Vulkan/RADV on current b9049 | Speed-first option. Use the default/balanced quant if quality matters more than raw t/s. | [`max campaign`](data/max_performance_campaign.csv), [`raw run`](data/raw/2026-05-07/max-performance-campaign/benchmarks/qwen36-top-confirm-r20/q4-0-ub2048.csv) |
| Qwen3.6 27B dense control | Official Qwen3.6 27B MTP Q8_0: 7.61-7.74 t/s without MTP, 14.59-14.69 t/s with the best MTP setting; a direct b9467 `llama-bench` follow-up measured 7.70 t/s tg128 | Useful practical row for people comparing 27B versus 35B-A3B. It runs, but this dense Q8 route is much slower than the 35B-A3B MoE paths and is not a speed candidate. | [`Performance notes`](PERFORMANCE_NOTES.md#qwen36-27b-mtp-q8_0-status), [`MTP CSV`](data/mtp_speculative.csv), [`raw b9235`](data/raw/2026-05-19/qwen36-27b-mtp-q8-llamacpp-9235/), [`raw latest`](data/raw/2026-06-01/qwen36-27b-mtp-latest-de6f727/), [`raw b9467`](data/raw/2026-06-02/reddit-look-int-dot-reproduction/) |
| Experimental Qwen3.6 MTP server path | Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn: 101.16 t/s best local Beelink six-prompt average on b9360, with t16 repeats at 101.15 / 101.10 / 101.06 t/s; first GMKtec community reproduction reached 93.29 t/s on b9235 | Advanced speculative-decoding route. Useful if you are testing a local API server; keep separate from direct `llama-bench`. | [`MTP notes`](MTP_SPECULATIVE_DECODING.md), [`MTP CSV`](data/mtp_speculative.csv), [`local raw`](data/raw/2026-05-27/latest-llamacpp-b9360/), [`GMKtec raw`](data/raw/2026-05-19/community-gmktec-mtp-issue18/) |
| Experimental Gemma 4 QAT MTP server path | Gemma 4 26B-A4B QAT UD-Q4_K_XL + matched Q4_0 MTP head: 110.00 t/s best repeat, 107.42 t/s T3-only repeat, 102.69 t/s cold repeat, 73.96 t/s no-spec baseline on ac4cddeb0 | Strong current-model server route: matched QAT MTP heads can materially lift a current Google model on Strix Halo. Treat as `llama-server` speculative evidence, not a direct `llama-bench` replacement. | [`headline claims`](data/headline_claims.csv), [`MTP CSV`](data/mtp_speculative.csv), [`warm raw`](data/raw/2026-06-11/gemma4-26b-qat-mtp-sixprompt-ac4cddeb/), [`cold raw`](data/raw/2026-06-12/gemma4-26b-qat-mtp-cold-repeat-ac4cddeb/), [`T3-only raw`](data/raw/2026-06-12/gemma4-26b-qat-mtp-t3-only-repeat-ac4cddeb/) |
| Official Gemma 4 31B QAT multimodal route | Official Q4_0 GGUF: 308.28 pp512 / 11.38 tg128 direct on b10066; narrow text, `STRIX 395` vision, and native calculator tool-call smokes passed | Current dense Google-model compatibility route for buyers who value text, vision, and tools over maximum decode speed. The matched Q8_0 DFlash sidecar loaded but was slower on the measured 5.5K/21.9K synthetic prompt shapes because acceptance stayed low. | [`benchmarks CSV`](data/benchmarks.csv), [`MTP CSV`](data/mtp_speculative.csv), [`raw evidence`](data/raw/2026-07-18/gemma4-31b-qat-dflash-b10066/) |
| Experimental CHADROCK ROCmFP4 MTP server path | CHADROCK ACE/SABER 35B ROCmFP4 through `ciru-ai/ROCmFPX`: 141.37 t/s mean across three repeats on the exact 3946-token reference profile, with 100% mean draft acceptance | Fastest repeat-confirmed server/speculative reference profile in the guide, but not a universal speed. Separate 1K/8K/16K profiles measured 78.00/83.85/107.23 t/s as acceptance changed. Treat as advanced ROCmFPX/CHADROCK evidence, not a direct `llama-bench` replacement. | [`ROCMFP4_CHADROCK.md`](ROCMFP4_CHADROCK.md), [`raw stability profile`](data/raw/2026-07-16/rocmfpx-chadrock-stability-profile/), [`MTP CSV`](data/mtp_speculative.csv) |
| Frontier-size agent server | Step 3.7 Flash 198B-A11B ROCmFPX Q3 plus Q8 MTP draft: 23.84 t/s matched 4K no-spec baseline, 34.50 t/s 4K MTP, 33.83 t/s 16K MTP, native tool-call pass, and 256K allocation | Shows the capacity and agent value of 128GB unified memory rather than chasing the fastest small-model row. Advanced pinned runtime; server/MTP result, and the 48K row has one repeat. | [`ROCmFPX guide`](ROCMFP4_CHADROCK.md#step-37-q3-qualityplus-first-party-reproduction), [`raw evidence`](data/raw/2026-07-16/step37-rocmfpx-q3-qualityplus/), [`MTP CSV`](data/mtp_speculative.csv) |
| 80B MoE coding/reasoning experiments | Qwen3-Next 80B-A3B UD-Q4_K_XL: 59.06 t/s direct llama.cpp Vulkan/RADV on b9172 | Best current 80B Qwen-family path measured here; use when model size and 256K context matter more than smallest footprint. | [`headline claims`](data/headline_claims.csv), [`raw r20`](data/raw/2026-05-16/latest-stack-b9172/qwen3-next-confirm-r20/qwen3-next-80b-b9172-ub1024-r20.csv) |
| Open-weight 120B reasoning model | gpt-oss-120b MXFP4: 55.57 t/s direct llama.cpp Vulkan/RADV on current b9049 | 128GB unified memory can run a 117B-parameter MoE locally; this is speed evidence, not a model-quality eval. | [`headline claims`](data/headline_claims.csv), [`raw run`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/) |
| Current 120B-class GGUF capacity route | Nemotron 3 Super 120B-A12B UD-IQ4_XS: 18.43 t/s direct llama.cpp Vulkan/RADV, b9544 control at 18.93 tg128 r3 | Answers a different buyer question: yes, a current 120B-class MoE GGUF route can run directly on one 128GB Strix Halo box. | [`headline claims`](data/headline_claims.csv), [`raw latest/int-dot`](data/raw/2026-06-05/latest-llamacpp-intdot-regression/), [`b9544 control`](data/raw/2026-06-07/latest-llamacpp-b9544-regression/) |
| Current NVIDIA Omni/FP4 route | The same Nemotron 3 Nano Omni MXFP4 artifact improved from 56.56 tg128 on b9747 to 64.26 on b10034; a separate NVFP4 + F16 projector route measured 53.21 tg128 and correctly read `STRIX 395` from an image | Shows both current runtime maintenance and a first-party image-capable Nemotron route. The OCR check is not broad vision/audio/video validation and neither row replaces the Qwen speed headlines. | [`benchmarks CSV`](data/benchmarks.csv), [`raw MXFP4 sentinel`](data/raw/2026-07-16/nemotron-omni-mxfp4-b10034-sentinel/), [`raw multimodal scout`](data/raw/2026-07-16/nemotron-omni-nvfp4-multimodal/) |
| Current agent/reasoning scouts | Nemotron Cascade 2 30B-A3B `IQ4_XS`: 78.95 tg128; Qwen AgentWorld 35B-A3B `UD-IQ4_XS`: 65.65 tg128 with a correct terminal-world smoke and 128K allocation pass | These answer current-model and agent-use-case questions without pretending every new model is a speed headline. Cascade's forced no-think prefix did not hide reasoning; AgentWorld's 128K result is an allocation smoke, not a filled-context quality claim. | [`CURRENT_MODELS.md`](CURRENT_MODELS.md), [`Cascade evidence`](data/raw/2026-07-16/nemotron-cascade2-iq4xs/), [`AgentWorld evidence`](data/raw/2026-07-16/agentworld-iq4xs/) |
| Local API for tools or several clients | Qwen3-Coder 30B-A3B b9979: 228.18 aggregate t/s stock at np8; opt-in density+dense16 reached 234.12 at np9, while density alone reached 266.07 at np16 | A software dispatch cliff, not memory capacity, can limit multi-user value. Keep stock for low concurrency; advanced users should compare density Vulkan and ROCm at their exact target. | [`MOE_CONCURRENCY.md`](MOE_CONCURRENCY.md), [`summary CSV`](data/moe_density_gate_summary.csv), [`30B chart`](charts/moe_density_gate_30b.svg) |
| FP16 vLLM at 8-16 concurrent requests | Official ROCm 7.14 image, PyTorch 2.11, Qwen3-0.6B: `TORCH_BLAS_PREFER_HIPBLASLT=1` improved aggregate throughput by 40.50% / 38.96% / 41.54% at concurrency 8/9/16 | This reproduces AMD's Ryzen AI batch-8+ workaround without changing the host. It is a small-model FP16 server A/B, not a direct GGUF or 27B/35B claim; concurrency 4 was slightly slower. | [`ROCm/vLLM notes`](ROCM_VLLM_BUGWATCH.md), [`processed A/B`](data/rocm_714_hipblaslt_ab.csv), [`raw evidence`](data/raw/2026-07-16/rocm-714-vllm-hipblaslt-ab/) |
| Current ROCm/HIP `llama.cpp` compatibility | Official b10046, Qwen3-0.6B Q8_0: 4666.05 pp512 / 208.73 tg128 small-model sentinel; full 120,124 MiB free UMA detected and `ROCm_Host` buffers used | This reproduces the merged HIP integrated-device fix on Strix Halo without `HSA_OVERRIDE_GFX_VERSION`. It is compatibility/setup evidence, not a speed headline or Vulkan comparison. | [`ROCm/HIP notes`](ROCM_VLLM_BUGWATCH.md), [`raw evidence`](data/raw/2026-07-16/llamacpp-b10046-rocm-integrated-host-buffer/) |
| Long documents or codebase context | Qwen3.6 35B-A3B: 32.23 t/s decode after a filled 128K KV cache | Long-context use is possible, but prompt ingestion cost matters. | [`filled KV CSV`](data/filled_kv_decode.csv), [`chart`](charts/filled_kv_decode.svg) |
| Large-model proof point | MiniMax M2.7 230B-class MoE loaded and generated locally; Llama 4 Scout 109B measured 18.32 t/s historically | 128GB unified memory makes very large local models practical on one compact PC, but capacity and speed are different wins. | [`CURRENT_MODELS.md`](CURRENT_MODELS.md), [`benchmarks CSV`](data/benchmarks.csv) |

## Use This If You Want

| Goal | Start with | Why | Evidence |
|------|------------|-----|----------|
| Easiest private local chat | Ollama 0.31.2 system service with Vulkan/RADV | normal install path; model pulling, vision, restart/reboot persistence, and Open WebUI compatibility | 60.57 t/s fully qualified service run; controlled isolated 0.31.1/0.31.2/0.32.0 binaries later measured 72.55-73.20 t/s, [`data/benchmarks.csv`](data/benchmarks.csv) |
| Fast coding or scripts on one machine | `llama-server` Vulkan/RADV | fastest measured Qwen3.6 path at 1-4 parallel requests | [`SERVER_SHOOTOUT.md`](SERVER_SHOOTOUT.md) |
| Speculative decoding experiments | `llama-server` MTP on current master / ROCmFPX | measured server speedups on Qwen3.6 MTP GGUFs, Gemma 4 QAT matched MTP heads, and CHADROCK ROCmFP4; Qwen3.6 reached about 101.1 t/s on b9360, Gemma 4 26B-A4B QAT reached 110.0 t/s best-repeat, and the exact CHADROCK reference profile averaged 141.37 t/s over three repeats at 100% draft acceptance | [`MTP_SPECULATIVE_DECODING.md`](MTP_SPECULATIVE_DECODING.md), [`ROCMFP4_CHADROCK.md`](ROCMFP4_CHADROCK.md), [`data/mtp_speculative.csv`](data/mtp_speculative.csv) |
| Several local tools or users hitting one API | Start with stock Vulkan up to 8; above that, compare opt-in density Vulkan and Lemonade ROCm on the exact model | b9979 repeats show density recovers the Vulkan np9 cliff, but the backend winner differs between the tested 30B and 80B models | [`MOE_CONCURRENCY.md`](MOE_CONCURRENCY.md), [`data/moe_density_gate_summary.csv`](data/moe_density_gate_summary.csv) |
| Long local documents or codebase context | `llama-server` Vulkan/RADV first, test ROCm/HIP for prompt-heavy ingestion | 128K prompt plus generation completed; HIP can win prompt processing | [`data/filled_kv_decode.csv`](data/filled_kv_decode.csv), [`BACKEND_CROSSOVER.md`](BACKEND_CROSSOVER.md) |
| Prompt-heavy ROCm experiments | Keep a reproducible ROCm/HIP + ZenDNN path available, but do not treat it as a decode-speed headline. | A community Beelink GTR9 Pro on CachyOS / kernel 7.0.11 / ROCm 7.2.4 / ZenDNN measured Qwen3.6 27B MTP `UD-Q6_K_XL` at 303.20 pp5000 on ROCm versus 155.89 pp5000 on Vulkan, while decode stayed around 8 t/s on both backends. | [`BACKEND_CROSSOVER.md`](BACKEND_CROSSOVER.md#community-beelink-cachyos-rocmzendnn-crossover), [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md#beelink-gtr9-pro-cachyos-rocmzendnn-crossover) |
| NPU sidecar work | Treat the NPU as a possible low-overhead sidecar, not as a replacement for the main iGPU LLM path. | A ciru-ai GMKtec EVO-X2 NixOS artifact kept IOMMU enabled and measured only +3.29% main 64k iGPU workload latency with concurrent NPU load, versus +68.96% with a comparable iGPU auxiliary load. The same package reports FastFlowLM-NPU LFM2.5 1.2B at 32k around 1646 prompt tok/s, 38.18 decode tok/s, and about 2.09GiB RSS. | [`COMMUNITY_RESULTS.md#gmktec-evo-x2-nixos--npu--rocmfp4-evidence-package`](COMMUNITY_RESULTS.md#gmktec-evo-x2-nixos--npu--rocmfp4-evidence-package), [`data/community_ciru_evox2_metrics.csv`](data/community_ciru_evox2_metrics.csv) |
| vLLM-style serving experiments | Start with isolated ROCm containers; for ROCm 7.14 plus PyTorch before 2.14, A/B `TORCH_BLAS_PREFER_HIPBLASLT=1` at batch 8+ | The local Qwen3-0.6B FP16 A/B measured about 39-42% more aggregate throughput at concurrency 8/9/16. This validates the setting and container path, but no practical 27B/35B vLLM throughput claim exists yet. | [`processed A/B`](data/rocm_714_hipblaslt_ab.csv), [`ROCM_VLLM_BUGWATCH.md`](ROCM_VLLM_BUGWATCH.md) |
| Sustained inference on a Corsair/Sixunited AXB35 system | Verify the expected EC/fan module and dependent services after every kernel update before applying a clock cap. | A strict three-system campaign found a useful 2400 MHz fleet tradeoff, but historical journals also showed missing `ec_su_axb35` modules and failed fan services after updates. The root cause remains unresolved and the cap is not universal. | [`THERMAL_STABILITY.md`](THERMAL_STABILITY.md), [`data/community_thermal_sclk.csv`](data/community_thermal_sclk.csv) |

## Community-Tested Rules Of Thumb

These are the practical decisions extracted from the primary Beelink runs plus community reports from Corsair, GMKtec, MS-S1-Max, Nimo, a second Beelink owner stack, and a ciru-ai GMKtec EVO-X2 NixOS/NPU artifact. Use them to avoid retesting dead ends first; follow the evidence links if your setup differs.

| Situation | Do this first | Why | Evidence |
|-----------|---------------|-----|----------|
| One Strix Halo AI PC | Use Vulkan/RADV for GGUF chat, coding, and generation-heavy inference. | It is the fastest measured practical path for the main Qwen MoE rows. | [`headline claims`](data/headline_claims.csv), [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md) |
| Native Linux on another Strix Halo vendor | Expect the same performance class if backend, model, quant, and command match. | GMKtec EVO-X2 96GB on Ubuntu 26.04, Mesa RADV 26.0.3, and llama.cpp b9156 reproduced the guide's Qwen3.6 UD-Q4_K_M row within -0.8% pp512 and -1.7% tg128. | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [#16](https://github.com/hogeheer499-commits/strix-halo-guide/issues/16) |
| Comparing Qwen3-Coder rows | Preserve the exact command flags before calling one system faster. | The GMKtec Qwen3-Coder b9235 follow-up measured 91.40-92.11 tg128, but the full row used smaller batch settings, `flash_attn=0`, and `use_mmap=1`, so it is portability evidence rather than a Beelink headline replacement. | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [#17](https://github.com/hogeheer499-commits/strix-halo-guide/issues/17) |
| Handling "older model" criticism | Add current-model rows, but keep speed and capability separate. | Qwen3-Coder-Next IQ4_XS runs locally at 61.91 t/s on the Beelink with b9467. That is a useful modern coding-model result, but it does not replace the older Qwen3-Coder 30B Q4_K_S speed-first headline. | [`raw Qwen3-Coder-Next run`](data/raw/2026-06-02/modern-model-clean-followup/), [`data/benchmarks.csv`](data/benchmarks.csv) |
| Seeing a direct 100 t/s 30B-class Qwen result | Check the exact model, quant, build, and claim category before comparing. | There are now two separate first-party direct 100-class Qwen rows: Qwen3-Coder 30B-A3B `Q4_K_S` at 100.99 t/s on official b9851, and Qwen3-30B-A3B-Instruct-2507 `IQ4_XS` at 100.04 t/s on b9467 with a b9544 control at 103.18 t/s. The Qwen3-Coder row is speed-first, not the balanced default; the 2507 row is a separate general-instruct model. | [`b9851 Qwen3-Coder raw`](data/raw/2026-06-30/latest-llamacpp-b9851-vulkan-sentinel/), [`2507 raw scout`](data/raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/), [`headline claims`](data/headline_claims.csv) |
| Seeing Qwen3-Coder around 100 t/s on another Strix Halo box | Treat it as a tuned-system clue, not a default claim. Capture thermals, power policy, Vulkan device line, `glslc --version`, driver/toolchain details, and exact command. | A Reddit GMKtec EVO-X2 report saw most `Q4_K_S -p 0 -n 128` runs around 99.90 t/s and a best 100.0 t/s after repasting, reseating memory pads, and using GPU `high` plus CPU EPP `performance`. Local Beelink b9467 follow-ups stayed around 95.27-96.72 t/s, so thermals/power/toolchain still need to be separated before calling this generally reproducible. | [`COMMUNITY_RESULTS.md#reddit-gmktec-evo-x2-tuned-100-ts-report`](COMMUNITY_RESULTS.md#reddit-gmktec-evo-x2-tuned-100-ts-report), [`PERFORMANCE_NOTES.md#vulkan-integer-dot-and-100-ts-reproduction-status`](PERFORMANCE_NOTES.md#vulkan-integer-dot-and-100-ts-reproduction-status), [`raw reproduction`](data/raw/2026-06-02/reddit-look-int-dot-reproduction/) |
| Starting on Windows | LM Studio Vulkan is now a documented Windows path, but keep it separate from Linux `llama-bench`. | The first Windows MS-S1-Max report measured a 89.49 tok/s script average through LM Studio with `n_parallel=4` and 262K context; the long 512-token prompt rows were around 69-70 tok/s. This is useful Windows buyer evidence, not a same-machine Windows-vs-Linux comparison. | [`COMMUNITY_RESULTS.md#windows-lm-studio-ms-s1-max-report`](COMMUNITY_RESULTS.md#windows-lm-studio-ms-s1-max-report), [`raw Windows report`](data/raw/2026-06-02/community-windows-lmstudio-issue3/) |
| Evaluating a compact non-Beelink chassis | Look for setup metadata, thermal context, and large-model feasibility, not only headline t/s. | The Nimo AI Mini PC issue #4 bundle adds Ubuntu 25.04 / Mesa 25.2.8 / ROCm rows, Qwen 122B-class serving, StepFun 198B-class serving, Qwen3-Coder-Next server rows, DFlash negative/control evidence, Gemma 4 QAT/MTP assistant-head follow-up data, and supplemental fan/power/temperature telemetry. | [`COMMUNITY_NIMO.md`](COMMUNITY_NIMO.md), [`data/community_nimo_issue4.csv`](data/community_nimo_issue4.csv), [`raw Nimo bundle`](data/raw/2026-06-03/community-nimo-issue4/), [`Gemma QAT follow-up`](data/raw/2026-06-06/community-nimo-gemma4-qat-issue4/) |
| Choosing an IOMMU policy | Keep IOMMU enabled/default for normal systems, NPU work, and mobile suspend. Use `amd_iommu=off` only for the optional always-on desktop benchmark profile. | The Beelink headline profile preserves the measured performance route, while the safer general default avoids silently losing the NPU or deep laptop/tablet sleep. ciru-ai's GMKtec EVO-X2 NixOS artifact also shows an IOMMU-on stack where the NPU can run sidecar work with low measured main-workload impact. | [setup policy](#step-12-choose-the-iommu-policy), [`COMMUNITY_RESULTS.md#gmktec-evo-x2-nixos--npu--rocmfp4-evidence-package`](COMMUNITY_RESULTS.md#gmktec-evo-x2-nixos--npu--rocmfp4-evidence-package) |
| Testing MTP/speculative decoding | Treat MTP as an advanced server route, not a direct benchmark replacement. | The Qwen3.6 MTP IQ4_XS-Q8nextn route has a local b9360 rerun at 101.16 t/s and a GMKtec b9235 reproduction at 93.29 t/s. The Gemma 4 26B-A4B QAT route adds a current Google-model matched-head example at 102.69-110.00 t/s. The exact CHADROCK ACE/SABER reference profile averaged 141.37 t/s over three repeats at 100% acceptance, while lower-acceptance shapes were much slower. | [`MTP_SPECULATIVE_DECODING.md`](MTP_SPECULATIVE_DECODING.md), [`ROCMFP4_CHADROCK.md`](ROCMFP4_CHADROCK.md), [`data/mtp_speculative.csv`](data/mtp_speculative.csv), [#18](https://github.com/hogeheer499-commits/strix-halo-guide/issues/18) |
| The model fits on one Strix Halo box | Do not use `llama.cpp` RPC for raw single-stream speed. | 2-node RPC lost about 14-22% tg128 on fits-on-one models; 3-node was slower again. | [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md), [`data/community_rpc.csv`](data/community_rpc.csv) |
| A huge GGUF does not fit on one box | Try ROCm RPC first, starting with the smallest node count that fits. | In the tested MiniMax-M2.7 140.8GB case, one box failed, 2-node ROCm worked, and 3-node ROCm was slower. This is a capacity rule from that case, not a universal speedup rule. | [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md) |
| Testing huge MoE capacity on one box | Separate "loads and processes prompts" from "fast generation". | A Corsair AI Workstation 300 `ai-2` community row loaded MiMo-V2.5 `UD-IQ2_M`, a 310B-total / 15B-active GGUF route, and measured 30.65 pp512 with wall-power/GPU telemetry. The pasted CSV row has `n_gen=0`, so it is capacity/telemetry evidence, not a tg128 speed claim. | [`COMMUNITY_RESULTS.md#corsair-ai-workstation-300-mimo-v25-capacity-row`](COMMUNITY_RESULTS.md#corsair-ai-workstation-300-mimo-v25-capacity-row), [#26](https://github.com/hogeheer499-commits/strix-halo-guide/issues/26) |
| Building a USB4 Strix Halo cluster | Start with MTU 9000 and `pm_qos_resume_latency_us=100`. | MTU 9000 beat 1500 and 65520; `pm_qos` added about +2% tg128 with only about 1.5 W idle cost per toggled box in the community report. | [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md) |
| Choosing Qwen3.6 quantization | Use Q4_K_M/UD-Q4_K_M for balanced defaults; use Q4_0 only when speed matters more than quality. | Q4_0 was faster locally and in the Corsair report, but this guide has not made a model-quality claim for it. | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`data/community_results.csv`](data/community_results.csv) |
| Serving an interactive local API | Prefer single-box `llama-server` when the model fits. | Community `llama-server` TTFT was about 201 ms on 1 node versus about 301 ms on 2-node RPC, with higher RPC variance. | [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md), [`data/community_rpc_server.csv`](data/community_rpc_server.csv) |
| Comparing your t/s to this guide | Treat about 2% tg128 spread as normal between well-matched Strix Halo systems. | Three matched Corsair boxes showed 0.11% pp512 spread and 2.05% tg128 spread; the GMKtec native Qwen3.6 row landed within 2% of the Beelink row. | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md) |
| Estimating electricity and heat | Use wall-power rows as workload-specific context, not universal TDP. | Community wall-power data measured about 150 W / 1.6 J/token for Qwen3-Coder, 148 W / 2.0 J/token for Qwen3.6, 174 W / 3.1 J/token for gpt-oss-120b, and 137 W / 3.4 J/token for Qwen3-Coder-Next. | [`COMMUNITY_RESULTS.md#whole-system-power`](COMMUNITY_RESULTS.md#whole-system-power), [`data/community_power.csv`](data/community_power.csv) |
| Seeing a Vulkan/RADV failure on a huge MoE | Check for per-buffer allocation limits, not only total memory. | MiniMax-M2.7 hit the same 830472192-byte RADV allocation failure on 1-node and RPC follower paths. | [`data/community_rpc_failures.csv`](data/community_rpc_failures.csv), [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md) |

## Results Wanted

Have a Strix Halo / Ryzen AI MAX system? Please share results, even if they are slower, failed, or contradict this guide.

- Open a [benchmark report](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=benchmark-report.md) with your system, BIOS UMA setting, kernel, Mesa/ROCm versions, backend, model, command, CSV/raw output, and notes.
- Open a [power / efficiency report](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=power-report.md) if you can measure wall power, UPS power, or validated board power during the same benchmark command.
- Open a [model request](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=model-request.md) if there is a model/backend combination that should be tested.
- Use [Discussions](https://github.com/hogeheer499-commits/strix-halo-guide/discussions) for setup questions, comparisons, and early results that are not ready for a benchmark issue yet.
- Power telemetry is useful if you have reliable wall-power data; it helps turn raw tokens/sec into tokens-per-watt context for buying, cooling, and always-on server decisions.
- Current community reports live in [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`COMMUNITY_NIMO.md`](COMMUNITY_NIMO.md), [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md), [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md), and the `community_*` CSVs listed in [`data/README.md`](data/README.md).
- See [`SHARE.md`](SHARE.md) for short Reddit/HN/forum text and the current social preview image if you want to share the guide.

## For Vendors, Partners, And Reviewers

This guide is primarily a technical resource for AMD Strix Halo local-AI users. For vendors, reviewers, and partners, it also documents a reproducible way to reduce buyer setup friction and validate real-world local-AI use cases without weakening independent benchmark discipline.

Start with the public [vendor and reviewer overview](https://strixhaloguide.com/partners/), then inspect the linked GitHub evidence, raw artifacts, negative results, disclosure policy, and upstream contribution record here.

Start with [`ONE_PAGE_BRIEF.md`](ONE_PAGE_BRIEF.md) and [`PARTNERSHIP.md`](PARTNERSHIP.md). Supporting docs cover [`BEELINK_OUTREACH.md`](BEELINK_OUTREACH.md), [`VENDOR_OUTREACH_PLAN.md`](VENDOR_OUTREACH_PLAN.md), [`SPONSORSHIP.md`](SPONSORSHIP.md), [`VENDOR_DISCLOSURE.md`](VENDOR_DISCLOSURE.md), [`BUYER_USE_CASES.md`](BUYER_USE_CASES.md), [`SPONSOR_ROADMAP.md`](SPONSOR_ROADMAP.md), [`TRACTION.md`](TRACTION.md), and [`OUTREACH_TEMPLATES.md`](OUTREACH_TEMPLATES.md).

## Best Current Setup Tested Here

Best current AMD Strix Halo / Ryzen AI MAX+ 395 local LLM setup from this guide's measured runs. This section is the practical path; the detailed evidence is linked below.

If you are new, do this first:

1. Use Ubuntu 24.04.
2. Set BIOS UMA Frame Buffer Size to 512MB if available, or 2GB if that is your vendor minimum.
3. Keep IOMMU enabled/default if you use suspend, the NPU, RDMA, VFIO, passthrough, or clustering. On an always-on desktop benchmark box, `amd_iommu=off` remains an optional measured performance profile.
4. Use the [setup script](#setup-script) to install the Vulkan/RADV + Ollama path.
5. Start with Ollama for chat, then add [Open WebUI](#chatgpt-like-web-interface-open-webui) if you want a browser UI.
6. Move to direct `llama.cpp` only when you want exact benchmark control or the fastest measured single-box path.

The quickest sanity check after the setup script finishes is:

```bash
ollama run qwen3.6:35b-a3b
```

Expect roughly the same performance class as the guide's Ollama Vulkan/RADV rows if your BIOS, kernel parameters, Vulkan ICD, model, quant, and power profile match.

Choose the backend by what you are trying to do:

| Use case | Do this first | Why |
|----------|---------------|-----|
| You want private chat working today | Use the [setup script](#setup-script), then run `ollama run qwen3.6:35b-a3b`. | Easiest path to model pulling, local chat, and Open WebUI. |
| You want to reproduce the headline speed rows | Use [Reproduce One Headline Result](#reproduce-one-headline-result). | Exact model, quant, build, and command matter for benchmark comparisons. |
| You want a local API server or MTP tests | Read [MTP/speculative decoding](MTP_SPECULATIVE_DECODING.md) and use `llama-server`. | Supports serving, batching, long-context tests, and speculative decoding. |
| You have many parallel local requests | Read [SERVER_SHOOTOUT.md](SERVER_SHOOTOUT.md) and test Lemonade `llamacpp-rocm`. | Best measured Qwen3.6 aggregate throughput at 8-16 parallel requests. |
| You are testing prompt-heavy, vLLM, or future server paths | Read [BACKEND_CROSSOVER.md](BACKEND_CROSSOVER.md) and [VLLM_BASELINE.md](VLLM_BASELINE.md). | Useful for prompt processing, batching, vLLM, and long-context experiments. |

If you only want a working local AI PC, stop after Ollama works. If you want to compare numbers, use the exact commands and evidence links in [Reproduce One Headline Result](#reproduce-one-headline-result), the [AI/search setup summary](STRIX_HALO_LOCAL_LLM_SETUP.md), [headline claim index](data/headline_claims.csv), and raw evidence under [`data/raw/`](data/raw/).

## Headline Evidence

The machine-readable index for these rows is [`data/headline_claims.csv`](data/headline_claims.csv).

Dates below are measurement dates. A row being from May does not mean it is stale; it means later checks did not produce a stronger replacement headline. The latest controls and current-model rows are documented in [`CURRENT_MODELS.md`](CURRENT_MODELS.md), [`BENCHMARKS.md`](BENCHMARKS.md), [`PERFORMANCE_NOTES.md`](PERFORMANCE_NOTES.md), and the raw evidence links below.

| Claim | Date | Backend | Model | Result | CSV | Raw | Chart | Notes |
|-------|------|---------|-------|--------|-----|-----|-------|-------|
| Fastest direct 30B-class Qwen MoE route | 2026-06-02; b9544 control 2026-06-07 | llama.cpp Vulkan/RADV b9467; b9544 | Qwen3-30B-A3B-Instruct-2507 IQ4_XS | 100.04 tg128 r50, 1416.03 pp512; b9544 control 103.18 tg128 r10 | [`benchmarks`](data/benchmarks.csv) | [`raw r50`](data/raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/qwen3-30b-2507-iq4xs-b9467-r50.csv), [`b9544 control`](data/raw/2026-06-07/latest-llamacpp-b9544-regression/) | n/a | first local direct `llama-bench` row above 100 t/s; separate general-instruct Qwen route; not the Qwen3-Coder headline or balanced default |
| Fastest current small-MoE scout | 2026-06-05; b9544 control 2026-06-07 | llama.cpp Vulkan/RADV 2016bf2; b9544 | LFM2.5 8B-A1B Q4_K_M | 168.96 tg128, 3414.61 pp512; generation-only 170.02 tg128; b9544 control 176.48 tg128 r10 | [`benchmarks`](data/benchmarks.csv) | [`raw latest/int-dot`](data/raw/2026-06-05/latest-llamacpp-intdot-regression/), [`b9544 control`](data/raw/2026-06-07/latest-llamacpp-b9544-regression/) | n/a | small active-parameter MoE speed/currentness row; not a 30B-class model replacement |
| Largest current direct GGUF capacity route | 2026-07-16 | llama.cpp Vulkan/RADV b10034 | DeepSeek V4 Flash 284B UD-IQ2_XXS | 155.64 pp512 / 13.27 tg128 r3; deterministic answer `9` | [`benchmarks`](data/benchmarks.csv) | [`raw direct pass`](data/raw/2026-07-16/deepseek-v4-flash-ud-iq2-xxs/) | n/a | pinned 90.86GB ordinary GGUF; direct load/basic-correctness capacity proof, not a speed or broad quality recommendation |
| Current 120B-class direct GGUF route | 2026-06-05; b9544 control 2026-06-07 | llama.cpp Vulkan/RADV 2016bf2; b9544 | Nemotron 3 Super 120B-A12B UD-IQ4_XS | 18.43 tg128, 294.99 pp512; b9544 control 18.93 tg128 r3 | [`benchmarks`](data/benchmarks.csv) | [`raw latest/int-dot`](data/raw/2026-06-05/latest-llamacpp-intdot-regression/), [`b9544 control`](data/raw/2026-06-07/latest-llamacpp-b9544-regression/) | n/a | direct 120B-class MoE route on one 128GB Strix Halo system; capacity/current-model proof, not a speed headline |
| Fastest measured short-context coding MoE speed-first quant | 2026-06-30 | llama.cpp Vulkan/RADV b9851 official release binary | Qwen3-Coder 30B-A3B Q4_K_S | 100.99 tg128 r50, 1423.05 pp512 | [`benchmarks`](data/benchmarks.csv) | [`raw r50`](data/raw/2026-06-30/latest-llamacpp-b9851-vulkan-sentinel/qwen3-coder-q4ks-b9851-p512-n128-r50.csv) | n/a | speed-first lower-quality quant; not the balanced UD default; older b9179 strict-clean row remains preserved at 98.51 t/s |
| Fast balanced short-context coding MoE | 2026-05-07 | llama.cpp Vulkan/RADV b9049 | Qwen3-Coder 30B-A3B UD-Q4_K_XL | 96.76 tg128, 1320.52 pp512 | [`max campaign`](data/max_performance_campaign.csv) | [`raw run`](data/raw/2026-05-07/max-performance-campaign/benchmarks/qwen3-coder-top-confirm-r20/guide.csv) | n/a | max-performance r20 confirmation; previous b9010 peak was 97.24 t/s |
| Default Qwen3.6 direct path | 2026-05-07 | llama.cpp Vulkan/RADV b9049 | Qwen3.6 35B-A3B UD-Q4_K_M | 62.56 tg128, 1059.45 pp512 | [`benchmarks`](data/benchmarks.csv) | [`raw run`](data/raw/2026-05-07/latest-stack-rerun/clean-b9049-rerun/qwen36-35b-b9049-clean-r20.csv) | [`chart`](charts/backend_spot_check.svg) | clean latest-stack r20 rerun; rounds to 63 t/s |
| Fastest measured Qwen3.6 speed-first quant | 2026-05-07 | llama.cpp Vulkan/RADV b9049 | Qwen3.6 35B-A3B Q4_0 | 81.30 tg128, 1243.51 pp512 | [`max campaign`](data/max_performance_campaign.csv) | [`raw run`](data/raw/2026-05-07/max-performance-campaign/benchmarks/qwen36-top-confirm-r20/q4-0-ub2048.csv) | n/a | speed-first lower-quality quant; not the default all-round recommendation without a quality sanity check |
| Current normal Ollama buyer path | 2026-07-10 | Ollama 0.31.2 system service Vulkan/RADV | Qwen3.6 35B-A3B Q4_K_M | 60.57 t/s warm API generation average | [`benchmarks`](data/benchmarks.csv) | [`raw service run`](data/raw/2026-07-10/ollama-0312-buyer-path/) | n/a | normal service-upgrade path; iGPU, vision, service restart, and full-host reboot persistence passed; later controlled local binaries did not reproduce a version-wide slowdown |
| Experimental Qwen3.6 MTP server path | 2026-05-27 | `llama-server` Vulkan/RADV b9360 | Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn | 101.16 t/s best local average over six prompts; t16 repeats at 101.15 / 101.10 / 101.06 t/s; 93.29 t/s GMKtec community average on b9235 | [`MTP CSV`](data/mtp_speculative.csv) | [`local raw`](data/raw/2026-05-27/latest-llamacpp-b9360/), [`GMKtec raw`](data/raw/2026-05-19/community-gmktec-mtp-issue18/) | n/a | server/speculative result; localweights Q8-next-token-head quant; not the direct `llama-bench` headline |
| Experimental Gemma 4 QAT MTP server path | 2026-06-12 | `llama-server` Vulkan/RADV ac4cddeb0 | Gemma 4 26B-A4B IT QAT UD-Q4_K_XL + Q4_0 MTP head | 102.69 t/s cold repeat; 107.42 t/s T3-only repeat; 110.00 t/s best repeat; 73.96 t/s no-spec baseline | [`MTP CSV`](data/mtp_speculative.csv) | [`cold raw`](data/raw/2026-06-12/gemma4-26b-qat-mtp-cold-repeat-ac4cddeb/), [`T3-only raw`](data/raw/2026-06-12/gemma4-26b-qat-mtp-t3-only-repeat-ac4cddeb/), [`warm raw`](data/raw/2026-06-11/gemma4-26b-qat-mtp-sixprompt-ac4cddeb/) | n/a | server/speculative result with matched QAT MTP head; current Google model route; host-workload sensitive; not direct `llama-bench` |
| Experimental CHADROCK ROCmFP4 MTP server path | 2026-06-21 | `llama-server` ROCmFPX/RADV helper route | CHADROCK ACE/SABER 35B ROCmFP4 | 140.40 and 139.93 t/s gen512 high-acceptance repeats; 127.77 t/s gen2048 check | [`MTP CSV`](data/mtp_speculative.csv) | [`raw helper repro`](data/raw/2026-06-21/rocmfpx-chadrock-ace-saber-helper-repro/) | n/a | server/speculative result with `ciru-ai/ROCmFPX`; prompt/acceptance-sensitive; not direct `llama-bench` |
| Best current 80B Qwen-family path | 2026-05-16 | llama.cpp Vulkan/RADV b9172 | Qwen3-Next 80B-A3B UD-Q4_K_XL | 59.06 tg128, 751.70 pp512 | [`benchmarks`](data/benchmarks.csv) | [`raw r20`](data/raw/2026-05-16/latest-stack-b9172/qwen3-next-confirm-r20/qwen3-next-80b-b9172-ub1024-r20.csv) | n/a | b9172 improved this 80B MoE path versus the older 54.92 t/s b8933 row |
| gpt-oss-120b loaded locally | 2026-05-07 | llama.cpp Vulkan/RADV b9049 | gpt-oss-120b MXFP4 split GGUF | 55.57 tg128, 726.99 pp512, 293.73 pp65536 r1 | [`max campaign`](data/max_performance_campaign.csv) | [`raw run`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/) | n/a | performance evidence only; no model-quality eval; pp65536 is one repeat |
| User-local Ollama comparator | 2026-07-02 | Ollama 0.31.1 local binary Vulkan/RADV | Qwen3.6 35B-A3B Q4_K_M | 71.82 t/s warm API generation average | [`benchmarks`](data/benchmarks.csv) | [`raw API run`](data/raw/2026-07-02/ollama-0311-qwen36-buyer-path/) | n/a | 9 warm API runs after one cold run; required `OLLAMA_IGPU_ENABLE=1`; faster than the earlier normal-service check, but a later controlled comparison found no version-wide 0.31.2 regression |
| Best measured Qwen3.6 server split | 2026-05-05 | Vulkan/RADV and Lemonade ROCm | Qwen3.6 35B-A3B UD-Q4_K_M | Vulkan wins 1-4 parallel; Lemonade ROCm wins 8-16 | [`server data`](data/server_shootout.csv) | [`raw sweep`](data/raw/2026-05-05/server-shootout/full-sweep-qwen36-workstation-baseline/summary.csv) | n/a | 5 reps per concurrency, 0 errors |
| HIP/Vulkan workload split | 2026-05-07 | Vulkan/RADV and ROCm/HIP from b9049 source | Qwen3.6 35B-A3B, Qwen3-Coder 30B-A3B | HIP won pp16384; Vulkan won tg128 on both local Qwen rows | [`max campaign`](data/max_performance_campaign.csv) | [`same-source matrix`](data/raw/2026-05-07/max-performance-campaign/benchmarks/same-build-hip-vulkan-b9049/) | n/a | HIP binary reports unknown build id due container git safe-directory, but source checkout was b9049 |
| Best measured Qwen3-Coder local API point | 2026-05-03 | `llama-server` Vulkan/RADV b9010 | Qwen3-Coder 30B-A3B UD-Q4_K_XL | 173.16 aggregate t/s at `-np 8` | [`multi-user`](data/multi_user.csv) | [`raw summary`](data/raw/2026-05-03/multi-user-coder/qwen3-coder-30b-ud-llama-server-multi-user-summary.csv) | [`chart`](charts/multi_user_aggregate.svg) | `-np 16` regressed |
| 128K filled-context Qwen3.6 decode completed | 2026-05-03 | `llama-server` Vulkan/RADV b9010 | Qwen3.6 35B-A3B UD-Q4_K_M | 32.23 t/s decode after 128K fill, no truncation | [`filled KV`](data/filled_kv_decode.csv) | [`raw 128K summary`](data/raw/2026-05-03/filled-kv-decode-128k/filled-kv-decode-128k-summary.csv) | [`chart`](charts/filled_kv_decode.svg) | f16 KV, synthetic long prompt |
| Real documents are slower than synthetic repeated prompts | 2026-05-03 | `llama-server` Vulkan/RADV b9010 | Qwen3.6 35B-A3B and Qwen3-Next 80B-A3B | real 64K prompt ingest was 24-33% slower; decode barely changed | [`filled KV`](data/filled_kv_decode.csv) | [`real-corpus summary`](data/raw/2026-05-03/filled-kv-decode-real-corpus/filled-kv-decode-real-corpus-summary.csv) | [`chart`](charts/real_vs_synthetic.svg) | avoids overclaiming synthetic prompt speed |

## Reproduce One Headline Result

Pick the row that matches what you want to verify. The balanced coding row is the best first reproduction target for most users. The direct 100 t/s row is useful if you specifically want to verify the fastest measured 30B-class Qwen speed scout. Keep them separate: they use different model files, quants, builds, and quality tradeoffs.

### Balanced Qwen3-Coder Row

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
~/llama-cpp-upstream-2026-05-07/build-vulkan/bin/llama-bench \
  -m ~/models/Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf \
  -fa 1 -ngl 999 -mmp 0 -p 0 -n 128 -r 20 -o csv
```

Measured local result: 96.76 tg128 in the max-performance b9049 campaign: [`raw CSV`](data/raw/2026-05-07/max-performance-campaign/benchmarks/qwen3-coder-top-confirm-r20/guide.csv). This is the practical balanced Qwen3-Coder row. The fastest first-party Qwen3-Coder row is now 100.99 tg128 with Q4_K_S on the official b9851 Vulkan release binary, but that is a speed-first quant rather than the balanced default: [`raw b9851 r50`](data/raw/2026-06-30/latest-llamacpp-b9851-vulkan-sentinel/qwen3-coder-q4ks-b9851-p512-n128-r50.csv). The older b9179 strict-clean 98.51 t/s row remains preserved for historical host-state context: [`raw b9179 r50`](data/raw/2026-05-16/break-97-24-strict-noise-settings/b9179-q4-k-s-r50.csv).

### Direct 100 t/s Qwen3 30B Speed Scout

Use this only if you have the exact `Qwen3-30B-A3B-Instruct-2507` `IQ4_XS-3.63bpw` GGUF and a comparable b9467 Vulkan/RADV build. Adjust the binary and model paths to your checkout; the flags, model hash, build, and raw CSV are the reproducibility anchors. This is a direct `llama-bench` result, but it is not Qwen3-Coder and not the balanced default.

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
~/llama-cpp-b9467/build-vulkan/bin/llama-bench \
  -m ~/models/Qwen3-30B-A3B-Instruct-2507-IQ4_XS-3.63bpw.gguf \
  -fa 1 -ngl 999 -mmp 0 -b 2048 -ub 512 -t 16 --poll 50 -p 512 -n 128 -r 50 -o csv
```

Measured local result: 100.04 tg128 and 1416.03 pp512 on the r50 confirmation: [`raw r50`](data/raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/qwen3-30b-2507-iq4xs-b9467-r50.csv), [`model hash`](data/raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/model-iq4xs.sha256), [`scout notes`](data/raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/README.md).

## Not Yet Proven Here

- A first-party Beelink wall-power tokens-per-watt claim. Local amdgpu `PPT` telemetry exists, and community Corsair wall-power rows exist, but the guide still needs a Beelink wall-meter run before publishing Beelink J/token claims.
- Same-machine Windows versus Linux performance. Windows LM Studio and WSL2/HIP community rows now exist, but they are not same-machine, same-model, same-shape comparisons against native Linux Vulkan/RADV.
- A default or balanced first-party 100 t/s Qwen3-Coder claim. The first-party Qwen3-Coder `Q4_K_S` speed-first row now reaches 100.99 t/s on b9851, but the practical balanced `UD-Q4_K_XL` row remains in the 96-99.6 t/s class depending on build/repeat length. A tuned community GMKtec report touched 100.0 t/s on Qwen3-Coder, and a separate first-party Qwen3-30B-A3B-Instruct-2507 IQ4_XS route reached 100.04 t/s, but those are separate evidence categories.
- Production-ready NPU/FastFlowLM inference. The kernel sees `amdxdna` and `/dev/accel/accel0`, but XRT/FastFlowLM user-space is not installed and no local NPU LLM row is published yet.
- A broadly useful DFlash/PFlash speedup on Strix Halo. The official Gemma 4 31B QAT target and matched DFlash sidecar now load and serve on b10066, but DFlash `n_max=8` was 5.54% slower at 5,471 prompt tokens and 20.42% slower at 21,855 on the measured synthetic shapes because acceptance stayed low. Representative chat, coding, and reasoning prompts still need separate profiling.
- A vLLM/DFlash server path that competes with `llama-server` or Ollama for a real 35B Strix Halo use case. Plain AWQ without the gated DFlash drafter was only a smoke test here at about 25 t/s.
- A local tuned rocWMMA long-context comparison against the current Vulkan/RADV path. External rocWMMA evidence exists, but the local lhl branch built here failed to load the current Qwen3.6 GGUFs.
- Multi-machine clustering numbers from this guide's own hardware. Community RPC and USB4 tuning data exists in [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md) and [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md), but it is not a local Beelink headline claim.

## Do Not Copy These Claims Without Matching Setup

These numbers are local measurements from one primary machine: a Beelink GTR9 Pro with Ryzen AI MAX+ 395 and 128GB LPDDR5X-8000. Treat the headline results as directional unless your setup matches the measured run closely.

Performance depends on the exact hardware SKU, RAM configuration, BIOS UMA setting, IOMMU setting, firmware, kernel, Mesa/RADV version, ROCm version, Vulkan ICD selection, power profile, GPU clocks, thermal state, backend commit/build flags/container image, model file, quant type, model hash/path, context length, prompt length, generated token count, batch size, parallel slots, request concurrency, API endpoint, environment variables, and background system load.

If your setup differs, rerun the benchmark scripts and cite the date, command, CSV, raw log, chart, model file, and backend version with any copied claim.

## Documentation Map

| File | Purpose |
|------|---------|
| [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) | Exact machine, BIOS/software state, commands, raw data paths, and chart generation. |
| [`SERVER_SHOOTOUT.md`](SERVER_SHOOTOUT.md) | Practical local-AI-server comparison: Ollama, `llama-server`, Lemonade ROCm, and vLLM candidates. |
| [`BACKEND_CROSSOVER.md`](BACKEND_CROSSOVER.md) | HIP versus Vulkan workload split: prompt processing versus token generation. |
| [`POWER_BASELINE.md`](POWER_BASELINE.md) | Local amdgpu `PPT` telemetry status and Beelink power-sampling caveats. |
| [`PERFORMANCE_NOTES.md`](PERFORMANCE_NOTES.md) | Narrow notes on strict-stack reruns, failed headline reproduction attempts, and useful negative model results. |
| [`CURRENT_MODELS.md`](CURRENT_MODELS.md) | Current-model triage: latest model scouts, speed versus capability framing, and practical next-test value. |
| [`UNSLOTH_STRIX_HALO.md`](UNSLOTH_STRIX_HALO.md) | Measured local fine-tuning, GGUF export, ROCm deployment, persistence, and troubleshooting path. |
| [`data/current_test_queue.csv`](data/current_test_queue.csv) | Machine-readable current test priorities, readiness, artifact size, blockers, and evidence questions. |
| [`ROCM_VLLM_BUGWATCH.md`](ROCM_VLLM_BUGWATCH.md) | Fast-moving ROCm/vLLM upstream issue and release watchlist. |
| [`BENCHMARKS.md`](BENCHMARKS.md) | Compact benchmark source-of-truth for current README numbers. |
| [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md) | Independent benchmark reports from other Strix Halo systems, kept separate from headline claims. |
| [`COMMUNITY_FEEDBACK.md`](COMMUNITY_FEEDBACK.md) | Community feedback loop: trust friction, public corrections, and how criticism turns into reproducible evidence. |
| [`COMMUNITY_NIMO.md`](COMMUNITY_NIMO.md) | Nimo AI Mini PC community bundle with large-model, MTP, StepFun, Qwen 122B, Gemma 4 QAT/MTP assistant-head, and thermal context. |
| [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md) | Community multi-node `llama.cpp` RPC over USB4 results, kept separate from single-machine headline claims. |
| [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md) | Community USB4 latency tuning for active Strix Halo cluster nodes. |
| [`THERMAL_STABILITY.md`](THERMAL_STABILITY.md) | Scoped Corsair/Sixunited sustained-inference evidence: SCLK tradeoffs, bounded stock controls, fan-module/service checks, raw telemetry, and upstream safety work. |
| [`ROCMFP4_CHADROCK.md`](ROCMFP4_CHADROCK.md) | Advanced ROCmFP4 / CHADROCK tuned-GGUF route tracking. The exact first-party reference profile averaged 141.37 t/s across three repeats at 100% acceptance, but other prompt shapes were much slower; it is not the beginner/default setup path or a direct `llama-bench` replacement. |
| [`UPSTREAM_CONTRIBUTIONS.md`](UPSTREAM_CONTRIBUTIONS.md) | Accepted upstream engineering work in `llama.cpp`, LocalAI, Qwen Code, OpenTelemetry GenAI, NVIDIA AICR, and vLLM GGUF tooling, with direct review links and claim boundaries. |
| [`CONTRIBUTORS.md`](CONTRIBUTORS.md) | Community benchmark contributor credits and contribution path. |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | What data is most useful, which issue template to use, and how community reports become structured evidence. |
| [`data/headline_claims.csv`](data/headline_claims.csv) | Machine-readable map from public headline claims to data, raw evidence, charts, and notes. |
| [`data/README.md`](data/README.md) | Structured CSV schema and raw-data conventions. |
| [`charts/README.md`](charts/README.md) | Generated chart inventory and regeneration command. |
| [`SHARE.md`](SHARE.md) | Copyable Reddit/HN/forum/Discord text and share links. |
| [`SECURITY.md`](SECURITY.md) | Official-source and impersonation reporting policy. |
| [`SUPPORT.md`](SUPPORT.md) | How to support ongoing testing without changing the evidence-first benchmark policy. |
| [`ONE_PAGE_BRIEF.md`](ONE_PAGE_BRIEF.md), [`PARTNERSHIP.md`](PARTNERSHIP.md), [`SPONSORSHIP.md`](SPONSORSHIP.md), [`VENDOR_DISCLOSURE.md`](VENDOR_DISCLOSURE.md) | Vendor/partner-facing explanation of how the technical proof layer reduces buyer adoption friction while preserving independence. |
| [`BUYER_USE_CASES.md`](BUYER_USE_CASES.md), [`SPONSOR_ROADMAP.md`](SPONSOR_ROADMAP.md), [`TRACTION.md`](TRACTION.md), [`BEELINK_OUTREACH.md`](BEELINK_OUTREACH.md), [`VENDOR_OUTREACH_PLAN.md`](VENDOR_OUTREACH_PLAN.md), [`OUTREACH_TEMPLATES.md`](OUTREACH_TEMPLATES.md) | Buyer-use-case, roadmap, public-evidence, and outreach support docs. |

## Table of Contents

- [20-Second Summary](#20-second-summary)
- [Use This Guide If](#use-this-guide-if)
- [Quick Start (6 Steps)](#quick-start-6-steps)
- [Setup Script](#setup-script)
- [What You Can Run: Quick Snapshot](#what-you-can-run-quick-snapshot)
- [Use This If You Want](#use-this-if-you-want)
- [Community-Tested Rules Of Thumb](#community-tested-rules-of-thumb)
- [Results Wanted](#results-wanted)
- [Community Results](COMMUNITY_RESULTS.md)
- [Best Current Setup Tested Here](#best-current-setup-tested-here)
- [Headline Evidence](#headline-evidence)
- [Reproduce One Headline Result](#reproduce-one-headline-result)
- [Not Yet Proven Here](#not-yet-proven-here)
- [Do Not Copy These Claims Without Matching Setup](#do-not-copy-these-claims-without-matching-setup)
- [Documentation Map](#documentation-map)
- [Hardware](#hardware)
- [What You Can Run](#what-you-can-run)
- [Benchmark Results](#benchmark-results)
  - [Benchmark Charts](#benchmark-charts)
  - [Ollama Vulkan (RADV)](#ollama-vulkan-radv)
  - [llama-server Multi-User Serving](#llama-server-multi-user-serving-b9010)
  - [ROCm HIP (llama.cpp)](#rocm-hip-llamacpp)
  - [Backend Comparison](#backend-comparison-table)
  - [Hardware Comparison](#hardware-comparison)
  - [Long Context Performance](#long-context-performance)
- [Backend Decision Guide](#backend-decision-guide)
- [Server Shootout](SERVER_SHOOTOUT.md)
- [Phase 1: BIOS Configuration](#phase-1-bios-configuration)
- [Phase 2: Ubuntu 24.04 Installation](#phase-2-ubuntu-2404-installation)
- [Phase 3: Kernel Configuration](#phase-3-kernel-configuration)
- [Phase 4: Performance Tuning](#phase-4-performance-tuning)
- [Phase 5: Ollama Setup (Vulkan)](#phase-5-ollama-setup-vulkan)
- [Phase 6: Benchmarking](#phase-6-benchmarking)
- [Phase 7: ROCm with llama.cpp (Containers)](#phase-7-rocm-with-llamacpp-containers)
- [Phase 8: vLLM Serving](#phase-8-vllm-serving)
- [Phase 9: Multi-Node Clustering (RDMA)](#phase-9-multi-node-clustering-rdma)
- [Phase 10: SSH and Remote Access](#phase-10-ssh-and-remote-access)
- [Vulkan Driver Comparison](#vulkan-driver-comparison)
- [Key Findings and Corrections](#key-findings-and-corrections)
- [Known Issues](#known-issues)
- [Troubleshooting](#troubleshooting)
- [Kernel and ROCm Compatibility](#kernel-and-rocm-compatibility)
- [Power Measurement Status](#power-measurement-status)
- [Testing Checklist](#testing-checklist)
- [Model Recommendation Guide](#model-recommendation-guide)
- [Cost: Local vs Cloud](#cost-local-vs-cloud)
- [Buying Guide](#buying-guide)
- [Glossary](#glossary)
- [FAQ](#faq)
- [Community Resources](#community-resources)
- [Credits and References](#credits-and-references)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [License](#license)

---

## Hardware

### Evidence Coverage: 11 Systems Or Independent Sources

The count includes separately measured owner systems or independently sourced reports, not eleven unique product models. This makes the public `11 systems/sources` claim auditable without treating every row as an equal-quality benchmark.

| Evidence source | Systems/sources counted | Running total | Evidence |
|-----------------|------------------------:|--------------:|----------|
| Primary Beelink GTR9 Pro | 1 | 1 | First-party raw evidence throughout this repository |
| Corsair AI Workstation 300 fleet | 3 | 4 | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`THERMAL_STABILITY.md`](THERMAL_STABILITY.md), [`data/community_results.csv`](data/community_results.csv) |
| GMKtec EVO-X2 native contributor system | 1 | 5 | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`data/raw/2026-05-14/community-gmktec-native-issue16/`](data/raw/2026-05-14/community-gmktec-native-issue16/) |
| GMKtec EVO-X2 tuned Reddit report | 1 | 6 | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`raw note`](data/raw/2026-06-02/community-reddit-look-qwen-coder/) |
| Minisforum MS-S1-Max | 1 | 7 | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`raw report`](data/raw/2026-06-02/community-windows-lmstudio-issue3/) |
| Nimo AI Mini PC | 1 | 8 | [`COMMUNITY_NIMO.md`](COMMUNITY_NIMO.md) |
| Second Beelink GTR9 Pro owner stack | 1 | 9 | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`raw report`](data/raw/2026-06-12/community-devoidfury-cachyos-rocm-zendnn/) |
| ciru-ai GMKtec EVO-X2 NixOS/NPU artifact | 1 | 10 | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`source artifact`](https://github.com/ciru-ai/strix-halo-evo-x2-evidence) |
| Minix Elite ER939 Ai | 1 | **11** | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`raw report`](data/raw/2026-06-24/community-minix-er939-ollama-issue27/) |

### Hardware Context

This table is a product/context map, not an endorsement list or the source of the eleven-system count above. Rows without linked community evidence are useful hardware context only.

| System | CPU | GPU | RAM | Notes |
|--------|-----|-----|-----|-------|
| **Beelink GTR9 Pro** | Ryzen AI MAX+ 395 | Radeon 8060S (40 CU) | 128GB LPDDR5X-8000 | This guide's primary test system |
| Corsair AI Workstation 300 | Ryzen AI MAX+ 395 | Radeon 8060S (40 CU) | 128GB LPDDR5X-8000 | Three community systems reproduced the Qwen3-Coder path |
| Framework Desktop | Ryzen AI MAX+ 395 | Radeon 8060S (40 CU) | 128GB LPDDR5X-8000 | Used by kyuz0, lhl |
| GMKtec EVO-X2 | Ryzen AI MAX+ 395 | Radeon 8060S (40 CU) | 96GB or 128GB LPDDR5X-8000 | Native 96GB community run reproduced the Qwen3.6 row; a separate tuned Reddit GMKtec report touched 100.0 t/s on Qwen3-Coder `Q4_K_S`; [pablo-ross guide](https://github.com/pablo-ross/strix-halo-gmktec-evo-x2) |
| Minisforum MS-S1-Max | Ryzen AI MAX+ 395 | Radeon 8060S (40 CU) | 128GB LPDDR5X | Windows LM Studio community serving report imported; not a same-shape Linux comparison |
| Nimo AI Mini PC | Ryzen AI MAX+ 395 | Radeon 8060S (40 CU) | 128GB LPDDR5X | Community issue #4 bundle imported; adds compact-chassis large-model serving, MTP, StepFun/Qwen 122B, Gemma 4 QAT/MTP assistant-head follow-up data, and thermal context |
| HP ZBook Ultra G1a | Ryzen AI MAX+ 395 | Radeon 8060S (40 CU) | 128GB LPDDR5X-8000 | Workstation laptop |

### Strix Halo Specs

| Component | Spec |
|-----------|------|
| CPU | AMD Ryzen AI MAX+ 395 (16 cores / 32 threads, Zen 5) |
| GPU | Radeon 8060S (gfx1151, RDNA 3.5, 40 CUs) |
| RAM | 96GB or 128GB unified LPDDR5X-8000 depending on vendor; primary measured system is 128GB (~215 GB/s measured, 256 GB/s theoretical) |
| NPU | RyzenAI-npu5 (XDNA 2) |

> **Why this hardware?** 96GB/128GB unified memory shared between CPU and GPU means you can run **70B+ models entirely on the GPU** -- something an RTX 4090 (24GB VRAM) cannot do. You trade raw bandwidth (~215 GB/s vs ~1 TB/s on this Beelink) for the ability to run much larger, smarter models on one compact machine. Price changes quickly by vendor; check the [Buying Guide](#buying-guide) before making a purchase decision.

---

## What You Can Run

Real-world generation speeds measured on the Beelink GTR9 Pro, primarily with Vulkan/RADV. Speeds marked with * are via `llama-bench` direct; others are via Ollama unless noted. Use this table to choose a first model, then follow the evidence links above before copying a benchmark claim.

| Model | Size | Type | Generation Speed | Use Case |
|-------|------|------|------------------|----------|
| Qwen3-0.6B (Q8_0) | 0.8 GB | Dense | 266 t/s * | Ultra-fast tiny model |
| Llama 2 7B | 3.8 GB | Dense | 48-52 t/s | Testing, lightweight tasks |
| Qwen2.5-VL 7B | 6.0 GB | Vision | 21.4 t/s | Image understanding |
| LFM2.5-VL 1.6B (Q4_0) | 1.19 GB with projector | Vision | functional local pass | Lightweight official-GGUF image route; one-image smoke, not a speed/quality headline |
| Qwen3-ASR 0.6B (Q8_0) | 0.95 GB with projector | Speech | functional local pass | Short offline English transcription; experimental audio path |
| LFM2.5 8B-A1B (Q4_K_M) | 5.1 GB | MoE | **170.0 t/s** * | Fastest current small-MoE scout; not a 30B-class replacement |
| Gemma 4 26B-A4B IT QAT (UD-Q4_K_XL) | 14.2 GB | MoE | **74.8 t/s** direct; **102.7-110.0 t/s** MTP server | Current practical Google-model route; direct row is `llama-bench`, MTP row is server/speculative |
| Qwen3-30B-A3B-Instruct-2507 (IQ4_XS) | 13.9 GB | MoE | **100.0 t/s** * | Fastest direct 30B-class Qwen row; general-instruct route, not Qwen3-Coder |
| Qwen3-Coder 30B-A3B (Q4_K_S) | 17.5 GB | MoE | **101.0 t/s** * | Fastest measured coding speed; speed-first quant, not the balanced default |
| Qwen3-Coder 30B-A3B (UD-Q4_K_XL) | 17.7 GB | MoE | **97 t/s** * | Best coding-model speed/quality ratio; current b9049 measured 96.76 t/s and previous b9010 peak was 97.24 t/s |
| Qwen3.6 35B-A3B (Q4_0) | 19.7 GB | MoE | **81 t/s** * | Fastest measured Qwen3.6 speed-first quant; use a balanced quant if quality matters more than raw speed |
| Qwen3.6 35B-A3B (Q4_K_M / UD-Q4_K_M) | 20-22 GB | MoE | **63 t/s** * | Best all-rounder balanced direct path; separate speed-first/alternate quants reach higher but need quality sanity |
| Qwen3.5 35B-A3B | 23 GB | MoE | 48-**65 t/s** | General purpose, coding (65 with measured direct llama.cpp builds) |
| Qwen3-Coder 30B-A3B (Q8_0) | 32 GB | MoE | 51 t/s | Coding (highest quality MoE) |
| Qwen3-Coder-Next | 51 GB | Dense | 38-39 t/s | Large dense model |
| Llama 3.1 70B (Q4_K_M) | 42 GB | Dense | **4.7-4.9 t/s** | 70B intelligence, doesn't fit on RTX 4090 |
| Llama 4 Scout 109B (Q4_K_M) | 61 GB | MoE | **18.3 t/s** * | 109B params on a mini PC -- RTX 4090 can't even load this |
| Nemotron 3 Nano 30B-A3B (IQ4_XS) | 18.2 GB | MoE | **76.0 t/s** * | Practical NVIDIA Nemotron 30B-class route |
| DeepSeek V4 Flash 284B (UD-IQ2_XXS) | 90.9 GB | MoE | **13.3 t/s** * | Largest current direct ordinary-GGUF capacity proof; low-bit quant, not a quality recommendation |
| Nemotron 3 Super 120B-A12B (UD-IQ4_XS) | 64.5 GB | MoE | **18.4 t/s** * | Current 120B-class GGUF route on one 128GB Strix Halo |
| gpt-oss-120b MXFP4 | 63.4 GB | MoE | **55.6 t/s** * | 117B-parameter open-weight model; local load and long-context speed check |
| Qwen3-Next 80B-A3B (UD-Q4_K_XL) | 42.9 GB | MoE | **59 t/s** * | 80B model, 256K context -- faster than dense 51B |
| Kimi K2.5 1T (4-node cluster) | ~500 GB | MoE | distributed | [AMD technical article](https://www.amd.com/en/developer/resources/technical-articles/2026/how-to-run-a-one-trillion-parameter-llm-locally-an-amd.html) |

---

## Benchmark Results

Benchmarks below were run on 2026-03-20, 2026-03-21, 2026-04-26, 2026-05-03, 2026-05-07, 2026-05-16, 2026-05-26, 2026-05-27, 2026-05-31, 2026-06-01, 2026-06-02, 2026-06-05, 2026-06-07, 2026-06-11, 2026-06-12, 2026-06-21, 2026-06-30, and 2026-07-02. Primary benchmark system: Beelink GTR9 Pro. Recorded local runs used kernel 6.19.4, Mesa RADV 26.0.2-26.1.3 where captured, AMDVLK removed, and `tuned` `accelerator-performance` where captured; individual raw directories and CSV rows are the source of truth for exact run metadata, and some older or scout rows intentionally record missing metadata as `not recorded`. Before running new benchmarks, verify `tuned-adm active` and keep `power-profiles-daemon` inactive; it can conflict with `tuned`.

These rows are included because they answer practical setup questions: which model to try first, which backend removes the most friction, which paths are only experimental, and which results are strong enough to cite.

### Benchmark Charts

These generated SVGs summarize the current structured benchmark data. The CSV files in `data/` and raw logs in `data/raw/` remain the source of truth; regenerate charts with `python3 scripts/generate_charts.py`.

| Multi-user serving | Long-context prompt scaling |
|--------------------|-----------------------------|
| <img src="charts/multi_user_aggregate.svg" alt="llama-server multi-user aggregate throughput chart" width="455"> | <img src="charts/long_context_prompt.svg" alt="long-context prompt processing chart" width="455"> |

| Filled-KV decode | KV-cache quantization tradeoff |
|------------------|-------------------------------|
| <img src="charts/filled_kv_decode.svg" alt="decode speed after filled KV cache chart" width="455"> | <img src="charts/kv_cache_tradeoff.svg" alt="Qwen3.6 KV-cache quantization tradeoff chart" width="455"> |

| Real versus synthetic prompts | Backend spot check |
|-------------------------------|--------------------|
| <img src="charts/real_vs_synthetic.svg" alt="real documentation corpus versus synthetic prompt chart" width="455"> | <img src="charts/backend_spot_check.svg" alt="Vulkan RADV versus ROCm HIP spot check chart" width="455"> |

### Ollama Vulkan (RADV)

**Qwen3.6-35B-A3B** (Q4_K_M, ~20-23GB, MoE):

| Prompt Tokens | Prompt Eval | Generation | Notes |
|---------------|-------------|------------|-------|
| 25 | 944 t/s | **71.8 t/s** | 2026-07-02 user-local Ollama 0.31.1 binary sanity check; required `OLLAMA_IGPU_ENABLE=1`; 9-run warm average after one cold run |
| 19 | 158 t/s | **50.5 t/s** | Controlled 2026-05-07 API warm average across 10 runs; matches 0.21.2 |
| 20 | 163 t/s | 45.6 t/s | Older result, superseded by controlled API run |
| 22 | 174 t/s | 45.4 t/s | Older result, superseded by controlled API run |

**Qwen3.5-35B-A3B** (Q4_K_M, ~23GB, MoE -- Ollama 0.20.4):

| Prompt Tokens | Prompt Eval | Generation | vs Previous (Mesa 26.0.1) |
|---------------|-------------|------------|---------------------------|
| 14 | 121.3 t/s | **48.0 t/s** | tg +4.8% |
| 23 | 182.3 t/s | **47.5 t/s** | tg +4.4% |
| 122 | 456.7 t/s | **47.4 t/s** | tg +4.2% |

**Qwen3-Coder 30B-A3B** (Q8_0, ~32GB, MoE):

| Prompt Tokens | Prompt Eval | Generation | Notes |
|---------------|-------------|------------|-------|
| 12 | 118.3 t/s | **51.4 t/s** | Fastest via Ollama |
| 21 | 205.2 t/s | **51.3 t/s** | Higher quality than Q4_K_M |

**Qwen3-Coder-Next** (~51GB, dense):

| Prompt Tokens | Prompt Eval | Generation | vs Previous |
|---------------|-------------|------------|-------------|
| 12 | 90.7 t/s | **39.1 t/s** | tg +2.9% |
| 21 | 129.5 t/s | **38.4 t/s** | tg +3.8% |
| 120 | 301.2 t/s | **37.9 t/s** | NEW |

**Other Models:**

| Model | Size | Prompt Tokens | pp (t/s) | tg (t/s) |
|-------|------|---------------|----------|----------|
| Llama 2 7B | 3.8 GB | 24 | 384.6 | 52.0 |
| Qwen2.5-VL 7B | 6.0 GB | 23 | 81.7 | 21.4 |
| Qwen3.5 35B (no-think) | 23 GB | 14 | 127.1 | 47.4 |

**Llama 3.1 70B** (Q4_K_M, 42GB, Dense -- the "doesn't fit on RTX 4090" showcase):

| Prompt Tokens | Prompt Eval | Generation | Notes |
|---------------|-------------|------------|-------|
| 14 | 22.1 t/s | 4.9 t/s | Cold start |
| 23 | 36.8 t/s | 4.8 t/s | Realistic chat |
| 122 | 79.6 t/s | 4.7 t/s | Long prompt |

> **Why so slow?** This is a 42GB dense model -- every token reads all 42GB of weights. At ~215 GB/s bandwidth, the theoretical maximum is 215/42 = 5.1 t/s. We hit 4.8 t/s = **94% of the theoretical ceiling**. The model is slow not because of poor optimization, but because it's massive. An RTX 4090 (24GB VRAM) cannot run this model at all. This is the Strix Halo advantage: running models that don't fit on consumer GPUs.

> **What improved?** Mesa 26.0.1 to 26.0.2 plus enabling the `tuned accelerator-performance` profile gave a consistent **+4-5% generation speed improvement** across all models.

### llama-server Multi-User Serving (b9010)

Single-user `llama-bench` tells you the ceiling for one stream. For a real local API box, the more practical question is what happens when multiple tools or users hit `llama-server` at the same time.

**Qwen3.6-35B-A3B** (UD-Q4_K_M, Vulkan RADV, llama.cpp b9010, continuous batching, 4096 context tokens per slot):

| `-np` | Concurrent Requests | Aggregate Generation | Avg per Request | Mean TTFT | Mean ITL | Notes |
|-------|---------------------|----------------------|-----------------|-----------|----------|-------|
| 1 | 1 | 59.21 t/s | 59.21 t/s | 0.117 s | 16.1 ms | Server/API baseline |
| 2 | 2 | 92.21 t/s | 46.11 t/s | 0.198 s | 20.3 ms | Good scaling |
| 4 | 4 | 130.81 t/s | 32.71 t/s | 0.237 s | 29.0 ms | Strong batching gain |
| 8 | 8 | **161.98 t/s** | 20.25 t/s | 0.307 s | 47.4 ms | Practical sweet spot |
| 16 | 16 | 165.98 t/s | 10.38 t/s | 0.547 s | 92.9 ms | Throughput plateau |

> **Takeaway:** continuous batching makes Strix Halo look much stronger as a local API server than single-user tg numbers suggest. `-np 8` delivers about **2.7x** the `-np 1` aggregate throughput while keeping TTFT around 0.3 seconds. `-np 16` works with no errors in this test, but aggregate throughput barely improves while per-user speed drops sharply.

**Qwen3-Coder 30B-A3B** (UD-Q4_K_XL, Vulkan RADV, llama.cpp b9010, continuous batching, 4096 context tokens per slot):

| `-np` | Concurrent Requests | Aggregate Generation | Avg per Request | Mean TTFT | Mean ITL | Notes |
|-------|---------------------|----------------------|-----------------|-----------|----------|-------|
| 1 | 1 | 90.20 t/s | 90.20 t/s | 0.079 s | 10.6 ms | Server/API baseline |
| 2 | 2 | 121.65 t/s | 60.83 t/s | 0.133 s | 15.5 ms | Good scaling |
| 4 | 4 | 157.41 t/s | 39.36 t/s | 0.207 s | 24.0 ms | Strong batching gain |
| 8 | 8 | **173.16 t/s** | 21.65 t/s | 0.382 s | 43.5 ms | Practical sweet spot |
| 16 | 16 | 129.56 t/s | 8.10 t/s | 0.571 s | 119.9 ms | Regression |

> **Coding server takeaway:** `-np 8` is also the best measured setting for Qwen3-Coder, but here `-np 16` is actively worse. More parallel slots are not automatically better.

Raw data: `data/multi_user.csv`, `data/raw/2026-05-03/multi-user/`, and `data/raw/2026-05-03/multi-user-coder/`.

### llama-bench Direct -- Key llama.cpp Builds (b9049, b9010, and b8460) vs kyuz0 Containers (b8298)

> **UPDATE (2026-03-21): Updating llama.cpp from b8298 to b8460 gave +25% on both pp and tg for MoE models.** The new build includes a Vulkan Flash Attention refactor ([PR #19625](https://github.com/ggml-org/llama.cpp/pull/19625)), graphics queue optimization for AMD ([PR #20551](https://github.com/ggml-org/llama.cpp/pull/20551)), and GDN shader support for Qwen3.5 ([PR #20334](https://github.com/ggml-org/llama.cpp/pull/20334)).
>
> **Important caveats:**
> - The +25% improvement is specific to **MoE models on Vulkan** due to the Wave32 FA refactor and graphics queue change. Dense models (Llama 2 7B, Llama 3.1 70B) showed minimal change (<2%) because they were already at the memory bandwidth ceiling.
> - If you use [kyuz0's containers](https://github.com/kyuz0/amd-strix-halo-toolboxes), you get these updates automatically -- the containers rebuild on every llama.cpp master update. kyuz0's toolboxes remain the easiest way to stay current. Our finding here validates the importance of their approach.
> - **WARNING: AMDVLK silently overrides RADV.** If AMDVLK is installed, its `/etc/vulkan/icd.d/amd_icd64.json` takes priority over RADV. This halves your pp speed (1080 -> 660 pp512) without any visible error. Always set `AMD_VULKAN_ICD=RADV` or uninstall AMDVLK entirely: `sudo dpkg -r amdvlk && sudo rm -f /etc/vulkan/icd.d/amd_icd64.json`. Check your driver: RADV shows `(RADV STRIX_HALO) (radv)` with `shared memory: 65536` in llama-bench output. AMDVLK shows `(AMD open-source driver)` with `shared memory: 32768`. We [originally reported this as a llama.cpp regression](https://github.com/ggml-org/llama.cpp/issues/22375) -- it wasn't.

**Qwen3.5-35B-A3B** (Q4_K_M, 19.9GB, MoE) -- the biggest improvement:

| Build | Driver | pp128 | pp512 | tg128 | vs old RADV |
|-------|--------|-------|-------|-------|-------------|
| **b8460 (newer March build)** | **RADV** | **623** | **1080** | **64.85** | **pp +24%, tg +25%** |
| b8460 (newer March build) | AMDVLK | 521 | 663 | 64.10 | pp -24%, tg +23% |
| b8298 (kyuz0) | RADV | 583 | 868 | 52.06 | baseline |
| b8298 (kyuz0) | AMDVLK | 479 | 576 | 56.08 | |

> **Beginner rule: use RADV for Vulkan. Do not install AMDVLK.** In the newer b8460 Vulkan comparison, RADV is faster than AMDVLK on both pp (+63%) and tg (+1.2%), and AMDVLK can silently hijack your Vulkan driver. Advanced note: ROCm/HIP is a different backend, not a Vulkan driver. HIP can still be worth testing for long prompts, RAG ingest, and other prompt-processing-heavy workloads.

Extended context scaling (b8460 RADV):

| pp512 | pp2048 | pp4096 | pp8192 | Drop at 8K |
|-------|--------|--------|--------|------------|
| **1080** | **1057** | **1049** | **1049** | **-3%** |

> pp is virtually flat from 512 to 8192 tokens. Only 3% drop at 8K context.

**Qwen3-Coder 30B-A3B** (Q4_K_S speed-first and UD-Q4_K_XL balanced, MoE):

| Build | Driver | pp512 | tg128 | Notes |
|-------|--------|-------|-------|-------|
| **b9851** | **RADV** | **1423** | **100.99** | Official release binary; Q4_K_S speed-first quant; not the balanced default |
| **b9179** | **RADV** | **1396** | **98.51** | Q4_K_S speed-first quant, strict-clean r50 confirmation |
| **b9049** | **RADV** | **1321** | **96.76** | 2026-05-07 max-performance guide-flags r20 confirmation |
| **b9010** | **RADV** | **1346** | **97.24** | Controlled 2026-05-03 two-run r20 average |
| b8460 | RADV | 1342 | 87.11 | Previous headline |
| b8298 (kyuz0) | RADV | 1350 | 86.81 | ~same (model was already at ceiling) |

> A controlled May 2026 rerun moved the balanced Qwen3-Coder 30B headline from 87 t/s to 97 t/s on b9010 Vulkan RADV. The 2026-05-07 b9049 max-performance campaign measured 96.76 t/s on UD-Q4_K_XL. A later strict-clean b9179 run measured 98.51 t/s with Q4_K_S, and the official b9851 Vulkan release binary lifted the same speed-first quant to 100.99 t/s. This is still not the default balanced row.

**Gemma 4 26B-A4B historical non-QAT baseline** (UD-Q4_K_M, 15.7GB, MoE) -- tested on b8933 (earliest build with Gemma 4 support):

| Build | Driver | pp512 | tg128 | Notes |
|-------|--------|-------|-------|-------|
| **b8933** | **RADV** | **1142** | **48.46** | early non-QAT Gemma 4 MoE baseline |

> This row is historical and non-QAT. The current practical Gemma 4 route in this guide is **Gemma 4 26B-A4B IT QAT UD-Q4_K_XL**, which measured **74.80 t/s direct** and **102.69 cold / 107.42 T3-only / 110.00 best-repeat t/s** through a matched MTP `llama-server` route. Keep the direct row and server/speculative row separate.
>
> The older non-QAT Gemma 4 row is architecturally slower on tg than Qwen MoE models despite similar size. The reason: head_dim 256/512 (vs Qwen's 128) makes flash attention less efficient, mixed sliding-window/full attention adds overhead, and 3.8B active params vs Qwen's 3.3B. This is not a llama.cpp issue -- it's inherent to the model design. 48.5 t/s is still 3x human reading speed and very usable for interactive chat.
>
> **WARNING:** Gemma 4 is extremely sensitive to KV cache quantization. Using q8_0 KV cache causes 3.5x worse quality degradation compared to Qwen models. Stick with f16 KV cache for Gemma 4. Do NOT use `--cache-type-k q4_0`.

**Llama 4 Scout 109B** (Q4_K_M, 60.9GB, MoE -- 109B total params, 17B active):

| Build | Driver | pp512 | tg128 | Notes |
|-------|--------|-------|-------|-------|
| **b8933** | **RADV** | **331** | **18.32** | 109B model running on a mini PC |

> A 109 billion parameter model running at 18.3 t/s on a 128GB Strix Halo mini PC. An RTX 4090 (24GB VRAM) cannot even load this model. The speed is bandwidth-limited at 17B active parameters -- theoretical max is ~25 t/s at 215 GB/s, we hit 73% of that ceiling.

**Qwen3-Next 80B-A3B** (UD-Q4_K_XL, 42.9GB, MoE -- 80B total params, 3B active, 256K context):

| Build | Driver | pp512 | tg128 | Notes |
|-------|--------|-------|-------|-------|
| **b9172** | **RADV** | **752** | **59.06** | Latest-stack r20 confirmation; best current 80B Qwen-family path |
| **b8933** | **RADV** | **657** | **54.92** | 80B model at 55 t/s |

> 80 billion parameters running at 59 t/s on a mini PC. This is the largest Qwen3-family MoE model -- 80B total with only 3B active parameters and a 256K context window. Despite being 42.9 GB on disk, the MoE routing keeps only 3B params active per token, making it faster than the 51B dense Qwen3-Coder-Next (38 t/s). The 2026-05-16 b9172 check improved this row, while Qwen3-Coder, Qwen3.6, and gpt-oss did not improve on the same latest-stack rerun.

**Qwen3.6-35B-A3B** (Q4_K_M, 19.9GB, MoE -- drop-in upgrade from Qwen3.5, released April 2026):

| Build | Driver | pp512 | tg128 | Notes |
|-------|--------|-------|-------|-------|
| **b9049** | **RADV** | **1059** | **62.56** | Clean 2026-05-07 latest-stack r20 rerun |
| **b8460** | **RADV** | **1064** | **63.76** | Same speed as Qwen3.5 |
| **b9010** | **RADV** | **1109** | **63.06** | UD-Q4_K_M controlled rerun; plain Q4 blob not loadable by upstream b9010 |
| b8933 | RADV | 1040 | 63.66 | No regression between builds |

> Qwen3.6 is a drop-in replacement for Qwen3.5 with significantly improved coding and reasoning quality (same architecture, same active parameters, effectively identical speed). Older April data showed a 13% UD-Q4_K_M penalty, but the controlled May b9010 and b9049 reruns did **not** reproduce that large gap. Prefer plain Q4_K_M when you have a direct-compatible GGUF, but treat the old "UD is always 13% slower" warning as superseded until same-build plain-vs-UD is rerun.

### ROCm HIP -- usable on kernel 6.19.4 with HSA override

We discovered that `HSA_OVERRIDE_GFX_VERSION=11.5.1` + `HSA_ENABLE_SDMA=0` fixes the ROCm segfault on kernel 6.19.x. We also rebuilt ROCm with the same b8460 source to make the comparison fair:

| Build | pp128 | pp512 | tg128 | Notes |
|-------|-------|-------|-------|-------|
| **b8460 (newer March build, kernel 6.19.4)** | **547** | **1047** | **54.67** | **tg +14% vs b8301** |
| b8301 (self-compiled, kernel 6.19.4) | 542 | 1059 | 47.87 | old build |
| b8301 (self-compiled, kernel 6.18.14) | 488 | 996 | 48.80 | previous best |

> ROCm also improved in the b8460 comparison: tg went from 47.87 to **54.67** (+14%) thanks to generic llama.cpp optimizations. But **Vulkan RADV was still faster on both pp and tg in this short-context pair**: RADV 1080 vs ROCm 1047 pp512 (+3%), RADV 64.85 vs ROCm 54.67 tg128 (+19%). The +25% Vulkan improvement was ~14% generic (ROCm got this too) plus ~11% Vulkan-specific (FA refactor, graphics queue). ROCm's remaining advantage is hipBLASLt and rocWMMA at very long context (32K+).

**ROCm HIP spot check (2026-05-03, b8460 HIP build):**

| Model | Quant | ROCm pp512 | ROCm tg128 | Vulkan Reference |
|-------|-------|------------|------------|------------------|
| Qwen3.6 35B-A3B | UD-Q4_K_M | 1186 | 52.7 | Vulkan b9010: 1109 pp, 63.1 tg |
| Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 1285 | 73.7 | Vulkan b9010: 1346 pp, 97.2 tg |

> This HIP run required `LD_LIBRARY_PATH=/usr/local/lib/ollama/rocm` plus the HSA override and emitted a missing `TensileLibrary_lazy_gfx1151.dat` warning. Treat it as a ROCm HIP baseline, not a tuned rocBLASLt/rocWMMA result. Vulkan RADV remains the recommended short-context generation backend.

**Build version matters enormously:**

| What we tested | pp512 | tg128 | Lesson |
|----------------|-------|-------|--------|
| Ollama Vulkan RADV (b8298) | ~457 (via API) | 47.4 | Ollama adds overhead |
| llama-bench RADV (b8298) | 868 | 52.06 | Eliminating Ollama helps |
| llama-bench RADV **(b8460)** | **1080** | **64.85** | **Updating llama.cpp = +25%** |
| ROCm HIP (b8301, HSA fix) | 1059 | 47.87 | Old build, unfair comparison |
| ROCm HIP **(b8460, HSA fix)** | **1047** | **54.67** | **ROCm got +14% tg from same update** |

> The single biggest optimization in this early campaign was **updating llama.cpp**. It gave more improvement (+25% on MoE models) than all kernel tuning, batch size sweeps, and driver comparisons combined. This is counter-intuitive -- people spend hours on kernel parameters, GRUB flags, and Mesa versions, while a current source build can deliver more than everything else put together. Note: this applies to MoE models specifically. Dense models were already at the bandwidth ceiling and show <2% change.

**Batch size and ubatch tuning results (b8298, for reference):**

We swept batch sizes 64-2048 and ubatch sizes 32-1024. Result: **default 512 is optimal.** No headroom via tuning -- the improvement came from updating the build.

**How to build the latest llama.cpp with Vulkan:**

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
CC=/usr/bin/gcc CXX=/usr/bin/g++ cmake -B build -S . \
  -DGGML_VULKAN=ON \
  -DCMAKE_BUILD_TYPE=Release \
  -G "Unix Makefiles"
cmake --build build -j$(nproc)

# Benchmark
AMD_VULKAN_ICD=RADV ./build/bin/llama-bench \
  -m ~/models/your-model.gguf \
  -fa 1 -ngl 999 -mmp 0 -p 512 -n 128
```

### ROCm on kernel 6.19.x (the fix)

```bash
# Add these environment variables before running llama-bench:
export HSA_OVERRIDE_GFX_VERSION=11.5.1
export HSA_ENABLE_SDMA=0
export ROCBLAS_USE_HIPBLASLT=1
```

**Llama 2 7B** (Q4_K_M, 3.8GB, Dense):

| Driver | pp128 | pp512 | pp1024 | tg128 |
|--------|-------|-------|--------|-------|
| **RADV** | **1154** | **1377** | **1356** | 48.12 |
| AMDVLK | 335 | 327 | 325 | 48.02 |

> AMDVLK is 3-4X slower on pp for dense models (2 GiB buffer limit). Use RADV.

**Qwen3-0.6B** (Q8_0, 762MB, Dense) -- maximum throughput:

| Driver | pp128 | pp512 | tg128 |
|--------|-------|-------|-------|
| RADV | **10,313** | **13,112** | **266** |

### ROCm HIP (llama.cpp)

> **NOTE (March 2026):** Kernel 6.19.x misidentifies gfx1151 as gfx1100 for ROCm, but this is fixable with `HSA_OVERRIDE_GFX_VERSION=11.5.1` and `HSA_ENABLE_SDMA=0`. See [ROCm on kernel 6.19.x](#rocm-on-kernel-619x-the-fix) for the full fix. Without these environment variables, ROCm containers will segfault.

**Previous results on kernel 6.18.14** (for reference -- these worked):

| Build | Model | pp128 | pp512 | tg128 |
|-------|-------|-------|-------|-------|
| Self-compiled b8301, FA on, -mmp 0 | Qwen3.5-35B-A3B Q4_K_M | 488 | 996 | 48.8 |
| kyuz0 b8298, FA on | Qwen3.5-35B-A3B Q4_K_M | 306 | 520 | 55.3 |
| kyuz0 b8298, FA off | Qwen3.5-35B-A3B Q4_K_M | 352 | 524 | 53.8 |
| kyuz0 b8189, FA + hipBLASLt | Llama 2 7B Q4_K_M | 1163 | 1261 | 45.07 |

**Vulkan llama-bench Direct (kyuz0 containers, b8298) -- March 2026:**

| Driver | Model | pp128 | pp256 | pp512 | pp1024 | tg128 |
|--------|-------|-------|-------|-------|--------|-------|
| **RADV** | Qwen3.5-35B-A3B Q4_K_M | **503.67** | - | **858.88** | - | 52.15 |
| **AMDVLK** | Qwen3.5-35B-A3B Q4_K_M | 477.28 | - | 575.59 | - | **55.54** |
| **RADV** | Llama 2 7B Q4_K_M | **1153.53** | **1364.45** | **1377.18** | **1355.88** | 48.12 |
| **AMDVLK** | Llama 2 7B Q4_K_M | 334.50 | 337.96 | 327.35 | 325.33 | 48.02 |

> **Critical finding (b8298):** AMDVLK has a 2 GiB single buffer allocation limit that cripples pp on dense models (3-4X slower on Llama 2 7B). On MoE models, AMDVLK was slightly faster on tg (+6.5%) with b8298, but **this advantage disappeared with b8460** -- see the [key build comparison](#llama-bench-direct-key-llamacpp-builds-b9049-b9010-and-b8460-vs-kyuz0-containers-b8298). For beginners: keep AMDVLK removed and use RADV for Vulkan.

**Vulkan RADV vs ROCm HIP (same build b8460, Qwen3.5-35B-A3B):**

| Metric | Ollama (b8298) | Vulkan RADV (b8460) | ROCm HIP (b8460) | Best |
|--------|----------------|---------------------|-------------------|------|
| pp512 | ~457 | **1080** | 1047 | **Vulkan RADV** |
| tg128 | 47.4 | **64.85** | 54.67 | **Vulkan RADV** |

> **Vulkan RADV wins on both pp512 and tg128 for this Qwen3.5 b8460 short-context pair.** ROCm works on kernel 6.19.x with the HSA override fix, and newer spot checks show HIP can win longer prompt-processing rows. Use `llama-bench` or `llama-server` directly instead of Ollama to avoid the current ~20-25% short-context overhead on Qwen3.6.

### Backend Comparison Table

Based on our measurements and [lhl's detailed testing](https://github.com/lhl/strix-halo-testing):

| Backend | Best For | pp (relative) | tg (relative) | Context Scaling | Setup Difficulty |
|---------|----------|---------------|---------------|-----------------|------------------|
| Ollama + Vulkan RADV | General use, chat | Good | Good | Degrades at 8K+ | Easiest |
| llama.cpp + Vulkan RADV (container) | Best-tested generation-heavy GGUF path | Best-tested in measured short-context rows | **Best-tested short-context generation** | Degrades at 8K+ | Easy |
| llama.cpp + Vulkan AMDVLK | Not recommended | Slower than RADV on b8460 | Slower on dense (2 GiB limit) | Degrades at 8K+ | Easy |
| ROCm HIP | Batch processing | Excellent | Good | Poor at 32K+ | Medium (needs HSA fix on 6.19.x) |
| ROCm + rocWMMA (tuned) | Long context | Excellent | Best at 32K | **Best scaling** | Very hard |
| vLLM (TheRock) | API serving | Good | Good | Good | Hard |

### Hardware Comparison

| Hardware | Bandwidth | tg (MoE ~30B) | Max Model Size | Price |
|----------|-----------|---------------|----------------|-------|
| RTX 4090 | ~1008 GB/s | 100-122 t/s | 24 GB | ~$1600 GPU only |
| RTX 3090 | ~936 GB/s | 100-112 t/s | 24 GB | ~$800 used |
| Apple Mac Studio M4 Max high-memory | ~546 GB/s | ~100 t/s (MLX) | 96-128 GB depending on availability | verify current Apple config |
| **Beelink GTR9 Pro** | **~215 GB/s** | **63-101.0 t/s current direct Qwen MoE rows; 81 t/s speed-first Qwen3.6** | **120+ GB** | **$4,349 official (July 27, 2026 US snapshot)** |
| NVIDIA DGX Spark | ~273 GB/s | 52-56 t/s (120B) | 128 GB | $4,699 |

> **Apples-to-apples (gpt-oss-120b, same model family):** this guide now measures Strix Halo at 55.57 t/s tg128 locally via llama.cpp Vulkan/RADV b9049. External DGX Spark reports are around 52-56 t/s on comparable generation rows. At Beelink's July 27, 2026 official US price snapshot, the price gap to DGX Spark is about $350 ($4,349 vs $4,699), although other Strix Halo systems remain cheaper. On smaller MoE models (Qwen3-30B), Strix Halo measures 96.76 t/s on the balanced Qwen3-Coder b9049 campaign, 100.99 t/s with Qwen3-Coder b9851 Q4_K_S, and 100.04 t/s with a separate Qwen3-30B-A3B-Instruct-2507 IQ4_XS b9467 row. The DGX Spark wins on prompt processing and long-context rows in external reports. High-memory Mac Studio pricing/availability changed quickly in May 2026, so verify current Apple configs before using it as a purchase comparison. Source: [local raw data](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/), [NVIDIA DGX Spark](https://marketplace.nvidia.com/en-us/enterprise/personal-ai-supercomputers/dgx-spark/), [Framework Community](https://community.frame.work/t/dgx-spark-vs-strix-halo-initial-impressions/77055), [lhl](https://github.com/lhl/strix-halo-testing).

### Long Context Performance

Local prompt-processing scaling on the May 2026 b9010 Vulkan RADV stack:

| Model | 4K pp | 8K pp | 16K pp | 32K pp | 64K pp | Notes |
|-------|-------|-------|--------|--------|--------|-------|
| Qwen3.6 35B-A3B UD-Q4_K_M | 1082 | 1089 | 1025 | 909 | 740 | 68% of 4K speed retained at 64K |
| Qwen3-Next 80B-A3B UD-Q4_K_XL | 742 | 736 | 700 | 645 | 544 | 73% of 4K speed retained at 64K |

> **Local result:** long-prompt ingestion remains usable through 64K on both tested MoE models. This table measures prompt processing, not generation after a fully occupied KV cache. Raw data: `data/long_context.csv` and `data/raw/2026-05-03/long-context/`.

Filled-KV decode through `llama-server` on the same stack:

| Model | Prompt | KV | Prompt Eval | Decode After Fill | Wall Time |
|-------|--------|----|-------------|-------------------|-----------|
| Qwen3.6 35B-A3B | 32K | f16 | 1217 t/s | 51.0 t/s | 29.5 s |
| Qwen3.6 35B-A3B | 32K | q4_0 | 1049 t/s | 56.0 t/s | 33.6 s |
| Qwen3.6 35B-A3B | 64K | f16 | 932 t/s | 41.4 t/s | 73.5 s |
| Qwen3.6 35B-A3B | 64K | q4_0 | 750 t/s | 51.3 t/s | 90.0 s |
| Qwen3.6 35B-A3B | 128K | f16 | 617 t/s | 32.2 t/s | 216.7 s |
| Qwen3-Next 80B-A3B | 32K | f16 | 973 t/s | 46.2 t/s | 36.5 s |
| Qwen3-Next 80B-A3B | 64K | f16 | 753 t/s | 38.2 t/s | 90.5 s |
| Qwen3-Next 80B-A3B | 128K | f16 | 498 t/s | 29.1 t/s | 268.5 s |

> **KV-cache takeaway:** q4_0/q8_0 KV improves Qwen3.6 decode speed after the context is filled, but slows prompt ingestion enough that full first-turn wall time is worse than f16 in this benchmark. Use f16 for first-turn long prompts. Consider q4_0/q8_0 only when memory pressure or long continued generation matters more than prompt-ingest speed. The 128K f16 rows completed without truncation. Raw data: `data/filled_kv_decode.csv`, `data/raw/2026-05-03/filled-kv-decode/`, and `data/raw/2026-05-03/filled-kv-decode-128k/`.

Real-corpus 64K check using this guide's own documentation files:

| Model | Prompt Type | Tokens | Prompt Eval | Decode After Fill | Wall Time |
|-------|-------------|--------|-------------|-------------------|-----------|
| Qwen3.6 35B-A3B | synthetic repeated token | 65,533 | 932 t/s | 41.4 t/s | 73.5 s |
| Qwen3.6 35B-A3B | real guide corpus | 65,120 | 706 t/s | 40.8 t/s | 95.4 s |
| Qwen3-Next 80B-A3B | synthetic repeated token | 65,532 | 753 t/s | 38.2 t/s | 90.5 s |
| Qwen3-Next 80B-A3B | real guide corpus | 63,507 | 505 t/s | 37.8 t/s | 129.4 s |

> **Real-corpus takeaway:** synthetic repeated-token prompts are optimistic for prompt ingest. Real documentation text slowed prompt eval by 24-33%, while decode-after-fill barely changed. Raw data: `data/raw/2026-05-03/filled-kv-decode-real-corpus/`.

Based on [lhl's measurements](https://github.com/lhl/strix-halo-testing) with gpt-oss-120b (tg32):

| Context | Vulkan AMDVLK | ROCm Standard | ROCm rocWMMA-tuned |
|---------|---------------|---------------|---------------------|
| 2K | 50.05 t/s | 46.56 t/s | 48.97 t/s |
| 4K | 46.11 t/s | 38.25 t/s | 45.42 t/s |
| 8K | 43.15 t/s | 32.65 t/s | 43.55 t/s |
| 16K | 38.46 t/s | 25.50 t/s | 40.91 t/s |
| 32K | 31.54 t/s | 17.82 t/s | **36.43 t/s** |

> At 32K context, standard ROCm drops to 17.82 t/s. Vulkan holds at 31.54 t/s (1.8X faster). But lhl's tuned rocWMMA branch is the **overall winner at 36.43 t/s** -- 2X faster than standard ROCm and 15% faster than Vulkan at 32K.

At extreme context (130K tokens, from [strixhalo.wiki](https://strixhalo.wiki/AI/llamacpp-performance)):

| Backend | pp512 (t/s) | tg128 (t/s) |
|---------|-------------|-------------|
| Vulkan RADV | 17 | 13 |
| ROCm | 41 | 5 |
| ROCm rocWMMA-tuned | 51 | 13 |

---

## Backend Decision Guide

```
                        Which backend should I use?
                                  |
                    Do you need long context (>32K)?
                         /                \
                       NO                  YES
                       |                    |
              Just want it easy?      ROCm + rocWMMA-tuned
                /          \            (lhl's branch)
              YES           NO          Best for 32K+ context
               |             |
          Ollama +      Build latest
          Vulkan RADV   llama.cpp yourself
               |             |
          "It just      llama-server +
           works"       Vulkan RADV
           50 t/s        63 t/s
```

## Phase 1: BIOS Configuration

Do this BEFORE installing the OS.

### Step 1.1: Set UMA Frame Buffer Size

Navigate to `Integrated Graphics` then `UMA Frame Buffer Size` and set it to **512MB** if your BIOS exposes that option. If your vendor BIOS only exposes **2GB** as the minimum, leave it at 2GB; do not flash or fight the BIOS only to chase 512MB.

> **Why?** On the primary Beelink 128GB system, the default BIOS setting reserved ~97GB for GPU VRAM and left only ~31GB visible to the OS. Setting UMA to 512MB lets Linux see almost all system RAM. Some vendor BIOSes use 2GB as the lowest fixed reserve; that is fine if Linux still sees the large system-memory pool. Vulkan/RADV uses GTT system memory, so the fixed UMA reserve is not the total memory available to the iGPU path. The practical check is `free -h`: a 128GB box should show roughly 124-126GiB usable, not ~31GiB.

### Step 1.2: Choose the IOMMU policy

For a normal system, leave IOMMU **Enabled** or at the firmware default. This preserves NPU access, RDMA/VFIO/passthrough support, and mobile suspend behavior.

Use `amd_iommu=off` only as an optional profile for an always-on desktop benchmark box where the NPU and suspend do not matter. [lhl's memory-bandwidth testing](https://github.com/lhl/strix-halo-testing) measured about 6% faster memory reads with IOMMU off (234 vs 221 GB/s), and this guide's primary Beelink headline runs used that profile. It is a reproducibility choice, not a universal requirement: a GMKtec EVO-X2 community Vulkan/RADV run with translated IOMMU mode reproduced the guide within about 2%.

> **Laptop/tablet and NPU warning:** a reproduced ROG Flow Z13 case found that `amd_iommu=off` prevented s0i3 hardware sleep, leaving 0% s0ix residency, spinning fans, heat, and battery drain. The Linux `amdxdna` driver also now refuses to run without IOMMU because the NPU firmware requires it. See [kyuz0 issue #104](https://github.com/kyuz0/amd-strix-halo-toolboxes/issues/104) and [Linux commit `a8878e19`](https://github.com/torvalds/linux/commit/a8878e19d2f5205ad1f170fc230c2cc25a3b9390).

---

## Phase 2: Ubuntu 24.04 Installation

### Step 2.1: Install Ubuntu 24.04 LTS

Install Ubuntu 24.04 LTS Desktop with default settings. After installation:

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2.2: Switch to X11

Wayland can cause issues with remote desktop, screen sharing, and some GPU monitoring tools.

```bash
sudo tee -a /etc/gdm3/custom.conf > /dev/null << 'EOF'
WaylandEnable=false
EOF
```

> If the line already exists (commented out), uncomment it instead. Reboot to apply.

> **Ubuntu 26.04 LTS** (released April 2026) ships with Linux 7.0, Mesa 26.0, and native `apt install rocm`. However, 26.04 is **Wayland-only** (X11 switch above does not work) and the performance-relevant components (kernel, Mesa RADV) are already available on 24.04 via the [kisak PPA](https://launchpad.net/~kisak/+archive/ubuntu/kisak-mesa) and [mainline kernel PPA](https://kernel.ubuntu.com/mainline/). **Upgrading is not needed for LLM performance.** This guide stays on 24.04 LTS.

---

## Phase 3: Kernel Configuration

### Step 3.1: Kernel Version

> **Measured setup:** This guide's primary system uses kernel 6.19.4.
> - Older kernels may have gfx1151 stability or ROCm issues.
> - Kernel 6.19.x works here with the documented HSA override for ROCm because it can report gfx1151 as gfx1100.
> - Treat kernel guidance here as this guide's tested state, not a universal support matrix.

Check your kernel:

```bash
uname -r
```

### Step 3.2: Configure GRUB Boot Parameters

```bash
sudo tee /tmp/grub_update.txt << 'EOF'
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash amdgpu.gttsize=131072 ttm.pages_limit=31457280 amdgpu.cwsr_enable=0"
EOF
```

Then edit `/etc/default/grub` and replace the `GRUB_CMDLINE_LINUX_DEFAULT` line with the content above.

| Parameter | Purpose | Impact |
|-----------|---------|--------|
| `amd_iommu=off` | Optional always-on desktop benchmark profile | About +6% memory reads in lhl's test; disables NPU access and can break deep suspend on mobile systems |
| `amdgpu.gttsize=131072` | Set GTT (GPU-accessible system memory) to 128GB | Required for large models |
| `ttm.pages_limit=31457280` | Set TTM page limit to ~120GB | Required for large models |
| `amdgpu.cwsr_enable=0` | Disable compute wave save/restore | Not needed for LLM inference |

> **Optional desktop benchmark profile:** to match the primary Beelink headline environment, add `amd_iommu=off` to the line above. Do not use that profile when you need the NPU, RDMA/VFIO/passthrough, or reliable laptop/tablet suspend. kyuz0's toolboxes use `iommu=pt`; the performance difference is documented in [issue #66](https://github.com/kyuz0/amd-strix-halo-toolboxes/issues/66), while the mobile suspend failure is documented in [issue #104](https://github.com/kyuz0/amd-strix-halo-toolboxes/issues/104).

Apply:

```bash
sudo update-grub
```

### Step 3.3: Create AMD GPU Modprobe Configuration

```bash
sudo tee /etc/modprobe.d/amdgpu_llm_optimized.conf > /dev/null << 'EOF'
options amdgpu gttsize=122800
options ttm pages_limit=31457280
options ttm page_pool_size=31457280
EOF
```

Update initramfs:

```bash
sudo update-initramfs -u -k all
```

### Step 3.4: Create udev Rules for GPU Access

```bash
sudo tee /etc/udev/rules.d/99-amd-kfd.rules > /dev/null << 'EOF'
SUBSYSTEM=="kfd", GROUP="render", MODE="0666"
SUBSYSTEM=="drm", KERNEL=="card[0-9]*", GROUP="render", MODE="0666"
SUBSYSTEM=="drm", KERNEL=="renderD[0-9]*", GROUP="render", MODE="0666"
EOF
```

> **IMPORTANT:** The `renderD[0-9]*` rule is critical. Without it, you get `HSA_STATUS_ERROR_OUT_OF_RESOURCES` errors with ROCm.

Add your user to GPU groups:

```bash
sudo usermod -aG render $USER
sudo usermod -aG video $USER
```

Reload and reboot:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
sudo reboot
```

---

## Phase 4: Performance Tuning

### Step 4.1: Install and Configure tuned

```bash
sudo apt install tuned -y
sudo systemctl disable --now power-profiles-daemon || true
sudo systemctl enable --now tuned
sudo tuned-adm profile accelerator-performance
```

Verify:

```bash
tuned-adm active
# Expected: Current active profile: accelerator-performance
systemctl is-active power-profiles-daemon
# Expected: inactive
```

> **Impact:** +5-8% overall performance improvement. Memory bandwidth improves from ~221 GB/s to ~234 GB/s write. We measured +4-5% token generation improvement when tuned was running vs not running.

> **WARNING:** tuned conflicts with Ubuntu's `power-profiles-daemon`. If `power-profiles-daemon` starts, it can stop `tuned` and cost several percent on benchmark rows. For publishable runs, keep `tuned` active and `power-profiles-daemon` inactive.

### Step 4.2: Upgrade Mesa Vulkan Drivers

The default Mesa on Ubuntu 24.04 is significantly slower. Upgrade to Mesa 26.0.2 or newer from the kisak-mesa PPA. Exact driver metadata is recorded per run in the CSV and raw evidence when available.

```bash
sudo add-apt-repository ppa:kisak/kisak-mesa
sudo apt update
sudo apt upgrade -y
```

Verify:

```bash
vulkaninfo --summary 2>&1 | grep driverInfo
# Expected: Mesa 26.0.2+ RADV from kisak-mesa PPA.
```

> **Impact:** Mesa 25.2.8 to 26.0.1 gave **+9% prompt eval** (87 to 96 t/s). Mesa 26.0.1 to 26.0.2 gave an additional small improvement.

> **Note:** You may see DKMS errors about `mt76-mt7925` during the upgrade. These are harmless -- see [Troubleshooting](#troubleshooting).

### Step 4.3: Verify GPU Clock

The GPU should run at its maximum clock speed (2900 MHz) during inference:

```bash
cat /sys/class/drm/card*/device/pp_dpm_sclk
# Expected: 2: 2900Mhz *  (asterisk on highest clock)
```

> **GPU Clock Bug:** On some kernel/firmware combinations, the GPU gets stuck at 900 MHz, causing ~8% performance loss. If your GPU is not at 2900 MHz during load, see [Troubleshooting](#troubleshooting).

### Step 4.4: Linux Firmware

```bash
dpkg -l | grep linux-firmware | head -5
```

> **CRITICAL:** Do NOT install `linux-firmware-20251125`. It breaks ROCm support on Strix Halo (confirmed by [kyuz0 toolboxes](https://github.com/kyuz0/amd-strix-halo-toolboxes)). Symptoms: instability, crashes, ROCm containers failing to start. The safe versions are `20240318` or `20260110+`. If you're on 20251125, downgrade immediately:
>
> ```bash
> # Check your version
> dpkg -l | grep linux-firmware
> # If 20251125, hold the package to prevent auto-updates pulling it back
> sudo apt-mark hold linux-firmware
> ```

---

## Phase 5: Ollama Setup (Vulkan)

Ollama is the easiest way to run LLMs on Strix Halo. With the right configuration, it works great.

### Step 5.1: Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Step 5.2: Configure Ollama for Vulkan

> **Update (April 2026):** Ollama ROCm now works on gfx1151 with `HSA_OVERRIDE_GFX_VERSION=11.5.1` ([ollama/ollama#14855](https://github.com/ollama/ollama/issues/14855)). However, **Vulkan is still ~9% faster** on token generation (46.6 vs 42.4 t/s on Qwen3.5-35B). We recommend Vulkan for best performance. If you need ROCm (for vLLM compatibility or other reasons), add `HSA_OVERRIDE_GFX_VERSION=11.5.1` and `HSA_ENABLE_SDMA=0` to your Ollama environment instead of the Vulkan variables below.

```bash
sudo systemctl edit ollama
```

Add between the comment lines:

```ini
[Service]
Environment="OLLAMA_VULKAN=1"
Environment="OLLAMA_IGPU_ENABLE=1"
Environment="HIP_VISIBLE_DEVICES=-1"
Environment="OLLAMA_FLASH_ATTENTION=1"
Environment="OLLAMA_CONTEXT_LENGTH=8192"
Environment="AMD_VULKAN_ICD=RADV"
Environment="VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json"
Environment="OLLAMA_NUM_BATCH=512"
Environment="OLLAMA_NUM_PARALLEL=1"
```

Restart:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

| Variable | Purpose |
|----------|---------|
| `OLLAMA_VULKAN=1` | Force Vulkan backend (9% faster than ROCm on Strix Halo) |
| `OLLAMA_IGPU_ENABLE=1` | Let current Ollama builds use the Strix Halo integrated GPU instead of dropping it during GPU discovery |
| `HIP_VISIBLE_DEVICES=-1` | Disable HIP device enumeration (avoids ROCm fallback) |
| `OLLAMA_FLASH_ATTENTION=1` | Enable flash attention (+13% prompt processing) |
| `OLLAMA_CONTEXT_LENGTH=8192` | Limit context to prevent OOM (increase if needed) |
| `AMD_VULKAN_ICD=RADV` | Force RADV driver (faster than AMDVLK for general use) |
| `VK_ICD_FILENAMES=...` | Explicitly point to RADV ICD file |
| `OLLAMA_NUM_BATCH=512` | Larger batch size for better throughput |
| `OLLAMA_NUM_PARALLEL=1` | Single request at a time (maximizes single-request speed) |

### Step 5.3: Pull Models

```bash
# Fast MoE model, great for general use and coding (~20GB)
ollama pull qwen3.6:35b-a3b

# Higher quality MoE, Q8_0 quantization (~32GB)
ollama pull qwen3-coder:30b-a3b-q8_0

# Google's MoE model, strong reasoning (~16GB)
ollama pull gemma4:26b-a4b

# Large dense model for complex tasks (~51GB)
ollama pull qwen3-coder-next
```

### Step 5.4: Test

```bash
ollama run qwen3.6:35b-a3b
```

You should see responses generating at ~50 t/s.

---

## Phase 6: Benchmarking

### Step 6.1: Quick Benchmark Script

```bash
tee ~/bench-ollama.sh > /dev/null << 'SCRIPT'
#!/bin/bash
MODEL="${1:-qwen3.6:35b-a3b}"
PROMPT="${2:-hello how are you}"
echo "Model: $MODEL"
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
curl -s http://localhost:11434/api/generate -d "{\"model\":\"$MODEL\",\"prompt\":\"$PROMPT\",\"stream\":false}" | python3 -c "
import sys,json
d=json.load(sys.stdin)
pp=d['prompt_eval_count']/d['prompt_eval_duration']*1e9
tg=d['eval_count']/d['eval_duration']*1e9
print(f'Prompt eval: {pp:.1f} t/s ({d[\"prompt_eval_count\"]} tokens)')
print(f'Generation:  {tg:.1f} t/s ({d[\"eval_count\"]} tokens)')
print(f'Total time:  {d[\"total_duration\"]/1e9:.2f}s')
"
SCRIPT
chmod +x ~/bench-ollama.sh
```

Usage:

```bash
# Default (qwen3.6:35b-a3b, short prompt)
bash ~/bench-ollama.sh

# Specific model with custom prompt
bash ~/bench-ollama.sh qwen3-coder-next "explain backpropagation in simple terms"
```

### Step 6.2: Long Prompt Benchmark

```bash
tee ~/bench-ollama-long.sh > /dev/null << 'SCRIPT'
#!/bin/bash
MODEL="${1:-qwen3.6:35b-a3b}"
echo "Model: $MODEL (long prompt)"
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
curl -s http://localhost:11434/api/generate -d "{\"model\":\"$MODEL\",\"prompt\":\"You are an expert software architect. I need you to review and refactor the following Python code for a web application that handles user authentication, session management, database connections, API rate limiting, error handling, logging, caching with Redis, background job processing with Celery, WebSocket connections for real-time updates, file upload handling with S3 integration, email notification service, payment processing with Stripe, and search functionality with Elasticsearch. Please provide a comprehensive architecture review covering separation of concerns, SOLID principles, design patterns, security best practices, performance optimization, and scalability considerations.\",\"stream\":false}" | python3 -c "
import sys,json
d=json.load(sys.stdin)
pp=d['prompt_eval_count']/d['prompt_eval_duration']*1e9
tg=d['eval_count']/d['eval_duration']*1e9
print(f'Prompt eval: {pp:.1f} t/s ({d[\"prompt_eval_count\"]} tokens)')
print(f'Generation:  {tg:.1f} t/s ({d[\"eval_count\"]} tokens)')
print(f'Total time:  {d[\"total_duration\"]/1e9:.2f}s')
"
SCRIPT
chmod +x ~/bench-ollama-long.sh
```

### Prompt Length Impact on Speed

Prompt processing speed scales with prompt length due to GPU parallelism:

| Prompt Tokens | pp (qwen3.5:35b-a3b) | pp (qwen3-coder-next) |
|---------------|----------------------|-----------------------|
| 12-14 | 121 t/s | 91 t/s |
| 21-23 | 182 t/s | 130 t/s |
| 120-122 | 457 t/s | 301 t/s |

---

## Phase 7: ROCm with llama.cpp (Containers)

For ROCm-specific workloads, batch processing, and long-context experiments, use llama.cpp with ROCm via [kyuz0 containers](https://github.com/kyuz0/amd-strix-halo-toolboxes). For short-context MoE inference, current measured results still favor Vulkan RADV.

> **NOTE:** On kernel 6.19.x, ROCm requires `HSA_OVERRIDE_GFX_VERSION=11.5.1` and `HSA_ENABLE_SDMA=0` to work. Without these, it segfaults. See [ROCm on kernel 6.19.x](#rocm-on-kernel-619x-the-fix).

### Step 7.1: Install Distrobox and Podman

```bash
sudo apt install podman -y
curl -s https://raw.githubusercontent.com/89luca89/distrobox/main/install | sudo sh
```

> **Note:** Ubuntu 24.04 does not include `toolbox` in its repos. Use Distrobox instead. The default `toolbox` on Ubuntu also breaks GPU access.

### Step 7.2: Create the ROCm Container

```bash
distrobox create llama-rocm-72 \
  --image docker.io/kyuz0/amd-strix-halo-toolboxes:rocm-7.2 \
  --additional-flags "--device /dev/dri --device /dev/kfd --group-add video --group-add render --group-add sudo --security-opt seccomp=unconfined"
```

### Step 7.3: Enter and Test

```bash
distrobox enter llama-rocm-72
rocm-smi  # Should show your gfx1151 GPU
```

### Step 7.4: Run llama-bench

The container comes with pre-built, optimized llama.cpp binaries:

```bash
export ROCBLAS_USE_HIPBLASLT=1
llama-bench -m ~/models/your-model.gguf -fa 1 -ngl 999 -mmp 0 -p 128,512 -n 128
```

**Critical flags:**

| Flag | Impact | Notes |
|------|--------|-------|
| `-fa 1` | +13% prompt processing | Always use on Strix Halo |
| `-mmp 0` (--no-mmap) | +22% pp128, more stable | **Always** use on Strix Halo |
| `ROCBLAS_USE_HIPBLASLT=1` | +8% token generation | Set in environment |
| `-ngl 999` | Full GPU offload | Use all available VRAM |

> The kyuz0 pre-built binary includes the critical compiler flag `--amdgpu-unroll-threshold-local=600` which works around the [LLVM compiler regression](https://github.com/llvm/llvm-project/issues/147700) in ROCm 7+. Self-compiled binaries without this flag may be significantly slower.

### Step 7.5: Self-Compiling llama.cpp for ROCm

If you need the latest llama.cpp features or want to use lhl's rocWMMA patches:

```bash
# Inside a ROCm container
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp

# Standard build (without rocWMMA)
cmake -B build -S . \
  -DGGML_HIP=ON \
  -DAMDGPU_TARGETS="gfx1151" \
  -DCMAKE_HIP_FLAGS="-mllvm --amdgpu-unroll-threshold-local=600" \
  -DCMAKE_BUILD_TYPE=Release

# With rocWMMA (for long context, use lhl's tuned branch)
cmake -B build -S . \
  -DGGML_HIP=ON \
  -DAMDGPU_TARGETS="gfx1151" \
  -DGGML_HIP_ROCWMMA_FATTN=ON \
  -DCMAKE_HIP_FLAGS="-mllvm --amdgpu-unroll-threshold-local=600" \
  -DCMAKE_BUILD_TYPE=Release

cmake --build build -j$(nproc)
```

> **WARNING:** Do NOT enable `GGML_HIP_ROCWMMA_FATTN=ON` on upstream llama.cpp without lhl's patches. ROCm 7.2 has a [73% performance regression](https://github.com/ggml-org/llama.cpp/issues/19984) with rocWMMA FA enabled. lhl's custom [rocm-wmma-tune branch](https://github.com/lhl/strix-halo-testing) fixes this and delivers 2X better performance at 32K context.
>
> **Local status (2026-05-03):** the current machine has ROCm HIP evidence but no tuned local rocWMMA build yet. All local HIP build caches checked so far have `GGML_HIP_ROCWMMA_FATTN=OFF`. See [`ROCM_ROCWMMA_BASELINE.md`](ROCM_ROCWMMA_BASELINE.md) before adding any rocWMMA benchmark claims.

---

## Phase 8: vLLM Serving

[kyuz0's vLLM toolboxes](https://github.com/kyuz0/amd-strix-halo-vllm-toolboxes) enable API serving on gfx1151. Treat vLLM as a separate serving benchmark path, not as something to install into the host Python environment.

On Ubuntu, use Distrobox. Prefer `:stable` for measured runs; use `:latest` only for an explicit update/regression test.

Local preflight status: `vllm-gfx1151` was created and smoke-tested on 2026-05-03 with the `:stable` image. See [`VLLM_BASELINE.md`](VLLM_BASELINE.md). This is setup evidence, not a throughput benchmark.

```bash
distrobox create vllm-gfx1151 \
  --image docker.io/kyuz0/vllm-therock-gfx1151:stable \
  --additional-flags "--device /dev/kfd --device /dev/dri --group-add video --group-add render --security-opt seccomp=unconfined"

distrobox enter vllm-gfx1151
rocm-smi
start-vllm
```

Record vLLM results separately from llama.cpp server results. At minimum, capture image tag, ROCm/TheRock build, model, quant, max context, concurrency, aggregate throughput, TTFT, p50/p95 latency, memory use, and any kernel compile/cache warmup behavior.

**Known vLLM issues on gfx1151:**

1. **Qwen3.5 block_size validation** ([issue #28](https://github.com/kyuz0/amd-strix-halo-vllm-toolboxes/issues/28)): Hybrid mamba/attention models compute `block_size=1056` which gets rejected by a hardcoded whitelist. Fix available in the issue.
2. **MIOpen encoder hang** ([issue #30](https://github.com/kyuz0/amd-strix-halo-vllm-toolboxes/issues/30)): Vision models hang during kernel search because MIOpen lacks pre-compiled solver DBs for gfx1151. Workaround: disable encoder profiling.

**Tested models on vLLM:**

| Model | Max Context |
|-------|-------------|
| Llama-3.1-8B | 128K |
| Gemma-3-12b | 128K |
| Qwen3-Coder-30B-A3B (GPTQ 4-bit) | 256K |
| gpt-oss-120b | 128K |
| Qwen3-Next-80B-A3B (GPTQ Int4) | 256K |

---

## Phase 9: Multi-Node Clustering (RDMA)

For models that exceed 128GB, you can cluster multiple Strix Halo machines using RDMA.

From [kyuz0's vLLM clustering guide](https://github.com/kyuz0/amd-strix-halo-vllm-toolboxes):

**Hardware needed:**
- 2x Strix Halo machines (e.g., Framework Desktop)
- 2x Intel E810-CQDA1 100GbE NICs
- 1x DAC cable (direct attach copper, no switch needed for 2 nodes)

**Performance:**
- ~50 Gbps bandwidth, ~5 us latency (vs ~70-100 us TCP/IP)
- TP=2 across machines = 256GB unified memory
- Enables trillion-parameter model inference ([AMD article](https://www.amd.com/en/developer/resources/technical-articles/2026/how-to-run-a-one-trillion-parameter-llm-locally-an-amd.html))

**Additional kernel parameter for clustering:**

```
pci=realloc
```

**Network configuration:**

```bash
# Set MTU to 9000 (jumbo frames)
sudo ip link set <interface> mtu 9000
```

---

## Phase 10: SSH and Remote Access

### Step 10.1: Install SSH and fail2ban

```bash
sudo apt install openssh-server fail2ban -y
```

### Step 10.2: Disable Root Login

```bash
sudo sed -i 's/^#*PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart ssh
```

> fail2ban starts automatically and blocks IPs after repeated failed login attempts. We found **68 brute-force attempts** on our system within hours of enabling SSH -- fail2ban is essential.

---

## Vulkan Driver Comparison

We tested both Vulkan drivers via llama-bench. Results depend heavily on the llama.cpp build version:

**With kyuz0 containers (b8298):**

| Driver | Model | pp512 | tg128 |
|--------|-------|-------|-------|
| **RADV** | Qwen3.5-35B-A3B | **859** | 52.15 |
| AMDVLK | Qwen3.5-35B-A3B | 576 | **55.54** |
| **RADV** | Llama 2 7B | **1377** | 48.12 |
| AMDVLK | Llama 2 7B | 327 | 48.02 |

**With newer tested llama.cpp (b8460) -- AMDVLK advantage is gone:**

| Driver | Model | pp512 | tg128 |
|--------|-------|-------|-------|
| **RADV** | Qwen3.5-35B-A3B | **1080** | **64.85** |
| AMDVLK | Qwen3.5-35B-A3B | 663 | 64.10 |

> AMDVLK is [discontinued](https://github.com/GPUOpen-Drivers/AMDVLK/discussions/416). **Uninstall it** -- even inactive, its ICD file silently hijacks Vulkan and halves your pp speed. See [AMDVLK warning above](#things-that-dont-work-dont-waste-your-time).

> **Our recommendation:** Use **RADV**. AMDVLK is [discontinued](https://github.com/GPUOpen-Drivers/AMDVLK/discussions/416) (last release April 2025) -- RADV is now AMD's only supported open-source Vulkan driver. In this newer Vulkan driver comparison, RADV won both pp and tg, and AMDVLK also had a 2 GiB buffer limit that caused 3-4X slower pp on dense models. Don't install AMDVLK.

**Optimal ubatch sizes per driver** (from lhl's testing):
- AMDVLK: `-ub 512`
- RADV: `-ub 1024`
- ROCm HIP: `-ub 2048`

---

## Key Findings and Corrections

> These findings correct several common recommendations found in other Strix Halo guides.

### Things That DON'T Work (Don't Waste Your Time)

| Issue | Common Advice | Reality | What Happens If You Try |
|-------|---------------|---------|------------------------|
| ~~Ollama HIP/ROCm~~ | ~~"Use ROCm backend"~~ | **Fixed in Ollama 0.20+** with `HSA_OVERRIDE_GFX_VERSION=11.5.1`. Works but ~9% slower tg than Vulkan | Use Vulkan for best speed, ROCm if you need vLLM compatibility |
| `iommu=pt` for speed alone | "Use pass-through only for more speed" | No benefit over default in lhl's memory-read test | Still useful when IOMMU-dependent NPU, suspend, RDMA, VFIO, or passthrough behavior matters |
| AMDVLK for all workloads | "AMDVLK is fastest" | [Project discontinued](https://github.com/GPUOpen-Drivers/AMDVLK/discussions/416) (last release April 2025). RADV beats AMDVLK on both pp (+63%) and tg. **Worse: even if you don't use AMDVLK, its ICD file (`/etc/vulkan/icd.d/amd_icd64.json`) silently hijacks Vulkan and halves your pp speed.** You won't see an error -- just mysteriously slow prompt processing | **Uninstall it completely:** `sudo dpkg -r amdvlk && sudo rm -f /etc/vulkan/icd.d/amd_icd64.json`. Verify with llama-bench: RADV shows `(RADV STRIX_HALO)` with `shared memory: 65536`. AMDVLK shows `(AMD open-source driver)` with `shared memory: 32768` |
| rocWMMA on upstream llama.cpp | "Enable for 2x speed" | [73% regression](https://github.com/ggml-org/llama.cpp/issues/19984) on ROCm 7.2 | Massively slower prompt processing |
| BIOS VRAM increase for speed | "More GPU VRAM = faster" | Zero speed difference, but a very large fixed UMA reserve can cripple OS-visible RAM and GTT capacity. Use 512MB if available; 2GB is fine when that is the vendor minimum. | If Linux only sees ~31GB on a 128GB box, large models will not load |
| ROCm 7.0 RC | "Use ROCm 7 RC" | Segfaults on kernel 6.18.14+ | `HSA_STATUS_ERROR` crash |
| Kernel 6.19.x with ROCm (without fix) | "Just use latest kernel" | GPU misidentified as gfx1100 without HSA override | Segfaults unless you set `HSA_OVERRIDE_GFX_VERSION=11.5.1` |
| linux-firmware-20251125 | Auto-update | Breaks ROCm on Strix Halo | Instability, crashes |
| PyTorch / HuggingFace Transformers | "Just load the model" | [92-95% of decode time is hipMemcpy](https://github.com/pytorch/pytorch/issues/171687), not compute. ~1.5 t/s on 70B vs llama.cpp's 4.8 t/s | PyTorch doesn't handle UMA correctly -- use llama.cpp or Ollama |

### Things That DO Work

| Optimization | Impact | How |
|-------------|--------|-----|
| Mesa 25.2.8 to 26.0.2 | **+9-10% pp** | `sudo add-apt-repository ppa:kisak/kisak-mesa` |
| Flash Attention | **+13% pp** | `-fa 1` or `OLLAMA_FLASH_ATTENTION=1` |
| `--no-mmap` (disable mmap) | **+22% pp128** | `-mmp 0` in llama.cpp, always use on Strix Halo |
| hipBLASLt | **+8% tg** | `ROCBLAS_USE_HIPBLASLT=1` (ROCm only) |
| tuned accelerator-performance | **+5-8% overall** | `sudo tuned-adm profile accelerator-performance` |
| RADV over AMDVLK | **+63% pp, +1.2% tg** | Uninstall AMDVLK entirely (see above). `AMD_VULKAN_ICD=RADV` works too but is easy to forget |
| `OLLAMA_IGPU_ENABLE=1` | Avoids CPU-only Ollama on current builds | Required for both the Ollama 0.31.1 local-binary comparator and the normal 0.31.2 service path on the measured Beelink system |
| `amd_iommu=off` | **About +6% memory reads in one measured desktop test** | Optional benchmark profile; do not use for NPU or mobile suspend workflows |
| BIOS UMA/VRAM reserve low enough | OS sees ~124-126GiB instead of ~31GiB on 128GB systems; GTT gets the large shared pool | No speed change from 512MB vs sane low reserves, but required to avoid losing most system RAM. Use 512MB if available; 2GB is fine when that is the vendor minimum |
| `HIP_VISIBLE_DEVICES=-1` | Fixes Ollama crash | Required for Vulkan-only mode |
| LLVM unroll workaround | Restores ROCm 7+ perf | `-mllvm --amdgpu-unroll-threshold-local=600` |
| lhl's rocWMMA-tuned | **2X tg at 32K context** | Custom branch, requires manual build |
| **Updating llama.cpp** | **+25% pp and tg (MoE)** | `git pull && cmake --build` -- biggest single optimization |
| HSA_OVERRIDE_GFX_VERSION=11.5.1 | Fixes ROCm on kernel 6.19.x | Required for ROCm on 6.19.x, +6% pp vs 6.18.x |

---

## Known Issues

### Current Upstream Compatibility Alerts

Before changing kernels, ROCm containers, Ollama deployment type, or DeepSeek environment variables, check the scoped [`ROCm and vLLM bugwatch`](ROCM_VLLM_BUGWATCH.md#current-strix-halo-compatibility-alerts). It currently tracks:

- one kernel-specific ComfyUI/FLUX load deadlock report;
- a reported ROCm `mmap` limit above 64GB on one Ubuntu 26.04 setup;
- a container-only Ollama UMA-reporting regression;
- a Windows bare-metal `llama.cpp` ROCm performance regression;
- a DeepSeek ROCm environment-variable trap where defining a variable as `0` can still enable its path; and
- an older ROCm playbook failure that AMD reports as passing with current pinned wheels.

These are troubleshooting signals, not proof that every Strix Halo system or every version is affected. Match the exact OS, kernel, backend, deployment type, and artifact before applying a workaround.

### Corsair/Sixunited Custom Fan Control After Kernel Updates (Community Evidence)

Fail-Safe's three-system Corsair AI Workstation 300 campaign found that two systems had previously booted without the out-of-tree `ec_su_axb35` module after a kernel update, causing dependent custom fan/power services to fail. That is a plausible major contributor to the earlier sustained-load event, not a proven sole root cause and not evidence that every Corsair or Strix Halo system needs a clock cap.

If you use this custom fan path, verify the module and services after kernel updates before sustained inference. The contributor's measured 2400 MHz tradeoff is scoped to the tested fleet. See [`THERMAL_STABILITY.md`](THERMAL_STABILITY.md) for commands, charts, raw evidence, limitations, and the open upstream fan-reset candidate.

### Kernel 6.19.x ROCm GPU Misidentification (March 2026 -- FIXED)

**Symptoms:** Without the fix, ROCm containers segfault. `ggml_cuda_init` reports `gfx1100 (0x1100)` instead of `gfx1151`.

**Fix:** Set these environment variables before running any ROCm binary:

```bash
export HSA_OVERRIDE_GFX_VERSION=11.5.1
export HSA_ENABLE_SDMA=0
```

With this fix, ROCm worked on the measured kernel 6.19.4 setup and improved prompt-processing throughput versus the older measured 6.18.14 row. See [benchmarks](#rocm-hip-usable-on-kernel-6194-with-hsa-override) for numbers.

### Qwen3.5 ROCm Hang Bug ([ROCm #6027](https://github.com/ROCm/ROCm/issues/6027))

**Symptoms:** Qwen3.5 models (35B-A3B and 27B) hang during `load_tensors` on ROCm. CPU pegs at 99.9%.

**Status:** Open. AMD confirmed working with TheRock 7.13.0a20260316+ nightlies.

**Workaround:** Use very conservative flags: `--batch-size 128 --ubatch-size 32 --flash-attn off --n-gpu-layers 1`

### GPU Clock Bug

**Symptoms:** GPU stays at 900 MHz instead of 2900 MHz, causing ~8% performance loss.

**Check:**

```bash
cat /sys/class/drm/card*/device/pp_dpm_sclk
# Should show: 2: 2900Mhz *
```

**Fix:** Force highest performance level:

```bash
echo high | sudo tee /sys/class/drm/card*/device/power_dpm_force_performance_level
```

### GFX1151 1.5X VGPR Capacity

Newer kernels (6.18.4+) recognize gfx1151's 1.5X VGPR capacity compared to standard gfx11 chips. This enables better occupancy for compute shaders. If you're on an older kernel, you may not be getting full performance.

---

## Troubleshooting

<details>
<summary><strong>DKMS mt7925 WiFi Errors During apt install</strong></summary>

You'll see this on every `apt install`:

```
Error! Bad return status for module build on kernel: 6.18.14-061814-generic
dkms autoinstall failed for mt76-mt7925(10)
```

**This is harmless.** WiFi works fine via the kernel driver. To permanently silence:

```bash
sudo dkms remove mt76-mt7925/1.5.0 --all
```

</details>

<details>
<summary><strong>Ollama "Out of Memory" Even with Small Models</strong></summary>

This happens when Ollama tries to use HIP/ROCm instead of Vulkan:

```bash
# Check current Ollama environment
systemctl show ollama | grep Environment

# Fix: ensure these are set
sudo systemctl edit ollama
# Add: OLLAMA_VULKAN=1, HIP_VISIBLE_DEVICES=-1
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

</details>

<details>
<summary><strong>ROCm Container Segfaults (Kernel 6.19.x)</strong></summary>

If your ROCm containers crash immediately with segfaults on kernel 6.19.x:

```bash
# Fix: set these BEFORE running any ROCm binary
export HSA_OVERRIDE_GFX_VERSION=11.5.1
export HSA_ENABLE_SDMA=0
export ROCBLAS_USE_HIPBLASLT=1

# Then run llama-bench or llama-server as normal
llama-bench -m model.gguf -fa 1 -ngl 999 -mmp 0 -p 512 -n 128
```

The GPU is misidentified as gfx1100 instead of gfx1151 on kernel 6.19.x. The `HSA_OVERRIDE_GFX_VERSION` forces correct identification. This is a kernel/ROCm compatibility issue that will likely be fixed in future ROCm releases.

</details>

<details>
<summary><strong>Verifying GPU Memory Configuration</strong></summary>

```bash
# Check TTM pages limit
cat /sys/module/ttm/parameters/pages_limit

# Check GTT size
cat /sys/module/amdgpu/parameters/gttsize

# Check Vulkan driver
vulkaninfo --summary 2>&1 | grep -E "driverName|driverInfo"

# Check OS-visible RAM
free -h

# Check GPU memory allocation
for file in /sys/class/drm/card*/device/mem_info*; do
  echo "$file: $(cat $file)"
done
```

</details>

<details>
<summary><strong>rocm-smi Shows Wrong VRAM</strong></summary>

For APUs with unified memory, `mem_info_vram_total` showing ~1GB is **normal**. The actual compute memory is in GTT, which should show ~128GB.

</details>

<details>
<summary><strong>tuned Not Running After Reboot</strong></summary>

```bash
# Check status
tuned-adm active

# If not running:
sudo systemctl disable --now power-profiles-daemon || true
sudo systemctl enable --now tuned
sudo tuned-adm profile accelerator-performance

# Verify it persists
tuned-adm active
systemctl is-active power-profiles-daemon
```

</details>

<details>
<summary><strong>GPU Stuck at Low Clock Speed</strong></summary>

```bash
# Check current clock
cat /sys/class/drm/card*/device/pp_dpm_sclk

# If not on highest (2900Mhz):
echo high | sudo tee /sys/class/drm/card*/device/power_dpm_force_performance_level

# To make persistent, add to /etc/rc.local or a udev rule
```

</details>

---

## Kernel and ROCm Compatibility

Based on community testing and our own findings:

| Kernel | ROCm 6.4.4 | ROCm 7.2 | ROCm 7 Nightly | Vulkan (Ollama) |
|--------|------------|----------|----------------|-----------------|
| 6.17.7 | Works (with right firmware) | Unknown | Works | Works |
| 6.18.4-6.18.14 | Works (patched) | Works | Works | Works |
| **6.19.4** | **Works (HSA fix)** | **Works (HSA fix)** | **Unknown** | **Works** |

**Key rules:**
- Kernel 6.18.4+ changed gfx1151 handling; use current ROCm builds/containers instead of old ROCm RC builds
- Kernel 6.19.x misidentifies gfx1151 as gfx1100, fixable with `HSA_OVERRIDE_GFX_VERSION=11.5.1`
- linux-firmware-20251125 breaks ROCm regardless of kernel
- linux-firmware-20260110+ is safe

> **Current measured recommendation:** Kernel 6.19.x works for both Vulkan and ROCm in this guide's May/June 2026 runs (ROCm requires `HSA_OVERRIDE_GFX_VERSION=11.5.1`). Kernel 6.18.6-6.18.14 works without the HSA workaround. Before publishing benchmark numbers, also verify Mesa, AMDVLK removal, GPU clock, and `tuned` status.

---

## Power Measurement Status

Beelink wall-power efficiency is not published yet. `powercap` is empty on this system, but `amdgpu` exposes `PPT` telemetry through `power1_average` / `power1_input`. A 2026-05-16 local PPT run measured roughly 111-113 W during Qwen3-Coder/Qwen3.6 Vulkan workloads, but this is GPU/APU telemetry, not wall power.

Community wall-power data does exist from Corsair AI Workstation 300 systems. The current issue #6 cross-section measures about 150 W / 1.6 J/token for Qwen3-Coder, 148 W / 2.0 J/token for Qwen3.6, 174 W / 3.1 J/token for gpt-oss-120b, and 137 W / 3.4 J/token for Qwen3-Coder-Next during sustained generation. Use that as practical community context, not as a Beelink claim.

A separate three-system Corsair thermal/SCLK campaign reports Linux AMDGPU socket-power telemetry from 80.90 W at a 2200 MHz cap to 118.71 W at 2600 MHz, plus 119.54 W mean in bounded stock controls. Those are socket-power readings, not wall power or Beelink measurements. See [`THERMAL_STABILITY.md`](THERMAL_STABILITY.md).

See [`POWER_BASELINE.md`](POWER_BASELINE.md), [`COMMUNITY_RESULTS.md#whole-system-power`](COMMUNITY_RESULTS.md#whole-system-power), [`data/community_power.csv`](data/community_power.csv), [`data/beelink_power_telemetry.csv`](data/beelink_power_telemetry.csv), and `scripts/sample_power.py` before adding tokens-per-watt claims.

---

## Testing Checklist

After completing setup, verify each item:

- [ ] `free -h` shows most of your installed memory, not ~31GB (~124GiB on 128GB systems; lower on 96GB systems)
- [ ] `vulkaninfo --summary` shows RADV Mesa 26.0.2+ (latest full host-state audit here: 26.1.2 on 2026-06-07; per-run raw metadata is the source of truth)
- [ ] `tuned-adm active` shows `accelerator-performance`
- [ ] `systemctl is-active power-profiles-daemon` shows `inactive`
- [ ] `cat /sys/class/drm/card*/device/pp_dpm_sclk` shows 2900Mhz with asterisk
- [ ] `cat /sys/module/ttm/parameters/pages_limit` shows 31457280
- [ ] `ollama --version` returns without error
- [ ] `ollama run qwen3.6:35b-a3b "hello"` generates at 50+ t/s
- [ ] `systemctl show ollama | grep Environment` includes `OLLAMA_VULKAN=1` and `OLLAMA_IGPU_ENABLE=1`
- [ ] `cat /etc/default/grub | grep CMDLINE` includes the GTT/TTM parameters; `amd_iommu=off` appears only if you deliberately selected the optional desktop benchmark profile
- [ ] `uname -r` shows 6.18.x+ (ROCm on 6.19.x requires HSA override -- see Known Issues)
- [ ] `dpkg -l | grep linux-firmware` does NOT show 20251125

---

## Community Resources

- [kyuz0/amd-strix-halo-toolboxes](https://github.com/kyuz0/amd-strix-halo-toolboxes) -- Community standard containers for llama.cpp (1.2k+ stars)
- [kyuz0/amd-strix-halo-vllm-toolboxes](https://github.com/kyuz0/amd-strix-halo-vllm-toolboxes) -- vLLM serving + RDMA clustering
- [kyuz0/amd-strix-halo-gfx1151-toolboxes](https://github.com/kyuz0/amd-strix-halo-gfx1151-toolboxes) -- Meta repository with all toolboxes
- [kyuz0 Backend Benchmarks Dashboard](https://kyuz0.github.io/amd-strix-halo-toolboxes/) -- Interactive benchmark comparison
- [lhl/strix-halo-testing](https://github.com/lhl/strix-halo-testing) -- Deep performance research and rocWMMA patches
- [nabe2030/hip-vs-vulkan-evo-x2](https://github.com/nabe2030/hip-vs-vulkan-evo-x2) -- Independent HIP versus Vulkan workload-crossover benchmark on Strix Halo
- [hec-ovi/vllm-awq4-qwen](https://github.com/hec-ovi/vllm-awq4-qwen) -- Experimental Qwen3.6 AWQ/DFlash vLLM path for Strix Halo
- [strixhalo.wiki](https://strixhalo.wiki/AI/llamacpp-with-ROCm) -- Community wiki
- [llm-tracker.info](https://llm-tracker.info/AMD-Strix-Halo-(Ryzen-AI-Max+-395)-GPU-Performance) -- GPU performance comparison
- [Level1Techs Forum](https://forum.level1techs.com/t/strix-halo-ryzen-ai-max-395-llm-benchmark-results/233796) -- Community benchmark results
- [Framework Community](https://community.frame.work/t/pytorch-w-flash-attention-vllm-for-strix-halo/74736) -- Framework Desktop discussions
- [ROCm Strix Halo Optimization Guide](https://rocm.docs.amd.com/en/latest/how-to/system-optimization/strixhalo.html) -- Official AMD guide

---

## Model Recommendation Guide

Not sure which model to run? Here's what we recommend based on use case:

| I want to... | Model | Size | Speed | Why |
|--------------|-------|------|-------|-----|
| **Fastest 30B-class Qwen direct row** | Qwen3-30B-A3B-Instruct-2507 (IQ4_XS) | 13.9 GB | 100.0 t/s | First direct `llama-bench` row above 100 t/s; general-instruct, not coding-specific |
| **Code** (best speed) | Qwen3-Coder 30B-A3B (Q4_K_S) | 17.5 GB | 101.0 t/s | Fastest measured coding speed on official b9851 Vulkan; speed-first quant |
| **Code** (balanced speed/quality) | Qwen3-Coder 30B-A3B (UD-Q4_K_XL) | 17.7 GB | 96-97 t/s | Strong coding default, MoE architecture |
| **Code** (best quality) | Qwen3-Coder 30B-A3B (Q8_0) | 32 GB | 51 t/s | Same model, higher fidelity quantization |
| **Chat** (general) | Qwen3.6 35B-A3B (Q4_K_M) | 20 GB | **63 t/s** | Best all-rounder, successor to 3.5 |
| **Chat** (no thinking) | Qwen3.6 35B-A3B (no-think) | 20 GB | 63 t/s | Same speed, direct answers |
| **Code** (best quality, 256K ctx) | Qwen3-Next 80B-A3B | 42.9 GB | **59 t/s** | 80B MoE, only 3B active, 256K context |
| **Chat** (smartest possible) | Qwen3-Coder-Next | 51 GB | 38 t/s | Dense 51B model, slower but smarter |
| **Reasoning / current Google route** | Gemma 4 26B-A4B IT QAT | 14.2 GB | 74.8 t/s direct; 102.7-110.0 t/s MTP server | Strong current Google-model route. Use the direct row for benchmark comparisons; use MTP only for server/speculative experiments |
| **Analyze images** | Qwen2.5-VL 7B | 6 GB | 21 t/s | Vision-language model |
| **Maximum intelligence** | Llama 3.3 70B (Q4) | ~40 GB | ~5 t/s | Slow but very capable |
| **"Can it run?"** | Llama 4 Scout 109B | 61 GB | 18 t/s | 109B model on a mini PC. RTX 4090 can't |
| **Process documents** | Qwen3.6 35B-A3B (Q4_K_M) | 20 GB | 63 t/s | Fast enough for RAG pipelines |
| **Learn / experiment** | Llama 2 7B | 3.8 GB | 52 t/s | Small, fast, well-documented |
| **Throughput testing** | Qwen3-0.6B (Q8_0) | 0.8 GB | 266 t/s | Speed ceiling benchmark |

**How to install any model:**

```bash
# Via Ollama (easiest)
ollama pull qwen3.6:35b-a3b

# For llama-bench direct (need GGUF file)
# Download from huggingface.co, place in ~/models/
```

### Understanding Model Names

```
  Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf
  |     |      |   |   |        |  |
  |     |      |   |   |        |  +-- Quantization (see Glossary)
  |     |      |   |   |        +-- "Unsloth Dynamic" quant method
  |     |      |   |   +-- Fine-tuned for instructions
  |     |      |   +-- 3B Active parameters (MoE)
  |     |      +-- 30B Total parameters
  |     +-- Optimized for coding
  +-- Model family (by Alibaba)
```

---

## Cost: Local vs Cloud

### Is a Strix Halo system worth it vs paying for cloud AI?

**Assumptions:** Qwen3.6-35B-A3B level intelligence, 1000 tokens per query, 50 queries per day.

| Option | Monthly Cost | Speed | Privacy | Offline |
|--------|-------------|-------|---------|---------|
| **ChatGPT Plus** | $20/mo | Fast | No | No |
| **Claude Pro** | $20/mo | Fast | No | No |
| **OpenAI API** (gpt-4o, 50 queries/day) | ~$15/mo | Fast | No | No |
| **Anthropic API** (Claude Sonnet, 50 queries/day) | ~$12/mo | Fast | No | No |
| **Strix Halo** (after purchase) | **~$8/mo electricity** | ~50-100.0 t/s on larger local assistant paths; small-MoE scouts can be higher | **Yes** | **Yes** |

**Break-even calculation:**

| Scenario | System Cost | Monthly Savings | Break-even |
|----------|------------|-----------------|------------|
| vs ChatGPT Plus | ~$4,349 high-end Beelink example | $12/mo | ~30 years |
| vs API heavy use (200 queries/day) | ~$4,349 high-end Beelink example | ~$50/mo | ~7.2 years |
| vs API power use (1000+ queries/day) | ~$4,349 high-end Beelink example | ~$200/mo | **~22 months** |

> **The real value is not subscription arbitrage.** It's running AI with **no rate limits, no content filters, no data leaving your machine, and no internet required**. Casual chat users should keep paying for hosted subscriptions; local hardware makes sense when privacy, offline use, heavy API usage, or large local models matter.

**Power consumption:**
- Idle: ~30W
- Under inference load: 120-140W
- Monthly electricity (8 hours/day inference): ~$8 at $0.15/kWh

---

## Use Cases

### AI Coding Assistant (Claude Code, Cursor, Continue.dev)

Ollama provides an OpenAI-compatible API. Point any coding tool at it:

```bash
# For Cursor, Continue.dev, or any OpenAI-compatible client:
# Base URL: http://localhost:11434/v1
# Model: qwen3.6:35b-a3b (or qwen3-coder-next for max quality)
# API Key: ollama (or leave empty)
```

For Claude Code specifically:

```bash
ANTHROPIC_BASE_URL=http://localhost:11434 claude --model qwen3.6:35b-a3b
```

At roughly 50-100.0 t/s on the larger local assistant paths measured here, local inference feels fast enough for code completion and review workflows. Smaller active-parameter MoE scouts can be much faster, but they answer a different model-capability question.

### ChatGPT-like Web Interface (Open WebUI)

```bash
docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```

Open `http://localhost:3000`. You get conversation history, document upload, multi-model support, and built-in RAG -- all local, no cloud.

### RAG (Document Q&A)

For querying your own documents locally:

```bash
# 1. Pull an embedding model
ollama pull nomic-embed-text

# 2. Use Open WebUI's built-in RAG (easiest)
#    or set up LangChain + ChromaDB for custom pipelines
```

For a more current local embedding route, NVIDIA Llama Nemotron Embed 1B v2 now has a first-party CPU sanity pass. It ranked a relevant Strix Halo UMA passage above an unrelated passage, returned 2048-dimensional embeddings, and reproduced the exact vector in a fresh offline process. Follow the pinned [`reproduction and raw evidence`](data/raw/2026-07-25/nemotron-embed-1b-v2-official/). Keep this scoped to local functionality: a real Dutch/English corpus, long documents, batch throughput, memory, and ROCm acceleration still need measurement.

### Fine-Tuning And GGUF Export

The measured [Unsloth Strix Halo path](UNSLOTH_STRIX_HALO.md) uses an isolated ROCm 7.2 container. It completed a Radeon GPU gate, one-step SFT smoke, checkpoint inference, `Q4_K_M` export, ROCm `llama.cpp` inference, and a post-restart load from the host-persisted artifact.

Start there before attempting a longer QLoRA campaign. The smoke proves the workflow, not useful adaptation quality or large-model training performance.

### Speech Recognition

The official Qwen3-ASR 0.6B Q8_0 GGUF now has a first-party `llama.cpp` b10107 Vulkan/RADV pass. It transcribed a known short English sample as `Front, center.` and returned the exact transcript after a fresh process. Use the exact command in the [`reproduction and raw evidence`](data/raw/2026-07-25/qwen3-asr-06b-official-gguf/).

This proves a local load/transcription path, not general ASR quality. Dutch/multilingual accuracy, long audio, streaming, real-time factor, the 1.7B tradeoff, and word-error rate remain open; `llama.cpp` currently labels audio support experimental.

### Lightweight Image Understanding

The official LFM2.5-VL 1.6B Q4_0 GGUF plus Q8_0 projector now has a first-party `llama.cpp` b10107 Vulkan/RADV pass. It correctly read the guide title, AMD Strix Halo platform, `101.0 t/s`, `140.4 t/s`, and `128 GB` from the repository image, then repeated the exact answer in a fresh process. Use the exact command in the [`reproduction and raw evidence`](data/raw/2026-07-25/lfm25-vl-16b-official-gguf/).

This is the low-download, lightweight vision route in the measured profiles. It is one image-functionality check, not a scored screenshot/photo/document benchmark.

### Image Generation

kyuz0's [ComfyUI toolboxes](https://github.com/kyuz0/amd-strix-halo-gfx1151-toolboxes) provide ROCm containers for Flux, Wan 2.2, and Hunyuan on gfx1151. For Vulkan-only: `stable-diffusion.cpp` works with the RADV driver.

AMD also publishes an [official native-Windows ComfyUI route](https://rocm.blogs.amd.com/artificial-intelligence/comfyui-windows/README.html) for Windows 11 24H2, current Adrenalin drivers, and ROCm 7.2.1, covering SDXL, Flux, and WAN workflows. That is useful official setup guidance, but this guide has not reproduced it on the Beelink or compared it with the measured Linux paths.

### Voice / TTS

Qwen3-TTS and Chatterbox TTS both run on Strix Halo with GPU acceleration. lhl's [voicechat2](https://github.com/lhl) provides a complete local AI voice chat system.

---

## Buying Guide

Current Strix Halo systems use the same AMD Ryzen AI MAX+ 395 APU with 64GB, 96GB, or 128GB LPDDR5X-8000 depending on vendor and variant. The differentiators are memory size, form factor, cooling, ports, support, stock status, price, and how much public evidence exists for the exact chassis.

Prices, coupons, and availability change quickly. Treat this as a dated **US-storefront** buyer snapshot checked on **2026-07-27**, not a permanent ranking or a checkout quote. The strongest recommendation in this guide is not only price: it is how much reproducible evidence exists for that chassis and workflow. Listed prices exclude tax and may change with region, shipping, coupons, or cart configuration; verify final cart totals before buying.

| System | Price/config snapshot checked 2026-07-27 | Evidence depth in this guide | Buyer read |
|--------|-------------------------------------------|------------------------------|------------|
| **GMKtec EVO-X2** | Official US listing starts at $1,999.99 for 64GB+1TB. The checked 128GB+2TB selection was unavailable, so the base price is not a 128GB quote. | Strong community evidence: native Ubuntu Vulkan/RADV within about 2% of the Beelink Qwen3.6 row, WSL2/HIP baseline, Qwen3-Coder follow-ups, MTP reproduction, and tuned thermal/power-policy Reddit report. | High-value candidate when the selected 128GB configuration is available and its cart total is favorable. Do not compare the 64GB base price against 128GB systems. |
| **Bosgame M5** | $2,899 for the listed 128GB+2TB configuration ($3,299 compare-at). | No dedicated same-shape guide benchmark row yet; likely relevant as a closely related platform, but not validated here like Beelink/Corsair/GMKtec/Nimo. | Interesting price comparator, but evidence depth is thinner. Buy on ports/support/return terms, not benchmark proof from this repo. |
| **Framework Desktop** | $3,149 for the 128GB Ryzen AI Max+ 395 mainboard. Full Desktop/cart pricing is regional and configuration-dependent. | External/community interest and Framework ecosystem are strong, but this guide has less same-shape imported evidence than Beelink/Corsair/GMKtec/Nimo. | Best repairability/modularity ecosystem. Needs more direct guide rows before treating it as a benchmark-proven chassis here. |
| **Beelink GTR9 Pro** | $4,349 for the listed 128GB+2TB configuration ($4,699 compare-at); current listing marks it available. | Deepest first-party evidence: this guide's primary Beelink system produced the local headline, regression-control, power-telemetry, backend, server, and current-model rows. | Most evidence-backed choice in this repo, with premium positioning in this dated comparison. Confirm the exact board/NIC revision with the seller. |
| **Corsair AI Workstation 300** | $2,999.99 for the listed 128GB/4TB configuration ($3,399.99 original); current product page marked it in stock. | Strongest community-validated fleet: three systems reproduced the Qwen3-Coder Vulkan/RADV path, plus wall-power rows, USB4/RPC cluster evidence, and a MiMo-V2.5 310B-class prompt-processing capacity row. | Best community validation if you value repeatability across multiple same-vendor systems. Stock status matters. |
| **Minisforum MS-S1 MAX** | $3,639 for the 128GB+2TB Max AI Compute Edition, with estimated shipping in mid-August. | Windows LM Studio serving/API community evidence is imported for MS-S1-Max; not a same-shape native Linux comparison. | Interesting for dual 10GbE, USB4 v2, PCIe expansion, and rack/cluster experiments. Verify exact regional SKU and shipping date. |
| **Nimo AI Mini PC** | $3,899.99 for the listed 128GB+2TB configuration; page showed it in stock. | Strong compact-chassis community bundle: large-model serving, MTP, StepFun/Qwen 122B, Gemma 4 QAT/MTP assistant-head follow-up data, and thermal context. | Useful compact 128GB option if large-model feasibility and thermal context matter more than raw headline speed. |
| **HP ZBook Ultra G1a** | HP's US configurator displayed $11,874 MSRP for the selected 128GB+1TB Ryzen AI Max+ PRO 395 configuration. | No same-shape guide benchmark evidence yet. | Portable/workstation-laptop option. Treat as a different buyer category, not a mini-PC value comparison. |

> Snapshot sources checked 2026-07-27:
> [GMKtec](https://www.gmktec.com/products/amd-ryzen%E2%84%A2-ai-max-395-evo-x2-ai-mini-pc),
> [Bosgame](https://www.bosgamepc.com/products/bosgame-m5-ai-mini-desktop-ryzen-ai-max-395),
> [Framework mainboard](https://frame.work/products/framework-desktop-mainboard-amd-ryzen-ai-max-300-series),
> [Beelink](https://www.bee-link.com/products/beelink-gtr9-pro-amd-ryzen-ai-max-395),
> [Corsair](https://www.corsair.com/us/en/p/gaming-computers/cs-9080003-na/corsair-ai-workstation-300-amd-ryzen-ai-max-395-processor-amd-radeon-8060s-igpu-up-to-96gb-vram-128gb-lpddr5x-memory-4tb-2tb-2tb-m2-ssd-win11-home-cs-9080003-na),
> [Minisforum 128GB listing](https://store.minisforum.com/products/minisforum-ms-s1-max-mini-pc?rdt_cid=4946120491028296516),
> [Nimo](https://www.nimopc.com/products/nimos-smallest-office-gaming-ai-pc-amd-ryzen-ai-max-395-up-to-5-1-ghz-128gb-lpddr5-8000mhz-16gb-8-2tb-4tb-ssd-with-3-performance-modes-up-to-120w),
> [HP US 128GB configuration](https://www.hp.com/us-en/shop/custom/hp-zbook-ultra-g1a-mobile-workstation-pc-customizable-14-inch-amd-ryzen-ai-128gb-ram-1tb-ssd-eclipse-gray-AY8K7AV_156618?catEntryId=3074457345621963823).
> Dynamic vendor pages can show different currency, stock, and coupon state by region.

> **Board/NIC revision note (Beelink GTR9 Pro):** Some, but not all, original v1.0 systems with Intel E610-XT2 networking have reported NIC recovery/disconnection failures. Beelink has published update guidance and later introduced the v2.2 board with Realtek RTL8127 networking. Because field reports vary by unit and revision, confirm the exact board/NIC version with the seller and contact Beelink support with the serial number when troubleshooting. See the [Beelink forum thread](https://bbs.bee-link.com/d/7762-gtr-9-pro-ethernet-malfunction-under-load) and Beelink's [Q1 2026 BIOS summary](https://www.bee-link.com/blogs/all/bios-update-summary-for-q1-2026).

**Recommendation tiers:**
- **Most evidence-backed in this repo:** Beelink GTR9 Pro, because it is the first-party benchmark system.
- **Best value candidate:** GMKtec EVO-X2, if the selected cart price and memory config are favorable.
- **Best ecosystem/support:** Framework Desktop -- strongest repairability/modularity story, but thinner same-shape guide evidence so far.
- **Best already community-validated vendor fleet:** Corsair AI Workstation 300 -- three systems reproduced the Qwen3-Coder Vulkan/RADV path.
- **Best for clustering/expansion experiments:** Minisforum MS-S1 MAX or Beelink GTR9 Pro v2.2 -- dual 10GbE for RDMA/cluster experiments, but verify stock, regional SKU, and board revision.
- **Compact large-model community evidence:** Nimo AI Mini PC -- useful for large-model serving/MTP/thermal context.
- **Only if you need portability:** HP ZBook Ultra G1a, with the exact regional configuration and final cart total verified separately.

> **Important:** many Chinese mini PCs in this class, including Bosgame, GMKtec, and Beelink, appear to use closely related Sixunited platform designs. Do not assume every config is literally identical, but the first native GMKtec EVO-X2 community run reproduced the guide's Qwen3.6 Vulkan/RADV row within about 2%. Pick based on price, memory size, ports, cooling, and support.

### Windows vs Linux

| Feature | Linux (recommended) | Windows |
|---------|-------------------|---------|
| LLM performance | Best-tested path; native GMKtec Vulkan/RADV reproduced the Beelink row within about 2% | LM Studio Vulkan works as a Windows serving/API path; WSL2/HIP baseline works but measured lower and with high prompt variance |
| Max model size | ~120 GB usable GPU memory via GTT | Up to 96GB VGM on 128GB systems; 109B/128B demos exist, not yet tested here |
| ROCm/HIP | Supported (6.19.x requires HSA override) | WSL2 HIP can see the GPU with DXG detection, but current community data is a baseline, not a recommended fast path |
| vLLM serving | Works | Not supported |
| Image generation | Works (ComfyUI) | Limited |
| Setup effort | Higher (this guide helps) | Lower (but slower) |

> Linux is strongly recommended for Strix Halo LLM work because it is the path with the strongest native Vulkan/RADV evidence. Windows is now represented by a community MS-S1-Max LM Studio report: Qwen3.6 Q4_K_M through LM Studio measured a 89.49 tok/s script average across mixed prompts, with long 512-token prompt rows around 69-70 tok/s. That is useful Windows serving/API evidence, not a same-shape comparison against native Linux `llama-bench`. One GMKtec EVO-X2 community report also measured WSL2/HIP at 44.05 t/s on a TG512 Qwen3.6 generation-only run, while the same contributor's native Ubuntu Vulkan/RADV run measured 61.52 t/s on the guide's TG128 shape. Treat both as useful Windows-path baselines, not a clean same-machine Windows-vs-Linux conclusion.

---

## Glossary

New to local LLMs? Here's what the technical terms mean.

<details>
<summary><strong>Click to expand glossary</strong></summary>

**APU** -- Accelerated Processing Unit. AMD's term for a chip that combines CPU and GPU on one die. Strix Halo's APU shares 128GB of memory between CPU and GPU, which is why it can run large models.

**GGUF** -- GPT-Generated Unified Format. The file format used by llama.cpp to store AI models. A .gguf file contains the model weights and metadata needed to run inference.

**Quantization** -- Reducing the precision of model weights to use less memory and run faster. Common types:
- **Q4_K_M** -- 4-bit quantization, medium quality. Good balance of size and quality.
- **Q8_0** -- 8-bit quantization. Better quality, ~2x the size of Q4.
- **UD-Q4_K_XL** -- Unsloth Dynamic 4-bit. Uses higher precision for important layers.
- **BF16** -- Full precision (16-bit). Best quality, largest size.

**MoE (Mixture of Experts)** -- A model architecture where only a subset of parameters are active for each token. A "30B-A3B" model has 30 billion total parameters but only activates 3 billion per token, making it much faster than a dense 30B model while retaining most of the intelligence.

**Dense Model** -- A model where all parameters are used for every token. Slower but potentially smarter per parameter count. A dense 7B model uses all 7 billion parameters for every token.

**Token** -- The basic unit of text for LLMs. Roughly 3/4 of a word in English. "Hello, how are you?" is about 6 tokens.

**Prompt Processing (pp)** -- How fast the model reads your input. Measured in tokens/second. Higher is better. A pp of 800 t/s means the model can read ~600 words per second.

**Token Generation (tg)** -- How fast the model writes its response. Measured in tokens/second. This is the speed you "feel" when chatting. 50 t/s feels instant. 5 t/s feels slow.

**Unified Memory** -- Memory shared between CPU and GPU. Unlike discrete GPUs (RTX 4090 has separate 24GB VRAM), Strix Halo's GPU uses the same 128GB as the CPU. This means you can load models up to ~120GB.

**GTT (Graphics Translation Table)** -- The portion of system memory that the GPU can access via Vulkan. On Strix Halo, you configure this to ~128GB so the GPU can use all available memory.

**Vulkan** -- A graphics/compute API. On Strix Halo, Vulkan is the most reliable backend for LLM inference via Ollama.

**ROCm** -- AMD's GPU compute platform (like NVIDIA's CUDA). Provides HIP backend for llama.cpp. On kernel 6.19.x, requires `HSA_OVERRIDE_GFX_VERSION=11.5.1` to work in the measured local setup. Vulkan RADV is still faster for measured generation rows, but HIP can win prompt-processing-heavy rows.

**RADV** -- Mesa's open-source Vulkan driver for AMD GPUs. AMD's only supported open-source Vulkan driver since AMDVLK was discontinued. Fastest measured default path here for Ollama, llama.cpp generation, and low-concurrency local API work.

**AMDVLK** -- AMD's former open-source Vulkan driver. [Discontinued](https://github.com/GPUOpen-Drivers/AMDVLK/discussions/416) (last release April 2025). **Uninstall it** -- even inactive, its ICD file silently hijacks Vulkan and halves pp speed.

**Ollama** -- A tool that makes running LLMs as easy as `ollama run model-name`. Handles model downloading, GPU acceleration, and provides an API. Uses Vulkan on Strix Halo.

**llama.cpp** -- The open-source C++ library that powers most local LLM inference. Supports Vulkan, ROCm/HIP, and CPU backends.

**Flash Attention** -- An optimized attention algorithm that reduces memory usage and improves speed. Always enable it on Strix Halo (`-fa 1` or `OLLAMA_FLASH_ATTENTION=1`).

**tuned** -- A Linux daemon that applies system performance profiles. The `accelerator-performance` profile gives +5-8% LLM speed on Strix Halo.

</details>

---

## FAQ

<details>
<summary><strong>What is the difference between Ollama and llama.cpp? Why is llama.cpp faster?</strong></summary>

They are not two different programs. **Ollama is a wrapper around llama.cpp.** It adds model management (`ollama pull`), a simple API, and easy commands (`ollama run`). Under the hood, it runs the same llama.cpp inference engine.

So why can llama.cpp direct be faster on Qwen3.6 and Qwen3-Coder? Two reasons:

1. **Wrapper/API overhead and run conditions.** Ollama adds layers between you and the GPU: model loading, API translation, memory management, and service behavior. The normal Ollama 0.31.2 service path measured 60.57 t/s and passed iGPU, vision, restart, and reboot checks. A separate 0.31.1 run reached 71.82 t/s, while a later same-port/same-cache comparison put 0.31.1, 0.31.2, and 0.32.0 in the same 72.55-73.20 t/s class. Both service paths required `OLLAMA_IGPU_ENABLE=1` so the Strix Halo iGPU was not dropped during GPU discovery.

2. **Bundled version.** Ollama ships with a specific llama.cpp version baked in. Direct source builds can pick up new `llama.cpp` optimizations earlier. The March b8298-to-b8460 jump gave +25% on some MoE Vulkan rows; later rows are tracked separately in [`BENCHMARKS.md`](BENCHMARKS.md).

**Think of it like a web browser:** Ollama is Chrome (easy to use, auto-updates, but bundles a specific engine version). llama.cpp direct is building Chromium from source (more work, but you get the latest engine immediately).

**What should you use?**

| Use case | Recommendation |
|----------|---------------|
| Just want it to work | **Ollama 0.31.2 system service** -- install and go; the fully qualified path reached 60.57 t/s on Qwen3.6 with `OLLAMA_IGPU_ENABLE=1` and survived restart/reboot. Controlled isolated 0.31.1/0.31.2/0.32.0 binaries later measured in the same 72.55-73.20 t/s class. |
| Want maximum speed | **llama-server** direct Vulkan/RADV -- 101.0 t/s on speed-first Qwen3-Coder, 100.0 t/s on Qwen3-30B-A3B-Instruct-2507 IQ4_XS, 96-99.6 t/s on balanced Qwen3-Coder depending on build/repeat length, 63-81 t/s on Qwen3.6 depending on quant, and 59 t/s on Qwen3-Next 80B, with the same API style as Ollama |
| Using kyuz0 containers | **kyuz0** -- they auto-rebuild on llama.cpp updates, best of both worlds |
| Benchmarking | **llama-bench** -- eliminates all overhead, pure GPU measurement |

**How to run llama-server (Ollama replacement with full speed):**

```bash
# Start llama-server with your model (OpenAI-compatible API on port 8080)
cd ~/llama-cpp-latest
AMD_VULKAN_ICD=RADV ./build-vulkan/bin/llama-server \
  -m ~/models/Qwen3.6-35B-A3B-Q4_K_M.gguf \
  -ngl 999 -fa --no-mmap -c 8192 \
  --host 0.0.0.0 --port 8080
```

Then point your tools at `http://localhost:8080/v1` instead of `http://localhost:11434/v1`. Same API style, with less wrapper overhead and more control over the exact `llama.cpp` build and flags.

</details>

<details>
<summary><strong>Can I run useful coding and chat models locally?</strong></summary>

Yes. Qwen3.6-35B-A3B and Qwen3-Coder 30B-A3B are fast enough here for practical local chat, coding, scripts, and tool use. This guide measures local performance, not model quality against hosted systems.

</details>

<details>
<summary><strong>Do I need Linux? Can I use Windows?</strong></summary>

Linux gives the best-tested performance and the strongest native Vulkan/RADV evidence. Windows works for Vulkan-based inference via Ollama/LM Studio, and AMD's Adrenalin 25.8.1+ drivers added Variable Graphics Memory support for up to 96GB VGM. The guide now includes a Windows MS-S1-Max LM Studio serving/API report and a GMKtec EVO-X2 WSL2/HIP baseline. Treat both as useful Windows-path evidence, not proof that Windows matches native Linux `llama-bench`.

</details>

<details>
<summary><strong>Is 128GB enough for the biggest models?</strong></summary>

128GB unified memory lets you run models up to ~120GB (some memory reserved for OS and GPU overhead). This covers all 70B Q4 models and most 120B MoE models. For larger models, you can cluster two Strix Halo systems via RDMA for 256GB unified memory. AMD demonstrated a 4-node cluster running a 1 trillion parameter model.

</details>

<details>
<summary><strong>How does this compare to a Mac Studio?</strong></summary>

Prices, availability, and external benchmark numbers change quickly; treat this as a dated comparison snapshot. Earlier May 2026 Mac Studio M4 Max 128GB price snapshots around $3,699 were useful for comparison, but high-memory Mac Studio availability changed quickly during the same month. Beelink's official GTR9 Pro US price snapshot is $4,349 (July 27, 2026), and this guide measures 71.82-101.0 t/s on the larger current Vulkan/Ollama headline paths, depending on model, backend, and quant, with ~215 GB/s bandwidth; Qwen3.6 also has an 81.30 t/s speed-first quant row, and smaller active-parameter MoE scouts can be higher. Apple Silicon usually wins per-model bandwidth-sensitive inference. Strix Halo's advantages are Linux flexibility, ROCm/vLLM ecosystem access, dual 10GbE on some systems, and broader vendor choice with lower-priced alternatives.

</details>

<details>
<summary><strong>Why is my speed lower than the guide says?</strong></summary>

Common causes:
1. **tuned not running or power-profiles-daemon active** -- Run `tuned-adm active` and `systemctl is-active power-profiles-daemon`. `tuned` should show `accelerator-performance`; `power-profiles-daemon` should be inactive. This alone is worth several percent.
2. **Old Mesa drivers** -- Check `vulkaninfo --summary | grep driverInfo`. Should be Mesa 26.0.2+ from the kisak-mesa PPA; exact driver metadata is recorded per run when available.
3. **Using Ollama instead of llama-bench** -- Ollama and direct `llama-bench` are different claim categories. The fully qualified 0.31.2 system service measured 60.57 t/s on Qwen3.6; controlled isolated 0.31.1/0.31.2/0.32.0 binaries later measured 72.55-73.20 t/s. All used `OLLAMA_IGPU_ENABLE=1`. The 96-101 t/s Qwen rows are direct `llama-bench`, not Ollama.
4. **GPU clock stuck low** -- Check `cat /sys/class/drm/card*/device/pp_dpm_sclk`. Should show 2900Mhz with asterisk.
5. **Wrong BIOS VRAM setting** -- Check `free -h`. On a 128GB system it should show roughly ~124-126GiB OS-visible memory; a 96GB system will be lower. If a 128GB box only shows ~31GiB, lower the UMA Frame Buffer reserve in BIOS. Use 512MB if available; if your vendor minimum is 2GB, leave it at 2GB.
6. **Different model/quantization** -- The 100.99 t/s Qwen3-Coder result is specifically Qwen3-Coder-30B-A3B Q4_K_S via RADV on official b9851 Vulkan. The older strict-clean b9179 row for the same speed-first quant remains 98.51 t/s. The 100.04 t/s result is a separate Qwen3-30B-A3B-Instruct-2507 IQ4_XS route. The balanced Qwen3-Coder UD-Q4_K_XL row is 96-99.6 t/s depending on build/repeat length. Larger or denser models are slower.

</details>

<details>
<summary><strong>Can I use this for AI coding assistants like Cursor or Continue.dev?</strong></summary>

Yes. Ollama provides an OpenAI-compatible API at `http://localhost:11434/v1`. You can point any tool that supports OpenAI API to your local Ollama:

```bash
# In Continue.dev, Cursor, or any OpenAI-compatible client:
# Base URL: http://localhost:11434/v1
# Model: qwen3.6:35b-a3b
# API Key: (leave empty or use "ollama")
```

At 50 t/s, local inference feels instant for code completion and review tasks.

</details>

<details>
<summary><strong>Can I run image generation (Stable Diffusion, Flux)?</strong></summary>

Yes. kyuz0's [ComfyUI toolboxes](https://github.com/kyuz0/amd-strix-halo-gfx1151-toolboxes) provide ROCm containers for image and video generation on gfx1151, supporting Flux, Wan 2.2, and Hunyuan models.

</details>

<details>
<summary><strong>Can I fine-tune models on this hardware?</strong></summary>

Yes, with limitations. The guide now has a measured [Unsloth/ROCm train-to-GGUF path](UNSLOTH_STRIX_HALO.md): GPU detection, a one-step SFT smoke, checkpoint inference, GGUF export, ROCm `llama.cpp` inference, and post-restart artifact loading all passed on the retail Beelink. That proves the toolchain, not useful training quality or large-model speed. For longer campaigns, kyuz0's [fine-tuning toolbox](https://github.com/kyuz0/amd-strix-halo-gfx1151-toolboxes) remains another ecosystem route. Full fine-tuning of large models is not practical compared with datacenter GPUs; use LoRA/QLoRA and validate held-out quality.

</details>

---

## Credits and References

- [kyuz0](https://github.com/kyuz0) -- Maintainer of the Strix Halo toolbox ecosystem, community standard containers
- [lhl](https://github.com/lhl) -- Deep performance research, rocWMMA patches, IOMMU/bandwidth testing
- [pablo-ross](https://github.com/pablo-ross/strix-halo-gmktec-evo-x2) -- Original GMKtec EVO-X2 setup guide
- [TechnigmaAI / Hardware Corner](https://www.hardware-corner.net/strix-halo-llm-optimization/) -- Alternative optimization guide
- [AMD](https://www.amd.com/en/developer/resources/technical-articles/2026/how-to-run-a-one-trillion-parameter-llm-locally-an-amd.html) -- Trillion-parameter LLM clustering article
- [Lychee-Technology](https://github.com/Lychee-Technology/llama-cpp-for-strix-halo) -- Pre-built llama.cpp binaries for gfx1151
- [kisak-mesa PPA](https://launchpad.net/~kisak/+archive/ubuntu/kisak-mesa) -- Latest Mesa drivers for Ubuntu
- [GPUOpen-Drivers/AMDVLK](https://github.com/GPUOpen-Drivers/AMDVLK) -- Discontinued AMD Vulkan driver; kept here only as context for the ICD hijacking issue

---

## Contributing

Found something that's wrong, outdated, or missing?

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full contribution path and the highest-value data currently wanted.

1. Open a [benchmark report](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=benchmark-report.md) with hardware, BIOS, kernel, driver, model, backend, command, and raw output.
2. Open a [power / efficiency report](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=power-report.md) with wall-power or board-power readings, idle baseline, sample interval, raw readings, and the exact benchmark command.
3. Use [Discussions](https://github.com/hogeheer499-commits/strix-halo-guide/discussions) for setup questions, early results, and comparisons.
4. PRs welcome -- especially from other Strix Halo systems (Framework, GMKtec, HP ZBook).
5. If you find a new optimization, include before/after benchmarks.

---

## Support This Guide

This guide stays free and evidence-first. If it saved you setup time or helped you choose hardware/software, the most useful support is a GitHub star, a benchmark report, a correction, or a pull request.

Financial support may fund hardware, storage, model downloads, testing time, and ongoing maintenance, but it does not influence benchmark conclusions. See [`SUPPORT.md`](SUPPORT.md) for the funding policy.

---

## Changelog

### 2026-07-27 -- Buyer Price Snapshot Refresh

- **Official US storefronts rechecked:** the buyer table now records the displayed configuration, price, and availability state for GMKtec, Bosgame, Framework, Beelink, Corsair, Minisforum, Nimo, and HP. The dated snapshot is deliberately not a tax-, shipping-, coupon-, or regional-cart quote.
- **Material changes reflected:** Beelink's listed 128GB+2TB price is now $4,349, Corsair's listed 128GB/4TB price is $2,999.99 and in stock, and Minisforum's listed 128GB+2TB Max AI Compute Edition price is $3,639 with mid-August estimated shipping. The current Beelink value is also used in the hardware comparison and break-even examples.

### 2026-07-25 -- Current Runtime, Lightweight Vision, Speech, And Retrieval

- **Ollama 0.32.3 isolated qualification passed:** same-cache Qwen3.6 measured **73.13 t/s** versus **73.20 t/s** on 0.31.2 with exact outputs. Qwen2.5-VL fully offloaded to the iGPU, read the test image correctly, and repeated after process restart. The installed 0.31.2 service remains the default until a normal package upgrade and full-host reboot pass.
- **Official `llama.cpp` b10107 capability routes added:** LFM2.5-VL 1.6B correctly read the guide image and Qwen3-ASR 0.6B transcribed a short known English sample. Both reproduced exactly after a fresh process. These are scoped function/restart smokes, not broad vision or speech-quality benchmarks.
- **Modern local embedding route added:** Llama Nemotron Embed 1B v2 ranked a relevant Strix Halo UMA passage above an unrelated passage, returned 2048-dimensional embeddings, and reproduced the exact vector offline. The measured route used CPU and remains a tiny retrieval sanity check rather than multilingual-corpus or ROCm evidence.
- **PR #25666 independently checked:** the Qwen3.6 MTP stock-versus-PR A/B preserved exact generated outputs and **80.187%** draft acceptance. Warm repeats were only **0.55%** faster on the PR head, so the result is recorded as correctness/no-regression evidence rather than a performance headline.

### 2026-07-21 -- Corsair Thermal/SCLK Evidence And Fan-Control Correction

- **Strict three-system campaign imported:** Fail-Safe's matched Corsair AI Workstation 300 sweep now has normalized CSV rows, two generated charts, a complete raw bundle, analyzer, contamination checks, cap/reset harness, and bounded stock controls.
- **Scoped buyer guidance:** 2400 MHz was the best measured conservative tradeoff on this fleet; moving to 2600 MHz added 6.39% prompt throughput and 0.87% generation while mean AMDGPU socket power increased 21.70%. This is not a universal cap recommendation.
- **Root-cause framing corrected:** historical logs showed missing `ec_su_axb35` modules and failed dependent services after kernel updates on two systems. The guide records this as a plausible major confounder, keeps the root cause unresolved, and tracks the open upstream fan-reset patch.

### 2026-07-16 -- Current Runtime, Frontier Capacity, And ROCm 7.14

- **Current direct capacity:** DeepSeek V4 Flash 284B `UD-IQ2_XXS` loaded and generated from a pinned 90.86GB ordinary GGUF on official `llama.cpp` b10034 at **155.64 pp512 / 13.27 tg128**. A deterministic smoke answered correctly; this remains low-bit capacity/current-model evidence rather than a speed or broad quality recommendation.
- **Current agent/server route:** Step 3.7 Flash 198B-A11B ROCmFPX Q3 plus its Q8 MTP draft measured **34.50 t/s at 4K** and **33.83 t/s at 16K**, passed a native tool call, and allocated 256K context on one 128GB Beelink.
- **ROCm 7.14 workaround reproduced:** in the pinned official ROCm 7.14 / PyTorch 2.11 / vLLM image, enabling hipBLASLt improved Qwen3-0.6B FP16 aggregate throughput by **40.50% / 38.96% / 41.54%** at concurrency 8/9/16. Concurrency 1 was unchanged and 4 was slightly slower, so this is a batch-8+ server profile rather than a universal tuning rule.
- **HIP integrated-host-buffer fix reproduced:** official `llama.cpp` b10046 detected the full Strix Halo UMA pool and used `ROCm_Host` model/output/compute buffers without a gfx-version override. The official binary needed the existing Ollama ROCm library path on this host, so the guide preserves both the compatibility win and the remaining packaging friction.
- **Current runtime checks:** official b10034 still showed the Vulkan MoE 8-to-9 sequence cliff on two model shapes; a same-cache Ollama 0.31.1/0.31.2/0.32.0 comparison found no material version regression; current Nemotron Omni, Cascade, AgentWorld, Audex, and CHADROCK routes were also rechecked with scoped evidence.

### 2026-07-06 -- b9888 Vulkan Sentinel And DeepSeek V4 Flash Route Triage

- **Official b9888 Vulkan sentinel checked:** Qwen3-Coder 30B-A3B `Q4_K_S` measured **1404.73 pp512 / 98.12 tg128 r50** on b9888 with the b9851/b9859-matching command shape, and **98.59 t/s** generation-only. `UD-Q4_K_XL` measured **1410.82 pp512 / 96.53 tg128 r5**.
- **Claim boundary preserved:** b9888 is the latest official `llama.cpp` runtime control, but it does not replace the stronger b9851 Qwen3-Coder **100.99 t/s** speed-first headline.
- **DeepSeek V4 Flash route triaged again:** current routes include very large ordinary GGUF artifacts, a 92.8GiB `IQ2_M` GGUF candidate whose download was too slow to complete in this pass, and a smaller 46.98GiB REAP route that needs a separate ds4 runtime. No local pass/fail or speed claim is published yet.

### 2026-07-02 -- Ollama 0.31.1 Buyer Path And b9859 Runtime Control

- **Ollama easy-path sanity check updated:** a user-local Ollama 0.31.1 binary on port 11435 measured **71.82 t/s** warm API generation mean on `qwen3.6:35b-a3b`, with a 71.62-72.05 t/s warm range after one cold run. This is Ollama API / buyer-path evidence, not direct `llama-bench`.
- **Important setup fix:** current Ollama builds can drop the Strix Halo iGPU during GPU discovery unless `OLLAMA_IGPU_ENABLE=1` is set. The setup script and README environment guidance now include that variable.
- **Official b9859 Vulkan sentinel checked:** Qwen3-Coder 30B-A3B `Q4_K_S` measured **1413.38 pp512 / 98.48 tg128 r50** on b9859 with the b9851-matching command shape, and **99.09 t/s** generation-only. `UD-Q4_K_XL` measured **1411.76 pp512 / 97.01 tg128 r5**; Gemma 4 26B-A4B `UD-Q4_K_M` measured **1323.39 pp512 / 54.18 tg128 r5**.
- **Claim boundary preserved:** b9859 is a useful current-runtime control, but it does not replace the stronger b9851 Qwen3-Coder **100.99 t/s** speed-first headline.

### 2026-07-01 -- Corsair MiMo V2.5 Capacity Evidence

- **Fail-Safe added a Corsair MiMo V2.5 capacity row:** issue #26 reports MiMo-V2.5 `UD-IQ2_M`, described by `llama-bench` as `mimo2 310B.A15B IQ2_M - 2.7 bpw`, on Corsair AI Workstation 300 `ai-2` with Fedora 44, kernel 7.0.12, Mesa RADV 25.3.6 inside the kyuz0 Vulkan container, and IOMMU off.
- **Claim boundary preserved:** the pasted CSV row is **30.65 pp512** with `n_gen=0`, so this guide treats it as prompt-processing capacity evidence, not as a tg128/generation headline.
- **Vendor/buyer value:** the row includes wall-power/GPU telemetry: Home Assistant wall power 29.7-162.4 W with a 114.14 W mean, GPU edge 40-75 C, and GPU socket power 14.098-104.021 W with a 70.92 W mean. This strengthens the Corsair evidence layer beyond Qwen speed rows.

### 2026-06-30 -- b9851 Qwen3-Coder Direct 100 t/s And Minix ER939 Community Row

- **Qwen3-Coder direct speed-first row crossed 100 t/s:** the exact `Q4_K_S` Qwen3-Coder 30B-A3B file measured **1423.05 pp512 / 100.99 tg128 r50** on the official `llama.cpp` b9851 Ubuntu Vulkan release binary with explicit `-dev Vulkan0`. This is direct `llama-bench` evidence, not MTP/server speculation. The older b9179 strict-clean **98.51 t/s** row remains preserved as historical context.
- **Balanced Qwen3-Coder latest-build control improved:** `UD-Q4_K_XL` measured **1416.79 pp512 / 99.55 tg128 r5** on b9851. Treat this as a short latest-build control unless a longer repeat is needed.
- **Gemma direct control stayed secondary:** Gemma 4 26B-A4B `UD-Q4_K_M` measured **1326.52 pp512 / 55.45 tg128 r5** on b9851, so the existing Gemma 4 26B-A4B QAT MTP route remains the useful high-throughput Gemma path.

- **Community map expanded to 11 systems/sources:** papagenic contributed a Minix Elite ER939 Ai Ollama 0.30.10 report for `qwen3.6:35b-a3b` on Ubuntu 26.04, kernel 7.0.0-22, Mesa 26.1.3, BIOS UMA 1G, and IOMMU disabled.
- **Claim boundary preserved:** the row is useful buyer-path evidence for Minix/Ollama/Ubuntu 26.04, but it is not a direct `llama-bench` headline because backend/Vulkan ICD, script details, repeats, and warm/cold state are not yet confirmed.
- **Public traction snapshot refreshed:** the guide reached **192 GitHub stars**, **9 forks**, and **4 watchers** in the 2026-07-02 GitHub API snapshot. This remains a small-niche demand signal; the main value is still reproducible public evidence that reduces buyer setup friction.
- **Runtime watchlist refreshed:** the `llama.cpp` b9851 sentinel is now measured; the later 2026-07-02 check separately measured `llama.cpp` b9859 and a user-local Ollama 0.31.1 sanity path.

### 2026-06-21 -- Traction Snapshot And ROCmFP4 Watch Lane

- **Public traction snapshot refreshed:** the guide reached **160+ GitHub stars** and **10 Strix Halo-class systems represented** in the 2026-06-21 snapshot. This is a small-niche demand signal; the main vendor value remains reproducible public evidence that reduces buyer setup friction.
- **ROCmFP4 / CHADROCK advanced lane added:** [`ROCMFP4_CHADROCK.md`](ROCMFP4_CHADROCK.md) tracks the `rocmfp4-llama` / tuned-GGUF route separately from the beginner Vulkan/RADV/Ollama path and from first-party direct `llama-bench` headline rows.
- **ROCmFP4 Crown Halo smoke added:** the `jcbtc/qwen3.6-35b-a3b-crown-halo-mtp-dynamic` artifact now has first-party Beelink load/API/MTP smoke evidence. It runs, but the high-speed community dynamic-MTP band is not yet reproduced on this HIP-only Beelink route.
- **CHADROCK ACE/SABER stability profile added:** the `jcbtc/chadrock-35b-ace-saber-rocmfp4-mtp` artifact loads and serves on the guide's Beelink/RADV path with the pinned `ciru-ai/ROCmFPX` runner. The exact 3946-token reference profile averaged 141.37 t/s over three gen512 repeats at 100% draft acceptance; 1K/8K/16K profiles measured 78.00/83.85/107.23 t/s. This is strong advanced-lane evidence and practical acceptance guidance, but still separate from direct `llama-bench` rows.
- **Nemotron 3 Nano Omni b9747 smoke added:** `unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-GGUF` `MXFP4_MOE` loads and runs directly on the official `llama.cpp` b9747 Vulkan binary at 1277.60 pp512 / 56.56 tg128. This is current NVIDIA Omni/FP4 support evidence, not a new speed headline.
- **Current model watchlist refreshed:** Kimi-K2.7-Code, GLM-5.2, MiniMax-M3, Nemotron 3 Nano Omni NVFP4/MXFP4, DeepSeek V4 Flash REAP, `llama.cpp` b9747, and Ollama 0.30.10 were triaged for practical guide value.

### 2026-06-14 -- Ciru-ai EVO-X2 NixOS / NPU / ROCmFP4 Artifact

- **GMKtec EVO-X2 NixOS evidence package linked:** ciru-ai published a public artifact for GMKtec EVO-X2 / NixOS / IOMMU-on / NPU-aware Strix Halo benchmarking, including sanitized CSV/SQLite exports and a compact public metrics index.
- **NPU sidecar evidence added:** the artifact reports +3.29% main 64k iGPU workload latency with concurrent NPU load versus +68.96% with a comparable iGPU auxiliary load, plus FastFlowLM-NPU LFM2.5 1.2B at 32k around 1646 prompt tok/s and 38.18 decode tok/s.
- **ROCmFP4 and quality-eval context added:** selected Chadrock/Qwopus/Qwen3.6/Gemma/CrownV7 rows are linked as community tuned-route evidence with quality metrics. These are not first-party Beelink direct `llama-bench` headlines.

### 2026-06-12 -- Gemma 4 QAT MTP Repeat And Guide Freshness

- **Gemma 4 26B-A4B QAT MTP repeat documented:** the matched-head `llama-server` route measured **102.69 t/s** cold, **107.42 t/s** with only T3 left among known local services, and **110.00 t/s** as the best repeat on `ac4cddeb0`. This is server/speculative evidence, not a direct `llama-bench` replacement.
- **Current setup routing improved:** the README now sends new users to `setup.sh` first, then Ollama/Open WebUI for local chat, and only then to direct `llama.cpp`, MTP, Lemonade, or ROCm/vLLM paths when they need benchmark or server control.
- **Community Beelink CachyOS ROCm/ZenDNN row added:** devoidfury contributed a second Beelink owner stack with CachyOS, kernel 7.0.11, ROCm 7.2.4, local ZenDNN, and Qwen3.6 27B MTP `UD-Q6_K_XL`. ROCm roughly doubled pp5000 versus Vulkan on that setup while decode stayed around 8 t/s, making it backend-crossover evidence rather than a decode headline.

### 2026-06-11 -- Latest ac4cddeb0 Controls And Gemma QAT Route

- **Latest-control rows added:** Qwen3-30B-A3B-Instruct-2507 stayed above 100 t/s at **100.38 t/s**, LFM2.5 stayed in the 170 t/s class at **171.17 t/s**, and Nemotron 3 Super stayed in the 18 t/s capacity class at **18.24 t/s**.
- **Gemma 4 QAT direct route added:** Gemma 4 26B-A4B IT QAT `UD-Q4_K_XL` measured **74.80 t/s** direct and became the practical current Google-model row, replacing the older non-QAT Gemma 4 row as the recommendation.
- **Negative/control evidence preserved:** Qwen3.6 27B NVFP4 loaded but was not a speed route on this Vulkan/RADV path, and the MTP smoke result remained too slow to recommend.

### 2026-06-07 -- b9544 Regression Controls

- **No Vulkan/RADV sentinel regression found:** Qwen3-30B-A3B-Instruct-2507 measured **103.18 t/s**, the exact Qwen3-Coder Q4_K_S speed-first file reproduced the 98 t/s class at **98.02 t/s r50** and **98.49 t/s generation-only**, and Qwen3-Coder UD-Q4_K_XL stayed in the 96-97 t/s class.
- **Small-MoE and capacity rows held up:** LFM2.5 measured **176.48 t/s**, and Nemotron 3 Super measured **18.93 t/s** on the b9544 control.

### 2026-06-05 -- Latest/int-dot Scout Rows

- **New speed and capacity scouts added:** LFM2.5 8B-A1B reached **170.02 t/s** generation-only, Nemotron 3 Nano reached **75.97 t/s**, and Nemotron 3 Super 120B-A12B reached **18.43 t/s** direct on one 128GB Strix Halo system.
- **Failure data kept:** DeepSeek V4 Flash and other large-model routes stayed documented as blocked or impractical where model distribution, architecture support, or storage/runtime requirements prevented a clean local benchmark.

### 2026-06-03 -- Nimo AI Mini PC Community Bundle

- **Nimo AI Mini PC evidence added:** boxwrench contributed a Ryzen AI MAX+ 395 / Radeon 8060S / 128GB Nimo bundle in issue #4 with system metadata, reproducibility notes, raw benchmark rows, thermal telemetry, and model-specific follow-ups.
- **Community map now covers 8 systems:** the guide now tracks Beelink first-party data plus three Corsair systems, two GMKtec sources, MS-S1-Max, and Nimo community evidence. This was later expanded to 11 systems/sources with a second Beelink owner stack, ciru-ai's GMKtec EVO-X2 NixOS/NPU artifact, and papagenic's Minix Elite ER939 Ai Ollama report.
- **Large-model buyer context added:** Nimo rows cover Qwen 3.5/3.6 35B, Qwen 122B-class serving, Qwen3-Coder-Next, StepFun Step-3.7-Flash, GPT-OSS/Gemma notes in the raw bundle, and DFlash negative/control evidence. These are community serving/eval rows, not first-party direct `llama-bench` headline claims.
- **Gemma 4 QAT follow-up added:** boxwrench added Gemma 4 12B, 26B-A4B, and 31B QAT Q4_0 rows with matched MTP assistant-head comparisons. The useful lesson is not a homepage headline; it is that matched QAT assistant heads can materially improve single-stream decode and acceptance. Atomic PR #26 later fixed the reported `PARALLEL=2` Gemma 4 MTP crash, so fresh post-merge 2-slot community numbers are now the useful follow-up.
- **Vendor/adoption value improved:** [`COMMUNITY_NIMO.md`](COMMUNITY_NIMO.md) summarizes what the Nimo bundle proves and what it does not prove, so vendors/reviewers can see how additional hardware reduces setup and buyer uncertainty without turning community data into endorsement language.

### 2026-06-02 -- Direct 100 t/s, Windows, And Tuned GMKtec Evidence

- **First local direct 100 t/s row added:** Qwen3-30B-A3B-Instruct-2507 `IQ4_XS` reached **100.04 t/s** tg128 r50 and **1416.03 t/s** pp512 on llama.cpp b9467 / Vulkan/RADV. This is a direct `llama-bench` result, but it is explicitly kept separate from the Qwen3-Coder 98.51 t/s headline and the Qwen3.6 MTP server route.
- **Windows LM Studio evidence added:** bennos1911 contributed a Minisforum MS-S1-Max Windows 11 / LM Studio 0.4.15 / Qwen3.6 Q4_K_M serving report with benchmark script, CSV output, and hardware telemetry. It is documented as Windows-path evidence, not as a same-shape Linux `llama-bench` comparison.
- **Tuned GMKtec 100 t/s report added:** Look_Over_There contributed a Reddit GMKtec EVO-X2 Qwen3-Coder `Q4_K_S` b9467 report where most short-context runs were around **99.90 t/s** and the best observed run reached **100.0 t/s** after about 10 runs. It is explicitly labeled as tuned thermal/power-policy evidence because the system had heatsink repaste, memory-pad reseating, lower reported temperatures, and GPU/CPU high-performance policy.
- **Community signal updated:** community results now include Beelink first-party data plus Corsair, GMKtec, and MS-S1-Max community evidence across Linux Vulkan/RADV, WSL2/HIP, Windows LM Studio, wall-power, RPC, USB4 tuning, and tuned thermal/power-policy reports.

### 2026-06-01 -- Watchlist, Controls, And Sharing Hygiene

- **Upstream watch rechecked:** ROCm production remains **7.2.4**, vLLM has moved to **0.22.1**, and the previous isolated Ollama **0.24.0** check did not change the then-installed Ollama 0.23.1 guidance at that time.
- **No new headline from latest llama.cpp direct reruns:** the 2026-06-01 `de6f727aa` Qwen3-Coder direct check measured **95.55 t/s** tg128 with `mmap=0`, so the direct headline stays at **98.51 t/s** on the b9179 strict-clean speed-first row.
- **Qwen3.6 27B MTP control confirmed:** the latest-build rerun measured **7.61 t/s** without MTP and **14.69 t/s** with MTP, so the official dense 27B Q8_0 route remains useful negative evidence rather than a speed candidate. Details live in [`PERFORMANCE_NOTES.md`](PERFORMANCE_NOTES.md).
- **Community hygiene improved:** responsible-sharing guidance was added to [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`SHARE.md`](SHARE.md), and Fail-Safe's `.gitignore` PR added macOS/Windows cache-file ignores for cleaner community contributions.

### 2026-05-27 -- Latest b9360 MTP Breaks 100 t/s Server Average

- **MTP route crossed 100 t/s broad average:** llama.cpp b9360 (`6b4e4bd58`) with Mesa/RADV 26.1.1 pushed Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn to **101.16 t/s** best six-prompt average with `draft-n=2`, `--poll 100`, and `-ub 1024`. Three t16 repeats landed at **101.15 / 101.10 / 101.06 t/s**.
- **At that date, still not a direct 100 t/s claim:** b9360 direct Qwen3-Coder Q4_K_S measured **97.23 tg128**, and UD-Q4_K_XL measured **92.60 tg128**. The Qwen3-Coder direct row remained b9179 Q4_K_S **98.51 t/s** and balanced b9049/b9010 **96-97 t/s** until the later 2026-06-02 guide update added a separate Qwen3-30B-A3B-Instruct-2507 direct 100.04 t/s row.
- Added raw evidence under `data/raw/2026-05-27/latest-llamacpp-b9360/` and updated `BENCHMARKS.md`, `MTP_SPECULATIVE_DECODING.md`, `data/benchmarks.csv`, `data/mtp_speculative.csv`, and `data/headline_claims.csv`.

### 2026-05-26 -- Latest b9334 MTP And Direct Rerun

- **MTP route improved again:** llama.cpp b9334 (`192d8ae`) with Mesa/RADV 26.1.1 raised the local Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn six-prompt average to **98.57 t/s** with `draft-n=3`; the best b9334 prompt reached **116.75 t/s**.
- **At that point, still not a broad 100 t/s claim:** repeated b9334 MTP runs landed around **97.76-98.57 t/s** depending on thread/poll settings. This was close and valuable, but later got superseded by the b9360 `-ub 1024` MTP rerun.
- **Direct latest-stack check stayed below the headline:** llama.cpp b9334 direct Qwen3-Coder Q4_K_S measured **96.27 tg128**, and UD-Q4_K_XL measured **94.15 tg128**. The existing direct headline remains the b9179 Q4_K_S **98.51 t/s** strict-clean row and the balanced b9049/b9010 **96-97 t/s** UD row.
- Added raw evidence under `data/raw/2026-05-26/latest-llamacpp-b9334/` and updated `BENCHMARKS.md`, `MTP_SPECULATIVE_DECODING.md`, `data/benchmarks.csv`, `data/mtp_speculative.csv`, and `data/headline_claims.csv`.

### 2026-05-26 -- GMKtec Qwen3-Coder Full Follow-Up

- **GMKtec Qwen3-Coder full row:** mottledMantis added the requested full `pp512/tg128` Qwen3-Coder 30B-A3B UD-Q4_K_XL b9235 run on GMKtec EVO-X2: **1157.29 pp512 / 91.40 tg128**.
- **Command-shape caveat preserved:** the full row used `-b 512 -ub 512`, `flash_attn=0`, and `use_mmap=1`, so it is documented as portability and flag-sensitivity evidence, not as an apples-to-apples replacement for the Beelink headline row.
- Added the raw CSV under `data/raw/2026-05-19/community-gmktec-qwen-coder-issue17/` and updated `COMMUNITY_RESULTS.md`, `CONTRIBUTORS.md`, `BENCHMARKS.md`, `SHARE.md`, and `data/community_results.csv`.

### 2026-05-20 -- GMKtec MTP And Qwen3-Coder Community Follow-Up

- **GMKtec MTP reproduction:** mottledMantis reproduced the exact Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn route from the guide on a GMKtec EVO-X2 with Ubuntu 26.04, kernel 7.0.0-15, Mesa RADV 26.0.3, and llama.cpp b9235. `draft-n=2` averaged **93.29 t/s** over six prompts, slightly above the local Beelink b9235 92.30 t/s row. This strengthens the MTP route but still is not a broad 100 t/s claim.
- **GMKtec Qwen3-Coder baseline:** the same contributor added a Qwen3-Coder 30B-A3B UD-Q4_K_XL b9235 generation-only row at **92.11 t/s**. This is lower than the Beelink/Corsair b9049 rows, but useful as a GMKtec/latest-stack baseline and as evidence that build/model/source/host-state details matter.
- Added raw community artifacts under `data/raw/2026-05-19/community-gmktec-*`, updated `COMMUNITY_RESULTS.md`, `data/community_results.csv`, and `data/mtp_speculative.csv`.

### 2026-05-19 -- Latest llama.cpp MTP Rerun

- **Latest MTP master rerun at the time:** llama.cpp b9235 (`d14ce3dab`) raised the Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn six-prompt average to **92.30 t/s** with `draft-n=3`. The fastest prompt in this rerun was **109.21 t/s**; the older b9187 sweep held the best single-prompt MTP result at **110.61 t/s** until the later b9334 rerun.
- **Official 27B MTP Q8_0 checked:** `ggml-org/Qwen3.6-27B-MTP-GGUF` was tested on the same b9235 Vulkan/RADV stack. It reached **7.74 t/s** without MTP and **14.59 t/s** with the best MTP setting, making it a useful negative result rather than a speed/headline candidate.
- Added raw evidence under `data/raw/2026-05-19/` and updated the MTP CSV/claim index.

### 2026-05-17 -- MTP, Wall Power, And Community Flow

- **MTP speculative decoding documented:** Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn reached **90.80 t/s** average over six `llama-server` prompts and **110.61 t/s** on the best prompt. This is a server/speculative result, not a replacement for the direct `llama-bench` headline and not a broad 100 t/s average.
- **Qwen3-Coder ngram server route checked:** Qwen3-Coder Q4_K_S with `llama-server` ngram speculation reached **95.21 t/s** average, below the direct 98.51 t/s speed-first headline.
- **Community wall-power cross-section added:** Fail-Safe's Corsair AI Workstation 300 power data now covers Qwen3-Coder, Qwen3.6, gpt-oss-120b, and Qwen3-Coder-Next, with sustained generation rows from about **137-174 W** and **1.6-3.4 J/token**.
- **Contribution flow tightened:** `CONTRIBUTING.md` and the benchmark/power issue templates now ask for the metadata needed to turn community reports into structured evidence.
- Added raw evidence under `data/raw/2026-05-17/` and `data/raw/2026-05-10/community-power-issue6/`.

### 2026-05-16 -- Latest-Stack b9172 Spot Check

- **Qwen3-Next 80B improved:** llama.cpp b9172 with Vulkan/RADV confirmed **59.06 t/s** tg128 and **751.70 pp512**, replacing the old 54.92 t/s b8933 row as the best current 80B Qwen-family result.
- **Qwen3-Coder speed-first peak:** b9179 plus Q4_K_S confirmed **98.51 t/s** r50 after fixing the `tuned`/`power-profiles-daemon` conflict and pausing benchmark noise. This is a speed-first quant row, not the balanced UD default.
- **No main headline speedup from b9172:** Qwen3-Coder UD, Qwen3.6, and gpt-oss-120b did not beat the current b9049/b9010 balanced headline rows.
- **Ollama 0.24.0 isolated check:** Qwen3.6 measured **49.05 t/s** warm generation, effectively identical to the same-prompt Ollama 0.23.1 control at **49.09 t/s**.
- **ROCm nuance confirmed again:** Lemonade ROCm b1259 won Qwen3-Next pp512 (**800.38** vs Vulkan **751.70**), but Vulkan/RADV won tg128 (**59.06** vs ROCm **49.57**). The guide now avoids "RADV wins everything" wording and keeps the beginner rule focused on generation-heavy GGUF chat/coding.
- Added raw evidence under `data/raw/2026-05-16/`.

### 2026-05-07 -- Latest-Stack Rerun

- **llama.cpp b9049 rerun:** Qwen3-Coder 30B-A3B measured **96.76 t/s** generation in the max-performance guide-flags confirmation; Qwen3.6 35B-A3B measured **62.56 t/s** on the balanced UD row and **81.30 t/s** on the speed-first Q4_0 row.
- **Ollama upgraded to 0.23.1:** Qwen3.6 API warm average remained **50.51 t/s**, matching the 0.21.2 baseline.
- **gpt-oss-120b local check:** ggml-org MXFP4 split GGUF loaded locally and measured **55.57 t/s** tg128, **726.99 t/s** pp512, and prompt processing through 65K tokens via llama.cpp b9049 Vulkan/RADV.
- **HIP/Vulkan workload split added:** local spot check shows HIP winning pp16384 and Vulkan winning tg128 on both Qwen3.6 and Qwen3-Coder rows; see [`BACKEND_CROSSOVER.md`](BACKEND_CROSSOVER.md).
- **ROCm/vLLM bugwatch added:** current upstream ROCm/vLLM release and issue status moved to [`ROCM_VLLM_BUGWATCH.md`](ROCM_VLLM_BUGWATCH.md).
- **Headline range tightened:** current direct llama.cpp headline range became **63-97 t/s** for the balanced rows. The previous b9010 Qwen3-Coder peak of **97.24 t/s** remains in the data as historical evidence, and Qwen3.6 added an **81.30 t/s** speed-first quant row.
- Added clean raw evidence under `data/raw/2026-05-07/latest-stack-rerun/clean-b9049-rerun/`.

### 2026-05-03 -- Controlled Qwen3-Coder Headline Rerun

- **Qwen3-Coder 30B-A3B benchmark updated:** controlled b9010 Vulkan RADV rerun averaged **97.24 t/s** generation and 1346 pp512 across two separate `-r 20` runs.
- **Qwen3.6 UD rerun:** controlled b9010 Vulkan RADV rerun averaged **63.06 t/s** generation and 1109 pp512 across two separate `-r 20` runs. The old "UD costs 13%" warning was not reproduced on the current stack.
- **Ollama Qwen3.6 rerun:** controlled API test averaged **50.5 t/s** warm generation across 10 runs, replacing the older 45-46 t/s easy-path claim. Current Qwen3.6 Ollama overhead is about 20-21%, not ~30%.
- **Multi-user Qwen3.6 serving:** `llama-server` continuous batching reached **162 t/s aggregate** at `-np 8` with ~0.31 s TTFT, then plateaued at 166 t/s at `-np 16`.
- **Multi-user Qwen3-Coder serving:** `llama-server` continuous batching reached **173 t/s aggregate** at `-np 8`; `-np 16` regressed to 130 t/s aggregate.
- **Local long-context prompt scaling:** Qwen3.6 processed 64K prompts at **740 t/s** and Qwen3-Next 80B processed 64K prompts at **544 t/s** on Vulkan RADV.
- **Filled-KV decode:** Qwen3.6 generated **41.4 t/s after a 64K f16 prompt**; q4_0 KV raised decode to **51.3 t/s** but increased total request time from 73.5 s to 90.0 s because prompt ingest slowed.
- **128K filled-KV decode:** Qwen3.6 generated **32.2 t/s after 128K** and Qwen3-Next 80B generated **29.1 t/s after 128K**, both without truncation.
- **Real-corpus 64K check:** using this guide's own documentation as the prompt, Qwen3.6 decoded at **40.8 t/s after ~65K tokens** and Qwen3-Next 80B at **37.8 t/s after ~64K tokens**. Prompt ingest was slower than synthetic prompts, but decode-after-fill barely changed.
- **ROCm HIP spot check:** current local HIP b8460 path is usable with the HSA override, but remains behind Vulkan for short-context tg: Qwen3.6 **52.7 t/s** and Qwen3-Coder **73.7 t/s**.
- At that point, the headline range moved from **65-87 t/s** to **65-97 t/s**. This was later tightened to **63-97 t/s** for balanced rows in the 2026-05-07 rerun, extended to **63-98.5 t/s** by the 2026-05-16 Qwen3-Coder speed-first Q4_K_S row, extended with a separate **100.04 t/s** Qwen3-30B-A3B-Instruct-2507 IQ4_XS direct row on 2026-06-02, and later lifted to **101.0 t/s** for Qwen3-Coder Q4_K_S on official b9851. The previous 87.11 t/s result remains in `data/benchmarks.csv` as historical-local data.
- Added raw benchmark output under `data/raw/2026-05-03/` so the new headline can be audited.

### 2026-05-01 -- Price Audit + Documentation Reconciliation

- **Beelink price audit:** The official GTR9 Pro page now lists the 128GB+2TB variant at **$4,399** with a $4,699 compare-at price. Earlier snapshots and checkout prices were substantially lower, so the guide no longer uses the old lower Beelink figure as a headline claim.
- Removed stale "Strix Halo is much cheaper than DGX Spark" wording. At the current Beelink official price, the gap to DGX Spark is only about $300, while lower-priced Strix Halo systems still exist.
- Updated cost, hardware comparison, buying guide, and Mac Studio FAQ language so price-sensitive claims are clearly date-bound.

### 2026-04-26 -- April Update + Qwen3.6 + Qwen3-Next 80B Benchmarks

- **AMDVLK ICD hijacking discovered:** All "pp regression" findings (b8460 vs b8933, Mesa 26.0.2 vs 26.0.5) were caused by AMDVLK's `/etc/vulkan/icd.d/amd_icd64.json` silently overriding RADV. No actual regression exists. [Corrected on #22375](https://github.com/ggml-org/llama.cpp/issues/22375). All benchmarks re-verified on actual RADV
- **Qwen3.6-35B-A3B benchmark:** **64 t/s** tg, 1064 pp512 via Vulkan RADV. Drop-in replacement for Qwen3.5 with better coding/reasoning quality, identical speed. The old UD-Q4_K_M penalty note is superseded by the May 2026 controlled rerun.
- **Qwen3-Next 80B-A3B benchmark:** **55 t/s** tg, 657 pp512 via Vulkan RADV (b8933). 80B MoE (3B active) with 256K context window. Faster than the 51B dense Qwen3-Coder-Next (38 t/s)
- **Gemma 4 26B-A4B benchmark:** 48.5 t/s tg, 1142 pp512 via Vulkan RADV (b8933). First Strix Halo benchmark for this model. Includes KV cache quantization warning (3.5x worse quality degradation vs Qwen at q8_0)
- **Llama 4 Scout 109B benchmark:** 18.3 t/s tg, 331 pp512 via Vulkan RADV (b8933). 109B parameter model running on a mini PC -- RTX 4090 can't load this
- Merged PR #1: vulkan-tools install check in setup.sh (thanks @ignasivt)
- Updated April price snapshot for Beelink, Corsair, and GMKtec; superseded by the May 1 price audit above
- Added linux-firmware-20251125 source attribution and downgrade instructions
- Added Ubuntu 26.04 LTS note (Wayland-only, testing in progress)
- **Ollama upgraded to 0.21.2:** FA now enabled by default. Original Qwen3.6 via Ollama result was 45.5 t/s; superseded by the May 2026 controlled 50.5 t/s rerun.
- **Ollama ROCm confirmed working** on gfx1151 with `HSA_OVERRIDE_GFX_VERSION=11.5.1` (Ollama 0.20.4). Benchmarked: 42.4 t/s tg vs Vulkan's 46.6 t/s (-9%). Vulkan still recommended for speed

### 2026-03-21 -- Performance Breakthrough + Beginner Content

**Performance discoveries:**
- llama.cpp b8298 to b8460 = +25% tg and +24% pp on MoE models (52 to 65 t/s tg, 868 to 1080 pp512)
  - Key PRs: #19625 (FA refactor), #20551 (graphics queue), #20334 (GDN shader)
  - +25% breaks down as ~14% generic (both backends got this) + ~11% Vulkan-specific
  - Dense models show <2% change (already at bandwidth ceiling)
- RADV now beats AMDVLK on both pp AND tg with latest build (old AMDVLK tg advantage gone)
- Exceeded theoretical tg ceiling: measured 65 t/s vs calculated max of ~57 t/s. The standard formula (bandwidth / active_model_size) underestimates MoE performance because it ignores caching and memory access optimizations in newer llama.cpp builds. The real ceiling is a moving target.
- RADV now beats ROCm on both pp (1080 vs 1047) and tg (65 vs 55) on same b8460 build
- ROCm works on kernel 6.19.4 with `HSA_OVERRIDE_GFX_VERSION=11.5.1` + `HSA_ENABLE_SDMA=0`
- ROCm b8460 got +14% tg from generic improvements (47.87 to 54.67)
- Batch/ubatch sweep: default 512 is optimal, no tuning headroom left

**New benchmarks:**
- Llama 3.1 70B (4.8 t/s, 94% of theoretical ceiling, doesn't fit on RTX 4090)
- Qwen3-Coder-30B UD-Q4_K_XL (87 t/s tg via RADV, superseded by the May 2026 97 t/s controlled rerun)
- Qwen3-0.6B (266 t/s tg, 13,112 pp512)
- Extended context scaling (pp flat from 512 to 8K, only 3% drop)

**Beginner content:**
- Ollama vs llama.cpp FAQ with browser analogy and llama-server setup
- Model recommendation guide (10 use cases)
- Cost comparison (local vs cloud with break-even analysis)
- Buying guide (7 systems with a historical March 2026 price snapshot and Beelink board/NIC revision guidance)
- Glossary (20+ terms for beginners)
- FAQ (8 common questions)
- Use cases (Claude Code, Cursor, RAG, image gen, TTS)
- Windows vs Linux comparison

**Infrastructure:**
- One-command setup script (`setup.sh`)
- Auto-update script for llama.cpp (`update-and-build.sh`)
- CONTRIBUTING.md and initial GitHub issue templates; expanded in later May updates for benchmarks, power reports, model requests, bugs, suggestions, and impersonation/security reports
- Historical launch release v1.0.0; latest release is v2.2.0 from 2026-05-17
- 19 topics for discoverability
- GitHub stars + last-commit badges

**Fixes:**
- At that time, prices were verified against current retail (March 2026 snapshot)
- DGX Spark comparison is now apples-to-apples (same model, same context)
- Fixed 12 outdated "ROCm broken on 6.19.x" references
- A low BIOS UMA reserve is mandatory, not just speed-neutral: use 512MB if available, but 2GB is fine when that is the vendor minimum
- Vulkan Driver Comparison updated with b8460 data
- RADV_PERFTEST env vars (cswave32, nogttspill) tested and found to be -10% slower. Don't use.
- Posted findings on [llama.cpp Vulkan discussion](https://github.com/ggml-org/llama.cpp/discussions/10879#discussioncomment-16235771)

### 2026-03-20 -- Major Rewrite

- Complete rewrite with live benchmarks on current system
- Added: Kernel 6.19.x ROCm fix (HSA_OVERRIDE_GFX_VERSION=11.5.1)
- Added: Mesa 26.0.2 results (+4-5% tg improvement over 26.0.1)
- Added: qwen3-coder:30b-a3b-q8_0 benchmarks (51.4 t/s -- fastest model in that initial run)
- Added: Long context performance data from lhl (Vulkan vs ROCm at 32K)
- Added: rocWMMA status update (upstream broken, lhl's tuned branch works)
- Added: vLLM setup and known issues
- Added: RDMA clustering section
- Added: Kernel/ROCm compatibility matrix
- Added: linux-firmware-20251125 warning
- Added: LLVM compiler regression workaround
- Added: Qwen3.5 ROCm hang bug (ROCm #6027)
- Added: Backend decision guide
- Added: Testing checklist
- Added: Collapsible troubleshooting sections
- Updated: ROCm HIP works on kernel 6.19.4 with HSA override (even +6% faster pp than 6.18.14)
- Updated: All benchmark numbers re-measured
- Updated: Replaced `nano` instructions with `tee` for copy-paste ready commands
- Corrected: rocWMMA is no longer blanket "don't use" -- lhl's tuned branch is best for long context
- Historical benchmark correction: `iommu=pt` did not improve the measured memory-read result; later buyer guidance separated the faster `amd_iommu=off` desktop profile from NPU and mobile-suspend requirements

### Initial Release

- Basic setup guide based on pablo-ross' GMKtec guide
- Ollama Vulkan configuration
- ROCm container setup

---

## Next Useful Tests

These are the highest-value tests to add next, because they answer practical buyer/setup questions that current evidence only partially covers:

- **Lemonade/FastFlowLM NPU on Linux:** local preflight shows `amdxdna` and `/dev/accel/accel0`, but XRT/FastFlowLM are not installed. Next step is a separate NPU lane: install XRT/FastFlowLM, reboot, run `flm validate`, then test small Qwen/Gemma rows for speed and power.
- **Same-machine Windows native Vulkan/Ollama/LM Studio vs Linux:** Windows LM Studio and WSL2/HIP now have community baselines, but the most useful beginner answer is still a same-machine native Windows app result versus native Linux Vulkan/RADV with the same model and benchmark shape.
- **More GMKtec/Bosgame/Framework native Linux reproductions:** The first GMKtec native result matched within about 2%; more vendors turn the guide from one-machine evidence into a platform map.
- **DeepSeek V4 Flash current route:** the pinned 90.86GB ordinary `UD-IQ2_XXS` GGUF now loads and generates directly on official b10034 at 13.27 tg128 and passes a basic deterministic check. The smaller 46.98GiB REAP route still needs its separate ds4 runtime; future work should compare quality/runtime tradeoffs rather than repeat the resolved ordinary-GGUF load test.
- **Tokens per watt with wall-power data:** Fail-Safe supplied valuable Corsair wall-power telemetry, and this guide now has Beelink amdgpu PPT telemetry. A Beelink wall-meter run would make the efficiency story publishable.
- **NPU/iGPU telemetry tooling:** `xdna-top` and similar tools could make NPU-sidecar and iGPU contention claims easier to verify, but should be documented as instrumentation until they produce measured model rows.
- **Lucebox / DFlash / PFlash:** highest-upside experimental route for 27B long-prompt + generation workloads, but local preflight currently needs an isolated ROCm/HIP dev toolchain with `hipcc` and rocWMMA.
- **vLLM/AWQ/DFlash throughput:** keep this experimental until it has a reproducible OpenAI-compatible server row that competes with `llama-server`/Ollama for a real use case. Plain AWQ smoke works, but it is not the fastest default.
- **Future Strix Halo successors:** Gorgon Halo / Ryzen AI Max 400 and later Medusa Halo / Ryzen AI Max 500 should be treated as future comparison targets, not current setup advice.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

---

*Found this guide useful? Give it a star on GitHub -- it helps other Strix Halo owners find it. Found something wrong? [Open an issue](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new/choose).*
