---
layout: default
title: "Best Strix Halo Mini PC for Local LLMs (2026): Beelink vs Framework vs GMKtec vs Corsair"
description: "Evidence-based comparison of AMD Ryzen AI MAX+ 395 mini PCs for local LLMs: measured cross-OEM benchmarks, 64GB vs 128GB fit guidance, dated prices, and buy-now-or-wait timing."
permalink: /best-strix-halo-mini-pc/
date: "2026-08-21T00:00:00+02:00"
last_modified_at: "2026-08-21T00:00:00+02:00"
image:
  path: "https://hogeheer499-commits.github.io/strix-halo-guide/assets/social-preview.png"
  height: 640
  width: 1280
  alt: "AMD Strix Halo mini PC comparison for local LLMs with measured cross-OEM evidence"
seo:
  type: "TechArticle"
  date_modified: "2026-08-21T00:00:00+02:00"
---

# Best Strix Halo Mini PC for Local LLMs (2026)

**Short answer:** for local LLM work on a Strix Halo / Ryzen AI MAX+ 395 box, the measured speed differences between OEMs are small (about 5% on the same model and settings). Buy on **price per 128GB config, availability, cooling, and support** rather than on benchmark deltas — and buy **128GB** unless your budget hard-caps you, because the useful large-model routes need it.

