# Controlled GMKtec EVO-X2 benchmark — llama.cpp v0.3.0 (current build)

Community benchmark report from @mottledMantis (GMKtec EVO-X2). This is the controlled
current-build follow-up to the earlier Gemma 4 / Qwen3-Coder / Qwen3.6 rows, run at the
2:30 AM quiet window to match a clean host state.

## System
- **Device:** GMKtec EVO-X2
- **CPU/GPU:** AMD Ryzen AI MAX+ 395 / Radeon 8060S (gfx1151)
- **RAM:** 96GB LPDDR5X-8000
- **BIOS UMA:** 1GB (minimum)
- **IOMMU:** Disabled
- **OS:** Ubuntu 26.04 LTS
- **Kernel:** 7.0.0-30-generic
- **Mesa:** (RADV STRIX_HALO)
- **Vulkan ICD:** RADV
- **Host state:** idle (scheduled quiet-window run)

## Build & command
- **llama.cpp:** v0.3.0 (commit `c1d0e7a`), Vulkan backend
- **Command (all rows):**
  ```
  llama-bench -m <model> -ngl 999 -fa on -mmp 0 -b 512 -ub 512 -t 16 -p 512 -n 128 -r 20 -o csv
  ```
  Note: v0.3.0 deprecates `-mmp 0` in favor of `--load-mode`; `-mmp 0` still honored (mmap off).

## Results (20 repeats, t/s)

| Model | Quant | File size | pp512 | tg128 (sd) |
|---|---|---|---|---|
| Qwen3-Coder 30B-A3B | Q4_K_S | 17.5 GB | 1257.19 | **99.08** (0.19) |
| Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 17.7 GB | 1290.47 | 96.75 (0.26) |
| Qwen3.6 35B-A3B MTP | IQ4_XS-Q8nextn | 19.4 GB | 1146.41 | **76.20** (0.09) |
| Gemma 4 26B-A4B | UD-Q4_K_M | 16.9 GB | 1181.98 | **54.15** (0.10) |

## Model hashes (SHA256)
- Gemma 4 26B-A4B UD-Q4_K_M: `34c746b1d50ab813e29cd46c4796e3f43c741901a582f93a67b55b9fc9687b35`
- Qwen3-Coder Q4_K_S: `56a7d00783419bcb0ae566253c371bcb3678261bb79881a553539f5679864db4`
- Qwen3-Coder UD-Q4_K_XL: `2841aa314d916434860cfb8990347528dcdfe5c350dbcb9d1461dbee88ff2533`
- Qwen3.6 35B-A3B MTP IQ4_XS: `4d2349305663bc59bacab26d8eba8ed1218de84b8d1f0456208037e13efa9a98`

## Comparison against guide references (Beelink, matched flags)
- **Gemma 4 26B UD-Q4_K_M:** 54.15 t/s on GMKtec v0.3.0 vs Beelink b9851 55.45 / b9859 54.18.
  Within ~1-2%, same practical band, now on a current build with matched `-fa on -mmp 0` shape.
- **Qwen3-Coder Q4_K_S:** 99.08 t/s on GMKtec v0.3.0 vs Beelink b9851 100.99 / b9859 98.48.
  Untuned GMKtec lands within ~2% of the tuned Beelink headline on the current build.
- **Qwen3.6 MTP IQ4_XS:** 76.20 t/s direct llama-bench (no speculative draft; this is the
  plain IQ4_XS decode). This is a fresh MTP-rerun-after-llama.cpp-update data point.

## Notable finding: v0.3.0 MTP on Qwen3.6 is quant-dependent
- Qwen3.6 **IQ4_XS-Q8nextn** loads and runs MTP cleanly on v0.3.0 (the file includes the
  Q8 next-token head; server-mode MTP was verified separately at ~76 t/s).
- Qwen3.6 **Q6_K_XL + Q4_K_XL MTP draft** FAILS to load on v0.3.0 with a reproducible
  `vk::Queue::submit: ErrorDeviceLost` at draft-model load (`radv/amdgpu: Not enough memory
  for command submission`), even with ample system RAM. This reproduces reliably. b9235
  loads the same Q6+draft combination fine. **For Qwen3.6 Q6 users, stay on b9235 (or switch
  to the IQ4_XS quant) — do not upgrade to v0.3.0 without changing quant.**

## Caveats
- GMKtec-only; this is a controlled single-OEM current-build row, not a cross-OEM ranking.
- `-mmp 0` (mmap off) matches the Beelink control shape; `flash_attn=1`, batch 512, threads 16.
- Kernel 7.0.0-30 and Mesa are current for this box; no power/thermal telemetry captured.

## Raw data
Raw llama-bench CSV output is available on request (4 files, one per model, same command shape).
