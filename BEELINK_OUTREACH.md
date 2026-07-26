# Beelink Outreach Brief

Purpose: prepare the first vendor outreach around the Beelink GTR9 Pro without making the repo feel like an advertisement or a request for free hardware.

Use this as the Beelink-first context sheet before sending an email, contact-form message, LinkedIn message, or support/product inquiry.

## Why Beelink First

The guide's primary measured system is the Beelink GTR9 Pro with Ryzen AI MAX+ 395 / Radeon 8060S / 128GB unified memory. That makes Beelink the cleanest first vendor because the existing proof layer already shows what their retail hardware can do when the setup is reproducible.

This is not primarily about stars. The repo has 239 GitHub stars in a small hardware/software niche as of the 2026-07-25 GitHub API snapshot, but the stronger point is that the guide reduces buyer setup friction with public, reproducible evidence.

The maintainer also has accepted upstream work in `llama.cpp` and other AI
infrastructure. This improves the execution case for collaboration: a
reproducible software issue can become tested guidance or a narrowly scoped
upstream change, not just another downstream complaint. See
[`UPSTREAM_CONTRIBUTIONS.md`](UPSTREAM_CONTRIBUTIONS.md).

## Value To Beelink

The guide can help Beelink buyers and reviewers answer practical local-AI questions:

- which OS and backend path to start with
- which BIOS/UMA/IOMMU assumptions matter
- which models and quantizations fit
- which benchmark claims are reproducible
- which paths are still experimental or failed
- which setup mistakes waste buyer time

For Beelink, that can reduce support friction and make the GTR9 Pro easier to evaluate, recommend, review, and buy.

## Current Beelink Evidence To Point At

- Primary setup and guide: [`README.md`](README.md)
- Reproducibility notes: [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md)
- Benchmark snapshot: [`BENCHMARKS.md`](BENCHMARKS.md)
- Headline claim index: [`data/headline_claims.csv`](data/headline_claims.csv)
- Structured data and raw artifacts: [`data/README.md`](data/README.md), [`data/raw/`](data/raw/)
- Current model triage: [`CURRENT_MODELS.md`](CURRENT_MODELS.md)
- Buyer-use-case translation: [`BUYER_USE_CASES.md`](BUYER_USE_CASES.md)
- Partner brief: [`ONE_PAGE_BRIEF.md`](ONE_PAGE_BRIEF.md)
- Accepted upstream contributions: [`UPSTREAM_CONTRIBUTIONS.md`](UPSTREAM_CONTRIBUTIONS.md)
- Disclosure policy: [`VENDOR_DISCLOSURE.md`](VENDOR_DISCLOSURE.md)

Useful headline examples, kept scoped:

- Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`: 100.04 t/s direct `llama-bench`, with a later b9544 control at 103.18 t/s.
- Qwen3-Coder 30B-A3B `Q4_K_S`: 100.99 t/s speed-first direct `llama-bench` on the official b9851 Vulkan binary.
- LFM2.5 8B-A1B `Q4_K_M`: 170.02 t/s generation-only small-MoE scout.
- Nemotron 3 Super 120B-A12B `UD-IQ4_XS`: 18.43 t/s direct 120B-class GGUF capacity/current-model route.
- DeepSeek V4 Flash 284B `UD-IQ2_XXS`: pinned 90.86GB ordinary GGUF loaded and generated directly at 13.27 t/s on official b10034; low-bit capacity evidence, not a speed or broad quality claim.
- gpt-oss-120b MXFP4: 55.57 t/s direct local load/speed check.
- Normal Ollama 0.31.2 system-service path: 60.57 t/s Qwen3.6 generation with iGPU, vision, restart, and full-host-reboot checks passed.
- Multi-user software finding: official b9979 Vulkan loses 30.9-35.5% aggregate decode from concurrency 8 to 9 on two tested MoE shapes; an opt-in AMD/RADV density policy recovers 25.3-42.7% at concurrency 9.

Do not present these as universal Beelink marketing claims. Present them as dated, reproducible evidence under documented setup conditions.

## Specific Asks

Start with technical feedback before asking for hardware.

Best first asks:

- Can Beelink confirm recommended BIOS settings for local-AI workloads, especially UMA and IOMMU?
- Can Beelink confirm current firmware/BIOS guidance for GTR9 Pro buyers?
- Can Beelink clarify board-revision / NIC guidance for buyers where relevant?
- Are there Beelink setup notes for Linux, Vulkan/RADV, Ollama, or `llama.cpp` that should be added or corrected?
- Is there a technical contact who can review setup assumptions for factual accuracy?

Possible collaboration asks after the technical ask:

- review/loaner access for follow-up validation
- early BIOS/firmware notes where public disclosure is allowed
- scoped benchmark campaign sponsorship
- a second Beelink unit for repeatability, wall-power, or regression testing

## Suggested First Email

Subject: Independent Beelink GTR9 Pro local-AI evidence and setup-friction feedback

```text
Hello [name/team],

