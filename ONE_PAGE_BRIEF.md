# Strix Halo Local-AI Guide: Partner Brief

Independent, reproducible setup and benchmark evidence for AMD Strix Halo / Ryzen AI MAX+ 395 local-AI systems.

Public project overview: <https://strixhaloguide.com/>

Vendor and reviewer overview: <https://strixhaloguide.com/partners/>

Canonical technical evidence: <https://github.com/hogeheer499-commits/strix-halo-guide>

## Problem

High-end local-AI hardware can be technically strong but commercially under-leveraged if buyers cannot easily reproduce good results. Strix Halo buyers must navigate BIOS settings, OS choice, Vulkan/RADV, ROCm, Ollama, `llama.cpp`, vLLM, model formats, quantization, context settings, power behavior, and benchmark claims before they can trust the purchase.

AMD's public Ryzen AI Halo / Ryzen AI Developer Platform direction makes this category more visible, but visibility does not remove setup friction by itself. Buyers still need clear, reproducible, vendor-neutral evidence for what works on real systems.

## Proof Already Available

The [September 19 vendor proof summary](VENDOR_PROOF_SUMMARY.md) describes the
new existing-user qualification, scoped HIP controls, exact-SKU storefront
comparison and remaining GMKtec retail-evidence gap. These are technical
outcomes, not measured conversion or support-cost improvements.

The repo already includes a technical proof layer:

