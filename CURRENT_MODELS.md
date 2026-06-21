# Current Model Triage

This page tracks fast-moving local-model targets that are useful for Strix Halo / Ryzen AI MAX+ 395 buyers, reviewers, and benchmark contributors.

It is not a leaderboard. The goal is to separate three questions that often get mixed together:

- Is the model current and interesting?
- Does it run locally on one 128 GB Strix Halo system?
- Is it fast, or is its value mainly capability, memory capacity, multimodality, or setup friction?

Measured rows below are first-party Beelink GTR9 Pro direct `llama-bench` Vulkan/RADV scouts unless stated otherwise. Normal workstation services were left running, so treat these as practical workstation scouts rather than cold/clean headline rows.

## Best Current Headline Rows

| Question | Best current row | Why it matters |
| --- | --- | --- |
| Fastest direct 30B-class Qwen MoE | Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`: 100.04 t/s direct `llama-bench` on b9467; latest b9544 control measured 103.18 tg128 r10 | Shows a direct 30B-class Qwen route can cross 100 t/s on Strix Halo. Keep separate from the Qwen3-Coder headline and balanced-default rows. |
| Fastest current small-MoE scout | LFM2.5 8B-A1B `Q4_K_M`: 170.02 t/s generation-only on the 2026-06-05 check; latest b9544 control measured 176.48 tg128 r10 | Shows how fast newer small active-parameter MoE routes can be. This is not a 30B-class capability replacement. |
| Largest current direct GGUF capacity route | Nemotron 3 Super 120B-A12B `UD-IQ4_XS`: 18.43 tg128 direct `llama-bench`; latest b9544 control measured 18.93 tg128 r3 | Proves a 120B-class MoE GGUF route can run directly on one box; value is capacity/currentness, not raw speed. |
| Fastest current-model MTP server route | CHADROCK ACE/SABER 35B ROCmFP4 through `ciru-ai/ROCmFPX`: 139.93-140.40 t/s gen512 on a 3946-token high-acceptance prompt; Gemma 4 26B-A4B QAT matched-head route remains the best six-prompt repeat at 110.00 t/s | Shows tuned ROCmFP4/MTP can be much faster than stock routes when draft acceptance is high. Keep separate from direct `llama-bench`; the CHADROCK row is advanced and prompt/acceptance-sensitive, while Gemma is the stronger broad repeat. |

## External Community Tuned Routes

ciru-ai's GMKtec EVO-X2 / NixOS / IOMMU-on artifact adds a separate current-model lane with ROCmFP4, Chadrock/Qwopus, Gemma QAT/MTP, CrownV7, and quality-eval rows. These are valuable because they connect Strix Halo speed to quality and NPU-sidecar workflows, but they are not first-party Beelink direct `llama-bench` rows.

The separate [`ROCMFP4_CHADROCK.md`](ROCMFP4_CHADROCK.md) page now tracks this as an advanced runtime lane. It is not the beginner/default setup path and should not be mixed with stock Vulkan/RADV headline claims. First-party Beelink smoke on 2026-06-21 confirmed that both the Crown Halo dynamic artifact and the corrected CHADROCK ACE/SABER route load and serve locally. The pinned ROCmFPX helper route reproduced a 139.93-140.40 t/s gen512 high-acceptance band on the Beelink system; longer/lower-acceptance repeats were slower.

| Route | Representative public result | Read |
| --- | ---: | --- |
| NPU sidecar | +3.29% main 64k iGPU latency with concurrent NPU load versus +68.96% with a comparable iGPU auxiliary load | Useful advanced IOMMU-on/NPU evidence; not a main iGPU replacement path. |
| Qwopus3.6 27B Chadrock | 0.9451 HumanEval+ and about 2.85x lower recorded request-generation time than the stored original Qwopus comparator | Strong tuned 27B quality-plus-speed evidence; keep as community served-route evidence. |
| Ace Saber 35B ROCmFP4 MTP | 0.9024 HumanEval+ in community data; first-party helper-route repro reached 140.40 and 139.93 predicted tok/s on gen512 high-acceptance repeats | Interesting high-quality 35B tuned-route evidence; local route works and the high-speed shape is reproducible when draft acceptance stays near 100%. |
| Gemma 4 26B-A4B QAT/MTP | 122.8 decode tok/s after TTFP on a 512-token API row and 0.9207 HumanEval+ | Strong current Google-model community route; keep separate from the first-party Gemma 4 26B QAT MTP repeat. |
| CrownV7 Qwen3.6 35B dynamic route | 515.33 tok/s prompt processing at 128k, 0.83 BFCL v4 non-live accuracy | Useful long-context and tool/function-calling signal. |
| Crown Halo Qwen3.6 35B dynamic MTP Beelink smoke | short server 60.66 predicted t/s with 76/152 accepted; long structured server 57.61 predicted t/s with 168/344 accepted | First-party load/API/MTP smoke succeeded, but high-speed dynamic-MTP behavior remains a reproduction target. |

First practical ROCmFP4/CHADROCK artifact candidates for local reproduction are around 13.8-21.0 GiB, which makes them much more testable than Kimi/GLM/MiniMax extreme-capacity routes.

Source: [`COMMUNITY_RESULTS.md#gmktec-evo-x2-nixos--npu--rocmfp4-evidence-package`](COMMUNITY_RESULTS.md#gmktec-evo-x2-nixos--npu--rocmfp4-evidence-package), [`data/community_ciru_evox2_metrics.csv`](data/community_ciru_evox2_metrics.csv), and [`ciru-ai/strix-halo-evo-x2-evidence`](https://github.com/ciru-ai/strix-halo-evo-x2-evidence).

