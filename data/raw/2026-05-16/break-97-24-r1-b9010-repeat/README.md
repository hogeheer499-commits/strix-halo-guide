# Break 97.24 R1 - b9010 Historical Repeat

Question: can the previous b9010 UD-Q4_K_XL path reproduce or beat the old 97.24 t/s peak on the current host?

## Results

| Run | Host state | pp512 | tg128 | Read |
|-----|------------|------:|------:|------|
| [`guide-r20.csv`](guide-r20.csv) | practical cleanup, but `tuned`/desktop power-profile drift later found | 1368.56 | 92.58 | Did not reproduce the old peak. |
| [`guide-r20-perfstate-v2.csv`](guide-r20-perfstate-v2.csv) | CPU/GPU performance toggles set, but before final strict `tuned`/`power-profiles-daemon` fix | 1334.72 | 93.66 | Still below the old peak. |

Interpretation: R1 did not provide a new headline. The later strict run in [`../break-97-24-strict-noise-settings/`](../break-97-24-strict-noise-settings/) showed that the speed-first Q4_K_S path, not the historical UD path, is the current fastest measured route.
