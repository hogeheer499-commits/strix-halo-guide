# Research Findings - Current Reconciled Notes

This file tracks external Strix Halo research and how it relates to this guide. It is not the benchmark source-of-truth; current measured numbers live in `BENCHMARKS.md` and the README.

## Source 1: kyuz0/amd-strix-halo-toolboxes

**What it does best:** turnkey containers, automated rebuilds, backend variants, and community-standard setup paths.

**Configuration notes:**
- OS baseline: Fedora 42/43 in many examples
- Kernel baseline: 6.18.6+ commonly recommended
- Firmware warning: `linux-firmware-20251125` breaks ROCm on Strix Halo
- Container tags include Vulkan RADV, Vulkan AMDVLK, ROCm 6.4.4, ROCm 7.2, and ROCm nightlies
- Common flags: `-fa 1`, `--no-mmap`, full GPU offload

**How this guide uses it:** kyuz0's containers are still the easiest way to stay current with llama.cpp rebuilds. Our b8298 to b8460 finding validates why auto-rebuilt containers matter.

## Source 2: lhl/strix-halo-testing

**What it does best:** deep backend testing, long-context behavior, and rocWMMA experiments.

**Key findings used here:**
- `amd_iommu=off` measured faster than default/`iommu=pt` for memory reads in lhl testing
- Backend choice changes with context length
- Standard ROCm can degrade badly at long context
- lhl's tuned rocWMMA branch can beat standard ROCm and Vulkan at 32K context

**Long-context reference data from lhl, gpt-oss-120b tg32:**

| Context | Vulkan AMDVLK | ROCm Standard | ROCm rocWMMA-tuned |
|---------|---------------|---------------|---------------------|
| 2K | 50.05 | 46.56 | 48.97 |
| 8K | 43.15 | 32.65 | 43.55 |
| 16K | 38.46 | 25.50 | 40.91 |
| 32K | 31.54 | 17.82 | 36.43 |

**Open follow-up for this guide:** reproduce long-context results locally on current RADV/ROCm builds and add TTFT/ITL.

## Source 3: kyuz0/amd-strix-halo-vllm-toolboxes

**What it does best:** vLLM serving on gfx1151 with TheRock/ROCm patches.

**Known areas:**
- vLLM works but is harder to set up than Ollama or direct llama.cpp
- Some vision models need MIOpen profiling workarounds
- RDMA clustering has been demonstrated with multiple Framework Desktop systems

**Open follow-up for this guide:** vLLM should be treated as a serving/concurrency benchmark target, not as the first easy setup path.

## Source 4: ROCm/ROCm and llama.cpp issues

**Old state:** Earlier March notes said kernel 6.19.4 made ROCm unusable because gfx1151 was detected as gfx1100 and containers segfaulted.

**Current corrected state:** ROCm is no longer documented as "all broken" on kernel 6.19.x. It works when these variables are set before ROCm/HIP binaries:

```bash
export HSA_OVERRIDE_GFX_VERSION=11.5.1
export HSA_ENABLE_SDMA=0
```

**Measured local result:** ROCm HIP b8460 reached 1047 pp512 and 54.67 tg128 on Qwen3.5-35B-A3B Q4_K_M. Vulkan RADV b8460 remains faster on the same short-context workload at 1080 pp512 and 64.85 tg128.

## Source 5: Strix Halo Wiki and llm-tracker

**What they do best:** index community resources, cross-link hardware notes, and collect independent benchmark pointers.

**Key imported context:**
- Extreme-context behavior can look very different from short-context tg128
- Backend choice should be documented per workload, not as a single global winner
- Community readers value raw command lines, versions, and reproducibility more than headline claims

## Our Current Findings

1. **AMDVLK ICD hijacking:** AMDVLK's ICD file could silently override RADV for direct llama.cpp commands, creating false regression reports. Current recommendation: uninstall AMDVLK and verify RADV in benchmark output.
2. **llama.cpp build age matters:** b8298 to b8460 gave +24% pp and +25% tg on Qwen3.5-35B-A3B MoE via Vulkan RADV.
3. **Vulkan RADV is current short-context winner:** On the measured Qwen MoE workloads, RADV beats ROCm HIP on both pp and tg with the same b8460 source.
4. **ROCm still matters:** Use ROCm for hipBLASLt, vLLM, batch/concurrency testing, and long-context/rocWMMA experiments.
5. **Ollama remains the easy path:** the controlled 2026-05-03 API run measured Ollama 0.21.2 on Qwen3.6-35B-A3B at 50.5 t/s warm average, about 20-21% below direct llama-bench on current short-context data.
6. **Continuous batching changes the serving story:** the 2026-05-03 `llama-server` Qwen3.6 test reached 162 t/s aggregate at `-np 8` with ~0.31 s TTFT. `-np 16` plateaued at 166 t/s while per-request speed fell to 10.4 t/s.
7. **Live system readiness matters:** The 2026-05-01 audit now confirms Mesa 26.0.6, Ollama 0.21.2, AMDVLK removed, GPU clock correct, linux-firmware safe, and `tuned accelerator-performance` active. Keep those checks in the benchmark preflight.

## Next Research Tasks

1. Build a single CSV/JSON benchmark corpus for all existing data.
2. Re-run a small smoke benchmark under the verified May 2026 state to confirm Mesa 26.0.6 did not change headline numbers.
3. Extend the new multi-user `llama-server` baseline with power draw and a vLLM comparison.
4. Add local long-context tests at 32K, 64K, and 128K with RADV, ROCm HIP, and rocWMMA where practical.
5. Run same-model comparisons against Mac Studio, DGX Spark, and RTX cards only when exact model/quant/backend details are available.
