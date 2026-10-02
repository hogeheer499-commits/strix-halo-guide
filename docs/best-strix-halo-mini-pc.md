---
layout: default
title: "Best Strix Halo Mini PC for Local LLMs: 128GB Buyer Guide"
description: "Compare Strix Halo mini PCs using dated prices, memory requirements (64, 128 or 192GB), first-party and community evidence, and practical local-AI buying checks for the US and Europe."
permalink: /best-strix-halo-mini-pc/
canonical_url: "https://strixhaloguide.com/best-strix-halo-mini-pc/"
sitemap: false
date: "2026-08-21T00:00:00+02:00"
last_modified_at: "2026-10-01T00:00:00+02:00"
image:
  path: "https://hogeheer499-commits.github.io/strix-halo-guide/assets/social-preview.png"
  height: 640
  width: 1280
  alt: "AMD Strix Halo local AI setup, benchmarks and buyer evidence"
seo:
  type: "TechArticle"
  date_modified: "2026-10-01T00:00:00+02:00"
---

# Best Strix Halo Mini PC for Local LLMs (2026)

**Evidence reviewed:** October 1, 2026.

Start with the independent [Strix Halo Guide](https://strixhaloguide.com/) for
the current setup and evidence model; use this page for the buyer comparison.

**Short answer:** choose a Strix Halo mini PC by the exact model artifact and context you need, the delivered price for that memory configuration, cooling, firmware and support. The guide has useful first-party and community results, but the cross-OEM rows below are not a controlled ranking. A 128GB system is valuable for the larger measured artifacts; a smaller configuration may be sufficient for a smaller workload.

This page interprets the evidence in the [canonical Strix Halo guide repository](https://github.com/hogeheer499-commits/strix-halo-guide). Every number links to a dated source; first-party and community measurements stay labeled. The first-party Beelink GTR9 Pro was bought by the maintainer; no loaned, gifted or sponsored hardware is used for first-party results (statement as of 2026-09-26 in [`VENDOR_DISCLOSURE.md`](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/VENDOR_DISCLOSURE.md#current-relationships-and-hardware-provenance)).

Newest price observations (US, EU, NL/DE; observed 2026-09-30): the [September 30 exact-SKU snapshot](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BUYER_SNAPSHOT_2026-10-01.md) and its [CSV](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/buyer_price_snapshot_2026-09-30.csv).

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

- **64GB** is a capacity candidate for the smaller Q4 MoE artifacts, such as Qwen3-Coder 30B and LFM2.5 8B-A1B, and for the dense Qwen3.8 27B (Ollama `Q4_K_M` artifact, 17.7GB). Confirm runtime overhead, context, concurrent requests and OS memory on the actual machine. It cannot hold the ~91GB DeepSeek capacity artifact entirely in memory. Of the four newer 30B-class candidates in the [model hub](models.md), three (Nemotron 3.5 Lightning, Laguna XS 2.1 and Muse Glimmer 30B) were scouted on 2026-09-26; Granite 4.2 30B is published but not measured here. Qwen3.8 27B (dense) was measured through Ollama 0.32.15 on 2026-09-26 at 12.89 tok/s without a draft model and 22.71 tok/s with MTP ([raw bundle](https://github.com/hogeheer499-commits/strix-halo-guide/tree/main/data/raw/2026-09-26/qwen38-27b-ollama-03215-mtp-vs-nodraft)). All of these were measured on the 128GB machine: speed and load only, not a 64GB fit. Complete 64GB MAX+ 395 systems exist (for example Minisforum's MS-S1 MAX 64GB/2TB listing; see [hardware context](#other-strix-halo-systems-hardware-context-only)); they do not inherit the 128GB results on this page.
- **What a 64GB buyer should check before ordering (claims of a third party, not tested here).** A Level1Techs review of a 64GB Minisforum N5 MAX ([review notes](https://forum.level1techs.com/t/nas-review-notes-minisforum-n5-max-amd-strix-halo/251183), tested on Proxmox VE 9.1.1, read 2026-10-02; details in [LAPTOPS_AND_HOMELAB.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/LAPTOPS_AND_HOMELAB.md#nas-style-chassis-minisforum-n5-max)) reports that the GPU sees about 30 GiB by default, that models above about 30 GiB load only after the memory split is changed, and that the memory is soldered, so it cannot be upgraded later. That is one review of one chassis. Whether the same holds for another system was not checked here, so confirm the memory configuration with the seller before ordering. This guide has no 64GB memory profile: `setup.sh` accepts only about 120 to 136 GiB of visible RAM, and the README says not to copy the 128GB values to other sizes.
- **128GB** unlocks the routes that make this platform special: Nemotron 3 Super 120B-A12B direct GGUF (~18–19 t/s measured), Step 3.7 Flash 198B server route, and the pinned 90.86GB DeepSeek V4 Flash 284B artifact ([capacity evidence](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/raw/2026-07-16/deepseek-v4-flash-ud-iq2-xxs/), a scoped direct speed and basic correctness result, not a broad quality qualification).
- The measured Llama 3.1 70B Q4_K_M route generates ~4.7–4.9 t/s. Decide whether that latency is acceptable for your task. It does not establish the speed of every dense 70B model or a universal minimum for useful chat.

Budget for model weights, KV cache, runtime buffers, concurrent sequences and the OS. A fixed 10–20GB allowance does not qualify every architecture or context length. Use the [model hub](models.md) to separate measured artifacts from published-size estimates. The [best-known profiles table](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BEST_KNOWN_PROFILES.md) maps workloads to measured routes. For 192GB systems see [128GB or 192GB?](#128gb-or-192gb) below.

**Vendor tier table (claims of a vendor, not reproduced).** Framework's Desktop product page (NL, checked 2026-09-30) lists a recommended open model per memory tier as of September 2026, stated as measured on Framework's reference configuration: 32GB Qwen3.8-27B UD-Q4_K_XL (17.6GB), 64GB Qwen3.5-122B-A10B Q3_K_S (52.5GB), 128GB DeepSeek V4 Flash 0731 UD-IQ2_XXS (90.9GB) and 192GB DeepSeek V4.1 Flash Q2 (163GB). The 128GB entry has the same quantization and size class (90.9GB) as the pinned artifact above; whether it is the same file was not checked. For 64GB this guide names smaller artifacts (Qwen3-Coder 30B, LFM2.5 8B-A1B and the dense Qwen3.8 27B, all measured only on the 128GB machine), and the 122B MoE at Q3 is a candidate that was not tested here, not a recommendation ([Framework Desktop page](https://frame.work/nl/en/desktop)).

## 128GB or 192GB?

**Checked 2026-09-30.** 192GB configurations use the Ryzen AI Max+ PRO 495 (systems and prices: [PRO 400 table](#ryzen-ai-max-pro-400-systems-checked-2026-09-30)). No 192GB system is measured here, and the guide's setup script and memory profile are written for 128GB systems: `setup.sh` stops above about 136GiB of visible RAM because no 192GB profile is qualified. The amounts below are arithmetic on dated list prices, or claims of vendors and third parties, not measurements.

| Vendor and store | 128GB reference | 192GB configuration | Difference (calculation) |
|---|---|---|---|
| Framework, NL store, EUR, VAT included (store tooltip) | [Desktop DIY, Max+ 395, 128GB](https://frame.work/nl/en/products/desktop-diy-amd-aimax300/configuration/new): €3,889, listed as out of stock | [Desktop DIY, Max+ PRO 495, 192GB](https://frame.work/nl/en/products/desktop-diy-amd-aimax400/configuration/new): €7,659, pre-order, ships in November | €3,770. Both are DIY editions without storage or operating system |
| Framework, US, USD, tax not stated | 128GB Desktop from $3,449 ([Phoronix](https://www.phoronix.com/news/Framework-Desktop-Gorgon-Halo), secondary source) | DIY Edition from $6,799 ([Framework on X](https://x.com/FrameworkPuter/status/2105326903225925740)) | $3,350 |
| GMKtec, US store, USD, tax not stated | [EVO-X2](https://www.gmktec.com/products/amd-ryzen%E2%84%A2-ai-max-395-evo-x2-ai-mini-pc) 128GB/2TB: $3,649.99 | [EVO-X5 Pro](https://www.gmktec.com/products/gmktec-evo-x5-pro-amd-ryzen-ai-max-pro-495-ai-mini-pc) 192GB/2TB: regular price $6,799 (temporary early-bird price $6,599) | $3,149 at the regular price. Different chassis |
| Minisforum, US store, USD, tax not stated | [MS-S1 MAX](https://store.minisforum.com/products/minisforum-ms-s1-max-mini-pc) 128GB/2TB: $3,799 | [MS-S1 MAX-P495](https://store.minisforum.com/products/minisforum-ms-s1-max-p495-ai-workstation) 192GB/2TB: $7,399 (compare-at price $9,249) | $3,600. Different model |

- **Memory speed is not settled by store text.** AMD lists LPDDR5x-8533 as the maximum for the [PRO 495](https://www.amd.com/en/products/processors/laptop/ryzen-pro/ai-max-pro-400-series/amd-ryzen-ai-max-plus-pro-495.html). Framework, Minisforum and Acemagic state 8533 MT/s for their 192GB systems, Lenovo states 8533MHz for its X Ultra (up to 128GB), and GMKtec's page says "up to" 8533 for 192GB. HP's [product page](https://www.hp.com/us-en/workstations/mobile-workstation-pc/zbook-ultra-g3.html) footnote says up to 8000 MT/s for 128GB and 192GB, while HP's [QuickSpecs](https://www8.hp.com/h20195/v2/GetDocument.aspx?docname=c09287369) (version 3, 2026-09-22) says the system runs at 8533 MT/s. The guide's measured 128GB systems run LPDDR5X-8000 ([host record](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/REPRODUCIBILITY.md)). Check the configured speed after delivery with `sudo dmidecode -t memory`; the guide makes no speed claim for 192GB systems.
- **"Up to 160GB of VRAM" is a vendor figure.** HP's product page says up to 192GB of unified memory sharing up to 160GB of dedicated VRAM via BIOS or GUI, Minisforum's EU page lists 160GB of allocatable VRAM for the P495, and [Tweakers](https://tweakers.net/nieuws/251824/192gb-mini-pcs-met-nieuwe-amd-processor-kosten-rond-8000-dollar.html) wrote on 2026-09-06 that the PRO 495's GPU cannot address the full 192GB but at most 160GB (claim of a third party). This guide recommends a small fixed BIOS reserve plus GTT instead of a large fixed carve-out (see the [setup page](https://strixhaloguide.com/amd-strix-halo-setup/)). Neither approach is tested on 192GB, and whether 160GB is the limit on Linux with GTT is to verify.
- **More memory is not more speed.** Framework states 273 GB/s for its 192GB configuration ([launch post](https://community.frame.work/t/192gb-framework-desktop-open-for-pre-order/85192), 2026-09-30), which equals 8533 MT/s on a 256-bit bus; the same bus at 8000 MT/s gives 256 GB/s (calculation). Framework's blog claims about 6.7 percent more theoretical bandwidth than Strix Halo. The guide uses a rough weight-streaming estimate of ~215 GB/s divided by the weight size for dense models (see the [README](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md); an estimate, not a ceiling). If the artifact you need fits in 128GB, this guide has no measurement showing a speed gain from 192GB; a larger dense artifact fits but streams more weight bytes per token.
- **NPU on Linux.** The PRO 495 NPU needs a driver change targeted at Linux 7.4: the patch was posted on 2026-09-29 and applied to the drm-misc-next tree ([Phoronix](https://www.phoronix.com/news/AMD-Gorgon-Halo-NPU-LInux), 2026-09-30); the merge window is expected in late October and a stable release around year-end. A backport is possible but unconfirmed. Framework states that existing software carries over to the 192GB Desktop ([post](https://community.frame.work/t/what-192gb-changes-for-local-ai-on-the-framework-desktop/85191)); that is a vendor statement about the GPU route and is not tested here.
- **Vendor-published model claims (not reproduced).** Framework's [launch blog](https://frame.work/nl/en/blog/what-192gb-changes-for-local-ai-on-the-framework-desktop) (2026-09-30) reports DeepSeek V4.1 Flash Q2 running on a single 192GB machine at about 14 t/s without speculative decoding, and MiMo V2.6 Flash falling from about 18 to about 16 t/s between 0 and 64K context. These are vendor-published claims about Framework's reference configuration; this guide has not reproduced them. Which published artifacts need more than 128GB is tracked in the [model hub](models.md).

### One 192GB system or two 128GB systems?

Price arithmetic plus the guide's existing cluster data. Nothing here is measured on 192GB.

| | One 192GB system | Two 128GB systems |
|---|---|---|
| Price example, Framework NL DIY, EUR, VAT included (2026-09-30) | €7,659 | 2 × €3,889 = €7,778 (the 128GB DIY edition was listed as out of stock) |
| Price example, Framework US, USD (2026-09-30) | $6,799 | 2 × $3,449 = $6,898 (secondary source for the 128GB price) |
| Memory | 192GB in one machine | 256GB in total, split across two machines; per-node limits and overhead apply |
| Speed when the model fits on one box | No measured gain from the extra memory | Guide data: 2-node RPC lost about 14-22% tg128 on models that fit one box ([community RPC](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/COMMUNITY_RPC.md)) |
| Models larger than 128GB | One memory pool; no 192GB result measured here | The MiniMax-M2.7 case (140.8GB) needed two nodes in the guide's community RPC data |
| Operation | One machine | Two machines to power and maintain, plus a network link and cluster software; see the cluster notes in [Secure local AI](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/SECURE_LOCAL_AI.md) |

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
| 2026-09-30 | $4,349, pre-sale; the page text says orders ship within 35 days (US store, USD, tax not stated) | [vendor page](https://www.bee-link.com/products/beelink-gtr9-pro-amd-ryzen-ai-max-395), [September 30 snapshot](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BUYER_SNAPSHOT_2026-10-01.md) |

**Board/NIC revision (checked 2026-09-30):** Beelink's [Q1 2026 BIOS summary](https://www.bee-link.com/blogs/all/bios-update-summary-for-q1-2026) lists separate BIOS lines for the original GTR9 Pro board (GTRPR05) and a "New NIC v2.2" board (GTRPR07); it does not name the network chip. User reports in the [Beelink forum thread](https://bbs.bee-link.com/d/7762-gtr-9-pro-ethernet-malfunction-under-load) describe v1.0 boards with Intel E610 networking, some with NIC disconnection failures under load, and v2.2 boards with a Realtek RTL8127 chip. Independent press reported the same pattern: [ComputerBase](https://www.computerbase.de/news/pc-systeme/gtr9-pro-beelinks-2-400-euro-strix-halo-pc-ist-von-problemen-geplagt.95273/) (2025-12-03, before the v2.2 board) wrote that on the Intel E610 LAN ports a local LLM run (LM Studio, Llama 4 Scout) crashed the system reproducibly, and that the ports worked again only after the power cable was removed; according to ComputerBase, Beelink pointed to Intel's driver and said it would replace or repair units it cannot fix. Beelink also publishes dated BIOS files, including a test BIOS described as a fix for an E610 LAN issue (see the [BIOS update route](#bios-update-route-checked-2026-09-30)); this guide has not tested them, and a test BIOS is not qualified here. The guide has not recorded the BIOS version of its own first-party unit for its published runs ([host record](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/REPRODUCIBILITY.md)), and the board/NIC revision of that unit is not stated in this guide. Confirm the board/NIC revision and BIOS with the seller before ordering. See the README [board/NIC revision note](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#buying-guide).

The recorded Beelink prices increased over this period, with a small step down from $4,399 (May 1) to $4,349 (July 27 onward). That history does not establish every vendor's cost structure or predict the next price. As one vendor-stated cost driver, Framework's [memory-pricing updates](https://frame.work/blog/updates-on-memory-pricing-and-navigating-the-volatile-memory-market) (latest update dated 2026-09-08 when read on 2026-09-25) attribute repeated 2026 price increases for its 128GB Desktop to LPDDR5x memory costs; that is Framework's statement about its own products, not a forecast for other OEMs. Compare the exact RAM/SSD variant, region, tax, delivery date and warranty before purchasing; a storefront's lowest advertised price can belong to a smaller configuration.

The [September 19 exact-SKU snapshot](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BUYER_SNAPSHOT_2026-09-19.md) separates complete systems, mainboards, regions, selected variants and unresolved checkout fields. US-facing/USD observations of that date: GMKtec EVO-X2 **128GB/2TB $3,649.99** (the $2,199.99 offer is **64GB/1TB**), Beelink **128GB/2TB $4,349** pre-sale with seller-stated dispatch within 35 days, Bosgame **128GB/2TB $2,999** with present ETA unresolved, Minisforum **128GB/2TB $3,799** with early-October shipping, and Nimo **128GB/2TB $3,899.99**, structured InStock but delivery ETA unresolved.

In the September 19 snapshot, Framework's 128GB **mainboard** quote and HP's selected laptop quote remained unresolved (Framework's NL store prices are in the September 30 snapshot). Corsair's exact 128GB/4TB SKU was out of stock with price unresolved. Tax/shipping/import are not complete delivered quotes. No older price was silently re-dated. GMKtec EVO-X3 128GB/2TB was $3,799.99 with MAX+ 395; EVO-X2 benchmarks do not qualify EVO-X3.

**What changed by September 30 (items re-checked).** US/USD prices were unchanged for GMKtec EVO-X2 128GB/2TB ($3,649.99), Beelink ($4,349), Minisforum MS-S1 MAX 128GB/2TB ($3,799) and Acemagic M1A PRO+ ($3,099); the "early October" shipping text for Minisforum is no longer shown on the MAX+ 395 variants, so its ETA is unknown. GMKtec's EU store listed higher EVO-X2 prices than on 2026-09-25 (the location of the earlier observation was not recorded; see [Buying in Europe](#buying-in-europe-checked-2026-09-30)). Bosgame has two stores with different prices ($3,099 on bosgame.com on 2026-09-30; $2,999 on bosgamepc.com on 2026-09-19, not re-checked), and prices can differ by visitor location, so each row names its country. Nimo, ONEXStation, Corsair and the HP laptop quote were not re-checked; details are in the [September 30 snapshot](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BUYER_SNAPSHOT_2026-10-01.md).

GMKtec evidence here remains community/external, not a first-party exact-retail-SKU buyer-path campaign. The missing proof is a stock exact-SKU setup, text/image/tool/client and restart/reboot reproduction, including firmware, elapsed time and interventions. The [September 13 snapshot](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BUYER_SNAPSHOT_2026-09-13.md) and [July CSV](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/buyer_price_snapshot_2026-07-27.csv) remain historical.

Stock banners do not predict future prices.

## Buying in Europe (checked 2026-09-30)

Two routes exist for EU buyers: **(a)** the manufacturer's EU web store, and **(b)** a local retailer, found through a price-comparison site such as [Tweakers Pricewatch](https://tweakers.net/pricewatch/) (NL) or [Geizhals](https://geizhals.de/) (DE/AT). All figures are listings observed on 2026-09-30, not delivered checkout quotes. Store terms are quoted as stated on each page ("according to the store's terms"); this is not legal advice, and the guide has not examined whether any clause is enforceable. No USD price was converted to EUR here.

### Route (a): manufacturer EU web stores

| Store and configuration | Listed price (EUR) | Seller and governing law, as stated | Returns, as stated | Factory warranty and commercial use, as stated |
|---|---|---|---|---|
| [GMKtec EU](https://de.gmktec.com/en/products/gmktec-evo-x2-amd-ryzen%E2%84%A2-ai-max-395-mini-pc-1), EVO-X2 128GB/1TB, 128GB/2TB, 64GB/1TB | €3,299.99, €3,399.99, €1,999.99 (VAT inclusion not established; observed from a Netherlands IP address). On 2026-09-25 the same page listed €3,229.99 and €3,349.99 for the two 128GB variants | The [terms of service](https://de.gmktec.com/policies/terms-of-service) state Hong Kong law and Hong Kong courts; the footer names Shenzhen GMK Technology Co., Ltd. The store states EU warehouse fulfillment (Germany where available) and that VAT or import duties may apply for non-EU origin | 7-day return window; a 15% fee applies whether or not the item was opened; no return or refund after 15 days | The [warranty page](https://de.gmktec.com/pages/warranty) states 2 years and, elsewhere on the same page, one year; its exclusions list commercial use |
| [Beelink EU](https://eu.bee-link.com/products/beelink-gtr9-pro-amd-ryzen-ai-max-395), GTR9 Pro 128GB/2TB | €4,619 (unchanged since 2026-09-25; VAT inclusion not established) | The [terms of service](https://eu.bee-link.com/policies/terms-of-service) state that Hong Kong law governs; no legal entity is named beyond the "© 2026 Beelink, Inc." footer | Product page: 30-day "risk-free trial". [Warranty page](https://eu.bee-link.com/pages/warranty-policy): 30-day return for new-condition items, customs costs on returns to the warehouse paid by the customer, and a clause that high-value products cannot be returned; how these fit together is not resolved here | The warranty page states 3 years and says it applies only to personal use, not to products used for commercial purposes |
| [Minisforum EU](https://minisforumpc.eu/products/minisforum-ms-s1-max-mini-pc), MS-S1 MAX 128GB/2TB | €3,999 (4TB: €4,319; unchanged for 2TB since 2026-09-25; VAT inclusion not established) | Not captured in this review | 30-day money-back wording; the store publishes an [EU right-of-withdrawal page](https://minisforumpc.eu/pages/eu-right-of-withdrawal) | The [refund policy page](https://minisforumpc.eu/policies/refund-policy) states 24 months in one section and 36 months elsewhere; its exclusions list commercial or corporate bulk purchases (contact separately) and, in Article 4, items used for rental or commercial purposes |

According to the stores' own terms (checked 2026-09-30), the factory warranty of all three EU stores excludes commercial use, in different wording.

For consumers, [Your Europe](https://europa.eu/youreurope/citizens/consumers/shopping/guarantees/index_en.htm) states that the EU legal guarantee is at least 2 years against the seller and that a commercial guarantee cannot reduce it (page last checked by Your Europe on 2026-08-20). For the 14-day withdrawal right on online purchases see [Your Europe: returns](https://europa.eu/youreurope/citizens/consumers/shopping/returns/index_en.htm). Seller restocking and return terms are quoted as stated, not as legal advice. Beelink's main store bills the same GTR9 Pro configuration in USD ($4,349 above), so EU buyers can see two different official price points. The July EUR rows in the July CSV keep their own date.

### Route (b): local retailers in NL and DE

Prices are listings on the comparison sites on 2026-09-30. Geizhals states that its prices include VAT; Tweakers lists prices including VAT by default, which was not confirmed on each page.

| Site and country | System | Listing (EUR) | Notes |
|---|---|---|---|
| Tweakers Pricewatch, NL | [HP Z2 Mini G1a, 128GB (A40Q7ET)](https://tweakers.net/pricewatch/2223284/hp-z2-mini-g1a-a40q7et-qwerty-nl-toetsenbord.html) | €6,506.17 to €7,015 | 8 to 9 shops (the count changed between readings), mostly business resellers. A separate 128GB/2TB W11P listing starts at €5,687 (2 shops) |
| Tweakers Pricewatch, NL | [GMKtec EVO-X2](https://tweakers.net/pricewatch/2224254/gmktec-evo-x2-64gb-ram-1tb-ssd.html) | 64GB/1TB: €2,139 (Galaxus) to €2,548.01 (Proshop.nl). 128GB/2TB with Windows 11 Pro: €3,939 (3 shops) | The 128GB listing that Tweakers reviewed has no price |
| Tweakers Pricewatch, NL | Zotac ZBOX Magnus EAMAX395C, 128GB | €5,658.40 (3 shops) | SSD and OS not checked |
| Tweakers Pricewatch, NL | Framework Desktop, Beelink GTR9 Pro, Minisforum MS-S1 MAX, Bosgame M5, Corsair AI Workstation 300, any PRO 495 system | No prices, or no results | [Searches](https://tweakers.net/pricewatch/zoeken/?keyword=ryzen+ai+max%2B+395) on 2026-09-30 |
| Geizhals, DE/AT | [GMKtec EVO-X2 128GB/2TB](https://geizhals.de/gmktec-evo-x2-a3485299.html) | Five offers: €3,799.96 (GMKtec Direct via Amazon Marketplace), €3,999.96 (GMKtec-DE via Amazon), €4,119.60 (Proshop.de, +€5.99 shipping, 7 to 9 days), €4,205.59 (Galaxus, 5 to 7 working days), €5,112.99 (a Kaufland seller) | Includes VAT per Geizhals |
| Geizhals, DE/AT | [MSI PRO MAX EDGE AI+](https://geizhals.de/msi-msi-pro-max-edge-ai-00b4001s-001xat-a3947566.html), 128GB/2TB (00B4001S-001XAT) | €4,499 (5 offers) | Listed as immediately available; listed on Geizhals since 2026-09-18. Processor not checked here |
| Geizhals, DE/AT | [Acer Veriton RA110](https://geizhals.de/acer-veriton-ra110-ai-mini-workstation-v250970.html), 128GB/2TB (DT.R9QEG.002) | From €3,999 (3 offers) | Processor not checked here |
| Geizhals, DE/AT | [Zotac ZBOX Magnus EAMAX395C](https://geizhals.de/zotac-zbox-magnus-eamax-v225778.html), 128GB | From €5,199 (17 offers) | SSD and OS not checked |
| Geizhals, DE/AT | [Minisforum MS-S1 MAX 128GB/2TB](https://geizhals.de/?fs=minisforum+ms-s1+max&hloc=de); [Beelink GTR9 Pro 128GB/2TB](https://geizhals.de/?fs=beelink+gtr9+pro&hloc=de) | MS-S1 MAX: from €3,999 (3 offers). GTR9 Pro: €4,699 (1 offer) | Includes VAT per Geizhals |

Calculation: on the same Geizhals page, the two independent retailers (Proshop.de at €4,119.60 and Galaxus at €4,205.59) were €719.61 and €805.60 above the maker's EU store price of €3,399.99 for the EVO-X2 128GB/2TB (VAT treatment of the store price not established). A retailer places a local seller between you and the manufacturer; read the retailer's own return and warranty terms.

### Ordering notes

- Before paying, ask the seller from which country the parcel ships and whether import VAT or duties are included. Keep a screenshot of the stock and delivery text from the day of the order, and choose signature on delivery where the carrier offers it.

### What European reviews report (claims of third parties)

These measurements come from European publications, use their own models, quantizations and software stacks, and were not reproduced by this guide. Reader comments note that dense models were tested, while many of the guide's measured routes use MoE models; the guide has no matched cross-platform measurement and does not say these reviews are wrong.

- **Tweakers, 2026-03-12** ([review](https://tweakers.net/reviews/14328/nvidia-dgx-spark-asus-ascent-gx10-je-eigen-ai-supercomputer-op-je-bureau.html)): Framework Desktop against the ASUS Ascent GX10 (DGX Spark class) with `llama-bench`. As summarized from the review, the Framework's prompt processing was 3 to 5 times slower and its generation about 25 percent slower. Llama 3.3 70B Q8 stalled with dynamic VRAM allocation on the Framework and ran only with a fixed 64GB allocation; ComfyUI FLUX.2 took about 10 minutes per image against about 2 minutes, and the AMD driver crashed without a fixed VRAM setting. The guide's route uses a small fixed BIOS reserve plus GTT; whether the dynamic-allocation failure applies to that route was not tested here.
- **Tweakers, 2026-09-24** ([Mac mini M6 and Mac Studio M5 Ultra review](https://tweakers.net/reviews/15318/mac-mini-m6-en-mac-studio-m5-ultra-nieuwste-hardware-voor-vertrouwde-macs.html)): on Qwen3-Coder-Next 8-bit (about 80GB) the M5 Ultra was almost four times as fast as the Framework Desktop, and the Framework's time to first token fell far behind; the Mac mini M6 was slightly slower than the Framework and the Spark on Qwen3.5-9B. A reader comment notes that the quantization is not named.
- **c't 3003 via heise, 2025-11-14** ([article](https://www.heise.de/news/Duell-der-KI-Kisten-Nvidia-DGX-Spark-vs-AMD-Strix-Halo-11079206.html)): GPT-OSS 120B ran 11 percent faster on AMD than on the DGX Spark (LM Studio, Vulkan); a document of about 20k tokens took the DGX 14 seconds and the AMD system almost 4 minutes.
- **ComputerBase, 2025-12-03:** see the NIC note under [Price snapshot and trend](#price-snapshot-and-trend).

### Electricity cost with EU tariffs

The [README cost example](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#cost-local-vs-cloud) uses **assumed**, unmeasured 120 W active for one hour per day plus 30 W idle for 23 hours per day at $0.15/kWh ($3.65 over 30 days). Second scenario with European household tariffs: [Eurostat](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Electricity_price_statistics) (page checked 2026-09-30; data for the second half of 2025) gives about €0.2896/kWh for the EU average and about €0.3869/kWh for Germany. The consumption band and tax treatment are set out on the Eurostat page and were not transcribed here; the Netherlands value was not read.

| Scenario | Inputs | kWh per 30 days | At €0.2896 (EU average) | At €0.3869 (Germany) |
|---|---|---|---|---|
| A. Existing example, EU tariffs | 120 W × 1 h + 30 W × 23 h (assumed) | 24.3 | €7.04 | €9.40 |
| B. Same duty cycle, third-party idle | 120 W × 1 h (assumed) + 11.6 to 12.8 W × 23 h (Tweakers desktop idle, see below) | 11.6 to 12.4 | €3.36 to €3.60 | €4.49 to €4.81 |
| C. Continuous load | 140 W × 24 h (assumption inside the community-reported sustained-generation range of 137.4 to 173.6 W) | 100.8 (1,226 per year) | €29.19 (about €355 per year) | €39.00 (about €474 per year) |

Tweakers measured an idle draw of 11.6 W for the Framework Desktop and 12.8 W for the GMKtec EVO-X2 (claims of third parties; these are desktop idle and CPU-load measurements, not LLM inference, and use other software than the guide). The community wall-power rows in the [power baseline data](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/community_power.csv) show idle 28.89 to 38 W on Corsair AI Workstation 300 systems under Linux. The existing 30 W idle value remains an assumption; the guide has no wall-power measurement of its own Beelink. Scenario B is a calculation, not a measurement of any system under LLM load.

### GDPR and local AI

Running a model locally keeps prompts from being sent to a cloud processor, but GDPR (AVG, DSGVO) obligations for personal data remain: for example security of processing, access control and logging. This is not legal advice. See [Secure local AI](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/SECURE_LOCAL_AI.md) for exposure and sharing risks of a local server.

### Platform lifetime and firmware support

AMD announced the Ryzen AI Embedded X100 on Strix Halo silicon with "up to 10 years" of availability for 24/7 use ([ComputerBase](https://www.computerbase.de/news/prozessoren/ryzen-ai-embedded-x100-amds-embedded-sparte-geht-mit-strix-halo-all-in.98517/), 2026-07-24; ComputerBase states that AMD paid its travel and hotel). First partner systems are COM modules. This is a vendor statement about chip availability; it says nothing about how long a mini-PC maker supplies BIOS or driver updates. Check the public BIOS history of the exact system (see [BIOS update route](#bios-update-route-checked-2026-09-30)).

## Ryzen AI Max PRO 400 and other Strix Halo-class hardware (not measured here)

Everything in this section is dated hardware context. None of these systems or processors has first-party or community evidence in this guide, and none inherits the MAX+ 395 / 128GB results above. Specifications and prices are vendor statements or store listings, not measurements.

### Ryzen AI Max PRO 400 systems (checked 2026-09-30)

AMD [announced the Ryzen AI Max PRO 400 Series](https://www.amd.com/en/blogs/2026/amd-powers-next-generation-agent-computers-with-new-ryzen-ai-hal.html) on 2026-05-20 (reported under the codename Gorgon Halo). AMD lists the [Ryzen AI Max+ PRO 495](https://www.amd.com/en/products/processors/laptop/ryzen-pro/ai-max-pro-400-series/amd-ryzen-ai-max-plus-pro-495.html) with 16 cores, Radeon 8065S graphics with 40 CUs and up to 192GB LPDDR5x-8533; the [PRO 490](https://www.amd.com/en/products/processors/laptop/ryzen-pro/ai-max-pro-400-series/amd-ryzen-ai-max-pro-490.html) and [PRO 485](https://www.amd.com/en/products/processors/laptop/ryzen-pro/ai-max-pro-400-series/amd-ryzen-ai-max-pro-485.html) use Radeon 8050S graphics with 32 CUs. A later "Medusa Halo" (Ryzen AI Max 500) is rumored only and not confirmed by AMD ([VideoCardz report](https://videocardz.com/newz/amd-ryzen-max-500-medusa-halo-rumored-to-support-lpddr6-memory)).

The first PRO 495 systems opened for order between 2026-09-28 and 2026-09-30. The guide has not measured any of them, and a 192GB memory setup is not qualified here. Systems in alphabetical order, not a ranking:

| System | Configuration | Price and price kind | Country, currency, tax | Orderable | Ships | Source |
|---|---|---|---|---|---|---|
| Acemagic F9A PRO 495 (mini PC) | 192GB/2TB | $6,499, store listing | US store, USD, tax not stated | Pre-order | "Late October" (store estimate) | [store page](https://acemagic.com/products/f9a-495-ai-workstation) |
| AMD Ryzen AI Halo, PRO 495 version (reference platform) | 192GB memory support | None published | n/a | No ("Coming Soon" on AMD's page) | Not stated | [AMD](https://www.amd.com/en/products/processors/desktops/ryzen/ryzen-ai-halo.html) |
| Beelink GTR9 Pro with PRO 495 (mini PC) | Up to 128GB | CNY 29,998, reported from a China retail listing (secondary report) | China, CNY, tax not stated | China only; a search for "495" on Beelink's global store showed only the 395 model (2026-09-30) | Not stated | [Notebookcheck, 2026-09-29](https://www.notebookcheck.net/GTR9-Pro-495-Beelink-releases-new-mini-PC-with-10-GbE-and-128-GB-RAM.1411104.0.html), [Beelink search](https://www.bee-link.com/search?q=495) |
| Bosgame M5 MAX (mini PC) | 128GB and 192GB planned | No store price. A press release dated 2026-09-08 gave $3,600 to $3,800 for 128GB/2TB | US, USD, press release | No | Blog (2026-09-02): 128GB in November 2026, 192GB in early 2027. The press release named late September to mid-October (not reconciled) | [Bosgame blog](https://www.bosgamepc.com/blogs/coming-soon/new-product-launch--bosgame-m5-max-with-amd-ryzen-ai-max-pro-495-processor), [press release](https://www.digitaljournal.com/pr/news/access-newswire/bosgame-previews-its-flagship-m5-1140623009.html) |
| Framework Desktop, PRO 495 (NL store) | DIY Edition 192GB (no storage or OS), or pre-built 192GB/2TB with Fedora 44 | DIY €7,659; pre-built €8,379 (list prices) | NL store, EUR, VAT included (store tooltip) | Pre-order, "Limited Batch 1"; the store says a pre-order can be cancelled before shipment for a full refund | November (store) | [DIY](https://frame.work/nl/en/products/desktop-diy-amd-aimax400/configuration/new), [pre-built](https://frame.work/nl/en/products/desktop-amd-aimax400/configuration/new) |
| Framework Desktop, PRO 495 (US) | DIY Edition 192GB; pre-built | DIY from $6,799 (Framework on X); pre-built $7,449 (Phoronix, secondary source) | US, USD, tax not stated | Pre-order, one batch per Framework | November (Framework) | [Framework on X](https://x.com/FrameworkPuter/status/2105326903225925740), [Phoronix](https://www.phoronix.com/news/Framework-Desktop-Gorgon-Halo) |
| GMKtec EVO-X5 Pro (EU store) | 192GB/2TB (4TB: €6,899 list) | List €6,599; code X5EARLY €6,399 until 2026-10-06 23:59 CEST. Tweakers (2026-09-28) reports a ladder of €6,249 (first 30 customers), €6,399 (early bird, up to 7 days) and €6,599 (regular); 4TB €6,499, €6,699 and €6,899 | EU store, EUR, "DDP basis" stated, VAT inclusion not established | Listed for sale; 7-day return window stated | First batch dispatch expected at the end of October 2026 (seller) | [EU store](https://de.gmktec.com/en/products/gmktec-evo-x5-pro-ai-max-495), [Tweakers](https://tweakers.net/nieuws/252696/gmktec-en-minisforum-brengen-pcs-met-ryzen-ai-max+-495-vanaf-6249-en-7799-euro.html) |
| GMKtec EVO-X5 Pro (US store) | 192GB/2TB (4TB: $6,899) | Early-bird $6,599; regular $6,799. Vendor video (2026-09-28): first 30 units $6,399, promotion until 2026-10-05 | US store, USD, tax not stated | Orderable ("In Stock" label, no ETA on the page) | Not stated on the US page | [US store](https://www.gmktec.com/products/gmktec-evo-x5-pro-amd-ryzen-ai-max-pro-495-ai-mini-pc), [video](https://www.youtube.com/watch?v=iPtQO2GIL2c) |
| HP ZBook Ultra G3a (laptop) | PRO 495, up to 192GB; Windows 11 Pro or Ubuntu 26.04 LTS per HP's page | No HP store price. HP's Local AI Value Calculator uses $7,449 for a 192GB/512GB reference configuration as an editable input (an HP assumption, not a store price). B&H pre-order listings: 64GB/1TB $6,148.95; 128GB/2TB OLED $9,548.95 | US, USD; the calculator excludes sales tax; B&H tax not stated | HP: no. B&H: pre-order listings ("Coming Soon", no shipping to the Netherlands) | HP: expected October 2026, pricing closer to availability | [HP release](https://www.hp.com/us-en/newsroom/press-releases/2026/hp-redefines-the-mobile-workstation-for-the-era-of-agentic-ai.html), [HP page](https://www.hp.com/us-en/workstations/mobile-workstation-pc/zbook-ultra-g3.html), [calculator](https://www.hp.com/us-en/workstations/mobile-workstation-pc/zbook-ultra-g3-roi-calculator.html), [B&H 64GB](https://www.bhphotovideo.com/c/product/2003096-REG/hp_e77zlut_aba_16_zbook_ultra_g3a.html), [B&H 128GB](https://www.bhphotovideo.com/c/product/2003097-REG/hp_e77zmut_aba_16_zbook_ultra_g3a.html) |
| Lenovo ThinkCentre X Ultra | Up to 128GB (up to 96GB dedicated graphics memory per Lenovo) | "Expected starting price" 3100€ (press release; configuration not stated; a footnote says prices may not include taxes) | EUR; tax status unclear | No | Available starting November 2026 | [Lenovo](https://news.lenovo.com/pressroom/press-releases/hybrid-ai-for-business-devices-displays-solutions/) |
| Minisforum MS-S1 MAX-P495 (US store) | 192GB/2TB | $7,399 (compare-at $9,249) | US store, USD, tax not stated | Orderable (vendor post of 2026-09-28: "now available to order"); first batch limited to 100 units worldwide per the vendor's video | "Mid October" (store estimate) | [US store](https://store.minisforum.com/products/minisforum-ms-s1-max-p495-ai-workstation), [post](https://x.com/Hi_MINISFORUM/status/2104427342169039069), [video](https://www.youtube.com/watch?v=urFeX5GJI3Y) |
| Minisforum MS-S1 MAX-P495 (EU store) | 192GB/2TB | €7,799 sale price (regular €9,749) | EU store, EUR, VAT inclusion not established | Orderable; 30-day money-back wording | "Mid October" (store estimate) | [EU store](https://minisforumpc.eu/products/minisforum-ms-s1-max-p495) |
| SIXUNITED AXN88B-160M-YD (laptop, ODM) | PRO 495, 192GB LPDDR5X-8533, 16-inch, 120W | "Expected" about $10,000 (TechRadar, 2026-09-15); not a store price | US, USD | No | Not stated | [TechRadar](https://www.techradar.com/pro/chinese-vendor-debuts-worlds-first-amd-ryzen-ai-max-pro-495-laptop-but-192gb-lpddr5x-8533-for-gaming-really) |

- Price kinds differ: list, early-bird, batch, pre-order listing, calculator assumption and press-release range cannot be compared directly. GMKtec's temporary offers end on 2026-10-05 (US) and 2026-10-06 (EU); nothing was re-checked after 2026-09-30.
- The "In Stock" label on GMKtec's US page applies to the US store. On the EU store the first dispatch is expected at the end of October.
- Framework states that the 192GB Desktop is designed for Linux and has no Windows option; the pre-built version ships with Fedora ([launch post](https://community.frame.work/t/192gb-framework-desktop-open-for-pre-order/85192), 2026-09-30). It also lists an open-ended PCIe x4 slot on this configuration (vendor specification, not tested here).
- "PRO 495" does not automatically mean 192GB: Beelink's PRO 495 listing reported from China and Lenovo's X Ultra top out at 128GB. Memory speed, VRAM allocation, NPU status and the one-versus-two-box question are covered in [128GB or 192GB?](#128gb-or-192gb).

**AMD Ryzen AI Halo.** This is an AMD reference/developer platform, not a retail OEM mini PC. AMD's [2026-07-06 post](https://www.amd.com/en/blogs/2026/amd-ryzen-ai-halo-now-available-at-micro-center.html) says it is now available at Micro Center and calls Micro Center its "first global launch partner". A footnote (SHO-61) on AMD's [Ryzen AI Halo product page](https://www.amd.com/en/products/processors/desktops/ryzen/ryzen-ai-halo.html) (checked 2026-09-30) states a retail price of $3,999 for the Ryzen AI Halo (USD; testing as of May 2026; tested with a Ryzen AI Max+ 395 and 128GB). That is a price AMD states in a performance footnote, not an observed store price: the Micro Center page returned an access error when checked, so no store price was read. There is no first-party measurement of the Ryzen AI Halo; see the [Ryzen AI Halo context](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/RYZEN_AI_HALO_CONTEXT.md) for how reference-platform material stays separate from retail evidence.

**Other 2026 SKUs.** AMD's [CES 2026 announcement](https://ir.amd.com/news-events/press-releases/detail/1270/amd-expands-ai-leadership-across-client-graphics-and-software-with-new-ryzen-ryzen-ai-and-amd-rocm-announcements-at-ces-2026) (2026-01-05) added the Ryzen AI Max+ 392 (12 cores) and Max+ 388 (8 cores), both with the full 40-CU Radeon 8060S graphics. The PRO 490/485 above have 32-CU Radeon 8050S graphics. None of these SKUs is measured here; the MAX+ 395 results on this page do not qualify them. Check the exact processor on any listing.

### Laptops, handhelds and Linux with vendor support (not measured here)

- **A different class.** Laptops and handhelds with the Ryzen AI Max+ 388 or 392 (for example a Lenovo Legion 7a Gen 11 and a GPD Win Max 3, both with the 388, per video reviews of [2026-08-27](https://www.youtube.com/watch?v=4MtfhZdUajU) and [2026-09-07](https://www.youtube.com/watch?v=18h8V346-bA)) are not the MAX+ 395 / 128GB systems measured here. Check the CPU (388 and 392 are not 395) and the exact memory SKU: 32GB and 64GB variants fall under the 64GB guidance above, while 395 laptops with 128GB exist (for example the HP ZBook Ultra G1a in the README hardware table).
- **Power limits.** Laptop power profiles cap sustained performance. Examples reported by third parties: ASUS ProArt PX13 profiles from 50/40 W (Silent) to 85/70 W (Performance), and 60/55 W on battery ([Notebookcheck](https://www.notebookcheck.net/AMD-Strix-Halo-128-GB-RAM-in-a-13-inch-convertible-Asus-ProArt-PX13-GoPro-Edition-Review.1232755.0.html), 2026-02-25); HP ZBook Ultra G1a sustaining 55 W ([StorageReview](https://www.storagereview.com/review/hp-zbook-ultra-g3a-16-preview-192gb-of-unified-memory-aims-for-the-top-of-the-local-ai-laptop-leaderboard), 2026-09-15). The only LLM-versus-power-limit table found ([strixhalo.wiki](https://strixhalo.wiki/Guides/Power_Modes_and_Performance/), claim of a third party) was measured with a mini PC's power modes (GPU passed through to a Windows VM), so it is an extrapolation for laptops: Gemma 3 27B prompt processing 77/89/95 t/s at 55/85/120 W while generation stayed at 6 t/s. The guide has no laptop measurements.
- **Network exposure.** Do not bind Ollama or Open WebUI to all interfaces on a laptop that joins untrusted networks; see [Secure local AI](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/SECURE_LOCAL_AI.md).
- **Linux with vendor support.** Ubuntu's [certification search](https://ubuntu.com/certified?q=Ryzen+AI+Max&limit=50) for "Ryzen AI Max" (2026-09-30) listed the HP Z2 Mini G1a, the HP ZBook Ultra G1a and the Lenovo Yoga Pro 7 15ASH11 (Max+ 388); no Beelink, GMKtec, Minisforum or Bosgame mini PC appeared. HP's page lists Ubuntu 26.04 LTS for the ZBook Ultra G3a, and Lenovo's press release lists Linux Ubuntu (certification only) and Linux AMD AI OS for the X Ultra. A certificate records the kernel at certification time ([certificate 202411-36044](https://ubuntu.com/certified/202411-36044): Ubuntu 24.04 LTS, kernel 6.11.0-1015-oem); which kernel an installed vendor image runs is not established here. Compare `uname -r` with the kernel of the guide's measured route (see the [setup page](https://strixhaloguide.com/amd-strix-halo-setup/)) before following its benchmarks.

### Other Strix Halo systems: hardware context only

These systems exist but have no community or first-party evidence in this guide: hardware context, not evidence. Prices are exact-SKU storefront or price-comparison observations with country and currency per row (checked 2026-09-25 or 2026-09-30 as shown), not current offers. Listing order is alphabetical, not a ranking.

| System | Processor and configuration | Dated observation |
|---|---|---|
| [Acemagic M1A PRO+](https://acemagic.com/products/m1a-395) | MAX+ 395, 128GB/2TB | US, USD: $3,099 on acemagic.com (2026-09-25; $3,099 and available on 2026-09-30) |
| [Acer Veriton RA110](https://geizhals.de/acer-veriton-ra110-ai-mini-workstation-v250970.html) | 128GB/2TB (DT.R9QEG.002); processor not checked here | DE (Geizhals, EUR, includes VAT): from €3,999, 3 offers (2026-09-30) |
| Bosgame M5 (two stores) | MAX+ 395, 128GB/2TB | US, USD: $3,099 on [bosgame.com](https://www.bosgame.com/products/bosgame-m5-ai-mini-desktop-ryzen-ai-max-395-96gb-128gb-2tb) (2026-09-30); $2,999 on [bosgamepc.com](https://www.bosgamepc.com/products/bosgame-m5-ai-mini-desktop-ryzen-ai-max-395) (2026-09-19, not re-checked) |
| [GEEKOM A9 Mega](https://www.geekompc.com/geekom-a9-mega-ai-mini-pc/) | MAX+ 395 or MAX+ 388 per vendor page | price not captured |
| [HP Z2 Mini G1a](https://www.cdw.com/product/hp-z2-mini-g1a-workstation-1-x-amd-ryzen-ai-max-pro-395-128-gb-2-tb/8440785) | Ryzen AI Max PRO 395, 128GB/2TB (C3XE1UT#ABA) | US, USD: $7,707.99 at CDW, which also shows "sign in for your price" (2026-09-25). NL: see [Route (b)](#route-b-local-retailers-in-nl-and-de) |
| [Minisforum MS-S1 MAX 64GB](https://store.minisforum.com/products/minisforum-ms-s1-max-64gb) | MAX+ 395, 64GB/2TB (MS-S1-MAX62US) | US, USD: $2,599 (compare-at $3,249) on 2026-09-25; $2,599 listed on 2026-09-30 |
| [Minisforum N5 MAX AI NAS](https://store.minisforum.com/products/minisforum-n5-max-ai-nas) | MAX+ 395 in a NAS form factor, 64GB or 128GB | US, USD: $2,399 (64GB) and $3,599 (128GB), both listed as available (2026-09-30). The store text says MinisCloud OS is preinstalled with a local AI agent (MinisOpenClaw) running Qwen3.6-35B by default and per-account Docker isolation (vendor claims, not examined here). A community [review](https://forum.level1techs.com/t/nas-review-notes-minisforum-n5-max-amd-strix-halo/251183) (tested 2026-05-27, Proxmox 9.1.1) recorded about 2GiB fixed VRAM plus about 28GiB GTT on the 64GB model, which matches the default Linux GTT limit rather than a NAS-specific setting. The guide's recorded GTT values are for 128GB systems, not 64GB |
| [MSI PRO MAX EDGE AI+](https://geizhals.de/msi-msi-pro-max-edge-ai-00b4001s-001xat-a3947566.html) | 128GB/2TB (00B4001S-001XAT); processor not checked here | DE (Geizhals, EUR, includes VAT): €4,499, 5 offers (2026-09-30) |
| [ONEXStation](https://onexplayerstore.com/products/onexstation-mini-ai-workstation-ryzen%e2%84%a2-ai-max-395-up-to-128gb-ram-ai-mini-pc) | MAX+ 395, 128GB/1TB or 128GB/2TB | US, USD: $3,199 (1TB); $3,499 (2TB, compare-at $3,599) on 2026-09-25. The launch price reported in April 2026 was lower; this row uses the observed store price |
| [Zotac ZBOX Magnus EAMAX395C](https://geizhals.de/zotac-zbox-magnus-eamax-v225778.html) | 128GB (model code EAMAX395C); SSD, OS and processor not checked here | DE (Geizhals, EUR, includes VAT): from €5,199, 17 offers; NL (Tweakers Pricewatch): €5,658.40, 3 shops (2026-09-30) |

A community-maintained hardware list ([strixhalo.wiki](https://strixhalo.wiki/Hardware/PCs), read 2026-09-30) names further Strix Halo systems, including the Aoostar NEX395, FEVM FA-EX9, MSI AI Edge, Minix Elite ER939-AI, Morefine H1 and Abee AI Station. This is hardware context, not evidence; the guide has not checked those listings.

## Buy now or wait?

Buy when a currently available configuration supports a task you need now at an acceptable delivered price. Waiting can be sensible when your current machine is adequate, the price exceeds your budget, or your workload needs more capacity than the tested system offers. Future prices and performance are uncertain.

**State of the market (checked 2026-09-30).**

- **192GB systems are starting to open for order.** The first Ryzen AI Max+ PRO 495 systems with 192GB were listed between 2026-09-28 and 2026-09-30, with shipping from mid-October (Minisforum) to November (Framework); see the [PRO 400 table](#ryzen-ai-max-pro-400-systems-checked-2026-09-30). The early prices are early-bird, batch or pre-order prices, and some promotions end on 2026-10-05 or 2026-10-06. None of these systems is measured here.
- **Stock can run out.** On 2026-09-30 (about 18:13 UTC) all three 300-series Framework Desktop DIY variants (32, 64 and 128GB) showed as out of stock in the NL store. Framework's launch post states that it expects memory prices to keep rising over the next six months (vendor statement; this guide does not forecast prices).
- **The NPU of the PRO 495 on Linux.** See [128GB or 192GB?](#128gb-or-192gb): driver support is targeted at Linux 7.4, which is not released yet.
- **Software support is still arriving.** A Lemonade issue ([#3662](https://github.com/lemonade-sdk/lemonade/issues/3662), opened 2026-09-23 and still open when checked on 2026-09-30) reports that Lemonade's ROCm backend calls the GPU of a PRO 495 unsupported (Windows), while native llama.cpp ROCm works according to the issue title.
- **Platform lifetime and firmware support differ.** See [Platform lifetime and firmware support](#platform-lifetime-and-firmware-support): AMD's embedded availability statement concerns the chip, while BIOS updates depend on each OEM.
- **Laptops and handhelds with the 388 or 392 are a different class.** See [Laptops, handhelds and Linux with vendor support](#laptops-handhelds-and-linux-with-vendor-support-not-measured-here).
- **Preinstalled "local AI" editions exist.** See the FAQ below on keeping a factory image.

Published larger-memory options belong in a capacity comparison; they do not inherit the guide's 128GB speed or feature results. Check the exact processor, memory and shipping configuration on the [official Framework Desktop page](https://frame.work/desktop) and other vendor listings. Do not infer the specification of a new GMKtec model from its EVO-X generation number alone.

If your chosen artifact fits in a discrete GPU's VRAM, also compare an existing or used GPU system and Apple silicon against your actual workload. Include the complete host cost, software requirements, power and noise; this guide does not establish a universal price/performance winner across those platforms.

**Other 128GB-class platforms (dated context, no ranking).** US prices are in USD and checked 2026-09-30 unless noted; US tax is not stated.

- **NVIDIA and partners.** NVIDIA raised the DGX Spark Founders Edition MSRP to $4,699 in its [price-change announcement](https://forums.developer.nvidia.com/t/2-23-2026-price-change-announcement/361713) posted 2026-02-25 (AMD's Ryzen AI Halo footnote also uses $4,699). On the [NVIDIA Marketplace](https://marketplace.nvidia.com/en-us/enterprise/personal-ai-supercomputers/) the Founders Edition showed as out of stock without a price, and the ASUS Ascent GX10 was $5,999 (1TB) and $7,999 (4TB). The ASUS eShop US listed the GB10-based [Ascent GX10](https://eshop.asus.com/us/ascent-gx10.html) with the default 2TB configuration at $6,999.00 and states that all sales are final, with no returns once an order is processed. A [thread on NVIDIA's developer forum](https://forums.developer.nvidia.com/t/september-2026-availability-of-gb10s/382068) (September 2026) reports tight GB10 supply and higher prices (community reports, not store observations). NVIDIA's RTX Spark Windows systems were [announced](https://nvidianews.nvidia.com/news/nvidia-microsoft-windows-pcs-agents-rtx-spark) for "this fall"; no price or shipping date was read.
- **Apple.** Apple [announced](https://www.apple.com/newsroom/2026/08/apple-introduces-new-mac-studio-with-m5-max-and-m5-ultra/) the Mac Studio with M5 Max and M5 Ultra on 2026-08-25, [available from 2026-09-22](https://www.apple.com/newsroom/2026/09/the-new-mac-mini-and-mac-studio-are-available-today/). The US [Apple Store](https://www.apple.com/shop/buy-mac/mac-studio) listed M5 Max with 36GB memory and 512GB storage at $2,499, M5 Max with 64GB/1TB at $3,099, M5 Ultra with 96GB/1TB at $5,499 and an M5 Ultra configuration from $6,799. The 128GB M5 Max price was not captured, and the 512GB M5 Ultra memory option was listed as coming late October.
- **Germany (Geizhals, EUR, includes VAT).** ASUS Ascent GX10 1TB from €4,999 (26 offers), DGX Spark Founders Edition 4TB from €5,799, Gigabyte AI TOP ATOM 4TB from €5,499, Lenovo ThinkStation PGX 1TB from €4,999.99 and Mac Studio M5 Max 36GB/512GB from €2,727.10 (taken from the sidebar of the [MSI listing](https://geizhals.de/msi-msi-pro-max-edge-ai-00b4001s-001xat-a3947566.html): observed on that page on 2026-09-30, not reproducible by URL).
- **Netherlands (Tweakers Pricewatch, EUR, VAT status not confirmed per page).** ASUS Ascent GX10 (GX10-GG0003BN) from €5,299; DGX Spark Founders Edition €6,143.06 on a first reading and €6,199 on a later reading the same day; Mac Studio M5 Ultra from €6,629 (per the Tweakers [review](https://tweakers.net/reviews/15318/mac-mini-m6-en-mac-studio-m5-ultra-nieuwste-hardware-voor-vertrouwde-macs.html) page).
- Independent European measurements of some of these platforms are summarized under [What European reviews report](#what-european-reviews-report-claims-of-third-parties). The guide has no matched measurement on any of these platforms and does not rank them against Strix Halo; the [cost of local vs cloud](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#cost-local-vs-cloud) section covers the separate cloud question.

## Daily use: power, thermals, noise

There is no first-party Beelink wall-power or noise measurement in this guide. What exists is scoped:

- [Power baseline](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/POWER_BASELINE.md): community-reported whole-system wall power from Corsair AI Workstation 300 systems, kept separate from the Beelink's amdgpu `PPT` telemetry. PPT is not wall power, and neither is a Beelink efficiency claim.
- [Thermal stability](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/THERMAL_STABILITY.md): community sustained-load thermal and clock evidence from three Corsair / Sixunited systems in one fleet; not a general recommendation for other chassis.
- [Nimo community notes](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/COMMUNITY_NIMO.md): contributor-reported fan noise (peak around 46 dBA) and power/temperature values with incomplete instrument and sampling metadata. They do not qualify noise or wall-power comparisons between systems.
- **European press measurements (claims of third parties; desktop idle and CPU load, not LLM inference).** Tweakers measured the Framework Desktop ([review](https://tweakers.net/reviews/13614/framework-desktop-de-framework-die-je-niet-koopt-voor-de-upgrades.html), 2025-08-07) at 11.6 W idle, 187 W under a multi-core Cinebench load and 0.4 W off, and the GMKtec EVO-X2 ([review](https://tweakers.net/reviews/13438/gmktec-evo-x2-met-amd-ryzen-ai-max+-395-mini-pc-met-megahardware.html), 2025-07-08) at 12.8 W idle, 189 W load and 0.6 W off, with 26 dB (browser), 37 dB (PCMark) and 42 to 44 dB (gaming and Blender) at 0.5 m. A [heise test](https://www.heise.de/bestenlisten/testbericht/minisforum-ms-s1-max-mit-ryzen-ai-max-395-einer-der-staerksten-mini-pcs-im-test/6n5m46y) of the Minisforum MS-S1 MAX reports 5 to 7 W idle, 210 W maximum and more than 50 dB(A) under maximum load (read as a summary). These units, operating systems and workloads differ from the community wall-power rows above, so none of these is a measurement of the guide's Beelink under LLM load. For electricity cost with EU tariffs see [Buying in Europe](#electricity-cost-with-eu-tariffs).

Vendor noise or TDP figures on product pages are marketing statements, not measurements.

## How to compare the systems

The repository [Buying Guide](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#buying-guide) describes evidence depth per system. Beelink has the deepest first-party evidence here, not proof of intrinsically superior hardware. GMKtec and Corsair have attributed community evidence; Bosgame needs same-configuration buyer-path reproduction before a comparative performance claim. Framework's modular design is a selection consideration, not measured support superiority. Minisforum's networking may matter to a cluster buyer, but the exact network/runtime combination still needs qualification. None is a universal value winner on these unmatched results and dated offers.

For workflow fit, see the [buyer use cases](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BUYER_USE_CASES.md) and the [Windows vs Linux](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#windows-vs-linux) evidence table.

The comparison considers memory configuration, dated price/availability, evidence depth,
cooling/thermals, firmware/support, ports, expandability, workload fit, seller and
warranty terms (including commercial use) and the BIOS update route.
Affiliate commission is not a ranking input. If affiliate links are introduced,
each will be labeled near the link and entered in the public
[`affiliate link registry`](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/affiliate_link_registry.csv).

### BIOS update route (checked 2026-09-30)

AMD's security bulletins tie firmware fixes to AMD firmware (PI) versions that each OEM has to include in a BIOS update, and direct customers to their OEM for that update (for example [AMD-SB-4017](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-4017.html)). See the firmware section of [Secure local AI](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/SECURE_LOCAL_AI.md) for how to find your BIOS version. A search without a result does not prove that a vendor has no update channel; it means no LVFS listing was found with those search terms on 2026-09-30.

| Vendor | LVFS (fwupd) listing found | Public BIOS files | Notes |
|---|---|---|---|
| Framework | Yes, Framework Desktop | [BIOS 3.06](https://resources.frame.work/downloads/desktop/amd-ryzen-ai-max-300/3.06/) (2026-08-03) for the Ryzen AI Max 300 Desktop | Framework's release page states AMD PI 1.0.0.2c and publication to LVFS |
| HP | Yes, Z2 Mini G1a and ZBook Ultra G1a | Via LVFS | |
| Beelink | No | Public [download directory](https://dr.bee-link.cn/?dir=uploads%2FGTR%2FGTR9-395%2FBIOS) (read 2026-09-30) with dated folders: P108 (2025-09-16), P110 (2025-12-24), GTRPR05 (2026-04-01), GTRPR07 (2026-04-16), GTRPRPI1001C (2026-05-26, described as a secure boot update of AMD AGESA), GTRP112 (2026-06-10, described as a fix for an RDSEED issue), P110test (2026-07-31, described as a fix for an E610 LAN issue; a test BIOS) | Which BIOS belongs to which board revision is not stated in the listing as read; the Q1 2026 summary assigns GTRPR05 and GTRPR07 as in the board/NIC note and names no AMD PI version or CVE; a Q2 summary page returned "not found" |
| GMKtec | No | The EU [download center](https://de.gmktec.com/en/pages/download-center) lists drivers and OS images for the EVO X2, no BIOS file | |
| Minisforum, Bosgame, ASUS ROG Flow Z13 | No | Not checked | |

## FAQ

**Is a Strix Halo mini PC worth it for local LLMs?**
It can be useful when a measured model needs more memory than your existing GPU provides and its latency is acceptable. Start with a qualified model/runtime route and compare the delivered system cost with alternatives.

**Which Strix Halo mini PC is fastest for LLMs?**
The cross-OEM rows above use different campaigns and include build/flag differences. They support portability, but do not establish a controlled OEM speed ranking.

**Do I need 128GB of RAM?**
Choose from the exact artifact, context and concurrency requirement. Smaller Q4 MoE artifacts may fit in 64GB with sufficient headroom, but a third-party review of one 64GB chassis reports that the GPU sees only about 30 GiB by default and that the memory is soldered (see the 64GB checks above; not tested here). The guide's larger capacity results were measured on 128GB; nominal parameter count alone is not a memory requirement.

**Is 192GB worth the extra money?**
The guide has no 192GB measurement. On 2026-09-30 the 192GB configuration was listed €3,770 (Framework, NL store), $3,350 (Framework, US), $3,149 (GMKtec, regular price) and $3,600 (Minisforum) above the 128GB configuration of the same vendor (calculations; the GMKtec and Minisforum pairs are different models), and if your artifact fits in 128GB there is no measured speed gain here. See [128GB or 192GB?](#128gb-or-192gb), including the comparison with two 128GB systems.

**Should I wait for the next generation?**
Wait if a currently available configuration cannot meet your task or budget. As of 2026-09-30, the first Ryzen AI Max PRO 400 systems with 192GB were open for order with shipping from mid-October to November, and they are not measured here (see the [PRO 400 table](#ryzen-ai-max-pro-400-systems-checked-2026-09-30)). Check confirmed product specifications and shipping dates; more advertised memory does not by itself prove faster inference, and future prices are uncertain.

**Can I buy in the Netherlands or Germany from a local store?**
Some systems are listed by local retailers on Tweakers Pricewatch and Geizhals, at prices that differ from the maker's EU store; most mini PCs in this guide had no listing with prices on Tweakers Pricewatch on 2026-09-30. See [Buying in Europe](#buying-in-europe-checked-2026-09-30).

**Does the factory warranty cover business use?**
According to the terms of the GMKtec, Beelink and Minisforum EU stores (checked 2026-09-30), the factory warranty excludes commercial use, in different wording. Read the exact terms on each store's warranty page.

**Is running locally GDPR-compliant?**
Running a model locally keeps prompts from being sent to a cloud processor, but GDPR obligations for personal data remain (security, access control, logging). This is not legal advice; see [Secure local AI](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/SECURE_LOCAL_AI.md).

**Can I add a GPU to a Strix Halo mini PC?**
This guide has not measured an added GPU. Community reports (claims of third parties, 2025 to 2026): a [Level1Techs thread](https://forum.level1techs.com/t/franken-strix-halo-2x-r9700s-128gb-strix-halo-unified-memory/254736) reports prompt processing up to 2.2 times faster with two R9700 cards on an external PCIe switch, with the integrated GPU adding capacity but not generation speed, after three kernel parameters were changed; a USB4 eGPU repeatedly froze a Bosgame M5 while an M.2-to-OCuLink link worked, and a GMKtec EVO-X3 stopped booting after a BIOS change for OCuLink (both in [another thread](https://forum.level1techs.com/t/gmktec-evo-x3-ai-workstation-lemonade-benchmarks-and-specs/253262)); [strixhalo.wiki](https://strixhalo.wiki/Guides/External_GPU/) says the Sixunited board used by many boxes has no OCuLink, that an M.2-to-OCuLink adapter uses an NVMe slot (PCIe Gen4 x4), and that with AMD eGPUs the GPU power is tied to the APU limit set in the BIOS (two community reports from 2025). A community thread on the Framework x4 slot reports an unstable OCuLink attempt on Gen3 ([thread](https://community.frame.work/t/what-external-gpus-work-reliably-in-the-x4-slot/82939)). By vendor specification (not tested): the Framework 192GB configuration has an open-ended PCIe x4 slot that takes x8 and x16 cards, and the Minisforum MS-S1 MAX-P495 has a physical x16 slot running at PCIe 4.0 x4 ([Minisforum video](https://www.youtube.com/watch?v=urFeX5GJI3Y)). Send data through a benchmark report issue if you test it.

**Can I keep the preinstalled software image?**
The guide's measured route is a clean Ubuntu 24.04 install; it has not examined any vendor image. Vendors now sell preinstalled "local AI" editions: for example Beelink's [GTR9 Pro "OpenClaw & Local LLM Pre-installed"](https://www.bee-link.com/products/beelink-gtr9-pro-amd-ryzen-ai-max-395-processor-openclaw) at $4,349 for the Ubuntu edition (US, USD, checked 2026-09-30; the Ubuntu plus Windows edition at $4,499 was not orderable that day) and Minisforum's EU [MS-S1 MAX 64GB Local AI Pilot Edition](https://minisforumpc.eu/products/minisforum-ms-s1-max-64gb-local-ai-pilot-edition) at €2,679 (compare-at €3,449; VAT inclusion not established). The Beelink product page checked does not list software versions. Ask the seller for the software manifest and what listens on the LAN, and check it yourself (see [Secure local AI](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/SECURE_LOCAL_AI.md)). This guide makes no judgment about vendor images.

**Are these prices current?**
Every snapshot has its own date. Verify the exact region, RAM/SSD configuration, tax, shipping and stock on the vendor's current page. The historical price table is not a live quotation.


---

Community corrections are welcome — open an issue in the [repository](https://github.com/hogeheer499-commits/strix-halo-guide/issues). Pricing rows are dated snapshots, not live quotes. This page contains no affiliate links as of September 19, 2026 (links added on October 1, 2026 were checked by URL pattern for tracking parameters and affiliate-network domains and none was found); if that changes, links will be disclosed next to the relevant product and per [`VENDOR_DISCLOSURE.md`](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/VENDOR_DISCLOSURE.md).
