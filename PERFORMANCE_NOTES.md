# Performance Notes

This file keeps narrow performance conclusions that are useful for repeat testing, but too detailed for the first README screen.

## Direct 98.51 t/s Reproduction Status

The current direct `llama-bench` speed-first headline remains Qwen3-Coder 30B-A3B `Q4_K_S` at **98.51 t/s** on llama.cpp b9179, Vulkan/RADV, measured on 2026-05-16.

That result came from a strict host state:

- Mesa/RADV 26.0.6 from the then-current kisak Mesa stack.
- llama.cpp b9179 `b81c2cdd7`.
- Qwen3-Coder 30B-A3B `Q4_K_S`.
- `-fa 1`, `-mmp 0`, `-b 2048`, `-ub 512`, `-t 16`, `--poll 50`, `-ngl 999`.
- `tuned accelerator-performance` active and `power-profiles-daemon` inactive.
- CPU governors and EPP set to `performance`.
- GPU fixed high with 2900 MHz selected.
- RustDesk, Firefox, Zoom VM, and ffmpeg paused; T3 kept running and guarded.

Raw evidence:

- [`data/raw/2026-05-16/break-97-24-strict-noise-settings/b9179-q4-k-s-r50.csv`](data/raw/2026-05-16/break-97-24-strict-noise-settings/b9179-q4-k-s-r50.csv)
- [`data/raw/2026-05-16/break-97-24-strict-noise-settings/host-state-r50.txt`](data/raw/2026-05-16/break-97-24-strict-noise-settings/host-state-r50.txt)

## 2026-06-01 Reproduction Attempts

A 2026-06-01 rerun first landed around 92-93 t/s because it accidentally used `flash_attn=0`. That is not comparable to the original headline, which used `flash_attn=1`.

After correcting to `flash_attn=1`, the same b9179 Qwen3-Coder `Q4_K_S` path on the current Mesa/RADV 26.1.1 stack measured about **95.1 t/s** with the original flags. The latest `de6f727aa` build measured about **95.6 t/s** on the same path. These were local control runs and did not replace the public headline.

An isolated source-built Mesa 26.0.6 RADV test was also run without system downgrades. `vulkaninfo` confirmed `Mesa 26.0.6 (git-0e095aab43)`, but the best controlled r20 rerun was **96.84 t/s**, not 98.51 t/s.

Interpretation:

- Mesa/RADV version and exact driver stack matter.
- Source-built Mesa 26.0.6 is not identical to the old kisak Mesa 26.0.6 binary stack.
- The 98.51 t/s row remains valid as recorded evidence, but it should be treated as a strict-stack speed-first result, not a casual “always reproduce this” number.
- Do not change the headline unless a newer repeated run beats 98.51 t/s with raw CSV, host state, model hash, and exact command.

## Qwen3.6 27B MTP Q8_0 Status

The official Qwen3.6 27B MTP `Q8_0` GGUF is useful evidence because it answers a natural question: “Should I use the dense 27B route instead of the 35B-A3B MoE route on Strix Halo?”

Current answer: not for speed.

Measured server results:

- llama.cpp b9235, Mesa/RADV 26.0.6: **7.74 t/s** without MTP, **14.59 t/s** best MTP average.
- llama.cpp `de6f727aa`, Mesa/RADV 26.1.1: **7.61 t/s** without MTP, **14.69 t/s** with `draft-n=3`.

Raw evidence:

- [`data/raw/2026-05-19/qwen36-27b-mtp-q8-llamacpp-9235/`](data/raw/2026-05-19/qwen36-27b-mtp-q8-llamacpp-9235/)
- [`data/raw/2026-06-01/qwen36-27b-mtp-latest-de6f727/`](data/raw/2026-06-01/qwen36-27b-mtp-latest-de6f727/)

Interpretation:

- MTP nearly doubles the dense 27B Q8 route, but the route remains much slower than the 35B-A3B MoE paths.
- For a practical Strix Halo local-AI setup, Qwen3.6 35B-A3B GGUFs remain the better Qwen3.6 speed path in this guide.
- Keep the 27B result as a negative/control row, not as a headline.