This page interprets the evidence in the [canonical Strix Halo guide repository](https://github.com/hogeheer499-commits/strix-halo-guide). Every number links to a dated source; first-party and community measurements stay labeled.

## Same model, same class of settings, five OEM systems

Measured `llama.cpp` results on Qwen3-Coder 30B-A3B (UD-Q4_K_XL, tg128) across owner systems, from the guide's [community results index](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/COMMUNITY_RESULTS.md) and first-party rows:

| System | Result (t/s) | Source type |
|---|---|---|
| Beelink GTR9 Pro | 96.76 | first-party, [claim index](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv) |
| Corsair AI Workstation 300 (3 units) | 93.55–95.50 | community, [issue #10](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10) |
| GMKtec EVO-X2 | 91.40–92.11 | community, [issue #17](https://github.com/hogeheer499-commits/strix-halo-guide/issues/17) (different build/flags — see caveat) |

Read: a **~5% spread** on identical silicon. The GMKtec rows used a different `llama.cpp` build and flag set, so treat the exact gap as indicative, not a ranking. Full raw data: [`data/community_results.csv`](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/community_results.csv). The practical conclusion is the opposite of typical review-site framing: **OEM choice barely moves LLM speed; memory size, price, thermals, and firmware quality are the real decision.**

## 64GB vs 128GB: the decision that actually matters

Based on artifact sizes measured in the guide:

- **64GB** comfortably runs the 30B-class MoE workhorses (Qwen3-Coder 30B, Qwen3-30B-A3B, small MoE like LFM2.5 8B-A1B) at Q4 with normal context. It cannot hold the 120B-class Q4 routes or the ~91GB 284B capacity artifact.
- **128GB** unlocks the routes that make this platform special: Nemotron 3 Super 120B-A12B direct GGUF (~18–19 t/s measured), Step 3.7 Flash 198B server route, and the pinned 90.86GB DeepSeek V4 Flash 284B artifact ([capacity evidence](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/raw/2026-07-16/deepseek-v4-flash-ud-iq2-xxs/), a load/correctness pass, not a speed claim).
- Dense 70B models run on 128GB but measure only ~4.7–4.9 t/s — too slow for interactive chat. If your target is "70B dense", this platform is the wrong tool regardless of RAM; the value is in **MoE models and large-MoE capacity**.

Rule of thumb from the measured table: model file size + roughly 10–20GB for KV cache, runtime, and OS should fit inside your usable unified memory. The [best-known profiles table](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/BEST_KNOWN_PROFILES.md) maps workloads to measured routes.

## Price snapshot and trend

These systems are getting more expensive fast, and that is a documented fact rather than a sales line. The clearest case is the exact machine this guide's first-party benchmarks run on:

**Beelink GTR9 Pro (128GB/2TB) — documented price history**

| Date | Price | Source |
|---|---|---|
| Aug 2025 (launch preorder) | $1,985 | [TechRadar launch coverage](https://www.techradar.com/pro/a-mac-studio-windows-workstation-clone-just-went-on-preorder-with-amds-ai-395-beelink-gtr9-pro-costs-usd1985-has-two-10-gbe-ports-and-128gb-ram) |
| 2026-02-20 | $2,494 | maintainer's own purchase invoice for the benchmark unit used throughout this guide |
| Mar 2026 | $2,999 (preorder) | [Liliputing](https://liliputing.com/more-ryzen-ai-max-395-mini-pcs-with-128gb-are-now-available-if-you-can-afford-one/) |
| 2026-08-21 | $4,349 (list $4,699), pre-sale | [vendor page](https://www.bee-link.com/products/beelink-gtr9-pro-amd-ryzen-ai-max-395), checked today |

That is more than a doubling in about a year, and each documented step has been upward. The driver is the industry-wide DRAM shortage, not one vendor's margin — the same force raised DGX Spark to $4,699 and removed Apple's 512GB Mac Studio option. There is no evidence of a reversal on the horizon; memory pricing is projected to keep climbing into 2027 ([Tom's Hardware](https://www.tomshardware.com/pc-components/ram/memory-price-surge-begins-to-cool-as-consumers-hit-affordability-limit-ai-demand-still-keeps-dram-and-nand-prices-climbing-through-q3-2026)).

The guide's dated canonical snapshot (2026-07-27) is in [`data/buyer_price_snapshot_2026-07-27.csv`](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/buyer_price_snapshot_2026-07-27.csv). Current spot-check on 2026-08-21 (vendor pages / press):

| System (128GB) | 2026-07-27 snapshot | 2026-08-21 spot-check | Note |
|---|---|---|---|
| Bosgame M5 | $2,899 | ~$2,399–2,499 ([vendor](https://www.bosgamepc.com/products/bosgame-m5-ai-mini-desktop-ryzen-ai-max-395)) | currently the cheapest 128GB route |
| Framework Desktop | $3,149 (mainboard) | ~$3,449, batches repeatedly sold out ([TechRadar](https://www.techradar.com/pro/frameworks-desktop-is-selling-like-hot-cakes-ryzen-max-395-max-383-batches-are-sold-out-with-next-shipment-in-q3)) | best ecosystem/support |
| GMKtec EVO-X2 | €3,229–3,359 (EU) | $3,649, 128GB variants sold out on official store ([vendor](https://www.gmktec.com/products/amd-ryzen%e2%84%a2-ai-max-395-evo-x2-ai-mini-pc)) | best value when in stock |
| Corsair AI Workstation 300 | $3,399 (out of stock) | $2,699–3,399 ([Tom's Hardware](https://www.tomshardware.com/desktops/mini-pcs/corsairs-strix-halo-ai-workstation-300-gets-even-more-expensive-amid-the-rampocalypse-ryzen-ai-max-395-flagship-now-sits-at-usd3-399)) | community-validated 3-unit fleet in this guide |
| Minisforum MS-S1 MAX | $3,639 | ~$3,199; 64GB variant $2,639 ([Notebookcheck](https://www.notebookcheck.net/Powerful-Minisforum-MS-S1-Max-mini-PC-gets-a-lower-priced-64GB-RAM-config.1303111.0.html)) | 10GbE, clustering-friendly |
| Beelink GTR9 Pro | $4,349 (pre-sale) | $4,349, list $4,699 ([vendor](https://www.bee-link.com/products/beelink-gtr9-pro-amd-ryzen-ai-max-395), verified 2026-08-21) | deepest first-party evidence in this guide; see price history above |

Context: 128GB Strix Halo boxes launched around $1,800–2,000 in 2025 and have roughly doubled, driven primarily by DRAM contract prices (the industry-wide memory shortage), not vendor margin. The same force raised DGX Spark to $4,699 and removed Apple's 512GB Mac Studio option.

## Buy now or wait?

- **AMD's Strix Halo refresh (Ryzen AI Max 392/388 SKUs and a previewed 192GB Ryzen AI MAX+ PRO 495 Framework desktop)** extends this platform through 2026 ([VideoCardz](https://videocardz.com/newz/framework-previews-desktop-with-ryzen-ai-max-pro-495-and-192gb-memory)).
- **The true successor (Medusa Halo, Zen 6 + RDNA 5) is not expected before H2 2027** ([PC Gamer](https://www.pcgamer.com/hardware/processors/amd-confirms-next-gen-zen-6-cpus-to-launch-in-2026-and-medusa-apus-to-launch-in-2027/), [TweakTown](https://www.tweaktown.com/news/107301/amd-cpu-roadmap-leaks-tease-gator-range-and-medusa-point-plus-halo-zen-6-cpus-for-2027/index.html)).
- Memory prices are projected to keep rising into 2027 ([Tom's Hardware](https://www.tomshardware.com/pc-components/ram/memory-price-surge-begins-to-cool-as-consumers-hit-affordability-limit-ai-demand-still-keeps-dram-and-nand-prices-climbing-through-q3-2026)).

Honest read: waiting a year probably means paying more for the same memory, not less, and the successor is 12+ months out. If the workload exists today, buy the cheapest well-cooled 128GB config you can actually get; if you cannot justify current prices, a used RTX 3090 (~$1,100, 24GB) is the better buy for models that fit in 24GB.

## Recommendation tiers

The maintained tier list with evidence depth per system lives in the repository [Buying Guide](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#buying-guide). Summary: **most evidence-backed** — Beelink GTR9 Pro; **best value candidate** — Bosgame M5 / GMKtec EVO-X2 (stock permitting); **best ecosystem and support** — Framework Desktop; **community-validated fleet** — Corsair AI Workstation 300; **clustering** — Minisforum MS-S1 MAX.

## FAQ

**Is a Strix Halo mini PC worth it for local LLMs in 2026?**
If you want 100B+ MoE models running locally under ~$3,500, it is currently the only x86 option with 96–112GB usable GPU memory. If your models fit in 24GB, a used RTX 3090 is faster and cheaper.

**Which Strix Halo mini PC is fastest for LLMs?**
Measured spread across Beelink, Corsair, and GMKtec on the same model is about 5%. Buy on price, cooling, and support, not OEM benchmark deltas.

**Do I need 128GB of RAM?**
For 30B-class MoE models, 64GB is enough. For the 120B-class and larger capacity routes that justify this platform, you need 128GB.

**Should I wait for the next generation?**
Medusa Halo is not expected before late 2027, and memory prices are still rising. Waiting likely costs more than it saves.

**Why are Strix Halo mini PC prices rising so fast?**
The industry-wide DRAM shortage: 128GB of LPDDR5X is the dominant cost of these systems, and memory contract prices are projected to keep climbing into 2027. The documented Beelink GTR9 Pro history above went from $1,985 to $4,349 in about a year.

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is a Strix Halo mini PC worth it for local LLMs in 2026?",
      "acceptedAnswer": {"@type": "Answer", "text": "If you want 100B+ MoE models running locally under about $3,500, Strix Halo is currently the only x86 option with 96-112GB usable GPU memory. If your models fit in 24GB, a used RTX 3090 is faster and cheaper."}
    },
    {
      "@type": "Question",
      "name": "Which Strix Halo mini PC is fastest for LLMs?",
      "acceptedAnswer": {"@type": "Answer", "text": "Measured spread across Beelink, Corsair, and GMKtec on the same model and settings is about 5%. Buy on price, cooling, and support rather than OEM benchmark deltas."}
    },
    {
      "@type": "Question",
      "name": "Do I need 128GB of RAM for local LLMs on Strix Halo?",
      "acceptedAnswer": {"@type": "Answer", "text": "For 30B-class MoE models, 64GB is enough. For 120B-class and larger capacity routes that justify this platform, you need 128GB."}
    },
    {
      "@type": "Question",
      "name": "Should I wait for the Strix Halo successor?",
      "acceptedAnswer": {"@type": "Answer", "text": "Medusa Halo is not expected before late 2027 and memory prices are still rising, so waiting likely costs more than it saves."}
    },
    {
      "@type": "Question",
      "name": "Why are Strix Halo mini PC prices rising so fast?",
      "acceptedAnswer": {"@type": "Answer", "text": "The industry-wide DRAM shortage: 128GB of LPDDR5X dominates system cost and memory prices are projected to keep climbing into 2027. The documented Beelink GTR9 Pro history went from $1,985 at launch to $4,349 in about a year."}
    }
  ]
}
</script>

---

Community corrections are welcome — open an issue in the [repository](https://github.com/hogeheer499-commits/strix-halo-guide/issues). Pricing rows are dated snapshots, not live quotes. This page contains no affiliate links as of 2026-08-21; if that changes, links will be disclosed per [`VENDOR_DISCLOSURE.md`](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/VENDOR_DISCLOSURE.md).
