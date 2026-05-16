# Break 97.24 R2 - Qwen3-Coder Speed-Quant Scouts

Question: do Qwen3-Coder Q4_K_S or Q4_0 speed quants beat the old 97.24 t/s peak across b9010, b9049, and b9179?

These are short r5 scout runs. They were used to choose the strict r20/r50 confirmation path, not as final headline evidence.

## Results

| Build | Quant | pp512 | tg128 | Raw |
|-------|-------|------:|------:|-----|
| b9010 | Q4_K_S | 1374.62 | 95.87 | [`r5/b9010-q4ks.csv`](r5/b9010-q4ks.csv) |
| b9049 | Q4_K_S | 1190.14 | 94.95 | [`r5/b9049-q4ks.csv`](r5/b9049-q4ks.csv) |
| b9179 | Q4_K_S | 1360.90 | 95.73 | [`r5/b9179-q4ks.csv`](r5/b9179-q4ks.csv) |
| b9010 | Q4_0 | 1379.28 | 94.27 | [`r5/b9010-q40.csv`](r5/b9010-q40.csv) |
| b9049 | Q4_0 | 1300.78 | 94.95 | [`r5/b9049-q40.csv`](r5/b9049-q40.csv) |
| b9179 | Q4_0 | 1304.78 | 94.52 | [`r5/b9179-q40.csv`](r5/b9179-q40.csv) |

Interpretation: the first scout pass did not beat 97.24 t/s. The later strict host-state fix showed the main issue was benchmark state/noise, not the quant list itself.
