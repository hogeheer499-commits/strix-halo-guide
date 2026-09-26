# Strict-clean headline re-check on llama.cpp b11146 (2026-09-26)

**Question:** do the direct Vulkan/RADV `llama-bench` headline rows still hold on
the current official llama.cpp release v0.5.0 (build b11146, commit `7fe450e19`),
and how do they compare with the original builds measured the same night under
the same host conditions?

This bundle is **direct `llama-bench` evidence only**. It contains no
server/API, MTP/speculative, concurrency or Ollama results, and it does not
change any published headline number.

## Stack

- Beelink GTR9 Pro, Ryzen AI MAX+ 395, Radeon 8060S (RADV STRIX_HALO).
- Kernel `7.0.0-31-generic`; Mesa/RADV `26.2.3` (kisak PPA);
  linux-firmware `20240318.git3b128b60.0ubuntu3.1`. Both differ from the
  May headline lane (kernel 6.19.4, Mesa 26.0.6) and from the August 30 lane
  (kernel 7.0.0-30, Mesa 26.1.7).
- Tested runtime: official prebuilt release asset
  `llama-b11146-bin-ubuntu-vulkan-x64.tar.gz`
  (SHA-256 `d3ce40fce7403cc93bcf5718fc46c6efb61ed9709f8e5d9f10c86bf0e30e8fb3`,
  verified against the GitHub release digest), reports
  `version: 0.5.0-dev (build 11146, commit 7fe450e19)`, built with GNU 11.4.0.
  Device line: `fp16: dot2 | int dot: 1 | matrix cores: KHR_coopmat`.
- Same-night controls on the original builds (locally built, already on the host):
  b10687 `c841aee`, b9172 `1348f67c5`, b9049 `2496f9c14`. Old builds report
  `int dot: 0`; b9049/b9172 report `fp16: 1`.
- Model artifacts: SHA-256 in `artifact-sha256.txt`. Qwen3-Coder UD-Q4_K_XL,
  Qwen3-Next UD-Q4_K_XL and all three Qwen3.8-Flash-Next shards match the hashes
  recorded on 2026-08-30. The gpt-oss-120b shards are the files used on
  2026-05-07 (unchanged since download; no earlier hash was recorded). The
  Qwen3-Coder UD-Q4_K_XL file was refreshed before 2026-08-30, so the original
  2026-05-07 row may have used an older upload; the same-night b9049 control uses
  the current file.

## Host conditions (Background-Load Policy)

Paused for the whole run (04:07-04:39 local time):

- the libvirt desktop VM (`virsh suspend`; it still held about 7GB of RAM while
  paused, but no CPU or GPU work). Resumed at 04:38:59 by an exit trap; state
  after the run: `running` (`vm-state-after.txt`).
- Ollama: no model was loaded before or during the run (`ollama ps` empty).

Power: `powerprofilesctl` `performance` during all runs, applied through the
workstation's own power guard with a temporary boost and cleared afterwards
(profile back to `balanced`). AMDGPU DPM stayed `auto` (not forced `high`).
This matches the August 30 lane, not the May `tuned accelerator-performance` lane.

Remained active (not stopped, by design): the desktop session (gnome-shell,
Xorg), the Zoom desktop client, Chrome, the RustDesk remote-access agent,
terminal and CLI-agent sessions, and the power guard. Processes holding the GPU
render node are listed by runtime name in the host snapshots; none showed
sustained GPU load (`gpu_busy_percent` 0 before and after). Therefore this is a
**controlled strict-clean attempt within the approved scope**, not a fully idle
host.

The Qwen3.8-Flash-Next pair ran last behind a memory gate (MemAvailable
104.7GB at start). It completed, but pushed the 7GB swap to full; the other
rows were unaffected (they ran first).

Order: each model ran b11146 first, then the original build, 10 s apart, in one
session without reboot. Pair order was not alternated.

## Results

Mean t/s ± llama-bench stddev. "Original" is the published headline value and date.

