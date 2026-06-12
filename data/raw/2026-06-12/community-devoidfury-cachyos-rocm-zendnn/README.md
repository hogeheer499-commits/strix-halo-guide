# Community Beelink GTR9 Pro CachyOS ROCm/ZenDNN Crossover

Status: community-reported evidence, not a first-party headline claim.

Source:

- Original discussion report: https://github.com/hogeheer499-commits/strix-halo-guide/discussions/2#discussioncomment-17276639
- Follow-up with VMM / rocWMMA note: https://github.com/hogeheer499-commits/strix-halo-guide/discussions/2#discussioncomment-17277012
- Follow-up with exact llama.cpp commit and patch diff: https://github.com/hogeheer499-commits/strix-halo-guide/discussions/2#discussioncomment-17281378

## Why This Matters

This is a second Beelink GTR9 Pro owner stack, separate from the guide's primary Ubuntu 24.04 Beelink measurements. It adds:

- CachyOS instead of Ubuntu
- `linux-cachyos-server` 7.0.11-1
- `amd_iommu=on`, kept partly for NPU visibility
- ROCm 7.2.4-1
- local ZenDNN
- same-host Vulkan/RADV versus ROCm/HIP comparison on Qwen3.6 27B MTP `UD-Q6_K_XL`
- negative notes for VMM and `GGML_HIP_ROCWMMA_FATTN`

The useful signal is prompt-processing and long-context backend behavior, not decode speed. ROCm + ZenDNN roughly doubled pp5000 versus the Vulkan row on this setup, while decode stayed around 8 t/s on both backends.

## System

- System: Beelink GTR9 Pro
- CPU/GPU: AMD Ryzen AI MAX+ 395 / Radeon 8060S `gfx1151`
- Memory: ROCm reported 126976 MiB total VRAM/unified memory
- BIOS memory setting: video reserved / UMA set to 512MB
- OS: CachyOS
- Kernel: `linux-cachyos-server 7.0.11-1`
- `uname`: `Linux ai365 7.0.11-1-cachyos #1 SMP PREEMPT_DYNAMIC Fri, 05 Jun 2026 09:37:35 +0000 x86_64 GNU/Linux`
- Kernel parameters:

```text
ttm.pages_limit=32505856 ttm.page_pool_size=32505856 amd_iommu=on amdgpu.mcbp=0 amdgpu.cwsr_enable=0 amdgpu.si_support=0 amdgpu.cik_support=0 amdgpu.dc=1 amdgpu.dpm=1
```

## Software

- llama.cpp commit: `1593d5684d077c07fc788e9527ec1bd52287de7f`
- Commit message: `docker : support specifying the GCC version for CUDA (#24447)`
- ROCm: `7.2.4-1`
- ZenDNN: local build from upstream repo
- Model: `unsloth/Qwen3.6-27B-MTP-GGUF`
- File: `Qwen3.6-27B-MT-UD-Q6_K_XL.gguf`
- Quant: `UD-Q6_K_XL`

The contributor used local build tweaks. The exact diff was posted in the discussion:

- commented out a CDNA3 force-MMQ block in `ggml/src/ggml-cuda/mmq.cu`; the contributor reported this seemed to improve performance
- added `static_cast<int32_t>(iid1)` in `ggml/src/ggml-zendnn/ggml-zendnn.cpp`; the contributor reported this was required to build with local ZenDNN

## Command

```bash
build/bin/llama-bench \
    --n-gpu-layers 999 \
    --flash-attn on \
    -m /storage/models/qwen3.6-27b/Qwen3.6-27B-MT-UD-Q6_K_XL.gguf \
    -b 1024 \
    -ub 512 \
    -p 5000 \
    -n 512
```

## Results

| Backend | Workload | pp t/s | tg t/s | Notes |
|---------|----------|-------:|-------:|-------|
| Vulkan/RADV + ZenDNN | pp5000/tg512 | 155.89 +/- 0.39 | 8.09 +/- 0.01 | Device line reported `RADV STRIX_HALO`, `uma: 1`, `int dot: 1`, `matrix cores: KHR_coopmat`. |
| ROCm/HIP + ZenDNN | pp5000/tg512 | 303.20 +/- 2.40 | 8.38 +/- 0.00 | ROCm reported one `gfx1151` device, `VMM: no`, `VRAM: 126976 MiB`. |
| ROCm/HIP + ZenDNN | pp40000/tg1024 | 227.44 +/- 3.28 | 8.39 +/- 0.00 | Long-prompt bonus round. |

## Negative / Caveat Notes

- VMM: contributor reported VMM would build but crashed when loading any model.
- `GGML_HIP_ROCWMMA_FATTN`: contributor reported it remained a performance hit, with prompt-processing degrading faster than without it.
- `amd_iommu=on`: contributor was testing VMM and noted the main visible difference was that the NPU worked with IOMMU on.
- NPU/FastFlowLM: contributor experimented with using all three processors but did not get far enough for a guide claim.
- This is a community row with local patches and ZenDNN; do not compare it as a stock same-build Vulkan-vs-ROCm result.
- Decode stayed around 8 t/s, so this is not a speed headline.

## Guide Interpretation

This belongs in the guide as backend-crossover evidence:

- Vulkan/RADV remains the simplest default for direct GGUF chat and generation-heavy rows.
- ROCm/HIP remains worth testing for prompt-heavy, long-context, RAG, and batch/server experiments.
- ZenDNN and local build details can matter enough that raw build provenance must travel with the number.
- IOMMU-on/NPU workflows deserve a separate evidence lane; the guide's default `amd_iommu=off` path should not imply NPU-aware users have no route.
