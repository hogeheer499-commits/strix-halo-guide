# Optimal Ubuntu 24.04 Setup Roadmap for Beelink GTR9 Pro (Ryzen AI MAX+ 395)

A complete, tested guide for turning the Beelink GTR9 Pro into a local LLM inference machine. Based on real benchmarks and extensive testing — including things that **don't work** so you don't waste time.

> **Based on:** [pablo-ross/strix-halo-gmktec-evo-x2](https://github.com/pablo-ross/strix-halo-gmktec-evo-x2) — rewritten with corrections and additional findings for the Beelink GTR9 Pro.

## Hardware

| Component | Spec |
|-----------|------|
| CPU | AMD Ryzen AI MAX+ 395 (32 cores / 64 threads, Zen 5) |
| GPU | Radeon 8060S (gfx1151, RDNA 3.5 integrated GPU) |
| RAM | 128GB LPDDR5X-8000 unified memory (~256 GB/s bandwidth) |
| NPU | XDNA 2 (126 AI TOPS) |
| TDP | 140W (dual-turbine fans + vapor chamber, 32dB) |
| Storage | 2TB NVMe PCIe 4.0 (up to 7000 MB/s), dual M.2 slots |
| Connectivity | Dual 10GbE LAN, Dual USB4 (40Gbps), HDMI 2.1, DP 2.1 |
| WiFi | MediaTek MT7925 (mt7925e) |
| PSU | Built-in 230W |
| Price | [$2,699 USD](https://www.bee-link.com/products/beelink-gtr9-pro-amd-ryzen-ai-max-395) |

> **Why this hardware?** 128GB unified memory shared between CPU and GPU means you can run **50GB+ models entirely on the GPU** — something an RTX 4090 (24GB VRAM) cannot do. You trade raw speed (~256 GB/s vs ~1 TB/s) for the ability to run much larger, smarter models. The 140W TDP with vapor chamber cooling means no thermal throttling during sustained inference.

## Benchmark Results

All benchmarks: GPU clocks forced high (2900 MHz), `--no-mmap`, `ROCBLAS_USE_HIPBLASLT=1`, Flash Attention on.

### Qwen3.5-35B-A3B (Q4_K_M, 19.92 GiB) — Full Comparison

| Backend | Binary | pp64 | pp128 | pp256 | pp512 | pp1024 | pp2048 | tg128 | tg256 | tg512 |
|---------|--------|------|-------|-------|-------|--------|--------|-------|-------|-------|
| **ROCm 7.2 HIP** | Self-compiled (b8301) | 473 | 504 | 735 | **996** | **929** | **919** | 48.5 | — | — |
| **ROCm 6.4.4 HIP** | kyuz0 pre-built (b8298) | 436 | **472** | **680** | 672 | 653 | 828 | 52.0 | 51.8 | 52.1 |
| **ROCm 7.2 HIP** | kyuz0 pre-built (b8298) | 452 | 348 | 440 | 507 | 499 | 488 | **55.6** | **54.8** | **55.0** |
| **Ollama Vulkan** | RADV Mesa 26.0.1 | — | ~224 | — | ~467 | — | — | 45.8 | — | — |

> **Key finding: ROCm 6.4.4 gives +33% faster prompt processing** than ROCm 7.2 with the same pre-built binary (672 vs 507 t/s at pp512), but **-6.5% slower generation** (52.0 vs 55.6 t/s). Self-compiled ROCm 7.2 still has the best prompt processing (996 t/s) due to custom compiler optimizations.

> **Choose your backend:**
> - **Interactive chat** (fast responses): ROCm 7.2 kyuz0 pre-built → **55.6 t/s generation**
> - **RAG / long context**: Self-compiled ROCm 7.2 → **996 t/s prompt processing**
> - **Balanced workload**: ROCm 6.4.4 kyuz0 pre-built → good at both (672 pp512, 52 tg128)
> - **Easy setup**: Ollama Vulkan → 45.8 t/s, no containers needed

### Ubatch Size Impact (Qwen3.5-35B-A3B, ROCm 7.2 kyuz0)

| ubatch | pp512 (t/s) | tg128 (t/s) | Notes |
|--------|-------------|-------------|-------|
| 128 | 288 | 54.9 | Too small for MoE |
| 256 | 389 | 54.4 | Good balance |
| **512** | **507** | **55.6** | **Optimal for MoE models** |
| 1024 | 191 | 25.3 | Too large, causes stalls |

> **Recommendation:** Use `ubatch=512` for MoE models like Qwen3.5-35B-A3B. Larger ubatch sizes cause severe performance degradation.

### Llama 2 7B (Q4_K_M, 3.80 GiB) — Dense Model Comparison

Self-compiled ROCm 7.2 (b8301), Flash Attention + hipBLASLt:

| pp128 | pp256 | pp512 | pp1024 | tg128 |
|-------|-------|-------|--------|-------|
| 1183 | — | 1215 | 1082 | 40.87 |

kyuz0 pre-built ROCm 7.2 (b8189):

| pp128 | pp256 | pp512 | pp1024 | tg128 |
|-------|-------|-------|--------|-------|
| 1163 | 1199 | 1261 | 1256 | 45.07 |

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

### ROCm Version Comparison Summary

| ROCm Version | pp512 (kyuz0 b8298) | tg128 (kyuz0 b8298) | Verdict |
|-------------|---------------------|---------------------|---------|
| **ROCm 7.2** | 507 | **55.6** | Best generation |
| **ROCm 6.4.4** | **672** (+33%) | 52.0 (-6.5%) | Best prompt processing (pre-built) |
| ROCm 7.0 RC | — | — | Segfaults on kernel 6.18.14 |

> **ROCm HIP gives +51% prompt eval (pp128), +114% prompt eval (pp512), and +21% generation** compared to Ollama Vulkan on the same model.

### How This Compares

| Hardware | Bandwidth | Generation (t/s) | Max Model Size | Price |
|----------|-----------|-------------------|----------------|-------|
| RTX 4090 | ~1008 GB/s | 100-122 | 24 GB | ~$1600 GPU only |
| RTX 3090 | ~936 GB/s | 100-112 | 24 GB | ~$800 used |
| Apple M4 Max | ~546 GB/s | ~100 (MLX) | 128 GB | ~$4000+ |
| **Beelink GTR9 Pro** | **~256 GB/s** | **55.6** | **120+ GB** | **$2,699** |
| NVIDIA DGX Spark | ~273 GB/s | 38 | 128 GB | ~$3000 |

> The GTR9 Pro **beats the $3000 DGX Spark by 46%** on token generation and runs 51GB models that don't fit on any consumer GPU.

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

> **Impact:** +5-8% overall performance improvement. Sets CPU governor to `performance` instead of `powersave`.

> **WARNING:** After reboot, verify tuned is actually running with `tuned-adm active`. We found it can silently fail to start, leaving the CPU governor on `powersave` — a massive performance loss.

### Step 4.2: Force GPU High Performance Clocks

> **CRITICAL:** Due to a [known AMD driver bug](https://github.com/ROCm/ROCm/issues/5750), the GPU may stay stuck at ~900 MHz instead of ramping to the full 2900 MHz under compute load. This causes **significant performance loss** for prompt processing (+8% pp512 when fixed).

Check current GPU clock:

```bash
cat /sys/class/drm/card*/device/pp_dpm_sclk
```

If the `*` is next to a low clock (600-900 MHz) instead of the highest, force high performance:

```bash
echo high | sudo tee /sys/class/drm/card1/device/power_dpm_force_performance_level
```

To persist across reboots, create a systemd service:

```bash
sudo nano /etc/systemd/system/gpu-high-clocks.service
```

Add:

```ini
[Unit]
Description=Force AMD GPU to high performance clocks
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/bin/bash -c 'echo high > /sys/class/drm/card1/device/power_dpm_force_performance_level'
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

Enable:

```bash
sudo systemctl daemon-reload
sudo systemctl enable gpu-high-clocks.service
```

> **Note:** This increases idle power consumption. The GPU will always run at maximum clocks. For a dedicated LLM inference machine, this is the correct trade-off.

### Step 4.3: Sysctl and Memory Tuning

Create `/etc/sysctl.d/99-llm-performance.conf`:

```bash
sudo nano /etc/sysctl.d/99-llm-performance.conf
```

Add:

```
# Lower swappiness - keep LLM model weights in RAM
vm.swappiness=10

# Optimize dirty page writeback
vm.dirty_ratio=40
vm.dirty_background_ratio=10

# Increase max memory map areas (helps large mmap'd model files)
vm.max_map_count=2097152

# Network buffer tuning (helps API throughput)
net.core.rmem_max=16777216
net.core.wmem_max=16777216
```

Apply:

```bash
sudo sysctl --system
```

### Step 4.3: Enable Transparent Huge Pages

```bash
echo always | sudo tee /sys/kernel/mm/transparent_hugepage/enabled
echo 0 | sudo tee /proc/sys/kernel/numa_balancing
```

To persist across reboots, create `/etc/tmpfiles.d/llm-performance.conf`:

```bash
sudo nano /etc/tmpfiles.d/llm-performance.conf
```

Add:

```
w /sys/kernel/mm/transparent_hugepage/enabled - - - - always
w /proc/sys/kernel/numa_balancing - - - - 0
```

### Step 4.4: Upgrade Mesa Vulkan Drivers

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
Environment="VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json"
Environment="OLLAMA_NUM_BATCH=512"
Environment="OLLAMA_NUM_PARALLEL=1"
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
| `VK_ICD_FILENAMES=...` | Explicitly select RADV ICD (needed when AMDVLK is also installed — `AMD_VULKAN_ICD` alone may not work) |
| `OLLAMA_NUM_BATCH=512` | Larger batch size for better throughput on long prompts |
| `OLLAMA_NUM_PARALLEL=1` | Single parallel request for maximum per-request speed |

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

### Step 7.2: Create a ROCm Container

**ROCm 7.2** — Best generation speed (55.6 t/s):

```bash
distrobox create llama-rocm-72 \
  --image docker.io/kyuz0/amd-strix-halo-toolboxes:rocm-7.2 \
  --additional-flags "--device /dev/dri --device /dev/kfd --group-add video --group-add render --security-opt seccomp=unconfined"
```

**ROCm 6.4.4** — Better prompt processing (+33%), slightly slower generation (-6.5%):

```bash
distrobox create llama-rocm-644 \
  --image docker.io/kyuz0/amd-strix-halo-toolboxes:rocm-6.4.4 \
  --additional-flags "--device /dev/dri --device /dev/kfd --group-add video --group-add render --security-opt seccomp=unconfined"
```

> **Which to choose?** ROCm 7.2 for interactive chat (fastest generation). ROCm 6.4.4 for RAG/search workloads (faster prompt processing). Both containers include pre-built llama.cpp binaries.

### Step 7.3: Enter and Test

```bash
distrobox enter llama-rocm-72
```

Inside the container, verify ROCm works:

```bash
/opt/rocm/bin/rocm-smi  # Should show your gfx1151 GPU
```

### Step 7.4: Download a Compatible GGUF Model

> **IMPORTANT:** Ollama's GGUF files are NOT compatible with standalone llama.cpp due to different tensor naming conventions. You must download a proper GGUF from HuggingFace.

Install huggingface-hub (on the host, outside the container):

```bash
pipx install huggingface-hub
pipx inject huggingface-hub "huggingface-hub[cli]"
```

Download a compatible Qwen3.5-35B-A3B GGUF:

```bash
python3 -c "
from huggingface_hub import hf_hub_download
hf_hub_download('bartowski/Qwen_Qwen3.5-35B-A3B-GGUF',
                'Qwen_Qwen3.5-35B-A3B-Q4_K_M.gguf',
                local_dir='$HOME/models/')
"
```

> This downloads ~21GB. The model will be accessible inside the container via `~/models/`.

### Step 7.5: Rebuild llama.cpp (For Newer Models)

The kyuz0 pre-built binary (build 8189) is fast but too old for newer models like Qwen3.5. To rebuild:

Inside the container:

```bash
export PATH=/opt/rocm/bin:$PATH
cd ~/llama.cpp
git pull
rm -rf build && mkdir build && cd build
cmake .. -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx1151 -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
```

> **Build time:** ~5 minutes with 32 cores.

> **Note:** The kyuz0 pre-built binary (build 8189) is ~10% faster than self-compiled on small models (Llama 7B) due to undocumented compiler optimizations. However, for newer models like Qwen3.5-35B-A3B, you must use a newer build as the old one lacks support for the `qwen35moe` architecture.

### Step 7.6: Run llama-bench

```bash
export ROCBLAS_USE_HIPBLASLT=1
cd ~/llama.cpp/build
./bin/llama-bench -m ~/models/Qwen_Qwen3.5-35B-A3B-Q4_K_M.gguf -fa on -ngl 999 -mmp 0 -p 128,512 -n 128
```

Expected results (Qwen3.5-35B-A3B Q4_K_M):

| pp128 | pp512 | tg128 |
|-------|-------|-------|
| ~472 | ~922 | ~48.8 |

> **Important:** `ROCBLAS_USE_HIPBLASLT=1` + `-fa on` gives **+13% prompt processing** and **+8% token generation**.

> **Important:** Always use `-mmp 0` (disable mmap) with ROCm GPU backends. With mmap enabled, short prompt eval has high variance and is ~22% slower (388 ± 129 vs 472 ± 15 t/s at pp128) due to page fault overhead. Long prompts (pp512+) are unaffected.

### Step 7.7: Run llama-server (API Alternative to Ollama)

For the best inference performance, use `llama-server` instead of Ollama:

Inside the container:

```bash
export ROCBLAS_USE_HIPBLASLT=1
cd ~/llama.cpp/build
./bin/llama-server \
  -m ~/models/Qwen_Qwen3.5-35B-A3B-Q4_K_M.gguf \
  -ngl 999 \
  -fa on \
  --no-mmap \
  -c 8192 \
  --host 0.0.0.0 \
  --port 8080
```

The server provides an OpenAI-compatible API at `http://localhost:8080`. You can use it with any OpenAI-compatible client.

> **Performance:** llama-server via ROCm HIP gives **+5.4% generation speed** and **up to 2x faster prompt processing** compared to Ollama Vulkan on the same model.

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
| BIOS VRAM for speed | No speed difference after change | "More GPU VRAM = faster" | Speed stays the same, but you MUST set to lowest (512MB) to make GTT RAM available to the OS — without this, the OS only sees ~31GB |

### Things That DO Work

| Optimization | Impact | Notes |
|-------------|--------|-------|
| **ROCm HIP instead of Vulkan** | **+21% gen, +114% pp512** | llama-server via ROCm container — biggest win |
| **ROCm 6.4.4 instead of 7.2** | **+33% pp512** (pre-built) | Trade-off: -6.5% generation speed |
| Force GPU high clocks | **+8% pp512** | Fixes AMD driver bug where GPU stays at 900 MHz |
| Mesa 25.2.8 → 26.0.1 | **+9%** prompt eval | kisak PPA (Vulkan/Ollama only) |
| Flash Attention | **+13%** prompt processing | `-fa on` or `OLLAMA_FLASH_ATTENTION=1` |
| hipBLASLt | **+8%** token generation | `ROCBLAS_USE_HIPBLASLT=1` (ROCm only) |
| tuned accelerator-performance | **+5-8%** overall | Verify it's running after reboot! |
| Disable mmap (`-mmp 0`) | **+22% pp128**, stable | Eliminates page fault overhead on short prompts (ROCm only) |
| Transparent Huge Pages | marginal | `echo always > /sys/kernel/mm/transparent_hugepage/enabled` |
| Sysctl tuning | marginal | `vm.swappiness=10`, `vm.max_map_count=2097152` |
| RADV over AMDVLK | **+14%** prompt eval | Use `VK_ICD_FILENAMES` to force (Vulkan/Ollama only) |
| BIOS VRAM → 512MB | OS sees 125GB instead of 31GB | No speed change, but makes system usable |
| `HIP_VISIBLE_DEVICES=-1` | Fixes Ollama crash | Required for Vulkan-only mode |
| HuggingFace GGUF | Required for llama.cpp | Ollama GGUFs are incompatible with standalone llama.cpp |

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
