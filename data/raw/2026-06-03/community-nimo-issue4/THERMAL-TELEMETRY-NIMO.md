# Nimo AI Mini PC Supplemental Telemetry

This is a separate telemetry note for the Nimo AI Mini PC / Strix Halo bench
that can be plugged in when fan, temperature, and power numbers matter.

## System Summary

| Field | Value |
|---|---|
| Model | Nimo AI Mini PC |
| CPU | AMD Ryzen AI Max+ 395 (Strix Halo) |
| GPU | AMD Radeon 8060S |
| RAM | 128GB LPDDR5X (121Gi visible) |
| Storage | 2TB NVMe SSD |
| OS | Linux Mint 22.3 / Ubuntu 24.04 |
| Driver | Mesa 25.2.8 / ROCm 7.8.0 |

## AI Inference Telemetry

| Field | Value |
|---|---|
| Model | Mistral-Medium-128B-Q4_K_M (~75GB) |
| Generation speed | 1.57 tok/sec sustained |
| VRAM utilization | 79Gi unified memory |
| Peak power | 145.0W (prefill / bursts) |
| Peak noise | 46 dBA |
| Note | Entire 128B model was offloaded to the iGPU with about 40Gi remaining for context |

## Gaming / Graphics Telemetry

| Benchmark | Setting | Result |
|---|---|---|
| DOOM Eternal | 2560 x 1440, Ultra Nightmare | 137-144 FPS stable |
| Unigine Superposition | 4K Optimized | 7900 score, 59.1 FPS average |

## Hardware / Thermal Telemetry

| Metric | Idle | Peak |
|---|---:|---:|
| System power | 6.1W | 154.1W |
| Temperature | 40.9C | 88.0C GPU / 88.5C CPU |
| Fan noise | 27 dBA | 46 dBA |
| Max GPU clock | - | 2900 MHz |
| Max CPU load | - | 42.4% |
| Max VRAM used | - | 79 GB |

## Applied Fixes

- RAM carve-out: adjusted BIOS UMA settings to unlock the full 128GB (121Gi
  visible).
- Driver initialization: removed `amdgpu` from the modprobe blacklist for ROCm
  support.
- Optimizations: used `HIPFIRE_MMQ=1` and `HSA_OVERRIDE_GFX_VERSION=11.0.13`.

## Usage Note

Use this file when the benchmark submission wants fan, noise, temperature, or
power data. Leave it out when the target repo only wants model/runtime rows.