## June 2026 Scout Results

| Model | Quant | Size class | Result | Read |
| --- | --- | ---: | ---: | --- |
| LFM2.5 8B-A1B | `Q4_K_M` | 5.1 GB / 8B.A1B | 3414.61 pp512 / 168.96 tg128; 170.02 tg128 generation-only on the 2026-06-05 int-dot rerun | Fastest new small-MoE result in this scout. Strong speed/currentness hook, but not a 30B-class capability comparison. |
| LFM2.5 8B-A1B | `Q4_K_M` | 5.1 GB / 8B.A1B | 3363.94 pp512 / 171.17 tg128 on ac4cddeb0 | Latest upstream control still keeps the small-MoE route in the 170 t/s class. |
| Nemotron 3 Nano 30B-A3B | `IQ4_XS` | 18.2 GB / 31B.A3.5B MoE | 1312.47 pp512 / 75.97 tg128 on the 2026-06-05 int-dot rerun | Practical NVIDIA Nemotron route for one Strix Halo system after the Nemotron 3 Ultra release. |
| Nemotron 3 Super 120B-A12B | `UD-IQ4_XS` | 64.5 GB / 120B.A12B MoE | 294.99 pp512 / 18.43 tg128 on the 2026-06-05 int-dot rerun | Missing middle Nemotron route: much larger than Nano, directly runnable as GGUF on one Strix Halo, but not a speed result. |
| Nemotron 3 Super 120B-A12B | `UD-IQ4_XS` | 64.5 GB / 120B.A12B MoE | 296.26 pp512 / 18.24 tg128 on ac4cddeb0 | Latest upstream control keeps the same capacity conclusion: runnable, useful, not fast. |
| Qwen3-30B-A3B-Instruct-2507 | `IQ4_XS` | 13.9 GB / 30B.A3B | 1430.65 pp512 / 100.38 tg128 on ac4cddeb0 | Latest upstream control keeps the separate direct 30B-class Qwen route above 100 t/s. |
| Qwen3-Coder 30B-A3B | `IQ4_XS` | 16.4 GB / 30B.A3B | 1372.27 pp512 / 90.44 tg128; 90.72 tg128 generation-only | Negative/control row: `IQ4_XS` alone did not beat the older Qwen3-Coder Q4_K_S 98.51 t/s headline. |
| Qwen3-Coder 30B-A3B | `Q4_K_S` | 17.5 GB / 30B.A3B | 1395.99 pp512 / 94.20 tg128 on ac4cddeb0 | Latest upstream control did not beat the older strict-clean 98.51 t/s speed-first headline. |
| Qwen3 30B-A3B NEO-MAX | `IQ4_XS` | 16.4 GB / 30B.A3B | 1396.05 pp512 / 87.39 tg128; 87.77 tg128 generation-only | Alternate 30B-A3B control row; the 2507 100 t/s result does not generalize to every 30B-A3B IQ4_XS file. |
| Qwen3.5 35B-A3B | `IQ4_XS` | 19.7 GB / 35B.A3B | 1170.27 pp512 / 75.22 tg128; 75.53 tg128 generation-only | Current/larger Qwen comparator; newer or larger is not automatically faster. |
| Qwen3.5 9B | `Q4_K_M` | 5.7 GB / 9B dense | 1015.35 pp512 / 34.49 tg128; 34.34 tg128 generation-only | Useful comparator for current Gemma-vs-Qwen discussion. Not the newest Qwen family. |
| Gemma 4 12B IT | `IQ4_XS` | 6.4 GB / 12B | 680.17 pp512 / 25.74 tg128; 25.77 tg128 generation-only | New Google model runs locally. Use for current-model/multimodal coverage, not speed. |
| Gemma 4 12B IT | `Q4_K_M` | 7.4 GB / 12B | 684.92 pp512 / 24.42 tg128; 24.42 tg128 generation-only | Balanced Gemma route. Slower than Qwen3.5 9B and much slower than Qwen 30B-class MoE speed rows. |
| Gemma 4 12B IT QAT | `UD-Q4_K_XL` | 6.7 GB / 12B | 816.32 pp512 / 29.34 tg128 direct on ac4cddeb0; MTP smoke reached 73.33 t/s | Better local Gemma 4 12B route than the earlier non-QAT direct rows, but the strongest value is the matched QAT MTP server path. |
| Gemma 4 26B-A4B IT QAT | `UD-Q4_K_XL` + matched `Q4_0` MTP head | 14.2 GB / 26B.A4B | 1431.96 pp512 / 74.80 tg128 direct; 73.96 t/s no-spec server; 110.00 t/s best MTP repeat; 107.42 t/s T3-only repeat; 102.69 t/s cold repeat | Highest-value new route in this update: current Google model, direct baseline, matched MTP speedup, and host-workload sensitivity evidence on the same Beelink box. |
| Qwen3.6 27B MTP NVFP4 v3 | `NVFP4` | 16.1 GB / 27B dense | 373.97 pp512 / 13.17 tg128 direct; server smoke 13.32 t/s no-spec and 24.37 t/s MTP | Newer Qwen3.6 artifact runs, but it is a negative speed control. Valuable because it prevents chasing the wrong route. |
| NVIDIA Nemotron 3 Nano Omni 30B-A3B Reasoning | `MXFP4_MOE` | 21.7 GB / 31B.A3.5B MoE | 1277.60 pp512 / 56.56 tg128 direct on official `llama.cpp` b9747 | Current NVIDIA Omni/FP4 route runs locally on the Beelink/RADV path. Useful model-support evidence, not a speed headline versus the earlier Nano IQ4_XS or Qwen/LFM rows. |
| MiniMax M2.7 | `UD-IQ4_XS` | 108.4 GB / 230B.A10B MoE | 101.00 pp512 / 28.27 tg128; 28.60 tg128 generation-only | Large-model feasibility proof: 230B-class MoE runs locally on one Strix Halo. Not a speed result. |
| DeepSeek V4 Flash | `Q2_K` / 0xSero Spark-Mini targets | 103.3 GB original target; 52.6 GB local Spark-Mini file | Original route download-blocked; later smaller 0xSero/Spark-Mini local file still failed to load in `llama-bench` smoke attempts | Strong setup-friction evidence. Do not list as pass, speed result, or hardware limit without a successful load. |
| Nemotron 3 Ultra 550B-A55B | GGUF dry-run / BF16 / NVFP4 targets | 188.0 GB smallest scanned GGUF route; 1.1 TB BF16 / 352.4 GB NVFP4 | Artifact scan only | GGUF artifacts now exist, but the smallest scanned route is still too large for a practical one-box 128 GB Strix Halo internal-disk benchmark. |

