# Community Results

Community benchmark reports are kept separate from the guide's headline claims. They are valuable because they show how well the setup transfers to other Strix Halo systems, distros, kernels, Mesa versions, containers, and power-management setups.

Structured data:

- [`data/community_results.csv`](data/community_results.csv)
- [`data/community_nimo_issue4.csv`](data/community_nimo_issue4.csv)
- [`data/community_power.csv`](data/community_power.csv)
- [`data/community_rpc.csv`](data/community_rpc.csv)
- [`data/community_rpc_server.csv`](data/community_rpc_server.csv)
- [`data/community_rpc_failures.csv`](data/community_rpc_failures.csv)
- [`data/community_rpc_model_hashes.csv`](data/community_rpc_model_hashes.csv)
- [`data/community_usb4_latency.csv`](data/community_usb4_latency.csv)
- [`data/community_usb4_idle_power.csv`](data/community_usb4_idle_power.csv)
- [`CONTRIBUTORS.md`](CONTRIBUTORS.md)

Raw community follow-up artifacts:

- Qwen3-Coder issue-comment provenance: [`data/raw/2026-05-07/community-qwen-coder-issue10/`](data/raw/2026-05-07/community-qwen-coder-issue10/)
- Qwen3.6 raw rows: [`data/raw/2026-05-09/community-qwen36-issue10/`](data/raw/2026-05-09/community-qwen36-issue10/)
- Qwen3.6 source/build follow-up: [`data/raw/2026-05-10/community-qwen36-source-build-issue10/`](data/raw/2026-05-10/community-qwen36-source-build-issue10/)
- Whole-system wall-power rows: [`data/raw/2026-05-10/community-power-issue6/`](data/raw/2026-05-10/community-power-issue6/)
- RPC matrix CSVs: [`data/raw/2026-05-09/community-rpc-issue12/`](data/raw/2026-05-09/community-rpc-issue12/)
- RPC failure snippets: [`data/raw/2026-05-10/community-rpc-followup-issue12/`](data/raw/2026-05-10/community-rpc-followup-issue12/)
- USB4 tuning CSVs and patch notes: [`data/raw/2026-05-10/community-usb4-tuning-issue13/`](data/raw/2026-05-10/community-usb4-tuning-issue13/)
- GMKtec EVO-X2 WSL2/HIP baseline: [`data/raw/2026-05-13/community-gmktec-wsl2-issue15/`](data/raw/2026-05-13/community-gmktec-wsl2-issue15/)
- GMKtec EVO-X2 native Ubuntu Vulkan/RADV reproduction: [`data/raw/2026-05-14/community-gmktec-native-issue16/`](data/raw/2026-05-14/community-gmktec-native-issue16/)
- GMKtec EVO-X2 Qwen3-Coder follow-up: [`data/raw/2026-05-19/community-gmktec-qwen-coder-issue17/`](data/raw/2026-05-19/community-gmktec-qwen-coder-issue17/)
- GMKtec EVO-X2 Qwen3.6 MTP follow-up: [`data/raw/2026-05-19/community-gmktec-mtp-issue18/`](data/raw/2026-05-19/community-gmktec-mtp-issue18/)
- Windows LM Studio MS-S1-Max report: [`data/raw/2026-06-02/community-windows-lmstudio-issue3/`](data/raw/2026-06-02/community-windows-lmstudio-issue3/)
- Reddit GMKtec EVO-X2 tuned Qwen3-Coder report: [`data/raw/2026-06-02/community-reddit-look-qwen-coder/`](data/raw/2026-06-02/community-reddit-look-qwen-coder/)
- Nimo AI Mini PC issue #4 bundle: [`data/raw/2026-06-03/community-nimo-issue4/`](data/raw/2026-06-03/community-nimo-issue4/), summarized in [`COMMUNITY_NIMO.md`](COMMUNITY_NIMO.md)
- Nimo Gemma 4 QAT follow-up: [`data/raw/2026-06-06/community-nimo-gemma4-qat-issue4/`](data/raw/2026-06-06/community-nimo-gemma4-qat-issue4/)

Short version: these reports add trust signals the primary Beelink results cannot provide alone:

