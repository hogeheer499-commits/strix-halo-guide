#!/usr/bin/env bash
# Collect a reproducibility manifest without hostnames, serials, UUIDs, or IPs.
set -euo pipefail

OUT="${1:-/dev/stdout}"
NODE_LABEL="${NODE_LABEL:-node-unknown}"
CAMPAIGN_ID="${CAMPAIGN_ID:-strix-halo-thermal}"
MODEL="${MODEL:-/data/models/UD-IQ2_M/MiMo-V2.5-UD-IQ2_M-00001-of-00003.gguf}"
IMAGE="${STRIX_BENCH_IMAGE:-docker.io/kyuz0/amd-strix-halo-toolboxes@sha256:646283d9607d7d678b500c85e3bb397742a20ec75a9bbf536ce0418d27b6a11f}"
HASH_MODE="${HASH_MODE:-full}"
AMBIENT_C="${AMBIENT_C:-unknown}"
COOLING_CONTEXT="${COOLING_CONTEXT:-stock-unverified}"
EC_FIRMWARE_VERSION="${EC_FIRMWARE_VERSION:-unknown}"
BACKGROUND_CONDITION="${BACKGROUND_CONDITION:-unspecified}"

GPU_PCI="${GPU_PCI:-}"
GPU=""
for d in /sys/bus/pci/devices/*/pp_od_clk_voltage; do
  [[ -e "$d" ]] || continue
  dev="${d%/pp_od_clk_voltage}"
  [[ "$(cat "$dev/vendor" 2>/dev/null)" == "0x1002" ]] || continue
  if [[ -z "$GPU_PCI" || "$(basename "$dev")" == "$GPU_PCI" ]]; then
    GPU="$dev"
    GPU_PCI="$(basename "$dev")"
    break
  fi
done
[[ -n "$GPU" ]] || { echo "ERROR: no AMD overdrive node found" >&2; exit 1; }

mkdir -p "$(dirname "$OUT")"
exec > "$OUT"

emit() {
  local key="$1" value="${2:-}"
  value="${value//$'\n'/ }"
  value="${value//$'\r'/ }"
  printf '%s=%s\n' "$key" "$value"
}

read_dmi() {
  cat "/sys/class/dmi/id/$1" 2>/dev/null || printf 'unavailable'
}

emit schema_version 1
emit captured_utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
emit campaign_id "$CAMPAIGN_ID"
emit node_label "$NODE_LABEL"
emit ambient_c "$AMBIENT_C"
emit cooling_context "$COOLING_CONTEXT"
emit background_condition "$BACKGROUND_CONDITION"
emit background_running_container_count "$(podman ps --noheading 2>/dev/null | wc -l | tr -d ' ')"
emit background_model_process_count "$(ps -eo comm= | awk '$1 ~ /^(llama-server|llama-cli|llama-bench|vllm|sglang|ollama)$/{n++} END{print n+0}')"
# Two site-specific UI/browser service probes from the deployed collector are
# intentionally omitted from this public snapshot. Campaign validation relies
# on the container and model-process counts above.
emit memory_available_kib "$(awk '/^MemAvailable:/{print $2}' /proc/meminfo)"
emit system_vendor "$(read_dmi sys_vendor)"
emit product_name "$(read_dmi product_name)"
emit product_version "$(read_dmi product_version)"
emit board_vendor "$(read_dmi board_vendor)"
emit board_name "$(read_dmi board_name)"
emit board_version_smbios "$(read_dmi board_version)"
emit physical_pcb_revision not-exposed
emit bios_vendor "$(read_dmi bios_vendor)"
emit bios_version "$(read_dmi bios_version)"
emit bios_date "$(read_dmi bios_date)"
emit ec_firmware_version "$EC_FIRMWARE_VERSION"
emit ec_driver_commit "$(git -C "$HOME/src/ec-su_axb35-linux" rev-parse HEAD 2>/dev/null || printf 'unavailable')"
ec_module_path="$(modinfo -n ec_su_axb35 2>/dev/null || true)"
if [[ -r "$ec_module_path" ]]; then
  emit ec_driver_module_sha256 "$(sha256sum "$ec_module_path" | awk '{print $1}')"
else
  emit ec_driver_module_sha256 unavailable
fi
# This file exists on the Linux benchmark targets.
# shellcheck disable=SC1091
emit os_pretty_name "$(. /etc/os-release; printf '%s' "$PRETTY_NAME")"
emit kernel "$(uname -r)"
emit kernel_cmdline_relevant "$(tr ' ' '\n' < /proc/cmdline | grep -E '^(amd_iommu|iommu)=|^(amdgpu|ttm)\.' | paste -sd, - || true)"
emit gpu_pci_bdf "$GPU_PCI"
emit gpu_identity "$(lspci -Dnn -s "$GPU_PCI" 2>/dev/null || printf 'unavailable')"
emit gpu_perf_level "$(cat "$GPU/power_dpm_force_performance_level")"
emit gpu_od_min_mhz "$(awk '/^0:/{gsub(/[^0-9]/,"",$2);print $2;exit}' "$GPU/pp_od_clk_voltage")"
emit gpu_od_max_mhz "$(awk '/^1:/{gsub(/[^0-9]/,"",$2);print $2;exit}' "$GPU/pp_od_clk_voltage")"
emit ec_power_mode "$(cat /sys/class/ec_su_axb35/apu/power_mode 2>/dev/null || printf 'unavailable')"

for fan in /sys/class/ec_su_axb35/fan*; do
  [[ -d "$fan" ]] || continue
  fan_name="$(basename "$fan")"
  emit "${fan_name}_mode" "$(cat "$fan/mode" 2>/dev/null || printf 'unavailable')"
  emit "${fan_name}_rampup_curve" "$(cat "$fan/rampup_curve" 2>/dev/null || printf 'unavailable')"
  emit "${fan_name}_rampdown_curve" "$(cat "$fan/rampdown_curve" 2>/dev/null || printf 'unavailable')"
done

emit podman_version "$(podman --version 2>/dev/null || printf 'unavailable')"
emit container_reference "$IMAGE"
if podman image exists "$IMAGE"; then
  emit container_id "$(podman image inspect "$IMAGE" --format '{{.Id}}')"
  emit container_repo_digests "$(podman image inspect "$IMAGE" --format '{{json .RepoDigests}}')"
  emit container_created "$(podman image inspect "$IMAGE" --format '{{.Created}}')"
  emit llama_cpp_version "$(podman run --rm --pull=never --network=none \
    --entrypoint llama-cli "$IMAGE" --version 2>&1 || true)"
else
  emit container_id unavailable
  emit container_repo_digests unavailable
  emit container_created unavailable
  emit llama_cpp_version unavailable
fi

emit package_mesa_vulkan "$(rpm -q mesa-vulkan-drivers 2>/dev/null || printf 'unavailable')"
emit package_amd_gpu_firmware "$(rpm -q amd-gpu-firmware 2>/dev/null || printf 'unavailable')"
emit package_linux_firmware "$(rpm -q linux-firmware 2>/dev/null || printf 'unavailable')"

model_dir="$(dirname "$MODEL")"
model_base="$(basename "$MODEL")"
model_files=("$MODEL")
if [[ "$model_base" == *-00001-of-*.gguf ]]; then
  model_prefix="${model_base%%-00001-of-*}"
  shopt -s nullglob
  split_files=("$model_dir"/"$model_prefix"-*.gguf)
  shopt -u nullglob
  (( ${#split_files[@]} > 0 )) && model_files=("${split_files[@]}")
fi

emit model_file_count "${#model_files[@]}"
index=0
for model_file in "${model_files[@]}"; do
  index=$((index + 1))
  suffix="$(printf '%02d' "$index")"
  emit "model_${suffix}_name" "$(basename "$model_file")"
  emit "model_${suffix}_bytes" "$(stat -c %s "$model_file" 2>/dev/null || printf 'unavailable')"
  if [[ "$HASH_MODE" == "full" ]]; then
    emit "model_${suffix}_sha256" "$(sha256sum "$model_file" | awk '{print $1}')"
  else
    emit "model_${suffix}_sha256" not-collected
  fi
done
