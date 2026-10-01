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
- **Configured memory speed:** `sudo dmidecode -t memory | grep -i "configured memory speed"` output (do not paste serial numbers)
- **Visible RAM:** `free -g` output
- **BIOS / EC (embedded controller) version and BIOS date:** `cat /sys/class/dmi/id/bios_version /sys/class/dmi/id/bios_date` output
- **BIOS UMA setting:**
- **GTT / TTM limits:** `cat /sys/module/amdgpu/parameters/gttsize /sys/module/ttm/parameters/pages_limit` output, or the GRUB parameters you set
- **IOMMU setting:**
- **OS:** (`lsb_release -a`)
- **Kernel:** `uname -r` output
- **Mesa:** `vulkaninfo --summary 2>&1 | grep driverInfo` output
- **ROCm:** `rocminfo | head` or container/runtime version, if relevant
- **Ollama:** `ollama --version` output
- **Ollama model manifest ID, if using Ollama:** `ollama list` ID column for the tested model
- **Ollama model parameters, if using Ollama:** `ollama show <model> --parameters` output
- **Platform profile:** `cat /sys/firmware/acpi/platform_profile` output
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
- **Speculative decoding (MTP / draft model):** on / off
- **Draft model and `draft_num_predict` (or equivalent draft-token setting), if on:**
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

## Before you post
Remove or replace anything that is not needed to reproduce the result: host name (`<host>`), user name in paths (`~`), IP and MAC addresses (`<lan-ip>`), serial numbers (including `dmidecode` output), tokens and passwords, and full process or port listings (`ps`, `ss`, `docker ps`). Keep versions, flags, clocks, power profile, hashes, and the exact command. See [CONTRIBUTING.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/CONTRIBUTING.md#before-you-post-what-to-redact).
