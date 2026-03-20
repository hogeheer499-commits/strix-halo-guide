![AMD](https://img.shields.io/badge/AMD-Ryzen_AI_MAX+_395-ED1C24?style=for-the-badge&logo=amd&logoColor=white)
![GPU](https://img.shields.io/badge/GPU-gfx1151_RDNA_3.5-green?style=for-the-badge)
![RAM](https://img.shields.io/badge/RAM-128GB_LPDDR5X--8000-blue?style=for-the-badge)
![Ubuntu](https://img.shields.io/badge/Ubuntu-24.04_LTS-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

# AMD Strix Halo Local LLM Guide

**From unboxing to 70B+ inference on a single APU -- with real benchmarks, tested optimizations, and the things nobody else tells you don't work.**

[Quick Start](#quick-start-6-steps) | [Benchmarks](#benchmark-results) | [Which Backend?](#backend-decision-guide) | [What NOT To Do](#things-that-dont-work-dont-waste-your-time) | [Troubleshooting](#troubleshooting)

---

## Why This Guide Exists

There are several Strix Halo LLM guides out there. This one is different because:

1. **Every number is measured on this machine.** No theoretical estimates, no copy-pasted specs. Every benchmark was run on a Beelink GTR9 Pro with timestamps and exact configuration documented.
2. **We document what does NOT work.** Most guides only tell you what to enable. We spent weeks testing optimizations that turned out to be regressions, driver versions that crash, and kernel parameters that do nothing. That information is harder to find and more valuable.
3. **We track the moving target.** Strix Halo support in ROCm, llama.cpp, and the Linux kernel changes rapidly. This guide is updated with each significant change, noting what broke and what improved.
4. **We compare backends with data.** Vulkan (RADV vs AMDVLK) vs ROCm HIP vs vLLM -- each has strengths at different context lengths and model sizes. We measured them all.

> **Based on findings from:** [kyuz0/amd-strix-halo-toolboxes](https://github.com/kyuz0/amd-strix-halo-toolboxes) (community standard containers), [lhl/strix-halo-testing](https://github.com/lhl/strix-halo-testing) (deepest performance research), and our own extensive testing.

---

## Table of Contents

- [Hardware](#hardware)
- [What You Can Run](#what-you-can-run)
- [Benchmark Results](#benchmark-results)
  - [Ollama Vulkan (RADV)](#ollama-vulkan-radv-mesa-2602)
  - [ROCm HIP (llama.cpp)](#rocm-hip-llamacpp)
  - [Backend Comparison](#backend-comparison-table)
  - [Hardware Comparison](#hardware-comparison)
  - [Long Context Performance](#long-context-performance)
- [Backend Decision Guide](#backend-decision-guide)
- [Quick Start (6 Steps)](#quick-start-6-steps)
- [Phase 1: BIOS Configuration](#phase-1-bios-configuration)
- [Phase 2: Ubuntu 24.04 Installation](#phase-2-ubuntu-2404-installation)
- [Phase 3: Kernel Configuration](#phase-3-kernel-configuration)
- [Phase 4: Performance Tuning](#phase-4-performance-tuning)
- [Phase 5: Ollama Setup (Vulkan)](#phase-5-ollama-setup-vulkan)
- [Phase 6: Benchmarking](#phase-6-benchmarking)
- [Phase 7: ROCm with llama.cpp (Containers)](#phase-7-rocm-with-llamacpp-containers)
- [Phase 8: vLLM Serving](#phase-8-vllm-serving)
- [Phase 9: Multi-Node Clustering (RDMA)](#phase-9-multi-node-clustering-rdma)
- [Phase 10: SSH and Remote Access](#phase-10-ssh-and-remote-access)
- [Vulkan Driver Comparison](#vulkan-driver-comparison)
- [Key Findings and Corrections](#key-findings-and-corrections)
- [Known Issues](#known-issues)
- [Troubleshooting](#troubleshooting)
- [Kernel and ROCm Compatibility](#kernel-and-rocm-compatibility)
- [Testing Checklist](#testing-checklist)
- [Community Resources](#community-resources)
- [Credits and References](#credits-and-references)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [License](#license)

---

## Hardware

### Tested Systems

| System | CPU | GPU | RAM | Notes |
|--------|-----|-----|-----|-------|
| **Beelink GTR9 Pro** | Ryzen AI MAX+ 395 | Radeon 8060S (40 CU) | 128GB LPDDR5X-8000 | This guide's primary test system |
| Framework Desktop 13 | Ryzen AI MAX+ 395 | Radeon 8060S (40 CU) | 128GB LPDDR5X-8000 | Used by kyuz0, lhl |
| GMKtec EVO-X2 | Ryzen AI MAX+ 395 | Radeon 8060S (40 CU) | 128GB LPDDR5X-8000 | [pablo-ross guide](https://github.com/pablo-ross/strix-halo-gmktec-evo-x2) |
| HP ZBook Ultra G1a | Ryzen AI MAX+ 395 | Radeon 8060S (40 CU) | 128GB LPDDR5X-8000 | Workstation laptop |

### Strix Halo Specs

| Component | Spec |
|-----------|------|
| CPU | AMD Ryzen AI MAX+ 395 (32 cores / 64 threads, Zen 5) |
| GPU | Radeon 8060S (gfx1151, RDNA 3.5, 40 CUs) |
| RAM | 128GB unified LPDDR5X-8000 (~215 GB/s measured, 256 GB/s theoretical) |
| NPU | RyzenAI-npu5 (XDNA 2) |

> **Why this hardware?** 128GB unified memory shared between CPU and GPU means you can run **70B+ models entirely on the GPU** -- something an RTX 4090 (24GB VRAM) cannot do. You trade raw bandwidth (~215 GB/s vs ~1 TB/s) for the ability to run much larger, smarter models at a fraction of the cost.

---

## What You Can Run

Real-world model performance measured on the Beelink GTR9 Pro with Ollama Vulkan (RADV Mesa 26.0.2):

| Model | Size | Type | Generation Speed | Use Case |
|-------|------|------|------------------|----------|
| Llama 2 7B | 3.8 GB | Dense | 52.0 t/s | Testing, lightweight tasks |
| Qwen2.5-VL 7B | 6.0 GB | Vision | 21.4 t/s | Image understanding |
| Qwen3.5 35B-A3B | 23 GB | MoE | 47.4-48.0 t/s | General purpose, coding |
| Qwen3-Coder 30B-A3B (Q8_0) | 32 GB | MoE | **51.3-51.4 t/s** | Coding (highest quality MoE) |
| Qwen3-Coder-Next | 51 GB | Dense | 37.9-39.1 t/s | Large dense model |
| Llama 3.3 70B (Q4) | ~40 GB | Dense | ~5 t/s | When you need 70B intelligence |
| gpt-oss-120b | ~70 GB | MoE | ~34-38 t/s | Largest practical model |
| Qwen3-Next 80B-A3B (GPTQ) | ~45 GB | MoE | ~40 t/s | via vLLM, 256K context |
| Kimi K2.5 1T (4-node cluster) | ~500 GB | MoE | distributed | [AMD technical article](https://www.amd.com/en/developer/resources/technical-articles/2026/how-to-run-a-one-trillion-parameter-llm-locally-an-amd.html) |

---

## Benchmark Results

All benchmarks run on 2026-03-20. System: Beelink GTR9 Pro, kernel 6.19.4, tuned accelerator-performance active.

### Ollama Vulkan (RADV Mesa 26.0.2)

**Qwen3.5-35B-A3B** (Q4_K_M, ~23GB, MoE):

| Prompt Tokens | Prompt Eval | Generation | vs Previous (Mesa 26.0.1) |
|---------------|-------------|------------|---------------------------|
| 14 | 121.3 t/s | **48.0 t/s** | tg +4.8% |
| 23 | 182.3 t/s | **47.5 t/s** | tg +4.4% |
| 122 | 456.7 t/s | **47.4 t/s** | tg +4.2% |

**Qwen3-Coder 30B-A3B** (Q8_0, ~32GB, MoE):

| Prompt Tokens | Prompt Eval | Generation | Notes |
|---------------|-------------|------------|-------|
| 12 | 118.3 t/s | **51.4 t/s** | Fastest generation of any model tested |
| 21 | 205.2 t/s | **51.3 t/s** | Higher quality than Q4_K_M |

**Qwen3-Coder-Next** (~51GB, dense):

| Prompt Tokens | Prompt Eval | Generation | vs Previous |
|---------------|-------------|------------|-------------|
| 12 | 90.7 t/s | **39.1 t/s** | tg +2.9% |
| 21 | 129.5 t/s | **38.4 t/s** | tg +3.8% |
| 120 | 301.2 t/s | **37.9 t/s** | NEW |

**Other Models:**

| Model | Size | Prompt Tokens | pp (t/s) | tg (t/s) |
|-------|------|---------------|----------|----------|
| Llama 2 7B | 3.8 GB | 24 | 384.6 | 52.0 |
| Qwen2.5-VL 7B | 6.0 GB | 23 | 81.7 | 21.4 |
| Qwen3.5 35B (no-think) | 23 GB | 14 | 127.1 | 47.4 |

> **What improved?** Mesa 26.0.1 to 26.0.2 plus enabling the `tuned accelerator-performance` profile gave a consistent **+4-5% generation speed improvement** across all models.

### ROCm HIP (llama.cpp)

> **WARNING (March 2026):** Kernel 6.19.x breaks all ROCm containers on Strix Halo. GPU is misidentified as gfx1100 instead of gfx1151, causing segfaults. Stay on kernel 6.18.x for ROCm support. See [Kernel Compatibility](#kernel-and-rocm-compatibility).

**Previous results on kernel 6.18.14** (for reference -- these worked):

| Build | Model | pp128 | pp512 | tg128 |
|-------|-------|-------|-------|-------|
| Self-compiled b8301, FA on, -mmp 0 | Qwen3.5-35B-A3B Q4_K_M | 488 | 996 | 48.8 |
| kyuz0 b8298, FA on | Qwen3.5-35B-A3B Q4_K_M | 306 | 520 | 55.3 |
| kyuz0 b8298, FA off | Qwen3.5-35B-A3B Q4_K_M | 352 | 524 | 53.8 |
| kyuz0 b8189, FA + hipBLASLt | Llama 2 7B Q4_K_M | 1163 | 1261 | 45.07 |

**ROCm vs Vulkan (Qwen3.5-35B-A3B, kernel 6.18.14):**

| Metric | Ollama Vulkan | ROCm HIP (self-compiled) | Difference |
|--------|---------------|--------------------------|------------|
| pp128 | ~267 | 488 | **+83%** |
| pp512 | ~467 | 996 | **+113%** |
| tg128 | 45.8 | 48.8 | **+6.6%** |

ROCm HIP delivers massively faster prompt processing. For generation speed, the difference is smaller.

### Backend Comparison Table

Based on our measurements and [lhl's comprehensive testing](https://github.com/lhl/strix-halo-testing):

| Backend | Best For | pp (relative) | tg (relative) | Context Scaling | Setup Difficulty |
|---------|----------|---------------|---------------|-----------------|------------------|
| Ollama + Vulkan RADV | General use, chat | Good | Good | Degrades at 8K+ | Easy |
| Vulkan AMDVLK | Prompt-heavy workloads | Best (short ctx) | Good | Degrades at 8K+ | Easy |
| ROCm HIP | Batch processing | Excellent | Good | Poor at 32K+ | Hard (containers) |
| ROCm + rocWMMA (tuned) | Long context | Excellent | Best at 32K | **Best scaling** | Very hard |
| vLLM (TheRock) | API serving | Good | Good | Good | Hard |

### Hardware Comparison

| Hardware | Bandwidth | tg (MoE ~30B) | Max Model Size | Price |
|----------|-----------|---------------|----------------|-------|
| RTX 4090 | ~1008 GB/s | 100-122 t/s | 24 GB | ~$1600 GPU only |
| RTX 3090 | ~936 GB/s | 100-112 t/s | 24 GB | ~$800 used |
| Apple M4 Max 128GB | ~546 GB/s | ~100 t/s (MLX) | 128 GB | ~$4000+ |
| **Beelink GTR9 Pro** | **~215 GB/s** | **48-51 t/s** | **120+ GB** | **~$1500-2000** |
| NVIDIA DGX Spark | ~273 GB/s | ~56 t/s | 128 GB | ~$3999 |

> **Key insight:** The Beelink GTR9 Pro delivers **85-91% of the DGX Spark's generation speed at half the price**, while offering 2X better CPU performance (1600 vs 708 GFLOPS Linpack). The DGX Spark wins on prompt processing (2-5X faster). Source: [Framework Community](https://community.frame.work/t/dgx-spark-vs-strix-halo-initial-impressions/77055).

### Long Context Performance

Based on [lhl's measurements](https://github.com/lhl/strix-halo-testing) with gpt-oss-120b (tg32):

| Context | Vulkan AMDVLK | ROCm Standard | ROCm rocWMMA-tuned |
|---------|---------------|---------------|---------------------|
| 2K | 50.05 t/s | 46.56 t/s | 48.97 t/s |
| 4K | 46.11 t/s | 38.25 t/s | 45.42 t/s |
| 8K | 43.15 t/s | 32.65 t/s | 43.55 t/s |
| 16K | 38.46 t/s | 25.50 t/s | 40.91 t/s |
| 32K | 31.54 t/s | 17.82 t/s | **36.43 t/s** |

> At 32K context, standard ROCm drops to 17.82 t/s. Vulkan holds at 31.54 t/s (1.8X faster). But lhl's tuned rocWMMA branch is the **overall winner at 36.43 t/s** -- 2X faster than standard ROCm and 15% faster than Vulkan at 32K.

At extreme context (130K tokens, from [strixhalo.wiki](https://strixhalo.wiki/AI/llamacpp-performance)):

| Backend | pp512 (t/s) | tg128 (t/s) |
|---------|-------------|-------------|
| Vulkan RADV | 17 | 13 |
| ROCm | 41 | 5 |
| ROCm rocWMMA-tuned | 51 | 13 |

---

## Backend Decision Guide

```
                        Which backend should I use?
                                  |
                    Do you need long context (>8K)?
                         /                \
                       NO                  YES
                       |                    |
              Just want it easy?     Context > 32K?
                /          \           /        \
              YES           NO       NO         YES
               |             |        |           |
          Ollama +      Need max    Vulkan     ROCm +
          Vulkan RADV   pp speed?   AMDVLK   rocWMMA-tuned
               |          /    \      |         (lhl's branch)
          "It just       YES    NO    |
           works"         |      |    |
                    ROCm HIP  Vulkan  |
                    (container) AMDVLK|
                                      |
                              Best overall for
                              long context work
```

---

## Quick Start (6 Steps)

For those who want to get running as fast as possible:

1. **BIOS:** Set UMA Frame Buffer to 512MB, disable IOMMU
2. **Install Ubuntu 24.04 LTS**, switch to X11
3. **Kernel params:** Add `amd_iommu=off amdgpu.gttsize=131072 ttm.pages_limit=31457280` to GRUB
4. **Performance:** Install tuned, set `accelerator-performance` profile, upgrade Mesa via kisak PPA
5. **Ollama:** Install, configure Vulkan backend with `OLLAMA_VULKAN=1` and `HIP_VISIBLE_DEVICES=-1`
6. **Test:** `ollama run qwen3.5:35b-a3b` -- expect ~48 t/s generation

Each step is detailed in the phases below.

---

## Phase 1: BIOS Configuration

Do this BEFORE installing the OS.

### Step 1.1: Set UMA Frame Buffer Size

Navigate to `Integrated Graphics` then `UMA Frame Buffer Size` and set to **512MB**.

> **Why?** By default, the BIOS reserves ~97GB for GPU VRAM, leaving only ~31GB visible to the OS. Setting it to 512MB lets the OS see ~125GB RAM. This does NOT reduce GPU performance -- Vulkan uses GTT (system memory) anyway, so the GPU still has access to all 128GB for LLM inference. We benchmarked before and after: **zero speed difference**.

### Step 1.2: Disable IOMMU in BIOS

Find the IOMMU setting and set to **Disabled**.

> **Why?** [lhl's memory bandwidth testing](https://github.com/lhl/strix-halo-testing) shows `amd_iommu=off` gives ~6% better memory reads compared to default (234 vs 221 GB/s). `iommu=pt` (pass-through, recommended by some guides) gives **no benefit** over default. We use `amd_iommu=off` in the kernel command line as well, but disabling in BIOS ensures it's completely off. Only re-enable if you need VFIO/GPU passthrough or RDMA clustering.

---

## Phase 2: Ubuntu 24.04 Installation

### Step 2.1: Install Ubuntu 24.04 LTS

Install Ubuntu 24.04 LTS Desktop with default settings. After installation:

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2.2: Switch to X11

Wayland causes issues with RustDesk, Zoom screen sharing, and some GPU monitoring tools.

```bash
sudo tee -a /etc/gdm3/custom.conf > /dev/null << 'EOF'
WaylandEnable=false
EOF
```

> If the line already exists (commented out), uncomment it instead. Reboot to apply.

---

## Phase 3: Kernel Configuration

### Step 3.1: Kernel Version

> **CRITICAL:** Kernel version matters enormously for Strix Halo.
> - **Kernel 6.18.4+** is the minimum stable version (older kernels have gfx1151 stability bugs)
> - **Kernel 6.19.x** breaks ROCm containers (GPU misidentified as gfx1100) -- see [Known Issues](#known-issues)
> - **Recommended:** Kernel 6.18.6-6.18.14 for full ROCm + Vulkan support

Check your kernel:

```bash
uname -r
```

### Step 3.2: Configure GRUB Boot Parameters

```bash
sudo tee /tmp/grub_update.txt << 'EOF'
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash amd_iommu=off amdgpu.gttsize=131072 ttm.pages_limit=31457280 amdgpu.cwsr_enable=0"
EOF
```

Then edit `/etc/default/grub` and replace the `GRUB_CMDLINE_LINUX_DEFAULT` line with the content above.

| Parameter | Purpose | Impact |
|-----------|---------|--------|
| `amd_iommu=off` | Disable IOMMU completely | +6% memory bandwidth ([lhl](https://github.com/lhl/strix-halo-testing)) |
| `amdgpu.gttsize=131072` | Set GTT (GPU-accessible system memory) to 128GB | Required for large models |
| `ttm.pages_limit=31457280` | Set TTM page limit to ~120GB | Required for large models |
| `amdgpu.cwsr_enable=0` | Disable compute wave save/restore | Not needed for LLM inference |

> **Note:** kyuz0's toolboxes use `iommu=pt` instead of `amd_iommu=off`. We use `off` based on lhl's benchmark data showing ~6% better memory bandwidth. The difference is documented in [kyuz0 issue #66](https://github.com/kyuz0/amd-strix-halo-toolboxes/issues/66). If you need RDMA clustering, use `iommu=pt` instead (RDMA NICs require IOMMU for DMA remapping).

Apply:

```bash
sudo update-grub
```

### Step 3.3: Create AMD GPU Modprobe Configuration

```bash
sudo tee /etc/modprobe.d/amdgpu_llm_optimized.conf > /dev/null << 'EOF'
options amdgpu gttsize=122800
options ttm pages_limit=31457280
options ttm page_pool_size=31457280
EOF
```

Update initramfs:

```bash
sudo update-initramfs -u -k all
```

### Step 3.4: Create udev Rules for GPU Access

```bash
sudo tee /etc/udev/rules.d/99-amd-kfd.rules > /dev/null << 'EOF'
SUBSYSTEM=="kfd", GROUP="render", MODE="0666"
SUBSYSTEM=="drm", KERNEL=="card[0-9]*", GROUP="render", MODE="0666"
SUBSYSTEM=="drm", KERNEL=="renderD[0-9]*", GROUP="render", MODE="0666"
EOF
```

> **IMPORTANT:** The `renderD[0-9]*` rule is critical. Without it, you get `HSA_STATUS_ERROR_OUT_OF_RESOURCES` errors with ROCm.

Add your user to GPU groups:

```bash
sudo usermod -aG render $USER
sudo usermod -aG video $USER
```

Reload and reboot:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
sudo reboot
```

---

## Phase 4: Performance Tuning

### Step 4.1: Install and Configure tuned

```bash
sudo apt install tuned -y
sudo systemctl enable --now tuned
sudo tuned-adm profile accelerator-performance
```

Verify:

```bash
tuned-adm active
# Expected: Current active profile: accelerator-performance
```

> **Impact:** +5-8% overall performance improvement. Memory bandwidth improves from ~221 GB/s to ~234 GB/s write. We measured +4-5% token generation improvement when tuned was running vs not running.

> **WARNING:** tuned may not survive reboots on some systems. Add a check to your `.bashrc` or create a systemd service to verify it's running after boot.

### Step 4.2: Upgrade Mesa Vulkan Drivers

The default Mesa on Ubuntu 24.04 is significantly slower. Upgrade to 26.0.2+:

```bash
sudo add-apt-repository ppa:kisak/kisak-mesa
sudo apt update
sudo apt upgrade -y
```

Verify:

```bash
vulkaninfo --summary 2>&1 | grep driverInfo
# Expected: driverInfo = Mesa 26.0.2 - kisak-mesa PPA
```

> **Impact:** Mesa 25.2.8 to 26.0.1 gave **+9% prompt eval** (87 to 96 t/s). Mesa 26.0.1 to 26.0.2 gave an additional small improvement.

> **Note:** You may see DKMS errors about `mt76-mt7925` during the upgrade. These are harmless -- see [Troubleshooting](#troubleshooting).

### Step 4.3: Verify GPU Clock

The GPU should run at its maximum clock speed (2900 MHz) during inference:

```bash
cat /sys/class/drm/card*/device/pp_dpm_sclk
# Expected: 2: 2900Mhz *  (asterisk on highest clock)
```

> **GPU Clock Bug:** On some kernel/firmware combinations, the GPU gets stuck at 900 MHz, causing ~8% performance loss. If your GPU is not at 2900 MHz during load, see [Troubleshooting](#troubleshooting).

### Step 4.4: Linux Firmware

```bash
dpkg -l | grep linux-firmware | head -5
```

> **CRITICAL:** Do NOT install `linux-firmware-20251125`. It breaks ROCm support on Strix Halo. The safe version is `20240318` or `20260110+`. If you're on 20251125, downgrade immediately.

---

## Phase 5: Ollama Setup (Vulkan)

Ollama is the easiest way to run LLMs on Strix Halo. With the right configuration, it works great.

### Step 5.1: Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Step 5.2: Configure Ollama for Vulkan

> **CRITICAL:** Ollama's bundled ROCm/HIP crashes on gfx1151 with "out of memory" errors, even on small models. You MUST configure Vulkan as the backend.

```bash
sudo systemctl edit ollama
```

Add between the comment lines:

```ini
[Service]
Environment="OLLAMA_VULKAN=1"
Environment="HIP_VISIBLE_DEVICES=-1"
Environment="OLLAMA_FLASH_ATTENTION=1"
Environment="OLLAMA_CONTEXT_LENGTH=8192"
Environment="AMD_VULKAN_ICD=RADV"
Environment="VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json"
Environment="OLLAMA_NUM_BATCH=512"
Environment="OLLAMA_NUM_PARALLEL=1"
```

Restart:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

| Variable | Purpose |
|----------|---------|
| `OLLAMA_VULKAN=1` | Force Vulkan backend (bypasses broken HIP/ROCm) |
| `HIP_VISIBLE_DEVICES=-1` | Disable HIP device enumeration (prevents crash) |
| `OLLAMA_FLASH_ATTENTION=1` | Enable flash attention (+13% prompt processing) |
| `OLLAMA_CONTEXT_LENGTH=8192` | Limit context to prevent OOM (increase if needed) |
| `AMD_VULKAN_ICD=RADV` | Force RADV driver (faster than AMDVLK for general use) |
| `VK_ICD_FILENAMES=...` | Explicitly point to RADV ICD file |
| `OLLAMA_NUM_BATCH=512` | Larger batch size for better throughput |
| `OLLAMA_NUM_PARALLEL=1` | Single request at a time (maximizes single-request speed) |

### Step 5.3: Pull Models

```bash
# Fast MoE model, great for general use and coding (~23GB)
ollama pull qwen3.5:35b-a3b

# Higher quality MoE, Q8_0 quantization (~32GB)
ollama pull qwen3-coder:30b-a3b-q8_0

# Large dense model for complex tasks (~51GB)
ollama pull qwen3-coder-next
```

### Step 5.4: Test

```bash
ollama run qwen3.5:35b-a3b
```

You should see responses generating at ~48 t/s.

---

## Phase 6: Benchmarking

### Step 6.1: Quick Benchmark Script

```bash
tee ~/bench-ollama.sh > /dev/null << 'SCRIPT'
#!/bin/bash
MODEL="${1:-qwen3.5:35b-a3b}"
PROMPT="${2:-hello how are you}"
echo "Model: $MODEL"
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
curl -s http://localhost:11434/api/generate -d "{\"model\":\"$MODEL\",\"prompt\":\"$PROMPT\",\"stream\":false}" | python3 -c "
import sys,json
d=json.load(sys.stdin)
pp=d['prompt_eval_count']/d['prompt_eval_duration']*1e9
tg=d['eval_count']/d['eval_duration']*1e9
print(f'Prompt eval: {pp:.1f} t/s ({d[\"prompt_eval_count\"]} tokens)')
print(f'Generation:  {tg:.1f} t/s ({d[\"eval_count\"]} tokens)')
print(f'Total time:  {d[\"total_duration\"]/1e9:.2f}s')
"
SCRIPT
chmod +x ~/bench-ollama.sh
```

Usage:

```bash
# Default (qwen3.5:35b-a3b, short prompt)
bash ~/bench-ollama.sh

# Specific model with custom prompt
bash ~/bench-ollama.sh qwen3-coder-next "explain backpropagation in simple terms"
```

### Step 6.2: Long Prompt Benchmark

```bash
tee ~/bench-ollama-long.sh > /dev/null << 'SCRIPT'
#!/bin/bash
MODEL="${1:-qwen3.5:35b-a3b}"
echo "Model: $MODEL (long prompt)"
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
curl -s http://localhost:11434/api/generate -d "{\"model\":\"$MODEL\",\"prompt\":\"You are an expert software architect. I need you to review and refactor the following Python code for a web application that handles user authentication, session management, database connections, API rate limiting, error handling, logging, caching with Redis, background job processing with Celery, WebSocket connections for real-time updates, file upload handling with S3 integration, email notification service, payment processing with Stripe, and search functionality with Elasticsearch. Please provide a comprehensive architecture review covering separation of concerns, SOLID principles, design patterns, security best practices, performance optimization, and scalability considerations.\",\"stream\":false}" | python3 -c "
import sys,json
d=json.load(sys.stdin)
pp=d['prompt_eval_count']/d['prompt_eval_duration']*1e9
tg=d['eval_count']/d['eval_duration']*1e9
print(f'Prompt eval: {pp:.1f} t/s ({d[\"prompt_eval_count\"]} tokens)')
print(f'Generation:  {tg:.1f} t/s ({d[\"eval_count\"]} tokens)')
print(f'Total time:  {d[\"total_duration\"]/1e9:.2f}s')
"
SCRIPT
chmod +x ~/bench-ollama-long.sh
```

### Prompt Length Impact on Speed

Prompt processing speed scales with prompt length due to GPU parallelism:

| Prompt Tokens | pp (qwen3.5:35b-a3b) | pp (qwen3-coder-next) |
|---------------|----------------------|-----------------------|
| 12-14 | 121 t/s | 91 t/s |
| 21-23 | 182 t/s | 130 t/s |
| 120-122 | 457 t/s | 301 t/s |

---

## Phase 7: ROCm with llama.cpp (Containers)

For maximum prompt processing performance, use llama.cpp with ROCm via [kyuz0 containers](https://github.com/kyuz0/amd-strix-halo-toolboxes).

> **IMPORTANT:** ROCm requires kernel 6.18.x. Kernel 6.19.x causes segfaults. See [Kernel Compatibility](#kernel-and-rocm-compatibility).

### Step 7.1: Install Distrobox and Podman

```bash
sudo apt install podman -y
curl -s https://raw.githubusercontent.com/89luca89/distrobox/main/install | sudo sh
```

> **Note:** Ubuntu 24.04 does not include `toolbox` in its repos. Use Distrobox instead. The default `toolbox` on Ubuntu also breaks GPU access.

### Step 7.2: Create the ROCm Container

```bash
distrobox create llama-rocm-72 \
  --image docker.io/kyuz0/amd-strix-halo-toolboxes:rocm-7.2 \
  --additional-flags "--device /dev/dri --device /dev/kfd --group-add video --group-add render --group-add sudo --security-opt seccomp=unconfined"
```

### Step 7.3: Enter and Test

```bash
distrobox enter llama-rocm-72
rocm-smi  # Should show your gfx1151 GPU
```

### Step 7.4: Run llama-bench

The container comes with pre-built, optimized llama.cpp binaries:

```bash
export ROCBLAS_USE_HIPBLASLT=1
llama-bench -m ~/models/your-model.gguf -fa 1 -ngl 999 -mmp 0 -p 128,512 -n 128
```

**Critical flags:**

| Flag | Impact | Notes |
|------|--------|-------|
| `-fa 1` | +13% prompt processing | Always use on Strix Halo |
| `-mmp 0` (--no-mmap) | +22% pp128, more stable | **Always** use on Strix Halo |
| `ROCBLAS_USE_HIPBLASLT=1` | +8% token generation | Set in environment |
| `-ngl 999` | Full GPU offload | Use all available VRAM |

> The kyuz0 pre-built binary includes the critical compiler flag `--amdgpu-unroll-threshold-local=600` which works around the [LLVM compiler regression](https://github.com/llvm/llvm-project/issues/147700) in ROCm 7+. Self-compiled binaries without this flag may be significantly slower.

### Step 7.5: Self-Compiling llama.cpp for ROCm

If you need the latest llama.cpp features or want to use lhl's rocWMMA patches:

```bash
# Inside a ROCm container
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp

# Standard build (without rocWMMA)
cmake -B build -S . \
  -DGGML_HIP=ON \
  -DAMDGPU_TARGETS="gfx1151" \
  -DCMAKE_HIP_FLAGS="-mllvm --amdgpu-unroll-threshold-local=600" \
  -DCMAKE_BUILD_TYPE=Release

# With rocWMMA (for long context, use lhl's tuned branch)
cmake -B build -S . \
  -DGGML_HIP=ON \
  -DAMDGPU_TARGETS="gfx1151" \
  -DGGML_HIP_ROCWMMA_FATTN=ON \
  -DCMAKE_HIP_FLAGS="-mllvm --amdgpu-unroll-threshold-local=600" \
  -DCMAKE_BUILD_TYPE=Release

cmake --build build -j$(nproc)
```

> **WARNING:** Do NOT enable `GGML_HIP_ROCWMMA_FATTN=ON` on upstream llama.cpp without lhl's patches. ROCm 7.2 has a [73% performance regression](https://github.com/ggml-org/llama.cpp/issues/19984) with rocWMMA FA enabled. lhl's custom [rocm-wmma-tune branch](https://github.com/lhl/strix-halo-testing) fixes this and delivers 2X better performance at 32K context.

---

## Phase 8: vLLM Serving

[kyuz0's vLLM toolboxes](https://github.com/kyuz0/amd-strix-halo-vllm-toolboxes) enable API serving on gfx1151.

```bash
distrobox create vllm-gfx1151 \
  --image docker.io/kyuz0/vllm-therock-gfx1151:latest \
  --additional-flags "--device /dev/dri --device /dev/kfd --group-add video --group-add render --security-opt seccomp=unconfined"
```

**Known vLLM issues on gfx1151:**

1. **Qwen3.5 block_size validation** ([issue #28](https://github.com/kyuz0/amd-strix-halo-vllm-toolboxes/issues/28)): Hybrid mamba/attention models compute `block_size=1056` which gets rejected by a hardcoded whitelist. Fix available in the issue.
2. **MIOpen encoder hang** ([issue #30](https://github.com/kyuz0/amd-strix-halo-vllm-toolboxes/issues/30)): Vision models hang during kernel search because MIOpen lacks pre-compiled solver DBs for gfx1151. Workaround: disable encoder profiling.

**Tested models on vLLM:**

| Model | Max Context |
|-------|-------------|
| Llama-3.1-8B | 128K |
| Gemma-3-12b | 128K |
| Qwen3-Coder-30B-A3B (GPTQ 4-bit) | 256K |
| gpt-oss-120b | 128K |
| Qwen3-Next-80B-A3B (GPTQ Int4) | 256K |

---

## Phase 9: Multi-Node Clustering (RDMA)

For models that exceed 128GB, you can cluster multiple Strix Halo machines using RDMA.

From [kyuz0's vLLM clustering guide](https://github.com/kyuz0/amd-strix-halo-vllm-toolboxes):

**Hardware needed:**
- 2x Strix Halo machines (e.g., Framework Desktop)
- 2x Intel E810-CQDA1 100GbE NICs
- 1x DAC cable (direct attach copper, no switch needed for 2 nodes)

**Performance:**
- ~50 Gbps bandwidth, ~5 us latency (vs ~70-100 us TCP/IP)
- TP=2 across machines = 256GB unified memory
- Enables trillion-parameter model inference ([AMD article](https://www.amd.com/en/developer/resources/technical-articles/2026/how-to-run-a-one-trillion-parameter-llm-locally-an-amd.html))

**Additional kernel parameter for clustering:**

```
pci=realloc
```

**Network configuration:**

```bash
# Set MTU to 9000 (jumbo frames)
sudo ip link set <interface> mtu 9000
```

---

## Phase 10: SSH and Remote Access

### Step 10.1: Install SSH and fail2ban

```bash
sudo apt install openssh-server fail2ban -y
```

### Step 10.2: Disable Root Login

```bash
sudo sed -i 's/^#*PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart ssh
```

> fail2ban starts automatically and blocks IPs after repeated failed login attempts. We found **68 brute-force attempts** on our system within hours of enabling SSH -- fail2ban is essential.

---

## Vulkan Driver Comparison

We tested both Vulkan drivers on gfx1151 (qwen3-coder-next):

| Driver | Version | Prompt Eval | Generation | Verdict |
|--------|---------|-------------|------------|---------|
| **RADV** | Mesa 25.2.8 | 87 t/s | 38 t/s | Baseline |
| **RADV** | **Mesa 26.0.2** | **~91 t/s** | **39 t/s** | **Best for general use** |
| AMDVLK | 2025.Q2.1 | 83 t/s | 40 t/s | 14% slower pp |

> **Our recommendation:** Use **RADV** for general use. It's more stable and has better prompt processing. AMDVLK has a marginal +2 t/s advantage on generation but loses 14% on prompt eval.

> **However:** [lhl's testing](https://github.com/lhl/strix-halo-testing) shows AMDVLK can be faster on some workloads (especially prompt-heavy tasks on some distros). The relative performance depends on your kernel, Mesa version, and even distro. If you need every last bit of speed, test both on your system.

To install AMDVLK for comparison:

```bash
wget -O amdvlk.deb https://github.com/GPUOpen-Drivers/AMDVLK/releases/download/v-2025.Q2.1/amdvlk_2025.Q2.1_amd64.deb
sudo dpkg -i amdvlk.deb
```

To force RADV when both are installed: `AMD_VULKAN_ICD=RADV`

**Optimal ubatch sizes per driver** (from lhl's testing):
- AMDVLK: `-ub 512`
- RADV: `-ub 1024`
- ROCm HIP: `-ub 2048`

---

## Key Findings and Corrections

> These findings correct several common recommendations found in other Strix Halo guides.

### Things That DON'T Work (Don't Waste Your Time)

| Issue | Common Advice | Reality | What Happens If You Try |
|-------|---------------|---------|------------------------|
| Ollama HIP/ROCm | "Use ROCm backend" | Crashes with OOM on gfx1151 | `out of memory` error, even on 7B models |
| `iommu=pt` for speed | "Use pass-through for performance" | No benefit over default ([lhl](https://github.com/lhl/strix-halo-testing)) | Same speed as `iommu=on`, wastes a kernel param |
| rocWMMA on upstream llama.cpp | "Enable for 2x speed" | [73% regression](https://github.com/ggml-org/llama.cpp/issues/19984) on ROCm 7.2 | Massively slower prompt processing |
| BIOS VRAM increase for speed | "More GPU VRAM = faster" | Zero speed difference | OS sees less RAM, no benefit |
| ROCm 7.0 RC | "Use ROCm 7 RC" | Segfaults on kernel 6.18.14+ | `HSA_STATUS_ERROR` crash |
| Kernel 6.19.x with ROCm | "Use latest kernel" | GPU misidentified as gfx1100 | All ROCm containers segfault |
| linux-firmware-20251125 | Auto-update | Breaks ROCm on Strix Halo | Instability, crashes |

### Things That DO Work

| Optimization | Impact | How |
|-------------|--------|-----|
| Mesa 25.2.8 to 26.0.2 | **+9-10% pp** | `sudo add-apt-repository ppa:kisak/kisak-mesa` |
| Flash Attention | **+13% pp** | `-fa 1` or `OLLAMA_FLASH_ATTENTION=1` |
| `--no-mmap` (disable mmap) | **+22% pp128** | `-mmp 0` in llama.cpp, always use on Strix Halo |
| hipBLASLt | **+8% tg** | `ROCBLAS_USE_HIPBLASLT=1` (ROCm only) |
| tuned accelerator-performance | **+5-8% overall** | `sudo tuned-adm profile accelerator-performance` |
| RADV over AMDVLK | **+14% pp** | `AMD_VULKAN_ICD=RADV` |
| `amd_iommu=off` | **+6% memory bandwidth** | GRUB parameter |
| BIOS VRAM to 512MB | OS sees 125GB vs 31GB | No speed change, but required for usability |
| `HIP_VISIBLE_DEVICES=-1` | Fixes Ollama crash | Required for Vulkan-only mode |
| LLVM unroll workaround | Restores ROCm 7+ perf | `-mllvm --amdgpu-unroll-threshold-local=600` |
| lhl's rocWMMA-tuned | **2X tg at 32K context** | Custom branch, requires manual build |

---

## Known Issues

### Kernel 6.19.x Breaks ROCm (NEW -- March 2026)

**Symptoms:** All ROCm containers segfault. `ggml_cuda_init` reports `gfx1100 (0x1100)` instead of `gfx1151`.

**Affected:** All ROCm versions (6.4.4, 7.2, nightlies), all llama.cpp builds.

**Not affected:** Ollama Vulkan continues to work fine.

**Workaround:** Stay on kernel 6.18.x for ROCm. Vulkan-only workflows work on 6.19.x.

### Qwen3.5 ROCm Hang Bug ([ROCm #6027](https://github.com/ROCm/ROCm/issues/6027))

**Symptoms:** Qwen3.5 models (35B-A3B and 27B) hang during `load_tensors` on ROCm. CPU pegs at 99.9%.

**Status:** Open. AMD confirmed working with TheRock 7.13.0a20260316+ nightlies.

**Workaround:** Use very conservative flags: `--batch-size 128 --ubatch-size 32 --flash-attn off --n-gpu-layers 1`

### GPU Clock Bug

**Symptoms:** GPU stays at 900 MHz instead of 2900 MHz, causing ~8% performance loss.

**Check:**

```bash
cat /sys/class/drm/card*/device/pp_dpm_sclk
# Should show: 2: 2900Mhz *
```

**Fix:** Force highest performance level:

```bash
echo high | sudo tee /sys/class/drm/card*/device/power_dpm_force_performance_level
```

### GFX1151 1.5X VGPR Capacity

Newer kernels (6.18.4+) recognize gfx1151's 1.5X VGPR capacity compared to standard gfx11 chips. This enables better occupancy for compute shaders. If you're on an older kernel, you may not be getting full performance.

---

## Troubleshooting

<details>
<summary><strong>DKMS mt7925 WiFi Errors During apt install</strong></summary>

You'll see this on every `apt install`:

```
Error! Bad return status for module build on kernel: 6.18.14-061814-generic
dkms autoinstall failed for mt76-mt7925(10)
```

**This is harmless.** WiFi works fine via the kernel driver. To permanently silence:

```bash
sudo dkms remove mt76-mt7925/1.5.0 --all
```

</details>

<details>
<summary><strong>Ollama "Out of Memory" Even with Small Models</strong></summary>

This happens when Ollama tries to use HIP/ROCm instead of Vulkan:

```bash
# Check current Ollama environment
systemctl show ollama | grep Environment

# Fix: ensure these are set
sudo systemctl edit ollama
# Add: OLLAMA_VULKAN=1, HIP_VISIBLE_DEVICES=-1
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

</details>

<details>
<summary><strong>ROCm Container Segfaults (Kernel 6.19.x)</strong></summary>

If your ROCm containers crash immediately with segfaults:

1. Check kernel: `uname -r` -- if 6.19.x, this is the issue
2. Options:
   - Use Ollama Vulkan instead (no ROCm needed)
   - Downgrade to kernel 6.18.x for ROCm support
   - Wait for ROCm/kernel fix

```bash
# List installed kernels
dpkg --list | grep linux-image

# Boot into a specific kernel via GRUB
# Hold Shift during boot -> Advanced Options -> Select kernel
```

</details>

<details>
<summary><strong>Verifying GPU Memory Configuration</strong></summary>

```bash
# Check TTM pages limit
cat /sys/module/ttm/parameters/pages_limit

# Check GTT size
cat /sys/module/amdgpu/parameters/gttsize

# Check Vulkan driver
vulkaninfo --summary 2>&1 | grep -E "driverName|driverInfo"

# Check OS-visible RAM
free -h

# Check GPU memory allocation
for file in /sys/class/drm/card*/device/mem_info*; do
  echo "$file: $(cat $file)"
done
```

</details>

<details>
<summary><strong>rocm-smi Shows Wrong VRAM</strong></summary>

For APUs with unified memory, `mem_info_vram_total` showing ~1GB is **normal**. The actual compute memory is in GTT, which should show ~128GB.

</details>

<details>
<summary><strong>tuned Not Running After Reboot</strong></summary>

```bash
# Check status
tuned-adm active

# If not running:
sudo systemctl enable --now tuned
sudo tuned-adm profile accelerator-performance

# Verify it persists
tuned-adm active
```

</details>

<details>
<summary><strong>GPU Stuck at Low Clock Speed</strong></summary>

```bash
# Check current clock
cat /sys/class/drm/card*/device/pp_dpm_sclk

# If not on highest (2900Mhz):
echo high | sudo tee /sys/class/drm/card*/device/power_dpm_force_performance_level

# To make persistent, add to /etc/rc.local or a udev rule
```

</details>

---

## Kernel and ROCm Compatibility

Based on community testing and our own findings:

| Kernel | ROCm 6.4.4 | ROCm 7.2 | ROCm 7 Nightly | Vulkan (Ollama) |
|--------|------------|----------|----------------|-----------------|
| 6.17.7 | Works (with right firmware) | Unknown | Works | Works |
| 6.18.4-6.18.14 | Works (patched) | Works | Works | Works |
| **6.19.4** | **Segfault** | **Segfault** | **Unknown** | **Works** |

**Key rules:**
- Kernel 6.18.4+ has a fix that breaks ALL older ROCm versions
- Kernel 6.19.x misidentifies gfx1151 as gfx1100, breaking all ROCm
- linux-firmware-20251125 breaks ROCm regardless of kernel
- linux-firmware-20260110+ is safe

> **Our current recommendation (March 2026):** Use kernel 6.18.6-6.18.14 for full ROCm + Vulkan support. Use kernel 6.19.x only if you exclusively use Vulkan.

---

## Testing Checklist

After completing setup, verify each item:

- [ ] `free -h` shows ~124GB total RAM
- [ ] `vulkaninfo --summary` shows RADV Mesa 26.0.2+
- [ ] `tuned-adm active` shows `accelerator-performance`
- [ ] `cat /sys/class/drm/card*/device/pp_dpm_sclk` shows 2900Mhz with asterisk
- [ ] `cat /sys/module/ttm/parameters/pages_limit` shows 31457280
- [ ] `ollama --version` returns without error
- [ ] `ollama run qwen3.5:35b-a3b "hello"` generates at 45+ t/s
- [ ] `systemctl show ollama | grep Environment` includes `OLLAMA_VULKAN=1`
- [ ] `cat /etc/default/grub | grep CMDLINE` includes `amd_iommu=off`
- [ ] `uname -r` shows 6.18.x (if using ROCm) or 6.19.x (if Vulkan-only)
- [ ] `dpkg -l | grep linux-firmware` does NOT show 20251125

---

## Community Resources

- [kyuz0/amd-strix-halo-toolboxes](https://github.com/kyuz0/amd-strix-halo-toolboxes) -- Community standard containers for llama.cpp (1.2k+ stars)
- [kyuz0/amd-strix-halo-vllm-toolboxes](https://github.com/kyuz0/amd-strix-halo-vllm-toolboxes) -- vLLM serving + RDMA clustering
- [kyuz0/amd-strix-halo-gfx1151-toolboxes](https://github.com/kyuz0/amd-strix-halo-gfx1151-toolboxes) -- Meta repository with all toolboxes
- [kyuz0 Backend Benchmarks Dashboard](https://kyuz0.github.io/amd-strix-halo-toolboxes/) -- Interactive benchmark comparison
- [lhl/strix-halo-testing](https://github.com/lhl/strix-halo-testing) -- Deep performance research and rocWMMA patches
- [strixhalo.wiki](https://strixhalo.wiki/AI/llamacpp-with-ROCm) -- Community wiki
- [llm-tracker.info](https://llm-tracker.info/AMD-Strix-Halo-(Ryzen-AI-Max+-395)-GPU-Performance) -- GPU performance comparison
- [Level1Techs Forum](https://forum.level1techs.com/t/strix-halo-ryzen-ai-max-395-llm-benchmark-results/233796) -- Community benchmark results
- [Framework Community](https://community.frame.work/t/pytorch-w-flash-attention-vllm-for-strix-halo/74736) -- Framework Desktop discussions
- [ROCm Strix Halo Optimization Guide](https://rocm.docs.amd.com/en/latest/how-to/system-optimization/strixhalo.html) -- Official AMD guide

---

## Credits and References

- [kyuz0](https://github.com/kyuz0) -- Maintainer of the Strix Halo toolbox ecosystem, community standard containers
- [lhl](https://github.com/lhl) -- Deep performance research, rocWMMA patches, IOMMU/bandwidth testing
- [pablo-ross](https://github.com/pablo-ross/strix-halo-gmktec-evo-x2) -- Original GMKtec EVO-X2 setup guide
- [TechnigmaAI / Hardware Corner](https://www.hardware-corner.net/strix-halo-llm-optimization/) -- Alternative optimization guide
- [AMD](https://www.amd.com/en/developer/resources/technical-articles/2026/how-to-run-a-one-trillion-parameter-llm-locally-an-amd.html) -- Trillion-parameter LLM clustering article
- [Lychee-Technology](https://github.com/Lychee-Technology/llama-cpp-for-strix-halo) -- Pre-built llama.cpp binaries for gfx1151
- [kisak-mesa PPA](https://launchpad.net/~kisak/+archive/ubuntu/kisak-mesa) -- Latest Mesa drivers for Ubuntu
- [GPUOpen-Drivers/AMDVLK](https://github.com/GPUOpen-Drivers/AMDVLK) -- AMD open-source Vulkan driver

---

## Contributing

Found something that's wrong, outdated, or missing?

1. Open an issue with your hardware, kernel version, and benchmark results
2. PRs welcome -- especially from other Strix Halo systems (Framework, GMKtec, HP ZBook)
3. If you find a new optimization, include before/after benchmarks

---

## Changelog

### 2026-03-20 -- Major Rewrite

- Complete rewrite with live benchmarks on current system
- Added: Kernel 6.19.x breaks ROCm (GPU misidentified as gfx1100)
- Added: Mesa 26.0.2 results (+4-5% tg improvement over 26.0.1)
- Added: qwen3-coder:30b-a3b-q8_0 benchmarks (51.4 t/s -- fastest model)
- Added: Long context performance data from lhl (Vulkan vs ROCm at 32K)
- Added: rocWMMA status update (upstream broken, lhl's tuned branch works)
- Added: vLLM setup and known issues
- Added: RDMA clustering section
- Added: Kernel/ROCm compatibility matrix
- Added: linux-firmware-20251125 warning
- Added: LLVM compiler regression workaround
- Added: Qwen3.5 ROCm hang bug (ROCm #6027)
- Added: Backend decision guide
- Added: Testing checklist
- Added: Collapsible troubleshooting sections
- Updated: ROCm HIP is now broken on kernel 6.19.4 (was working on 6.18.14)
- Updated: All benchmark numbers re-measured
- Updated: Replaced `nano` instructions with `tee` for copy-paste ready commands
- Corrected: rocWMMA is no longer blanket "don't use" -- lhl's tuned branch is best for long context
- Corrected: `iommu=pt` has no benefit -- use `amd_iommu=off` instead

### Initial Release

- Basic setup guide based on pablo-ross' GMKtec guide
- Ollama Vulkan configuration
- ROCm container setup

---

## Upcoming

- **Gorgon Halo** (Ryzen AI Max 400, Q4 2026): Same architecture, higher clocks
- **Medusa Halo** (Ryzen AI Max 500): LPDDR6, ~80% more memory bandwidth
- **Lemonade 10.0** (March 2026): First Linux NPU support for LLM inference via FastFlowLM
- **AMD Variable Graphics Memory** (Windows): Up to 128B parameter models in Vulkan llama.cpp

---

## License

MIT
