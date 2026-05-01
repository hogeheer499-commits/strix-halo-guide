# System Audit - 2026-05-01

This file records the current live system state. It is separate from historical benchmark state: older benchmark numbers were measured with the same `tuned accelerator-performance` profile active.

## Hardware

| Component | Value |
|-----------|-------|
| System | Beelink GTR9 Pro |
| CPU | AMD Ryzen AI MAX+ 395 (16C/32T, Zen 5) |
| GPU | Radeon 8060S (gfx1151, RDNA 3.5 iGPU) |
| RAM | 128GB LPDDR5X-8000 unified, 124GiB OS-visible |
| Vulkan device | Radeon 8060S Graphics (RADV STRIX_HALO) |

## Live Software State

| Parameter | Current Value | Status |
|-----------|---------------|--------|
| Kernel | 6.19.4-061904-generic | Current tested kernel |
| Mesa RADV | 26.0.6, kisak-mesa PPA | Current Vulkan driver |
| AMDVLK | Not installed | Correct; avoids ICD hijacking |
| Ollama | 0.21.2 | Current easy path |
| linux-firmware | 20240318.git3b128b60-0ubuntu2.27 | Safe; not broken 20251125 |
| tuned | `accelerator-performance` active | Correct |
| GPU clock | 2900 MHz selected | Correct |

## CPU and Memory

Live `lscpu` summary:

```text
CPU(s): 32
Model name: AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
Thread(s) per core: 2
Core(s) per socket: 16
Socket(s): 1
```

Live memory:

```text
Mem: 124Gi total, 111Gi available
Swap: 8.0Gi total, 0B used
```

## Vulkan Drivers

Live `vulkaninfo --summary` reports:

```text
deviceName = Radeon 8060S Graphics (RADV STRIX_HALO)
driverName = radv
driverInfo = Mesa 26.0.6 - kisak-mesa PPA
```

No `amdvlk` package is installed. This is intentional. Earlier test sessions found that AMDVLK's ICD file could silently override RADV and create false pp-regression results.

## Benchmark Readiness

Before running or publishing new benchmarks, verify:

```bash
sudo systemctl enable --now tuned
sudo tuned-adm profile accelerator-performance
tuned-adm active
vulkaninfo --summary 2>&1 | grep driverInfo
cat /sys/class/drm/card*/device/pp_dpm_sclk
dpkg -l | grep -E 'amdvlk|linux-firmware'
```

Expected state:

- `tuned-adm active` shows `accelerator-performance`
- RADV Mesa is 26.0.2+; current live system is 26.0.6
- AMDVLK is absent
- GPU clock has the asterisk on `2900Mhz`
- linux-firmware is not `20251125`

## ROCm Status

ROCm is not "all broken" on kernel 6.19.x anymore. It works when these variables are set before ROCm/HIP commands:

```bash
export HSA_OVERRIDE_GFX_VERSION=11.5.1
export HSA_ENABLE_SDMA=0
```

Current measured comparison from the guide:

| Backend / Build | pp512 | tg128 | Notes |
|-----------------|-------|-------|-------|
| Vulkan RADV, llama.cpp b8460 | 1080 | 64.85 | Fastest measured short-context MoE path |
| ROCm HIP, llama.cpp b8460, HSA fix | 1047 | 54.67 | Works, but slower tg on this workload |

## Action Items Before New Tests

1. Keep `tuned accelerator-performance` active before every benchmark run.
2. Create a single benchmark dataset file before adding more runs.
3. Treat existing March/April numbers as historical snapshots unless the same command is re-run under the verified May 2026 state.
