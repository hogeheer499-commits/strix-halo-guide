---
name: Benchmark Report
about: Share benchmark results from your Strix Halo system
title: "[Benchmark] "
labels: benchmark
assignees: ''
---

## System
- **Device:** (e.g., Beelink GTR9 Pro, Framework Desktop 13)
- **CPU/GPU:** (e.g., Ryzen AI MAX+ 395 / Radeon 8060S)
- **RAM:** (e.g., 128GB LPDDR5X)
- **BIOS UMA setting:**
- **IOMMU setting:**
- **OS:** (`lsb_release -a`)
- **Kernel:** `uname -r` output
- **Mesa:** `vulkaninfo --summary 2>&1 | grep driverInfo` output
- **ROCm:** `rocminfo | head` or container/runtime version, if relevant
- **Ollama:** `ollama --version` output
- **tuned profile:** `tuned-adm active` output
- **Vulkan ICD:** RADV / AMDVLK / other

## Benchmark
- **Model:**
- **Quant / model file:**
- **Backend:** (Ollama Vulkan / llama-bench RADV / llama-server RADV / Lemonade ROCm / vLLM / other)
- **Tool version / build / container:**
- **Context length:**
- **Prompt tokens:**
- **Generated tokens:**
- **Parallel slots / concurrency, if applicable:**
- **Command used:**

## Results
```
paste benchmark output here
```

Attach or link CSV/raw logs if possible.

## Comparison
How do these results compare to the guide's numbers? Better, worse, or similar?

## Notes
Any other relevant observations (temperature, power draw, stability, etc.)
