# Retail Box To Working Local AI

This protocol measures the setup friction between opening a retail Strix Halo
system and reaching a reproducible local-AI result.

It is intended for review units, loaner systems, cross-OEM comparisons, and
community reproductions. It does not claim a current time-to-first-result. A
time, intervention count, or pass rate becomes public only after its completed
artifact is linked.

## What To Measure

Use one continuous timeline and record every manual intervention.

| Checkpoint | Pass condition | Evidence |
|---|---|---|
| 1. Hardware identified | Exact system, RAM, BIOS, firmware, and power profile recorded | Host snapshot |
| 2. BIOS ready | UMA and IOMMU policy recorded with vendor labels | Photo or setup note |
| 3. Linux ready | OS, kernel, Mesa, Vulkan ICD, and GPU device visible | Command output |
| 4. Setup completed | `setup.sh` completes or every failed/manual step is recorded | Installer log |
| 5. Runtime healthy | Ollama or the selected runtime sees the Radeon 8060S | Runtime log |
| 6. First model response | Named model returns a correct response through the intended interface | Request and response |
| 7. Capability check | Required text, vision, tool, server, or workload smoke passes | Workload artifact |
| 8. Restart persistence | The same route works after service restart and, when in scope, a full reboot | Repeat log |

## Required Summary

Publish these values together:

- system and configuration;
- start and finish timestamps in UTC;
- elapsed seconds to each checkpoint;
- number of manual interventions;
- number and category of failed steps;
- documentation or external pages consulted;
- exact runtime, model, quant, and command;
- final pass, partial pass, or blocked state;
- service-restart and full-reboot result;
- links to the raw capture and any correction.

Do not subtract download, reboot, troubleshooting, or manual-edit time unless
the report also publishes the complete wall-clock result. If network download
time is excluded for a controlled comparison, publish both values and explain
the exclusion.

## Failure Categories

Use one primary category per failed step:

- `firmware_or_bios`
- `linux_or_kernel`
- `graphics_or_vulkan`
- `rocm_or_runtime`
- `model_or_quant`
- `memory_or_storage`
- `network_or_distribution`
- `thermal_or_power`
- `documentation`
- `unknown`

Preserve failed attempts. They are part of the buyer-friction evidence.

## Capture Template

Copy [`data/buyer_path_validation_template.csv`](data/buyer_path_validation_template.csv)
into a dated raw-evidence directory and fill one row per checkpoint or failed
step. Put screenshots, logs, commands, and a short `README.md` beside it.

Suggested evidence path:

```text
data/raw/YYYY-MM-DD/buyer-path-<vendor>-<system>/
```

The completed raw directory is the source of truth. A buyer-facing summary may
then be linked from the README, partner brief, or a named vendor/system page.

## Campaign Value

The benchmark result shows what the hardware can do. This protocol shows how
difficult it is for a buyer to get there.

For buyers, it creates a realistic route from purchase to a working workload.
For vendors, it identifies exact BIOS, firmware, packaging, documentation, and
runtime friction that can be removed. For reviewers, it separates a polished
demo from a repeatable retail-system experience.

Support, loaned hardware, early access, or sponsorship must follow the
disclosure and independence rules in [`PARTNERSHIP.md`](PARTNERSHIP.md).