## 2026-06-07 b9544 Regression Control

This checked whether current `llama.cpp` b9544 regresses the guide's most important direct Vulkan/RADV sentinel rows. It used explicit `-dev Vulkan0`; automatic-device dry runs selected CPU and were discarded before publishing.

| Model | Quant | Build | Result | Read |
| --- | --- | --- | ---: | --- |
| Qwen3-30B-A3B-Instruct-2507 | `IQ4_XS` | b9544 `98d5e8ba8` | 1438.10 pp512 / 103.18 tg128 r10 | Latest build still keeps the direct 30B-class Qwen route above 100 t/s. |
| Qwen3-Coder 30B-A3B | `Q4_K_S` | b9544 `98d5e8ba8` | 1406.45 pp512 / 98.02 tg128 r50; 98.49 tg128 generation-only p0/n128 r20 | Exact SHA-matched speed-first file rerun. It reproduces the older 98 t/s class but does not beat the b9179 98.51 t/s headline. |
| Qwen3-Coder 30B-A3B | `UD-Q4_K_XL` | b9544 `98d5e8ba8` | 1399.98 pp512 / 97.08 tg128 r5 | Balanced coding row remains in the 96-97 t/s class. |
| LFM2.5 8B-A1B | `Q4_K_M` | b9544 `98d5e8ba8` | 3398.36 pp512 / 176.48 tg128 r10 | No latest-build regression in the current small-MoE speed route. |
| Nemotron 3 Super 120B-A12B | `UD-IQ4_XS` | b9544 `98d5e8ba8` | 297.14 pp512 / 18.93 tg128 r3 | No latest-build regression in the 120B-class direct GGUF capacity route. |

