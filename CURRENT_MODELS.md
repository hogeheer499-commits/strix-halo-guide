# Current Model Triage

This page tracks fast-moving local-model targets that are useful for Strix Halo / Ryzen AI MAX+ 395 buyers, reviewers, and benchmark contributors.

For tools and contributors, the prioritized queue below is also available as [`data/current_test_queue.csv`](data/current_test_queue.csv). That file tracks candidates and blockers; it is deliberately separate from the measured-only [`data/best_known_profiles.csv`](data/best_known_profiles.csv).

It is not a leaderboard. The goal is to separate three questions that often get mixed together:

- Is the model current and interesting?
- Does it run locally on one 128 GB Strix Halo system?
- Is it fast, or is its value mainly capability, memory capacity, multimodality, or setup friction?

Measured rows below are first-party Beelink GTR9 Pro direct `llama-bench` Vulkan/RADV scouts unless stated otherwise. Normal workstation services were left running, so treat these as practical workstation scouts rather than cold/clean headline rows.

## Best Current Headline Rows

| Question | Best current row | Why it matters |
| --- | --- | --- |
| Fastest direct 30B-class Qwen MoE | Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`: 100.04 t/s direct `llama-bench` on b9467; latest b9544 control measured 103.18 tg128 r10 | Shows a direct 30B-class Qwen route can cross 100 t/s on Strix Halo. Keep separate from the Qwen3-Coder headline and balanced-default rows. |
| Fastest direct Qwen3-Coder speed-first row | Qwen3-Coder 30B-A3B `Q4_K_S`: 100.99 t/s direct `llama-bench` on the official `llama.cpp` b9851 Ubuntu Vulkan release binary | First first-party Qwen3-Coder row above 100 t/s. Keep scoped as a speed-first quant, not the balanced default; the older b9179 strict-clean 98.51 t/s row remains useful historical context. |
| Fastest current small-MoE scout | LFM2.5 8B-A1B `Q4_K_M`: 170.02 t/s generation-only on the 2026-06-05 check; latest b9544 control measured 176.48 tg128 r10 | Shows how fast newer small active-parameter MoE routes can be. This is not a 30B-class capability replacement. |
| Largest current direct GGUF capacity route | Nemotron 3 Super 120B-A12B `UD-IQ4_XS`: 18.43 tg128 direct `llama-bench`; latest b9544 control measured 18.93 tg128 r3 | Proves a 120B-class MoE GGUF route can run directly on one box; value is capacity/currentness, not raw speed. |
| Fastest current-model MTP server route | CHADROCK ACE/SABER 35B ROCmFP4 through `ciru-ai/ROCmFPX`: 139.93-140.40 t/s gen512 on a 3946-token high-acceptance prompt; Gemma 4 26B-A4B QAT matched-head route remains the best six-prompt repeat at 110.00 t/s | Shows tuned ROCmFP4/MTP can be much faster than stock routes when draft acceptance is high. Keep separate from direct `llama-bench`; the CHADROCK row is advanced and prompt/acceptance-sensitive, while Gemma is the stronger broad repeat. |
| Current Ollama system-service buyer path | Qwen3.6 35B-A3B through Ollama 0.31.2: 60.57 t/s warm API generation mean on Vulkan/RADV; Qwen2.5-VL 7B vision smoke passed | This is the normal installed-service path, not a direct `llama-bench` headline. The separate user-local 0.31.1 check remains faster at 71.82 t/s, so 0.31.2 is a compatibility/currentness pass with a measured speed regression. Requires `OLLAMA_IGPU_ENABLE=1`. |

## External Community Tuned Routes

ciru-ai's GMKtec EVO-X2 / NixOS / IOMMU-on artifact adds a separate current-model lane with ROCmFP4, Chadrock/Qwopus, Gemma QAT/MTP, CrownV7, and quality-eval rows. These are valuable because they connect Strix Halo speed to quality and NPU-sidecar workflows, but they are not first-party Beelink direct `llama-bench` rows.

The separate [`ROCMFP4_CHADROCK.md`](ROCMFP4_CHADROCK.md) page now tracks this as an advanced runtime lane. It is not the beginner/default setup path and should not be mixed with stock Vulkan/RADV headline claims. First-party Beelink smoke on 2026-06-21 confirmed that both the Crown Halo dynamic artifact and the corrected CHADROCK ACE/SABER route load and serve locally. The pinned ROCmFPX helper route reproduced a 139.93-140.40 t/s gen512 high-acceptance band on the Beelink system; longer/lower-acceptance repeats were slower.

| Route | Representative public result | Read |
| --- | ---: | --- |
| NPU sidecar | +3.29% main 64k iGPU latency with concurrent NPU load versus +68.96% with a comparable iGPU auxiliary load | Useful advanced IOMMU-on/NPU evidence; not a main iGPU replacement path. |
| Qwopus3.6 27B Chadrock | 0.9451 HumanEval+ and about 2.85x lower recorded request-generation time than the stored original Qwopus comparator | Strong tuned 27B quality-plus-speed evidence; keep as community served-route evidence. |
| Ace Saber 35B ROCmFP4 MTP | 0.9024 HumanEval+ in community data; first-party helper-route repro reached 140.40 and 139.93 predicted tok/s on gen512 high-acceptance repeats | Interesting high-quality 35B tuned-route evidence; local route works and the high-speed shape is reproducible when draft acceptance stays near 100%. |
| Gemma 4 26B-A4B QAT/MTP | 122.8 decode tok/s after TTFP on a 512-token API row and 0.9207 HumanEval+ | Strong current Google-model community route; keep separate from the first-party Gemma 4 26B QAT MTP repeat. |
| StepFun Step-3.7-Flash ROCmFPX Q3 QualityPlus | 81.77GiB target shards; community card reports 29.39 t/s at 4k MTP, 85/100 on HermesAgent-20 at 35.31 t/s, and a 256k target-plus-draft load proof | High-value 198B-class capacity/agent target built for 128GB Strix Halo. Requires the pinned ROCmFPX runner and a separate Q8 MTP draft; first-party Beelink reproduction is still pending. |
| CrownV7 Qwen3.6 35B dynamic route | 515.33 tok/s prompt processing at 128k, 0.83 BFCL v4 non-live accuracy | Useful long-context and tool/function-calling signal. |
| Crown Halo Qwen3.6 35B dynamic MTP Beelink smoke | short server 60.66 predicted t/s with 76/152 accepted; long structured server 57.61 predicted t/s with 168/344 accepted | First-party load/API/MTP smoke succeeded, but high-speed dynamic-MTP behavior remains a reproduction target. |

First practical ROCmFP4/CHADROCK artifact candidates for local reproduction are around 13.8-21.0 GiB, which makes them much more testable than Kimi/GLM/MiniMax extreme-capacity routes.

Source: [`COMMUNITY_RESULTS.md#gmktec-evo-x2-nixos--npu--rocmfp4-evidence-package`](COMMUNITY_RESULTS.md#gmktec-evo-x2-nixos--npu--rocmfp4-evidence-package), [`data/community_ciru_evox2_metrics.csv`](data/community_ciru_evox2_metrics.csv), and [`ciru-ai/strix-halo-evo-x2-evidence`](https://github.com/ciru-ai/strix-halo-evo-x2-evidence).

