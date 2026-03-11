# Optimal Ubuntu 24.04 Setup Roadmap for Beelink GTR9 Pro (Ryzen AI MAX+ 395)

A complete, tested guide for turning the Beelink GTR9 Pro into a local LLM inference machine. Based on real benchmarks and extensive testing — including things that **don't work** so you don't waste time.

> **Based on:** [pablo-ross/strix-halo-gmktec-evo-x2](https://github.com/pablo-ross/strix-halo-gmktec-evo-x2) — rewritten with corrections and additional findings for the Beelink GTR9 Pro.

## Hardware

| Component | Spec |
|-----------|------|
| CPU | AMD Ryzen AI MAX+ 395 (32 cores / 64 threads, Zen 5) |
| GPU | Radeon 8060S (gfx1151, RDNA 3.5 integrated GPU) |
| RAM | 128GB unified memory (~215 GB/s bandwidth) |
| WiFi | MediaTek MT7925 (mt7925e) |
| Storage | NVMe SSD |

> **Why this hardware?** 128GB unified memory shared between CPU and GPU means you can run **50GB+ models entirely on the GPU** — something an RTX 4090 (24GB VRAM) cannot do. You trade raw speed (~215 GB/s vs ~1 TB/s) for the ability to run much larger, smarter models.

## Benchmark Results

### Ollama + Vulkan (RADV Mesa 26.0.1)

**Qwen3.5-35B-A3B** (Q4_K_M, ~23GB):

| Prompt Length | Prompt Eval | Generation |
|--------------|-------------|------------|
| 56 tokens | 267 t/s | 45.8 t/s |
| 201 tokens | 467 t/s | 45.5 t/s |

**Qwen3-Coder-Next** (Q4_K_M, ~51GB):

| Prompt Length | Prompt Eval | Generation |
|--------------|-------------|------------|
| 12 tokens | 96 t/s | 38 t/s |
| 54 tokens | 136 t/s | 37 t/s |

### llama.cpp via ROCm 7.2 (kyuz0 container)

**Llama 2 7B** (Q4_K_M, 3.80 GiB) with Flash Attention + hipBLASLt:

| pp128 | pp256 | pp512 | pp1024 | tg128 |
|-------|-------|-------|--------|-------|
| 1163 | 1199 | 1261 | 1256 | 45.07 |

### How This Compares

| Hardware | Bandwidth | Generation (t/s) | Max Model Size | Price |
|----------|-----------|-------------------|----------------|-------|
| RTX 4090 | ~1008 GB/s | 100-122 | 24 GB | ~$1600 GPU only |
| RTX 3090 | ~936 GB/s | 100-112 | 24 GB | ~$800 used |
| Apple M4 Max | ~546 GB/s | ~100 (MLX) | 128 GB | ~$4000+ |
| **Beelink GTR9 Pro** | **~215 GB/s** | **45.8** | **120+ GB** | **~$1500-2000** |
| NVIDIA DGX Spark | ~273 GB/s | 38 | 128 GB | ~$3000 |

> The GTR9 Pro **beats the $3000 DGX Spark** on token generation and runs 51GB models that don't fit on any consumer GPU.

---

## Phase 1: BIOS Configuration (BEFORE OS Installation)

### Step 1.1: Set UMA Frame Buffer Size

This is the most important BIOS setting.

- Navigate to: `Integrated Graphics` → `UMA Frame Buffer Size`
- Set to: **512MB**

> **Why?** By default, the BIOS reserves ~97GB for GPU VRAM, leaving only ~31GB visible to the OS. Setting it to 512MB lets the OS see ~125GB RAM. This does **NOT** reduce GPU performance — Vulkan uses GTT (system memory) anyway, so the GPU still has access to all 128GB for LLM inference. We benchmarked before and after: **zero speed difference**.

### Step 1.2: Disable IOMMU

- Find IOMMU setting in BIOS
- Set to: **Disabled**

> Only re-enable if you need VFIO/GPU passthrough later.

---

## Phase 2: Ubuntu 24.04 Base Installation

### Step 2.1: Install Ubuntu 24.04 LTS

Install Ubuntu 24.04 LTS Desktop with default settings. After installation:

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2.2: Switch to X11 (Disable Wayland)

Wayland causes issues with RustDesk, Zoom screen sharing, and some GPU applications.

```bash
sudo nano /etc/gdm3/custom.conf
```

Under `[daemon]`, uncomment or add:

```
WaylandEnable=false
```

Reboot to apply.

---

## Phase 3: Kernel Configuration

### Step 3.1: Configure GRUB Boot Parameters

```bash
sudo nano /etc/default/grub
```

Set `GRUB_CMDLINE_LINUX_DEFAULT` to:

```
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash amd_iommu=off amdgpu.gttsize=131072 ttm.pages_limit=31457280 amdgpu.cwsr_enable=0"
```

| Parameter | Purpose |
|-----------|---------|
| `amd_iommu=off` | Disable IOMMU for lower overhead |
| `amdgpu.gttsize=131072` | Set GTT (GPU-accessible system memory) to 128GB |
| `ttm.pages_limit=31457280` | Set TTM page limit to ~120GB |
| `amdgpu.cwsr_enable=0` | Disable compute wave save/restore (not needed for LLM inference) |

Apply:

```bash
sudo update-grub
```

### Step 3.2: Create AMD GPU Modprobe Configuration

```bash
sudo nano /etc/modprobe.d/amdgpu_llm_optimized.conf
```

Add:

```
options amdgpu gttsize=122800
options ttm pages_limit=31457280
options ttm page_pool_size=31457280
```

Update initramfs:

```bash
sudo update-initramfs -u -k all
```

### Step 3.3: Create udev Rules for GPU Access

```bash
sudo nano /etc/udev/rules.d/99-amd-kfd.rules
```

Add:

```
SUBSYSTEM=="kfd", GROUP="render", MODE="0666"
SUBSYSTEM=="drm", KERNEL=="card[0-9]*", GROUP="render", MODE="0666"
SUBSYSTEM=="drm", KERNEL=="renderD[0-9]*", GROUP="render", MODE="0666"
```

> **IMPORTANT:** The `renderD[0-9]*` rule is critical. Without it, you'll get `HSA_STATUS_ERROR_OUT_OF_RESOURCES` errors.

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
```

Expected: `Current active profile: accelerator-performance`

> **Impact:** +5-8% overall performance improvement.

### Step 4.2: Upgrade Mesa Vulkan Drivers

The default Mesa on Ubuntu 24.04 (25.2.x) is significantly slower than newer versions. Upgrade to 26.0.1+:

```bash
sudo add-apt-repository ppa:kisak/kisak-mesa
```

```bash
sudo apt update
```

```bash
sudo apt upgrade -y
```

Verify:

```bash
vulkaninfo --summary 2>&1 | grep driverInfo
```

Expected: `driverInfo = Mesa 26.0.1 - kisak-mesa PPA`

> **Impact:** Mesa 25.2.8 → 26.0.1 gave **+9% improvement** on prompt eval (87 → 96 t/s).

> **Note:** You may see DKMS errors about `mt76-mt7925` during the upgrade. These are harmless — WiFi works via the kernel driver. See [Troubleshooting](#troubleshooting) to silence them.

---

## Phase 5: Ollama Setup (Recommended for Most Users)

Ollama is the easiest way to run LLMs locally. With the right configuration, it works great on Strix Halo.

### Step 5.1: Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Step 5.2: Configure Ollama for Vulkan

> **CRITICAL:** Ollama's bundled ROCm/HIP **crashes on gfx1151** with "out of memory" errors, even on small models. You MUST configure Vulkan as the backend.

```bash
sudo systemctl edit ollama
```

Add the following content between the comment lines:

```ini
[Service]
Environment="OLLAMA_VULKAN=1"
Environment="HIP_VISIBLE_DEVICES=-1"
Environment="OLLAMA_FLASH_ATTENTION=1"
Environment="OLLAMA_CONTEXT_LENGTH=8192"
Environment="AMD_VULKAN_ICD=RADV"
Environment="OLLAMA_NUM_BATCH=256"
```

Save (Ctrl+O, Enter) and exit (Ctrl+X), then restart:

```bash
sudo systemctl daemon-reload
```

```bash
sudo systemctl restart ollama
```

| Variable | Purpose |
|----------|---------|
| `OLLAMA_VULKAN=1` | Force Vulkan backend (bypasses broken HIP/ROCm) |
| `HIP_VISIBLE_DEVICES=-1` | Disable HIP device enumeration (prevents crash) |
| `OLLAMA_FLASH_ATTENTION=1` | Enable flash attention for faster prompt processing |
| `OLLAMA_CONTEXT_LENGTH=8192` | Limit context to prevent memory over-allocation |
| `AMD_VULKAN_ICD=RADV` | Force RADV driver (faster than AMDVLK — see [Driver Comparison](#driver-comparison)) |
| `OLLAMA_NUM_BATCH=256` | Larger batch size for better throughput on long prompts |

### Step 5.3: Pull Models

```bash
# Fast MoE model, great for coding (~23GB)
ollama pull qwen3.5:35b-a3b

# Larger, smarter model (~51GB, slower generation)
ollama pull qwen3-coder-next
```

### Step 5.4: Test

```bash
ollama run qwen3.5:35b-a3b
```

You should see responses generating at ~45 t/s.

---

## Phase 6: Benchmarking

### Step 6.1: Quick Benchmark Script

Create `~/bench-ollama.sh`:

```bash
#!/bin/bash
MODEL="${1:-qwen3.5:35b-a3b}"
PROMPT="${2:-hello how are you}"
curl -s http://localhost:11434/api/generate -d "{\"model\":\"$MODEL\",\"prompt\":\"$PROMPT\",\"stream\":false}" | python3 -c "
import sys,json
d=json.load(sys.stdin)
pp=d['prompt_eval_count']/d['prompt_eval_duration']*1e9
tg=d['eval_count']/d['eval_duration']*1e9
print(f'Prompt eval: {pp:.2f} t/s ({d[\"prompt_eval_count\"]} tokens)')
print(f'Generation: {tg:.2f} t/s ({d[\"eval_count\"]} tokens)')
"
```

Usage:

```bash
# Default model (qwen3.5:35b-a3b)
bash ~/bench-ollama.sh

# Specific model
bash ~/bench-ollama.sh qwen3-coder-next
```

### Step 6.2: Realistic Benchmark (Long Prompt)

> **IMPORTANT:** Short prompts (< 20 tokens) heavily bottleneck prompt eval speed due to low GPU utilization. Always benchmark with realistic prompt lengths.

Create `~/bench-ollama-long.sh`:

```bash
#!/bin/bash
MODEL="${1:-qwen3.5:35b-a3b}"
curl -s http://localhost:11434/api/generate -d "{\"model\":\"$MODEL\",\"prompt\":\"You are an expert software architect. I need you to review and refactor the following Python code for a web application. The code handles user authentication, session management, database connections, API rate limiting, error handling, logging, caching with Redis, background job processing with Celery, WebSocket connections for real-time updates, file upload handling with S3 integration, email notification service, payment processing with Stripe, search functionality with Elasticsearch, GraphQL API endpoints, OAuth2 integration with Google and GitHub, two-factor authentication with TOTP, audit logging for compliance, data export functionality in CSV and PDF formats, automated testing with pytest fixtures, CI/CD pipeline configuration, Docker containerization, Kubernetes deployment manifests, monitoring with Prometheus metrics, and distributed tracing with OpenTelemetry. Please provide a comprehensive architecture review covering separation of concerns, SOLID principles, design patterns, security best practices, performance optimization, scalability considerations, and maintainability improvements. Include specific code examples for each recommendation.\",\"stream\":false}" | python3 -c "
import sys,json
d=json.load(sys.stdin)
pp=d['prompt_eval_count']/d['prompt_eval_duration']*1e9
tg=d['eval_count']/d['eval_duration']*1e9
print(f'Prompt eval: {pp:.2f} t/s ({d[\"prompt_eval_count\"]} tokens)')
print(f'Generation: {tg:.2f} t/s ({d[\"eval_count\"]} tokens)')
"
```

### Prompt Length Impact

| Prompt Length | Prompt Eval (qwen3-coder-next) | Prompt Eval (qwen3.5-35b-a3b) |
|--------------|-------------------------------|-------------------------------|
| 12 tokens | 96 t/s | ~245 t/s |
| 54 tokens | 136 t/s | ~267 t/s |
| 201 tokens | — | 467 t/s |

---

## Phase 7: Advanced — ROCm with llama.cpp (Container)

For maximum prompt processing performance, use llama.cpp with ROCm via the [kyuz0 containers](https://github.com/kyuz0/amd-strix-halo-toolboxes).

### Step 7.1: Install Distrobox and Podman

```bash
sudo apt install podman -y
```

```bash
curl -s https://raw.githubusercontent.com/89luca89/distrobox/main/install | sudo sh
```

> **Note:** Ubuntu 24.04 does not include `toolbox` in its repos. Use **Distrobox** instead.

### Step 7.2: Create the ROCm 7.2 Container

```bash
distrobox create llama-rocm-72 \
  --image docker.io/kyuz0/amd-strix-halo-toolboxes:llama-rocm-72 \
  --additional-flags "--device /dev/dri --device /dev/kfd --group-add video --group-add render --group-add sudo --security-opt seccomp=unconfined"
```

### Step 7.3: Enter and Test

```bash
distrobox enter llama-rocm-72
```

Inside the container:

```bash
rocm-smi  # Should show your gfx1151 GPU
```

### Step 7.4: Run llama-bench

The container comes with a pre-built, optimized llama.cpp binary:

```bash
export ROCBLAS_USE_HIPBLASLT=1
cd ~/llama.cpp
./build/bin/llama-bench -m ~/models/your-model.gguf -fa 1 -ngl 999
```

> **Important:** The pre-built kyuz0 binary uses the critical compiler flag `--amdgpu-unroll-threshold-local=600`. Self-compiled binaries without this flag are ~5% slower.

> **Important:** `ROCBLAS_USE_HIPBLASLT=1` + `-fa 1` gives **+13% prompt processing** and **+8% token generation**.

---

## Phase 8: SSH Security (Optional)

If you want remote access to your machine:

### Step 8.1: Install SSH and fail2ban

```bash
sudo apt install openssh-server fail2ban -y
```

### Step 8.2: Disable Root Login

```bash
sudo nano /etc/ssh/sshd_config
```

Find and set:

```
PermitRootLogin no
```

Restart SSH:

```bash
sudo systemctl restart ssh
```

> fail2ban starts automatically and blocks IPs after repeated failed login attempts. We found **68 brute-force attempts** on our system within hours of enabling SSH — fail2ban is essential.

---

## Driver Comparison

We extensively tested both Vulkan drivers on gfx1151:

| Driver | Version | Prompt Eval | Generation | Verdict |
|--------|---------|-------------|------------|---------|
| **RADV** | Mesa 25.2.8 | 87 t/s | 38 t/s | Baseline |
| **RADV** | **Mesa 26.0.1** | **96 t/s** | **38 t/s** | **Best overall** |
| AMDVLK | 2025.Q2.1 | 83 t/s | 40 t/s | Slower prompt eval |

**Conclusion:** Use **RADV (Mesa 26.0.1+)**. Despite [some reports](https://www.hardware-corner.net/strix-halo-llm-optimization/) that AMDVLK is faster, our testing shows AMDVLK is **14% slower for prompt processing** on gfx1151. AMDVLK has a marginal +2 t/s advantage on generation, but this does not compensate.

To install AMDVLK for your own testing:

```bash
wget -O amdvlk.deb https://github.com/GPUOpen-Drivers/AMDVLK/releases/download/v-2025.Q2.1/amdvlk_2025.Q2.1_amd64.deb
sudo dpkg -i amdvlk.deb
```

To force RADV when AMDVLK is installed, set `AMD_VULKAN_ICD=RADV`.

---

## Key Findings & Corrections

> **These findings correct several common recommendations found in other Strix Halo guides.**

### Things That DON'T Work (Don't Waste Your Time)

| Issue | Detail | Common Advice | Reality |
|-------|--------|---------------|---------|
| rocWMMA | **25% REGRESSION** on ROCm 7.2 + gfx1151 | "Enable for 2x speed" | 980 vs 1291 t/s — do NOT enable |
| Ollama HIP/ROCm | Crashes with "out of memory" on gfx1151 | "Use ROCm backend" | Use Vulkan instead |
| AMDVLK | 14% slower prompt eval than RADV | "AMDVLK is fastest" | RADV Mesa 26.0.1 is faster |
| ROCm 7.0 RC | Segfaults on kernel 6.18.14 | "Use ROCm 7 RC" | Use ROCm 7.2 |
| BIOS VRAM for speed | No speed difference after change | "More GPU VRAM = faster" | Vulkan uses GTT anyway |

### Things That DO Work

| Optimization | Impact | Notes |
|-------------|--------|-------|
| Mesa 25.2.8 → 26.0.1 | **+9%** prompt eval | kisak PPA |
| Flash Attention | **+13%** prompt processing | `-fa 1` or `OLLAMA_FLASH_ATTENTION=1` |
| hipBLASLt | **+8%** token generation | `ROCBLAS_USE_HIPBLASLT=1` (ROCm only) |
| tuned accelerator-performance | **+5-8%** overall | `sudo tuned-adm profile accelerator-performance` |
| RADV over AMDVLK | **+14%** prompt eval | `AMD_VULKAN_ICD=RADV` |
| BIOS VRAM → 512MB | OS sees 125GB instead of 31GB | No speed change, but makes system usable |
| `HIP_VISIBLE_DEVICES=-1` | Fixes Ollama crash | Required for Vulkan-only mode |

---

## Troubleshooting

### DKMS mt7925 WiFi Errors During apt install

You'll see this on every `apt install`:

```
Error! Bad return status for module build on kernel: 6.18.14-061814-generic
dkms autoinstall failed for mt76-mt7925(10)
```

**This is harmless.** WiFi works fine via the kernel-built driver. To permanently silence:

```bash
sudo dkms remove mt76-mt7925/1.5.0 --all
```

### Ollama "Out of Memory" Even with Small Models

This happens when Ollama tries to use HIP/ROCm instead of Vulkan:

```bash
sudo systemctl edit ollama
# Ensure OLLAMA_VULKAN=1 and HIP_VISIBLE_DEVICES=-1 are set
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

### Verifying GPU Memory Configuration

```bash
# Check TTM pages limit
cat /sys/module/ttm/parameters/pages_limit

# Check GTT size (bytes)
cat /sys/module/amdgpu/parameters/gttsize

# Check Vulkan driver in use
vulkaninfo --summary 2>&1 | grep -E "driverName|driverInfo"

# Check OS-visible RAM
free -h
```

### rocm-smi Shows Wrong VRAM

For APUs with unified memory, `mem_info_vram_total` showing ~1GB is **normal**. The actual compute memory is in GTT, which should show ~128GB. Check with:

```bash
for file in /sys/class/drm/card*/device/mem_info*; do
  echo "$file: $(cat $file)"
done
```

### tuned Not Running After Reboot

```bash
sudo systemctl enable --now tuned
sudo tuned-adm profile accelerator-performance
```

---

## Credits & References

- [pablo-ross/strix-halo-gmktec-evo-x2](https://github.com/pablo-ross/strix-halo-gmktec-evo-x2) — Original Strix Halo setup guide (GMKtec EVO-X2)
- [kyuz0/amd-strix-halo-toolboxes](https://github.com/kyuz0/amd-strix-halo-toolboxes) — ROCm containers for Strix Halo
- [lhl/strix-halo-testing](https://github.com/lhl/strix-halo-testing) — Comprehensive Strix Halo benchmarks
- [Level1Techs Forum](https://forum.level1techs.com/t/strix-halo-ryzen-ai-max-395-llm-benchmark-results/233796) — Community benchmark results
- [Hardware Corner](https://www.hardware-corner.net/strix-halo-llm-optimization/) — Strix Halo LLM optimization guide
- [kisak-mesa PPA](https://launchpad.net/~kisak/+archive/ubuntu/kisak-mesa) — Latest Mesa drivers for Ubuntu
- [GPUOpen-Drivers/AMDVLK](https://github.com/GPUOpen-Drivers/AMDVLK) — AMD open-source Vulkan driver

---

## License

MIT