Raw evidence:

- Gemma 4 12B: [`data/raw/2026-06-04/gemma-4-12b-it-direct-scout/`](data/raw/2026-06-04/gemma-4-12b-it-direct-scout/)
- Nimo Gemma 4 QAT/MTP follow-up: [`data/raw/2026-06-06/community-nimo-gemma4-qat-issue4/`](data/raw/2026-06-06/community-nimo-gemma4-qat-issue4/)
- Qwen3.5 9B comparator: [`data/raw/2026-06-04/qwen35-9b-q4km-direct-comparator/`](data/raw/2026-06-04/qwen35-9b-q4km-direct-comparator/)
- LFM2.5 8B-A1B: [`data/raw/2026-06-04/lfm25-8b-a1b-q4km-direct-scout/`](data/raw/2026-06-04/lfm25-8b-a1b-q4km-direct-scout/)
- Nemotron 3 Nano 30B-A3B: [`data/raw/2026-06-04/nemotron-3-nano-30b-a3b-iq4xs-direct-scout/`](data/raw/2026-06-04/nemotron-3-nano-30b-a3b-iq4xs-direct-scout/)
- Nemotron 3 Super 120B-A12B: [`data/raw/2026-06-04/nemotron-3-super-120b-a12b-udiq4xs-direct-scout/`](data/raw/2026-06-04/nemotron-3-super-120b-a12b-udiq4xs-direct-scout/)
- 2026-06-05 latest/int-dot rerun for LFM2.5, Nemotron Nano, Nemotron Super, Qwen3-30B-A3B-Instruct-2507, and Qwen3-Coder UD: [`data/raw/2026-06-05/latest-llamacpp-intdot-regression/`](data/raw/2026-06-05/latest-llamacpp-intdot-regression/)
- 2026-06-07 `llama.cpp` b9544 regression control for Qwen3-30B-A3B-Instruct-2507, Qwen3-Coder UD, LFM2.5, and Nemotron Super: [`data/raw/2026-06-07/latest-llamacpp-b9544-regression/`](data/raw/2026-06-07/latest-llamacpp-b9544-regression/)
- 2026-06-07 exact Qwen3-Coder `Q4_K_S` b9544 refresh: [`data/raw/2026-06-07/qwen3-coder-q4ks-b9544-refresh/`](data/raw/2026-06-07/qwen3-coder-q4ks-b9544-refresh/)
- 2026-06-11 latest `llama.cpp` ac4cddeb0 Vulkan/RADV direct controls for Qwen3-30B-A3B-Instruct-2507, Qwen3-Coder Q4_K_S, LFM2.5, Gemma 4 QAT, Nemotron Super, and Qwen3.6 27B NVFP4: [`data/raw/2026-06-11/latest-llamacpp-ac4cddeb-vulkan-clean/`](data/raw/2026-06-11/latest-llamacpp-ac4cddeb-vulkan-clean/)
- 2026-06-11 Gemma 4 26B-A4B QAT six-prompt MTP sweep and best repeat: [`data/raw/2026-06-11/gemma4-26b-qat-mtp-sixprompt-ac4cddeb/`](data/raw/2026-06-11/gemma4-26b-qat-mtp-sixprompt-ac4cddeb/)
- 2026-06-12 Gemma 4 26B-A4B QAT cold repeat after pausing nonessential local workload while leaving T3 and Hermes untouched: [`data/raw/2026-06-12/gemma4-26b-qat-mtp-cold-repeat-ac4cddeb/`](data/raw/2026-06-12/gemma4-26b-qat-mtp-cold-repeat-ac4cddeb/)
- 2026-06-12 Gemma 4 26B-A4B QAT T3-only repeat after pausing Hermes/Ollama/RustDesk/docflock/VM/browser-class noise while leaving T3 running: [`data/raw/2026-06-12/gemma4-26b-qat-mtp-t3-only-repeat-ac4cddeb/`](data/raw/2026-06-12/gemma4-26b-qat-mtp-t3-only-repeat-ac4cddeb/)
- 2026-06-21 Nemotron 3 Nano Omni MXFP4_MOE direct b9747 smoke: [`data/raw/2026-06-21/nemotron-3-nano-omni-mxfp4-b9747-smoke/`](data/raw/2026-06-21/nemotron-3-nano-omni-mxfp4-b9747-smoke/)
- Qwen3-Coder IQ4_XS control: [`data/raw/2026-06-03/qwen3-coder-iq4xs-direct-scout/`](data/raw/2026-06-03/qwen3-coder-iq4xs-direct-scout/)
- Qwen3 30B-A3B NEO-MAX IQ4_XS control: [`data/raw/2026-06-03/qwen3-30b-a3b-neo-max-iq4xs-direct-scout/`](data/raw/2026-06-03/qwen3-30b-a3b-neo-max-iq4xs-direct-scout/)
- Qwen3.5 35B-A3B IQ4_XS control: [`data/raw/2026-06-03/qwen35-35b-a3b-iq4xs-direct-scout/`](data/raw/2026-06-03/qwen35-35b-a3b-iq4xs-direct-scout/)
- MiniMax M2.7: [`data/raw/2026-06-03/minimax-m27-ud-iq4xs-local-smoke/`](data/raw/2026-06-03/minimax-m27-ud-iq4xs-local-smoke/)
- DeepSeek V4 Flash attempt: [`data/raw/2026-06-03/deepseek-v4-flash-q2k-download-attempt/`](data/raw/2026-06-03/deepseek-v4-flash-q2k-download-attempt/)
- DeepSeek V4 Flash 0xSero/Spark-Mini load failure: [`data/raw/2026-06-05/deepseek-v4-flash-0xsero-load-failure/`](data/raw/2026-06-05/deepseek-v4-flash-0xsero-load-failure/)
- Large-model feasibility scan: [`data/raw/2026-06-03/large-model-feasibility-scan/`](data/raw/2026-06-03/large-model-feasibility-scan/)
- Triage notes: [`data/raw/2026-06-04/latest-model-viral-scan/`](data/raw/2026-06-04/latest-model-viral-scan/), [`data/raw/2026-06-05/model-update-scan/`](data/raw/2026-06-05/model-update-scan/)

