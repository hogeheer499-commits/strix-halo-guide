# llama.cpp PR #22970 Vulkan K-Quant Transpose-A Test - 2026-05-16

Goal: test whether open PR #22970 (`vulkan: transpose A-matrix data layout for K-quant mul_mat performance`) can push Qwen3-Coder 30B-A3B Q4_K_S over 100 t/s on Strix Halo.

PR: https://github.com/ggml-org/llama.cpp/pull/22970

Host benchmark noise was temporarily paused while T3 stayed running.

## Result

| Run | Repeats | pp512 | tg128 | Read |
|-----|--------:|------:|------:|------|
| [`pr22970-q4ks-t15-r5.csv`](pr22970-q4ks-t15-r5.csv) | r5 | 1366.50 | 98.51 | No break-100 signal. |
| [`pr22970-q4ks-t15-r20.csv`](pr22970-q4ks-t15-r20.csv) | r20 | 1383.46 | 98.74 | Did not beat the 98.51 r50 row by enough to change the public headline, and did not approach 100. |

Conclusion: PR #22970 is not a Qwen3-Coder direct-generation break-100 route on this Beelink. Its upstream PR text mainly predicts prompt-processing gains for K-quants; this local test did not find a tg128 win large enough for the 100 t/s target.
