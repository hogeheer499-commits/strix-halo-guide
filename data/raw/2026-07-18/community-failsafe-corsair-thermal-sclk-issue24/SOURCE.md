# Source And Import Note

This directory preserves Fail-Safe's public-safe strict three-system Corsair AI
Workstation 300 thermal/SCLK evidence bundle from
[issue #24](https://github.com/hogeheer499-commits/strix-halo-guide/issues/24#issuecomment-5014049000).

- Original attachment:
  [`strix-halo-thermal-20260718.zip`](https://github.com/user-attachments/files/30160457/strix-halo-thermal-20260718.zip)
- Contributor-provided ZIP SHA-256:
  `8f47a0aae08c8873b3005e1ef0b00fe296794a3d3e32cb9068bd7b7624038273`
- Local import verified the same ZIP SHA-256 before extraction.
- Imported on: `2026-07-21`.
- Imported contents: contributor README, analyzer, public-safe harness, metadata,
  manifests, summaries, raw benchmark output, and raw telemetry.
- Deliberately omitted: generated Python `__pycache__` / `.pyc` files.

The contributor's later summary graph is preserved as
[`contributor-graph.svg`](contributor-graph.svg), sourced from
[this follow-up comment](https://github.com/hogeheer499-commits/strix-halo-guide/issues/24#issuecomment-5015746028).
Its local SHA-256 is
`c2f48f297f16140308264089ff7cd0e9dcd63c1a9268e8f459f4089a0afc052c`.

Run the contributor's independent checker from this directory:

```bash
python3 analyze.py
```

The guide's compact normalized rows are in
[`data/community_thermal_sclk.csv`](../../../community_thermal_sclk.csv). The
raw bundle remains the source of truth.

## Claim Boundary

This is community-reported evidence from three matched systems in one managed
Corsair/Sixunited fleet. It is not a first-party Beelink result, external
wall-power evidence, cross-OEM validation, or proof that every Corsair or Strix
Halo system needs an SCLK cap.

The original hard lock did not reproduce in the bounded stock controls. The
root cause remains unresolved. Historical journals show that a kernel-specific
`ec_su_axb35` module had temporarily been unavailable, which caused custom
fan-control services to fail and is therefore an important confounder and
possible major contributor.
