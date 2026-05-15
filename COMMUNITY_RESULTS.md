# Community Results

Community benchmark reports are kept separate from the guide's headline claims. They are valuable because they show how well the setup transfers to other Strix Halo systems, distros, kernels, Mesa versions, containers, and power-management setups.

Structured data:

- [`data/community_results.csv`](data/community_results.csv)
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
- RPC matrix CSVs: [`data/raw/2026-05-09/community-rpc-issue12/`](data/raw/2026-05-09/community-rpc-issue12/)
- RPC failure snippets: [`data/raw/2026-05-10/community-rpc-followup-issue12/`](data/raw/2026-05-10/community-rpc-followup-issue12/)
- USB4 tuning CSVs and patch notes: [`data/raw/2026-05-10/community-usb4-tuning-issue13/`](data/raw/2026-05-10/community-usb4-tuning-issue13/)
- GMKtec EVO-X2 WSL2/HIP baseline: [`data/raw/2026-05-13/community-gmktec-wsl2-issue15/`](data/raw/2026-05-13/community-gmktec-wsl2-issue15/)
- GMKtec EVO-X2 native Ubuntu Vulkan/RADV reproduction: [`data/raw/2026-05-14/community-gmktec-native-issue16/`](data/raw/2026-05-14/community-gmktec-native-issue16/)

Short version: these reports add trust signals the primary Beelink results cannot provide alone:

- independent portability across a different Strix Halo chassis, distro, kernel, Mesa version, and container setup
- same-SKU variance across three Corsair systems with matched software and model files
- first community whole-system power and energy-per-token baseline for the Qwen3-Coder Vulkan/RADV row
- first community multi-node `llama.cpp` RPC matrix over a 3-node USB4 mesh
- first community USB4 latency tuning result tied to a real RPC benchmark cell
- first community Qwen3.6 Q4_0/Q4_K_M comparison on a second Strix Halo chassis
- first GMKtec EVO-X2 native Ubuntu Vulkan/RADV reproduction of the guide's Qwen3.6 row, within about 2% of the Beelink result
- first GMKtec EVO-X2 WSL2/HIP baseline, useful as Windows/WSL2 evidence but not apples-to-apples with native Vulkan/RADV

