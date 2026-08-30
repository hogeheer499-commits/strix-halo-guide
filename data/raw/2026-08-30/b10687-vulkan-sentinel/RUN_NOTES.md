# b10687 Vulkan/RADV sentinel — 2026-08-30 (COMPLETE)

Purpose: first llama.cpp numbered-build sentinel on the CURRENT host stack.
NOT comparable as a control against the kernel-6.19.4 headline rows: the host
kernel is now 7.0.0-30-generic, so this run starts a new current-stack lane.

## Stack

- llama.cpp b10687, commit `c841aee`, built locally with `-DGGML_VULKAN=ON`,
  Release, on 2026-08-30. Device line: `Radeon 8060S Graphics (RADV
  STRIX_HALO) (radv) | uma: 1 | fp16: dot2 | warp size: 64 | shared memory:
  65536 | int dot: 0 | matrix cores: KHR_coopmat`.
- Kernel 7.0.0-30-generic (NEW vs the pinned 6.19.4 of all earlier first-party
  rows). Mesa/firmware per host snapshots in this directory.
- Power: `adaptive-power-guard` user service stopped for the runs;
  `powerprofilesctl set performance`. DEVIATION from the 2026-07-16 sentinel
  protocol: amdgpu DPM could NOT be forced to `high` (no sudo in this
  session); DPM stayed on auto. Guard and balanced profile restored after.
- Flag note: `-mmp` is deprecated on b10687; effective `load_mode=auto`
  (avoids mmap on iGPUs upstream since PR #26081). Recorded in the CSVs.

## Background load (recorded, per Background-Load Policy)

- ubuntu-zoom VM (held /dev/dri/renderD128, gl=on): gracefully shut off first.
- ffmpeg virtual-camera feed: stopped. User rustdesk server/tray: killed but
  respawned by the root service (~2% CPU, no GPU); left recorded.
- `scripts.banen.noauth_api` python job (~5-14% CPU, CPU-only): left running.
- Therefore: current-stack SENTINEL evidence, not a strict-clean headline.

## Results (llama-bench -fa 1 -ngl 999 -p 512 -n 128 -r 20 -o csv)

| Model | pp512 avg t/s | tg128 avg t/s | CSV |
|---|---|---|---|
| Qwen3-Coder-30B-A3B-Instruct UD-Q4_K_XL (fresh official unsloth artifact) | 1264.16 ± 22.07 | 94.64 ± 0.40 | qwen3-coder-30b-udq4kxl-b10687-p512-n128-r20.csv |
| Qwen3-Next-80B-A3B-Instruct UD-Q4_K_XL (existing artifact) | 675.76 ± 8.96 | 62.09 ± 0.22 | qwen3-next-80b-udq4kxl-b10687-p512-n128-r20.csv |

Context (older rows, DIFFERENT kernel/stack, not same-condition controls):
b9049 coder UD-Q4_K_XL measured 96.76 tg128 / 1320.52 pp512; b9172
Qwen3-Next measured 59.06 tg128 / 751.70 pp512. Read: the new stack lands in
the same class; decode slightly up on Qwen3-Next, prefill slightly down on
both. Establish same-stack A/Bs before claiming any regression/improvement.

Artifact hashes: ../artifact-sha256.txt
