# Nemotron Nano Omni MXFP4 `llama.cpp` b10034 Sentinel

Purpose: re-run the existing NVIDIA Nemotron 3 Nano Omni MXFP4 artifact on the
current official `llama.cpp` Vulkan release without changing the model or the
direct benchmark shape.

## Scope

- Hardware: Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S, 128GB unified memory
- Backend: Vulkan/RADV
- Runtime: official `llama.cpp` b10034, commit `505b1ed15`
- Model: `NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-MXFP4_MOE.gguf`
- Model source revision: `571758804835f56154718683f5c0e388b7d0fef9`
- Model SHA-256: see `model.sha256`
- Shape: direct `llama-bench`, `pp512/tg128`, three repeats, full GPU offload

## Result

| Runtime | pp512 | tg128 |
|---|---:|---:|
| b9747 (2026-06-21 control) | 1277.60 t/s | 56.56 t/s |
| b10034 (2026-07-16) | 1286.15 t/s | 64.26 t/s |

The current runtime is about 13.6% faster on generation for this exact model
artifact and benchmark shape. This is a useful runtime-maintenance result, not a
claim that every FP4 model or workload improved by the same amount.

This run only validates the language-model artifact. It does not test the
separate multimodal projector or claim image/audio correctness.

## Evidence

- `command.txt`: exact command
- `llama-bench.csv`: machine-readable result
- `llama-bench.stderr.txt`: loader/backend output
- `llama-version.txt`: runtime version and device inventory
- `host-snapshot.txt`: host and Vulkan context
- `model.sha256`: exact model identity

