# Qwen3-Coder On AMD Strix Halo: Direct llama.cpp Vulkan/RADV Benchmark Evidence


## Summary

This page isolates the Qwen3-Coder Strix Halo benchmark rows so they are easy to cite without mixing direct `llama-bench`, API serving, and speculative server results.

Measured primary system:

- Beelink GTR9 Pro
- AMD Ryzen AI MAX+ 395
- Radeon 8060S / `gfx1151`
- 128GB unified memory
- Ubuntu + Vulkan/RADV

## Current Direct Rows

| Model | Quant | Tool | Backend | Result | Evidence |
|-------|-------|------|---------|--------|----------|
| Qwen3-Coder 30B-A3B | Q4_K_S | `llama-bench` b9179 | Vulkan/RADV | 98.51 t/s tg128; 1396.11 pp512 | `data/raw/2026-05-16/break-97-24-strict-noise-settings/b9179-q4-k-s-r50.csv` |
| Qwen3-Coder 30B-A3B | UD-Q4_K_XL | `llama-bench` b9049 | Vulkan/RADV | 96.76 t/s tg128; 1320.52 pp512 | `data/raw/2026-05-07/max-performance-campaign/benchmarks/qwen3-coder-top-confirm-r20/guide.csv` |

The Q4_K_S row is a speed-first lower-quality quant candidate. The UD-Q4_K_XL row is the balanced row to use when quality tradeoff matters.

## Reproduce The Balanced Row

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
~/llama-cpp-upstream-2026-05-07/build-vulkan/bin/llama-bench \
  -m ~/models/Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf \
  -fa 1 -ngl 999 -mmp 0 -p 0 -n 128 -r 20 -o csv
```

## What To Include In A Reproduction

- device and memory size
- BIOS UMA and IOMMU setting
- OS/kernel
- Mesa/RADV version
- `llama.cpp` build/commit
- model source, filename, quant, and hash if available
- exact command
- raw CSV output
- power profile, thermals, and background load if known

## Caveats

- These rows are local measurements from one primary Beelink system.
- Community reproductions belong in `COMMUNITY_RESULTS.md` unless promoted with clear scope.
- Do not call the MTP route a direct Qwen3-Coder benchmark.
- Do not compare to Nvidia/Apple/other systems without matching model, quant, backend, context, and command.

## Links

- Headline claim index: `data/headline_claims.csv`
- Reproducibility: `REPRODUCIBILITY.md`
- Community results: `COMMUNITY_RESULTS.md`
- Benchmark issue template: `https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=benchmark-report.md`
