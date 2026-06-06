# Latest llama.cpp Int-Dot Regression Check

Date: 2026-06-05

Purpose: rerun selected current-model scout rows on a newer local `llama.cpp` build where the Vulkan device reports `int dot: 1`.

This is first-party Beelink GTR9 Pro evidence. It is a practical workstation scout, not a cold/strict-clean headline campaign.

## System

- System: Beelink GTR9 Pro
- APU: AMD Ryzen AI MAX+ 395 / Radeon 8060S
- Memory: 128 GB unified
- Backend: Vulkan/RADV
- Tool: `llama-bench`
- Build commit in CSVs: `2016bf2`
- Vulkan device line: `RADV_STRIX_HALO`, `uma: 1`, `int dot: 1`, `KHR_coopmat`

Device evidence: [`list-devices-intdot.txt`](list-devices-intdot.txt)

## Results

| Model | Quant | Command shape | Result | Raw |
| --- | --- | --- | ---: | --- |
| LFM2.5 8B-A1B | `Q4_K_M` | pp512/tg128 r5 | 3414.61 pp512 / 168.96 tg128 | [`lfm25-8b-a1b-q4km-b2016bf2-r5.csv`](lfm25-8b-a1b-q4km-b2016bf2-r5.csv) |
| LFM2.5 8B-A1B | `Q4_K_M` | generation-only `-p 0 -n 128` r20 | 170.02 tg128 | [`lfm25-8b-a1b-q4km-b2016bf2-p0-n128-r20.csv`](lfm25-8b-a1b-q4km-b2016bf2-p0-n128-r20.csv) |
| Qwen3-30B-A3B-Instruct-2507 | `IQ4_XS` | pp512/tg128 r3 | 1447.43 pp512 / 98.32 tg128 | [`qwen3-30b-2507-iq4xs-b2016bf2-r3.csv`](qwen3-30b-2507-iq4xs-b2016bf2-r3.csv) |
| Qwen3-30B-A3B-Instruct-2507 | `IQ4_XS` | generation-only `-p 0 -n 128` r20 | 99.10 tg128 | [`qwen3-30b-2507-iq4xs-b2016bf2-p0-n128-r20.csv`](qwen3-30b-2507-iq4xs-b2016bf2-p0-n128-r20.csv) |
| Nemotron 3 Nano 30B-A3B | `IQ4_XS` | pp512/tg128 r5 | 1312.47 pp512 / 75.97 tg128 | [`nemotron-3-nano-30b-a3b-iq4xs-b2016bf2-r5.csv`](nemotron-3-nano-30b-a3b-iq4xs-b2016bf2-r5.csv) |
| Nemotron 3 Super 120B-A12B | `UD-IQ4_XS` | pp512/tg128 r3 | 294.99 pp512 / 18.43 tg128 | [`nemotron-3-super-120b-a12b-udiq4xs-b2016bf2-r3.csv`](nemotron-3-super-120b-a12b-udiq4xs-b2016bf2-r3.csv) |
| Qwen3-Coder 30B-A3B | `UD-Q4_K_XL` | generation-only `-p 0 -n 128` r20 | 92.84 tg128 | [`qwen3-coder-30b-udq4kxl-b2016bf2-p0-n128-r20.csv`](qwen3-coder-30b-udq4kxl-b2016bf2-p0-n128-r20.csv) |

## Interpretation

- LFM2.5 is the fastest measured current small-MoE scout here. It should not be framed as a 30B-class capability replacement.
- Qwen3-30B-A3B-Instruct-2507 remains close to the earlier 100.04 t/s direct row but did not exceed it in this latest/int-dot check.
- Nemotron 3 Super is valuable as a direct 120B-class GGUF capacity/current-model route, not as a speed route.
- Nemotron Nano is the practical NVIDIA 30B-class route in this scan.
- The Qwen3-Coder balanced UD row is below the older b9049 96-97 t/s balanced row and below the b9179 98.51 t/s speed-first Q4_K_S headline.
