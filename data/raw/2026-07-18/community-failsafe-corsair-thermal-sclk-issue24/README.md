# Strix Halo strict capped-clock and stock thermal campaign — 2026-07-18

This bundle contains a controlled three-system comparison of 2200, 2400, 2500,
and 2600 MHz iGPU SCLK ceilings, followed by staged stock controls, on Corsair
AI Workstation 300 systems. It is a follow-up evidence set for
[strix-halo-guide issue #24](https://github.com/hogeheer499-commits/strix-halo-guide/issues/24).

The result supports 2400 MHz as a conservative performance/thermal compromise
for this specific three-system fleet. No stock-mode lockup was reproduced in a
five-minute gate and a 30-minute measured-load run on each system. Stock mode
nevertheless produced a 93 °C transient on one system, versus an 84 °C worst
case at the 2600 MHz cap. These data do **not** establish that every Corsair,
AXB35, or Strix Halo system needs a clock cap, or that the originally reported
failure can no longer occur.

## What makes this run strict

- All three systems ran each capped test concurrently with the same cap and
  workload; the higher-risk stock controls were run sequentially.
- Every manifest records `background_condition=zero-running-containers`, zero
  running background containers, and zero background model processes.
- The preliminary runs made before all idle containers were stopped are omitted.
- The model shards, container digest, benchmark version, arguments, fan curves,
  firmware, kernel, relevant kernel command line, and EC driver commit are
  recorded.
- SCLK was set through the same privileged control path on every system. The
  60-second production reapply timer was paused during each benchmark.
- Each soak counted 1800 seconds only after GPU power first reached 40 W. Raw
  edge-temperature, socket-power, and SCLK telemetry was sampled every two
  seconds.
- A 98 °C edge-temperature abort was armed for every capped run. The staged
  stock controls used a stricter 95 °C abort. No retained run reached its abort
  threshold.
- The harness captured the pre-test OD floor, ceiling, and performance level and
  restored that exact state on exit. The explicit stock path resets and
  recommits the OD table before returning the performance level to `auto`.
- The benchmark container used the fixed name `strix-bench`, `--replace`, and an
  explicit forced reap path so an orphaned duplicate model load could not remain.
- Stock testing was deliberately sequential: a five-minute gate on each system,
  then one 30-minute-under-load run per system. `stock` reset the OD table and
  selected `auto`, exposing the factory 2900 MHz ceiling. It did not force the
  SCLK floor and ceiling to 2900 MHz.

## Platform and software

The three systems reported the same relevant platform data:

| Item | Value |
|---|---|
| Product | Corsair AI Workstation 300 |
| Processor / GPU | AMD Ryzen AI Max+ 395 / Strix Halo Radeon graphics |
| Memory | 128 GB LPDDR5 |
| SMBIOS baseboard version | `Version 1.0` |
| Physical PCB revision | Not exposed by BIOS/SMBIOS; unknown |
| BIOS | `AXB35-02 3.07`, dated 2025-10-16 |
| EC firmware | `3.07` |
| EC driver checkout | node-a: `c0af008941ccf4be513901aca8ca2a93bf2f3438`; node-b/node-c: `e483ec93deab514c66d3e5c9eeed98b6c17887b4` |
| OS | Fedora Linux 44 Server |
| Kernel | `7.0.14-201.fc44.x86_64` |
| Mesa Vulkan | `26.1.3-1.fc44` |
| AMD GPU firmware | `20260622-1.fc44` |
| Container runtime | Podman 5.8.4 |
| Container image | `docker.io/kyuz0/amd-strix-halo-toolboxes@sha256:646283d9607d7d678b500c85e3bb397742a20ec75a9bbf536ce0418d27b6a11f` |
| llama.cpp | build 10064, commit `86d86ed43` |
| EC power/fans | performance mode; identical three-fan curves recorded in every `metadata.txt` |

`Version 1.0` is only an SMBIOS string. Because neither the BIOS UI nor SMBIOS
exposes a physical board marking, this bundle deliberately records the physical
PCB revision as `not-exposed` rather than treating that generic string as a
verified motherboard revision.

The workload was MiMo-V2.5 UD-IQ2_M, three GGUF shards (about 96.6 GB). The shard
hashes are in [`MODEL-SHA256SUMS`](MODEL-SHA256SUMS). They were verified identical
on all three systems before the campaign.

Relevant benchmark arguments were:

```text
-fa on -mmp 0 -ctk q8_0 -ctv q8_0 -b 4096 -ub 256 -ngl 99
```

The throughput sweep used 512 prompt tokens, 128 generated tokens, and 10
repetitions per cap. The soaks repeatedly used 512 prompt and 512 generated
tokens for 30 minutes under measured load. Stock controls used the same soak
workload and load-detection rule.

## Three-system aggregate

| Cap | Prompt tok/s | Generation tok/s | Soak avg W | Worst soak edge °C | Prompt vs 2200 | Generation vs 2200 |
|---:|---:|---:|---:|---:|---:|---:|
| 2200 | 116.73 | 29.84 | 80.90 | 71 | baseline | baseline |
| 2400 | 125.42 | 30.12 | 97.54 | 75 | +7.44% | +0.97% |
| 2500 | 129.53 | 30.25 | 107.43 | 78 | +10.96% | +1.39% |
| 2600 | 133.44 | 30.39 | 118.71 | 84 | +14.31% | +1.85% |

From 2400 to 2600 MHz, mean prompt throughput increased 6.39% and mean
generation throughput increased 0.87%, while mean sustained power increased
21.70% and the worst observed soak temperature increased from 75 to 84 °C.

All 12 capped soaks completed. Each contains 897–899 loaded samples and
1808–1811 seconds of measured load. The largest positive late-run temperature
slope was only +0.85 °C per 10 minutes; the other eleven late slopes were flat or
negative. Three automated `still-creeping` labels were triggered by the coarse
first-third versus last-third delta rule, but their late fitted slopes were
strongly negative. The raw trajectories therefore do not show continuing
thermal runaway within these capped 30-minute runs.

At 2600 MHz, node-a averaged 2564 MHz during its soak while node-b and node-c
averaged 2600 MHz. That makes 2600 less consistently delivered across the three
otherwise matched systems and reinforces the diminishing-return result.

## Staged stock controls

The stock path reset the OD table and returned the GPU to `auto`. Telemetry
confirmed a 2900 MHz OD ceiling and `auto` performance level in every loaded
sample. This is the normal stock configuration: 2900 MHz was available as a
ceiling, not forced as a constant clock.

All three five-minute gates completed before the longer tests. Their worst edge
temperatures were 87 °C on node-a, 85 °C on node-b, and 74 °C on node-c. The
30-minute results were:

| Node | Avg SCLK | Avg W | Max W | Max edge °C | Final edge °C | Late °C/10m | Result |
|---|---:|---:|---:|---:|---:|---:|---|
| node-a | 2588.7 | 119.55 | 139.06 | 80 | 72 | -6.20 | completed |
| node-b | 2601.0 | 119.50 | 139.08 | 93 | 79 | -0.51 | completed |
| node-c | 2620.9 | 119.57 | 139.04 | 74 | 72 | +1.05 | completed |

Across the three long stock runs, mean sustained SCLK was 2603.5 MHz and mean
sustained socket power was 119.54 W. Thus, this current stock configuration did
not sustain 2900 MHz under load; it dynamically settled near 2.6 GHz. No hard
lock or thermal abort occurred. Node-b's 93 °C raw transient was only 2 °C below
the safety cutoff, however, so this is not evidence that an unrestricted stock
configuration is categorically safe.

The 2600 MHz cap and stock mode had nearly identical mean sustained power
(118.71 versus 119.54 W), but their worst observed temperatures differed: 84 °C
at the cap and 93 °C at stock. Stock also reached about 139 W transient power,
versus 127 W or less in the 2600 MHz soaks. The cap's practical benefit in this
campaign was therefore chiefly reduced transient and worst-case thermal
exposure, rather than a large reduction in long-run mean power relative to the
GPU's present stock behavior.

## Interpretation

- **2400 MHz is the balanced operating point for this fleet.** It retained the
  full measured generation rate within about 1% of the higher caps, improved
  prompt throughput 7.44% over 2200, and held all three systems to 75 °C or less
  in the strict soak.
- **2200 MHz is the conservative efficiency option.** It reduced mean sustained
  power by about 17% relative to 2400 at the cost of 7% prompt throughput, while
  generation changed by less than 1%.
- **2500 and 2600 MHz mainly buy prompt throughput.** Generation was nearly flat,
  while power and temperature climbed more quickly than throughput.
- **The original stock-clock lockup did not reproduce in this bounded test.**
  Zero of three systems locked during one five-minute gate and one 30-minute
  stock run each. That is evidence about these runs, not proof that the earlier
  failure is fixed or impossible.
- **Stock was tested as stock, not as forced 2900 MHz.** The factory ceiling was
  2900 MHz, while the loaded clock averaged about 2604 MHz across the three long
  runs. Forcing both OD bounds to 2900 MHz would be a different and materially
  riskier experiment.

## Known limitations

- Ambient room temperature was not instrumented and is therefore `unknown`.
- The systems were not opened for this campaign, so cooler seating and TIM state
  are `stock-unverified`.
- `edge` temperature and socket power are the Linux amdgpu hwmon readings used by
  the harness; they are not external thermocouple or wall-power measurements.
- The three systems are a matched fleet, not independent validation on another
  owner's hardware or another known PCB revision.
- The checked-out EC repository commit differed: node-a reported `c0af0089`,
  while node-b and node-c reported `e483ec93`. Each value remained unchanged
  throughout the campaign. The upstream diff between these revisions changes
  only `scripts/su_axb35_monitor`; no kernel-module source file differs. The
  exposed power mode and fan settings also matched. This is retained as metadata
  provenance, not treated as a driver-behavior difference.
- Physical PCB revision is not exposed. BIOS/EC versions are exact; the generic
  SMBIOS baseboard-version string is preserved but not overinterpreted.
- The stock launch omitted the explicit EC firmware variable, so those six raw
  metadata files record `ec_firmware_version=unknown`. The capped runs before
  them record `3.07`; there was no intervening reboot or firmware change, and
  all six stock runs report the same loaded EC driver-module hash. The analyzer
  permits this exception only for the stock paths and does not rewrite the raw
  records.

## Firmware-update hypothesis

The originally reported behavior could plausibly depend on the combined kernel,
firmware, Mesa, runtime, or workload state. The installed firmware package in
this campaign was `amd-gpu-firmware-20260622-1.fc44`. Upstream comparison shows
that the 2026-03-09 to 2026-05-19 firmware interval changed Strix-relevant
`gc_11_5_1` graphics blobs and `smu_14_0_3_kicker.bin`, so a firmware interaction
is technically possible. The subsequent 2026-05-19 to 2026-06-22 release did
not change those candidate blobs, however. The present safer behavior therefore
cannot be attributed specifically to a June replacement of those files.

This campaign was not a controlled firmware bisect, and its result should not be
used to identify `linux-firmware` as the cause. The kernel also changed from the
earlier report, and eliminating duplicate/orphaned workload state is another
material difference. A firmware-only A/B test with all other software and the
workload fixed would be required for a causal claim. Upstream release tags are
available from the
[official linux-firmware repository](https://kernel.googlesource.com/pub/scm/linux/kernel/git/firmware/linux-firmware/),
and Fedora records the installed package lineage in its
[amd-gpu-firmware package history](https://packages.fedoraproject.org/pkgs/linux-firmware/amd-gpu-firmware/fedora-44-updates.html).

## Bundle layout and validation

Each `node-a`, `node-b`, and `node-c` directory contains one strict sweep, four
capped strict soaks, one five-minute stock gate, and one 30-minute stock soak.
Every test directory includes raw telemetry, raw benchmark output, run
configuration, metadata, summary, and a relative-path `SHA256SUMS` manifest.
The [`harness`](harness/) directory preserves the exact rendered production cap
unit and timer plus a behavior-equivalent public snapshot of the cap script used
for the campaign. It also contains public-safe source snapshots of the complete
benchmark, cleanup, metadata, and privileged-control paths.

Run the independent summary checker from this directory:

```bash
python3 analyze.py
```

It recomputes the soak metrics from raw telemetry, rejects incomplete runs or
non-zero background workload, checks the recorded summaries within their output
precision, verifies that loaded stock samples used a 2900 MHz ceiling in `auto`,
and prints the per-node and aggregate tables.

To validate all artifact manifests on a system with `shasum`:

```bash
find node-* -name SHA256SUMS -execdir shasum -a 256 -c SHA256SUMS \;
```

No BIOS photographs are included. Public node labels are intentionally limited
to `node-a`, `node-b`, and `node-c`.
