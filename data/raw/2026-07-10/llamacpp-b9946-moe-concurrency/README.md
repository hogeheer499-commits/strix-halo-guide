# llama.cpp b9946 MoE Concurrency Reproducer

This first-party Beelink GTR9 Pro run checks the concurrency cliff reported in
`llama.cpp` issue [#25356](https://github.com/ggml-org/llama.cpp/issues/25356).
It uses the local Qwen3-Coder 30B-A3B `UD-Q4_K_XL` artifact with the issue's
`pp512`, `tg128`, Q4_0 KV-cache, 32k-context, and 1/2/4/8/9/12/16/24/32
parallel sweep. The local artifact is a same-family reproducer; its filename is
not the literal artifact name shown in the issue.

## Result

| Route | np8 decode | np9 decode | np32 decode | Read |
| --- | ---: | ---: | ---: | --- |
| Official b9946 Vulkan | 214.23 t/s | 143.05 t/s | 321.97 t/s | Reproduces the sharp 8-to-9 cliff. |
| b9946 Vulkan with issue threshold patch | 202.73 t/s | 195.38 t/s | 321.02 t/s | Removes most of the cliff; experimental source build. |
| Official b9946 ROCm 7.2 | 77.30 t/s | 81.03 t/s | 97.58 t/s | Runs, but is much slower on this workload. |
| Lemonade ROCm b1259 | 184.93 t/s | 191.24 t/s | 354.59 t/s | Avoids the cliff and is competitive at high concurrency. |

The sysfs telemetry is GPU/APU telemetry, not wall power. The patched Vulkan
sweep reached a recorded 98 C maximum, so this one-pass result is not a default
setup recommendation or a thermal-safety conclusion. The official b9946 ROCm
run's `gpu_busy_percent` counter stayed at 1% despite active compute and should
not be treated as valid utilization telemetry for that backend.

## Evidence

- [`summary.csv`](summary.csv)
- [`central machine-readable CSV`](../../../moe_concurrency.csv)
- [`telemetry-summary.csv`](telemetry-summary.csv)
- [`b9946-issue25356-thresholds.patch`](b9946-issue25356-thresholds.patch)
- per-route JSONL, stderr, commands, and one-second telemetry files in this directory
- [`host-snapshot.txt`](host-snapshot.txt)
