# System Audit — 2026-03-20

## Hardware
| Component | Value |
|-----------|-------|
| System | Beelink GTR9 Pro |
| CPU | AMD Ryzen AI MAX+ 395 (32C/64T, Zen 5) |
| GPU | Radeon 8060S (gfx1151, RDNA 3.5 iGPU) |
| RAM | 128GB LPDDR5X-8000 (unified) |
| Device ID | 0x1586 |

## Software
| Parameter | Value | Previous | Changed? |
|-----------|-------|----------|----------|
| Kernel | 6.19.4-061904-generic | 6.18.14 | YES - major upgrade |
| Mesa (RADV) | 26.0.2 (kisak PPA) | 26.0.1 | YES - minor upgrade |
| AMDVLK | 2025.Q2.1 | 2025.Q2.1 | No |
| Ollama | 0.18.2 | unknown | Unknown |
| tuned profile | accelerator-performance | was not running | YES - fixed |
| linux-firmware | 20240318 | same | No (safe, not broken 20251125) |
| THP | always | unknown | - |

## Kernel Parameters
```
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash amd_iommu=off amdgpu.gttsize=131072 ttm.pages_limit=31457280 amdgpu.cwsr_enable=0 amdgpu.cwsr_enable=0 amdgpu.cwsr_enable=0"
```
Note: `amdgpu.cwsr_enable=0` is duplicated 3x (cosmetic issue, no functional impact).

## Memory
```
              total        used        free      shared  buff/cache   available
Mem:          124Gi        13Gi       105Gi        44Mi       6.8Gi       110Gi
Swap:          8.0Gi          0B       8.0Gi
```

## GPU
- Clock: 2900 MHz (highest DPM state, no clock bug)
- TTM pages_limit: 31457280
- GTT size: configured via GRUB (131072 = 128GB)

## Vulkan Drivers
- RADV: Mesa 26.0.2 (kisak-mesa PPA)
- AMDVLK: 2025.Q2.1
- Ollama configured: RADV (via AMD_VULKAN_ICD=RADV + VK_ICD_FILENAMES)

## Ollama Configuration
```
OLLAMA_HOST=0.0.0.0:11434
OLLAMA_VULKAN=1
HIP_VISIBLE_DEVICES=-1
OLLAMA_FLASH_ATTENTION=1
OLLAMA_CONTEXT_LENGTH=8192
AMD_VULKAN_ICD=RADV
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json
OLLAMA_NUM_BATCH=512
OLLAMA_NUM_PARALLEL=1
```

## ROCm Containers (Distrobox)
| Container | Image | Status |
|-----------|-------|--------|
| rocm | rocm/dev-ubuntu-24.04:7.1-complete | Exited |
| llama-rocm-7rc-rocwmma | kyuz0:rocm-7rc-rocwmma | Created |
| llama-rocm-72 | kyuz0:rocm-7.2 | Exited |
| llama-rocm-72-new | kyuz0:rocm-7.2 | Exited |
| llama-rocm-644 | kyuz0:rocm-6.4.4 | Exited |
| vllm-gfx1151 | kyuz0/vllm-therock-gfx1151 | Exited |
| llama-vulkan-amdvlk | kyuz0:vulkan-amdvlk | Exited |
| llama-vulkan-radv | kyuz0:vulkan-radv | Exited |

## Critical Finding
ALL ROCm containers segfault on kernel 6.19.4. GPU is detected as "gfx1100 (0x1100)" instead of "gfx1151". This is a kernel 6.19.x regression affecting ROCm/HIP compatibility.

Previously working on kernel 6.18.14.