I maintain an independent AMD Strix Halo local-AI setup and benchmark guide:

https://github.com/hogeheer499-commits/strix-halo-guide

The guide currently uses a Beelink GTR9 Pro as the primary measured system. It is evidence-backed rather than promotional: setup steps, BIOS/driver/backend notes, raw benchmark logs, CSVs, charts, reproducibility notes, caveats, community validation, and failed paths are all public.

The repo reached 239 GitHub stars in a small hardware/software niche as of the 2026-07-25 GitHub API snapshot, but the more important point is practical: the guide reduces adoption friction for buyers and reviewers who want to know what actually runs locally, which setup path works, and which claims are reproducible.

Because the GTR9 Pro is the primary measured system, Beelink feedback would be especially useful on:

- recommended BIOS / UMA / IOMMU settings for local AI
- current firmware and board-revision guidance
- Linux/Vulkan/RADV/Ollama/llama.cpp setup notes
- factual corrections to the current Beelink setup notes
- possible review/loaner access or a scoped benchmark campaign for future validation

All vendor involvement would be disclosed. Vendors may correct factual errors, but benchmark conclusions remain independent and negative findings stay if they are accurate.

Would you be open to discussing this, or routing me to the right product/technical contact?

Best,
[name]
GitHub: https://github.com/hogeheer499-commits
Email: hogeheer499@gmail.com
```

## Short Contact-Form Version

```text
I maintain an independent Beelink GTR9 Pro / AMD Strix Halo local-AI setup and benchmark guide:

https://github.com/hogeheer499-commits/strix-halo-guide

It reduces buyer setup friction with reproducible public evidence: setup steps, backend guidance, raw logs, CSVs, charts, caveats, community validation, and failed paths. The repo had 239 GitHub stars in this small niche as of the 2026-07-25 GitHub API snapshot, but the main value is helping buyers and reviewers reproduce a working local-AI setup.

Could you route me to the right Beelink product/technical contact for BIOS/firmware/setup feedback, and possibly review/loaner or scoped benchmark collaboration? Results would remain independent and disclosed.
```

## Follow-Up With A New Technical Reason

Reply in the original email thread. This is stronger than a generic
"just following up" message because the accepted contribution is new,
independently verifiable engineering evidence.

If a new subject is required:

```text
llama.cpp contributor: reducing GTR9 Pro local-AI buyer friction
```

```text
Hi Beelink team,

A short update since my earlier GTR9 Pro collaboration email: a fix I submitted to llama.cpp has now been reviewed and merged upstream.

https://github.com/ggml-org/llama.cpp/pull/25643

The change itself is preset/router maintenance, not a GTR9 Pro performance claim. What it adds to the collaboration case is practical engineering follow-through: I can reproduce software friction, document it for buyers, and where the scope is clear, take a fix through validation and upstream review.

The GTR9 Pro remains the primary system behind the guide. I would still like to connect with the right Beelink product or engineering contact about a better-validated "retail box to working local AI" buyer path, including BIOS/firmware guidance and possible access to a second Beelink configuration.

Project:
https://strixhaloguide.com/partners/

Canonical technical evidence:
https://github.com/hogeheer499-commits/strix-halo-guide

Verified upstream work:
https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/UPSTREAM_CONTRIBUTIONS.md

Best,
Jesse van Dijk
hogeheer499-commits
Strix Halo guide maintainer
```

## Do Not Say

- Do not lead with the current star count followed by a request for hardware.
- Do not imply Beelink endorses the guide.
- Do not ask for free hardware as the first sentence.
- Do not hide known caveats, failed paths, or board/firmware concerns.
- Do not promise positive coverage.
- Do not call the accepted `llama.cpp` preset/router change a Strix Halo
  performance fix or official `llama.cpp` endorsement of the guide.

## Good Framing

```text
The stars show there is demand. The guide itself is the asset: reproducible public evidence that helps buyers trust and use Beelink/Strix Halo local-AI hardware.
```
