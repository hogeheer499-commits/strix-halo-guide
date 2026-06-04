# System Metadata

| Field | Value |
|---|---|
| Host | AMD Ryzen AI Max+ 395 / Radeon 8060S (`gfx1151`) |
| OS | Ubuntu 25.04 (Plucky) |
| Kernel | `6.18.1-061801-generic` |
| RAM | 128 GB unified LPDDR5X |
| UMA / VRAM | 4 GB UMA dedicated VRAM |
| IOMMU | Enabled (`amd_iommu=on`) |
| Mesa / RADV | Mesa `25.2.8` / RADV |
| ROCm | `7.1.1` baseline; later runs also reference ROCm `7.2.x` runtime libraries |
| Windows build | N/A |
| AMD driver / Adrenalin | N/A |
| Power profile / performance mode | Not explicitly recorded in the benchmark docs |
| Thermal / fan notes | See [THERMAL-TELEMETRY-NIMO.md](./THERMAL-TELEMETRY-NIMO.md) for supplemental fan/power/temperature data from a separate Nimo AI Mini PC bench |

## Notes

- The Linux baseline and GPU stack above are the environment used for the
  benchmark rows in this bundle.
- Where a row uses a different llama.cpp build or runtime path, it is called
  out in the row itself.
