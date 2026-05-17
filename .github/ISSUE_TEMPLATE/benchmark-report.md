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
- **Model source / download repo:**
- **Quant / model file:**
- **Model hash, if available:**
- **Backend:** (Ollama Vulkan / llama-bench RADV / llama-server RADV / Lemonade ROCm / vLLM / other)
- **Tool version / build / container:**
- **Context length:**
- **Prompt tokens:**
- **Generated tokens:**
- **Repeats:**
- **Parallel slots / concurrency, if applicable:**
- **Command used:**

```bash
paste exact command here
```

## Results
```
paste benchmark output here
```

Attach or link CSV/raw logs if possible. `llama-bench -o csv` output is ideal for direct comparisons.

## Comparison
How do these results compare to the guide's numbers? Better, worse, or similar?

If you are reproducing a specific guide row, link it here:

## Notes
Any other relevant observations: temperature, power draw, clocks, throttling, background load, stability, model loading time, storage path, or failure mode.

Slower, failed, and surprising results are useful too if the setup details are complete.
