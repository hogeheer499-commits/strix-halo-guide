# High-Power Policy Follow-Up

Local Beelink GTR9 Pro follow-up after a community GMKtec EVO-X2 result reported
that forcing GPU DPM to `high` and CPU EPP to `performance` can sometimes improve
Strix Halo decode throughput.

This is a short policy-delta check, not a new headline benchmark. T3 stayed active.
Firefox, RustDesk, Ollama, a Zoom VM, ffmpeg/docflock, and local dev servers were
temporarily paused for the clean comparison and resumed afterward.

Model:

```text
/home/hoge-heer/benchmark-models/qwen3-coder-break100/Qwen3-Coder-30B-A3B-Instruct-Q4_K_S.gguf
```

Build:

```text
/home/hoge-heer/llama-cpp-upstream-2026-06-02-1fd5f4803/build-vulkan/bin/llama-bench
```

Command shape:

```text
llama-bench -m Qwen3-Coder-30B-A3B-Instruct-Q4_K_S.gguf -fa 1 -ngl 999 -mmp 0 -b 2048 -ub 512 -p 512 -n 128 -r 5
```

Clean comparison:

| Policy | SCLK state before run | pp512 | tg128 |
| --- | ---: | ---: | ---: |
| GPU `auto`, CPU EPP still reported `performance` | 1070 MHz selected, 2900 MHz available | 1216.82 +/- 68.76 t/s | 95.18 +/- 1.42 t/s |
| GPU `high`, CPU EPP `performance` | 2899-2900 MHz selected | 1390.03 +/- 7.91 t/s | 96.37 +/- 0.29 t/s |

Interpretation:

- The policy helped this short local run, especially prompt processing stability.
- It did not reproduce the external 100 t/s GMKtec result on this Beelink.
- The external result also included thermal rework: repaste plus better stock thermal-pad seating, reportedly lowering CPU/GPU temperatures by 15-20C.
- Treat this as advanced tuning context, not a beginner/default recommendation.

Other files:

- `clean_auto_pp512_tg128_r5.log`: clean auto-policy run.
- `clean_high_pp512_tg128_r5.log`: clean high-policy run.
- `policy_state_clean.log`: policy and DPM state snapshots.
- Earlier `auto_balance_performance.log` only reached device initialization before being stopped; it should not be used as a benchmark result.
