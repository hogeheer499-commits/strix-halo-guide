---
layout: default
title: "Best Strix Halo Mini PC for Local LLMs (2026): Beelink vs Framework vs GMKtec vs Corsair"
description: "Evidence-based comparison of AMD Ryzen AI MAX+ 395 mini PCs for local LLMs: measured cross-OEM benchmarks, 64GB vs 128GB fit guidance, dated prices, and buy-now-or-wait timing."
permalink: /best-strix-halo-mini-pc/
date: "2026-08-21T00:00:00+02:00"
last_modified_at: "2026-08-30T00:00:00+02:00"
image:
  path: "https://hogeheer499-commits.github.io/strix-halo-guide/assets/social-preview.png"
  height: 640
  width: 1280
  alt: "AMD Strix Halo mini PC comparison for local LLMs with measured cross-OEM evidence"
seo:
  type: "TechArticle"
  date_modified: "2026-08-30T00:00:00+02:00"
---

# Best Strix Halo Mini PC for Local LLMs (2026)

**Evidence reviewed:** August 30, 2026.

Start with the independent [Strix Halo Guide](https://strixhaloguide.com/) for
the current setup and evidence model; use this page for the buyer comparison.

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
| 2026-08-21 | $4,349 (list $4,699), pre-sale | [vendor page](https://www.bee-link.com/products/beelink-gtr9-pro-amd-ryzen-ai-max-395) |
| 2026-08-29 | $4,349 (list $4,699), pre-sale, ships within 35 days — unchanged | [vendor page](https://www.bee-link.com/products/beelink-gtr9-pro-amd-ryzen-ai-max-395), re-verified |

That is more than a doubling in about a year, and each documented step has been upward. The driver is the industry-wide DRAM shortage, not one vendor's margin — the same force raised DGX Spark to $4,699 and removed Apple's 512GB Mac Studio option. There is no evidence of a reversal on the horizon; memory pricing is projected to keep climbing into 2027 ([Tom's Hardware](https://www.tomshardware.com/pc-components/ram/memory-price-surge-begins-to-cool-as-consumers-hit-affordability-limit-ai-demand-still-keeps-dram-and-nand-prices-climbing-through-q3-2026)).

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

Context: 128GB Strix Halo boxes launched around $1,800–2,000 in 2025 and have roughly doubled, driven primarily by DRAM contract prices (the industry-wide memory shortage), not vendor margin. The same force raised DGX Spark to $4,699 and removed Apple's 512GB Mac Studio option.

## Buy now or wait?

- **The 192GB refresh is official, not a rumor.** AMD announced the Ryzen AI Max PRO 400 series ("Gorgon Halo") on 2026-05-20: the Max+ PRO 495 supports up to **192GB LPDDR5X-8533** but keeps the same Zen 5 + RDNA 3.5 architecture and the same ~273GB/s bandwidth class ([ServeTheHome](https://www.servethehome.com/amd-reveals-ryzen-ai-max-pro-400-series-192gb-ram-for-ai-systems/), [Tom's Hardware](https://www.tomshardware.com/pc-components/cpus/amd-ryzen-ai-max-400-gorgon-halo-packs-up-to-192gb-of-unified-memory-refreshed-apu-uses-zen-5-and-rdna-3-5-and-can-clock-up-to-5-2-ghz)). OEM systems (ASUS, HP, Lenovo, a Framework Desktop with a live "192GB coming soon" tab, and a confirmed GMKtec EVO-X3) are reported from Q3 2026.
- **What 192GB changes and does not change:** more memory means larger models and more context fit, but bandwidth — the main LLM decode limiter on this platform — stays in the same class. Expect capacity gains, not speed gains, and expect the 192GB tier to be priced well above current 128GB boxes at today's DRAM prices.
- **The true successor (Medusa Halo, Zen 6 + RDNA 5) is not expected before H2 2027** ([PC Gamer](https://www.pcgamer.com/hardware/processors/amd-confirms-next-gen-zen-6-cpus-to-launch-in-2026-and-medusa-apus-to-launch-in-2027/), [TweakTown](https://www.tweaktown.com/news/107301/amd-cpu-roadmap-leaks-tease-gator-range-and-medusa-point-plus-halo-zen-6-cpus-for-2027/index.html)); rumored LPDDR6 bandwidth gains remain unconfirmed leaks.
- Memory prices are projected to keep rising into 2027 ([Tom's Hardware](https://www.tomshardware.com/pc-components/ram/memory-price-surge-begins-to-cool-as-consumers-hit-affordability-limit-ai-demand-still-keeps-dram-and-nand-prices-climbing-through-q3-2026)).

Honest read: waiting a year probably means paying more for the same memory, not less, and the real generational jump is 12+ months out. Wait for a Gorgon Halo 192GB system only if your target models genuinely need more than ~112GB of usable GPU memory — it will fit more, not run faster. If the workload exists today, buy the cheapest well-cooled 128GB config you can actually get; if you cannot justify current prices, a used RTX 3090 (~$1,100, 24GB) is the better buy for models that fit in 24GB.

## Recommendation tiers

The maintained tier list with evidence depth per system lives in the repository [Buying Guide](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/README.md#buying-guide). Summary: **most evidence-backed** — Beelink GTR9 Pro; **best value candidate** — Bosgame M5 / GMKtec EVO-X2 (stock permitting); **best ecosystem and support** — Framework Desktop; **community-validated fleet** — Corsair AI Workstation 300; **clustering** — Minisforum MS-S1 MAX.

These tiers use memory configuration, dated price/availability, evidence depth,
cooling/thermals, firmware/support, ports, expandability, and workload fit.
Affiliate commission is not a ranking input. If affiliate links are introduced,
each will be labeled near the link and entered in the public
[`affiliate link registry`](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/affiliate_link_registry.csv).

## FAQ

**Is a Strix Halo mini PC worth it for local LLMs in 2026?**
If you want 100B+ MoE models running locally in the $2,000–4,500 mini-PC class, it is currently the only x86 option with 96–112GB usable GPU memory. If your models fit in 24GB, a used RTX 3090 is faster and cheaper.

**Which Strix Halo mini PC is fastest for LLMs?**
Measured spread across Beelink, Corsair, and GMKtec on the same model is about 5%. Buy on price, cooling, and support, not OEM benchmark deltas.

**Do I need 128GB of RAM?**
For 30B-class MoE models, 64GB is enough. For the 120B-class and larger capacity routes that justify this platform, you need 128GB.

**Should I wait for the next generation?**
The officially announced Gorgon Halo refresh (Q3 2026) adds a 192GB tier but keeps the same bandwidth class, so it fits more without running faster. The real successor, Medusa Halo, is not expected before late 2027, and memory prices are still rising. Waiting likely costs more than it saves unless you specifically need more than 128GB.

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
      "acceptedAnswer": {"@type": "Answer", "text": "If you want 100B+ MoE models running locally in the $2,000-4,500 mini-PC class, Strix Halo is currently the only x86 option with 96-112GB usable GPU memory. If your models fit in 24GB, a used RTX 3090 is faster and cheaper."}
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
      "acceptedAnswer": {"@type": "Answer", "text": "The announced Gorgon Halo refresh (Q3 2026) adds a 192GB tier at the same bandwidth class; the real successor, Medusa Halo, is not expected before late 2027 and memory prices are still rising, so waiting likely costs more than it saves unless you need more than 128GB."}
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

Community corrections are welcome — open an issue in the [repository](https://github.com/hogeheer499-commits/strix-halo-guide/issues). Pricing rows are dated snapshots, not live quotes. This page contains no affiliate links as of August 30, 2026; if that changes, links will be disclosed next to the relevant product and per [`VENDOR_DISCLOSURE.md`](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/VENDOR_DISCLOSURE.md).
