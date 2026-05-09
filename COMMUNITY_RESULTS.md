# Community Results

Community benchmark reports are kept separate from the guide's headline claims. They are valuable because they show how well the setup transfers to other Strix Halo systems, distros, kernels, Mesa versions, containers, and power-management setups.

Structured data:

- [`data/community_results.csv`](data/community_results.csv)
- [`data/community_power.csv`](data/community_power.csv)
- [`data/community_rpc.csv`](data/community_rpc.csv)
- [`data/community_usb4_latency.csv`](data/community_usb4_latency.csv)

Short version: this report adds three trust signals the primary Beelink results cannot provide alone:

- independent portability across a different Strix Halo chassis, distro, kernel, Mesa version, and container setup
- same-SKU variance across three Corsair systems with matched software and model files
- first community whole-system power and energy-per-token baseline for the Qwen3-Coder Vulkan/RADV row
- first community multi-node `llama.cpp` RPC matrix over a 3-node USB4 mesh
- first community USB4 latency tuning result tied to a real RPC benchmark cell

## Current Reports

| Date | Contributor | System | Stack | Model | Result | Why It Matters | Source |
|------|-------------|--------|-------|-------|--------|----------------|--------|
| 2026-05-07 | Fail-Safe | Corsair AI Workstation 300, Ryzen AI MAX+ 395, 128GB | Fedora 43, kernel 7.0-rc6, Mesa RADV 25.3.6, kyuz0 Vulkan container, llama.cpp b9049 | Qwen3-Coder 30B-A3B UD-Q4_K_XL | Session 1: 1393.00 pp512, 95.31 tg128. Session 2: 1393.47 pp512, 95.46 tg128. | Independent system, different chassis, different distro, newer RC kernel, older Mesa, no tuned daemon, and still within a few percent of the guide's Qwen3-Coder headline. The second session confirms the result is stable. | [#10](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10) |
| 2026-05-09 | Fail-Safe | 3x Corsair AI Workstation 300 over USB4 `thunderbolt-net` mesh | Fedora 43, kernel 7.0-rc6, Mesa RADV 25.3.6, kyuz0 Vulkan/RADV and ROCm 7.2 containers | Qwen3-Coder 30B, Qwen3-Coder-Next 80B, MiniMax-M2.7 230B | RPC loses on fits-on-one models; 2-node ROCm runs MiniMax-M2.7 at 238.62 pp512 / 21.41 tg128; 3-node ROCm is slower at 19.74 tg128. | Answers the practical multi-box question: RPC is not a free speedup, but ROCm RPC can make >single-box models usable. | [#12](https://github.com/hogeheer499-commits/strix-halo-guide/issues/12), [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md) |
| 2026-05-09 | Fail-Safe | 2-node Corsair USB4 RPC cell from the same fleet | Fedora 43, kernel 7.0-rc6, kyuz0 Vulkan/RADV container | Qwen3-Coder 30B-A3B UD-Q4_K_XL | `pm_qos_resume_latency_us=100` reduced USB4 ping RTT from about 600-700 us to 134 us and improved 2-node Vulkan/RADV tg128 from 75.27 to 76.79 t/s. | Gives a simple, reversible tuning step for active Strix Halo cluster nodes; the kernel-module patch remains experimental. | [#13](https://github.com/hogeheer499-commits/strix-halo-guide/issues/13), [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md) |

## Cross-Box Variance

Fail-Safe then repeated the same Qwen3-Coder benchmark across three Ansible-managed Corsair AI Workstation 300 systems with the same model SHA, kernel, Mesa, container digest, and llama.cpp b9049 commit.

| Scope | Result | Interpretation | Source |
|-------|--------|----------------|--------|
| pp512 across 3 boxes | 1393.0 to 1394.5 t/s, about 0.11% spread | Prompt-processing/compute-bound rows are effectively identical across this small fleet. | [comment](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10#issuecomment-4401323126) |
| tg128 across 3 boxes | 93.55 to 95.50 t/s, about 2.05% spread | Generation/bandwidth-bound rows show small but real per-system variance. The slowest box reproduced the same tg128 value after background load was removed. | [comment](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10#issuecomment-4401323126) |
| Thermal/clock instrumentation | SCLK held 2900MHz and MCLK held 1000MHz on all three boxes | The observed tg spread was not explained by obvious clock throttling. | [comment](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10#issuecomment-4401323126) |

Practical read: community Strix Halo reports within a few percent of the guide are likely matching the same performance class, especially for token generation where memory-subsystem variance can show up.

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

- Strix Halo Vulkan/RADV performance appears portable across at least Beelink GTR9 Pro and Corsair AI Workstation 300.
- The Qwen3-Coder 30B-A3B direct `llama-bench` result stays around 95-97 t/s even with a different distro/kernel/Mesa/container stack.
- N=3 community data suggests same-SKU Qwen3-Coder tg128 variance can be around 2% even when software and model files match.
- The first community whole-system power baseline is around 150 W sustained generation and about 1.6 J/token for this Qwen3-Coder Vulkan/RADV row.
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
