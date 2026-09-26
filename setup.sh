#!/bin/bash
# AMD Strix Halo LLM Setup Script
# Automates the entire setup from Phase 3 onwards (after BIOS and OS install)
# Profile evidence: Beelink GTR9 Pro (128GB), Ubuntu 24.04; kernel 6.19.4 for
# historical headline runs, Ubuntu HWE kernels 7.0.0-28/-30/-31 for later runs.
# Revised automation is offline-fixture-tested; fresh-install/upgrade hardware
# qualification remains pending.
#
# Usage: curl -fsSL https://raw.githubusercontent.com/hogeheer499-commits/strix-halo-guide/main/setup.sh | bash
#    or: bash setup.sh
# The curl route and a fresh clone both run the unpinned main branch, which is
# not fresh-install qualified. Prefer a reviewed tag or commit
# (git checkout <tag-or-commit>). OS releases other than Ubuntu 24.04 stop
# unless the variable is passed to bash, for example:
#   STRIX_HALO_ALLOW_UNQUALIFIED_OS=1 bash setup.sh
#
# What this script does:
#   1. Configures kernel parameters (GRUB)
#   2. Uses distribution GPU permissions and checks account/session groups
#   3. Preserves power policy by default (tuned is an explicit opt-in)
#   4. Upgrades Mesa Vulkan drivers (kisak PPA)
#   5. Installs Ollama with Vulkan backend
#   6. Pulls the recommended first model
#   7. Runs or prepares a verification benchmark
#
# What this script does NOT do:
#   - Change BIOS settings (do this manually first -- see README)
#   - Install Ubuntu (do this manually first)
#   - Install ROCm containers (optional, see README Phase 7)
#   - Run the final benchmark before reboot if boot parameters changed

set -euo pipefail