## July 2026 Runtime Controls

Latest observed upstream releases as of 2026-07-15 are `llama.cpp` b10012, Ollama 0.32.0, and ROCm 7.2.4. The latest measured first-party baselines remain b9979 and Ollama 0.31.2. b10005 introduced native Vulkan E2M1/E4M3 conversion support relevant to MXFP4/NVFP4 and initial Hy3/MTP support; b10012 contains those changes, while the seven intervening commits are server/UI/OpenCL/Hexagon maintenance rather than a new Vulkan inference-kernel claim. Ollama 0.32.0 is primarily an agent/CLI integration release, so it does not replace the measured 0.31.2 buyer path without a local regression check.

| Model / route | Quant | Tool | Result | Read |
| --- | --- | --- | ---: | --- |
| Qwen3-Coder 30B-A3B concurrency repeats | `UD-Q4_K_XL`, Q4_0 KV, 128 experts/top-8 | official b9979 stock vs opt-in AMD/RADV density gate | np9 mean: 147.19 t/s stock, 210.07 density, 234.12 density+dense16; five repeats | Density recovers 42.7% at np9 without changing np8. Dense16 reaches +59.1% at np9 but regresses versus density alone at np16, so it is not a universal default. |
| Qwen3-Next 80B-A3B concurrency repeats | `UD-Q4_K_XL`, Q4_0 KV, 512 experts/top-10 | official b9979 stock vs opt-in AMD/RADV density gate | np9 mean: 100.15 t/s stock, 125.48 density, 142.72 density+dense16; three repeats | Confirms the dispatch cliff and recovery on the many-expert/top-10 shape; same caveat about dense16 at np16. |
| 30B/80B backend crossover | same workloads | b9979 Vulkan modes vs Lemonade ROCm b1259 | 30B ROCm leads at np16 with 287.64 t/s; 80B density Vulkan leads at np16 with 150.82 t/s | Backend choice depends on the model topology and target concurrency. There is no universal batching winner. |
| Qwen3-Coder 30B-A3B concurrency sweep | `UD-Q4_K_XL`, Q4_0 KV | official `llama.cpp` b9946 Vulkan | Aggregate decode 214.23 t/s at np8, 143.05 at np9, and 321.97 at np32 | Reproduces the issue #25356 8-to-9 cliff on a same-family local artifact. |
| Qwen3-Coder 30B-A3B concurrency sweep | same artifact and workload | b9946 Vulkan with flat threshold patch | Aggregate decode 202.73 t/s at np8, 195.38 at np9, and 321.02 at np32 | Experimental 8-to-16 / 8-to-32 cutoff patch removes most of the cliff, but is not the later density-gate design; one sweep reached 98 C sysfs temperature, so this is not default guidance. |
| Qwen3-Coder 30B-A3B concurrency sweep | same artifact and workload | Lemonade ROCm b1259 | Aggregate decode 184.93 t/s at np8, 191.24 at np9, and 354.59 at np32 | No 8-to-9 cliff and strongest np32 comparator in this sweep. Official ROCm b9946 was much slower. |
| Qwen3.6 35B-A3B | `Q4_K_M` Ollama model | Ollama 0.31.2 system service, Vulkan/RADV API | 60.57 t/s warm generation mean; 60.00-61.22 t/s warm range | Current buyer-path pass with full iGPU offload, vision smoke, service restart, and full-host-reboot persistence. Slower than the separate 0.31.1 user-local 71.82 t/s run. |
| Qwen3.6 35B-A3B | `Q4_K_M` Ollama model | Ollama 0.31.1 local binary, Vulkan/RADV API | 71.82 t/s warm generation mean; 71.62-72.05 t/s warm range | Strong buyer-path update. Ollama 0.31.1 works on the measured Beelink system, but `OLLAMA_IGPU_ENABLE=1` is required to keep the Strix Halo iGPU active. |
| Qwen3-Coder 30B-A3B | `Q4_K_S` | official `llama.cpp` b9888 Vulkan | 1404.73 pp512 / 98.12 tg128 r50; 98.59 tg128 generation-only | Latest official runtime sentinel. Works cleanly and reproduces the 98 t/s class, but does not replace the b9851 100.99 t/s speed-first headline. |
| Qwen3-Coder 30B-A3B | `UD-Q4_K_XL` | official `llama.cpp` b9888 Vulkan | 1410.82 pp512 / 96.53 tg128 r5 | Balanced coding quant latest-runtime control. |
| Qwen3-Coder 30B-A3B | `Q4_K_S` | official `llama.cpp` b9859 Vulkan | 1413.38 pp512 / 98.48 tg128 r50; 99.09 tg128 generation-only | Current-runtime control. Reproduces the 98-99 t/s class but does not replace the b9851 100.99 t/s speed-first headline. |
| Qwen3-Coder 30B-A3B | `UD-Q4_K_XL` | official `llama.cpp` b9859 Vulkan | 1411.76 pp512 / 97.01 tg128 r5 | Balanced current-runtime control. |
| Gemma 4 26B-A4B IT | `UD-Q4_K_M` | official `llama.cpp` b9859 Vulkan | 1323.39 pp512 / 54.18 tg128 r5 | Direct Gemma control remains secondary to the Gemma QAT/MTP server route. |

