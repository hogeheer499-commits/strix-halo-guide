# Community GMKtec WSL2/HIP Issue #15

Source: https://github.com/hogeheer499-commits/strix-halo-guide/issues/15

Contributor: mottledMantis.

This directory documents the GMKtec EVO-X2 WSL2/HIP baseline. This is useful Windows/WSL2 evidence, but it is not apples-to-apples with the guide's native Vulkan/RADV rows.

## System

- Device: GMKtec EVO-X2.
- APU: Ryzen AI MAX+ 395 / Radeon 8060S.
- Memory: 96GB LPDDR5X-8000, 80000MB assigned to WSL2.
- OS/kernel: Ubuntu 24.04 LTS on WSL2, kernel `6.6.87.2-microsoft-standard-WSL2`.
- ROCm: 7.2.53211.
- Required WSL2 GPU visibility setting: `HSA_ENABLE_DXG_DETECTION=1`.
- Backend: HIP/ROCm.
- Tool: llama.cpp b9127, commit `a9883db8e`.
- Model: Qwen3.6 35B-A3B UD-Q4_K_M.

## Files

- `benchmark_wsl2_hip_tg512.csv`: raw TG512 generation-only row copied from the issue body.

## Caveats

- Primary confidence is the TG512 generation-only row: 44.051854 t/s.
- The PP512 figure, 538.08 t/s, came from a separate high-variance WSL2 combined run.
- The issue explicitly reports extreme prompt-phase variance on WSL2.
- Vulkan/RADV is unavailable inside WSL2, so this is a HIP/ROCm baseline, not a direct native Vulkan comparison.

## Practical Read

This proves a GMKtec EVO-X2 can run the Qwen3.6 UD-Q4_K_M path through WSL2/HIP, but it also supports the guide's current recommendation: use native Linux Vulkan/RADV first when performance and reproducibility matter.
