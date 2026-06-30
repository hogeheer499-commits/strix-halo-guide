# llama.cpp b9851 Vulkan Sentinel

Purpose: check the newest official `llama.cpp` b9851 Ubuntu Vulkan release
binary against local Strix Halo / Radeon 8060S direct `llama-bench` sentinel
routes.

This is first-party Beelink GTR9 Pro evidence. It is direct `llama-bench`
Vulkan/RADV evidence, not `llama-server`, not Ollama, and not MTP/speculative
decoding.

## Build And Host

- System: Beelink GTR9 Pro
- APU: AMD Ryzen AI MAX+ 395 / Radeon 8060S
- Memory: 128GB unified memory
- OS/kernel: Ubuntu 24.04, `6.19.4-061904-generic`
- Mesa/RADV: Mesa 26.1.3 kisak, RADV `STRIX_HALO`
- Tool: official `llama.cpp` b9851 Ubuntu Vulkan x64 release binary
- Build reported by CSV: `0eca4d490`, build `9851`
- Device: explicit `-dev Vulkan0`
- Host state: T3 was left running. Known browser/VM/media/backend noise was
  paused where possible; root RustDesk service remained present.

The first dry run used an invalid `VK_ICD_FILENAMES` path and failed before a
benchmark. Published CSV rows below use the working automatic RADV loader plus
explicit `-dev Vulkan0`.

## Results

| Model | Quant | Shape | Result | Raw CSV |
| --- | --- | --- | ---: | --- |
| Qwen3-Coder 30B-A3B | `Q4_K_S` | pp512/tg128 r50 | 1423.05 pp512 / 100.99 tg128 | [`qwen3-coder-q4ks-b9851-p512-n128-r50.csv`](qwen3-coder-q4ks-b9851-p512-n128-r50.csv) |
| Qwen3-Coder 30B-A3B | `Q4_K_S` | p0/tg128 r50 | 100.74 tg128 | [`qwen3-coder-q4ks-b9851-p0-n128-r50.csv`](qwen3-coder-q4ks-b9851-p0-n128-r50.csv) |
| Qwen3-Coder 30B-A3B | `Q4_K_S` | pp512/tg128 r10 | 1412.48 pp512 / 99.85 tg128 | [`qwen3-coder-q4ks-b9851-r10.csv`](qwen3-coder-q4ks-b9851-r10.csv) |
| Qwen3-Coder 30B-A3B | `UD-Q4_K_XL` | pp512/tg128 r5 | 1416.79 pp512 / 99.55 tg128 | [`qwen3-coder-udq4kxl-b9851-r5.csv`](qwen3-coder-udq4kxl-b9851-r5.csv) |
| Gemma 4 26B-A4B IT | `UD-Q4_K_M` | pp512/tg128 r5 | 1326.52 pp512 / 55.45 tg128 | [`gemma4-26b-a4b-udq4km-b9851-r5.csv`](gemma4-26b-a4b-udq4km-b9851-r5.csv) |

## Interpretation

- The exact Qwen3-Coder `Q4_K_S` speed-first route crossed 100 t/s on the
  official b9851 Vulkan release binary.
- This is now the strongest direct Qwen3-Coder speed-first row in the guide.
- The older b9179 strict-clean 98.51 t/s row remains useful historical context
  because it was the earlier cleaned host-state claim and has exact evidence.
- `UD-Q4_K_XL` also improved versus older balanced rows in this short r5 check,
  but it should be treated as a latest-build control until a longer repeat is
  needed.
- Gemma 4 26B-A4B direct b9851 is not a new speed headline. The existing Gemma
  4 26B-A4B QAT MTP route remains the useful high-throughput Gemma path.

## Command Shape

```bash
/home/hoge-heer/benchmark-tools/llama-b9851/llama-b9851/llama-bench \
  -m /path/to/model.gguf \
  -dev Vulkan0 -fa on -ngl 999 -mmp 0 -b 2048 -ub 512 \
  -p 512 -n 128 -r 50 -o csv
```

Host/device snapshot: [`host-snapshot.txt`](host-snapshot.txt)
