---
layout: default
title: "Best Strix Halo Mini PC for Local LLMs: 128GB Buyer Guide"
description: "Compare Strix Halo mini PCs using dated prices, memory requirements, first-party and community evidence, and practical local-AI buying checks."
permalink: /best-strix-halo-mini-pc/
canonical_url: "https://strixhaloguide.com/best-strix-halo-mini-pc/"
sitemap: false
date: "2026-08-21T00:00:00+02:00"
last_modified_at: "2026-09-19T00:00:00+02:00"
image:
  path: "https://hogeheer499-commits.github.io/strix-halo-guide/assets/social-preview.png"
  height: 640
  width: 1280
  alt: "AMD Strix Halo local AI setup, benchmarks and buyer evidence"
seo:
  type: "TechArticle"
  date_modified: "2026-09-19T00:00:00+02:00"
---

# Best Strix Halo Mini PC for Local LLMs (2026)

**Evidence reviewed:** September 26, 2026.

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

- **64GB** is a capacity candidate for the smaller Q4 MoE artifacts, such as Qwen3-Coder 30B and LFM2.5 8B-A1B. Confirm runtime overhead, context, concurrent requests and OS memory on the actual machine. It cannot hold the ~91GB DeepSeek capacity artifact entirely in memory. Newer 30B-class candidates that are published but not measured here are listed in the [model hub](models.md). Complete 64GB MAX+ 395 systems exist (for example Minisforum's MS-S1 MAX 64GB/2TB listing; see [hardware context](#other-strix-halo-systems-hardware-context-only)); they do not inherit the 128GB results on this page.
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
| 2026-05-01 | $4,399 (compare-at $4,699) | vendor page as recorded in the [May 1 price audit](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#2026-05-01----price-audit--documentation-reconciliation) |
| 2026-07-27 | $4,349 (list $4,699), pre-sale, ships within 35 days | [July CSV](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/buyer_price_snapshot_2026-07-27.csv) |
| 2026-08-21 | $4,349 (list $4,699), pre-sale | [vendor page](https://www.bee-link.com/products/beelink-gtr9-pro-amd-ryzen-ai-max-395) |
| 2026-08-29 | $4,349 (list $4,699), pre-sale, ships within 35 days — unchanged | [vendor page](https://www.bee-link.com/products/beelink-gtr9-pro-amd-ryzen-ai-max-395), re-verified |
| 2026-09-13 | $4,349 (compare-at $4,699), pre-sale | [September 13 snapshot](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BUYER_SNAPSHOT_2026-09-13.md) |
| 2026-09-19 | $4,349, pre-sale, seller-stated dispatch within 35 days | [September 19 snapshot](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BUYER_SNAPSHOT_2026-09-19.md) |

**Board/NIC revision (checked 2026-09-25):** Beelink's [Q1 2026 BIOS summary](https://www.bee-link.com/blogs/all/bios-update-summary-for-q1-2026) lists separate BIOS lines for the original GTR9 Pro board (GTRPR05) and a "New NIC v2.2" board (GTRPR07); it does not name the network chip. User reports in the [Beelink forum thread](https://bbs.bee-link.com/d/7762-gtr-9-pro-ethernet-malfunction-under-load) describe v1.0 boards with Intel E610 networking, some with NIC disconnection failures under load, and v2.2 boards with a Realtek RTL8127 chip. This guide has not established which revision current stock ships; confirm the board/NIC revision with the seller before ordering. See the README [board/NIC revision note](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#buying-guide).

The recorded Beelink prices increased over this period, with a small step down from $4,399 (May 1) to $4,349 (July 27 onward). That history does not establish every vendor's cost structure or predict the next price. As one vendor-stated cost driver, Framework's [memory-pricing updates](https://frame.work/blog/updates-on-memory-pricing-and-navigating-the-volatile-memory-market) (latest update dated 2026-09-08 when read on 2026-09-25) attribute repeated 2026 price increases for its 128GB Desktop to LPDDR5x memory costs; that is Framework's statement about its own products, not a forecast for other OEMs. Compare the exact RAM/SSD variant, region, tax, delivery date and warranty before purchasing; a storefront's lowest advertised price can belong to a smaller configuration.

The [September 19 exact-SKU snapshot](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BUYER_SNAPSHOT_2026-09-19.md) separates complete systems, mainboards, regions, selected variants and unresolved checkout fields. US-facing/USD observations: GMKtec EVO-X2 **128GB/2TB $3,649.99** (the $2,199.99 offer is **64GB/1TB**), Beelink **128GB/2TB $4,349** pre-sale with seller-stated dispatch within 35 days, Bosgame **128GB/2TB $2,999** with present ETA unresolved, Minisforum **128GB/2TB $3,799** with early-October shipping, and Nimo **128GB/2TB $3,899.99**, structured InStock but delivery ETA unresolved.

Framework's current 128GB **mainboard** quote and HP's selected laptop quote remained unresolved. Corsair's exact 128GB/4TB SKU was out of stock with price unresolved. Tax/shipping/import are not complete delivered quotes. No older price was silently re-dated. GMKtec EVO-X3 128GB/2TB was $3,799.99 with MAX+ 395; EVO-X2 benchmarks do not qualify EVO-X3.

GMKtec evidence here remains community/external, not a first-party exact-retail-SKU buyer-path campaign. The missing proof is a stock exact-SKU setup, text/image/tool/client and restart/reboot reproduction, including firmware, elapsed time and interventions. The [September 13 snapshot](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BUYER_SNAPSHOT_2026-09-13.md) and [July CSV](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/buyer_price_snapshot_2026-07-27.csv) remain historical.

**EU storefront observations (EUR, observed 2026-09-25).** Listed prices on official EU storefronts, not delivered checkout quotes:

| Store | Configuration | Listed price | Seller terms as stated on the page |
|---|---|---|---|
| [GMKtec EU](https://de.gmktec.com/en/products/gmktec-evo-x2-amd-ryzen%E2%84%A2-ai-max-395-mini-pc-1) | EVO-X2 128GB/1TB | €3,229.99 | Prices based on EU warehouse fulfillment (Germany where available); VAT or import duties may apply for shipments from non-EU origin; change-of-mind returns carry a 15% repackaging/restocking fee |
| GMKtec EU (same page) | EVO-X2 128GB/2TB | €3,349.99 | as above |
| [Beelink EU](https://eu.bee-link.com/products/beelink-gtr9-pro-amd-ryzen-ai-max-395) | GTR9 Pro 128GB/2TB | €4,619 (compare-at €5,199) | VAT inclusion not established from this capture |
| [Minisforum EU](https://minisforumpc.eu/products/minisforum-ms-s1-max-mini-pc) | MS-S1 MAX 128GB/2TB | €3,999 | VAT inclusion not established from this capture; the store publishes an [EU right-of-withdrawal page](https://minisforumpc.eu/pages/eu-right-of-withdrawal) |

Beelink's main store bills the same GTR9 Pro configuration in USD ($4,349 above), so EU buyers can see two different official price points. No USD price was converted to EUR here. For the statutory 14-day withdrawal right on online purchases in the EU, see [Your Europe](https://europa.eu/youreurope/citizens/consumers/shopping/returns/index_en.htm); seller restocking terms are quoted as stated, not as legal advice. The July EUR rows in the July CSV keep their own date.

Stock banners do not predict future prices.

## Announced and other Strix Halo-class hardware (not measured here)

Everything in this section is dated hardware context. None of these systems or processors has first-party or community evidence in this guide, and none inherits the MAX+ 395 / 128GB results above. Specifications are vendor statements, not measurements.

**Ryzen AI Max PRO 400 Series: announced, systems pending (checked 2026-09-25).** AMD [announced the Ryzen AI Max PRO 400 Series](https://www.amd.com/en/blogs/2026/amd-powers-next-generation-agent-computers-with-new-ryzen-ai-hal.html) on 2026-05-20. AMD lists the [Ryzen AI Max+ PRO 495](https://www.amd.com/en/products/processors/laptop/ryzen-pro/ai-max-pro-400-series/amd-ryzen-ai-max-plus-pro-495.html) with 16 cores, Radeon 8065S graphics with 40 CUs and up to 192GB LPDDR5x-8533; the [PRO 490](https://www.amd.com/en/products/processors/laptop/ryzen-pro/ai-max-pro-400-series/amd-ryzen-ai-max-pro-490.html) and [PRO 485](https://www.amd.com/en/products/processors/laptop/ryzen-pro/ai-max-pro-400-series/amd-ryzen-ai-max-pro-485.html) use Radeon 8050S graphics with 32 CUs. OEM systems have been announced but were not shipping when checked: HP's [ZBook Ultra G3a](https://www.hp.com/us-en/newsroom/press-releases/2026/hp-redefines-the-mobile-workstation-for-the-era-of-agentic-ai.html) laptop (announced 2026-09-15, expected October 2026), Lenovo's [ThinkCentre X Ultra](https://news.lenovo.com/pressroom/press-releases/hybrid-ai-for-business-devices-displays-solutions/) (announced 2026-09-03, starting November 2026, up to 128GB) and Framework's [Desktop page](https://frame.work/desktop?tab=192gb-coming-soon), which lists a PRO 495 configuration with 192GB as "coming soon" with no price or date. The guide has not measured any of them, and a 192GB memory setup is not qualified here: the setup script and memory guidance were written for 128GB systems.

**AMD Ryzen AI Halo.** This is an AMD reference/developer platform, not a retail OEM mini PC. AMD's [2026-07-06 post](https://www.amd.com/en/blogs/2026/amd-ryzen-ai-halo-now-available-at-micro-center.html) says it is now available at Micro Center and calls Micro Center its "first global launch partner". AMD's post gives no price, and this guide has not read a price on a Micro Center page, so the price is left unresolved here. There is no first-party measurement of the Ryzen AI Halo; see the [Ryzen AI Halo context](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/RYZEN_AI_HALO_CONTEXT.md) for how reference-platform material stays separate from retail evidence.

**Other 2026 SKUs.** AMD's [CES 2026 announcement](https://ir.amd.com/news-events/press-releases/detail/1270/amd-expands-ai-leadership-across-client-graphics-and-software-with-new-ryzen-ryzen-ai-and-amd-rocm-announcements-at-ces-2026) (2026-01-05) added the Ryzen AI Max+ 392 (12 cores) and Max+ 388 (8 cores), both with the full 40-CU Radeon 8060S graphics. The PRO 490/485 above have 32-CU Radeon 8050S graphics. None of these SKUs is measured here; the MAX+ 395 results on this page do not qualify them. Check the exact processor on any listing.

### Other Strix Halo systems: hardware context only

These systems exist but have no community or first-party evidence in this guide. Prices are exact-SKU storefront observations in US/USD on 2026-09-25, not current offers. Listing order is alphabetical, not a ranking.

| System | Processor and configuration | Dated observation (2026-09-25) |
|---|---|---|
| [Acemagic M1A PRO+](https://acemagic.com/products/m1a-395) | MAX+ 395, 128GB/2TB | $3,099 on acemagic.com |
| [GEEKOM A9 Mega](https://www.geekompc.com/geekom-a9-mega-ai-mini-pc/) | MAX+ 395 or MAX+ 388 per vendor page | price not captured |
| [HP Z2 Mini G1a](https://www.cdw.com/product/hp-z2-mini-g1a-workstation-1-x-amd-ryzen-ai-max-pro-395-128-gb-2-tb/8440785) | Ryzen AI Max PRO 395, 128GB/2TB (C3XE1UT#ABA) | $7,707.99 at CDW, which also shows "sign in for your price" |
| [Minisforum MS-S1 MAX 64GB](https://store.minisforum.com/products/minisforum-ms-s1-max-64gb) | MAX+ 395, 64GB/2TB (MS-S1-MAX62US) | $2,599 (compare-at $3,249) |
| [ONEXStation](https://onexplayerstore.com/products/onexstation-mini-ai-workstation-ryzen%e2%84%a2-ai-max-395-up-to-128gb-ram-ai-mini-pc) | MAX+ 395, 128GB/1TB or 128GB/2TB | $3,199 (1TB); $3,499 (2TB, compare-at $3,599). The launch price reported in April 2026 was lower; this row uses the observed store price |

## Buy now or wait?

Buy when a currently available configuration supports a task you need now at an acceptable delivered price. Waiting can be sensible when your current machine is adequate, the price exceeds your budget, or your workload needs more capacity than the tested system offers. Future prices and performance are uncertain.

Published larger-memory options belong in a capacity comparison; they do not inherit the guide's 128GB speed or feature results. Check the exact processor, memory and shipping configuration on the [official Framework Desktop page](https://frame.work/desktop) and other vendor listings. Do not infer the specification of a new GMKtec model from its EVO-X generation number alone.

If your chosen artifact fits in a discrete GPU's VRAM, also compare an existing or used GPU system and Apple silicon against your actual workload. Include the complete host cost, software requirements, power and noise; this guide does not establish a universal price/performance winner across those platforms.

**Other 128GB-class platforms (dated context, no ranking).** NVIDIA raised the DGX Spark Founders Edition MSRP to $4,699 in its [price-change announcement](https://forums.developer.nvidia.com/t/2-23-2026-price-change-announcement/361713) posted 2026-02-25. The ASUS eShop US listed the GB10-based [Ascent GX10](https://eshop.asus.com/us/ascent-gx10.html) with 2TB at $6,999 when observed on 2026-09-25. NVIDIA's RTX Spark Windows systems were [announced](https://nvidianews.nvidia.com/news/nvidia-microsoft-windows-pcs-agents-rtx-spark) for "this fall" and were not shipping when checked. Apple [announced](https://www.apple.com/newsroom/2026/08/apple-introduces-new-mac-studio-with-m5-max-and-m5-ultra/) the Mac Studio with M5 Max and M5 Ultra on 2026-08-25, [available from 2026-09-22](https://www.apple.com/newsroom/2026/09/the-new-mac-mini-and-mac-studio-are-available-today/). On 2026-09-25 the US [Apple Store](https://www.apple.com/shop/buy-mac/mac-studio) listed M5 Max with 36GB memory and 512GB storage at $2,499, M5 Max with 64GB/1TB at $3,099 and M5 Ultra with 96GB/1TB at $5,499. The 128GB M5 Max price was not captured, and the 512GB M5 Ultra memory option was listed as coming late October. The guide has no matched measurement on any of these platforms and does not rank them against Strix Halo; the [cost of local vs cloud](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#cost-local-vs-cloud) section covers the separate cloud question.

## Daily use: power, thermals, noise

There is no first-party Beelink wall-power or noise measurement in this guide. What exists is scoped:

- [Power baseline](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/POWER_BASELINE.md): community-reported whole-system wall power from Corsair AI Workstation 300 systems, kept separate from the Beelink's amdgpu `PPT` telemetry. PPT is not wall power, and neither is a Beelink efficiency claim.
- [Thermal stability](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/THERMAL_STABILITY.md): community sustained-load thermal and clock evidence from three Corsair / Sixunited systems in one fleet; not a general recommendation for other chassis.
- [Nimo community notes](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/COMMUNITY_NIMO.md): contributor-reported fan noise (peak around 46 dBA) and power/temperature values with incomplete instrument and sampling metadata. They do not qualify noise or wall-power comparisons between systems.

Vendor noise or TDP figures on product pages are marketing statements, not measurements.

## How to compare the systems

The repository [Buying Guide](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#buying-guide) describes evidence depth per system. Beelink has the deepest first-party evidence here, not proof of intrinsically superior hardware. GMKtec and Corsair have attributed community evidence; Bosgame needs same-configuration buyer-path reproduction before a comparative performance claim. Framework's modular design is a selection consideration, not measured support superiority. Minisforum's networking may matter to a cluster buyer, but the exact network/runtime combination still needs qualification. None is a universal value winner on these unmatched results and dated offers.

For workflow fit, see the [buyer use cases](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BUYER_USE_CASES.md) and the [Windows vs Linux](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#windows-vs-linux) evidence table.

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
Wait if a currently available configuration cannot meet your task or budget. As of 2026-09-25, Ryzen AI Max PRO 400 systems were announced but not shipping and are not measured here (see [announced hardware](#announced-and-other-strix-halo-class-hardware-not-measured-here)). Check confirmed product specifications and shipping dates; more advertised memory does not by itself prove faster inference, and future prices are uncertain.

**Are these prices current?**
Every snapshot has its own date. Verify the exact region, RAM/SSD configuration, tax, shipping and stock on the vendor's current page. The historical price table is not a live quotation.


---

Community corrections are welcome — open an issue in the [repository](https://github.com/hogeheer499-commits/strix-halo-guide/issues). Pricing rows are dated snapshots, not live quotes. This page contains no affiliate links as of September 19, 2026; if that changes, links will be disclosed next to the relevant product and per [`VENDOR_DISCLOSURE.md`](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/VENDOR_DISCLOSURE.md).
