# ROCmFP4 / CHADROCK Advanced Lane

This page tracks the experimental ROCmFP4 / CHADROCK route for AMD Strix Halo / Ryzen AI MAX+ 395 systems.

It is not the default setup path. New users should start with [`setup.sh`](setup.sh), Ollama, and Vulkan/RADV as described in the [`README.md`](README.md). ROCmFP4 is an advanced route for people who want to test tuned GGUFs, MTP/speculative decoding, ROCm/HIP behavior, NPU-aware stacks, and quality/speed tradeoffs.

## What It Is

[`charlie12345/rocmfp4-llama`](https://github.com/charlie12345/rocmfp4-llama) is an experimental `llama.cpp` branch focused on AMD Strix Halo / `gfx1151`.

The branch documents:

- custom ROCmFP4 GGUF tensor formats
- Strix Halo / `gfx1151` build scripts
- ROCm/HIP and Vulkan integration work
- MTP/speculative decoding guard tests
- reproducibility notes for Strix Halo runs

Treat it as a separate runtime lane. Do not mix its results with stock upstream `llama.cpp` Vulkan/RADV direct `llama-bench` headline rows.

## Why It Matters

The guide already has a community evidence package from ciru-ai's GMKtec EVO-X2 / NixOS / IOMMU-on stack that includes ROCmFP4, Chadrock/Qwopus, Gemma QAT/MTP, CrownV7, quality metrics, and NPU sidecar data:

- [`COMMUNITY_RESULTS.md#gmktec-evo-x2-nixos--npu--rocmfp4-evidence-package`](COMMUNITY_RESULTS.md#gmktec-evo-x2-nixos--npu--rocmfp4-evidence-package)
- [`data/community_ciru_evox2_metrics.csv`](data/community_ciru_evox2_metrics.csv)
- [`ciru-ai/strix-halo-evo-x2-evidence`](https://github.com/ciru-ai/strix-halo-evo-x2-evidence)

That makes ROCmFP4 valuable for the guide because it answers different buyer and vendor questions than the default path:

- Can tuned Strix Halo GGUFs improve practical quality/speed tradeoffs?
- Can an IOMMU-on setup keep NPU workflows usable while the iGPU handles the main model?
- Which routes are promising enough to reproduce on a second system?
- Which runtime/model combinations are too experimental for beginner guidance?

## Current Public Artifacts To Watch

These are artifact scans, not first-party Beelink benchmark claims.

| Artifact | Size observed | Why it is interesting |
| --- | ---: | --- |
| [`jcbtc/qwopus3.6-27b-v2-chadrock-rocmfp4-mtp`](https://huggingface.co/jcbtc/qwopus3.6-27b-v2-chadrock-rocmfp4-mtp) | 13.8 GiB | Practical 27B tuned ROCmFP4/MTP candidate with existing ciru quality context. |
| [`jcbtc/chadrock3.6-27b-pi-agent-rocmfp4-mtp`](https://huggingface.co/jcbtc/chadrock3.6-27b-pi-agent-rocmfp4-mtp) | 13.8 GiB | Small enough for a clean local smoke/repro attempt; useful for agent-profile testing. |
| [`jcbtc/chadrock-35b-ace-saber-rocmfp4-mtp`](https://huggingface.co/jcbtc/chadrock-35b-ace-saber-rocmfp4-mtp) | 17.7 GiB | 35B-class tuned ROCmFP4/MTP route; useful because ciru's evidence includes quality-plus-speed signals. |
| [`jcbtc/CHADROCK3.6-35B-UNCENSORED-MTP-STRIX-LEAN`](https://huggingface.co/jcbtc/CHADROCK3.6-35B-UNCENSORED-MTP-STRIX-LEAN) | 17.7 GiB | Earlier 35B STRIX_LEAN candidate; useful for format/runtime checks. |
| [`jcbtc/qwen3.6-35b-a3b-crown-halo-mtp-dynamic`](https://huggingface.co/jcbtc/qwen3.6-35b-a3b-crown-halo-mtp-dynamic) | 21.0 GiB | CrownV7-style dynamic route; useful for tool/function-calling and long-context behavior if reproduced cleanly. |
| [`jcbtc/Step-3.7-Flash-ROCmFPX-Q3-QualityPlus`](https://huggingface.co/jcbtc/Step-3.7-Flash-ROCmFPX-Q3-QualityPlus) | 81.77 GiB target shards, plus separate Q8 MTP draft | 198B-class / ~11B-active capacity and agent route built for 128GB Strix Halo. The smaller Q3 footprint leaves more room for KV cache and long context, but requires the pinned ROCmFPX runner and is not a stock `llama.cpp` artifact. |

## First Repro Plan

The first local Beelink test should be a smoke/repro route, not a broad benchmark campaign.

Record:

- `rocmfp4-llama` commit
- exact model repository, filename, size, and hash
- ROCm, kernel, Mesa, and firmware context
- exact command
- no-spec baseline when possible
- MTP/speculative route when possible
- acceptance rate or available speculative metrics
- short decode and sustained decode separately
- whether the route loads cleanly without breaking the default Vulkan/RADV setup

The first useful result can be negative. A clean "does not build", "loads but crashes", "runs but slower than Vulkan", or "needs IOMMU-on/ROCm tuning" result still removes setup friction.

## Step 3.7 Q3 QualityPlus First-Party Reproduction

On 2026-07-16, the guide reproduced [`Step 3.7 Q3 QualityPlus`](https://huggingface.co/jcbtc/Step-3.7-Flash-ROCmFPX-Q3-QualityPlus) on the Beelink GTR9 Pro. [`StepFun`](https://github.com/stepfun-ai/Step-3.7-Flash) describes the model as a 198B sparse MoE with about 11B active parameters and 256K context. The tested package used 81.76GiB for the target and 85.22GiB for target, separate Q8 MTP draft, and templates together.

Read the raw evidence: [`data/raw/2026-07-16/step37-rocmfpx-q3-qualityplus/`](data/raw/2026-07-16/step37-rocmfpx-q3-qualityplus/)

Pinned route:

- target revision: `fa311ca5a82bf82a2338151c4790e3f659abd88d`
- draft revision: `c7bc8526b2b7004ce045112edebdf13a9eceb7eb`
- `ciru-ai/ROCmFPX`: `221402af8574faf652b101b6afe225a3f329561f`
- `Vulkan0`, one slot, Q8 KV, `n_max=2`, `p_min=0.75`, batch 8192, ubatch 2048

| Profile | Result | Acceptance |
| --- | ---: | ---: |
| 4,109-token no-spec baseline, three repeats | 23.84 t/s mean | n/a |
| 4,109-token MTP, three repeats | 34.50 t/s mean, **+44.68%** | 100.00% |
| 16,401-token MTP, three repeats | 33.83 t/s mean | 99.61% |
| 49,175-token MTP, one repeat | 28.06 t/s | 97.56% |

The target and draft also allocated the full 262,144-token context. A native tool-call smoke returned the requested `terminal` call with the exact `printf step37-ok` argument. The allocation result is not a filled-256K quality benchmark, and the 48K row has only one repeat.

This is valuable capacity and agent evidence: one 128GB Strix Halo box can hold a current 198B sparse target, its speculative draft, long-context KV headroom, and a working tool-call path. It remains an advanced pinned ROCmFPX route, not a beginner default or a direct `llama-bench` headline. Keep the separate Nimo and community Step 3.7 rows labeled as independent systems.

## First-Party Beelink Smoke

On 2026-06-21, the guide tested [`jcbtc/qwen3.6-35b-a3b-crown-halo-mtp-dynamic`](https://huggingface.co/jcbtc/qwen3.6-35b-a3b-crown-halo-mtp-dynamic) on the Beelink GTR9 Pro using a local `charlie12345/rocmfp4-llama` HIP-only build at commit `4795079b0`.

Read the raw evidence: [`data/raw/2026-06-21/rocmfp4-crown-halo-dynamic-mtp-smoke/`](data/raw/2026-06-21/rocmfp4-crown-halo-dynamic-mtp-smoke/)

What worked:

- model download and sha256 matched the model card
- HIP-only build succeeded through the existing `vllm-gfx1151` Distrobox / TheRock-style environment
- `llama-cli` loaded the model and generated with `draft-mtp`
- `llama-server` loaded target plus MTP draft context and served OpenAI-compatible responses
- server responses exposed timing and draft-acceptance metadata

What did not reproduce yet:

- ciru-ai's higher dynamic-MTP community speed band
- high draft acceptance on the guide's Beelink HIP-only path

Measured smoke rows:

| Run | Result |
| --- | ---: |
| short `llama-cli` MTP | 72.2 generation t/s |
| short `llama-cli` no-spec | 52.4 generation t/s |
| long structured `llama-cli` MTP | 51.1 generation t/s |
| long structured `llama-cli` no-spec | 49.9 generation t/s |
| short `llama-server`, `-sm row`, mmap | 60.66 predicted t/s, 76/152 draft tokens accepted |
| long structured `llama-server`, `-sm none`, `--no-mmap` | 57.61 predicted t/s, 168/344 draft tokens accepted |

Interpretation: this is a successful load/API/MTP smoke, not a new speed headline. The next useful step is to reproduce the newer dynamic runner/policy that ciru-ai described, preferably with exact model-card updates, runner commit, backend choice, prompt shapes, and acceptance policy.

## CHADROCK ACE/SABER Helper Repro

Also on 2026-06-21, the guide tested ciru-ai's corrected CHADROCK reproduction route for [`jcbtc/chadrock-35b-ace-saber-rocmfp4-mtp`](https://huggingface.co/jcbtc/chadrock-35b-ace-saber-rocmfp4-mtp).

Read the successful helper-route evidence: [`data/raw/2026-06-21/rocmfpx-chadrock-ace-saber-helper-repro/`](data/raw/2026-06-21/rocmfpx-chadrock-ace-saber-helper-repro/)

Earlier lower-speed attempt, kept for audit trail: [`data/raw/2026-06-21/rocmfpx-chadrock-ace-saber-repro-attempt/`](data/raw/2026-06-21/rocmfpx-chadrock-ace-saber-repro-attempt/)

Route:

- model file: `Qwen3.6-35B-A3B-NSC-ACE-SABER-MTP-F16-to-ROCmFP4-STRIX_LEAN.gguf`
- model sha256: `6a635d1d8ac4af8f2c4ca6ff528bc6bad9b3a6d45e8630ef6e5728f04898eeed`
- runner: `ciru-ai/ROCmFPX`
- runner commit: `deaa996dab90b3ca6dd3ae5d453bedfcd983012d`
- local build: `build-strix-rocmfp4` helper build from the pinned ROCmFPX tree
- device: `Vulkan0` / RADV STRIX_HALO
- request path: served `/completion` with request-level `speculative.n_max`, `speculative.n_min`, and `speculative.p_min`

What worked:

- the corrected helper runner built and launched locally through the ROCmFPX Strix build path
- the ACE/SABER ROCmFP4 GGUF sha matched the model-card hash
- `llama-server` loaded the model with `draft-mtp`
- OpenAI-compatible completion requests returned timing and draft-acceptance metadata
- the high-acceptance 3946-token / gen512 path reproduced locally

Measured rows:

| Run | Result |
| --- | ---: |
| 3946-token prompt, `n_max=4`, `p_min=0.25`, gen512 repeat 1 | 1071.04 prompt t/s / 140.40 predicted t/s, 408/408 draft tokens accepted |
| 3946-token prompt, `n_max=4`, `p_min=0.25`, gen512 repeat 2 | 1067.52 prompt t/s / 139.93 predicted t/s, 408/408 draft tokens accepted |
| 3946-token prompt, `n_max=4`, `p_min=0.25`, gen512 repeat 3 | 1048.90 prompt t/s / 114.95 predicted t/s, 386/467 draft tokens accepted |
| 3946-token prompt, `n_max=4`, `p_min=0.25`, gen2048 check | 1068.66 prompt t/s / 127.77 predicted t/s, 1595/1753 draft tokens accepted |

Interpretation: the high-speed CHADROCK path is real and reproduced locally when the helper runner, CHADROCK model, request-level speculative controls, and high-acceptance prompt shape line up. The third repeat and gen2048 check show why this should still be framed as an advanced, acceptance-sensitive server route rather than a default beginner claim.

For guide purposes, this is now strong positive evidence for the ROCmFP4/CHADROCK lane. It should still stay separate from direct `llama-bench` headline rows.

## 2026-07-16 Prompt-Shape Stability Profile

The same pinned runner and exact ACE/SABER model were retested across four prompt shapes with three repeats per shape. Every request generated 512 tokens at temperature zero with prompt caching disabled.

| Profile | Prompt tokens | Decode mean | Range | Mean draft acceptance |
| --- | ---: | ---: | ---: | ---: |
| Approx. 1K | 984 | 78.00 t/s | 75.36-80.67 | 41.93% |
| Exact reference | 3,946 | **141.37 t/s** | **140.84-141.79** | **100.00%** |
| Approx. 8K | 7,893 | 83.85 t/s | 79.31-86.14 | 51.28% |
| Approx. 16K | 15,787 | 107.23 t/s | 78.46-123.18 | 83.64% |

This confirms the highest reference shape more rigorously, but it also changes the recommendation: prompt length alone does not predict CHADROCK throughput. Draft acceptance and the generated-token pattern dominate. Operators should profile representative requests and treat 141.37 t/s as an exact repeat-confirmed profile, not as the speed of every 4K chat.

Raw requests, responses, acceptance rows, telemetry, hashes, and the harness are in [`data/raw/2026-07-16/rocmfpx-chadrock-stability-profile/`](data/raw/2026-07-16/rocmfpx-chadrock-stability-profile/).

## How To Use This In The Guide

Use ROCmFP4 / CHADROCK as:

- an advanced Strix Halo runtime lane
- community tuned-route evidence
- a possible bridge between raw benchmark rows and "best known settings per model"
- a source of vendor/reviewer questions about ROCm, NPU, IOMMU, and tuned GGUF support

Do not use it as:

- the beginner setup path
- a replacement for direct `llama-bench` Vulkan/RADV headline claims
- official AMD, OEM, or upstream `llama.cpp` performance evidence
- a universal recommendation before local reproduction

## Status

Status as of 2026-07-16: first-party Beelink load/API/MTP smoke succeeded for the Crown Halo dynamic artifact and the corrected CHADROCK ACE/SABER route. The follow-up CHADROCK stability profile showed that lower acceptance materially reduces speed. The separate Step 3.7 Q3 QualityPlus campaign is now complete: target plus draft fit, 4K/16K/48K served rows were measured, and 256K allocation plus native tool-call smokes passed.
