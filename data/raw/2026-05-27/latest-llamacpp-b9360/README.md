# Latest llama.cpp b9360 Spot Check

Measured 2026-05-27 on the Beelink GTR9 Pro with Ryzen AI MAX+ 395, Radeon 8060S, kernel `6.19.4-061904-generic`, Mesa/RADV `26.1.1`, and `tuned accelerator-performance`.

The normal workspace dependency was left running. Non-essential GUI, remote-desktop, media, local model-server, and demo-app noise was paused with `SIGSTOP` during the run and restored afterward.

## Direct llama-bench

| Route | Build | pp512 | tg128 | Read |
|-------|-------|------:|------:|------|
| Qwen3-Coder 30B-A3B Q4_K_S | b9360 `6b4e4bd58` | 1408.59 | 97.23 | Better than the b9334 direct rerun, but still below the b9179 98.51 t/s direct speed-first headline. |
| Qwen3-Coder 30B-A3B UD-Q4_K_XL | b9360 `6b4e4bd58` | 1398.69 | 92.60 | No new balanced headline; below the b9049/b9010 96-97 t/s rows. |

## Qwen3.6 MTP IQ4_XS-Q8nextn llama-server

| Case | Mean t/s | Min | Max | Read |
|------|---------:|----:|----:|------|
| baseline, no MTP | 74.88 | 74.82 | 74.97 | Current no-speculative server baseline. |
| draft-n=2, `-t 16`, `--poll 50`, `-ub 512` | 99.43 | 86.76 | 107.77 | Default-ubatch route is very close to 100 t/s but stayed below it. |
| draft-n=2, `-t 16`, `--poll 100`, `-ub 512` | 99.56 | 86.91 | 108.28 | Same conclusion: strong, but still below broad 100 t/s. |
| draft-n=2, `-t 16`, `--poll 100`, `-ub 1024` | 101.15 | 88.36 | 109.87 | First repeated local broad 100+ t/s MTP server route. |
| draft-n=2, `-t 16`, `--poll 100`, `-ub 1024`, repeat 2 | 101.10 | 88.25 | 109.81 | Repeat confirms the 100+ average. |
| draft-n=2, `-t 16`, `--poll 100`, `-ub 1024`, repeat 3 | 101.06 | 88.27 | 109.78 | Repeat confirms the 100+ average. |
| draft-n=2, `-t 12`, `--poll 100`, `-ub 1024` | 101.16 | 88.29 | 109.71 | Highest single six-prompt average in this sweep, essentially tied with t16. |
| draft-n=2, `-t 20`, `--poll 100`, `-ub 1024` | 100.99 | 88.47 | 109.94 | Still above 100, but not better than t12/t16. |
| draft-n=3, `-t 16`, `--poll 100`, `-ub 1024` | 99.83 | 83.28 | 117.53 | Higher prompt peak, lower broad average than draft-n=2. |

## Interpretation

- Latest b9360 direct `llama-bench` did not beat the existing direct Qwen3-Coder headlines.
- Latest b9360 MTP with `draft-n=2`, `--poll 100`, and `-ub 1024` did cross 100 t/s repeatedly across the six-prompt harness.
- This is an experimental `llama-server` / speculative-decoding result. It is not a replacement for the direct non-speculative `llama-bench` headline.
- The honest public wording is: direct Qwen3-Coder remains 98.51 t/s, while the best local Qwen3.6 MTP server route now reaches about 101.1 t/s across six prompts on b9360.
