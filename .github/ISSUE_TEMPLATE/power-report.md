---
name: Power / Efficiency Report
about: Share wall-power or board-power measurements for Strix Halo LLM workloads
title: "[Power] "
labels: benchmark, reproducibility
assignees: ''
---

## System
- **Device:** (e.g., Beelink GTR9 Pro, Corsair AI Workstation 300, Framework Desktop, GMKtec EVO-X2)
- **CPU/GPU:** (e.g., Ryzen AI MAX+ 395 / Radeon 8060S)
- **RAM:** (e.g., 128GB LPDDR5X)
- **BIOS version and date:** `cat /sys/class/dmi/id/bios_version /sys/class/dmi/id/bios_date` output
- **BIOS UMA setting:**
- **IOMMU setting:**
- **OS / kernel:** (`lsb_release -a`, `uname -r`)
- **Mesa / ROCm / driver stack:**
- **Backend / build / container:**
- **Power profile:** (`cat /sys/firmware/acpi/platform_profile`, `tuned-adm active`, `powerprofilesctl get`, or equivalent)
- **Cooling / fan profile / ambient room temp, if known:**

## Measurement Method
- **Meter / tool:** (wall meter, smart plug, board sensor, UPS, vendor tool, etc.)
- **What is measured:** whole-system wall power / board power / APU PPT / other
- **Sample interval:** (e.g., 1 sec, 5 sec, event-based plus polling)
- **Raw readings attached:** yes / no
- **Idle baseline before run:** W
- **Idle baseline after run:** W
- **Background services / user activity during run:**

## Benchmark
- **Model and quant:**
- **Model source / hash, if available:**
- **Command used:**

```bash
paste command here
```

## Results
- **pp throughput:** tokens/sec, prompt length, repeats
- **tg throughput:** tokens/sec, generated tokens, repeats
- **Peak or sustained pp power:** W
- **Sustained tg power:** W
- **Tokens/J or J/token, if already calculated:**
- **Above-idle / marginal J/token, if calculated:**

```text
paste benchmark output and/or power summary here
```

## Notes
Anything that could affect the result: thermal state, clocks, throttling, plugged-in peripherals, display attached, GUI/no-GUI, container limits, network storage, or meter limitations.

## Before you post
Remove or replace anything that is not needed to reproduce the result: host name (`<host>`), user name in paths (`~`), IP and MAC addresses (`<lan-ip>`), serial numbers (including `dmidecode` output), tokens and passwords, and full process or port listings (`ps`, `ss`, `docker ps`). Keep versions, flags, clocks, power profile, hashes, and the exact command. See [CONTRIBUTING.md](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/CONTRIBUTING.md#before-you-post-what-to-redact).
