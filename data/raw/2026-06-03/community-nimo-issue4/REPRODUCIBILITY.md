# Reproducibility Notes

This file is the checklist for copying, rerunning, or challenging benchmark
claims from this share bundle. The README is the human-facing entry point;
`data/headline_claims.csv`, `manifest.csv`, and `RAW-BENCHMARK-ROWS.md` are
the structured evidence layer.

## Scope

Current rows were measured on the Strix Halo host described in
[SYSTEM-METADATA.md](./SYSTEM-METADATA.md) unless a row explicitly says
otherwise. Treat them as local measurements, not universal hardware
guarantees.

The source-style claim index for this bundle is
[headline_claims.csv](./headline_claims.csv).

## Primary Machine

| Component | Measured state |
|---|---|
| System | AMD Ryzen AI Max+ 395 / Radeon 8060S (`gfx1151`) |
| Memory | 128 GB unified LPDDR5X |
| OS | Ubuntu 25.04 (Plucky) |
| Kernel | `6.18.1-061801-generic` |
| Mesa / RADV | Mesa `25.2.8` / RADV |
| ROCm | `7.1.1` baseline; later rows also reference ROCm `7.2.x` runtime libraries |
| BIOS UMA | 4 GB UMA dedicated VRAM |
| IOMMU | Enabled (`amd_iommu=on`) |
| Power profile | Not explicitly recorded |
| Supplemental telemetry | See [THERMAL-TELEMETRY-NIMO.md](./THERMAL-TELEMETRY-NIMO.md) |

## Before Running

Record the host state before every publishable rerun:

```bash
date -Is
uname -a
free -h
cat /proc/cmdline
vulkaninfo --summary | sed -n '/Devices:/,$p' | sed -n '1,40p'
dpkg -l | grep -E 'amdvlk|mesa-vulkan-drivers|linux-firmware|rocm|hip' || true
```

Then run whatever local hygiene check applies to the backend or harness.

## Benchmark Command Shapes

The exact model, backend, and settings are captured row-by-row in
[RAW-BENCHMARK-ROWS.md](./RAW-BENCHMARK-ROWS.md) and summarized in
[manifest.csv](./manifest.csv).

Where the source used a launcher script instead of a one-line shell command,
the launcher path is preserved in the row.

Common shapes in this bundle:

- direct `llama-bench` short-context rows
- `llama-server` rows with `--jinja`, `--reasoning`, or speculative decoding
- MTP rows with `DRAFT_N`, `POLL`, `THREADS`, and `THINKING`
- Lucebox / DFlash rows with `LUCE_TARGET`, `LUCE_DRAFT`, and
  `DFLASH_ENABLE_THINKING`

## Raw Data Map

| Claim family | Structured data | Raw logs | Notes |
|---|---|---|---|
| Claim index | `data/headline_claims.csv` | Row-level evidence summarized in `RAW-BENCHMARK-ROWS.md` | Source-style index for the share bundle |
| Exact rows | `manifest.csv` | `RAW-BENCHMARK-ROWS.md` | Compact bundle map |
| Supplemental telemetry | N/A | `THERMAL-TELEMETRY-NIMO.md` | Separate Nimo fan, temp, and power note |

## Claim Hygiene

Do not copy these claims without matching setup.

Performance depends on exact hardware SKU, RAM configuration, BIOS UMA,
IOMMU, firmware, kernel, Mesa/RADV, ROCm, Vulkan ICD selection, power
profile, GPU clocks, thermal state, backend commit/build flags, model file,
quant type, context length, generated token count, batch size, and
background system load.

If your setup differs, rerun the benchmark scripts and cite the date,
command, CSV, raw output, and backend version with any copied claim.