For the shortest practical decision layer, see the README section [Community-Tested Rules Of Thumb](README.md#community-tested-rules-of-thumb).

## Current Reports

| Date | Contributor | System | Stack | Model | Result | Why It Matters | Source |
|------|-------------|--------|-------|-------|--------|----------------|--------|
| 2026-05-07 | Fail-Safe | Corsair AI Workstation 300, Ryzen AI MAX+ 395, 128GB | Fedora 43, kernel 7.0-rc6, Mesa RADV 25.3.6, kyuz0 Vulkan container, llama.cpp b9049 | Qwen3-Coder 30B-A3B UD-Q4_K_XL | Session 1: 1393.00 pp512, 95.31 tg128. Session 2: 1393.47 pp512, 95.46 tg128. | Independent system, different chassis, different distro, newer RC kernel, older Mesa, no tuned daemon, and still within a few percent of the guide's Qwen3-Coder headline. The second session confirms the result is stable. | [#10](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10) |
| 2026-05-09 | Fail-Safe | Corsair AI Workstation 300 ai-2 | Fedora 43, kernel 7.0-rc6, Mesa RADV 25.3.6, kyuz0 Vulkan/RADV container, llama.cpp b9093 | Qwen3.6 35B-A3B Q4_0 and Q4_K_M | Q4_0: 1267.18 pp512 / 75.75 tg128. Q4_K_M: 1116.23 pp512 / 70.10 tg128. | Reproduces the same speed-vs-balanced quant shape on another Strix Halo system. Also shows model-source/stack choices matter: this bartowski run is slower than the guide's local 0xSero Strix Q4_0 row. | [#10 comment](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10#issuecomment-4413965527) |
| 2026-05-10 | Fail-Safe | Corsair AI Workstation 300 ai-2 | Fedora 43, kernel 7.0-rc6, Mesa RADV 25.3.6, kyuz0 Vulkan/RADV container, llama.cpp b9093 | Qwen3.6 35B-A3B Q4_0, UD-Q4_K_XL, UD-Q6_K_XL | 0xSero Q4_0: 79.82 tg128 with guide flags. Unsloth UD-Q4_K_XL: 60.14 tg128. Unsloth UD-Q6_K_XL: 55.52 tg128. | Quant/source/build follow-up: GGUF source explains about +5.3% tg128 between bartowski and 0xSero Q4_0; b9049 to b9093 is small and bidirectional; guide flags are effectively noise on this build. | [#10 comment](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10#issuecomment-4415454932) |
| 2026-05-09 | Fail-Safe | 3x Corsair AI Workstation 300 over USB4 `thunderbolt-net` mesh | Fedora 43, kernel 7.0-rc6, Mesa RADV 25.3.6, kyuz0 Vulkan/RADV and ROCm 7.2 containers | Qwen3-Coder 30B, Qwen3-Coder-Next 80B, MiniMax-M2.7 230B | RPC loses on fits-on-one models; 2-node ROCm runs MiniMax-M2.7 at 238.62 pp512 / 21.41 tg128; 3-node ROCm is slower at 19.74 tg128. | Answers the practical multi-box question: RPC is not a free speedup, but ROCm RPC can make >single-box models usable. | [#12](https://github.com/hogeheer499-commits/strix-halo-guide/issues/12), [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md) |
| 2026-05-09 | Fail-Safe | 2-node Corsair USB4 RPC cell from the same fleet | Fedora 43, kernel 7.0-rc6, kyuz0 Vulkan/RADV container | Qwen3-Coder 30B-A3B UD-Q4_K_XL | `pm_qos_resume_latency_us=100` reduced USB4 ping RTT from about 600-700 us to 134 us and improved 2-node Vulkan/RADV tg128 from 75.27 to 76.79 t/s. | Gives a simple, reversible tuning step for active Strix Halo cluster nodes; the kernel-module patch remains experimental. | [#13](https://github.com/hogeheer499-commits/strix-halo-guide/issues/13), [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md) |
| 2026-05-13 | mottledMantis | GMKtec EVO-X2, Ryzen AI MAX+ 395, 96GB | Ubuntu 24.04 on WSL2, ROCm 7.2.53211 / HIP, llama.cpp b9127 | Qwen3.6 35B-A3B UD-Q4_K_M | TG512 generation-only: 44.05 t/s. PP512: 538 t/s from a separate high-variance run. | First GMKtec EVO-X2 WSL2/HIP baseline. Useful Windows/WSL2 evidence, but not apples-to-apples with native Vulkan/RADV because prompt variance was high and the primary result is TG512. | [#15](https://github.com/hogeheer499-commits/strix-halo-guide/issues/15) |
| 2026-05-14 | mottledMantis | GMKtec EVO-X2, Ryzen AI MAX+ 395, 96GB | Ubuntu 26.04, kernel 7.0.0-15, Mesa RADV 26.0.3, llama.cpp b9156 | Qwen3.6 35B-A3B UD-Q4_K_M | 1050.82 pp512 / 61.52 tg128. Guide Beelink b9049 row: 1059.45 pp512 / 62.56 tg128. | Second independent contributor and first GMKtec native Ubuntu Vulkan/RADV reproduction. Despite 96GB RAM, IOMMU translated mode, no tuned daemon, newer kernel/Mesa/build, and model storage via mounted WSL2 VHDX, it lands within -0.8% pp and -1.7% tg of the Beelink row. | [#16](https://github.com/hogeheer499-commits/strix-halo-guide/issues/16) |

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

Fail-Safe also captured whole-system wall power during the same Corsair Qwen3-Coder runs using Zigbee smart plugs and Home Assistant.

| Scope | Community Reported Result | Notes |
|-------|--------------------------|-------|
| Idle baseline | about 33-38 W | Fedora 43 server, no GUI, no AI services running. |
| pp512 peak | about 237-251 W whole-system | Chassis, APU, DRAM, storage, fans. |
| tg128 sustained generation | about 150-157 W whole-system | Qwen3-Coder 30B-A3B UD-Q4_K_XL on Vulkan/RADV. |
| Energy per generated token | about 1.6 J/token | Useful baseline for future tokens-per-watt comparisons, but not yet a local headline claim. |

Power data source: [comment](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10#issuecomment-4401438242). Structured rows: [`data/community_power.csv`](data/community_power.csv).

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
- N=3 community data suggests same-SKU Qwen3-Coder tg128 variance can be around 2% even when software and model files match.
- The first community whole-system power baseline is around 150 W sustained generation and about 1.6 J/token for this Qwen3-Coder Vulkan/RADV row.
- The Qwen3.6 Q4_0-vs-Q4_K_M shape reproduced on a second Strix Halo system, but absolute numbers differ enough to reinforce the "model file and stack matter" warning.
- The Qwen3.6 source/build follow-up puts rough size on that warning: GGUF source can move tg128 by about 5%, build changes can move pp and tg in different directions, and flags may be irrelevant when they already match tool defaults.
- The WSL2/HIP baseline is useful for Windows users, but native Linux Vulkan/RADV remains the recommended fast path for this guide's measured workloads.
- The first community RPC matrix says multi-box Strix Halo is useful for capacity, not automatic speed. Shard only when the model does not fit or when the capacity tradeoff is worth the RPC tax.
- The first community USB4 tuning result gives cluster operators a low-friction step for lower latency and tighter benchmark variance, with an idle-power tradeoff.
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

Slower, failed, and surprising results are useful too.