- independent portability across a different Strix Halo chassis, distro, kernel, Mesa version, and container setup
- same-SKU variance across three Corsair systems with matched software and model files
- first community whole-system wall-power and energy-per-token cross-section across Qwen3-Coder, Qwen3.6, gpt-oss-120b, and Qwen3-Coder-Next
- first community multi-node `llama.cpp` RPC matrix over a 3-node USB4 mesh
- first community USB4 latency tuning result tied to a real RPC benchmark cell
- first community Qwen3.6 Q4_0/Q4_K_M comparison on a second Strix Halo chassis
- first GMKtec EVO-X2 native Ubuntu Vulkan/RADV reproduction of the guide's Qwen3.6 row, within about 2% of the Beelink result
- first GMKtec EVO-X2 Qwen3-Coder UD-Q4_K_XL rows, including generation-only and full `pp512/tg128` b9235 follow-up data
- first independent Qwen3.6 MTP exact-model reproduction, with a 93.29 t/s six-prompt average on GMKtec
- first GMKtec EVO-X2 WSL2/HIP baseline, useful as Windows/WSL2 evidence but not apples-to-apples with native Vulkan/RADV
- first Windows / LM Studio / Ryzen AI MAX+ 395 community serving report, useful for Windows buyers but not a native-Linux comparison
- first Reddit-reported tuned GMKtec EVO-X2 Qwen3-Coder `Q4_K_S` row around 99.9-100.0 t/s, with explicit thermal and power-policy qualifiers
- first Nimo AI Mini PC community bundle, adding another compact 128GB Strix Halo chassis plus large-model, MTP, StepFun, Qwen 122B, and thermal-context evidence
- first Nimo Gemma 4 QAT + matched MTP assistant-head follow-up, showing where QAT heads improve single-stream decode and where concurrency/tooling caveats still matter

