# Framework Desktop Strix Halo Local LLM Results Wanted


## Goal

Framework Desktop owners can help answer whether the measured Beelink Strix Halo local LLM rows transfer cleanly to Framework Desktop hardware.

Useful results include fast, slow, failed, and contradictory runs.

## Most Useful First Tests

| Priority | Test | Why |
|----------|------|-----|
| 1 | Qwen3-Coder 30B-A3B UD-Q4_K_XL direct `llama-bench` | Best comparison against the balanced 96.76 t/s row. |
| 2 | Qwen3-Coder 30B-A3B Q4_K_S direct `llama-bench` | Checks whether the 98.51 t/s speed-first row transfers. |
| 3 | Qwen3.6 35B-A3B UD-Q4_K_M direct `llama-bench` | Checks all-rounder direct path. |
| 4 | Ollama Qwen3.6 API row | Checks easy user-facing path. |
| 5 | Wall-power readings during the same command | Converts t/s into practical heat/efficiency context. |

## Required Metadata

- Framework Desktop CPU/GPU SKU
- memory size
- BIOS version
- UMA setting
- IOMMU setting
- OS/kernel
- Mesa/RADV, AMDVLK, or ROCm version
- tool and build commit
- model file/source/hash
- exact command
- raw output or CSV
- power profile
- cooling/fan profile if changed

## Where To Send Results

- Benchmark report: https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=benchmark-report.md
- Power report: https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=power-report.md
- Discussion: https://github.com/hogeheer499-commits/strix-halo-guide/discussions

## Suggested Share Text

```text
I reproduced one Strix Halo local LLM row on Framework Desktop. Here is my hardware, command, raw output, and where it matched or differed from the guide.
```

Do not ask for upvotes or coordinated stars. The useful contribution is the measurement.
