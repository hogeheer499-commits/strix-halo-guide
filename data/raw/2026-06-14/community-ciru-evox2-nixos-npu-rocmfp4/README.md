# Ciru-ai GMKtec EVO-X2 NixOS / NPU / ROCmFP4 Evidence Package

Community source of truth:

- https://github.com/ciru-ai/strix-halo-evo-x2-evidence

Contributor:

- [`ciru-ai`](https://github.com/ciru-ai)

Status:

- Community-reported external artifact.
- This directory intentionally stores only a provenance note. The full sanitized CSV/SQLite bundle stays in ciru-ai's repository and is linked from the guide.
- Rows from this package are not first-party Beelink headline claims and are not direct replacements for the guide's direct `llama-bench` rows.

System snapshot from the public artifact:

- GMKtec NucBox_EVO-X2 / EVO-X2-001, hardware version 1.0
- AMD Ryzen AI MAX+ 395 with Radeon 8060S
- 128GB-class memory, 123GiB visible to Linux
- BIOS VRAM setting: 2GB
- NixOS 26.05 pre-release, Linux 7.0.1
- RADV STRIX_HALO, Mesa 26.0.5, Vulkan 1.4.341
- AMD Strix/Krackan/Strix Halo NPU exposed through `/dev/accel/accel0`
- IOMMU enabled with `iommu.passthrough=0`

Why this matters:

- It adds a second GMKtec EVO-X2 owner/source with a different OS and setup philosophy than the earlier Ubuntu GMKtec rows.
- It is the first imported guide-linked package focused on NPU sidecar use while keeping IOMMU enabled.
- It links Strix Halo throughput with quality-eval evidence, not just short-context token speed.
- It provides a public sanitized data bundle with SQLite and CSV exports, making the contribution auditable without copying the full artifact into this repository.

Highest-value public metrics imported into this guide:

- 64k iGPU workload with concurrent NPU load: +3.29% main latency.
- Comparable iGPU auxiliary load: +68.96% main latency.
- FastFlowLM-NPU LFM2.5 1.2B at 32k: 1646 prompt tok/s, 38.18 decode tok/s, about 2.09GiB RSS.
- Qwopus3.6 27B Chadrock HumanEval+: 0.9451, with about 2.85x lower recorded request-generation time than the stored original Qwopus comparator.
- Qwen3.6 27B MTP ROCmFP4 HumanEval+: 0.9451.
- CHADROCK3.6 35B HumanEval+ around 0.91, with 95.6 and 108.2 tok/s public quality-run speed rows.
- Ace Saber 35B ROCmFP4 MTP HumanEval+: 0.9024, with 104.35 peak predicted tok/s and 101.33 last-active predicted tok/s.
- CrownV7 Qwen3.6 35B dynamic route: 515.33 tok/s prompt processing at 128k, 60.71 tok/s diagnostic TG, HumanEval+ 0.8902, BFCL v4 non-live accuracy 0.83, HermesAgent-20 average 0.70.
- Gemma 4 26B-A4B QAT/MTP: 122.8 decode tok/s after TTFP on a 512-token API row, 120.14 tok/s at 8k, 96.36 tok/s at 16k, HumanEval+ 0.9207.
- Gemma 4 12B QAT/MTP: HumanEval+ 0.9329 and best 512-token decode speed 104.07 tok/s.

Guide integration:

- Summary: [`COMMUNITY_RESULTS.md`](../../../../COMMUNITY_RESULTS.md#gmktec-evo-x2-nixos--npu--rocmfp4-evidence-package)
- Contributor credit: [`CONTRIBUTORS.md`](../../../../CONTRIBUTORS.md)
- Structured metric subset: [`data/community_ciru_evox2_metrics.csv`](../../../community_ciru_evox2_metrics.csv)

Claim boundaries:

- Keep this as community evidence, not a first-party measured-local headline.
- Keep NPU sidecar claims separate from iGPU Vulkan/RADV decode claims.
- Keep served/API, MTP/speculative, ROCmFP4, quality-eval, and direct `llama-bench` rows separate.
- Treat ROCmFP4/Chadrock rows as external tuned-route evidence unless reproduced locally or upstreamed into a stock route.
