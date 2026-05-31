# 2026-05-31 Direct Qwen3-Coder Safe-Clean Scout Runs

Goal: check whether a newer or known-good llama.cpp Vulkan/RADV build can beat
the existing direct Qwen3-Coder 30B-A3B Q4_K_S 98.51 t/s headline while keeping
T3 running.

Host state:

- T3 stayed running and was checked before/after the runs.
- RustDesk, ffmpeg, browsers, Ollama, the Zoom VM, and local web servers were
  SIGSTOP-paused using the safe-clean manifest.
- Desktop/session/audio/T3 processes were not paused.
- `tuned` was active with `accelerator-performance`.
- CPU governors were `performance`.
- Radeon 8060S was on high performance with 2900 MHz sclk and 1000 MHz mclk.

Model:

- `/home/hoge-heer/benchmark-models/qwen3-coder-break100/Qwen3-Coder-30B-A3B-Instruct-Q4_K_S.gguf`

Results:

| Run | Commit / build | Command shape | pp512 | tg128 | Read |
|-----|----------------|---------------|------:|------:|------|
| [`latest-llamacpp-b9442-safe-clean/qwen3-coder-q4-k-s-r10.csv`](latest-llamacpp-b9442-safe-clean/qwen3-coder-q4-k-s-r10.csv) | `d4c8e2c29`, b9442 line | `-t 16 --poll 50 -r 10` | 1376.37 | 93.85 | Latest upstream did not beat the existing headline. |
| [`b9360-control-safe-clean/qwen3-coder-q4-k-s-r10.csv`](b9360-control-safe-clean/qwen3-coder-q4-k-s-r10.csv) | `6b4e4bd58`, b9360 | `-t 16 --poll 50 -r 10` | 1384.21 | 95.35 | Same host state also stayed below the previous b9360 97.23 r20 row. |
| [`b9187-control-safe-clean/qwen3-coder-q4-k-s-t15-r10.csv`](b9187-control-safe-clean/qwen3-coder-q4-k-s-t15-r10.csv) | `0253fb21f`, b9187 | `-t 15 --poll 50 -r 10` | 1388.21 | 95.09 | Older near-99 scout route did not reproduce a higher result today. |

Conclusion:

These are useful negative/control runs, not public headline updates. The current
direct headline remains the older strict-clean b9179 Q4_K_S r50 row at 98.51 t/s.
Today's safe-clean state stayed around 94-95 t/s, so no README benchmark claim
should be changed from these runs.
