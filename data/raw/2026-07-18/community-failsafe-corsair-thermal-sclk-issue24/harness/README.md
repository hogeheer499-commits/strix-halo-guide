# Harness snapshot

- `strix-sclk-cap.service` is the exact rendered production oneshot unit.
- `strix-sclk-cap.timer` is the exact rendered 60-second production reapply
  timer.
- `strix-sclk-cap` is behavior-equivalent to the rendered production script;
  only its diagnostic/logger tag was normalized for this public bundle.

Public-safe snapshots of the complete campaign harness are included in
[`source`](source/):

- [`llama-bench-box`](source/llama-bench-box)
- [`strix-bench-lib.sh`](source/strix-bench-lib.sh)
- [`strix-collect-metadata.sh`](source/strix-collect-metadata.sh)
- [`strix-soak.sh`](source/strix-soak.sh)
- [`strix-sclk-bench.sh`](source/strix-sclk-bench.sh)
- [`strix-bench-control`](strix-bench-control)

The public metadata-collector snapshot omits two site-specific service-name
probes. Those fields are not used by the analyzer; zero running containers and
zero model processes remain explicit validation requirements.

The privileged helper intentionally exposes only bounded benchmark operations:
check, timer stop/start, set a validated 100–3000 MHz range, reset to stock, and
restore a captured range plus `manual`/`auto` mode.
