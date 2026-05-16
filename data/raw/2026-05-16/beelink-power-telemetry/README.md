# Beelink Power Telemetry - 2026-05-16

This directory stores local Beelink GTR9 Pro amdgpu `PPT` telemetry captured with `scripts/sample_power.py`.

Important scope:

- This is kernel-exposed amdgpu/APU telemetry, not wall power.
- Use it for same-machine relative comparisons only.
- Do not mix these watts with community smart-plug wall-power rows as if they measure the same thing.
- The services that normally add benchmark noise were paused, but the normal workspace session stayed active.

Structured summary:

- [`data/beelink_power_telemetry.csv`](../../../beelink_power_telemetry.csv)

Files:

- `idle-paused-services-amdgpu-power.csv`: 60-sample idle run with benchmark-noise services paused.
- `qwen3-coder-30b-vulkan-r20.csv`: Qwen3-Coder llama-bench output.
- `qwen3-coder-30b-vulkan-r20-amdgpu-power.csv`: power samples during that run.
- `qwen36-q4km-vulkan-r20.csv`: Qwen3.6 Q4_K_M llama-bench output.
- `qwen36-q4km-vulkan-r20-amdgpu-power.csv`: power samples during that run.
- `*-timing.env`: UTC start/end markers for matching benchmark windows to power samples.
