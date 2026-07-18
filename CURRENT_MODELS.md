# Current Model Triage

This page tracks fast-moving local-model targets that are useful for Strix Halo / Ryzen AI MAX+ 395 buyers, reviewers, and benchmark contributors.

For tools and contributors, the prioritized queue below is also available as [`data/current_test_queue.csv`](data/current_test_queue.csv). That file tracks candidates and blockers; it is deliberately separate from the measured-only [`data/best_known_profiles.csv`](data/best_known_profiles.csv).

It is not a leaderboard. The goal is to separate three questions that often get mixed together:

- Is the model current and interesting?
- Does it run locally on one 128 GB Strix Halo system?
- Is it fast, or is its value mainly capability, memory capacity, multimodality, or setup friction?

Measured rows below are first-party Beelink GTR9 Pro direct `llama-bench` Vulkan/RADV scouts unless stated otherwise. Most model scouts used a practical workstation state; controlled server, runtime, and regression campaigns record their own background-load and power conditions in the linked raw evidence. Do not inherit one campaign's host state for another.

## Community Tests Wanted

These are the highest-value open tests where another Strix Halo owner can add evidence without repeating work already completed here. Comment on the linked source before starting a large download or long campaign so the model, runtime, command, and required evidence can be aligned first.

| Test | Why it matters | Best volunteer setup | Status / start here |
| --- | --- | --- | --- |
| ROCm 7.14 practical 27B/35B hipBLASLt follow-up | Checks whether the measured 39-42% batch gain on the small FP16 sentinel carries to a model class buyers would actually serve. | Strix Halo with a pinned ROCm 7.14 vLLM environment and a supported practical model artifact. | Needs a supported artifact; see [`ROCM_VLLM_BUGWATCH.md`](ROCM_VLLM_BUGWATCH.md). |
| Official `llama.cpp` HIP/UMA practical-model follow-up | Tests whether the b10046 integrated-host-buffer fix remains stable on a useful 27B/35B model and whether the manual runtime-library path can be avoided. | Strix Halo owner able to build or run official ROCm/HIP `llama.cpp`. | Ready for a controlled run; see the [`b10046 raw note`](data/raw/2026-07-16/llamacpp-b10046-rocm-integrated-host-buffer/). |
| Corsair/Sixunited sustained-inference SCLK validation | Could turn a three-node hard-lock report into scoped thermal/stability guidance and a concrete OEM support question. It must not become a universal clock-cap recommendation without raw logs and independent confirmation. | Corsair AI Workstation 300 or another clearly identified Sixunited AXB35 revision with sustained-load monitoring. | WIP community report; coordinate in [issue #24](https://github.com/hogeheer499-commits/strix-halo-guide/issues/24). |
| Same-machine Windows versus Linux buyer path | Answers a common purchase question with a fair comparison instead of mixing different machines, model files, and power states. | One dual-boot Strix Halo system that can run the same model and prompt through comparable local runtimes. | Test window needed; start with [`STRIX_HALO_LOCAL_LLM_SETUP.md`](STRIX_HALO_LOCAL_LLM_SETUP.md). |
| Wall-power efficiency pass | Adds buyer- and vendor-relevant tokens-per-watt evidence without confusing wall power, package PPT, or inferred efficiency. | Any Strix Halo system with a reliable external wall meter and synchronized benchmark telemetry. | Hardware needed; follow [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md). |

The complete machine-readable queue, including blocked model downloads and maintainer-only runtime checks, remains in [`data/current_test_queue.csv`](data/current_test_queue.csv). Proven recommendations remain separate in [`BEST_KNOWN_PROFILES.md`](BEST_KNOWN_PROFILES.md).

## Best Current Headline Rows

| Question | Best current row | Why it matters |
| --- | --- | --- |
| Fastest direct 30B-class Qwen MoE | Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`: 100.04 t/s direct `llama-bench` on b9467; latest b9544 control measured 103.18 tg128 r10 | Shows a direct 30B-class Qwen route can cross 100 t/s on Strix Halo. Keep separate from the Qwen3-Coder headline and balanced-default rows. |
| Fastest direct Qwen3-Coder speed-first row | Qwen3-Coder 30B-A3B `Q4_K_S`: 100.99 t/s direct `llama-bench` on the official `llama.cpp` b9851 Ubuntu Vulkan release binary | First first-party Qwen3-Coder row above 100 t/s. Keep scoped as a speed-first quant, not the balanced default; the older b9179 strict-clean 98.51 t/s row remains useful historical context. |
| Fastest current small-MoE scout | LFM2.5 8B-A1B `Q4_K_M`: 170.02 t/s generation-only on the 2026-06-05 check; latest b9544 control measured 176.48 tg128 r10 | Shows how fast newer small active-parameter MoE routes can be. This is not a 30B-class capability replacement. |
| Largest current direct GGUF capacity route | DeepSeek V4 Flash 284B `UD-IQ2_XXS`: 155.64 pp512 / 13.27 tg128 direct `llama-bench` on official b10034 | Proves a pinned 90.86GB ordinary GGUF can load, generate, and answer a basic correctness check on one 128GB box. This is low-bit capacity/current-model evidence, not a speed or broad quality recommendation. |
| Current 120B-class direct GGUF route | Nemotron 3 Super 120B-A12B `UD-IQ4_XS`: 18.43 tg128 direct `llama-bench`; latest b9544 control measured 18.93 tg128 r3 | Keeps a more balanced 120B-class MoE capacity route visible separately from the much larger low-bit DeepSeek scout. |
| Largest first-party agent/MTP route | StepFun Step-3.7-Flash ROCmFPX Q3 QualityPlus: 198B total / about 11B active, 34.50 t/s at 4K and 33.83 t/s at 16K with MTP; 256K target-plus-draft allocation and native tool-call smokes passed | Shows what 128GB unified memory buys beyond short speed tests: a current sparse agent model, its draft, long-context headroom, and tools on one box. Advanced pinned server route, not direct `llama-bench`. |
| Fastest current-model MTP server route | CHADROCK ACE/SABER 35B ROCmFP4 through `ciru-ai/ROCmFPX`: 141.37 t/s mean across three repeats on the exact 3946-token reference profile, with a 140.84-141.79 t/s range and 100% mean draft acceptance; Gemma 4 26B-A4B QAT remains the stronger six-prompt repeat at 110.00 t/s | Shows tuned ROCmFP4/MTP can be much faster than stock routes when draft acceptance is high. Keep separate from direct `llama-bench`: the CHADROCK number is a repeat-confirmed reference profile, not a universal 4K speed, while Gemma is the broader prompt mix. |
| Current Ollama system-service buyer path | Qwen3.6 35B-A3B through Ollama 0.31.2: 60.57 t/s warm API generation mean on Vulkan/RADV; Qwen2.5-VL 7B vision smoke passed | This is the normal installed-service path, not a direct `llama-bench` headline. A later controlled same-port/same-cache comparison put 0.31.1, 0.31.2, and 0.32.0 in the same 72.55-73.20 t/s class, so the slower installed-service row is not evidence of a version-wide regression. Requires `OLLAMA_IGPU_ENABLE=1`. |
| Current ROCm 7.14 FP16 vLLM batch route | Qwen3-0.6B FP16 in the pinned official ROCm image: hipBLASLt on versus off improved aggregate throughput by 40.50% at concurrency 8, 38.96% at 9, and 41.54% at 16 | Reproduces AMD's Ryzen AI batch-8+ workaround without changing the host. It is small-model server evidence, not a direct GGUF or practical 27B/35B throughput claim; concurrency 4 was 0.77% slower. |
| Current `llama.cpp` HIP/UMA compatibility route | Official b10046 ROCm/HIP detected 120,124 MiB free UMA and used `ROCm_Host` model, output, and compute buffers without `HSA_OVERRIDE_GFX_VERSION` | Locally reproduces merged PR #24233 on `gfx1151`. The official binary needed the existing Ollama ROCm library path on this host; this is compatibility/setup evidence, not a Vulkan speed comparison or new beginner default. |

## External Community Tuned Routes

ciru-ai's GMKtec EVO-X2 / NixOS / IOMMU-on artifact adds a separate current-model lane with ROCmFP4, Chadrock/Qwopus, Gemma QAT/MTP, CrownV7, and quality-eval rows. These are valuable because they connect Strix Halo speed to quality and NPU-sidecar workflows, but they are not first-party Beelink direct `llama-bench` rows.

The separate [`ROCMFP4_CHADROCK.md`](ROCMFP4_CHADROCK.md) page now tracks this as an advanced runtime lane. It is not the beginner/default setup path and should not be mixed with stock Vulkan/RADV headline claims. First-party Beelink smoke on 2026-06-21 confirmed that both the Crown Halo dynamic artifact and the corrected CHADROCK ACE/SABER route load and serve locally. A 2026-07-16 profile then measured four prompt shapes with three repeats each: the exact 3946-token reference averaged 141.37 t/s at 100% draft acceptance, while the roughly 1K and 8K profiles fell to 78.00 and 83.85 t/s as acceptance dropped. This turns the former speed headline into practical operator guidance: benchmark the real prompt distribution.

| Route | Representative public result | Read |
| --- | ---: | --- |
| NPU sidecar | +3.29% main 64k iGPU latency with concurrent NPU load versus +68.96% with a comparable iGPU auxiliary load | Useful advanced IOMMU-on/NPU evidence; not a main iGPU replacement path. |
| Qwopus3.6 27B Chadrock | 0.9451 HumanEval+ and about 2.85x lower recorded request-generation time than the stored original Qwopus comparator | Strong tuned 27B quality-plus-speed evidence; keep as community served-route evidence. |
| Ace Saber 35B ROCmFP4 MTP | 0.9024 HumanEval+ in community data; first-party reference-profile follow-up averaged 141.37 t/s over three repeats at 100% draft acceptance | Interesting high-quality 35B tuned-route evidence; the local route works, but the four-shape profile proves the speed depends heavily on draft acceptance and generated-token shape. |
| Gemma 4 26B-A4B QAT/MTP | 122.8 decode tok/s after TTFP on a 512-token API row and 0.9207 HumanEval+ | Strong current Google-model community route; keep separate from the first-party Gemma 4 26B QAT MTP repeat. |
| StepFun Step-3.7-Flash ROCmFPX Q3 QualityPlus | First-party Beelink reproduction: 23.84 t/s no-spec versus 34.50 t/s MTP at 4K; 33.83 t/s at 16K; 28.06 t/s one-repeat 48K scout; 256K allocation and native tool call passed | High-value 198B-class capacity/agent route built for 128GB Strix Halo. MTP improved the matched 4K server baseline by 44.68%. Requires the pinned ROCmFPX runner and separate Q8 MTP draft. |
| CrownV7 Qwen3.6 35B dynamic route | 515.33 tok/s prompt processing at 128k, 0.83 BFCL v4 non-live accuracy | Useful long-context and tool/function-calling signal. |
| Crown Halo Qwen3.6 35B dynamic MTP Beelink smoke | short server 60.66 predicted t/s with 76/152 accepted; long structured server 57.61 predicted t/s with 168/344 accepted | First-party load/API/MTP smoke succeeded, but high-speed dynamic-MTP behavior remains a reproduction target. |

First practical ROCmFP4/CHADROCK artifact candidates for local reproduction are around 13.8-21.0 GiB, which makes them much more testable than Kimi/GLM/MiniMax extreme-capacity routes.

Source: [`COMMUNITY_RESULTS.md#gmktec-evo-x2-nixos--npu--rocmfp4-evidence-package`](COMMUNITY_RESULTS.md#gmktec-evo-x2-nixos--npu--rocmfp4-evidence-package), [`data/community_ciru_evox2_metrics.csv`](data/community_ciru_evox2_metrics.csv), and [`ciru-ai/strix-halo-evo-x2-evidence`](https://github.com/ciru-ai/strix-halo-evo-x2-evidence).

## July 2026 Runtime Controls

Latest audited upstream releases as of 2026-07-16 are `llama.cpp` b10046, Ollama 0.32.0 stable with 0.32.1 still prerelease, ROCm 7.14.0, vLLM 0.25.1, and SGLang 0.5.15.post1. The first-party Vulkan concurrency sentinel remains official b10034 because the later commits do not supersede its controlled model/backend comparison. Official b10046 does add a relevant HIP fix: merged PR #24233 restores integrated-device host-buffer support. The local b10046 ROCm binary detected the full 120GB-class UMA pool and used `ROCm_Host` buffers on `gfx1151` without a gfx-version override, although it needed the existing Ollama ROCm library path on this host. The b10034 repeats show that the 8-to-9 parallel-sequence MoE cliff still exists, while the exact existing Nemotron Omni MXFP4 artifact improved from 56.56 to 64.26 tg128 on the newer Vulkan runtime. A controlled same-port/same-cache Ollama comparison put 0.31.1, 0.31.2, and 0.32.0 in the same 72.55-73.20 t/s generation class. The installed 0.31.2 service remains the beginner default because the 0.32.0 test was an isolated local binary, not a system upgrade and full-reboot qualification. An isolated ROCm 7.14 / PyTorch 2.11 / vLLM A/B reproduced AMD's batch-8+ hipBLASLt workaround on `gfx1151`, with roughly 39-42% more aggregate throughput at concurrency 8/9/16 and no host-wide ROCm upgrade.

| Model / route | Quant | Tool | Result | Read |
| --- | --- | --- | ---: | --- |
| Qwen3-Coder 30B-A3B latest-runtime sentinel | `UD-Q4_K_XL`, Q4_0 KV | official b10034 Vulkan | np8 232.69 t/s vs np9 145.79 t/s mean over three repeats; -37.34% | The multi-user cliff persists on the latest measured official Vulkan runtime. The b9979 density-gate campaign remains the source for the experimental recovery comparison. |
| Qwen3-Next 80B-A3B latest-runtime sentinel | `UD-Q4_K_XL`, Q4_0 KV | official b10034 Vulkan | np8 144.61 t/s vs np9 98.78 t/s mean over three repeats; -31.69% | Confirms persistence on a second expert topology. This is regression evidence, not a positive speed headline. |
| Nemotron 3 Nano Omni 30B-A3B Reasoning | `MXFP4_MOE` | official b10034 Vulkan | 1286.15 pp512 / 64.26 tg128 | The exact b9747 artifact improved about 13.6% in generation versus its 56.56 t/s control. Do not generalize this to every FP4 model. |
| Qwen3.6 35B-A3B | `Q4_K_M` Ollama model | controlled Ollama 0.31.1 / 0.31.2 / 0.32.0 local binaries | warm means 72.55 / 73.19 / 73.20 t/s | Same cache, environment, prompt, port shape, and nine warm requests. No version-wide 0.31.2 regression appears under controlled conditions. Ollama 0.32.0 also passed full iGPU offload, vision, and process restart checks. |
| Qwen3 0.6B HIP compatibility sentinel | `Q8_0` | official `llama.cpp` b10046 ROCm/HIP | 4666.05 pp512 / 208.73 tg128; full 120,124 MiB free UMA detected | Small-model confirmation that merged integrated-host-buffer support works locally. The CPU-heavy smoke used real `ROCm_Host` allocations; do not treat this as a speed or Vulkan comparison. |
| Qwen3-Coder 30B-A3B concurrency repeats | `UD-Q4_K_XL`, Q4_0 KV, 128 experts/top-8 | official b9979 stock vs opt-in AMD/RADV density gate | np9 mean: 147.19 t/s stock, 210.07 density, 234.12 density+dense16; five repeats | Density recovers 42.7% at np9 without changing np8. Dense16 reaches +59.1% at np9 but regresses versus density alone at np16, so it is not a universal default. |
| Qwen3-Next 80B-A3B concurrency repeats | `UD-Q4_K_XL`, Q4_0 KV, 512 experts/top-10 | official b9979 stock vs opt-in AMD/RADV density gate | np9 mean: 100.15 t/s stock, 125.48 density, 142.72 density+dense16; three repeats | Confirms the dispatch cliff and recovery on the many-expert/top-10 shape; same caveat about dense16 at np16. |
| 30B/80B backend crossover | same workloads | b9979 Vulkan modes vs Lemonade ROCm b1259 | 30B ROCm leads at np16 with 287.64 t/s; 80B density Vulkan leads at np16 with 150.82 t/s | Backend choice depends on the model topology and target concurrency. There is no universal batching winner. |
| Qwen3-Coder 30B-A3B concurrency sweep | `UD-Q4_K_XL`, Q4_0 KV | official `llama.cpp` b9946 Vulkan | Aggregate decode 214.23 t/s at np8, 143.05 at np9, and 321.97 at np32 | Reproduces the issue #25356 8-to-9 cliff on a same-family local artifact. |
| Qwen3-Coder 30B-A3B concurrency sweep | same artifact and workload | b9946 Vulkan with flat threshold patch | Aggregate decode 202.73 t/s at np8, 195.38 at np9, and 321.02 at np32 | Experimental 8-to-16 / 8-to-32 cutoff patch removes most of the cliff, but is not the later density-gate design; one sweep reached 98 C sysfs temperature, so this is not default guidance. |
| Qwen3-Coder 30B-A3B concurrency sweep | same artifact and workload | Lemonade ROCm b1259 | Aggregate decode 184.93 t/s at np8, 191.24 at np9, and 354.59 at np32 | No 8-to-9 cliff and strongest np32 comparator in this sweep. Official ROCm b9946 was much slower. |
| Qwen3.6 35B-A3B | `Q4_K_M` Ollama model | Ollama 0.31.2 system service, Vulkan/RADV API | 60.57 t/s warm generation mean; 60.00-61.22 t/s warm range | Current buyer-path pass with full iGPU offload, vision smoke, service restart, and full-host-reboot persistence. The later controlled comparison did not reproduce a version-wide slowdown. |
| Qwen3.6 35B-A3B | `Q4_K_M` Ollama model | Ollama 0.31.1 local binary, Vulkan/RADV API | 71.82 t/s warm generation mean; 71.62-72.05 t/s warm range | Strong buyer-path update. Ollama 0.31.1 works on the measured Beelink system, but `OLLAMA_IGPU_ENABLE=1` is required to keep the Strix Halo iGPU active. |
| Qwen3-Coder 30B-A3B | `Q4_K_S` | official `llama.cpp` b9888 Vulkan | 1404.73 pp512 / 98.12 tg128 r50; 98.59 tg128 generation-only | Latest official runtime sentinel. Works cleanly and reproduces the 98 t/s class, but does not replace the b9851 100.99 t/s speed-first headline. |
| Qwen3-Coder 30B-A3B | `UD-Q4_K_XL` | official `llama.cpp` b9888 Vulkan | 1410.82 pp512 / 96.53 tg128 r5 | Balanced coding quant latest-runtime control. |
| Qwen3-Coder 30B-A3B | `Q4_K_S` | official `llama.cpp` b9859 Vulkan | 1413.38 pp512 / 98.48 tg128 r50; 99.09 tg128 generation-only | Current-runtime control. Reproduces the 98-99 t/s class but does not replace the b9851 100.99 t/s speed-first headline. |
| Qwen3-Coder 30B-A3B | `UD-Q4_K_XL` | official `llama.cpp` b9859 Vulkan | 1411.76 pp512 / 97.01 tg128 r5 | Balanced current-runtime control. |
| Gemma 4 26B-A4B IT | `UD-Q4_K_M` | official `llama.cpp` b9859 Vulkan | 1323.39 pp512 / 54.18 tg128 r5 | Direct Gemma control remains secondary to the Gemma QAT/MTP server route. |

## 2026-07-16 Current-Model Scouts

These rows use official `llama.cpp` b10034 with Vulkan/RADV on the Beelink GTR9 Pro. They answer practical model-support questions; none replaces the direct Qwen speed headlines.

| Model | Quant / route | Result | Practical read |
| --- | --- | ---: | --- |
| Nemotron Cascade 2 30B-A3B | `IQ4_XS` direct | 1325.31 pp512 / **78.95 tg128** | Current 30B-total/3B-active reasoning route loads cleanly and answered two small correctness checks. The attempted no-think prefix did not suppress visible reasoning, so no reliable no-think claim is made. |
| Qwen AgentWorld 35B-A3B | `UD-IQ4_XS` language-only | 1182.77 pp512 / **65.65 tg128** | Correctly simulated `echo agentworld-ok`; a separate 128K Q8 KV allocation smoke passed. Useful agent/environment route, not an ordinary chat recommendation or filled-128K quality result. |
| Nemotron 3 Nano Omni 30B-A3B | `NVFP4` plus F16 projector | 1143.91 pp512 / **53.21 tg128**; image OCR passed | First first-party image-capable Nemotron Omni route in the guide. The model read `STRIX 395`; this small smoke does not prove broad vision, audio, video, or production quality. |
| Nemotron Labs Audex 30B-A3B | text-only `MXFP4_MOE` | 1318.50 pp512 / **60.73 tg128** | Text GGUF loads and answered a small correctness check. The full audio pipeline needs a separate HF/vLLM sidecar and was not tested; its NVIDIA OneWay Noncommercial license also limits commercial use. |
| Nemotron Labs Puzzle 75B-A9B | candidate GGUF | **blocked before download** | Current official b10034 lacks the `nemotron_h_puzzle` architecture. Support is still in open llama.cpp PR #25444, so downloading 38-48 GiB now would not produce a clean upstream pass. |

Raw evidence: [`data/raw/2026-07-16/`](data/raw/2026-07-16/).

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
| DeepSeek V4 Flash 284B | `UD-IQ2_XXS` | 90.86 GB / 284.33B | 155.64 pp512 / 13.27 tg128 on official b10034; deterministic 12-minus-3 smoke answered `9` | Ordinary three-shard GGUF now loads and generates directly. Strong current capacity proof, but the low-bit quant and visible thinking block make this a load/basic-correctness pass rather than a broad quality recommendation. |
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
- DeepSeek V4 Flash 284B ordinary-GGUF direct pass: [`data/raw/2026-07-16/deepseek-v4-flash-ud-iq2-xxs/`](data/raw/2026-07-16/deepseek-v4-flash-ud-iq2-xxs/)
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

MiniMax M2.7 remains useful 230B-class MoE capacity evidence: a 108 GB GGUF route loaded and generated locally. DeepSeek V4 Flash now extends the direct ordinary-GGUF map to 284.33B at a smaller 90.86GB artifact size, but with a much more aggressive low-bit quant. These are useful buyer tradeoffs even though neither is a speed-first recommendation.

DeepSeek V4 Flash now shows how upstream runtime support can remove an adoption blocker. Earlier routes were blocked by download friction or failed to load; the pinned 90.86GB Unsloth `UD-IQ2_XXS` artifact now loads and generates directly on official b10034 at 13.27 tg128. The result proves current 284.33B ordinary-GGUF capacity on one 128GB system, while preserving the low-bit quality tradeoff and the separate specialized REAP route.

Nemotron 3 Ultra shows the same pattern at a larger scale. The new Ultra release is important, and a GGUF route was found in the 2026-06-05 follow-up scan. The smallest scanned Ultra GGUF route was still about 188 GB, so it remains a watchlist/external-storage/multi-node target rather than a practical one-box 128 GB Strix Halo benchmark. The practical NVIDIA family map is now: Ultra as watchlist, Super 120B-A12B as the larger direct GGUF capacity route, and Nano 30B-A3B as the faster practical route.

## Good Post Hooks

- "LFM2.5 8B-A1B at 170 t/s generation-only on Strix Halo: new small-MoE models are a different speed class."
- "Google Gemma 4 12B runs locally on Strix Halo, but Qwen/LFM are faster for text-only generation."
- "Gemma 4 26B-A4B QAT with matched MTP head: 110.0 t/s best-repeat on Strix Halo as a local server route."
- "Current model reality check: newest does not automatically mean fastest."
- "A 230B-class MiniMax MoE runs locally on one 128 GB Strix Halo system, but speed and capacity are different wins."
- "DeepSeek V4 Flash 284B runs as a 90.86GB ordinary GGUF on one 128GB Strix Halo system: 13.27 t/s, with the low-bit quality caveat kept visible."
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
| 1 | Practical 27B/35B ROCm 7.14 vLLM follow-up | The small FP16 A/B reproduced AMD's hipBLASLt batch-8+ workaround. A larger supported model is needed before this becomes normal buyer/server guidance. |
| 2 | Practical 27B/35B `llama.cpp` b10046 HIP host-buffer follow-up | The merged integrated-device fix now works on the small local sentinel. A normal guide-class model is needed to compare packaging, memory behavior, and usable generation against Vulkan/RADV. |
| 3 | Nemotron Labs Puzzle 75B-A9B after upstream architecture support merges | Do not download 38-48GiB while `nemotron_h_puzzle` support remains in open PR #25444. Re-test only after an official release includes the architecture. This avoids turning model distribution into another known load failure. |
| 4 | External-storage feasibility plan for Kimi-K2.7-Code, GLM-5.2, MiniMax-M3, Hy3, and Nemotron Ultra class routes | These are high-traffic model names, but most practical artifacts exceed the comfortable internal-disk/test envelope. A clean external NVMe plan is more valuable than pretending they are simple one-box downloads. |
| 5 | Second-system reproduction of the b10034 MoE np8-to-np9 cliff | The latest first-party sentinel confirms the problem on two model shapes. Independent Beelink/GMKtec/Corsair reproduction would turn it into stronger vendor and upstream engineering evidence. |

## Watch List

| Target | Status |
| --- | --- |
| StepFun Step-3.7-Flash ROCmFPX Q3 QualityPlus | **Measured locally:** the 81.77GiB target plus Q8 MTP draft ran on one 128GB Beelink. MTP measured 34.50 t/s at 4K and 33.83 t/s at 16K, with 44.68% uplift over the matched 4K no-spec server baseline. A one-repeat 48K scout, 256K allocation, and native tool-call smoke also passed. Advanced pinned ROCmFPX route, not direct `llama-bench`. |
| Nemotron-Cascade-2-30B-A3B | **Measured locally:** `IQ4_XS` reached 78.95 tg128 and passed two small answer checks on official b10034. The attempted no-think prefix did not suppress visible reasoning, so treat it as a practical reasoning route rather than a proven dual-mode profile. |
| Qwen-AgentWorld-35B-A3B | **Measured locally:** `UD-IQ4_XS` reached 65.65 tg128, simulated a terminal command correctly, and passed a 128K Q8 KV allocation smoke. Keep scoped to agent/world simulation; no filled-128K quality claim. |
| Nemotron Labs Puzzle 75B-A9B | **Blocked before download:** community GGUFs fit one 128GB system, but official b10034 lacks `nemotron_h_puzzle`. Wait for open llama.cpp PR #25444 or a later official release. |
| Hy3 295B-A21B + MTP | Official `llama.cpp` b10005 introduced initial Hy3 and split-MTP support, which is also present in b10012. Tencent describes 295B total, 21B active, 3.8B MTP, and 256K context; the official BF16 repository is about 598GB. Treat as an artifact-scan/external-storage target until a compatible one-box route is identified and measured. |
| Qwen3.6 new quants/sources | Already important in the guide. Add only if a new source answers a new question. |
| Kimi-K2.7-Code | Very high viral value and active GGUF ecosystem. Smallest scanned routes remain huge: AesSedai `IQ2_XXS` about 262.8 GiB, Unsloth `UD-IQ1_M` about 283.0 GiB, and a pruned `deep55` route about 188.7 GiB. Treat as external-storage/watchlist, not a quick local default. |
| GLM-5.2 | Very high viral value. Unsloth GGUF exists with smallest scanned `UD-IQ1_S` about 201.8 GiB; REAP50 Q2 route scanned at 129.4 GiB; MXFP4/NVFP4 routes are about 400GB+. External-storage/watchlist unless a smaller compatible route appears. |
| MiniMax M3 | GGUF routes now exist, but smallest scanned Unsloth route is about 119.6 GiB and practical quants are much larger. Treat as watchlist/runtime-support route, not proven local guidance. |
| Nemotron 3 Nano Omni NVFP4/MXFP4 | MXFP4_MOE now has a first-party direct b9747 smoke pass at 1277.60 pp512 / 56.56 tg128. Good current NVIDIA Omni/FP4 support evidence; do not promote as a speed headline. NVFP4/mmproj remains a possible follow-up if it answers a multimodal or quality question. |
| DeepSeek V4 Flash | **Measured locally:** pinned Unsloth `UD-IQ2_XXS` at 90.86GB loaded and generated directly on official b10034 at 155.64 pp512 / 13.27 tg128 and answered the deterministic smoke correctly. This resolves the ordinary-GGUF blocker, but remains low-bit capacity evidence rather than a speed or quality recommendation. The 46.98GiB REAP path still requires its separate ds4 runtime. |
| Nemotron 3 Ultra 550B-A55B | GGUF route found in the 2026-06-05 scan, but the smallest scanned route is about 188 GB. Watch for smaller practical artifacts or test only with external storage / multi-node planning. |
| Nemotron 3 Super 120B-A12B | Tested with `UD-IQ4_XS`. Add lower/higher quant comparisons only if they answer a specific buyer question. |
| `llama.cpp` b10034 / b10046 / b10066 | Official b10034 remains the measured Vulkan concurrency/model sentinel. Official b10046 was separately reproduced on ROCm/HIP: it detected the full UMA pool and used `ROCm_Host` model/output/compute buffers without a gfx-version override. b10066 is the current upstream release and includes automatic Hugging Face discovery/download for `dflash-` and `eagle3-` sidecars. The first b10066 Gemma 4 31B campaign now passes text, vision, and native tool-call smokes; its DFlash result is a workload-specific negative rather than a replacement headline. |
| ROCm 7.14.0 | New production release checked on 2026-07-16. AMD documents lower-than-expected inference on Ryzen AI MAX / MAX+ in some FP16 vLLM batch-8+ workloads with PyTorch earlier than 2.14 and recommends `TORCH_BLAS_PREFER_HIPBLASLT=1`. Treat this as an isolated vLLM/PyTorch A/B target, not a host-upgrade or universal backend recommendation. |
| Ollama 0.32.0 | Controlled local-binary pass on 2026-07-16: Qwen3.6 averaged 73.20 t/s over nine warm requests, fully offloaded to the iGPU, and Qwen2.5-VL vision worked before and after a process restart. This does not yet replace the installed 0.31.2 system-service buyer profile because no package upgrade or full-host reboot was performed. |
| Ollama 0.32.1 | **Stable release, not yet service-qualified here:** improves Gemma 4 tool calling and multi-turn reasoning and fixes an MLX cache leak. The existing 0.31.2 installed-service profile remains the buyer default until 0.32.1 passes the same iGPU, vision, restart, and full-reboot checks. |
| Gemma 4 official 31B QAT GGUF + DFlash | **Measured locally on b10066:** the official 31B Q4_0 target reached 308.28 pp512 / 11.38 tg128 direct and passed narrow text, `STRIX 395` vision, and native calculator tool-call checks. The matched Q8_0 DFlash sidecar loaded, but `n_max=8` was 5.54% slower at 5,471 prompt tokens and 20.42% slower at 21,855 because mean acceptance was only 14.12% and 10.91%. This is a useful current Google compatibility route and a warning that DFlash is not an automatic Vulkan/RADV speedup, not a headline replacement for the 26B-A4B QAT MTP route. [`raw evidence`](data/raw/2026-07-18/gemma4-31b-qat-dflash-b10066/) |
| `llama.cpp` PR #25666 | **Open AMD/RADV A/B target:** the author reports 75.2 to 84.9 t/s speculative decode and higher acceptance on Ryzen AI MAX+ 395 by avoiding MMVQ for small speculative steps. This is not merged guidance. Test in an isolated worktree and report reproduction data on the existing PR; no new PR is required. |
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
- `llama.cpp` b10034: <https://github.com/ggml-org/llama.cpp/releases/tag/b10034>
- `llama.cpp` b10046: <https://github.com/ggml-org/llama.cpp/releases/tag/b10046>
- `llama.cpp` b10066: <https://github.com/ggml-org/llama.cpp/releases/tag/b10066>
- `llama.cpp` HIP integrated-device fix PR #24233: <https://github.com/ggml-org/llama.cpp/pull/24233>
- `llama.cpp` DFlash sidecar auto-discovery PR #25811: <https://github.com/ggml-org/llama.cpp/pull/25811>
- `llama.cpp` AMD speculative-decode PR #25666: <https://github.com/ggml-org/llama.cpp/pull/25666>
- Google Gemma 4 31B QAT Q4_0 GGUF: <https://huggingface.co/google/gemma-4-31B-it-qat-q4_0-gguf>
- ggml-org Gemma 4 31B target and DFlash sidecars: <https://huggingface.co/ggml-org/gemma-4-31B-it-GGUF>
- ROCm 7.14.0: <https://github.com/ROCm/ROCm/releases/tag/rocm-7.14.0>
- vLLM 0.25.1: <https://github.com/vllm-project/vllm/releases/tag/v0.25.1>
- SGLang 0.5.15.post1: <https://github.com/sgl-project/sglang/releases/tag/v0.5.15.post1>
- `llama.cpp` b9859: <https://github.com/ggml-org/llama.cpp/releases/tag/b9859>
- `llama.cpp` b9851 measured sentinel: <https://github.com/ggml-org/llama.cpp/releases/tag/b9851>
- `llama.cpp` b9747: <https://github.com/ggml-org/llama.cpp/releases/tag/b9747>
- Ollama 0.31.1: <https://github.com/ollama/ollama/releases/tag/v0.31.1>
- Ollama 0.31.2: <https://github.com/ollama/ollama/releases/tag/v0.31.2>
- Ollama 0.32.0: <https://github.com/ollama/ollama/releases/tag/v0.32.0>
- Ollama 0.32.1: <https://github.com/ollama/ollama/releases/tag/v0.32.1>
- `llama.cpp` issue #25356: <https://github.com/ggml-org/llama.cpp/issues/25356>
- Ollama 0.30.11 historical watch target: <https://github.com/ollama/ollama/releases/tag/v0.30.11>
