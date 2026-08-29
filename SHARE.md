# Community Sharing Guide

This page is for readers and contributors who want to share the Strix Halo
Guide because it answers a real question, documents their contribution, or
helps someone reproduce a result. It is not a posting campaign, outreach plan,
or request for coordinated promotion.

Canonical web guide:

```text
https://strixhaloguide.com/
```

Technical evidence repository:

```text
https://github.com/hogeheer499-commits/strix-halo-guide
```

Current Qwen3.8 evidence and route comparison:

```text
https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/QWEN38_STRIX_HALO.md
```

Share images:

- [`social-preview.png`](social-preview.png): general project preview.
- [`qwen38-route-preview.png`](qwen38-route-preview.png): Qwen3.8 route comparison.

The images can be regenerated with `python3 generate_preview.py`.

## Share Responsibly

- Share the guide only where it directly helps answer the conversation.
- Follow the rules and self-promotion policy of the destination community.
- Do not coordinate votes, request stars or upvotes, brigade discussions, or
  require sharing as a condition of contributing.
- State your relationship to the project. Contributors should say which result
  or document they contributed.
- Disclose any relevant vendor, sponsor, affiliate, loaner, gifted-hardware, or
  early-access relationship.
- Keep first-party, community, direct `llama-bench`, server/API,
  MTP/speculative, and custom runtime or quantization claims separate.
- Invite corrections, slower results, failed routes, and independent
  reproductions.
- Link benchmark claims to the most specific evidence page available.

The repository contains no affiliate links as of August 30, 2026. If that
changes, the relevant links and relationships must be disclosed under
[`VENDOR_DISCLOSURE.md`](VENDOR_DISCLOSURE.md).

## Neutral Project Summary

Use or adapt this when someone asks what the project is:

```text
Strix Halo Guide is an independent, evidence-backed resource for running local
AI on AMD Ryzen AI MAX / Strix Halo systems. It covers BIOS and Linux setup,
Ollama, llama.cpp, Vulkan/RADV, ROCm, model and quantization choices, measured
benchmarks, failed routes, and community reproductions across multiple systems.

Readable guide:
https://strixhaloguide.com/

Commands, raw data, caveats, and contribution paths:
https://github.com/hogeheer499-commits/strix-halo-guide
```

This wording is intentionally neutral. Do not change it to `I built` unless you
are the maintainer, and do not imply that you measured a result unless you did.

## Current Coverage Wording

Use this exact distinction in profiles, CVs, project descriptions, and short
public summaries:

```text
Public benchmark evidence covers 13 owner systems or independent sources.
The auditable split is 10 described owner systems plus 3 independently attributable external sources, with 10 credited community benchmark contributors.
Repeated evidence from one physical machine counts once.
```

Independent community reproductions exist on multiple Strix Halo systems, but
do not shorten that to `benchmarks reproduced on 13 systems`. The 13-entry map
also includes the first-party system, external evidence packages, capacity and
failure evidence, and unlike benchmark routes. It is an evidence-coverage
count, not a claim that one matched benchmark ran on all 13 entries.

## Short Share Text

```text
Independent AMD Strix Halo local-AI setup and benchmark guide: BIOS, Linux,
Ollama, llama.cpp, Vulkan/ROCm, model choices, raw evidence, failed paths, and
cross-system community reproductions.

https://strixhaloguide.com/
```

## Qwen3.8 Share Text

```text
Qwen3.8 27B results on Strix Halo currently combine different quants, runtimes,
backends, prompts, context states, and speculative-decoding routes. This guide
separates the measured official Ollama route from community MTP, ROCmFP4,
DFlash, and other advanced reports, with links to the underlying evidence:

https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/QWEN38_STRIX_HALO.md

Corrections and matched reproductions—including slower and failed runs—are
welcome.
```

For a post that quotes a performance number, copy the exact scope and caveat
from [`QWEN38_STRIX_HALO.md`](QWEN38_STRIX_HALO.md) instead of turning the
largest number into a general recommendation.

## Contributor Share Text

Contributors can adapt this to describe their own work:

```text
I contributed a community reproduction to the Strix Halo Guide using [system],
[backend/runtime], [model and quant], and [test conditions]. The report includes
the exact command, raw output, and where the result matched or differed from
other evidence in the guide:

[direct contribution or evidence link]

Slower, failed, and contradictory reproductions are useful too.
```

Only claim the parts you personally measured or reviewed. Link to the original
issue, raw bundle, or contributor credit so readers can inspect the provenance.

## Correction Or Failure Share Text

```text
I found a correction, regression, or failed route while following the Strix
Halo Guide. The exact hardware, software versions, command, output, and current
assessment are documented here:

[direct issue or evidence link]

The result is being shared to improve the public setup guidance, not as a
general claim about every Strix Halo system.
```

## Where To Link

- General setup or project question: <https://strixhaloguide.com/>
- Exact command, benchmark, or caveat: link the relevant GitHub evidence page.
- Qwen3.8 route question: [`QWEN38_STRIX_HALO.md`](QWEN38_STRIX_HALO.md).
- Community benchmark contribution: use the
  [benchmark issue template](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=benchmark-report.md).
- Early result or setup discussion: use
  [GitHub Discussions](https://github.com/hogeheer499-commits/strix-halo-guide/discussions).

Prefer the page that directly answers the question. A specific evidence link is
more useful than sending every technical discussion to the homepage.

## Attribution And Evidence Boundaries

When sharing a community contribution:

- name the contributor or project when that attribution is already public;
- identify the exact system, backend, runtime, model, quantization, and test;
- distinguish reproduced measurements from external leads or unverified claims;
- preserve important caveats and negative findings;
- avoid language that implies AMD, OEM, vendor, or contributor endorsement.

The contributor index is [`CONTRIBUTORS.md`](CONTRIBUTORS.md). Structured
community results are in [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), and
public headline claims map to their sources in
[`data/headline_claims.csv`](data/headline_claims.csv).

## Check Freshness Before Sharing Numbers

Evidence was reviewed on August 30, 2026. Ollama 0.33.2 and `llama.cpp`
v0.3.0 / b10687 were current checked targets on that date; they are not
automatic replacements for the runtime versions attached to older measured
rows.

Before copying a version or benchmark claim, check
[`data/public_state.json`](data/public_state.json) and the linked evidence page.
