# Partnership Overview

`strix-halo-guide` is an independent, evidence-backed AMD Strix Halo / Ryzen AI MAX+ 395 local-AI setup and benchmark guide. It turns scattered setup details into reproducible instructions, benchmark reports, raw logs, CSVs, charts, and caveats so developers and buyers can evaluate real local-LLM workflows before committing time or money to a system.

Public partner overview: <https://strixhaloguide.com/partners/>

Canonical technical evidence: <https://github.com/hogeheer499-commits/strix-halo-guide>

## The Buyer And Developer Problem

Strix Halo local-AI hardware is powerful, but the setup path is fragmented, confusing, and hard to trust. Buyers often have to piece together BIOS settings, Linux versus Windows tradeoffs, Vulkan/RADV, ROCm, Ollama, `llama.cpp`, model formats, quantization choices, context settings, server behavior, and benchmark claims from disconnected posts and issues.

That uncertainty creates adoption friction. A technically strong AI PC can still be commercially under-leveraged if buyers cannot easily reproduce good results or understand which results apply to their workflow.

## Value Proposition

This guide reduces setup friction, provides reproducible benchmark evidence, and helps buyers evaluate AMD local-AI hardware with clearer expectations. It gives developers and buyers a practical path from "what should I install?" to "which backend, model, and settings should I try first?"

The repo also has a visible demand signal: 239 GitHub stars, 14 forks, 5 watchers, 8 credited community benchmark contributors, and 11 Strix Halo-class systems/sources represented as of the 2026-07-25 GitHub/project snapshot. GitHub's available traffic window captured 835 unique repository visitors and 180 unique cloners; Google was the largest recorded referrer with 324 unique visitors. These dated figures are preserved in [`data/raw/2026-07-25/github-traction-snapshot/`](data/raw/2026-07-25/github-traction-snapshot/) and should not be treated as the main value proposition. The main value is the proof layer below: reproducible public evidence that makes the hardware easier to evaluate, trust, support, review, and buy.

The technical proof layer already includes:

- Setup and workflow guidance in [`README.md`](README.md).
- Accepted upstream engineering in [`UPSTREAM_CONTRIBUTIONS.md`](UPSTREAM_CONTRIBUTIONS.md): 15+ merged contributions with direct merge and review links, including `llama.cpp`, AMD's Lemonade local-AI server, a Strix Halo detection fix in llmfit, OpenAI's official .NET SDK, and Kubernetes SIG inference-perf. This demonstrates the ability to move from reproduction through validation and upstream review without misrepresenting those merges as vendor endorsement or Strix Halo performance fixes.
- Current buyer-path setup checks, including the normal Ollama 0.31.2 system-service route with `OLLAMA_IGPU_ENABLE=1`, 60.57 t/s Qwen3.6 generation, working vision, and restart/reboot persistence. A controlled same-port/same-cache comparison puts isolated 0.31.1, 0.31.2, and 0.32.0 local binaries in the same 72.55-73.20 t/s class. A later isolated 0.32.3 qualification preserved exact output at 73.13 t/s versus 73.20 t/s on the controlled 0.31.2 binary and passed iGPU vision plus process restart. The installed 0.31.2 service remains the buyer default until current 0.32.5 completes the normal package-upgrade/full-reboot path.
- A repeatable [`BUYER_PATH_VALIDATION.md`](BUYER_PATH_VALIDATION.md) protocol for measuring retail-box-to-working-local-AI friction through timed checkpoints, intervention counts, restart persistence, and public evidence links without inventing a current time-to-result claim.
- Reproducibility notes in [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).
- Current benchmark snapshot in [`BENCHMARKS.md`](BENCHMARKS.md).
- A current multi-user engineering case in [`MOE_CONCURRENCY.md`](MOE_CONCURRENCY.md): official b10034 still loses 31.7-37.3% aggregate decode from concurrency 8 to 9 on two tested MoE shapes; a separate controlled b9979 campaign shows an opt-in AMD/RADV density policy recovering 25.3-42.7% at np9 without changing np8 materially.
- Direct current-model capacity evidence: a pinned 90.86GB DeepSeek V4 Flash 284.33B ordinary GGUF loaded and generated on one 128GB Beelink through official b10034 Vulkan/RADV. This is explicitly scoped as low-bit capacity/basic-correctness evidence rather than a speed or broad quality claim.
- End-to-end local model-development evidence in [`UNSLOTH_STRIX_HALO.md`](UNSLOTH_STRIX_HALO.md): a digest-pinned ROCm 7.2 route passed Radeon GPU detection, one-step SFT, checkpoint inference, `Q4_K_M` GGUF export, ROCm `llama.cpp` inference, artifact persistence, and post-restart loading. The tiny smoke remains explicitly separated from useful fine-tuning quality or performance claims.
- Claim-to-evidence mapping in [`data/headline_claims.csv`](data/headline_claims.csv).
- Structured data in [`data/`](data/README.md).
- Raw logs and CSVs in [`data/raw/`](data/raw/).
- Generated charts in [`charts/`](charts/README.md).
- Community validation in [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md), and [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md).

