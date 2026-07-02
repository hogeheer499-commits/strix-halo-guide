# Partnership Overview

`strix-halo-guide` is an independent, evidence-backed AMD Strix Halo / Ryzen AI MAX+ 395 local-AI setup and benchmark guide. It turns scattered setup details into reproducible instructions, benchmark reports, raw logs, CSVs, charts, and caveats so developers and buyers can evaluate real local-LLM workflows before committing time or money to a system.

## The Buyer And Developer Problem

Strix Halo local-AI hardware is powerful, but the setup path is fragmented, confusing, and hard to trust. Buyers often have to piece together BIOS settings, Linux versus Windows tradeoffs, Vulkan/RADV, ROCm, Ollama, `llama.cpp`, model formats, quantization choices, context settings, server behavior, and benchmark claims from disconnected posts and issues.

That uncertainty creates adoption friction. A technically strong AI PC can still be commercially under-leveraged if buyers cannot easily reproduce good results or understand which results apply to their workflow.

## Value Proposition

This guide reduces setup friction, provides reproducible benchmark evidence, and helps buyers evaluate AMD local-AI hardware with clearer expectations. It gives developers and buyers a practical path from "what should I install?" to "which backend, model, and settings should I try first?"

The repo also has a visible demand signal: 192 GitHub stars and 11 Strix Halo-class systems/sources represented as of the 2026-07-02 GitHub/project snapshot. That should not be treated as the main value proposition. The main value is the proof layer below: reproducible public evidence that makes the hardware easier to evaluate, trust, support, review, and buy.

The technical proof layer already includes:

- Setup and workflow guidance in [`README.md`](README.md).
- Current buyer-path setup checks, including the Ollama 0.31.1 `OLLAMA_IGPU_ENABLE=1` Vulkan/RADV sanity row that turns a silent iGPU-drop risk into a documented setup instruction.
- Reproducibility notes in [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).
- Current benchmark snapshot in [`BENCHMARKS.md`](BENCHMARKS.md).
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
- Buyer use-case documentation that translates technical results into practical decisions.
- Disclosure-compliant public writeup for sponsored, loaned, gifted, or early-access work.
- Vendor-neutral technical findings, including negative results when they are accurate.

## Independence

This guide does not sell paid-positive reviews. Sponsorship, loaned hardware, gifted hardware, affiliate links, or early-access software must be disclosed clearly. Vendors may correct factual errors, but they do not receive editorial control over benchmark conclusions.

No fake claims, hidden influence, unsupported marketing language, or undisclosed vendor involvement.

## Contact

For collaboration inquiries, open a GitHub issue or contact the maintainer through the GitHub profile.

Email: hogeheer499@gmail.com.
