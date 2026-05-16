# Power Measurement Baseline

This file records available power telemetry. It is not a tokens-per-watt result.

## 2026-05-03 Probe

Status: candidate `amdgpu` PPT telemetry exists, but wall-power is not validated.

Unavailable:

- `/sys/class/powercap` did not expose usable `energy_uj` or package power data in this environment.
- No wall meter or smart-plug export has been connected to this dataset yet.

Available candidate telemetry:

```text
/sys/class/drm/card1/device/hwmon/hwmon6/name = amdgpu
/sys/class/drm/card1/device/hwmon/hwmon6/power1_label = PPT
/sys/class/drm/card1/device/hwmon/hwmon6/power1_average = <microwatts>
/sys/class/drm/card1/device/hwmon/hwmon6/power1_input = <microwatts>
```

Short idle/transient sample observed values around 24-39 W:

```text
25.1 W
28.1 W
25.1 W
24.1 W
26.1 W
39.1 W
31.1 W
27.0 W
25.1 W
25.0 W
```

Interpretation:

- This is likely AMD GPU/APU PPT telemetry, not full system wall power.
- It may be useful for relative load comparisons on the same machine.
- Do not publish total tokens-per-watt or ownership-cost claims from this alone.
- If used, label it clearly as `amdgpu PPT watts`, not wall watts.

Minimum protocol before publishing power data:

1. Record the exact telemetry path and label.
2. Record idle baseline for at least 60 seconds.
3. Record benchmark load for the full run, with timestamps.
4. Repeat each benchmark at least 3 times.
5. Prefer wall-meter data for public tokens/W. If only PPT is available, publish it separately as GPU/APU telemetry.

Helper:

```bash
python3 scripts/sample_power.py --seconds 60 --interval 1 > data/raw/YYYY-MM-DD/power-idle.csv
```

## 2026-05-16 Beelink PPT Telemetry

Status: local amdgpu `PPT` telemetry captured during real benchmark windows. This is still not wall power.

Structured data:

- [`data/beelink_power_telemetry.csv`](data/beelink_power_telemetry.csv)

Raw data:

- [`data/raw/2026-05-16/beelink-power-telemetry/`](data/raw/2026-05-16/beelink-power-telemetry/)

Environment:

- Beelink GTR9 Pro / Ryzen AI MAX+ 395 / 128GB.
- Kernel 6.19.4.
- Mesa/RADV 26.0.6.
- `tuned` profile: `accelerator-performance`.
- Benchmark-noise services paused; the normal workspace session stayed active.
- GPU clock remained in the high-performance state, so the idle PPT sample is not a whole-machine idle-power claim.

Measured rows:

| Workload | Backend | Model | Result | amdgpu PPT mean | amdgpu PPT median | Rough PPT J/token |
|----------|---------|-------|--------|-----------------|-------------------|-------------------|
| Paused-services idle sample | n/a | n/a | n/a | 68.10 W | 68.03 W | n/a |
| Qwen3-Coder r20 | Vulkan/RADV, llama.cpp b9172 | Qwen3-Coder 30B-A3B UD-Q4_K_XL | 92.85 tg128, 1389.04 pp512 | 111.42 W | 119.10 W | 1.20 |
| Qwen3.6 Q4_K_M r20 | Vulkan/RADV, llama.cpp b9172 | Qwen3.6 35B-A3B Q4_K_M | 74.86 tg128, 1113.99 pp512 | 112.66 W | 119.10 W | 1.51 |

Interpretation:

- These rows are useful local Beelink telemetry, not public wall-power efficiency claims.
- The Qwen3-Coder speed in this power run is lower than the 96-97 t/s headline because it used the b9172 power-sampling run, not the b9049 headline campaign.
- The rough J/token values divide token-generation speed by run-window PPT mean; they should be treated as same-machine context only.
- The next publishable efficiency step is a wall-meter run on the Beelink, ideally matching the same Qwen3-Coder and Qwen3.6 commands.
