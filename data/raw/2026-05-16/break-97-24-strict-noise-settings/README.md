# Qwen3-Coder Break 97.24 Strict Noise/Settings Run - 2026-05-16

Goal: verify whether the Beelink GTR9 Pro can beat the previous 97.24 t/s Qwen3-Coder decode peak after fixing host-state drift and pausing benchmark noise.

## Host State

Captured in [`host-state.txt`](host-state.txt) and [`host-state-r50.txt`](host-state-r50.txt):

- `tuned` active with `accelerator-performance`.
- `power-profiles-daemon` disabled/inactive to avoid stopping `tuned`.
- CPU governors and EPP set to `performance`.
- GPU forced to high performance, 2900 MHz selected.
- T3 health guard active.
- Firefox, Zoom, ffmpeg, and user RustDesk processes were temporarily paused and restored after each run.

## Results

| Run | Build | Model / Quant | Repeats | pp512 | tg128 | Notes |
|-----|-------|---------------|---------|------:|------:|-------|
| [`b9010-ud-q4-k-xl-r20.csv`](b9010-ud-q4-k-xl-r20.csv) | b9010 `d05fe1d7d` | Qwen3-Coder 30B-A3B UD-Q4_K_XL | r20 | 1356.47 | 96.15 | Balanced historical route did not beat the old 97.24 t/s peak. |
| [`b9179-q4-k-s-r20.csv`](b9179-q4-k-s-r20.csv) | b9179 `b81c2cdd7` | Qwen3-Coder 30B-A3B Q4_K_S | r20 | 1380.81 | 98.21 | First strict-clean result above 97.24 t/s. |
| [`b9179-q4-k-s-r50.csv`](b9179-q4-k-s-r50.csv) | b9179 `b81c2cdd7` | Qwen3-Coder 30B-A3B Q4_K_S | r50 | 1396.11 | 98.51 | Confirmed new speed-first row; not a default balanced-quality recommendation. |

## Interpretation

The previous b9179 Q4_K_S r20 run measured 97.22 t/s under a less strict host state. After fixing the `tuned` versus `power-profiles-daemon` conflict and pausing RustDesk/Firefox/Zoom/ffmpeg noise, the same speed-first quant confirmed at 98.51 t/s r50.

This is a new measured speed-first peak, not a 100 t/s result and not a claim that Q4_K_S is the best quality/default quant.
