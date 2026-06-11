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

- Deepens the public eight-system evidence map with a Nimo follow-up, counted separately from the Beelink, three Corsair boxes, two GMKtec sources, and the MS-S1-Max report.
- Adds a compact Nimo chassis, not just another Beelink or GMKtec variant.
- Shows useful rows with IOMMU enabled and 4GB UMA, which differs from this guide's main Beelink setup.
- Adds large-model serving evidence for 122B-class and StepFun-class routes that answer a different buyer question: "Can this compact unified-memory box run very large local models at all?"
- Adds Gemma 4 QAT + MTP assistant-head evidence, which answers a newer setup question: "Do matched QAT MTP heads matter on Strix Halo, and where do they help or fail?"
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
| Gemma 4 12B QAT Q4_0 + matched MTP head | Atomic TurboQuant fork, Vulkan/RADV b9360 | 539.9 tok/s prefill, 45.6 tok/s decode | Matched QAT MTP head raised acceptance to 78.4% and improved single-stream decode by 77.4% versus the plain QAT row. | [`GEMMA4-QAT-NUMBERS.md`](data/raw/2026-06-06/community-nimo-gemma4-qat-issue4/GEMMA4-QAT-NUMBERS.md) |
| Gemma 4 26B-A4B QAT Q4_0 + matched MTP head | Atomic TurboQuant fork, Vulkan/RADV b9360 | 729.3 tok/s prefill, 71.4 tok/s decode | Best single-stream Gemma QAT row in the submitted bundle; matched QAT head closed the non-QAT-head acceptance gap, 56.9% to 91.8%. The original report had a `PARALLEL=2` crash caveat; Atomic PR #26 has since landed, so fresh post-merge 2-slot numbers are the useful next evidence. | [`GEMMA4-QAT-NUMBERS.md`](data/raw/2026-06-06/community-nimo-gemma4-qat-issue4/GEMMA4-QAT-NUMBERS.md) |
| Gemma 4 31B QAT Q4_0 + matched MTP head | Atomic TurboQuant fork, Vulkan/RADV b9360 | 203.6 tok/s prefill, 19.1 tok/s decode | Dense 31B route is bandwidth-limited plain at 11.0 tok/s; matched MTP recovered significant single-stream speed, +73.6% decode. | [`GEMMA4-QAT-NUMBERS.md`](data/raw/2026-06-06/community-nimo-gemma4-qat-issue4/GEMMA4-QAT-NUMBERS.md) |
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
- The Gemma 4 QAT rows are useful because they separate three issues that are easy to mix up: QAT main-model speed, MTP assistant-head compatibility, and serving concurrency. Matched QAT heads improve single-stream decode; the submitted Atomic rows predate the merged `PARALLEL=2` fix, so post-fix aggregate throughput still needs fresh measurement.
- The DFlash 27B row is useful precisely because it is not fast; it prevents the guide from over-promoting a complex route without evidence.
- The Nimo metadata differs from the Beelink recommendation, so it should be read as portability evidence, not a universal setup recommendation.

## Boxwrench Follow-Up

boxwrench later added two useful follow-ups in issue #4:

- StepFun MTP tuning: lowering `--ubatch-size` from 512 to 256 improved the submitted StepFun decode from 26.0 to 27.9 tok/s and improved 2-slot aggregate from 35.7 to 38.5 tok/s in that harness. This is community server-tuning evidence, not a Beelink headline.
- Atomic PR #26: the Gemma 4 MTP `PARALLEL=2` crash fix was merged upstream. The useful next step is a fresh post-merge Gemma 4 QAT MTP repeat with exact Atomic commit, command, acceptance rate, single-stream decode, and 2-slot aggregate throughput.

That means the old Gemma QAT caveat should no longer be read as "this cannot be fixed." It should be read as "the submitted rows predate the fix, and the guide still needs measured post-fix evidence before changing the recommendation."

## Raw Evidence

- Bundle README: [`data/raw/2026-06-03/community-nimo-issue4/README.md`](data/raw/2026-06-03/community-nimo-issue4/README.md)
- System metadata: [`SYSTEM-METADATA.md`](data/raw/2026-06-03/community-nimo-issue4/SYSTEM-METADATA.md)
- Reproducibility notes: [`REPRODUCIBILITY.md`](data/raw/2026-06-03/community-nimo-issue4/REPRODUCIBILITY.md)
- Raw benchmark rows: [`RAW-BENCHMARK-ROWS.md`](data/raw/2026-06-03/community-nimo-issue4/RAW-BENCHMARK-ROWS.md)
- Manifest: [`manifest.csv`](data/raw/2026-06-03/community-nimo-issue4/manifest.csv)
- Contributor claim index: [`headline_claims.csv`](data/raw/2026-06-03/community-nimo-issue4/headline_claims.csv)
- Thermal telemetry: [`THERMAL-TELEMETRY-NIMO.md`](data/raw/2026-06-03/community-nimo-issue4/THERMAL-TELEMETRY-NIMO.md)
- Gemma 4 QAT follow-up: [`GEMMA4-QAT-NUMBERS.md`](data/raw/2026-06-06/community-nimo-gemma4-qat-issue4/GEMMA4-QAT-NUMBERS.md)
