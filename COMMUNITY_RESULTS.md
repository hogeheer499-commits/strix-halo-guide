# Community Results

Community benchmark reports are kept separate from the guide's headline claims. They are valuable because they show how well the setup transfers to other Strix Halo systems, distros, kernels, Mesa versions, containers, and power-management setups.

Structured data:

- [`data/community_results.csv`](data/community_results.csv)
- [`data/community_power.csv`](data/community_power.csv)

Short version: this report adds three trust signals the primary Beelink results cannot provide alone:

- independent portability across a different Strix Halo chassis, distro, kernel, Mesa version, and container setup
- same-SKU variance across three Corsair systems with matched software and model files
- first community whole-system power and energy-per-token baseline for the Qwen3-Coder Vulkan/RADV row

## Current Reports

| Date | Contributor | System | Stack | Model | Result | Why It Matters | Source |
|------|-------------|--------|-------|-------|--------|----------------|--------|
| 2026-05-07 | Fail-Safe | Corsair AI Workstation 300, Ryzen AI MAX+ 395, 128GB | Fedora 43, kernel 7.0-rc6, Mesa RADV 25.3.6, kyuz0 Vulkan container, llama.cpp b9049 | Qwen3-Coder 30B-A3B UD-Q4_K_XL | Session 1: 1393.00 pp512, 95.31 tg128. Session 2: 1393.47 pp512, 95.46 tg128. | Independent system, different chassis, different distro, newer RC kernel, older Mesa, no tuned daemon, and still within a few percent of the guide's Qwen3-Coder headline. The second session confirms the result is stable. | [#10](https://github.com/hogeheer499-commits/strix-halo-guide/issues/10) |

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

## Open Community Lead

Fail-Safe has a three-node Corsair AI Workstation 300 setup connected through a USB4 Ethernet ring and offered to run 2-node or 3-node `llama.cpp` RPC benchmarks. That would be a separate evidence track from single-machine inference, but it could answer a useful question for owners with multiple Strix Halo boxes: when does model sharding over USB4 Ethernet help, and when does network/RPC overhead dominate?

## Interpretation

This is strong independent validation for the Vulkan/RADV Qwen3-Coder path. It does not replace the guide's Beelink headline claims, but it makes the practical recommendation stronger:

- Strix Halo Vulkan/RADV performance appears portable across at least Beelink GTR9 Pro and Corsair AI Workstation 300.
- The Qwen3-Coder 30B-A3B direct `llama-bench` result stays around 95-97 t/s even with a different distro/kernel/Mesa/container stack.
- N=3 community data suggests same-SKU Qwen3-Coder tg128 variance can be around 2% even when software and model files match.
- The first community whole-system power baseline is around 150 W sustained generation and about 1.6 J/token for this Qwen3-Coder Vulkan/RADV row.
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
