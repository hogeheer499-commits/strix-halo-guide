# Community Qwen3-Coder Issue #10 Provenance

Source issue: https://github.com/hogeheer499-commits/strix-halo-guide/issues/10

Contributor: Fail-Safe.

This directory documents provenance for the original Qwen3-Coder community report. The original data was posted as issue text and follow-up comments rather than as separate attached raw files, so the canonical raw source remains the linked GitHub issue comments. Structured rows live in:

- `data/community_results.csv`
- `data/community_power.csv`

Mapped source comments:

| Source | Structured data | What it contributes |
|--------|-----------------|---------------------|
| https://github.com/hogeheer499-commits/strix-halo-guide/issues/10 | `data/community_results.csv` rows 2 and 3 context | Corsair AI Workstation 300 system metadata and first Qwen3-Coder Vulkan/RADV session. |
| https://github.com/hogeheer499-commits/strix-halo-guide/issues/10#issuecomment-4398735200 | `data/community_results.csv` row 3 | Second 20-rep Qwen3-Coder session about 12 hours later on the same box. |
| https://github.com/hogeheer499-commits/strix-halo-guide/issues/10#issuecomment-4401323126 | `data/community_results.csv` rows 4-10 | N=3 same-SKU cross-box variance plus thermal/clock instrumented rows. |
| https://github.com/hogeheer499-commits/strix-halo-guide/issues/10#issuecomment-4401438242 | `data/community_power.csv` rows 2-4 | Whole-system wall-power and energy-per-token baseline. |
| https://github.com/hogeheer499-commits/strix-halo-guide/issues/10#issuecomment-4413965527 | `data/community_results.csv` rows 11-12 and `data/raw/2026-05-09/community-qwen36-issue10/` | Qwen3.6 Q4_0 versus Q4_K_M follow-up rows. |

The main practical value of this issue is independent portability evidence: a different Strix Halo chassis, distro, RC kernel, Mesa version, container setup, and power-management profile still reproduced the guide's Qwen3-Coder Vulkan/RADV performance class within a few percent.
