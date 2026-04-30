#!/bin/bash
# AMD Strix Halo LLM Setup Script
# Automates the entire setup from Phase 3 onwards (after BIOS and OS install)
# Tested on: Beelink GTR9 Pro, Ubuntu 24.04, Kernel 6.18.x/6.19.x
#
# Usage: curl -fsSL https://raw.githubusercontent.com/hogeheer499-commits/strix-halo-guide/main/setup.sh | bash
#    or: bash setup.sh
#
# What this script does:
#   1. Configures kernel parameters (GRUB)
#   2. Creates GPU access rules (udev)
#   3. Installs and configures tuned (accelerator-performance)
#   4. Upgrades Mesa Vulkan drivers (kisak PPA)
#   5. Installs Ollama with Vulkan backend
#   6. Pulls recommended models
#   7. Runs a benchmark to verify setup
#
# What this script does NOT do:
#   - Change BIOS settings (do this manually first -- see README)
#   - Install Ubuntu (do this manually first)
#   - Install ROCm containers (optional, see README Phase 7)

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()  { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[!!]${NC} $1"; }
err()  { echo -e "${RED}[ERR]${NC} $1"; }
info() { echo -e "${BLUE}[..]${NC} $1"; }

echo ""
echo "============================================="
echo "  AMD Strix Halo LLM Setup Script"
echo "  github.com/hogeheer499-commits/strix-halo-guide"
echo "============================================="
echo ""

# Pre-flight checks
if [ "$(id -u)" -eq 0 ]; then
    err "Do not run this script as root. Run as your normal user (it will use sudo when needed)."
    exit 1
fi

if ! grep -qi "amd" /proc/cpuinfo 2>/dev/null; then
    warn "This does not appear to be an AMD system. Continuing anyway..."
fi

TOTAL_RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
if [ "$TOTAL_RAM_GB" -lt 60 ]; then
    warn "Only ${TOTAL_RAM_GB}GB RAM visible. Did you set UMA Frame Buffer to 512MB in BIOS?"
    warn "Without this, you cannot run large models. See README Phase 1."
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]] || exit 1
fi

# Phase 3: Kernel Configuration
echo ""
info "Phase 3: Kernel Configuration"
echo "---------------------------------------------"

GRUB_FILE="/etc/default/grub"
CURRENT_CMDLINE=$(grep "^GRUB_CMDLINE_LINUX_DEFAULT" "$GRUB_FILE" 2>/dev/null || echo "")

NEEDED_PARAMS="amd_iommu=off amdgpu.gttsize=131072 ttm.pages_limit=31457280 amdgpu.cwsr_enable=0"
MISSING_PARAMS=""

for param in $NEEDED_PARAMS; do
    key=$(echo "$param" | cut -d= -f1)
    if ! echo "$CURRENT_CMDLINE" | grep -q "$key"; then
        MISSING_PARAMS="$MISSING_PARAMS $param"
    fi
done

if [ -n "$MISSING_PARAMS" ]; then
    info "Adding kernel parameters:$MISSING_PARAMS"
    # Extract current value, add missing params
    CURRENT_VALUE=$(echo "$CURRENT_CMDLINE" | sed 's/GRUB_CMDLINE_LINUX_DEFAULT="//' | sed 's/"$//')
    NEW_VALUE="$CURRENT_VALUE$MISSING_PARAMS"
    sudo sed -i "s|^GRUB_CMDLINE_LINUX_DEFAULT=.*|GRUB_CMDLINE_LINUX_DEFAULT=\"$NEW_VALUE\"|" "$GRUB_FILE"
    sudo update-grub
    log "GRUB updated. Changes take effect after reboot."
else
    log "Kernel parameters already configured."
fi

# Modprobe configuration
if [ ! -f /etc/modprobe.d/amdgpu_llm_optimized.conf ]; then
    info "Creating modprobe configuration..."
    sudo tee /etc/modprobe.d/amdgpu_llm_optimized.conf > /dev/null << 'MODPROBE'