- Public GitHub demand signal: 345 stars and 24 forks in a small hardware/software niche as of 2026-09-25 (GitHub repository page); the previous 2026-08-27 GitHub API snapshot showed 300 stars, 21 forks, and 5 subscribers/watchers. Use this as supporting context, not the main claim.
- Upstream-reviewed engineering: 15 merged engineering PRs across 10 projects, including `llama.cpp`, the AMD-sponsored open-source Lemonade local-AI server, a Strix Halo detection fix in llmfit, OpenAI's official .NET SDK, and Kubernetes SIG inference-perf, plus 3 merged listing/docs PRs (counts reconciled 2026-09-13). The exact PRs, validation scope, and boundaries are listed in [`UPSTREAM_CONTRIBUTIONS.md`](UPSTREAM_CONTRIBUTIONS.md). The `llama.cpp` merge is preset/router maintenance, not a Strix Halo performance claim.
- Public evidence-coverage signal: 10 credited community benchmark contributors and 13 represented systems or independent sources (2026-09-19 evidence review). These are visible project and evidence-coverage signals, not attributable-sales claims.
- Setup and workflow guide: [`README.md`](README.md).
- Current benchmark snapshot: [`BENCHMARKS.md`](BENCHMARKS.md).
- Reproducibility notes: [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).
- Headline claim index: [`data/headline_claims.csv`](data/headline_claims.csv).
- Structured CSV data and raw artifacts: [`data/`](data/README.md), [`data/raw/`](data/raw/).
- Charts: [`charts/`](charts/README.md).
- Community validation: [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`COMMUNITY_NIMO.md`](COMMUNITY_NIMO.md), [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md), [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md).
- Backend/server caveats: [`SERVER_SHOOTOUT.md`](SERVER_SHOOTOUT.md), [`BACKEND_CROSSOVER.md`](BACKEND_CROSSOVER.md), [`VLLM_BASELINE.md`](VLLM_BASELINE.md), [`ROCM_VLLM_BUGWATCH.md`](ROCM_VLLM_BUGWATCH.md).
- Multi-user software-bottleneck evidence: [`MOE_CONCURRENCY.md`](MOE_CONCURRENCY.md) reproduces the Vulkan 8-to-9 MoE cliff on 30B and 80B expert shapes, confirms that it persists on official b10034, validates an opt-in AMD/RADV recovery path on b9979, and translates the result into model-specific Vulkan/ROCm buyer guidance.
- Sustained-workload support evidence: Fail-Safe's strict three-system Corsair/Sixunited campaign turns an intermittent lock report into scoped thermal/SCLK buyer guidance, preserves the corrected kernel-update fan-module confounder, and tracks an upstream fan-reset safety patch. See [`THERMAL_STABILITY.md`](THERMAL_STABILITY.md).
- Frontier-size agent evidence: a first-party Step 3.7 Flash 198B-total / about 11B-active ROCmFPX target plus MTP draft measured 34.50 t/s at 4K and 33.83 t/s at 16K, allocated 256K context, and returned a native tool call on one 128GB Beelink. This is scoped server/capacity evidence, not a direct speed headline.
- Frontier-size direct GGUF evidence: a pinned 90.86GB DeepSeek V4 Flash 284.33B `UD-IQ2_XXS` artifact loaded, generated, and passed a basic deterministic check through official `llama.cpp` b10034 Vulkan/RADV on one 128GB Beelink. The 13.27 tg128 row is capacity/current-model evidence with a low-bit quality caveat, not a speed claim.
- Ryzen AI server-optimization evidence: an isolated official ROCm 7.14 / PyTorch 2.11 / vLLM FP16 A/B reproduced AMD's documented batch-8+ hipBLASLt workaround on `gfx1151`, improving aggregate throughput by 40.50%, 38.96%, and 41.54% at concurrency 8, 9, and 16. This is scoped small-model server evidence, not a universal backend claim.
- Current HIP compatibility evidence: the September 19 v0.4.1 mitigation #28604 route passed bounded Coder retrieval and concurrent-output controls where historical b10687 failed. Both builds passed the Gemma image fixture. Official Qwen3.8, maximum memory and broad correctness remain unqualified; issue #26209 is not declared closed by this result. See [exact scope](RUNTIME_QUALIFICATION_2026-09-19.md).
- Local model-development evidence: a digest-pinned ROCm 7.2 Unsloth workflow on the retail Beelink passed Radeon GPU detection, one-step SFT, checkpoint inference, `Q4_K_M` GGUF export, ROCm `llama.cpp` inference, artifact persistence, and a post-restart reload. The public guide preserves the exact commands and two real path/export failures without presenting the tiny smoke as useful model quality or training speed. See [`UNSLOTH_STRIX_HALO.md`](UNSLOTH_STRIX_HALO.md).
- Buyer-friction measurement protocol: [`BUYER_PATH_VALIDATION.md`](BUYER_PATH_VALIDATION.md) defines a repeatable retail-box-to-working-local-AI campaign with timed checkpoints, intervention counts, restart persistence, failure classification, and evidence links. It is a protocol for future system campaigns, not an invented time-to-first-result claim.
- Platform context: [`RYZEN_AI_HALO_CONTEXT.md`](RYZEN_AI_HALO_CONTEXT.md).
- Current Qwen3.8 decision layer: [`QWEN38_STRIX_HALO.md`](QWEN38_STRIX_HALO.md) separates the measured official Ollama route, corrected 262K-class external evidence, stock/MTP controls, and current tuned-fork leads.

## Maintainer Capability

The project is not only downstream documentation. Its maintainer has taken
software problems through reproduction, scoped implementation, validation,
upstream review, and merge in projects used across the local-AI stack.

That reduces execution risk for a partner: technical feedback can be turned
into public setup guidance, reproducible reports, or narrowly scoped upstream
work instead of remaining an unverified support anecdote. Accepted upstream
work is still separate from vendor endorsement, and every guide benchmark
continues to require its own raw evidence.

## Commercial Value

This project turns scattered setup knowledge into public evidence and practical buyer confidence. It helps developers and buyers understand what AMD Strix Halo local-AI hardware can do, which setup path to try first, what remains experimental, and where more vendor support would remove friction.

For vendors and developer-relations teams, that means fewer adoption barriers, clearer buyer guidance, more credible reviews, and better signals about software or firmware gaps.

The current commercial thesis is not "vendor endorsement." It is: independent public evidence can make Ryzen AI Halo-class local-AI systems easier to evaluate, set up, support, review, and recommend.

The public evidence map currently covers:

- **13 Strix Halo-class systems or independent sources**: 10 described owner
  systems plus 3 independently attributable external sources, counted
  explicitly in the README's [`Evidence Coverage`](README.md#evidence-coverage-13-systems-or-independent-sources)
  table without recounting repeated evidence from one physical machine.