| Headline row id | Model / quant | Build (this run) | Flags | Repeats | Original pp512 / tg128 | This run pp512 | This run tg128 |
| --- | --- | --- | --- | ---: | --- | ---: | ---: |
| qwen3-coder-30b-b10687-sentinel | Qwen3-Coder 30B-A3B UD-Q4_K_XL | b11146 | `-fa 1 -ngl 999 -p 512 -n 128` (load mode auto) | 20 | 1264.16 / 94.64 (2026-08-30, b10687) | 1437.52 ± 11.26 | 96.33 ± 0.23 |
| (same-night control) | same | b10687 `c841aee` | same | 20 | | 1275.67 ± 11.02 | 99.39 ± 0.22 |
| qwen3-coder-30b-llama-bench | Qwen3-Coder 30B-A3B UD-Q4_K_XL | b11146 | `-fa 1 -ngl 999 -b 2048 -ub 512 -lm none` | 20 | 1320.52 / 96.76 (2026-05-07, b9049) | 1418.26 ± 16.68 | 96.30 ± 0.17 |
| (same-night control) | same | b9049 `2496f9c14` | `-fa 1 -ngl 999 -b 2048 -ub 512 -mmp 0` | 20 | | 1243.38 ± 9.58 | 96.83 ± 0.31 |
| qwen3-next-80b-b10687-sentinel | Qwen3-Next 80B-A3B UD-Q4_K_XL | b11146 | `-fa 1 -ngl 999 -p 512 -n 128` (load mode auto) | 20 | 675.76 / 62.09 (2026-08-30, b10687) | 865.62 ± 9.80 | 62.88 ± 0.08 |
| (same-night control) | same | b10687 `c841aee` | same | 20 | | 677.88 ± 10.11 | 64.31 ± 0.17 |
| qwen3-next-80b-llama-bench | Qwen3-Next 80B-A3B UD-Q4_K_XL | b11146 | `-fa 1 -ngl 999 -b 2048 -ub 1024 -lm none`, pp and tg as separate runs | 20 | 751.70 / 59.06 (2026-05-16, b9172) | 866.86 ± 9.57 | 63.58 ± 0.20 |
| (same-night control) | same | b9172 `1348f67c5` | same with `-mmp 0` | 20 | | 696.83 ± 19.19 | 60.76 ± 0.10 |
| gpt-oss-120b-llama-bench | gpt-oss-120b MXFP4 (3-shard GGUF) | b11146 | `-fa 1 -ngl 999 -b 2048 -ub 512 -lm none`; pp512 r3, tg128 r20 as separate runs | 3 / 20 | 726.99 / 55.57 (2026-05-07, b9049) | 772.03 ± 4.65 | 56.14 ± 0.16 |
| (same-night control) | same | b9049 `2496f9c14` | same with `-mmp 0` | 3 / 20 | | 651.98 ± 7.18 | 55.54 ± 0.10 |
| gpt-oss-120b-llama-bench (pp65536) | gpt-oss-120b MXFP4 | b11146 | same, `-p 65536 -n 0` | 1 | 293.73 pp65536 (2026-05-07, b9049) | 289.95 pp65536 | n/a |
| qwen38-flash-next-b10687-scout | Qwen3.8-Flash-Next UD-IQ4_XS (3 shards, ~93.7GB) | b11146 | `-fa 1 -ngl 999 -p 512 -n 128` (load mode auto) | 10 | 394.73 / 27.16 (2026-08-30, b10687) | 508.29 ± 5.22 | 28.61 ± 0.03 |
| (same-night control) | same | b10687 `c841aee` | same | 10 | | 396.56 ± 3.59 | 27.83 ± 0.08 |

No pp65536 control was run on b9049 (it takes about 8 minutes per run; kept the
VM pause short).

## Read

- **Prefill (pp512):** b11146 is faster than the same-night original build on
  every re-checked model: Qwen3-Coder +12.7% vs b10687 and +14.1% vs b9049;
  Qwen3-Next +27.7% vs b10687 and +24.4% vs b9172; gpt-oss-120b +18.4% vs
  b9049; Qwen3.8-Flash-Next +28.2% vs b10687.
- **Decode (tg128):** mixed and small. b11146 is slower than the same-night
  b10687 control on Qwen3-Coder (-3.1%) and Qwen3-Next (-2.2%), close to
  b9049 on Qwen3-Coder (-0.5%) and gpt-oss-120b (+1.1%), faster than b9172 on
  Qwen3-Next (+4.6%) and faster than b10687 on Qwen3.8-Flash-Next (+2.8%).
- The same-night controls land within 0-5% of their original decode values
  (b10687 decode is 2.5-5.0% above its August values). The b10687 prefill
  controls reproduce August within 1%, but the May prefill values do not
  reproduce: b9049 Qwen3-Coder pp512 (1243.38 vs 1320.52), b9172 Qwen3-Next
  pp512 (696.83 vs 751.70) and b9049 gpt-oss pp512 (651.98 vs 726.99) are
  lower tonight. Kernel, Mesa, power
  policy and possibly the Qwen3-Coder artifact differ from May, so compare
  b11146 with the same-night control, not with the May value.
- The fastest historical Qwen3-Coder decode on UD-Q4_K_XL tonight is still
  the old b10687 build (99.39), not b11146.

## Not re-run (headline direct rows)

| Row id | Reason |
| --- | --- |
| deepseek-v4-flash-284b-direct-capacity | Artifact no longer on the host; ~91GB download exceeds the 25GB limit. |
| nemotron-3-super-120b-direct-capacity | Artifact no longer on the host; ~64GB download exceeds the limit. |
| qwen3-coder-30b-q4ks-b9851-direct-101 | Q4_K_S artifact no longer on the host (~17.5GB); not downloaded in this pass. |
| qwen3-coder-30b-q4ks-speed-first | Same missing Q4_K_S artifact. |
| qwen3-30b-a3b-2507-iq4xs-direct-100 | IQ4_XS artifact no longer on the host (~13.9GB); not downloaded in this pass. |
| lfm25-8b-a1b-small-moe-speed | Artifact no longer on the host (~5.1GB); not downloaded in this pass. |
| qwen36-35b-llama-bench | Qwen3.6 35B-A3B UD-Q4_K_M artifact no longer on the host (~22.1GB); not downloaded in this pass. |
| qwen36-35b-q4-0-speed-first | Qwen3.6 35B-A3B Q4_0 artifact no longer on the host (~19.7GB); not downloaded in this pass. |
| hip-vulkan-workload-split | HIP/Vulkan pp16384 matrix needs a HIP build and the missing Qwen3.6 Q4_0 artifact; out of scope for a Vulkan-only direct re-check. |

## Files

- `run-strict-clean.sh`: the exact harness (VM pause/resume trap, snapshots, commands).
- `*.command.txt`, `*.csv`, `*.stderr.log`: per-run command, llama-bench CSV and stderr.
- `host-snapshot-{pre-cleanup,before,end-of-runs,after}.txt`: kernel, power, DPM,
  Mesa, memory, `ollama ps`, VM state, GPU render-node holders (runtime names only)
  and a `top` sample.
- `run-order.log`, `vm-state-after.txt`, `artifact-sha256.txt`.

Home paths are written as `~`; hostnames, LAN addresses and process command lines
are not recorded.