options amdgpu gttsize=122800
options ttm pages_limit=31457280
options ttm page_pool_size=31457280
MODPROBE
    sudo update-initramfs -u -k all 2>/dev/null || true
    log "Modprobe configuration created."
else
    log "Modprobe configuration already exists."
fi

# udev rules
if [ ! -f /etc/udev/rules.d/99-amd-kfd.rules ]; then
    info "Creating GPU udev rules..."
    sudo tee /etc/udev/rules.d/99-amd-kfd.rules > /dev/null << 'UDEV'
SUBSYSTEM=="kfd", GROUP="render", MODE="0666"
SUBSYSTEM=="drm", KERNEL=="card[0-9]*", GROUP="render", MODE="0666"
SUBSYSTEM=="drm", KERNEL=="renderD[0-9]*", GROUP="render", MODE="0666"
UDEV
    sudo udevadm control --reload-rules
    sudo udevadm trigger
    log "udev rules created."
else
    log "udev rules already exist."
fi

# Add user to GPU groups
if ! groups | grep -q render; then
    sudo usermod -aG render "$USER"
    sudo usermod -aG video "$USER"
    log "Added $USER to render and video groups."
else
    log "User already in GPU groups."
fi

# Phase 4: Performance Tuning
echo ""
info "Phase 4: Performance Tuning"
echo "---------------------------------------------"

if ! command -v tuned-adm &>/dev/null; then
    info "Installing tuned..."
    sudo apt install -y tuned
fi

sudo systemctl enable --now tuned 2>/dev/null || true
sudo tuned-adm profile accelerator-performance 2>/dev/null || true

ACTIVE_PROFILE=$(tuned-adm active 2>/dev/null | grep -o "accelerator-performance" || echo "")
if [ "$ACTIVE_PROFILE" = "accelerator-performance" ]; then
    log "tuned: accelerator-performance active."
else
    warn "tuned profile may not be set correctly. Run: sudo tuned-adm profile accelerator-performance"
fi

# Mesa upgrade
if ! command -v vulkaninfo &>/dev/null; then
    info "Installing vulkan-tools..."
    sudo apt install -y vulkan-tools
fi

MESA_VERSION=$(vulkaninfo --summary 2>&1 | grep "driverInfo" | head -1 | grep -o "Mesa [0-9.]*" || echo "unknown")
info "Current Mesa: $MESA_VERSION"

