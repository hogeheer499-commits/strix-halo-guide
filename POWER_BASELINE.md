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