# Pin a fresh installation to the reboot-qualified runtime. An explicit
# OLLAMA_VERSION selects another runtime; existing installations are retained.
OLLAMA_VERSION="${OLLAMA_VERSION:-0.31.2}"
if [[ ! "$OLLAMA_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+([.-][A-Za-z0-9.-]+)?$ ]]; then
    echo "Invalid OLLAMA_VERSION: use an explicit release such as 0.31.2." >&2
    exit 1
fi

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

# BEGIN PREFLIGHT GUARDS (also exercised by offline fixtures)
# Only Ubuntu 24.04 is recorded. Ubuntu 26.04 and other distributions are not
# qualified; STRIX_HALO_ALLOW_UNQUALIFIED_OS=1 continues at the user's risk.
OS_ID=""
OS_VERSION_ID=""
if [ -r /etc/os-release ]; then
    OS_ID=$(. /etc/os-release && printf '%s' "${ID:-}")
    OS_VERSION_ID=$(. /etc/os-release && printf '%s' "${VERSION_ID:-}")
fi
if [ "$OS_ID" != "ubuntu" ] || [ "$OS_VERSION_ID" != "24.04" ]; then
    if [ "${STRIX_HALO_ALLOW_UNQUALIFIED_OS:-0}" = "1" ]; then
        warn "Detected ${OS_ID:-unknown} ${OS_VERSION_ID:-unknown}; this script is only recorded on Ubuntu 24.04. Continuing because STRIX_HALO_ALLOW_UNQUALIFIED_OS=1."
    else
        err "Detected ${OS_ID:-unknown} ${OS_VERSION_ID:-unknown}. This script is only recorded on Ubuntu 24.04; Ubuntu 26.04 and other distributions are not qualified. Use the manual guide, or set STRIX_HALO_ALLOW_UNQUALIFIED_OS=1 to continue at your own risk."
        exit 1
    fi
fi

TOTAL_RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
if ! [[ "$TOTAL_RAM_GB" =~ ^[0-9]+$ ]]; then
    err "Could not read visible RAM from 'free -g'. Use the manual guide."
    exit 1
fi
if [ "$TOTAL_RAM_GB" -lt 120 ]; then
    err "This automatic memory profile is limited to the measured 128GB-class route with at least 120GiB visible. For 96GB/smaller or larger UMA-reserved systems, use the manual guide; no alternate memory limits are qualified here."
    exit 1
fi
if [ "$TOTAL_RAM_GB" -gt 136 ]; then
    err "About ${TOTAL_RAM_GB}GiB visible RAM is above the measured 128GB-class route. No 192GB-class profile (for example Ryzen AI Max+ PRO 495) is qualified; do not reuse the 128GB values. Use the manual guide."
    exit 1
fi
# END PREFLIGHT GUARDS

# Phase 3: Kernel Configuration
# Detect known migration holds before the first configuration mutation.
for legacy_file in /etc/modprobe.d/amdgpu_llm_optimized.conf /etc/udev/rules.d/99-amd-kfd.rules; do
    if [ -e "$legacy_file" ] || [ -L "$legacy_file" ]; then
        err "Existing legacy profile needs manual review before changes: $legacy_file (README Steps 3.3/3.4)."
        exit 1
    fi
done
echo ""
info "Phase 3: Kernel Configuration"
echo "---------------------------------------------"

REBOOT_REQUIRED=0
SESSION_REFRESH_REQUIRED=0

GRUB_FILE="/etc/default/grub"
CURRENT_CMDLINE=$(grep "^GRUB_CMDLINE_LINUX_DEFAULT" "$GRUB_FILE" 2>/dev/null || echo "")

# Keep IOMMU at the firmware/kernel default on the general buyer path. Disabling
# it is an optional desktop benchmark profile: it removes NPU access and can
# break s0i3/s2idle on mobile Strix Halo systems.
NEEDED_PARAMS="amdgpu.gttsize=131072 ttm.pages_limit=31457280 amdgpu.cwsr_enable=0"
MISSING_PARAMS=""

if grep -q "amd_iommu=off" /proc/cmdline 2>/dev/null || echo "$CURRENT_CMDLINE" | grep -q "amd_iommu=off"; then
    warn "amd_iommu=off is configured. This matches the optional desktop benchmark profile,"
    warn "but disables the NPU and can prevent deep s0i3/s2idle sleep on laptops/tablets."
    warn "See README Phase 1.2 before keeping it on a mobile or NPU-enabled system."
fi

for param in $NEEDED_PARAMS; do
    key=$(echo "$param" | cut -d= -f1)
    configured_value=$(printf '%s\n' "$CURRENT_CMDLINE" | tr '" ' '\n' | grep "^${key}=" || true)
    if [ -n "$configured_value" ] && [ "$configured_value" != "$param" ]; then
        err "Conflicting $key in GRUB; review the selected memory profile before continuing. Existing configuration preserved."
        exit 1
    fi
    if [ -z "$configured_value" ]; then
        MISSING_PARAMS="$MISSING_PARAMS $param"
    fi
done

if [ -n "$MISSING_PARAMS" ]; then
    info "Adding kernel parameters:$MISSING_PARAMS"
    # Extract current value, add missing params
    if [ -n "$CURRENT_CMDLINE" ] && [[ ! "$CURRENT_CMDLINE" =~ ^GRUB_CMDLINE_LINUX_DEFAULT=\"[^\"\$\`]*\"$ ]]; then
        err "GRUB assignment needs manual review (multiple assignments, shell expansion or unsupported quoting)."
        exit 1
    fi
    CURRENT_VALUE=$(echo "$CURRENT_CMDLINE" | sed 's/GRUB_CMDLINE_LINUX_DEFAULT="//' | sed 's/"$//')
    NEW_VALUE="$CURRENT_VALUE$MISSING_PARAMS"
    if [ -z "$CURRENT_CMDLINE" ]; then
        printf '\nGRUB_CMDLINE_LINUX_DEFAULT="%s"\n' "$NEW_VALUE" | sudo tee -a "$GRUB_FILE" > /dev/null
    else
        # Escape sed replacement metacharacters in retained administrator text.
        escaped_value=$(printf '%s' "$NEW_VALUE" | sed 's/[\\&|]/\\&/g')
        sudo sed -i "s|^GRUB_CMDLINE_LINUX_DEFAULT=.*|GRUB_CMDLINE_LINUX_DEFAULT=\"$escaped_value\"|" "$GRUB_FILE"
    fi
    sudo update-grub
    log "GRUB updated. Changes take effect after reboot."
    REBOOT_REQUIRED=1
else
    log "Kernel parameters already configured."
fi

# Files on disk do not establish the live boot state, including on a rerun.
for param in $NEEDED_PARAMS; do
    if ! tr ' ' '\n' < /proc/cmdline | grep -Fxq "$param"; then
        REBOOT_REQUIRED=1
    fi
done

# Modprobe configuration: avoid competing copies of the same module options.
if [ -f /etc/modprobe.d/amdgpu_llm_optimized.conf ]; then
    err "Legacy modprobe profile needs manual review against GRUB and live module values. Preserve custom options; see README Step 3.3."
    exit 1
fi

# Use the distribution's GPU device rules; do not grant all local users access.
if [ -f /etc/udev/rules.d/99-amd-kfd.rules ]; then
    err "Existing custom GPU rules need review: /etc/udev/rules.d/99-amd-kfd.rules. Preserve unrelated rules and replace any world-writable access deliberately; see README Step 3.4."
    exit 1
fi

# Check both memberships separately; a new login is needed for new groups.
for gpu_group in render video; do
    if ! id -nG "$USER" | tr ' ' '\n' | grep -Fxq "$gpu_group"; then
        sudo usermod -aG "$gpu_group" "$USER"
        SESSION_REFRESH_REQUIRED=1
    fi
    if ! id -nG | tr ' ' '\n' | grep -Fxq "$gpu_group"; then
        SESSION_REFRESH_REQUIRED=1
    fi
done

# Phase 4: Performance Tuning
echo ""
info "Phase 4: Performance Tuning"
echo "---------------------------------------------"

POWER_POLICY="${POWER_POLICY:-preserve}"
if [ "$POWER_POLICY" = "tuned" ]; then
    if systemctl is-active --quiet power-profiles-daemon; then
        err "Selected tuned profile conflicts with active power-profiles-daemon. Resolve deliberately using README Step 4.1."
        exit 1
    fi
if ! command -v tuned-adm &>/dev/null; then
    info "Installing tuned..."
    sudo apt install -y tuned
fi

sudo systemctl enable --now tuned
sudo tuned-adm profile accelerator-performance

ACTIVE_PROFILE=$(tuned-adm active 2>/dev/null | grep -o "accelerator-performance" || echo "")
if [ "$ACTIVE_PROFILE" = "accelerator-performance" ]; then
    log "tuned: accelerator-performance active."
else
    err "Selected tuned profile was not activated."
    exit 1
fi
elif [ "$POWER_POLICY" = "preserve" ]; then
    info "Preserving existing power policy. Record power-profiles-daemon/tuned and GPU DPM state for each run."
else
    err "POWER_POLICY must be preserve or tuned."
    exit 1
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
    info "Installing Ollama ${OLLAMA_VERSION}..."
    curl -fsSL https://ollama.com/install.sh | OLLAMA_VERSION="$OLLAMA_VERSION" sh
    log "Ollama installer completed for ${OLLAMA_VERSION}. Verify the running version after restart."
else
    log "Ollama already installed: $(ollama --version 2>/dev/null)"
    warn "Keeping the existing runtime; no automatic upgrade or downgrade to ${OLLAMA_VERSION}."
fi
warn "Only the runtime installation is pinned. Match the model, driver, kernel and reboot checks before comparing with a measured profile."

# BEGIN OLLAMA CONFIGURATION FUNCTIONS (also exercised by offline fixtures)
check_ollama_environment() {
    local require_all="$1" environment files unsets
    environment=$(systemctl show ollama -p Environment --value) || return 1
    files=$(systemctl show ollama -p EnvironmentFiles --value) || return 1
    unsets=$(systemctl show ollama -p UnsetEnvironment --value) || return 1
    # EnvironmentFile and UnsetEnvironment apply after Environment. Do not
    # pretend that checking a drop-in filename resolves those contracts.
    if [ -n "$files" ] || [ -n "$unsets" ]; then
        err "Ollama uses EnvironmentFile or UnsetEnvironment; review its effective environment manually before applying this profile."
        return 1
    fi
    OLLAMA_CHECK_ENV="$environment" python3 - "$require_all" <<'PY'
import os, shlex, sys
expected = {
    'OLLAMA_VULKAN': '1', 'OLLAMA_IGPU_ENABLE': '1',
    'HIP_VISIBLE_DEVICES': '-1', 'OLLAMA_FLASH_ATTENTION': '1',
    'OLLAMA_CONTEXT_LENGTH': '8192', 'AMD_VULKAN_ICD': 'RADV',
    'VK_ICD_FILENAMES': '/usr/share/vulkan/icd.d/radeon_icd.json',
    'OLLAMA_NUM_PARALLEL': '1',
}
try:
    actual = dict(item.split('=', 1) for item in shlex.split(os.environ['OLLAMA_CHECK_ENV']))
except ValueError:
    sys.exit('Cannot parse the effective Ollama environment; manual review required.')
bad = [key for key, value in expected.items()
       if (key in actual and actual[key] != value)
       or (sys.argv[1] == 'required' and key not in actual)]
if bad:
    sys.exit('Ollama profile conflicts or missing values: ' + ', '.join(bad)
             + '. Review service/drop-in precedence; existing settings were preserved.')
PY
}

configure_ollama() {
    local directory="$1" target desired
    target="$directory/60-strix-halo-guide.conf"
    desired=$(mktemp) || return 1
    cat > "$desired" << 'OLLAMA'
# Owned by strix-halo-guide; existing administrator drop-ins are preserved.
[Service]
Environment="OLLAMA_VULKAN=1"
Environment="OLLAMA_IGPU_ENABLE=1"
Environment="HIP_VISIBLE_DEVICES=-1"
Environment="OLLAMA_FLASH_ATTENTION=1"
Environment="OLLAMA_CONTEXT_LENGTH=8192"
Environment="AMD_VULKAN_ICD=RADV"
Environment="VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json"
Environment="OLLAMA_NUM_PARALLEL=1"
OLLAMA
    # Reload existing files before inspecting their effective precedence.
    if ! sudo systemctl daemon-reload || ! check_ollama_environment optional; then
        rm -f "$desired"
        return 1
    fi
    if [ -e "$target" ] || [ -L "$target" ]; then
        if [ -L "$target" ] || ! cmp -s "$desired" "$target"; then
            err "Guide drop-in already exists with different content: $target. Review it manually; it was not overwritten."
            rm -f "$desired"
            return 1
        fi
    else
        sudo mkdir -p "$directory" || { rm -f "$desired"; return 1; }
        sudo install -m 0644 "$desired" "$target" || { rm -f "$desired"; return 1; }
    fi
    rm -f "$desired"
    sudo systemctl daemon-reload || return 1
    check_ollama_environment required || return 1
    sudo systemctl restart ollama || return 1
    log "Ollama environment matches the Vulkan profile. Actual GPU offload still needs runtime verification."
}
# END OLLAMA CONFIGURATION FUNCTIONS

configure_ollama /etc/systemd/system/ollama.service.d
warn "Verify the Ollama service user has access to the distribution's render nodes (README Step 3.4)."

# Wait for Ollama to be ready
info "Waiting for Ollama to start..."
OLLAMA_READY=0
for i in $(seq 1 30); do
    if curl --fail --silent --show-error --connect-timeout 2 --max-time 5 http://localhost:11434/api/tags | python3 -c 'import json,sys; d=json.load(sys.stdin); sys.exit(0 if isinstance(d,dict) and isinstance(d.get("models"),list) else 1)' 2>/dev/null; then
        log "Ollama is running."
        OLLAMA_READY=1
        break
    fi
    sleep 1
done
if [ "$OLLAMA_READY" -ne 1 ]; then
    err "Ollama did not become ready within 30 bounded attempts. Check its logs before continuing."
    exit 1
fi

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

if [ "$REBOOT_REQUIRED" -eq 1 ]; then
    warn "Skipping the final benchmark because boot-time GPU/kernel changes were applied."
    warn "After this script finishes, reboot first, then run: bash ~/bench-ollama.sh"
    BENCH_RESULT="STATUS:SKIPPED"
else
    info "Benchmarking qwen3.6:35b-a3b..."
    BENCH_RESULT=$(curl --fail --silent --show-error --connect-timeout 5 --max-time 600 http://localhost:11434/api/generate -d '{"model":"qwen3.6:35b-a3b","prompt":"hello how are you","stream":false,"options":{"num_predict":128}}' | python3 -c "
import sys,json
try:
    d=json.load(sys.stdin)
    if d.get('done') is not True or not isinstance(d.get('response'), str) or not d['response'].strip() or d.get('error'):
        raise ValueError('Missing completed visible response or server error')
    for key in ('prompt_eval_count', 'prompt_eval_duration', 'eval_count', 'eval_duration'):
        if type(d.get(key)) is not int or d[key] <= 0:
            raise ValueError('Invalid counter: ' + key)
    pp=d['prompt_eval_count']/d['prompt_eval_duration']*1e9
    tg=d['eval_count']/d['eval_duration']*1e9
    print(f'Prompt eval: {pp:.1f} t/s | Generation: {tg:.1f} t/s')
    print('STATUS:PASS')
except:
    print('STATUS:FAIL')
    sys.exit(1)
" ) || BENCH_RESULT="STATUS:FAIL"

    echo "$BENCH_RESULT" | head -1
fi

if echo "$BENCH_RESULT" | grep -q "STATUS:PASS"; then
    log "Text API smoke completed with valid response and counters. This does not establish GPU offload or benchmark qualification."
elif echo "$BENCH_RESULT" | grep -q "STATUS:SKIPPED"; then
    warn "Benchmark skipped until reboot so the reported speed is not misleading."
else
    err "Benchmark failed. Check Ollama logs: journalctl -u ollama -n 50"
fi

# Create benchmark script
SMOKE_HELPER=$(mktemp)
tee "$SMOKE_HELPER" > /dev/null << 'SCRIPT'
#!/bin/bash
set -euo pipefail
MODEL="${1:-qwen3.6:35b-a3b}"
PROMPT="${2:-hello how are you}"
echo "Model: $MODEL | $(date -u +%Y-%m-%dT%H:%M:%SZ)"
if command -v ollama >/dev/null 2>&1; then
    echo "Local tag and manifest ID (ollama list):"
    ollama list 2>/dev/null | awk -v m="$MODEL" 'NR==1 || $1==m || $1==m":latest"' || true
    echo "Model parameters (a draft_num_predict above 0 means Ollama-default speculative drafting):"
    ollama show --parameters "$MODEL" 2>/dev/null || echo "  (ollama show --parameters unavailable)"
fi
python3 -c 'import json,sys; print(json.dumps({"model":sys.argv[1],"prompt":sys.argv[2],"stream":False,"options":{"num_predict":128}}))' "$MODEL" "$PROMPT" |
curl --fail --silent --show-error --connect-timeout 5 --max-time 600 http://localhost:11434/api/generate -H 'Content-Type: application/json' --data-binary @- | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('done') is not True or not isinstance(d.get('response'),str) or not d['response'].strip() or d.get('error'):
    raise ValueError('Missing completed visible response or server error')
for key in ('prompt_eval_count','prompt_eval_duration','eval_count','eval_duration','total_duration'):
    if type(d.get(key)) is not int or d[key] <= 0:
        raise ValueError('Invalid counter: ' + key)
pp=d['prompt_eval_count']/d['prompt_eval_duration']*1e9
tg=d['eval_count']/d['eval_duration']*1e9
print(f'Prompt eval: {pp:.1f} t/s ({d[\"prompt_eval_count\"]} tokens)')
print(f'Generation:  {tg:.1f} t/s ({d[\"eval_count\"]} tokens)')
print(f'Total time:  {d[\"total_duration\"]/1e9:.2f}s')
"
SCRIPT
if [ -e "$HOME/bench-ollama.sh" ] || [ -L "$HOME/bench-ollama.sh" ]; then
    if [ -L "$HOME/bench-ollama.sh" ] || ! cmp -s "$SMOKE_HELPER" "$HOME/bench-ollama.sh"; then
        rm -f "$SMOKE_HELPER"
        err "Existing ~/bench-ollama.sh differs; preserved. Review the current scripts/ollama_smoke.sh from the guide manually."
        exit 1
    fi
else
    install -m 0755 "$SMOKE_HELPER" "$HOME/bench-ollama.sh"
fi
rm -f "$SMOKE_HELPER"

# Summary
echo ""
echo "============================================="
echo "  Configuration run finished; qualification pending"
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

if [ "$REBOOT_REQUIRED" -eq 1 ]; then
    warn "REBOOT REQUIRED for boot-time GPU/kernel changes to take effect."
    warn "Run: sudo reboot"
elif [ "$SESSION_REFRESH_REQUIRED" -eq 1 ]; then
    warn "Log out and back in, or reboot, so GPU group membership applies to your shell."
else
    log "Requested command-line parameters are live. Verify service GPU access and actual offload separately."
fi
if echo "$BENCH_RESULT" | grep -q "STATUS:FAIL"; then
    err "Setup verification failed; configuration may have been applied but the runtime is not ready."
    exit 1
fi
