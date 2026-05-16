# Lucebox DFlash/PFlash Preflight - 2026-05-16

This directory records the local preflight for the Lucebox DFlash/PFlash Strix Halo route.

Source checked:

- <https://github.com/Luce-Org/lucebox-hub>
- Local cloned commit: `6fe0d9a0a9b79855cc56967a60f6d35a5532cdd7`

Why it matters:

- Lucebox documents an AMD Strix Halo/gfx1151 HIP path for Qwen3.5/Qwen3.6 27B DFlash/PFlash.
- Their README reports 37 tok/s DFlash decode on Qwen3.5-27B Q4_K_M and a 2.66x end-to-end speedup over vanilla llama.cpp HIP on a 16K prompt + 1K generation workload.
- That is a different workload from this guide's Vulkan/RADV Qwen3-Coder/Qwen3.6 generation headlines, so it cannot be promoted without local reproduction.

Local result:

- Clone and submodule checkout succeeded.
- CMake HIP configuration failed because the host has no ROCm root / `hipcc` developer stack:
  - `Failed to find ROCm root directory.`

Interpretation:

- Keep Lucebox as a high-value experimental route.
- Do not install ROCm dev packages into the host just to test it.
- Next safe step is an isolated ROCm/HIP dev container or toolbox with hipcc and rocWMMA, then download the 27B target/draft models only inside that test lane.