## Related Controls Already Covered Elsewhere

These rows are useful for context, but they are not promoted as new headline claims:

| Route | Result | Why it stays secondary |
| --- | ---: | --- |
| Qwen3-Coder-Next 80B-A3B `IQ4_XS` direct | 61.91 tg128 / 738.98 pp512 | Modern coding-model row for currentness. It is useful, but not a speed replacement for the 30B Qwen rows. |
| Qwen3.6 35B-A3B MTP repeat | 97.08 t/s six-prompt mean; 106.24 t/s max | Confirms code prompts can cross 100 t/s, but broad repeat average did not reproduce the earlier 101.1 t/s run. Keep as server/speculative evidence. |
| Qwen3-Coder 30B high-power policy check | 95.18 tg128 auto policy, 96.37 tg128 high policy | Shows power policy can help this Beelink run, but did not reproduce the tuned external GMKtec 100 t/s report. |
| Qwen3.6 27B dense Q8 control | 7.70 tg128 direct follow-up | Useful response to model requests, but this dense Q8 route is not a speed candidate versus the 35B-A3B MoE paths. |
| Qwen3.6 27B MTP NVFP4 v3 | 13.17 tg128 direct; 24.37 t/s MTP smoke | Newer artifact and lower footprint than Q8, but still a negative speed route versus Qwen3.6 35B-A3B and Gemma 4 26B QAT MTP. |
| Gemma 4 26B-A4B QAT direct baseline | 74.80 tg128 direct `llama-bench`; MTP repeats measured 102.69 t/s cold, 107.42 t/s T3-only, and 110.00 t/s best-repeat | Useful current-model baseline for the MTP server route; not itself a speed headline. |

