# Community GMKtec MTP Issue #18

Source: https://github.com/hogeheer499-commits/strix-halo-guide/issues/18

Contributor: mottledMantis.

This directory stores the community-reported GMKtec EVO-X2 rerun for the exact Qwen3.6 MTP IQ4_XS-Q8nextn GGUF referenced by the guide.

## System

- Device: GMKtec EVO-X2.
- APU: Ryzen AI MAX+ 395 / Radeon 8060S.
- Memory: 96GB unified memory.
- BIOS UMA: 1GB.
- IOMMU: disabled.
- OS/kernel: Ubuntu 26.04 LTS, kernel 7.0.0-15-generic.
- Mesa: RADV 26.0.3-1ubuntu1.
- Backend: llama-server Vulkan/RADV.
- Build: llama.cpp b9235, commit `d14ce3dab`.
- Model: `localweights/Qwen3.6-35B-A3B-MTP-IQ4_XS-Q8nextn-GGUF`.
- Model SHA256: `4d2349305663bc59bacab26d8eba8ed1218de84b8d1f0456208037e13efa9a98`.

## File

- `qwen36_mtp_iq4xs_q8nextn_b9235.csv`: normalized summary rows from the issue report.

## Results

| Mode | Mean t/s | Min-Max | Read |
|------|---------:|--------:|------|
| no MTP | 74.716 | 65.573-114.888 | Baseline for the exact MTP GGUF on this GMKtec stack. |
| `draft-n=2` | 93.292 | 71.793-161.536 | Best broad average in this community rerun. |
| `draft-n=3` | 93.012 | 68.275-175.974 | Slightly lower average, higher single-prompt peak. |

## Why It Matters

This is the first independent community reproduction of the guide's Qwen3.6 MTP IQ4_XS-Q8nextn route on another Strix Halo chassis.

It is valuable because it confirms:

- the exact `localweights` MTP GGUF works on GMKtec EVO-X2
- the MTP speedup shape transfers to another Strix Halo system
- `draft-n=2` can be the better broad-average setting even when `draft-n=3` has a higher single-prompt peak
- the best community broad MTP average reported so far is 93.292 t/s, slightly above the guide's local Beelink b9235 92.300 t/s row

This still does not justify a broad 100 t/s Qwen3.6 claim. The correct public interpretation is: MTP can exceed 100 t/s on favorable prompts, while broad six-prompt averages are currently around 92-93 t/s in the measured Beelink and GMKtec rows.
