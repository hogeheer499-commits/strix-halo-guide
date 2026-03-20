---
name: Benchmark Report
about: Share benchmark results from your Strix Halo system
title: "[Benchmark] "
labels: benchmark
assignees: ''
---

## System
- **Device:** (e.g., Beelink GTR9 Pro, Framework Desktop 13)
- **Kernel:** `uname -r` output
- **Mesa:** `vulkaninfo --summary 2>&1 | grep driverInfo` output
- **Ollama:** `ollama --version` output
- **tuned profile:** `tuned-adm active` output

## Benchmark
- **Model:**
- **Backend:** (Ollama Vulkan / llama-bench RADV / llama-bench AMDVLK / ROCm)
- **Command used:**

## Results
```
paste benchmark output here
```

## Comparison
How do these results compare to the guide's numbers? Better, worse, or similar?

## Notes
Any other relevant observations (temperature, power draw, stability, etc.)