Raw evidence:

- Qwen3-Coder-Next and MTP repeat: [`data/raw/2026-06-02/modern-model-clean-followup/`](data/raw/2026-06-02/modern-model-clean-followup/)
- High-power policy check: [`data/raw/2026-06-02/high-power-policy-test/`](data/raw/2026-06-02/high-power-policy-test/)
- Qwen3.6 27B dense follow-up: [`data/raw/2026-06-02/reddit-look-int-dot-reproduction/`](data/raw/2026-06-02/reddit-look-int-dot-reproduction/)
- Latest Gemma/Qwen/Nemotron/LFM controls: [`data/raw/2026-06-11/latest-llamacpp-ac4cddeb-vulkan-clean/`](data/raw/2026-06-11/latest-llamacpp-ac4cddeb-vulkan-clean/)
- Gemma 4 26B-A4B QAT MTP route: [`data/raw/2026-06-11/gemma4-26b-qat-mtp-sixprompt-ac4cddeb/`](data/raw/2026-06-11/gemma4-26b-qat-mtp-sixprompt-ac4cddeb/), [`cold repeat`](data/raw/2026-06-12/gemma4-26b-qat-mtp-cold-repeat-ac4cddeb/), [`T3-only repeat`](data/raw/2026-06-12/gemma4-26b-qat-mtp-t3-only-repeat-ac4cddeb/)

## What This Means

### Speed

For text generation speed, model architecture dominates. LFM2.5 8B-A1B is much faster than Gemma 4 12B in this scout because it is a small active-parameter MoE route. This does not mean it replaces larger coding or reasoning models.

The existing Qwen 30B-class rows remain the stronger 30B speed story:

