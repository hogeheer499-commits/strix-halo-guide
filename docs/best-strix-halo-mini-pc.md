---
layout: default
title: "Best Strix Halo Mini PC for Local LLMs (2026): Beelink vs Framework vs GMKtec vs Corsair"
description: "Evidence-based comparison of AMD Ryzen AI MAX+ 395 mini PCs for local LLMs: measured cross-OEM benchmarks, 64GB vs 128GB fit guidance, dated prices, and buy-now-or-wait timing."
permalink: /best-strix-halo-mini-pc/
date: "2026-08-21T00:00:00+02:00"
last_modified_at: "2026-09-05T00:00:00+02:00"
image:
  path: "https://hogeheer499-commits.github.io/strix-halo-guide/assets/social-preview.png"
  height: 640
  width: 1280
  alt: "AMD Strix Halo mini PC comparison for local LLMs with measured cross-OEM evidence"
seo:
  type: "TechArticle"
  date_modified: "2026-09-05T00:00:00+02:00"
---

# Best Strix Halo Mini PC for Local LLMs (2026)

**Evidence reviewed:** August 30, 2026.

Start with the independent [Strix Halo Guide](https://strixhaloguide.com/) for
the current setup and evidence model; use this page for the buyer comparison.

**Short answer:** choose a Strix Halo mini PC by the exact model artifact and context you need, the delivered price for that memory configuration, cooling, firmware and support. The guide has useful first-party and community results, but the cross-OEM rows below are not a controlled ranking. A 128GB system is valuable for the larger measured artifacts; a smaller configuration may be sufficient for a smaller workload.

This page interprets the evidence in the [canonical Strix Halo guide repository](https://github.com/hogeheer499-commits/strix-halo-guide). Every number links to a dated source; first-party and community measurements stay labeled.

## Beelink GTR9 Pro vs GMKtec EVO-X2 and Corsair: measured results

Measured `llama.cpp` results on Qwen3-Coder 30B-A3B (UD-Q4_K_XL, tg128) across owner systems, from the guide's [community results index](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/COMMUNITY_RESULTS.md) and first-party rows:

| System | Result (t/s) | Source type |
|---|---|---|
| Beelink GTR9 Pro | 96.76 | first-party, [claim index](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv) |
| Corsair AI Workstation 300 (3 units) | 93.55–95.50 | community, [issue #10](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10) |
| GMKtec EVO-X2 | 91.40–92.11 | community, [issue #17](https://github.com/hogeheer499-commits/strix-halo-guide/issues/17) (different build/flags — see caveat) |

These rows cover five physical systems across three OEMs. Their generation results are close, but the GMKtec runs used different builds and flags, and the campaigns were not a matched same-stack comparison. They demonstrate that the route works on more than one OEM; they do not isolate the performance effect of the chassis or firmware. Use the [raw community data](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/community_results.csv) and each run's conditions before comparing. The guide's deepest first-party evidence is on Beelink; GMKtec and Corsair results remain attributed community evidence.

## 64GB vs 128GB: the decision that actually matters

The first-party machine has 128GB. Smaller-memory fit guidance below is an estimate from artifact sizes, not a matched 64GB-versus-128GB benchmark:

- **64GB** is a capacity candidate for the smaller Q4 MoE artifacts, such as Qwen3-Coder 30B and LFM2.5 8B-A1B. Confirm runtime overhead, context, concurrent requests and OS memory on the actual machine. It cannot hold the ~91GB DeepSeek capacity artifact entirely in memory.
- **128GB** unlocks the routes that make this platform special: Nemotron 3 Super 120B-A12B direct GGUF (~18–19 t/s measured), Step 3.7 Flash 198B server route, and the pinned 90.86GB DeepSeek V4 Flash 284B artifact ([capacity evidence](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/raw/2026-07-16/deepseek-v4-flash-ud-iq2-xxs/), a scoped direct speed and basic correctness result, not a broad quality qualification).
- The measured Llama 3.1 70B Q4_K_M route generates ~4.7–4.9 t/s. Decide whether that latency is acceptable for your task. It does not establish the speed of every dense 70B model or a universal minimum for useful chat.

Budget for model weights, KV cache, runtime buffers, concurrent sequences and the OS. A fixed 10–20GB allowance does not qualify every architecture or context length. Use the [model hub](models.md) to separate measured artifacts from published-size estimates. The [best-known profiles table](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BEST_KNOWN_PROFILES.md) maps workloads to measured routes.

## Price snapshot and trend

Prices below are dated observations, not current offers or a forecast. The first-party Beelink system has the following recorded history:

**Beelink GTR9 Pro (128GB/2TB) — documented price history**

| Date | Price | Source |
|---|---|---|
| Aug 2025 (launch preorder) | $1,985 | [TechRadar launch coverage](https://www.techradar.com/pro/a-mac-studio-windows-workstation-clone-just-went-on-preorder-with-amds-ai-395-beelink-gtr9-pro-costs-usd1985-has-two-10-gbe-ports-and-128gb-ram) |
| 2026-02-20 | $2,494 | maintainer's own purchase invoice for the benchmark unit used throughout this guide |
| Mar 2026 | $2,999 (preorder) | [Liliputing](https://liliputing.com/more-ryzen-ai-max-395-mini-pcs-with-128gb-are-now-available-if-you-can-afford-one/) |
| 2026-08-21 | $4,349 (list $4,699), pre-sale | [vendor page](https://www.bee-link.com/products/beelink-gtr9-pro-amd-ryzen-ai-max-395) |
| 2026-08-29 | $4,349 (list $4,699), pre-sale, ships within 35 days — unchanged | [vendor page](https://www.bee-link.com/products/beelink-gtr9-pro-amd-ryzen-ai-max-395), re-verified |

The recorded Beelink prices increased over this period. That history does not establish every vendor's cost structure or predict the next price. Compare the exact RAM/SSD variant, region, tax, delivery date and warranty before purchasing; a storefront's lowest advertised price can belong to a smaller configuration.

The guide's dated canonical snapshot (2026-07-27) is in [`data/buyer_price_snapshot_2026-07-27.csv`](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/buyer_price_snapshot_2026-07-27.csv). Each spot-check cell below carries its own check date (latest vendor-page checks: 2026-08-29):

| System (128GB) | 2026-07-27 snapshot | Latest spot-check | Note |
|---|---|---|---|
| Bosgame M5 | $2,899 | ~$2,399–2,499 (2026-08-21, [vendor](https://www.bosgamepc.com/products/bosgame-m5-ai-mini-desktop-ryzen-ai-max-395)) | cheapest 128GB route at last check |
| GMKtec EVO-X2 | €3,229–3,359 (EU) | US $2,199.99 (list $2,599.99) but all variants sold out with a "price increase coming soon" banner; EU store from €1,959.99 in stock, verify the 128GB config price (2026-08-29, [US vendor](https://www.gmktec.com/products/amd-ryzen%e2%84%a2-ai-max-395-evo-x2-ai-mini-pc), [EU vendor](https://de.gmktec.com/en/products/gmktec-evo-x2-amd-ryzen%E2%84%A2-ai-max-395-mini-pc-1)) | best value if you catch stock |
| Corsair AI Workstation 300 | $3,399 (out of stock) | $2,699–3,399 (2026-08-21, [Tom's Hardware](https://www.tomshardware.com/desktops/mini-pcs/corsairs-strix-halo-ai-workstation-300-gets-even-more-expensive-amid-the-rampocalypse-ryzen-ai-max-395-flagship-now-sits-at-usd3-399)) | community-validated 3-unit fleet in this guide |
| Framework Desktop | $3,149 (mainboard) | ~$3,449 (2026-07-22, [Notebookcheck](https://www.notebookcheck.net/Framework-launches-world-s-first-mini-ITX-desktop-PC-with-Ryzen-AI-Max-Pro-495-and-192-GB-RAM.1349336.0.html)); a 192GB PRO 495 tab is live as "coming soon" (2026-08-29, [vendor](https://frame.work/desktop)) | best ecosystem/support |
| Minisforum MS-S1 MAX | $3,639 | $3,799 (list $4,749) 128GB/2TB preorder, estimated mid-September shipping; EU €3,999 (2026-08-29, [US vendor](https://store.minisforum.com/products/minisforum-ms-s1-max-mini-pc), [EU vendor](https://minisforumpc.eu/products/minisforum-ms-s1-max-mini-pc)) | 10GbE, clustering-friendly |
| AMD Ryzen AI Halo (Micro Center exclusive) | not yet listed | $3,999.99, Windows 11 or Linux, in-store pickup only, in US stores since 2026-07-10 (checked 2026-08-29, [AMD](https://www.amd.com/en/blogs/2026/amd-ryzen-ai-halo-now-available-at-micro-center.html), [Micro Center](https://www.microcenter.com/site/content/amd-ryzen-ai-halo.aspx)) | AMD's own 128GB reference box with 10GbE |
| Beelink GTR9 Pro | $4,349 (pre-sale) | $4,349, list $4,699 (re-verified 2026-08-29, [vendor](https://www.bee-link.com/products/beelink-gtr9-pro-amd-ryzen-ai-max-395)) | deepest first-party evidence in this guide; see price history above |

**Before buying:** open the current vendor listing and select the exact configuration. These August snapshots can be stale. Stock labels and a seller's price-increase banner are not independent evidence that waiting will cost more.

## Buy now or wait?

Buy when a currently available configuration supports a task you need now at an acceptable delivered price. Waiting can be sensible when your current machine is adequate, the price exceeds your budget, or your workload needs more capacity than the tested system offers. Future prices and performance are uncertain.

Published larger-memory options belong in a capacity comparison; they do not inherit the guide's 128GB speed or feature results. Check the exact processor, memory and shipping configuration on the [official Framework Desktop page](https://frame.work/desktop) and other vendor listings. Do not infer the specification of a new GMKtec model from its EVO-X generation number alone.

If your chosen artifact fits in a discrete GPU's VRAM, also compare an existing or used GPU system and Apple silicon against your actual workload. Include the complete host cost, software requirements, power and noise; this guide does not establish a universal price/performance winner across those platforms.

## Recommendation tiers

The maintained tier list with evidence depth per system lives in the repository [Buying Guide](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#buying-guide). Summary: **most evidence-backed** — Beelink GTR9 Pro; **best value candidate** — Bosgame M5 / GMKtec EVO-X2 (stock permitting); **best ecosystem and support** — Framework Desktop; **community-validated fleet** — Corsair AI Workstation 300; **clustering** — Minisforum MS-S1 MAX.

These tiers use memory configuration, dated price/availability, evidence depth,
cooling/thermals, firmware/support, ports, expandability, and workload fit.
Affiliate commission is not a ranking input. If affiliate links are introduced,
each will be labeled near the link and entered in the public
[`affiliate link registry`](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/affiliate_link_registry.csv).

## FAQ

**Is a Strix Halo mini PC worth it for local LLMs?**
It can be useful when a measured model needs more memory than your existing GPU provides and its latency is acceptable. Start with a qualified model/runtime route and compare the delivered system cost with alternatives.

**Which Strix Halo mini PC is fastest for LLMs?**
The cross-OEM rows above use different campaigns and include build/flag differences. They support portability, but do not establish a controlled OEM speed ranking.

**Do I need 128GB of RAM?**
Choose from the exact artifact, context and concurrency requirement. Smaller Q4 MoE artifacts may fit in 64GB with sufficient headroom. The guide's larger capacity results were measured on 128GB; nominal parameter count alone is not a memory requirement.

**Should I wait for the next generation?**
Wait if a currently available configuration cannot meet your task or budget. Check confirmed product specifications and shipping dates; more advertised memory does not by itself prove faster inference, and future prices are uncertain.

**Are these prices current?**
Every snapshot has its own date. Verify the exact region, RAM/SSD configuration, tax, shipping and stock on the vendor's current page. The historical price table is not a live quotation.


---

Community corrections are welcome — open an issue in the [repository](https://github.com/hogeheer499-commits/strix-halo-guide/issues). Pricing rows are dated snapshots, not live quotes. This page contains no affiliate links as of August 30, 2026; if that changes, links will be disclosed next to the relevant product and per [`VENDOR_DISCLOSURE.md`](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/VENDOR_DISCLOSURE.md).
