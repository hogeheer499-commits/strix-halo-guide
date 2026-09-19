---
layout: default
title: "Best Strix Halo Mini PC for Local LLMs (2026): Beelink vs Framework vs GMKtec vs Corsair"
description: "Evidence-based comparison of AMD Ryzen AI MAX+ 395 mini PCs for local LLMs: measured cross-OEM benchmarks, 64GB vs 128GB fit guidance, dated prices, and buy-now-or-wait timing."
permalink: /best-strix-halo-mini-pc/
canonical_url: "https://strixhaloguide.com/best-strix-halo-mini-pc/"
sitemap: false
date: "2026-08-21T00:00:00+02:00"
last_modified_at: "2026-09-19T00:00:00+02:00"
image:
  path: "https://hogeheer499-commits.github.io/strix-halo-guide/assets/social-preview.png"
  height: 640
  width: 1280
  alt: "AMD Strix Halo mini PC comparison for local LLMs with measured cross-OEM evidence"
seo:
  type: "TechArticle"
  date_modified: "2026-09-19T00:00:00+02:00"
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

The [September 13 configuration-specific snapshot](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BUYER_SNAPSHOT_2026-09-13.md) records exact RAM/SSD selections, complete-system versus mainboard scope, currency, fulfillment and seller-advertised warranty/return terms. Delivered tax/shipping/import totals remain unknown. The [July CSV](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/buyer_price_snapshot_2026-07-27.csv) is retained as historical evidence.

In the **September 13, 2026 US-facing/USD snapshot**, the observed offers were Beelink 128GB/2TB $4,349, Bosgame M5 128GB/2TB US-plug $2,999, Framework 128GB **mainboard** $3,149, and Minisforum 128GB/2TB $3,799. GMKtec US $2,199.99 was a **64GB/1TB** selection, not a 128GB price. These observations were not re-priced for this editorial update. See the linked snapshot for source URLs and fulfillment conflicts; these are not checkout quotes. At that check, Corsair's exact 128GB/4TB SKU was out of stock with extracted price unknown; Nimo and HP selected quotes remained unresolved. Confirm present stock before ordering.

Earlier August claims of an exact AMD Micro Center price/exclusivity/start date and a Framework 192GB PRO 495 successor lacked sufficient linked primary substantiation and are withdrawn from current buying guidance. Stock banners do not predict future prices.

## Buy now or wait?

Buy when a currently available configuration supports a task you need now at an acceptable delivered price. Waiting can be sensible when your current machine is adequate, the price exceeds your budget, or your workload needs more capacity than the tested system offers. Future prices and performance are uncertain.

Published larger-memory options belong in a capacity comparison; they do not inherit the guide's 128GB speed or feature results. Check the exact processor, memory and shipping configuration on the [official Framework Desktop page](https://frame.work/desktop) and other vendor listings. Do not infer the specification of a new GMKtec model from its EVO-X generation number alone.

If your chosen artifact fits in a discrete GPU's VRAM, also compare an existing or used GPU system and Apple silicon against your actual workload. Include the complete host cost, software requirements, power and noise; this guide does not establish a universal price/performance winner across those platforms.

## How to compare the systems

The repository [Buying Guide](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#buying-guide) describes evidence depth per system. Beelink has the deepest first-party evidence here, not proof of intrinsically superior hardware. GMKtec and Corsair have attributed community evidence; Bosgame needs same-configuration buyer-path reproduction before a comparative performance claim. Framework's modular design is a selection consideration, not measured support superiority. Minisforum's networking may matter to a cluster buyer, but the exact network/runtime combination still needs qualification. None is a universal value winner on these unmatched results and dated offers.

The comparison considers memory configuration, dated price/availability, evidence depth,
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