## June 2026 Scout Results

| Model | Quant | Size class | Result | Read |
| --- | --- | ---: | ---: | --- |
| LFM2.5 8B-A1B | `Q4_K_M` | 5.1 GB / 8B.A1B | 3414.61 pp512 / 168.96 tg128; 170.02 tg128 generation-only on the 2026-06-05 int-dot rerun | Fastest new small-MoE result in this scout. Strong speed/currentness hook, but not a 30B-class capability comparison. |
| LFM2.5 8B-A1B | `Q4_K_M` | 5.1 GB / 8B.A1B | 3363.94 pp512 / 171.17 tg128 on ac4cddeb0 | Latest upstream control still keeps the small-MoE route in the 170 t/s class. |
| Nemotron 3 Nano 30B-A3B | `IQ4_XS` | 18.2 GB / 31B.A3.5B MoE | 1312.47 pp512 / 75.97 tg128 on the 2026-06-05 int-dot rerun | Practical NVIDIA Nemotron route for one Strix Halo system after the Nemotron 3 Ultra release. |
| Nemotron 3 Super 120B-A12B | `UD-IQ4_XS` | 64.5 GB / 120B.A12B MoE | 294.99 pp512 / 18.43 tg128 on the 2026-06-05 int-dot rerun | Missing middle Nemotron route: much larger than Nano, directly runnable as GGUF on one Strix Halo, but not a speed result. |
| Nemotron 3 Super 120B-A12B | `UD-IQ4_XS` | 64.5 GB / 120B.A12B MoE | 296.26 pp512 / 18.24 tg128 on ac4cddeb0 | Latest upstream control keeps the same capacity conclusion: runnable, useful, not fast. |
| Qwen3-30B-A3B-Instruct-2507 | `IQ4_XS` | 13.9 GB / 30B.A3B | 1430.65 pp512 / 100.38 tg128 on ac4cddeb0 | Latest upstream control keeps the separate direct 30B-class Qwen route above 100 t/s. |
| Qwen3-Coder 30B-A3B | `Q4_K_S` | 17.5 GB / 30B.A3B | 1423.05 pp512 / 100.99 tg128 r50 on official b9851 Vulkan | Current direct speed-first coding row now crosses 100 t/s on an official release binary. Not the balanced default. |
| Qwen3-Coder 30B-A3B | `UD-Q4_K_XL` | 17.7 GB / 30B.A3B | 1416.79 pp512 / 99.55 tg128 r5 on official b9851 Vulkan | Strong latest-build balanced-control signal, but short r5 only; keep separate from the longer Q4_K_S speed-first headline. |
| Qwen3-Coder 30B-A3B | `IQ4_XS` | 16.4 GB / 30B.A3B | 1372.27 pp512 / 90.44 tg128; 90.72 tg128 generation-only | Negative/control row: `IQ4_XS` alone did not beat the older Qwen3-Coder Q4_K_S 98.51 t/s headline. |
| Qwen3-Coder 30B-A3B | `Q4_K_S` | 17.5 GB / 30B.A3B | 1395.99 pp512 / 94.20 tg128 on ac4cddeb0 | Latest upstream control did not beat the older strict-clean 98.51 t/s speed-first headline. |
| Qwen3 30B-A3B NEO-MAX | `IQ4_XS` | 16.4 GB / 30B.A3B | 1396.05 pp512 / 87.39 tg128; 87.77 tg128 generation-only | Alternate 30B-A3B control row; the 2507 100 t/s result does not generalize to every 30B-A3B IQ4_XS file. |
| Qwen3.5 35B-A3B | `IQ4_XS` | 19.7 GB / 35B.A3B | 1170.27 pp512 / 75.22 tg128; 75.53 tg128 generation-only | Current/larger Qwen comparator; newer or larger is not automatically faster. |
| Qwen3.5 9B | `Q4_K_M` | 5.7 GB / 9B dense | 1015.35 pp512 / 34.49 tg128; 34.34 tg128 generation-only | Useful comparator for current Gemma-vs-Qwen discussion. Not the newest Qwen family. |
| Gemma 4 12B IT | `IQ4_XS` | 6.4 GB / 12B | 680.17 pp512 / 25.74 tg128; 25.77 tg128 generation-only | New Google model runs locally. Use for current-model/multimodal coverage, not speed. |
| Gemma 4 12B IT | `Q4_K_M` | 7.4 GB / 12B | 684.92 pp512 / 24.42 tg128; 24.42 tg128 generation-only | Balanced Gemma route. Slower than Qwen3.5 9B and much slower than Qwen 30B-class MoE speed rows. |
| Gemma 4 12B IT QAT | `UD-Q4_K_XL` | 6.7 GB / 12B | 816.32 pp512 / 29.34 tg128 direct on ac4cddeb0; MTP smoke reached 73.33 t/s | Better local Gemma 4 12B route than the earlier non-QAT direct rows, but the strongest value is the matched QAT MTP server path. |
| Gemma 4 26B-A4B IT QAT | `UD-Q4_K_XL` + matched `Q4_0` MTP head | 14.2 GB / 26B.A4B | 1431.96 pp512 / 74.80 tg128 direct; 73.96 t/s no-spec server; 110.00 t/s best MTP repeat; 107.42 t/s T3-only repeat; 102.69 t/s cold repeat | Highest-value new route in this update: current Google model, direct baseline, matched MTP speedup, and host-workload sensitivity evidence on the same Beelink box. |
| Gemma 4 26B-A4B IT | `UD-Q4_K_M` | 16.9 GB / 26B.A4B | 1326.52 pp512 / 55.45 tg128 r5 on official b9851 Vulkan | Useful latest-release direct control, but not a new Gemma speed path; the QAT/MTP route remains stronger for throughput. |
| Qwen3.6 27B MTP NVFP4 v3 | `NVFP4` | 16.1 GB / 27B dense | 373.97 pp512 / 13.17 tg128 direct; server smoke 13.32 t/s no-spec and 24.37 t/s MTP | Newer Qwen3.6 artifact runs, but it is a negative speed control. Valuable because it prevents chasing the wrong route. |
| NVIDIA Nemotron 3 Nano Omni 30B-A3B Reasoning | `MXFP4_MOE` | 21.7 GB / 31B.A3.5B MoE | 1277.60 pp512 / 56.56 tg128 direct on official `llama.cpp` b9747 | Current NVIDIA Omni/FP4 route runs locally on the Beelink/RADV path. Useful model-support evidence, not a speed headline versus the earlier Nano IQ4_XS or Qwen/LFM rows. |
| MiniMax M2.7 | `UD-IQ4_XS` | 108.4 GB / 230B.A10B MoE | 101.00 pp512 / 28.27 tg128; 28.60 tg128 generation-only | Large-model feasibility proof: 230B-class MoE runs locally on one Strix Halo. Not a speed result. |
| DeepSeek V4 Flash | GGUF / REAP / ds4 targets | 46.98-162 GB depending on route | Original 103.3GB route was download-blocked; later 52.6GB 0xSero/Spark-Mini local file failed to load; 2026-07-06 scan found a 92.8GiB `IQ2_M` GGUF candidate but the download was too slow to complete in this pass; the 46.98GiB REAP route requires a separate ds4 runtime | Strong setup-friction evidence. Do not list as pass, speed result, or hardware limit without a successful load. |
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
- 2026-06-30 official `llama.cpp` b9851 Vulkan sentinel for Qwen3-Coder `Q4_K_S`, Qwen3-Coder `UD-Q4_K_XL`, and Gemma 4 26B-A4B IT: [`data/raw/2026-06-30/latest-llamacpp-b9851-vulkan-sentinel/`](data/raw/2026-06-30/latest-llamacpp-b9851-vulkan-sentinel/)
- 2026-07-02 Ollama 0.31.1 buyer-path sanity check for Qwen3.6 35B-A3B: [`data/raw/2026-07-02/ollama-0311-qwen36-buyer-path/`](data/raw/2026-07-02/ollama-0311-qwen36-buyer-path/)
- 2026-07-02 official `llama.cpp` b9859 Vulkan sentinel for Qwen3-Coder `Q4_K_S`, Qwen3-Coder `UD-Q4_K_XL`, and Gemma 4 26B-A4B IT: [`data/raw/2026-07-02/latest-llamacpp-b9859-vulkan-sentinel/`](data/raw/2026-07-02/latest-llamacpp-b9859-vulkan-sentinel/)
- 2026-07-06 official `llama.cpp` b9888 Vulkan sentinel for Qwen3-Coder `Q4_K_S` and `UD-Q4_K_XL`: [`data/raw/2026-07-06/latest-llamacpp-b9888-vulkan-sentinel/`](data/raw/2026-07-06/latest-llamacpp-b9888-vulkan-sentinel/)
- 2026-07-10 `llama.cpp` b9946 stock/patched Vulkan and ROCm/Lemonade MoE concurrency sweep: [`data/moe_concurrency.csv`](data/moe_concurrency.csv), [`raw evidence`](data/raw/2026-07-10/llamacpp-b9946-moe-concurrency/)
- 2026-07-13 `llama.cpp` b9979 AMD/RADV density-gate correctness, 30B/80B concurrency repeats, thermals, and ROCm crossover: [`MOE_CONCURRENCY.md`](MOE_CONCURRENCY.md), [`detail CSV`](data/moe_density_gate.csv), [`summary CSV`](data/moe_density_gate_summary.csv), [`raw evidence`](data/raw/2026-07-13/llamacpp-b9979-amd-density-gate/)
- 2026-07-10 Ollama 0.31.2 installed-service Qwen3.6 and vision buyer-path check: [`data/raw/2026-07-10/ollama-0312-buyer-path/`](data/raw/2026-07-10/ollama-0312-buyer-path/)
- Qwen3-Coder IQ4_XS control: [`data/raw/2026-06-03/qwen3-coder-iq4xs-direct-scout/`](data/raw/2026-06-03/qwen3-coder-iq4xs-direct-scout/)
- Qwen3 30B-A3B NEO-MAX IQ4_XS control: [`data/raw/2026-06-03/qwen3-30b-a3b-neo-max-iq4xs-direct-scout/`](data/raw/2026-06-03/qwen3-30b-a3b-neo-max-iq4xs-direct-scout/)
- Qwen3.5 35B-A3B IQ4_XS control: [`data/raw/2026-06-03/qwen35-35b-a3b-iq4xs-direct-scout/`](data/raw/2026-06-03/qwen35-35b-a3b-iq4xs-direct-scout/)
- MiniMax M2.7: [`data/raw/2026-06-03/minimax-m27-ud-iq4xs-local-smoke/`](data/raw/2026-06-03/minimax-m27-ud-iq4xs-local-smoke/)
- DeepSeek V4 Flash attempt: [`data/raw/2026-06-03/deepseek-v4-flash-q2k-download-attempt/`](data/raw/2026-06-03/deepseek-v4-flash-q2k-download-attempt/)
- DeepSeek V4 Flash 0xSero/Spark-Mini load failure: [`data/raw/2026-06-05/deepseek-v4-flash-0xsero-load-failure/`](data/raw/2026-06-05/deepseek-v4-flash-0xsero-load-failure/)
- DeepSeek V4 Flash current-route triage: [`data/raw/2026-07-06/deepseek-v4-flash-current-route-triage/`](data/raw/2026-07-06/deepseek-v4-flash-current-route-triage/)
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

