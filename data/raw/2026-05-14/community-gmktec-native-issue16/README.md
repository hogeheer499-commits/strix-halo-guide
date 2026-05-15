# Community GMKtec Native Ubuntu Issue #16

Source: https://github.com/hogeheer499-commits/strix-halo-guide/issues/16

Contributor: mottledMantis.

This directory stores the raw CSV attachments for the first GMKtec EVO-X2 native Ubuntu Vulkan/RADV reproduction in the guide.

## System

- Device: GMKtec EVO-X2.
- APU: Ryzen AI MAX+ 395 / Radeon 8060S.
- Memory: 96GB LPDDR5X-8000.
- BIOS UMA: 1GB.
- IOMMU: enabled, translated mode.
- OS/kernel: Ubuntu 26.04 LTS, kernel 7.0.0-15-generic.
- Mesa: RADV 26.0.3-1ubuntu1.
- Backend: llama.cpp Vulkan/RADV b9156, commit `834a24366`.
- Model: `unsloth/Qwen3.6-35B-A3B-GGUF`, `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`.
- Model SHA256: `ac0e2c1189e055faa36eff361580e79c5bd6f8e76bffb4ce547f167d53e31a61`.

## Files

- `benchmark_native_vulkan_b9156.csv`: primary native Ubuntu Vulkan/RADV run, `pp512=1050.820405`, `tg128=61.524843`.
- `benchmark_native_vulkan_b9156_tuned.csv`: `accelerator-performance` rerun, `pp512=1035.688807`, `tg128=60.590845`.

## Why It Matters

The guide's Beelink GTR9 Pro b9049 Qwen3.6 UD-Q4_K_M row is `pp512=1059.45`, `tg128=62.56`.

The GMKtec primary run is:

- -0.8% on pp512
- -1.7% on tg128

That is strong cross-vendor portability evidence for the native Linux Vulkan/RADV setup. It also shows that 96GB GMKtec EVO-X2 systems can land in the same performance class as the guide's 128GB Beelink row for this model and command shape.
