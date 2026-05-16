# Qwen3-Coder 30B Break-100 Routes - Strict Follow-Up - 2026-05-16

Goal: test whether the Beelink GTR9 Pro can produce a reliable 100 t/s Qwen3-Coder 30B-A3B direct generation result after the 98.51 t/s strict-clean Q4_K_S row.

## Host Handling

- T3 stayed running and healthy throughout the run.
- `tuned accelerator-performance` was active.
- `power-profiles-daemon` was stopped/disabled.
- CPU governors and EPP were set to `performance`.
- GPU was held at the high 2900 MHz state.
- RustDesk, Zoom, Firefox, ffmpeg, and the qemu Zoom VM were temporarily paused for the strict window and restored afterward.
- T3 processes were temporarily reniced lower for one max-push sub-run, without stopping T3, then restored to normal priority.

## Result

No stable 100 t/s path was found.

Best short scout:

| Run | Repeats | Flags | tg128 |
|-----|--------:|-------|------:|
| [`16-t12-cpumask-r5.csv`](16-t12-cpumask-r5.csv) | r5 | `-fa 1 -t 12 --cpu-strict 1 -C 0xffff0000 --poll 50` | 99.11 t/s |

Best longer confirmation:

| Run | Repeats | Flags | pp512 | tg128 |
|-----|--------:|-------|------:|------:|
| [`29-max-t15-poll50-r20.csv`](29-max-t15-poll50-r20.csv) | r20 | `-fa 1 -t 15 --poll 50` | 1382.12 t/s | 98.96 t/s |

## Negative Findings

- `-t 12` and `-t 15` are slightly better than the default `-t 16`, but not enough to cross 100 t/s.
- CPU masks can produce a strong r5 scout, but the masked r10 candidates did not hold up.
- `--poll 75` can look slightly better in r5, but it did not produce a confirmed 100 t/s path.
- `--no-host`, larger batch/ubatch, mmap, direct I/O, KV q8/q4, Flash Attention off, and no-op/no-KV variants did not produce a stable 100 t/s result.
- OS-visible GPU overclock headroom is not available in the current boot: `pp_od_clk_voltage` reports 2900 MHz max and the active high state is already 2900 MHz.

## Interpretation

The measured Beelink is extremely close to the 100 t/s marketing threshold, but the honest current ceiling remains below 100 t/s for this direct llama-bench workload. Keep the public headline at the confirmed 98.51 t/s r50 speed-first row unless a future BIOS/PBO/driver route produces a repeatable r20/r50 result above 100 t/s.

Summary files:

- [`summary-all-break100-scouts.csv`](summary-all-break100-scouts.csv)
- [`top-all-break100-scouts.txt`](top-all-break100-scouts.txt)