For the shortest practical decision layer, see the README section [Community-Tested Rules Of Thumb](README.md#community-tested-rules-of-thumb).

## Current Reports

| Date | Contributor | System | Stack | Model | Result | Why It Matters | Source |
|------|-------------|--------|-------|-------|--------|----------------|--------|
| 2026-05-07 | Fail-Safe | Corsair AI Workstation 300, Ryzen AI MAX+ 395, 128GB | Fedora 43, kernel 7.0-rc6, Mesa RADV 25.3.6, kyuz0 Vulkan container, llama.cpp b9049 | Qwen3-Coder 30B-A3B UD-Q4_K_XL | Session 1: 1393.00 pp512, 95.31 tg128. Session 2: 1393.47 pp512, 95.46 tg128. | Independent system, different chassis, different distro, newer RC kernel, older Mesa, no tuned daemon, and still within a few percent of the guide's Qwen3-Coder headline. The second session confirms the result is stable. | [#10](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10) |
| 2026-05-09 | Fail-Safe | Corsair AI Workstation 300 ai-2 | Fedora 43, kernel 7.0-rc6, Mesa RADV 25.3.6, kyuz0 Vulkan/RADV container, llama.cpp b9093 | Qwen3.6 35B-A3B Q4_0 and Q4_K_M | Q4_0: 1267.18 pp512 / 75.75 tg128. Q4_K_M: 1116.23 pp512 / 70.10 tg128. | Reproduces the same speed-vs-balanced quant shape on another Strix Halo system. Also shows model-source/stack choices matter: this bartowski run is slower than the guide's local 0xSero Strix Q4_0 row. | [#10 comment](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10#issuecomment-4413965527) |
| 2026-05-10 | Fail-Safe | Corsair AI Workstation 300 ai-2 | Fedora 43, kernel 7.0-rc6, Mesa RADV 25.3.6, kyuz0 Vulkan/RADV container, llama.cpp b9093 | Qwen3.6 35B-A3B Q4_0, UD-Q4_K_XL, UD-Q6_K_XL | 0xSero Q4_0: 79.82 tg128 with guide flags. Unsloth UD-Q4_K_XL: 60.14 tg128. Unsloth UD-Q6_K_XL: 55.52 tg128. | Quant/source/build follow-up: GGUF source explains about +5.3% tg128 between bartowski and 0xSero Q4_0; b9049 to b9093 is small and bidirectional; guide flags are effectively noise on this build. | [#10 comment](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10#issuecomment-4415454932) |
| 2026-05-10 | Fail-Safe | Corsair AI Workstation 300 ai-1 / ai-2 | Fedora 43, Mesa RADV 25.3.6, kyuz0 Vulkan/RADV container, llama.cpp b9049/b9093 | Qwen3-Coder, Qwen3.6, gpt-oss-120b, Qwen3-Coder-Next | Sustained tg wall power: 137-174 W. Generated-token energy: 1.59 J/token for Qwen3-Coder, 1.96 for Qwen3.6, 3.10 for gpt-oss-120b, 3.44 for Qwen3-Coder-Next. | First multi-model community wall-power cross-section. It turns raw t/s into practical energy context and shows power does not scale simply with model file size. | [#6](https://github.com/hogeheer499-commits/strix-halo-guide/issues/6), [`community_power.csv`](data/community_power.csv) |
| 2026-05-09 | Fail-Safe | 3x Corsair AI Workstation 300 over USB4 `thunderbolt-net` mesh | Fedora 43, kernel 7.0-rc6, Mesa RADV 25.3.6, kyuz0 Vulkan/RADV and ROCm 7.2 containers | Qwen3-Coder 30B, Qwen3-Coder-Next 80B, MiniMax-M2.7 230B | RPC loses on fits-on-one models; 2-node ROCm runs MiniMax-M2.7 at 238.62 pp512 / 21.41 tg128; 3-node ROCm is slower at 19.74 tg128. | Answers the practical multi-box question: RPC is not a free speedup, but ROCm RPC can make >single-box models usable. | [#12](https://github.com/hogeheer499-commits/strix-halo-guide/issues/12), [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md) |
| 2026-05-09 | Fail-Safe | 2-node Corsair USB4 RPC cell from the same fleet | Fedora 43, kernel 7.0-rc6, kyuz0 Vulkan/RADV container | Qwen3-Coder 30B-A3B UD-Q4_K_XL | `pm_qos_resume_latency_us=100` reduced USB4 ping RTT from about 600-700 us to 134 us and improved 2-node Vulkan/RADV tg128 from 75.27 to 76.79 t/s. | Gives a simple, reversible tuning step for active Strix Halo cluster nodes; the kernel-module patch remains experimental. | [#13](https://github.com/hogeheer499-commits/strix-halo-guide/issues/13), [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md) |
| 2026-05-13 | mottledMantis | GMKtec EVO-X2, Ryzen AI MAX+ 395, 96GB | Ubuntu 24.04 on WSL2, ROCm 7.2.53211 / HIP, llama.cpp b9127 | Qwen3.6 35B-A3B UD-Q4_K_M | TG512 generation-only: 44.05 t/s. PP512: 538 t/s from a separate high-variance run. | First GMKtec EVO-X2 WSL2/HIP baseline. Useful Windows/WSL2 evidence, but not apples-to-apples with native Vulkan/RADV because prompt variance was high and the primary result is TG512. | [#15](https://github.com/hogeheer499-commits/strix-halo-guide/issues/15) |
| 2026-05-14 | mottledMantis | GMKtec EVO-X2, Ryzen AI MAX+ 395, 96GB | Ubuntu 26.04, kernel 7.0.0-15, Mesa RADV 26.0.3, llama.cpp b9156 | Qwen3.6 35B-A3B UD-Q4_K_M | 1050.82 pp512 / 61.52 tg128. Guide Beelink b9049 row: 1059.45 pp512 / 62.56 tg128. | Second independent contributor and first GMKtec native Ubuntu Vulkan/RADV reproduction. Despite 96GB RAM, IOMMU translated mode, no tuned daemon, newer kernel/Mesa/build, and model storage via mounted WSL2 VHDX, it lands within -0.8% pp and -1.7% tg of the Beelink row. | [#16](https://github.com/hogeheer499-commits/strix-halo-guide/issues/16) |
| 2026-05-19 / 2026-05-24 | mottledMantis | GMKtec EVO-X2, Ryzen AI MAX+ 395, 96GB | Ubuntu 26.04, kernel 7.0.0-15, Mesa RADV 26.0.3, llama.cpp b9235 | Qwen3-Coder 30B-A3B UD-Q4_K_XL | 92.11 tg128 generation-only. Full follow-up: 1157.29 pp512 / 91.40 tg128. | First GMKtec Qwen3-Coder UD rows. Lower than the Beelink/Corsair b9049 rows, but still in the same practical performance class. The full follow-up is especially useful because it shows command-shape sensitivity: it used `-b 512 -ub 512`, `flash_attn=0`, and `use_mmap=1`, so keep it as portability evidence rather than a headline replacement. | [#17](https://github.com/hogeheer499-commits/strix-halo-guide/issues/17) |
| 2026-05-19 | mottledMantis | GMKtec EVO-X2, Ryzen AI MAX+ 395, 96GB | Ubuntu 26.04, kernel 7.0.0-15, Mesa RADV 26.0.3, llama.cpp b9235 | Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn | no MTP: 74.72 t/s; MTP `draft-n=2`: 93.29 t/s; MTP `draft-n=3`: 93.01 t/s. | First independent reproduction of the guide's exact MTP GGUF route. It slightly exceeds the local Beelink b9235 broad MTP average, while still keeping the "not a broad 100 t/s claim" boundary intact. | [#18](https://github.com/hogeheer499-commits/strix-halo-guide/issues/18), [`mtp_speculative.csv`](data/mtp_speculative.csv) |
| 2026-06-02 | bennos1911 | Minisforum MS-S1-Max, Ryzen AI MAX+ 395, 128GB | Windows 11 Pro 25H2, AMD Adrenalin 26.5.2, LM Studio 0.4.15 build 2, Vulkan llama.cpp v2.18.0 | Qwen3.6 35B-A3B Q4_K_M | LM Studio API script summary: 45 runs, 89.49 tok/s average, 78.53 tok/s median; long 512-token prompt rows around 69-70 tok/s. | First Windows / LM Studio / Ryzen AI MAX+ 395 community serving report. It helps Windows-first buyers, but it is a different benchmark shape from native Linux `llama-bench` and does not prove Windows-vs-Linux parity. | [#3](https://github.com/hogeheer499-commits/strix-halo-guide/issues/3#issuecomment-4602020775), [`raw`](data/raw/2026-06-02/community-windows-lmstudio-issue3/) |
| 2026-06-02 | Look_Over_There | GMKtec EVO-X2, Ryzen AI MAX+ 395 | Vulkan/RADV device line `RADV_STRIX_HALO`, llama.cpp b9467 `1fd5f4803`; OS/kernel/Mesa not reported | Qwen3-Coder 30B-A3B Q4_K_S | Short-context `-p 0 -n 128`: most runs around 99.90 t/s; best observed 100.0 t/s after about 10 runs. | Independent Reddit result showing that a tuned GMKtec can touch 100 t/s on this speed-first Qwen3-Coder shape. The contributor disclosed repaste, reseated memory pads, 15-20C lower CPU/GPU temps, and high-power policy, so treat it as tuned thermal/power-policy evidence rather than a default headline. | [Reddit thread](https://www.reddit.com/r/StrixHalo/comments/1tu78x5/qwen3coder_30b_at_985_ts_on_strix_halo_has_anyone/), [`raw note`](data/raw/2026-06-02/community-reddit-look-qwen-coder/) |
| 2026-06-03 | boxwrench | Nimo AI Mini PC, Ryzen AI MAX+ 395, 128GB | Ubuntu 25.04, kernel 6.18.1, Mesa RADV 25.2.8, ROCm 7.1.1 baseline, UMA 4GB, IOMMU on | Qwen 3.6 35B, Qwen3-Coder-Next, Qwen 122B, StepFun Step-3.7-Flash, DFlash rows | Key rows include Qwen3-Coder-Next Vulkan server at 723.2 pp / 44.4 decode, Qwen 122B MTP tuned decode at 28.3 t/s, StepFun MTP at 211.2 pp / 26.0 decode, and Qwen3.6 MTP Q4_K_M at 81.2 t/s. | Adds another compact 128GB Strix Halo chassis and broad large-model/server evidence. This is valuable buyer/OEM portability evidence, but the rows are server/eval/community rows, not first-party direct `llama-bench` headlines. | [#4](https://github.com/hogeheer499-commits/strix-halo-guide/issues/4#issuecomment-4608440144), [`COMMUNITY_NIMO.md`](COMMUNITY_NIMO.md), [`structured`](data/community_nimo_issue4.csv) |
| 2026-06-06 | boxwrench | Nimo AI Mini PC follow-up, Ryzen AI MAX+ 395, 128GB | llama.cpp b9360 Vulkan/RADV; Atomic llama.cpp TurboQuant fork for Gemma 4 MTP assistant-head rows | Gemma 4 12B / 26B-A4B / 31B QAT Q4_0 plus matched MTP heads | Best rows: 12B QAT MTP 45.6 decode, 26B-A4B QAT MTP 71.4 decode, 31B QAT MTP 19.1 decode. Plain 26B-A4B QAT still wins 2-slot aggregate at 90.9 tok/s. | Adds a strong Gemma 4 QAT/MTP lesson: matched QAT assistant heads can materially improve single-stream decode and acceptance, but the current Atomic path has a `PARALLEL=2` crash caveat, so serving shape matters. | [#4](https://github.com/hogeheer499-commits/strix-halo-guide/issues/4#issuecomment-4639263658), [`raw`](data/raw/2026-06-06/community-nimo-gemma4-qat-issue4/GEMMA4-QAT-NUMBERS.md), [`structured`](data/community_nimo_issue4.csv) |

## Nimo AI Mini PC Large-Model Bundle

boxwrench contributed the first Nimo AI Mini PC bundle in [#4](https://github.com/hogeheer499-commits/strix-halo-guide/issues/4#issuecomment-4608440144). The summary lives in [`COMMUNITY_NIMO.md`](COMMUNITY_NIMO.md), with structured rows in [`data/community_nimo_issue4.csv`](data/community_nimo_issue4.csv) and raw attachments under [`data/raw/2026-06-03/community-nimo-issue4/`](data/raw/2026-06-03/community-nimo-issue4/).

The practical value is vendor/chassis coverage and large-model feasibility, not a replacement speed headline. The bundle adds:

- Nimo AI Mini PC, Ryzen AI MAX+ 395 / Radeon 8060S, 128GB unified memory
- Ubuntu 25.04, kernel 6.18.1, Mesa 25.2.8, ROCm 7.1.1 baseline
- 4GB UMA and IOMMU enabled, different from this guide's primary Beelink recommendation
- Qwen 3.6 35B, Qwen3-Coder-Next, Qwen 122B, StepFun Step-3.7-Flash, DFlash, GPT-OSS/Gemma rows in the raw bundle
- Gemma 4 QAT Q4_0 rows for 12B, 26B-A4B, and 31B, including matched QAT MTP assistant-head follow-up data
- thermal and power context that is useful for compact-chassis buyers

Important caveat: these are community serving/eval rows with their own harnesses, not same-shape direct Beelink `llama-bench` comparisons.

## Cross-Box Variance

Fail-Safe then repeated the same Qwen3-Coder benchmark across three Ansible-managed Corsair AI Workstation 300 systems with the same model SHA, kernel, Mesa, container digest, and llama.cpp b9049 commit.

| Scope | Result | Interpretation | Source |
|-------|--------|----------------|--------|
| pp512 across 3 boxes | 1393.0 to 1394.5 t/s, about 0.11% spread | Prompt-processing/compute-bound rows are effectively identical across this small fleet. | [comment](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10#issuecomment-4401323126) |
| tg128 across 3 boxes | 93.55 to 95.50 t/s, about 2.05% spread | Generation/bandwidth-bound rows show small but real per-system variance. The slowest box reproduced the same tg128 value after background load was removed. | [comment](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10#issuecomment-4401323126) |
| Thermal/clock instrumentation | SCLK held 2900MHz and MCLK held 1000MHz on all three boxes | The observed tg spread was not explained by obvious clock throttling. | [comment](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10#issuecomment-4401323126) |

Practical read: community Strix Halo reports within a few percent of the guide are likely matching the same performance class, especially for token generation where memory-subsystem variance can show up.

## GMKtec EVO-X2 Native Ubuntu Reproduction

mottledMantis contributed the first native Ubuntu Vulkan/RADV GMKtec EVO-X2 result in [#16](https://github.com/hogeheer499-commits/strix-halo-guide/issues/16). This is especially valuable because it is a second community contributor, a different vendor/chassis, 96GB instead of 128GB, Ubuntu 26.04 instead of the guide's Ubuntu 24.04 setup, kernel 7.0.0-15, Mesa RADV 26.0.3, and llama.cpp b9156.

| System | Backend | Model | pp512 | tg128 | Delta vs guide Beelink Qwen3.6 row |
|--------|---------|-------|------:|------:|------------------------------------|
| Beelink GTR9 Pro, 128GB, Ubuntu 24.04, b9049 | Vulkan/RADV | Qwen3.6 UD-Q4_K_M | 1059.45 | 62.56 | baseline |
| GMKtec EVO-X2, 96GB, Ubuntu 26.04, b9156 | Vulkan/RADV | Qwen3.6 UD-Q4_K_M | 1050.82 | 61.52 | -0.8% pp512, -1.7% tg128 |
| GMKtec EVO-X2 tuned rerun | Vulkan/RADV | Qwen3.6 UD-Q4_K_M | 1035.69 | 60.59 | -2.2% pp512, -3.1% tg128 |

The practical conclusion is strong: native Linux Vulkan/RADV performance transfers across Beelink, Corsair, and GMKtec Strix Halo systems when the model/backend shape is comparable. This does not make every platform detail identical, but it does make the guide's native Vulkan/RADV setup much more credible for people choosing a GMKtec EVO-X2.

Raw CSV attachments are imported under [`data/raw/2026-05-14/community-gmktec-native-issue16/`](data/raw/2026-05-14/community-gmktec-native-issue16/). Structured rows are in [`data/community_results.csv`](data/community_results.csv).

## GMKtec EVO-X2 Qwen3-Coder And MTP Follow-Ups

mottledMantis then added follow-up reports on the same GMKtec EVO-X2 class system: Qwen3-Coder UD-Q4_K_XL on llama.cpp b9235, including the later full `pp512/tg128` command, and the exact Qwen3.6 MTP IQ4_XS-Q8nextn GGUF referenced by the guide.

| Issue | Model | Mode | Result | Interpretation |
|-------|-------|------|--------|----------------|
| [#17](https://github.com/hogeheer499-commits/strix-halo-guide/issues/17) | Qwen3-Coder 30B-A3B UD-Q4_K_XL | Direct `llama-bench`, generation-only `-p 0 -n 128 -r 20` | 92.11 tg128 | Useful GMKtec/latest-b9235 baseline. It is lower than the Beelink/Corsair b9049 rows, so keep it as community portability evidence rather than a headline replacement. |
| [#17 follow-up](https://github.com/hogeheer499-commits/strix-halo-guide/issues/17#issuecomment-4526903409) | Qwen3-Coder 30B-A3B UD-Q4_K_XL | Direct `llama-bench`, full `pp512/tg128`, `-b 512 -ub 512`, `flash_attn=0`, `use_mmap=1` | 1157.29 pp512 / 91.40 tg128 | Completes the missing prompt+generation shape for GMKtec b9235. It is valuable reproducibility evidence, but not apples-to-apples with the guide's optimized Beelink row because the flags differ. |
| [#18](https://github.com/hogeheer499-commits/strix-halo-guide/issues/18) | Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn | `llama-server`, no MTP | 74.72 t/s average over six prompts | Confirms the exact MTP GGUF baseline works on GMKtec. |
| [#18](https://github.com/hogeheer499-commits/strix-halo-guide/issues/18) | Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn | `llama-server`, `draft-n=2` | 93.29 t/s average over six prompts | Best community broad MTP average reported so far; slightly above the local Beelink b9235 92.30 t/s row. |
| [#18](https://github.com/hogeheer499-commits/strix-halo-guide/issues/18) | Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn | `llama-server`, `draft-n=3` | 93.01 t/s average, 175.97 t/s best prompt | Higher single-prompt peak, but `draft-n=2` was the better broad-average setting in this GMKtec rerun. |

The #17 follow-up is useful because it converts the original generation-only Qwen3-Coder report into a full `pp512/tg128` reference row while preserving why it should not be over-promoted: batch size, flash attention, mmap, build, and host setup all matter. The #18 result is especially useful because it validates the guide's MTP route on a second Strix Halo vendor/chassis with a different kernel and Mesa stack. It also sharpens the public wording: MTP is a real server-speed route and can spike far above 100 t/s on favorable prompts, but the broad six-prompt averages are still in the 92-93 t/s range, not a general 100 t/s guarantee.

## Reddit GMKtec EVO-X2 Tuned 100 t/s Report

Look_Over_There contributed a Reddit-reported GMKtec EVO-X2 Qwen3-Coder `Q4_K_S` result on llama.cpp b9467 `1fd5f4803`. The reported command shape was:

```bash
llama-bench -fa 1 -n 128 -p 0 -m ./Qwen3-Coder-30B-A3B-Instruct-Q4_K_S.gguf
```

They reported that most short-context runs sat around 99.90 t/s and the best observed run reached 100.0 t/s after about 10 runs. This is valuable because it is the first external Strix Halo report to touch the round 100 t/s mark on the same speed-first Qwen3-Coder family used by the Beelink headline.

The qualifier matters just as much as the number: the contributor repasted the heatsink, reseated memory thermal pads, saw CPU/GPU temperatures drop by about 15-20C, and used a high-power Linux policy that forces GPU `power_dpm_force_performance_level=high` plus CPU EPP `performance`. They also warned that the high-power policy can add about 15-20W, may help or hurt depending on workload, and should not be treated as a full-time recommendation without thermal checks.

Local Beelink follow-up did not reproduce 100 t/s with the same b9467 command. The default local build path measured 96.38-96.72 t/s, a `glslc v2026.1` build enabled `int dot: 1` but still measured 95.27-95.91 t/s, and a separate high-power-policy test improved one short b9467 run from 95.18 to 96.37 t/s. Practical interpretation: 100 t/s is plausible on tuned Strix Halo hardware, but the guide should not promote it as the default Beelink direct headline.

## Windows LM Studio MS-S1-Max Report

bennos1911 contributed the first Windows / LM Studio / Ryzen AI MAX+ 395 report in [#3](https://github.com/hogeheer499-commits/strix-halo-guide/issues/3#issuecomment-4602020775). This is especially useful for beginner buyers because many people start from Windows and want to know whether they can use local AI before committing to native Ubuntu.

| System | Backend | Model | Result | Interpretation |
|--------|---------|-------|--------|----------------|
| Minisforum MS-S1-Max, Ryzen AI MAX+ 395, 128GB, Windows 11 Pro 25H2, AMD Adrenalin 26.5.2 | LM Studio 0.4.15 build 2, Vulkan llama.cpp v2.18.0 | Qwen3.6 35B-A3B Q4_K_M, `n_parallel=4`, `n_ctx=262144`, max tokens 512 | Script summary: 89.49 tok/s average, 78.53 tok/s median across 45 runs; the long 512-token prompt rows were around 69-70 tok/s | Useful Windows serving/API evidence. Not a same-shape comparison against native Linux `llama-bench`, so keep it out of headline speed claims. |

The benchmark script was run from WSL2 Ubuntu while LM Studio performed GPU work on the Windows host. The imported raw artifacts include the benchmark script, CSV output, and hardware telemetry. This report does not close the same-machine Windows-vs-Linux question yet, but it does prove that Windows + LM Studio is a real path worth documenting instead of ignoring.

## Qwen3.6 Community Quant Check

Fail-Safe also ran Qwen3.6 35B-A3B Q4_0 and Q4_K_M from `bartowski/Qwen_Qwen3.6-35B-A3B-GGUF` on the same Corsair ai-2 system.

| Quant | Source | pp512 mean | tg128 mean | Run-to-run spread | Interpretation |
|-------|--------|------------|------------|-------------------|----------------|
| Q4_0 | bartowski | 1267.18 t/s | 75.75 t/s | 0.17% pp, 0.08% tg | Speed-first path; +13.5% pp512 and +8.1% tg128 versus Q4_K_M in this community run. |
| Q4_K_M | bartowski | 1116.23 t/s | 70.10 t/s | 0.16% pp, 0.09% tg | Balanced candidate; slower than Q4_0 but likely safer if quality matters. |

Fail-Safe then followed up with an apples-to-apples source/build check using 0xSero and Unsloth GGUFs on the same Corsair ai-2 system, all on llama.cpp b9093.

| Quant | Source | Flags | pp512 mean | tg128 mean | Interpretation |
|-------|--------|-------|------------|------------|----------------|
| Q4_0 | 0xSero/Strix | kyuz0 defaults | 1281.48 t/s | 79.77 t/s | Fastest community Qwen3.6 row on this stack. |
| Q4_0 | 0xSero/Strix | guide flags | 1281.87 t/s | 79.82 t/s | Flags were effectively noise on b9093. |
| Q4_0 | bartowski | guide shape | 1267.18 t/s | 75.75 t/s | Same nominal quant, different source; about 5% slower tg128 than 0xSero on the same stack. |
| Q4_K_M | bartowski | guide shape | 1116.23 t/s | 70.10 t/s | Balanced bartowski row. |
| UD-Q4_K_XL | Unsloth | kyuz0 defaults | 1114.26 t/s | 60.14 t/s | Unsloth Dynamic 4-bit row, close to the guide's local UD-Q4_K_M class. |
| UD-Q6_K_XL | Unsloth | kyuz0 defaults | 1031.94 t/s | 55.52 t/s | Higher-precision dynamic quant, slower as expected. |

This supports the guide's main Qwen3.6 framing: Q4_0 is a speed-first choice, while Q4_K_M/UD variants are more conservative all-rounder choices. It also warns against treating all Q4_0 files as identical. In this follow-up, GGUF source explained about +5.3% tg128 between bartowski and 0xSero Q4_0, b9049 to b9093 was a small bidirectional build effect (+3% pp512, -1.85% tg128), and guide flags versus kyuz0 defaults were effectively noise on b9093. Keep these as throughput evidence, not model-quality claims.

## GMKtec EVO-X2 WSL2/HIP Baseline

mottledMantis also contributed a GMKtec EVO-X2 WSL2/HIP baseline in [#15](https://github.com/hogeheer499-commits/strix-halo-guide/issues/15):

| Setup | Backend | Model | Result | Interpretation |
|-------|---------|-------|--------|----------------|
| GMKtec EVO-X2, Windows/WSL2 Ubuntu 24.04, ROCm 7.2.53211 | HIP/ROCm | Qwen3.6 UD-Q4_K_M | 44.05 t/s TG512 generation-only; PP512 538 t/s from separate high-variance run | Useful proof that WSL2/HIP can run the model, but not a recommended fast path and not apples-to-apples with native Vulkan/RADV. |

The value of #15 is not that WSL2/HIP beats the guide. It does not. The value is that it gives a real baseline for people trying Windows/WSL2 and explains why native Linux Vulkan/RADV remains the simpler performance recommendation for Strix Halo LLM work.

## Whole-System Power

Fail-Safe captured whole-system wall power on Corsair AI Workstation 300 systems using Zigbee smart plugs and Home Assistant WebSocket capture. These rows include the whole box: chassis, APU, DRAM, storage, fans, and idle platform draw.

| Model | Box | Workload | Sustained tg wall W | tg throughput | Wall J/token | Wall tokens/J | pp peak wall W | Source |
|-------|-----|----------|--------------------:|--------------:|-------------:|--------------:|---------------:|--------|
| Qwen3-Coder 30B-A3B UD-Q4_K_XL | ai-2 | tg128 | 150 W | 95.31 t/s | 1.59 | 0.63 | 251 W | [#10 power](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10#issuecomment-4401438242) |
| Qwen3.6 35B-A3B Q4_0 | ai-2 | tg1024 | 148 W | 75.41 t/s | 1.96 | 0.510 | 203 W | [#6 Qwen3.6](https://github.com/hogeheer499-commits/strix-halo-guide/issues/6#issuecomment-4414228987) |
| gpt-oss-120b MXFP4 | ai-1 | tg1024 | 173.6 W | 55.90 t/s | 3.10 | 0.322 | 259.4 W | [#6 gpt-oss](https://github.com/hogeheer499-commits/strix-halo-guide/issues/6#issuecomment-4414323665) |
| Qwen3-Coder-Next 80B-A3B Q8_0 | ai-2 | tg1024 | 137.4 W | 39.98 t/s | 3.44 | 0.291 | 211.9 W | [#6 Qwen3-Coder-Next](https://github.com/hogeheer499-commits/strix-halo-guide/issues/6#issuecomment-4414411995) |

Practical read:

- Qwen3-Coder is still the best energy-per-generated-token row in this community set: about 1.6 J/token at the wall.
- gpt-oss-120b is usable locally, but roughly half as energy-efficient per generated token as Qwen3-Coder in this wall-power sample.
- Qwen3-Coder-Next Q8_0 draws the lowest sustained generation wall power in this set despite the largest file size, because throughput and actual memory/kernel utilization matter more than disk size alone.
- Prompt-processing peak power sits roughly in the 200-260 W band across these MoE rows.

Structured rows: [`data/community_power.csv`](data/community_power.csv). Provenance note: [`data/raw/2026-05-10/community-power-issue6/`](data/raw/2026-05-10/community-power-issue6/). These are community wall-power rows, not Beelink wall-power headline claims.

## Community RPC Result

Fail-Safe also ran the three-node USB4 `llama.cpp` RPC matrix tracked in [#12](https://github.com/hogeheer499-commits/strix-halo-guide/issues/12). This is now documented separately in [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md), with the imported raw CSV attachment under [`data/raw/2026-05-09/community-rpc-issue12/`](data/raw/2026-05-09/community-rpc-issue12/).

Short practical read:

- if the model fits on one Strix Halo box, one box is faster for raw single-stream throughput
- 2-node RPC costs about 14-22% tg128 on the measured fits-on-one models
- 3-node RPC costs more than 2-node RPC in the measured rows
- for the 140.8 GB MiniMax-M2.7 model that does not fit on one box, ROCm RPC worked and Vulkan/RADV failed to load
- for huge models, use the smallest ROCm node count that fits

Follow-up tuning from [#13](https://github.com/hogeheer499-commits/strix-halo-guide/issues/13): for active USB4 cluster nodes, `pm_qos_resume_latency_us=100` is now documented as the recommended simple tuning step in [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md). It improved the same Vulkan/RADV 2-node Qwen3-Coder RPC cell by about 2%. The thunderbolt IRQ-throttle patch is documented as experimental, not a default recommendation.

## Interpretation

This is strong independent validation for the Vulkan/RADV Qwen3-Coder path. It does not replace the guide's Beelink headline claims, but it makes the practical recommendation stronger:

- Strix Halo Vulkan/RADV performance appears portable across at least Beelink GTR9 Pro, Corsair AI Workstation 300, and GMKtec EVO-X2.
- The Qwen3-Coder 30B-A3B direct `llama-bench` result stays around 95-97 t/s even with a different distro/kernel/Mesa/container stack.
- The Qwen3.6 35B-A3B UD-Q4_K_M native Vulkan/RADV row reproduced within about 2% on GMKtec EVO-X2 despite 96GB memory, Ubuntu 26.04, kernel 7.0.0-15, Mesa 26.0.3, llama.cpp b9156, and IOMMU translated mode.
- The Qwen3.6 MTP IQ4_XS-Q8nextn route now has an independent GMKtec reproduction at 93.29 t/s average over six prompts, slightly above the local Beelink b9235 92.30 t/s row.
- The GMKtec Qwen3-Coder b9235 rows came in lower than the Beelink/Corsair b9049 rows, which is useful too: the full follow-up specifically shows that batch size, flash attention, mmap, build, model source, prompt shape, and host state can move results by several percent.
- N=3 community data suggests same-SKU Qwen3-Coder tg128 variance can be around 2% even when software and model files match.
- The community wall-power cross-section now has four model rows: Qwen3-Coder around 150 W and 1.6 J/token, Qwen3.6 around 148 W and 2.0 J/token, gpt-oss-120b around 174 W and 3.1 J/token, and Qwen3-Coder-Next around 137 W and 3.4 J/token.
- The Qwen3.6 Q4_0-vs-Q4_K_M shape reproduced on a second Strix Halo system, but absolute numbers differ enough to reinforce the "model file and stack matter" warning.
- The Qwen3.6 source/build follow-up puts rough size on that warning: GGUF source can move tg128 by about 5%, build changes can move pp and tg in different directions, and flags may be irrelevant when they already match tool defaults.
- The WSL2/HIP baseline is useful for Windows users, but native Linux Vulkan/RADV remains the recommended fast path for this guide's measured workloads.
- The first community RPC matrix says multi-box Strix Halo is useful for capacity, not automatic speed. Shard only when the model does not fit or when the capacity tradeoff is worth the RPC tax.
- The first community USB4 tuning result gives cluster operators a low-friction step for lower latency and tighter benchmark variance, with an idle-power tradeoff.
- The Nimo bundle extends the evidence map to another compact 128GB Strix Halo chassis and adds large-model/server/MTP rows that answer "what can this hardware attempt?" rather than only "what is the fastest short-context direct row?"
- The Nimo Gemma 4 QAT follow-up adds a useful serving/tooling caveat: matched QAT assistant heads improve single-stream decode and MTP acceptance, but current Gemma 4 MTP tooling is not a clean drop-in replacement for stock llama.cpp or multi-slot serving yet.
- `RADV GFX1151` on older Mesa and `RADV STRIX_HALO` on newer Mesa refer to the same Strix Halo iGPU class; the name changed with Mesa/device-string updates.
- Community rows should stay out of `data/headline_claims.csv` unless they are reproduced locally or promoted with clear scope.

## Add Your Result

Open a [benchmark report](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=benchmark-report.md) with:

- system and memory size
- BIOS UMA and IOMMU settings
- OS, kernel, Mesa/RADV or ROCm versions
- backend and build/container
- model file, quant, hash if available
- exact command
- CSV/raw output
- any background-load or power-management notes

If you have a wall meter, smart plug, UPS export, or validated board-power tool, open a [power / efficiency report](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=power-report.md) with idle, sustained load, sample interval, raw readings, command, and tokens/J or J/token if calculated.

Slower, failed, and surprising results are useful too.