## Commercial Leverage

High-end local-AI hardware can be technically strong but commercially under-leveraged if buyers cannot easily reproduce good results. This project turns scattered setup knowledge into public evidence and practical buyer confidence.

That creates a win-win:

- Buyers get a trustworthy path to local AI.
- AMD, OEMs, reviewers, and system vendors get fewer adoption barriers and more credible public proof of what the hardware can do.
- The project gets access to more systems, firmware, drivers, and technical context to produce better public evidence.
- The guide remains independent, transparent, and honest.

## Who This Is Useful For

- AMD Developer Relations, Ryzen AI, ROCm, and related software teams.
- Beelink, Framework, GMKtec, Corsair, Minisforum, and other Strix Halo system vendors.
- Reviewers, newsletters, YouTube creators, and technical publications.
- System integrators building local-AI workstations or appliances.
- Local-AI developers choosing between Ollama, `llama.cpp`, ROCm, vLLM, and server workflows.
- AI-PC buyers deciding whether Strix Halo fits their real workflow.

## What Partners Can Provide

Possible support includes:

- Technical contact for setup, firmware, driver, or reproducibility questions.
- Review unit.
- Loaner hardware.
- Early BIOS or firmware access.
- Early driver, ROCm, Ryzen AI, or local-AI software access.
- Sponsorship for a clearly scoped benchmark campaign.
- Affiliate relationship, if disclosed clearly.
- Longer-term hardware support for ongoing regression and cross-version testing.
- Engineering feedback on reproducibility, setup blockers, or driver behavior.

These are options, not demands. The useful collaboration is access to hardware, software, and context that lets the guide produce better public evidence.

## What I Can Deliver

- Reproducible setup guide for a specific system, OS, backend, and model path.
- Benchmark report with command lines, versions, settings, caveats, and interpretation.
- Raw logs, CSVs, generated charts, and claim-to-evidence links.
- Troubleshooting notes for failed paths, regressions, firmware issues, and driver blockers.
- Reproducible software-bottleneck reports that connect an upstream backend issue to buyer-facing guidance, second-system validation requests, and firmware/fan/engineering questions.
- Reproducible local fine-tuning, export, and deployment workflows for a named system and task.
- Buyer use-case documentation that translates technical results into practical decisions.
- Timed retail-box-to-working-local-AI validation with setup interventions, failures, and restart persistence documented.
- Disclosure-compliant public writeup for sponsored, loaned, gifted, or early-access work.
- Vendor-neutral technical findings, including negative results when they are accurate.

Current fixed and scoped professional-service options are listed in
[`SERVICES.md`](SERVICES.md). A paid scope does not weaken the disclosure or
independence rules below.

## Independence

This guide does not sell paid-positive reviews. Sponsorship, loaned hardware, gifted hardware, affiliate links, or early-access software must be disclosed clearly. Vendors may correct factual errors, but they do not receive editorial control over benchmark conclusions.

No fake claims, hidden influence, unsupported marketing language, or undisclosed vendor involvement.

## Contact

For collaboration inquiries, open a GitHub issue or contact the maintainer through the GitHub profile.

Email: hogeheer499@gmail.com.