- Qwen3-Coder 30B-A3B `Q4_K_S`: 98.51 t/s direct first-party Beelink headline.
- Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`: 100.04 t/s direct first-party scout on b9467; 99.10 t/s generation-only on the 2026-06-05 latest/int-dot rerun; 103.18 tg128 on the 2026-06-07 b9544 regression control.

Keep those separate from small-model speed results.

### Currentness

Gemma 4 12B is the strongest current-model brand hook in this scout. The practical result is not "Gemma is fastest"; it is "a newly released Google local model runs on Strix Halo, and the guide can show exactly how it compares."

The Nimo community follow-up adds a second Gemma 4 lesson for QAT/server users: matched QAT MTP assistant heads can materially improve single-stream decode and acceptance on Gemma 4 12B, 26B-A4B, and 31B QAT Q4_0 rows. Atomic PR #26 later fixed the Gemma 4 MTP `PARALLEL=2` crash upstream, so the useful next community evidence is fresh post-merge 1-slot and 2-slot numbers with exact Atomic commit, command, acceptance, single-stream decode, and aggregate throughput. Keep this separate from first-party direct `llama-bench` rows.

The first-party Beelink update adds the missing local counterpart: Gemma 4 26B-A4B QAT runs directly at 74.80 tg128, then the matched MTP head lifts `llama-server` from a 73.96 t/s no-spec six-prompt baseline to 102.69 t/s cold repeat, 107.42 t/s T3-only repeat, and 110.00 t/s best repeat. This is now the strongest current-model server route in the guide, but it is still a server/speculative result rather than a direct benchmark replacement.

Qwen3.5 9B is useful only as a community-discussion comparator. For current Qwen framing, prefer the existing Qwen3.6 rows in this guide.

### Capacity

MiniMax M2.7 is the best current evidence that 128 GB unified memory changes what a mini PC can attempt. A 108 GB GGUF route loaded and generated locally. That is valuable for buyers even though it is not fast.

DeepSeek V4 Flash shows a different adoption blocker: one route was blocked by 100GB+ download/resume friction, while a later smaller 0xSero/Spark-Mini local file still failed during `llama-bench` load. That is not a hardware speed result, but it is valuable adoption-friction evidence.

Nemotron 3 Ultra shows the same pattern at a larger scale. The new Ultra release is important, and a GGUF route was found in the 2026-06-05 follow-up scan. The smallest scanned Ultra GGUF route was still about 188 GB, so it remains a watchlist/external-storage/multi-node target rather than a practical one-box 128 GB Strix Halo benchmark. The practical NVIDIA family map is now: Ultra as watchlist, Super 120B-A12B as the larger direct GGUF capacity route, and Nano 30B-A3B as the faster practical route.

## Good Post Hooks

- "LFM2.5 8B-A1B at 170 t/s generation-only on Strix Halo: new small-MoE models are a different speed class."
- "Google Gemma 4 12B runs locally on Strix Halo, but Qwen/LFM are faster for text-only generation."
- "Gemma 4 26B-A4B QAT with matched MTP head: 110.0 t/s best-repeat on Strix Halo as a local server route."
- "Current model reality check: newest does not automatically mean fastest."
- "A 230B-class MiniMax MoE runs locally on one 128 GB Strix Halo system, but speed and capacity are different wins."
- "NVIDIA Nemotron 3 Ultra just dropped; on one 128 GB Strix Halo, Super 120B-A12B is the runnable middle route and Nano 30B-A3B is the faster route."
- "Nemotron 3 Super 120B-A12B runs directly on Strix Halo: 295.0 pp512 / 18.4 tg128 via `llama.cpp` Vulkan/RADV."
- "The hidden local-AI friction is not just GPU speed. It is model format, quant choice, download size, backend support, and reproducible commands."

## Guide Value To Add

The most useful public addition is not another single headline number. It is a repeatable "current model triage" workflow:

1. Check whether the model has official or credible GGUF artifacts.
2. Record artifact size, architecture, context length, and quant options before downloading.
3. Run one balanced quant and one speed/footprint quant when available.
4. Keep speed rows, large-model load proofs, MTP/server rows, and download-blocked attempts separate.
5. Explain what buyer uncertainty the result removes: speed, currentness, capacity, setup path, or distribution friction.

This helps buyers and vendors because it turns "can this AI PC run the latest models?" into dated, reproducible evidence instead of scattered social screenshots.

The Nemotron 3 Super row is also an example of the community feedback loop documented in [`COMMUNITY_FEEDBACK.md`](COMMUNITY_FEEDBACK.md): a public correction identified a missing route, and the guide added a measured result instead of leaving the original framing unchanged.

## Highest-Value Next Tests

These are prioritized for buyer/vendor guide value, not social-media hooks:

| Priority | Test | Why it adds guide value |
| ---: | --- | --- |
| 1 | ROCmFP4 / CHADROCK stability follow-up from [`ROCMFP4_CHADROCK.md`](ROCMFP4_CHADROCK.md) | The helper route now reproduces ~140 t/s gen512 on a high-acceptance prompt. Next value is a cleaner multi-prompt profile: when does it stay near 140, when does it fall back toward 115-128, and which prompt/model profiles should users actually choose? |
| 2 | Ollama 0.30.10 Linux sanity check for one default chat model and one 30B-class MoE | Ollama is the easiest buyer path. Version drift matters more to typical users than another raw `llama-bench` row. |
| 3 | `llama.cpp` b9747 sentinel check for the current direct headline rows | Official b9747 Vulkan binary already ran the Nemotron Omni smoke cleanly. Next value is a sentinel rerun for Qwen3-30B-A3B-Instruct-2507, Qwen3-Coder Q4_K_S, LFM2.5, and Nemotron Super if the exact model files are restored locally. |
| 4 | Nemotron 3 Nano Omni NVFP4 or quality/multimodal follow-up | MXFP4_MOE now has a direct b9747 smoke pass at 56.56 tg128. A follow-up only matters if it compares NVFP4/MXFP4 quality, multimodal/mmproj behavior, or an easier recommended route. |
| 5 | DeepSeek V4 Flash REAP 47 GiB loadability follow-up | Smaller than the earlier 100GB+ DeepSeek routes and directly answers whether the previous blocker was artifact/runtime support rather than hardware capacity. |
| 6 | External-storage feasibility plan for Kimi-K2.7-Code, GLM-5.2, MiniMax-M3, and Nemotron Ultra class routes | These are high-traffic model names, but most artifacts are 120-300GB+. A clean external NVMe plan is more valuable than pretending they are simple internal-disk tests. |

## Watch List

| Target | Status |
| --- | --- |
| Qwen3.6 new quants/sources | Already important in the guide. Add only if a new source answers a new question. |
| Kimi-K2.7-Code | Very high viral value and active GGUF ecosystem. Smallest scanned routes remain huge: AesSedai `IQ2_XXS` about 262.8 GiB, Unsloth `UD-IQ1_M` about 283.0 GiB, and a pruned `deep55` route about 188.7 GiB. Treat as external-storage/watchlist, not a quick local default. |
| GLM-5.2 | Very high viral value. Unsloth GGUF exists with smallest scanned `UD-IQ1_S` about 201.8 GiB; REAP50 Q2 route scanned at 129.4 GiB; MXFP4/NVFP4 routes are about 400GB+. External-storage/watchlist unless a smaller compatible route appears. |
| MiniMax M3 | GGUF routes now exist, but smallest scanned Unsloth route is about 119.6 GiB and practical quants are much larger. Treat as watchlist/runtime-support route, not proven local guidance. |
| Nemotron 3 Nano Omni NVFP4/MXFP4 | MXFP4_MOE now has a first-party direct b9747 smoke pass at 1277.60 pp512 / 56.56 tg128. Good current NVIDIA Omni/FP4 support evidence; do not promote as a speed headline. NVFP4/mmproj remains a possible follow-up if it answers a multimodal or quality question. |
| DeepSeek V4 Flash | Original 103GB route was download-blocked; smaller 0xSero/Spark-Mini route reached local load attempts but failed before benchmarking. New REAP Q2 route scanned at 47.0 GiB, making loadability worth revisiting before claiming performance. |
| Nemotron 3 Ultra 550B-A55B | GGUF route found in the 2026-06-05 scan, but the smallest scanned route is about 188 GB. Watch for smaller practical artifacts or test only with external storage / multi-node planning. |
| Nemotron 3 Super 120B-A12B | Tested with `UD-IQ4_XS`. Add lower/higher quant comparisons only if they answer a specific buyer question. |
| `llama.cpp` b9747 | Latest release observed 2026-06-21. The official Vulkan binary ran the Nemotron Omni smoke cleanly; direct headline sentinel reruns still require restoring the exact local model files. |
| Ollama 0.30.10 | Latest release observed 2026-06-17. Useful for buyer-path sanity checks because Ollama is the easiest local chat route. |

## Sources

- Google Gemma 4 12B announcement: <https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12b/>
- Gemma 4 12B GGUF: <https://huggingface.co/ggml-org/gemma-4-12B-it-GGUF>
- Gemma 4 12B GGUF: <https://huggingface.co/unsloth/gemma-4-12b-it-GGUF>
- LFM2.5 8B-A1B GGUF: <https://huggingface.co/LiquidAI/LFM2.5-8B-A1B-GGUF>
- Qwen3.5 9B GGUF: <https://huggingface.co/unsloth/Qwen3.5-9B-GGUF>
- Nemotron 3 Nano 30B-A3B GGUF: <https://huggingface.co/unsloth/Nemotron-3-Nano-30B-A3B-GGUF>
- Nemotron 3 Super 120B-A12B GGUF: <https://huggingface.co/unsloth/NVIDIA-Nemotron-3-Super-120B-A12B-GGUF>
- Nemotron 3 Ultra 550B-A55B GGUF: <https://huggingface.co/unsloth/NVIDIA-Nemotron-3-Ultra-550B-A55B-GGUF>
- Nemotron 3 Ultra BF16: <https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16>
- Nemotron 3 Ultra NVFP4: <https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-NVFP4>
- ROCmFP4 / CHADROCK route: <https://github.com/charlie12345/rocmfp4-llama>
- Kimi-K2.7-Code GGUF: <https://huggingface.co/unsloth/Kimi-K2.7-Code-GGUF>
- GLM-5.2 GGUF: <https://huggingface.co/unsloth/GLM-5.2-GGUF>
- MiniMax-M3 GGUF: <https://huggingface.co/unsloth/MiniMax-M3-GGUF>
- Nemotron 3 Nano Omni MXFP4 GGUF: <https://huggingface.co/unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-GGUF>
- Nemotron 3 Nano Omni NVFP4 GGUF: <https://huggingface.co/FreedomAISVR/Nemotron-3-30B-Nano-Omni-NVFP4-GGUF>
- DeepSeek V4 Flash REAP Q2 GGUF: <https://huggingface.co/sleepyeldrazi/deepseek-v4-flash-reap-k128-Q2-GGUF>
- `llama.cpp` b9747: <https://github.com/ggml-org/llama.cpp/releases/tag/b9747>
- Ollama 0.30.10: <https://github.com/ollama/ollama/releases/tag/v0.30.10>
