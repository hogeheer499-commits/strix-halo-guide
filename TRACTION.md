# Traction And Public Evidence

This file collects social proof, reach, and evidence that the guide helps real buyers and developers evaluate AMD Strix Halo / Ryzen AI MAX+ local-AI hardware.

Do not invent traction numbers. Fill the TODOs only from current public GitHub data, screenshots, issues, discussions, or documented external mentions.

## Current Public GitHub Stats

Repository-stat snapshot date: 2026-07-14. Traffic remains the separately dated GitHub 14-day window ending 2026-07-08.

| Metric | Current value | Source |
|--------|---------------|--------|
| Stars | 215 | [GitHub repository page](https://github.com/hogeheer499-commits/strix-halo-guide) |
| Forks | 10 | [GitHub repository page](https://github.com/hogeheer499-commits/strix-halo-guide) |
| Watchers | 4 | [GitHub repository page](https://github.com/hogeheer499-commits/strix-halo-guide) |
| Open issues | 7 | [GitHub Issues](https://github.com/hogeheer499-commits/strix-halo-guide/issues) |
| Open pull requests | 0 | [GitHub Pull Requests](https://github.com/hogeheer499-commits/strix-halo-guide/pulls) |
| Releases | 5 | [GitHub Releases](https://github.com/hogeheer499-commits/strix-halo-guide/releases) |
| GitHub contributors | 3 | [GitHub Contributors](https://github.com/hogeheer499-commits/strix-halo-guide/graphs/contributors) |
| Community benchmark contributors credited | 8 | [`CONTRIBUTORS.md`](CONTRIBUTORS.md) |
| Strix Halo-class systems/sources represented | 11 | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`COMMUNITY_NIMO.md`](COMMUNITY_NIMO.md) |
| Repository views | 1,837 total / 816 unique | GitHub Traffic API snapshot, 2026-07-10 |
| Repository clones | 169 total / 100 unique | GitHub Traffic API snapshot, 2026-07-10 |
| Largest recorded referrer | Google: 548 views / 352 unique visitors | GitHub Traffic API snapshot, 2026-07-10 |

Read the star count as a small-niche demand signal, not the main argument. The stronger vendor evidence is the technical proof layer: reproducible commands, raw logs, CSVs, claim indexes, community rows, and documented failures.

## Evidence Already In The Repo

| Evidence type | Where to read it | Why it matters |
|---------------|------------------|----------------|
| Community validation | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`COMMUNITY_NIMO.md`](COMMUNITY_NIMO.md), [`data/community_results.csv`](data/community_results.csv), [`data/community_nimo_issue4.csv`](data/community_nimo_issue4.csv) | Shows independent reproduction and portability evidence across Beelink owner stacks, Corsair, GMKtec, MS-S1-Max, and Nimo without treating community data as vendor endorsement. |
| Community power context | [`COMMUNITY_RESULTS.md#whole-system-power`](COMMUNITY_RESULTS.md#whole-system-power), [`data/community_power.csv`](data/community_power.csv) | Helps buyers think about efficiency, heat, and always-on operation. |
| Community RPC and USB4 data | [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md), [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md), [`data/community_rpc.csv`](data/community_rpc.csv) | Shows advanced capacity/scaling experiments while keeping them separate from default single-machine guidance. |
| Raw benchmark data | [`data/raw/`](data/raw/) | Lets readers inspect command output and provenance instead of relying on summary claims. |
| Structured CSV data | [`data/README.md`](data/README.md) | Makes benchmark rows reusable and auditable. |
| Claim index | [`data/headline_claims.csv`](data/headline_claims.csv) | Maps public headline claims to evidence files and notes. |
| Charts | [`charts/`](charts/README.md) | Turns CSV data into reviewable visual summaries. |
| Reproducibility notes | [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) | Documents machine state, setup details, and benchmark caveats. |
| Issue-based reports | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md) links to public GitHub issues | Shows how community results are sourced and credited. |

## Traffic Screenshots

Store GitHub traffic screenshots here:

```text
docs/assets/traffic/
```

Suggested files:

- `docs/assets/traffic/github-traffic-YYYY-MM-DD.png`
- `docs/assets/traffic/github-referrers-YYYY-MM-DD.png`
- `docs/assets/traffic/github-clones-YYYY-MM-DD.png`

Rules:

- Do not invent visitor, clone, referrer, or search numbers.
- Include the screenshot date.
- If summarizing a screenshot in text, link to the screenshot and state the date range shown by GitHub.

## Testimonials And Quotes

Use this format only when the quote is real and permission is clear:

```text
Quote: "TODO: exact approved quote."
Name/handle: TODO
Source/link: TODO
Date: TODO
Permission: TODO: public quote / explicit permission / other documented basis
Related evidence: TODO
```

Do not invent testimonials, buyer quotes, vendor quotes, sponsor quotes, or endorsement language.

## External Mentions

Track external mentions only when there is a real source link.

| Source type | Link | Date | What it shows |
|-------------|------|------|---------------|
| Reddit | TODO | TODO | TODO |
| GitHub Discussions | TODO | TODO | TODO |
| Forums | TODO | TODO | TODO |
| Newsletters | TODO | TODO | TODO |
| Blogs | TODO | TODO | TODO |
| YouTube | TODO | TODO | TODO |
| Discord | TODO | TODO | TODO: include permission or public-link basis |
| Search / AI-search mentions | TODO | TODO | TODO |

## Why This Matters To Vendors

Traction is not just a vanity metric. For this project, traction is evidence that the guide removes uncertainty and increases buyer/developer confidence.

When buyers, developers, reviewers, and system owners use the guide to reproduce a setup, compare hardware, submit a benchmark, or avoid a broken path, that is adoption-friction evidence. It helps AMD, OEMs, reviewers, and developer-relations teams understand which hardware and software questions are blocking real local-AI adoption.
