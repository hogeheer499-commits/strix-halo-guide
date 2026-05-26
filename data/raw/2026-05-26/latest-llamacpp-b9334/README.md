# Latest llama.cpp b9334 Spot Check

Measured 2026-05-26 on the Beelink GTR9 Pro with Ryzen AI MAX+ 395, Radeon 8060S, kernel `6.19.4-061904-generic`, Mesa/RADV `26.1.1`, and `tuned accelerator-performance`.

The normal workspace dependency was left running. Non-essential GUI, remote-desktop, media, local model-server, and demo-app noise was paused with `SIGSTOP` during the run and restored afterward.

## Direct llama-bench

| Route | Build | pp512 | tg128 | Read |
|-------|-------|------:|------:|------|
| Qwen3-Coder 30B-A3B Q4_K_S | b9334 `192d8ae` | 1401.20 | 96.27 | No new direct headline; slower than the b9179 98.51 t/s strict-clean row. |
| Qwen3-Coder 30B-A3B UD-Q4_K_XL | b9334 `192d8ae` | 1402.17 | 94.15 | No new balanced headline; below the b9049/b9010 96-97 t/s rows. |
| Qwen3-Coder 30B-A3B Q4_K_S control | b9179 `1348f67c5` | 1409.36 | 97.61 | Same host state control; still faster than b9334 direct generation. |

## Qwen3.6 MTP IQ4_XS-Q8nextn llama-server

| Case | Mean t/s | Min | Max | Read |
|------|---------:|----:|----:|------|
| baseline, no MTP | 74.39 | 70.77 | 75.14 | Current no-speculative baseline. |
| draft-n=2, `-t 16`, `--poll 50` | 96.14 | 86.58 | 107.24 | Clear improvement over the older b9235 MTP average. |
| draft-n=3, `-t 16`, `--poll 10` | 98.52 | 82.24 | 116.75 | Best b9334 single-prompt peak. |
| draft-n=3, `-t 16`, `--poll 100` | 98.53 | 82.25 | 116.33 | First high-average run. |
| draft-n=3, `-t 16`, `--poll 100`, repeat | 98.57 | 81.94 | 116.22 | Best local broad MTP average measured so far. |
| draft-n=3, `-t 32`, `--poll 10`, repeat | 97.76 | 82.33 | 116.34 | Useful repeat showing the broad average is still below 100 t/s. |
| draft-n=4, `-t 16`, `--poll 50` | 87.89 | 66.66 | 110.46 | Higher draft depth hurt average stability. |
| synthetic512 ignore-EOS draft-n=3 | 93.93 | 74.78 | 114.88 | Synthetic prompt variant did not improve the broad average. |

`draft-n=5` produced an invalid timing artifact: one prompt emitted only one token/EOS and reported `predicted_ms=0.001`, creating a bogus 1,000,000 t/s row. Do not use it as a benchmark result.

## Interpretation

- Latest b9334 direct `llama-bench` did not beat the existing direct Qwen3-Coder headlines.
- Latest b9334 MTP did materially improve the experimental Qwen3.6 server/speculative route from about 92-93 t/s to about 98.5 t/s across the six-prompt harness.
- This still is not an honest broad 100 t/s average claim. It is a strong experimental MTP result and should stay separate from the direct `llama-bench` headline.