- Qwen3-Coder 30B-A3B `Q4_K_S`: 100.99 t/s direct first-party Beelink speed-first headline on official b9851; older b9179 strict-clean row preserved at 98.51 t/s.
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
| 1 | Focused official `llama.cpp` b10012 Vulkan sentinel | Recheck the 30B np8/np9 stock boundary and the existing Nemotron Omni MXFP4 artifact. This answers whether the open multi-user cliff persists and whether the post-b10005 native E2M1/E4M3 Vulkan conversions change a current FP4 route without rerunning the full matrix. |
| 2 | Nemotron-Cascade-2-30B-A3B GGUF direct and thinking/instruct scout | NVIDIA's new 30B-total / 3B-active reasoning model now has credible 16.9-23.0GiB GGUF routes. It is a current, practical one-box target and can be compared against the existing Nemotron Nano and Qwen 30B-class paths. |
| 3 | StepFun Step-3.7-Flash ROCmFPX Q3 QualityPlus first-party repro | The new 81.77GiB target is materially smaller than the existing Step 3.7 Q3/ROCmFP4 routes and is explicitly tuned for 128GB Strix Halo. Reproduce the pinned runner, no-spec/MTP behavior, acceptance, memory use, 4k/16k speed, a practical 64k agent run, and quality smoke before promoting it beyond community evidence. |
| 4 | Qwen-AgentWorld-35B-A3B GGUF feasibility and long-context scout | Official Qwen describes 35B total / 3B active and 262K context; credible GGUFs range from about 16.6GiB `UD-IQ4_XS` to 20.6GiB `UD-Q4_K_M`. This is a practical new agent/world-model route, but its value depends on whether the language-only GGUF path and long-context behavior work cleanly. |
| 5 | ROCmFP4 / CHADROCK stability follow-up from [`ROCMFP4_CHADROCK.md`](ROCMFP4_CHADROCK.md) | The helper route now reproduces ~140 t/s gen512 on a high-acceptance prompt. Next value is a cleaner multi-prompt profile: when does it stay near 140, when does it fall back toward 115-128, and which prompt/model profiles should users actually choose? |
| 6 | Ollama 0.31.2 regression isolation plus a minimal 0.32.0 service smoke | The normal 0.31.2 system-service path passes iGPU, Qwen3.6, vision, and restart checks, but measured 60.57 t/s versus 71.82 t/s on the separate 0.31.1 local binary. First isolate that runner delta; treat 0.32.0 as a compatibility smoke unless its inference path materially differs. |
| 7 | Nemotron Labs Puzzle 75B-A9B GGUF load/direct scout | The new compressed Nemotron Super derivative is 75.3B total / 9.3B active with MTP and up to 1M context. Community GGUFs provide roughly 37.8-48.1GiB Q3/IQ4/Q4 routes, making it a realistic one-box middle-capacity target; runtime support and output correctness must be proven first. |
| 8 | Nemotron 3 Nano Omni NVFP4 quality/multimodal follow-up | MXFP4_MOE now has a direct b9747 smoke pass at 56.56 tg128. A follow-up only matters if it compares NVFP4/MXFP4 quality, multimodal/mmproj behavior, or an easier recommended route. |
| 9 | DeepSeek V4 Flash route follow-up with planned storage/runtime | Current route scan found three different blockers: ordinary GGUF routes around 92.8-162GB, a slow 92.8GiB `IQ2_M` download candidate, and a smaller 46.98GiB REAP route that needs ds4 runtime support. Next value is a planned external-storage or ds4 test, not another blind partial download. |
| 10 | External-storage feasibility plan for Kimi-K2.7-Code, GLM-5.2, MiniMax-M3, Hy3, and Nemotron Ultra class routes | These are high-traffic model names, but most practical artifacts exceed the comfortable internal-disk/test envelope. A clean external NVMe plan is more valuable than pretending they are simple internal-disk tests. |

