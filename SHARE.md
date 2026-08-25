# Share Pack

Use these copy-ready angles when the guide directly answers the discussion.
Lead with useful evidence, follow each community's rules, and adapt the text to
the audience instead of posting the same message everywhere.

Canonical repository:

```text
https://github.com/hogeheer499-commits/strix-halo-guide
```

Current Qwen3.8 decision page:

```text
https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/QWEN38_STRIX_HALO.md
```

Share images:

- [`qwen38-route-preview.png`](qwen38-route-preview.png): current Qwen3.8 comparison hook.
- [`social-preview.png`](social-preview.png): general project preview.

Regenerate them reproducibly with `python3 generate_preview.py`.

## Share Responsibly

- Do not ask for coordinated upvotes or stars, brigade a thread, or require
  sharing as a condition of contributing.
- Disclose your connection to this project and any vendor, sponsor, affiliate,
  loaner, gifted-hardware, or early-access relationship relevant to the post.
- Keep first-party, community, direct, API/server, MTP/speculative, and custom
  fork/quant claims separate.
- Invite corrections, slower results, failed paths, and independent
  reproductions.
- Link only when the page or evidence materially answers the conversation.

The repository contains no affiliate links as of August 25, 2026. Future
affiliate links must be labeled near the link and recorded under the public
[`VENDOR_DISCLOSURE.md`](VENDOR_DISCLOSURE.md) policy.

## Best Current Story: Qwen3.8 Route Reality Check

### Title Options

- Qwen3.8 on Strix Halo: why 20, 31, 52 and 65 t/s are not the same claim
- Qwen3.8 27B on Ryzen AI MAX+ 395: official easy path vs MTP/DFlash speed routes
- Qwen3.8 Strix Halo guide: 50K local retrieval, external 262K evidence, and the current speed frontier

### Reddit / Forum Copy

```text
Qwen3.8 27B now has several Strix Halo results ranging from roughly 20 to 65
tokens/sec, but they are not interchangeable.

I mapped the current routes by model/quant, backend, runtime fork, speculation,
prompt type, context behavior, and evidence status:

- measured official Ollama route: 292.49 prompt t/s and 20.42 generation t/s
  over nine warm repeats; image, tools, thinking, and exact retrieval through
  50,059 prompt tokens passed
- separate corrected GMKtec package: 13/13 retrieval through a 261,130-token
  case, but on an advanced patched-HIP route
- stock Q8 MTP, ROCmFP4/DFlash, and adaptive-speculation routes: promising
  community results that need their exact artifacts and matched controls

The point is not to dismiss the fast numbers. It is to show what each result
actually proves and make the next independent reproduction useful.

Guide and route matrix:
https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/QWEN38_STRIX_HALO.md

Corrections, exact commands, raw logs, and slower/failed reproductions are very
welcome.
```

## Short Social Copy

```text
Qwen3.8 27B on AMD Strix Halo: measured official Ollama path, 50K exact local
retrieval, separate external 262K-class evidence, and a route-by-route check of
current 22-65 t/s MTP/DFlash/fork claims.

The model, quant, backend, fork, speculation, prompt and context are part of the
number:
https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/QWEN38_STRIX_HALO.md
```

## General Project Story

### Title Options

- Show HN: Evidence-backed AMD Strix Halo local-AI setup and benchmark guide
- What actually runs on a 128GB Ryzen AI MAX+ 395—from easy chat to a 284B GGUF
- AMD Strix Halo local LLM guide with raw CSVs, logs, failures, and cross-OEM reproductions

### Hacker News / Technical Forum Copy

```text
I built an independent AMD Strix Halo / Ryzen AI MAX+ 395 local-AI guide because
the useful setup information and benchmark caveats were spread across releases,
issues, model cards, and forum posts.

It includes a copyable Ubuntu/Vulkan-RADV/Ollama path, direct llama.cpp and
server benchmarks, model/backend recommendations, long-context and concurrency
evidence, failed routes, and structured raw evidence. The current map covers 13
systems or independent sources from 10 credited community benchmark
contributors; community rows remain separate from first-party measurements.

Repo:
https://github.com/hogeheer499-commits/strix-halo-guide

I am especially interested in corrections and matched reproductions from other
OEM systems.
```

## Buyer-Oriented Copy

```text
Considering a 96GB or 128GB AMD Strix Halo machine for local AI?

This guide separates three questions that product pages often mix together:

1. what fits in memory;
2. what is fast for your workload;
3. what setup has actually survived restart, context, vision, tools, and
   reproducibility checks.

It covers the easiest Ollama route, direct llama.cpp performance, current
Qwen3.8 guidance, larger 120B/284B capacity evidence, cross-OEM community rows,
power/thermal caveats, and raw logs:
https://github.com/hogeheer499-commits/strix-halo-guide
```

If a future version includes affiliate links, add this sentence next to the
relevant buyer links—not only at the bottom of the post:

```text
Disclosure: marked hardware links are affiliate links. They do not determine
benchmark inclusion, ranking, conclusions, or whether negative results remain
published.
```

## Vendor / Reviewer Copy

```text
Independent AMD Strix Halo / Ryzen AI MAX local-AI evidence project:
https://strixhaloguide.com/

The project turns buyer uncertainty—BIOS memory settings, OS/backend choice,
runtime compatibility, model/quant fit, context, serving, power and
reproducibility—into public setup guidance and linked raw evidence.

Vendor/reviewer overview:
https://strixhaloguide.com/partners/

GitHub evidence:
https://github.com/hogeheer499-commits/strix-halo-guide

Loaned, gifted, sponsored, affiliate, vendor-feedback, and early-access work is
disclosed. Vendors may correct factual errors but do not receive editorial
control or guaranteed positive conclusions.
```

## Contributor Copy

```text
I reproduced one AMD Strix Halo local-AI route on my own system. Here are the
hardware, model, quant, backend, exact command, raw output, and where it matched
or differed from the guide.

[result/evidence link]

Slower and failed reproductions are useful too.
```

Use the [benchmark issue template](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=benchmark-report.md)
for results that should enter the structured evidence map.

## Current Version Note

Evidence was reviewed on August 25, 2026. Ollama 0.32.15 and `llama.cpp`
v0.3.0 / b10622 are current checked targets, not automatic replacements for
the guide's measured runtime rows. Use [`data/public_state.json`](data/public_state.json)
before copying a version claim into a new post.