if ! grep -q "kisak" /etc/apt/sources.list.d/*.list 2>/dev/null && \
   ! grep -q "kisak" /etc/apt/sources.list.d/*.sources 2>/dev/null; then
    info "Adding kisak-mesa PPA for latest Vulkan drivers..."
    sudo add-apt-repository -y ppa:kisak/kisak-mesa
    sudo apt update
    sudo apt upgrade -y
    log "Mesa upgraded. New version: $(vulkaninfo --summary 2>&1 | grep 'driverInfo' | head -1)"
else
    log "kisak-mesa PPA already added."
fi

# Phase 5: Ollama Setup
echo ""
info "Phase 5: Ollama Setup"
echo "---------------------------------------------"

if ! command -v ollama &>/dev/null; then
    info "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    log "Ollama installed."
else
    log "Ollama already installed: $(ollama --version 2>/dev/null)"
fi

# Configure Ollama for Vulkan
OLLAMA_OVERRIDE="/etc/systemd/system/ollama.service.d/override.conf"
if [ ! -f "$OLLAMA_OVERRIDE" ] || ! grep -q "OLLAMA_VULKAN" "$OLLAMA_OVERRIDE" 2>/dev/null; then
    info "Configuring Ollama for Vulkan..."
    sudo mkdir -p /etc/systemd/system/ollama.service.d
    sudo tee "$OLLAMA_OVERRIDE" > /dev/null << 'OLLAMA'
[Service]
Environment="OLLAMA_VULKAN=1"
Environment="HIP_VISIBLE_DEVICES=-1"
Environment="OLLAMA_FLASH_ATTENTION=1"
Environment="OLLAMA_CONTEXT_LENGTH=8192"
Environment="AMD_VULKAN_ICD=RADV"
Environment="VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json"
Environment="OLLAMA_NUM_BATCH=512"
Environment="OLLAMA_NUM_PARALLEL=1"
OLLAMA
    sudo systemctl daemon-reload
    sudo systemctl restart ollama
    log "Ollama configured for Vulkan (RADV)."
else
    log "Ollama already configured for Vulkan."
fi

# Wait for Ollama to be ready
info "Waiting for Ollama to start..."
for i in $(seq 1 30); do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        log "Ollama is running."
        break
    fi
    sleep 1
done

# Pull recommended model
echo ""
info "Phase 5.3: Pulling recommended model"
echo "---------------------------------------------"

if ! ollama list 2>/dev/null | grep -q "qwen3.6:35b-a3b"; then
    info "Pulling qwen3.6:35b-a3b (~23GB, this may take a while)..."
    ollama pull qwen3.6:35b-a3b
    log "Model pulled successfully."
else
    log "qwen3.6:35b-a3b already available."
fi

# Phase 6: Benchmark
echo ""
info "Phase 6: Running benchmark"
echo "---------------------------------------------"

info "Benchmarking qwen3.6:35b-a3b..."
BENCH_RESULT=$(curl -s http://localhost:11434/api/generate -d '{"model":"qwen3.6:35b-a3b","prompt":"hello how are you","stream":false}' 2>/dev/null | python3 -c "
import sys,json
try:
    d=json.load(sys.stdin)
    pp=d['prompt_eval_count']/d['prompt_eval_duration']*1e9
    tg=d['eval_count']/d['eval_duration']*1e9
    print(f'Prompt eval: {pp:.1f} t/s | Generation: {tg:.1f} t/s')
    if tg > 40:
        print('STATUS:PASS')
    else:
        print('STATUS:SLOW')
except:
    print('STATUS:FAIL')
" 2>/dev/null)

echo "$BENCH_RESULT" | head -1

if echo "$BENCH_RESULT" | grep -q "STATUS:PASS"; then
    log "Benchmark PASSED. Your system is performing well."
elif echo "$BENCH_RESULT" | grep -q "STATUS:SLOW"; then
    warn "Benchmark completed but speed is lower than expected."
    warn "Expected 45+ t/s. Check if tuned is running and Mesa is upgraded."
else
    err "Benchmark failed. Check Ollama logs: journalctl -u ollama -n 50"
fi

# Create benchmark script
tee ~/bench-ollama.sh > /dev/null << 'SCRIPT'
#!/bin/bash
MODEL="${1:-qwen3.6:35b-a3b}"
PROMPT="${2:-hello how are you}"
echo "Model: $MODEL | $(date -u +%Y-%m-%dT%H:%M:%SZ)"
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

# Summary
echo ""
echo "============================================="
echo "  Setup Complete!"
echo "============================================="
echo ""
echo "  System: $(uname -r)"
echo "  Mesa:   $(vulkaninfo --summary 2>&1 | grep 'driverInfo' | head -1 | grep -o 'Mesa [0-9.]*' || echo 'unknown')"
echo "  Ollama: $(ollama --version 2>/dev/null || echo 'unknown')"
echo "  tuned:  $(tuned-adm active 2>/dev/null | grep -o 'accelerator-performance' || echo 'not active')"
echo "  RAM:    $(free -h | awk '/^Mem:/{print $2}')"
echo ""
echo "  Quick start:"
echo "    ollama run qwen3.6:35b-a3b"
echo ""
echo "  Benchmark:"
echo "    bash ~/bench-ollama.sh"
echo ""
echo "  For ROCm containers and advanced setup, see:"
echo "    https://github.com/hogeheer499-commits/strix-halo-guide"
echo ""

if echo "$CURRENT_CMDLINE" | grep -q "amd_iommu=off"; then
    log "No reboot needed."
else
    warn "REBOOT REQUIRED for kernel parameters to take effect."
    warn "Run: sudo reboot"
fi