- **10 credited community benchmark contributors**, listed in [`CONTRIBUTORS.md`](CONTRIBUTORS.md), in addition to the primary first-party Beelink measurements.
- Beelink owner stacks, a three-system Corsair fleet, several independent GMKtec sources, MS-S1-Max, Nimo, and Minix evidence across Linux, Windows, Vulkan/RADV, ROCm, NPU, MTP, power, thermal, RPC, and large-model capacity routes.
- **Per-OEM evidence class (as of the 2026-09-19 evidence review; classes from the README [buying-guide table](README.md#buying-guide) and [`SYSTEM_EVIDENCE_MATRIX.md`](SYSTEM_EVIDENCE_MATRIX.md)):** Beelink GTR9 Pro: first-party (plus two community owner systems); GMKtec EVO-X2: community and external-reference, no first-party exact-SKU test; Corsair AI Workstation 300: community (three-system fleet); Nimo AI Mini PC: community; Minisforum MS-S1 MAX: community (Windows LM Studio); Minix Elite ER939: community (Ollama beginner path); Framework Desktop: external-reference rows only; Bosgame, HP and ASUS: none (price snapshots or a warning only); GMKtec EVO-X3: none (does not inherit EVO-X2 evidence).

The normal first-party buyer path includes an Ollama 0.31.2 system-service check at 60.57 t/s with the Strix Halo iGPU retained, vision working, and service-restart plus full-host-reboot persistence verified. Qwen3.8 27B is separately measured on Ollama 0.32.13 at 20.42 generation t/s (Ollama API with Ollama-default MTP drafting, `draft_num_predict 4`) with image, tools, thinking, and exact retrieval through 50,059 prompt tokens. Ollama 0.34.2 passed isolated available-model controls on September 19 but remains an unqualified normal-package/reboot target; community rows remain separated from first-party headline claims.

Community corrections and negative results improve the proof layer rather than being hidden: exact artifacts and commands, raw logs, separated claim types, explicit caveats, and corrected routes remain public. See [`COMMUNITY_FEEDBACK.md`](COMMUNITY_FEEDBACK.md).

## Collaboration Ask

I can produce independent, reproducible, public technical evidence that reduces adoption friction and helps buyers understand the value and limits of your hardware.

Useful collaboration can include technical contacts, review or loaner systems, early BIOS/firmware/software access, scoped benchmark campaign sponsorship, or engineering feedback. There are no affiliate links as of 2026-09-19; any future affiliate link follows [`VENDOR_DISCLOSURE.md`](VENDOR_DISCLOSURE.md).

## Example Deliverables

- Reproducible setup guide for a named system.
- Benchmark report with raw logs, CSVs, charts, and caveats.
- Buyer-focused known-good configuration notes.
- Cross-OEM reproduction report.
- Windows versus Linux comparison.
- Power and efficiency report.
- ROCm/vLLM/NPU blocker or progress report.
- Reproducible local fine-tuning, export, and deployment workflow for a named system and task.
- Disclosure-compliant public writeup.
- Timed retail-box-to-working-local-AI report with intervention and failure counts.

Current setup-support, reproduction, and OEM pilot scopes are listed in
[`SERVICES.md`](SERVICES.md).

## Disclosure And Independence

No paid-positive reviews. No hidden influence. No unsupported marketing claims. Sponsored, loaned, gifted, affiliate, or early-access work must be disclosed clearly. Vendors may correct factual errors, but benchmark conclusions remain independent. Affiliate commission is not a product-ranking input; attributable clicks or conversions, if measured later, remain separate from benchmark evidence and GitHub traffic.

## Contact

Maintainer: software engineer; Strix Halo guide maintainer.

For collaboration, service, or partner inquiries, email the maintainer privately at hogeheer499@gmail.com (see [`SERVICE_INTAKE.md`](SERVICE_INTAKE.md) for paid scopes). Do not put confidential material in a public GitHub issue. Public issues and discussions are for technical corrections and benchmark reports only.

TODO: typical turnaround, capacity, and invoicing entity (pending maintainer confirmation).
