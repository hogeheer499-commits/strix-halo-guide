# Strix Halo Local LLM Power Efficiency And Tokens Per Watt


## Why This Page Exists

Tokens/sec is not enough for homelab, workstation, and always-on local AI users. Wall power, cooling, noise, and tokens/J decide whether a setup is practical.

## Current Community Context

The guide currently includes community wall-power context for workloads such as:

- Qwen3-Coder around 150 W / 1.6 J/token
- Qwen3.6 around 148 W / 2.0 J/token
- gpt-oss-120b around 174 W / 3.1 J/token
- Qwen3-Coder-Next around 137 W / 3.4 J/token

These are workload-specific community rows, not universal TDP claims.

## Measurement Checklist

Include:

- meter/tool used
- whether it measures wall power, board power, UPS power, smart plug power, or telemetry
- sample interval
- idle baseline before and after
- sustained generation power window
- prompt-processing peak if measured
- tokens/sec
- J/token or tokens/J if calculated
- raw readings or CSV if possible
- cooling/fan profile
- ambient temperature if known
- attached displays/peripherals if relevant

## Do Not Mix These

- Wall power
- APU PPT telemetry
- GPU-only telemetry
- PSU estimates
- battery discharge estimates

If the source is `amdgpu` PPT, label it as PPT, not total system wall power.

## Submit A Power Report

Use:

```text
https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=power-report.md
```

Slower results are useful. Failed runs are useful. Incomplete power readings are useful if they are labeled clearly.