## Watch List

| Target | Status |
| --- | --- |
| StepFun Step-3.7-Flash ROCmFPX Q3 QualityPlus | New 81.77GiB, 3.57-BPW community artifact for a 198B sparse MoE with about 11B active parameters and 256k context. The model card reports strong local quality and fit results on Strix Halo, but it requires pinned `ciru-ai/ROCmFPX` support plus a separate Q8 MTP draft. Existing Nimo Step 3.7 evidence remains separate; first-party reproduction is the next step. |
| Nemotron-Cascade-2-30B-A3B | Official NVIDIA model is 30B total / 3B active, supports thinking and instruct modes plus up to 1M context, and now has credible GGUF artifacts. The balanced candidates fit comfortably on one 128GB box; first prove clean llama.cpp load, chat-template behavior, speed, and a practical context length. |
| Qwen-AgentWorld-35B-A3B | Official Qwen language world model is 35B total / 3B active with 262K context. Credible Unsloth GGUFs make it locally testable; use `--language-model-only` where the runtime otherwise expects absent visual weights, and treat it as an agent/environment-simulation target rather than a general-chat speed replacement. |
| Nemotron Labs Puzzle 75B-A9B | Official NVIDIA compression route reduces Nemotron Super to 75.3B total / 9.3B active and retains MTP and long-context support. Community GGUFs fit one 128GB system, but the `nemotron_h_puzzle` architecture and MTP path need first-party llama.cpp validation before recommendation. |
| Hy3 295B-A21B + MTP | Official `llama.cpp` b10005 introduced initial Hy3 and split-MTP support, which is also present in b10012. Tencent describes 295B total, 21B active, 3.8B MTP, and 256K context; the official BF16 repository is about 598GB. Treat as an artifact-scan/external-storage target until a compatible one-box route is identified and measured. |
| Qwen3.6 new quants/sources | Already important in the guide. Add only if a new source answers a new question. |
| Kimi-K2.7-Code | Very high viral value and active GGUF ecosystem. Smallest scanned routes remain huge: AesSedai `IQ2_XXS` about 262.8 GiB, Unsloth `UD-IQ1_M` about 283.0 GiB, and a pruned `deep55` route about 188.7 GiB. Treat as external-storage/watchlist, not a quick local default. |
| GLM-5.2 | Very high viral value. Unsloth GGUF exists with smallest scanned `UD-IQ1_S` about 201.8 GiB; REAP50 Q2 route scanned at 129.4 GiB; MXFP4/NVFP4 routes are about 400GB+. External-storage/watchlist unless a smaller compatible route appears. |
| MiniMax M3 | GGUF routes now exist, but smallest scanned Unsloth route is about 119.6 GiB and practical quants are much larger. Treat as watchlist/runtime-support route, not proven local guidance. |
| Nemotron 3 Nano Omni NVFP4/MXFP4 | MXFP4_MOE now has a first-party direct b9747 smoke pass at 1277.60 pp512 / 56.56 tg128. Good current NVIDIA Omni/FP4 support evidence; do not promote as a speed headline. NVFP4/mmproj remains a possible follow-up if it answers a multimodal or quality question. |
| DeepSeek V4 Flash | Original 103GB route was download-blocked; smaller 0xSero/Spark-Mini route reached local load attempts but failed before benchmarking. A 2026-07-06 scan found new ordinary-GGUF routes, including a 92.8GiB `IQ2_M` candidate, but the local download attempt was too slow to complete. REAP Q2 remains smaller at 46.98GiB but requires a ds4 runtime path. |
| Nemotron 3 Ultra 550B-A55B | GGUF route found in the 2026-06-05 scan, but the smallest scanned route is about 188 GB. Watch for smaller practical artifacts or test only with external storage / multi-node planning. |
| Nemotron 3 Super 120B-A12B | Tested with `UD-IQ4_XS`. Add lower/higher quant comparisons only if they answer a specific buyer question. |
| `llama.cpp` b10012 | Latest official release observed 2026-07-15; not yet measured here. It contains b10005's native Vulkan E2M1/E4M3 conversion and Hy3/MTP work. The seven later commits are maintenance outside the Vulkan inference kernel, so the same focused sentinel is sufficient. b9979 remains the measured multi-user baseline and b9851 the Qwen3-Coder speed-first headline. |
| Ollama 0.32.0 | Latest release observed 2026-07-14; not yet measured here. Release notes focus on the interactive agent/CLI experience and integration changes, so 0.31.2 remains the current measured system-service buyer path pending a minimal smoke check. |
| Ollama 0.31.2 | Measured system service installed and tested on 2026-07-10. Qwen3.6 reached 60.57 t/s warm API generation, Qwen2.5-VL 7B vision worked with Vulkan offload, and both service-restart and full-host-reboot persistence passed. Requires `OLLAMA_IGPU_ENABLE=1`; slower than the separate 0.31.1 local-binary run. |

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
- StepFun Step-3.7-Flash: <https://github.com/stepfun-ai/Step-3.7-Flash>
- StepFun Step-3.7-Flash ROCmFPX Q3 QualityPlus: <https://huggingface.co/jcbtc/Step-3.7-Flash-ROCmFPX-Q3-QualityPlus>
- Nemotron-Cascade-2-30B-A3B: <https://huggingface.co/nvidia/Nemotron-Cascade-2-30B-A3B>
- Nemotron-Cascade-2-30B-A3B GGUF: <https://huggingface.co/bartowski/nvidia_Nemotron-Cascade-2-30B-A3B-GGUF>
- Qwen-AgentWorld-35B-A3B: <https://huggingface.co/Qwen/Qwen-AgentWorld-35B-A3B>
- Qwen-AgentWorld-35B-A3B GGUF: <https://huggingface.co/unsloth/Qwen-AgentWorld-35B-A3B-GGUF>
- Nemotron Labs Puzzle 75B-A9B NVFP4: <https://huggingface.co/nvidia/NVIDIA-Nemotron-Labs-3-Puzzle-75B-A9B-NVFP4>
- Nemotron Labs Puzzle 75B-A9B GGUF: <https://huggingface.co/RemySkye/NVIDIA-Nemotron-Labs-3-Puzzle-75B-A9B-GGUF>
- Kimi-K2.7-Code GGUF: <https://huggingface.co/unsloth/Kimi-K2.7-Code-GGUF>
- GLM-5.2 GGUF: <https://huggingface.co/unsloth/GLM-5.2-GGUF>
- MiniMax-M3 GGUF: <https://huggingface.co/unsloth/MiniMax-M3-GGUF>
- Nemotron 3 Nano Omni MXFP4 GGUF: <https://huggingface.co/unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-GGUF>
- Nemotron 3 Nano Omni NVFP4 GGUF: <https://huggingface.co/FreedomAISVR/Nemotron-3-30B-Nano-Omni-NVFP4-GGUF>
- Hy3 official model and MTP documentation: <https://huggingface.co/tencent/Hy3>
- DeepSeek V4 Flash GGUF: <https://huggingface.co/unsloth/DeepSeek-V4-Flash-GGUF>
- DeepSeek V4 Flash IQ2_M GGUF: <https://huggingface.co/ilintar/DeepSeek-V4-Flash-GGUF>
- DeepSeek V4 Flash REAP Q2 GGUF: <https://huggingface.co/sleepyeldrazi/deepseek-v4-flash-reap-k128-Q2-GGUF>
- `llama.cpp` b9888: <https://github.com/ggml-org/llama.cpp/releases/tag/b9888>
- `llama.cpp` b10005: <https://github.com/ggml-org/llama.cpp/releases/tag/b10005>
- `llama.cpp` b10012: <https://github.com/ggml-org/llama.cpp/releases/tag/b10012>
- `llama.cpp` b9859: <https://github.com/ggml-org/llama.cpp/releases/tag/b9859>
- `llama.cpp` b9851 measured sentinel: <https://github.com/ggml-org/llama.cpp/releases/tag/b9851>
- `llama.cpp` b9747: <https://github.com/ggml-org/llama.cpp/releases/tag/b9747>
- Ollama 0.31.1: <https://github.com/ollama/ollama/releases/tag/v0.31.1>
- Ollama 0.31.2: <https://github.com/ollama/ollama/releases/tag/v0.31.2>
- Ollama 0.32.0: <https://github.com/ollama/ollama/releases/tag/v0.32.0>
- `llama.cpp` issue #25356: <https://github.com/ggml-org/llama.cpp/issues/25356>
- Ollama 0.30.11 historical watch target: <https://github.com/ollama/ollama/releases/tag/v0.30.11>
