# AMD Ryzen AI Halo Context

**Status:** the AMD launch statements below date from July 2026 and are vendor statements, not measurements. The section [Validated Versions: Reference Platform Versus Retail Systems](#validated-versions-reference-platform-versus-retail-systems) was checked on 2026-09-30 and 2026-10-01; the rest of this page has not been re-checked since July 2026.

This page explains how AMD's public Ryzen AI Halo / Ryzen AI Developer Platform direction relates to this independent Strix Halo local-AI guide. AMD launched the Ryzen AI Halo Developer Platform publicly in July 2026 and positions it as a preconfigured local-AI development system with 128GB unified memory, AMD-curated playbooks, and support for models up to 200B parameters.

It is not a benchmark page and it is not an AMD endorsement. Use it as platform context: AMD is publicly positioning Ryzen AI Halo-class hardware for local AI and developer workflows, while this repository documents the practical setup, benchmark evidence, failures, caveats, and community reproductions needed to make that hardware less confusing for buyers.

## Why This Matters

AMD's Ryzen AI Halo messaging makes the product category easier to explain:

- high-memory unified AMD local-AI systems
- integrated Radeon 8060S-class graphics
- local LLM and agentic workloads
- open local-AI software paths such as Ollama, `llama.cpp`, vLLM, and LM Studio
- developer systems meant to make local AI easier to use and test

AMD's reference platform also introduces a Best Known Configuration, an AMD Ryzen AI Developer Center, Variable Graphics Memory controls, and official playbooks for Ollama, Lemonade, vLLM, agents, fine-tuning, and multi-node work. That is a useful vendor-supported baseline. It is not automatically the same setup as a retail Beelink, GMKtec, Corsair, Framework, Minisforum, Nimo, or other Strix Halo system.

That is useful context, but it does not answer the buyer's practical questions by itself:

- Which BIOS settings should I use?
- Does Ubuntu see the memory correctly?
- Should I start with Ollama, direct `llama.cpp`, `llama-server`, ROCm/HIP, or vLLM?
- Which model and quant should I try first?
- Which benchmark claims are direct `llama-bench`, and which are server/MTP/API results?
- What works on Beelink, GMKtec, Corsair, Nimo, Minisforum, Framework-class, or other Strix Halo systems?
- What fails, regresses, or needs special runtime support?

This repository is the practical evidence layer for those questions.

## Reference Platform Versus Retail OEM Systems

Keep these two evidence types separate:

| AMD Ryzen AI Halo reference-platform context | Independent retail-OEM evidence in this guide |
| --- | --- |
| AMD-provided BIOS, recovery image, Developer Center, software sync, and Best Known Configuration | Vendor-specific BIOS labels, Ubuntu setup, kernel parameters, Mesa/RADV selection, ROCm experiments, and measured commands |
| AMD-configured Variable Graphics Memory controls | Beelink and community UMA/GTT/IOMMU behavior documented per system |
| Official AMD Playbooks and preinstalled applications | Reproduction notes showing whether equivalent workflows work on retail systems |
| AMD platform performance and capacity claims | First-party Beelink and separately labeled community benchmark evidence |

The highest-value follow-up is a compatibility matrix that runs selected AMD Playbooks on retail Strix Halo systems and records whether each workflow works unchanged, needs an OEM-specific adjustment, or remains blocked. That turns official platform guidance into practical cross-OEM buyer evidence without implying AMD or OEM endorsement. It is listed in [`SPONSOR_ROADMAP.md`](SPONSOR_ROADMAP.md) and has not been started.

## Validated Versions: Reference Platform Versus Retail Systems

AMD's playbooks repository records validated software versions per hardware category (`reference`, `apu`, `gpu`) in [`playbooks/dependency-versions.json`](https://github.com/amd/playbooks/blob/main/playbooks/dependency-versions.json) (file read 2026-09-30). In that file ROCm 10.0.0 and PyTorch 2.13 are listed for the `apu` category as well as for the reference platform. The Linux driver for `apu` is listed as the latest inbox driver. Several applications are pinned on the reference platform only, for example Lemonade 11.8 and vLLM 0.27, and are listed as `Latest` elsewhere; the file says that CI tests the current release there.

Whether a retail Ryzen AI Max+ system falls under AMD's `apu` category is not verified here, and this guide has not run these playbooks on a retail system (not measured here). AMD's [Ryzen AI Halo product page](https://www.amd.com/en/products/processors/desktops/ryzen/ryzen-ai-halo.html) lists a Halo configuration with the Ryzen AI Max+ PRO 495 and 192GB memory support as "coming soon" (checked 2026-10-01). This guide has no measurement of any Ryzen AI Max PRO 400 Series system.

## How This Guide Fits

The guide turns the general "Ryzen AI Halo can run local AI" story into reproducible public evidence:

| Buyer or vendor question | Where this guide helps |
| --- | --- |
| What should a new owner do first? | [`README.md#quick-start-6-steps`](README.md#quick-start-6-steps), [`setup.sh`](setup.sh), [`STRIX_HALO_LOCAL_LLM_SETUP.md`](STRIX_HALO_LOCAL_LLM_SETUP.md) |
| Which local chat path is easiest? | Ollama Vulkan/RADV guidance in [`STRIX_HALO_LOCAL_LLM_SETUP.md`](STRIX_HALO_LOCAL_LLM_SETUP.md) |
| Which direct benchmark claims are real? | [`data/headline_claims.csv`](data/headline_claims.csv), [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md), [`data/raw/`](data/raw/) |
| What can one 128GB-class system run? | [`CURRENT_MODELS.md`](CURRENT_MODELS.md), [`BENCHMARKS.md`](BENCHMARKS.md) |
| What differs across OEM systems? | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md), [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md) |
| What is still experimental? | [`ROCM_VLLM_BUGWATCH.md`](ROCM_VLLM_BUGWATCH.md), [`ROCMFP4_CHADROCK.md`](ROCMFP4_CHADROCK.md), [`MTP_SPECULATIVE_DECODING.md`](MTP_SPECULATIVE_DECODING.md) |
| What should vendors improve or clarify? | [`ONE_PAGE_BRIEF.md`](ONE_PAGE_BRIEF.md), [`SPONSOR_ROADMAP.md`](SPONSOR_ROADMAP.md), [how this guide works with vendors](VENDOR_DISCLOSURE.md#how-we-work-with-vendors) |

The adoption value is simple: a buyer who can copy a working setup, inspect raw benchmark evidence, and understand caveats is more likely to trust, keep, and recommend the hardware.

## Claim Boundary

This page should not be cited as:

- official AMD validation of this repository
- official Beelink, Framework, GMKtec, Corsair, Minisforum, Nimo, or OEM endorsement
- proof that every Ryzen AI Halo-class system performs like the primary Beelink result
- proof that an experimental ROCm, vLLM, MTP, NPU, or ROCmFP4 path is ready for beginners

Keep those claims separated. Official AMD pages describe AMD's platform direction. This guide supplies independent measured setup and benchmark evidence.

## Current Watch Items

These are platform-alignment items worth watching or testing because they affect buyer confidence and vendor value:

| Area | Why it matters |
| --- | --- |
| Latest `llama.cpp` official releases | Regression checks show whether the copyable Vulkan/RADV path stays stable as upstream changes. |
| Latest Ollama releases | Ollama is the easiest buyer path, so a small setup regression can affect many new owners. |
| ROCm/HIP and vLLM on `gfx1151` | Useful for prompt-heavy, batching, and server workflows, but still separate from the beginner Vulkan/RADV path. |
| NPU sidecar workflows | The NPU may be most useful for background agent, memory, transcription, or auxiliary tasks while the iGPU serves the main LLM. |
| OEM BIOS and memory behavior | UMA, IOMMU, GTT, thermal limits, and power policy can change the buyer experience across vendors. |
| Community evidence from more systems | More Beelink, GMKtec, Framework, Corsair, Minisforum, Nimo, HP, and other Strix Halo-class rows reduce "works only on one box" risk. |

## Sources

- AMD Ryzen AI Halo product and performance context: <https://www.amd.com/en/products/processors/desktops/ryzen/ryzen-ai-halo.html>
- AMD Ryzen AI Developer Platform context: <https://www.amd.com/en/blogs/2026/amd-ryzen-ai-developer-platform-open-ready-and-built.html>
- AMD Ryzen AI Halo user guide and Best Known Configuration: <https://developer.amd.com/playbooks/user-guide/>
- AMD AI Playbooks: <https://developer.amd.com/playbooks/>
- AMD AI Developer Program: <https://www.amd.com/en/developer/ai-dev-program.html>
- `llama.cpp` releases: <https://github.com/ggml-org/llama.cpp/releases>
- Ollama releases: <https://github.com/ollama/ollama/releases>
