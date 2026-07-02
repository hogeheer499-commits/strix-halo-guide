# llama.cpp b9859 Vulkan Sentinel

Purpose: check the latest observed official `llama.cpp` b9859 Ubuntu Vulkan
release binary against the guide's current measured b9851 sentinel rows.

## Environment

- Hardware: Beelink GTR9 Pro / Ryzen AI MAX+ 395 / Radeon 8060S
- Backend: direct `llama-bench` with Vulkan/RADV
- Tool: official `llama.cpp` b9859 Ubuntu Vulkan x64 release binary
- Build: `4fc4ec554`, build number `9859`
- Device: explicit `-dev Vulkan0`
- Matching b9851 command shape:
  - `-fa on`
  - `-ngl 999`
  - `-mmp 0`
  - `-b 2048`
  - `-ub 512`

Host state is in [`host-snapshot.txt`](host-snapshot.txt).

## Comparable Results

| Model | Quant | Shape | Result | Evidence |
| --- | --- | --- | ---: | --- |
| Qwen3-Coder 30B-A3B | `Q4_K_S` | pp512/tg128 r50 | 1413.38 pp512 / 98.48 tg128 | [`qwen3-coder-q4ks-b9859-faon-mmp0-p512-n128-r50.csv`](qwen3-coder-q4ks-b9859-faon-mmp0-p512-n128-r50.csv) |
| Qwen3-Coder 30B-A3B | `Q4_K_S` | p0/tg128 r50 | 99.09 tg128 | [`qwen3-coder-q4ks-b9859-faon-mmp0-p0-n128-r50.csv`](qwen3-coder-q4ks-b9859-faon-mmp0-p0-n128-r50.csv) |
| Qwen3-Coder 30B-A3B | `UD-Q4_K_XL` | pp512/tg128 r5 | 1411.76 pp512 / 97.01 tg128 | [`qwen3-coder-udq4kxl-b9859-faon-mmp0-r5.csv`](qwen3-coder-udq4kxl-b9859-faon-mmp0-r5.csv) |
| Gemma 4 26B-A4B IT | `UD-Q4_K_M` | pp512/tg128 r5 | 1323.39 pp512 / 54.18 tg128 | [`gemma4-26b-a4b-udq4km-b9859-faon-mmp0-r5.csv`](gemma4-26b-a4b-udq4km-b9859-faon-mmp0-r5.csv) |

## Interpretation

- b9859 is usable on Strix Halo with the official Ubuntu Vulkan release binary.
- b9859 does not replace the b9851 Qwen3-Coder speed-first headline. The b9851
  official-release row remains stronger at 100.99 tg128 r50.
- The b9859 Qwen3-Coder `Q4_K_S` fair rerun still reproduces the older
  98-99 t/s class and is useful as a current-runtime control.
- Gemma 4 direct remains secondary to the Gemma QAT/MTP server route for
  throughput.

## Non-Comparable Scout Files

The first b9859 pass was accidentally run without the b9851 command shape
(`-fa on -mmp 0`). Those files are kept only as raw context and should not be
used for the comparable b9859 claim:

- `qwen3-coder-q4ks-b9859-p512-n128-r50.csv`
- `qwen3-coder-q4ks-b9859-p0-n128-r50.csv`
- `qwen3-coder-udq4kxl-b9859-r5.csv`
- `gemma4-26b-a4b-udq4km-b9859-r5.csv`
