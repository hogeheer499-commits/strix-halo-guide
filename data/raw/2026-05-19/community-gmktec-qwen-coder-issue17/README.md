# Community GMKtec Qwen3-Coder Issue #17

Source: https://github.com/hogeheer499-commits/strix-halo-guide/issues/17

Contributor: mottledMantis.

This directory stores the raw CSV row for the GMKtec EVO-X2 Qwen3-Coder 30B-A3B UD-Q4_K_XL follow-up.

## System

- Device: GMKtec EVO-X2.
- APU: Ryzen AI MAX+ 395 / Radeon 8060S.
- Memory: 96GB LPDDR5X-8000.
- BIOS UMA: 1GB.
- IOMMU: disabled.
- OS/kernel: Ubuntu 26.04 LTS, kernel 7.0.0-15-generic.
- Mesa: RADV 26.0.3-1ubuntu1.
- Backend: llama.cpp Vulkan/RADV b9235, commit `d14ce3dab`.
- Model: `unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF`, `Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf`.
- Model SHA256: `2841aa314d916434860cfb8990347528dcdfe5c350dbcb9d1461dbee88ff2533`.

## File

- `qwen3_coder_ud_q4_k_xl_b9235_generation_only.csv`: generation-only `-p 0 -n 128 -r 20` row, `tg128=92.108999`.

## Why It Matters

This is the first GMKtec EVO-X2 native Vulkan/RADV Qwen3-Coder UD-Q4_K_XL row in the guide. It should not replace the Beelink headline because it is generation-only and uses b9235 rather than the Beelink b9049 headline stack.

The practical value is still high:

- it extends the GMKtec evidence from Qwen3.6 to Qwen3-Coder
- it shows Qwen3-Coder UD-Q4_K_XL remains in the same performance class on GMKtec
- it gives readers a realistic b9235/Ubuntu 26.04/Mesa 26.0.3 GMKtec number instead of assuming every Strix Halo box lands exactly on the Beelink row
- it reinforces the guide's claim hygiene: community rows validate portability, but local headline rows stay separate
