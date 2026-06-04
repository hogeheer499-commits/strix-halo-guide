# Community Nimo AI Mini PC Results

boxwrench contributed a Nimo AI Mini PC benchmark bundle in [issue #4](https://github.com/hogeheer499-commits/strix-halo-guide/issues/4#issuecomment-4608440144). This is community-submitted evidence, not a first-party Beelink headline claim.

The value is not one single faster headline number. The value is that another compact Ryzen AI MAX+ 395 / Radeon 8060S / 128GB system now has structured setup notes, model rows, thermal context, and large-model serving evidence. That reduces buyer uncertainty around whether Strix Halo results are tied only to the Beelink test box.

## System

| Field | Value |
|---|---|
| Contributor | [boxwrench](https://github.com/boxwrench) |
| System | Nimo AI Mini PC |
| APU | AMD Ryzen AI MAX+ 395 / Radeon 8060S (`gfx1151`) |
| Memory | 128GB unified LPDDR5X |
| OS | Ubuntu 25.04 in the benchmark bundle; supplemental telemetry also references Linux Mint 22.3 / Ubuntu 24.04 |
| Kernel | `6.18.1-061801-generic` |
| Mesa / RADV | Mesa 25.2.8 / RADV |
| ROCm | 7.1.1 baseline; some rows reference 7.2.x runtime libraries |
| BIOS / memory | 4GB UMA dedicated VRAM; IOMMU enabled (`amd_iommu=on`) |
| Raw bundle | [`data/raw/2026-06-03/community-nimo-issue4/`](data/raw/2026-06-03/community-nimo-issue4/) |

## Why This Matters

- Adds a fifth community contributor and brings the public evidence map to eight Strix Halo-class systems when counted with the Beelink, three Corsair boxes, two GMKtec sources, and the MS-S1-Max report.
- Adds a compact Nimo chassis, not just another Beelink or GMKtec variant.
- Shows useful rows with IOMMU enabled and 4GB UMA, which differs from this guide's main Beelink setup.
- Adds large-model serving evidence for 122B-class and StepFun-class routes that answer a different buyer question: "Can this compact unified-memory box run very large local models at all?"
- Includes thermal and power context, including rows that report no thermal throttle and a separate Nimo telemetry note with fan/noise/power observations.
- Gives vendors/OEMs a clearer path for what evidence is valuable: system metadata, exact model/backend/settings, raw rows, thermal notes, and caveats.

## Key Rows

These rows are not apples-to-apples `llama-bench` headline replacements. They are community serving/eval/large-model rows. Use the exact workload and backend before comparing them to the Beelink direct `llama-bench` rows.

| Route | Backend | Result | Practical read | Raw evidence |
|---|---|---:|---|---|
| Qwen 3.6 35B-A3B MXFP4 | Lemonade llama.cpp ROCm b9247 | 628.1 tok/s prefill, 44.2 tok/s decode | Practical 35B MoE serving row on Nimo; useful ROCm/Lemonade context. | [`RAW-BENCHMARK-ROWS.md`](data/raw/2026-06-03/community-nimo-issue4/RAW-BENCHMARK-ROWS.md) |
| Qwen 3.6 35B MTP Q4_K_M | Vulkan/RADV b9360 `llama-server` | 81.2 tok/s | Confirms the MTP/server lane is useful beyond the Beelink/GMKtec rows, but this is a server/speculative route. | [`RAW-BENCHMARK-ROWS.md`](data/raw/2026-06-03/community-nimo-issue4/RAW-BENCHMARK-ROWS.md) |
| Qwen3-Coder-Next UD-Q4_K_XL | Vulkan/RADV b9360 server | 723.2 tok/s prefill, 44.4 tok/s decode | Current coding-model serving row; Vulkan beat the contributor's ROCm baseline in this bundle. | [`QWEN3-CODER-NEXT-NUMBERS.md`](data/raw/2026-06-03/community-nimo-issue4/QWEN3-CODER-NEXT-NUMBERS.md) |
| Qwen 3.5 122B-A10B MXFP4 | Lemonade llama.cpp ROCm b9247 | 136.0 tok/s prefill, 19.5 tok/s decode | Important large-model feasibility row: 122B-class local serving works, but at a different speed class from 30B/35B MoE rows. | [`RAW-BENCHMARK-ROWS.md`](data/raw/2026-06-03/community-nimo-issue4/RAW-BENCHMARK-ROWS.md) |
| Qwen 3.5 122B-A10B MTP | Vulkan/RADV b9360 server | 28.3 tok/s best tuned decode | MTP tuning improved the 122B lane over the non-speculative baseline; `PMIN` pruning reduced throughput despite higher validation efficiency. | [`QWEN122B-MTP-TUNING-NUMBERS.md`](data/raw/2026-06-03/community-nimo-issue4/QWEN122B-MTP-TUNING-NUMBERS.md) |
| StepFun Step-3.7-Flash UD-IQ4_XS | Vulkan/RADV b9360 server | 43.13 tok/s prefill, 22.28 tok/s decode | 198B-class sparse MoE feasibility row; useful for "large model on 128GB unified memory" buyers. | [`STEPFUN-NUMBERS.md`](data/raw/2026-06-03/community-nimo-issue4/STEPFUN-NUMBERS.md) |
| StepFun Step-3.7-Flash MTP | Vulkan/RADV b9360 patched server | 211.2 tok/s prefill, 26.0 tok/s decode | MTP improved decode by about 27.5% in the contributor's harness, with high draft acceptance from raw timing logs. | [`STEPFUN-MTP-NUMBERS.md`](data/raw/2026-06-03/community-nimo-issue4/STEPFUN-MTP-NUMBERS.md) |
| Qwen 3.6 27B Dense DFlash | Lucebox HIP / DFlash | about 7 tok/s | Useful negative/control evidence: functional, but not a speed route in this bundle. | [`RAW-BENCHMARK-ROWS.md`](data/raw/2026-06-03/community-nimo-issue4/RAW-BENCHMARK-ROWS.md) |

## Thermal And Power Context

The submitted StepFun and Qwen 122B notes both describe the system as power-limited rather than thermally throttled in those runs. Supplemental Nimo telemetry also reports:

- Mistral-Medium-128B-Q4_K_M sustained about 1.57 tok/s with about 79Gi unified-memory use.
- Peak system power around 145-154W in the supplemental telemetry.
- Peak fan noise around 46 dBA.
- GPU/CPU peak temperatures around 88C in the supplemental telemetry.
- Full iGPU offload with substantial memory left for context in that Mistral run.

Treat these as contributor telemetry rows, not Beelink wall-power claims. They are useful buyer context for compact-chassis heat/noise expectations.

## Interpretation

This Nimo bundle expands the guide from "fastest direct rows on one Beelink" toward a broader Strix Halo evidence map:

- The direct Beelink headlines remain separate.
- The Nimo data is strongest for large-model feasibility, server/MTP routes, and buyer-friction reduction.
- The StepFun and Qwen 122B rows are especially useful because they answer "what can 128GB unified memory attempt?" rather than only "what is the fastest 30B decode number?"
- The DFlash 27B row is useful precisely because it is not fast; it prevents the guide from over-promoting a complex route without evidence.
- The Nimo metadata differs from the Beelink recommendation, so it should be read as portability evidence, not a universal setup recommendation.

## Raw Evidence

- Bundle README: [`data/raw/2026-06-03/community-nimo-issue4/README.md`](data/raw/2026-06-03/community-nimo-issue4/README.md)
- System metadata: [`SYSTEM-METADATA.md`](data/raw/2026-06-03/community-nimo-issue4/SYSTEM-METADATA.md)
- Reproducibility notes: [`REPRODUCIBILITY.md`](data/raw/2026-06-03/community-nimo-issue4/REPRODUCIBILITY.md)
- Raw benchmark rows: [`RAW-BENCHMARK-ROWS.md`](data/raw/2026-06-03/community-nimo-issue4/RAW-BENCHMARK-ROWS.md)
- Manifest: [`manifest.csv`](data/raw/2026-06-03/community-nimo-issue4/manifest.csv)
- Contributor claim index: [`headline_claims.csv`](data/raw/2026-06-03/community-nimo-issue4/headline_claims.csv)
- Thermal telemetry: [`THERMAL-TELEMETRY-NIMO.md`](data/raw/2026-06-03/community-nimo-issue4/THERMAL-TELEMETRY-NIMO.md)
