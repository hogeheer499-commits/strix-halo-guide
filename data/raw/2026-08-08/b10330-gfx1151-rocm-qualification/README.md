# llama.cpp b10330 gfx1151 ROCm Qualification

First-party Beelink GTR9 Pro qualification from 2026-08-08. This campaign
checks whether the official b10330 source can build and produce coherent,
repeatable output through the ROCm/HIP backend on the Radeon 8060S
(`gfx1151`). It is not a speed comparison between HIP and Vulkan.

## Result

- `test-llama-archs qwen3next` passed on the HIP build with an NMSE around
  `9.59e-14`, both with the default environment and with
  `GGML_CUDA_ENABLE_UNIFIED_MEMORY=1`.
- The practical 43 GiB Qwen3-Next 80B-A3B target produced coherent output in
  five default HIP repeats at `50.39-50.99 t/s`.
- `--no-mmap` and `HIP_LAUNCH_BLOCKING=1` controls also produced coherent
  output in the same roughly `50-51 t/s` class.
- The Vulkan control produced coherent output at `59.81-61.65 t/s`, but the
  exact generated text varied between repeats. This campaign did not force a
  deterministic sampler, so text hashes are not a HIP-versus-Vulkan quality
  comparison.
- The practical-model run with
  `GGML_CUDA_ENABLE_UNIFIED_MEMORY=1` repeatedly returned short corrupted
  fragments even though the tiny architecture test passed. Therefore this
  environment variable is **not** a safe generic Strix Halo recommendation.

The useful conclusion is narrow: b10330 HIP works on the measured `gfx1151`
system without an architecture override, but the unified-memory override must
not be inferred safe from a tiny synthetic test alone.

## Scope And Conditions

- System: Beelink GTR9 Pro, Ryzen AI MAX+ 395, Radeon 8060S, 128 GB
- Kernel: 7.0.0-28-generic
- `llama.cpp`: b10330 commit
  `687e7789271ec1276e3470f158428e11a4f80b6f`
- Model: `Qwen3-Next-80B-A3B-Instruct-UD-Q4_K_XL.gguf`
- Model SHA-256: recorded in `model-sha256.txt`
- Background state: practical workstation qualification; see
  `host-snapshot-before.txt`

## Evidence Map

- `test-llama-archs-*.log`: small architecture correctness controls.
- `real-model-default-repeats.csv`: five default HIP responses and hashes.
- `real-model-hip-launch-blocking-repeats.csv`: synchronization control.
- `real-model-unified-memory-repeats.csv`: repeatable corrupt-output failure.
- `real-model-vulkan-repeats.csv`: Vulkan performance/output control.
- Corresponding `*.json` and `*.server.log` files: raw responses and runtime
  diagnostics.
