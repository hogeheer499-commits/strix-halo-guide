# llama.cpp b9544 Vulkan Regression Check

Date: 2026-06-07

Purpose: check whether current `llama.cpp` b9544 regresses the guide's most important direct Vulkan/RADV sentinel rows.

System: Beelink GTR9 Pro, AMD Ryzen AI MAX+ 395 / Radeon 8060S, 128GB unified memory.

Build:

- `llama.cpp` tag: `b9544`
- commit: `98d5e8ba8`
- build: local Vulkan build in `/home/hoge-heer/llama.cpp-b9544/build-vulkan`
- device: explicit `-dev Vulkan0`

Important note:

The first automatic-device attempts selected CPU in the CSV and were removed from this raw directory. The committed CSVs below are the valid Vulkan/RADV rows; each has `backends=Vulkan`, `gpu_info=Radeon 8060S Graphics (RADV STRIX_HALO)`, and `devices=Vulkan0`.

## Results

| Model | Quant | Reps | Result |
| --- | --- | ---: | --- |
| Qwen3-30B-A3B-Instruct-2507 | `IQ4_XS` | r10 | 1438.10 pp512 / 103.18 tg128 |
| Qwen3-Coder 30B-A3B | `UD-Q4_K_XL` | r5 | 1399.98 pp512 / 97.08 tg128 |
| LFM2.5 8B-A1B | `Q4_K_M` | r10 | 3398.36 pp512 / 176.48 tg128 |
| Nemotron 3 Super 120B-A12B | `UD-IQ4_XS` | r3 | 297.14 pp512 / 18.93 tg128 |

## Interpretation

This is a latest-build control, not a replacement for every older headline row.

- Qwen3-30B-A3B-Instruct-2507 remains above 100 t/s on b9544.
- Qwen3-Coder `UD-Q4_K_XL` remains in the 96-97 t/s balanced range.
- LFM2.5 and Nemotron Super did not show a b9544 regression in these checks.
- The exact Qwen3-Coder `Q4_K_S` file used for the older 98.51 t/s speed-first headline was not present locally, so it was not rerun here to avoid a fresh large download on a low-disk system.

T3 remained reachable after the benchmark run; see `t3-after-vulkan-runs.json`.
