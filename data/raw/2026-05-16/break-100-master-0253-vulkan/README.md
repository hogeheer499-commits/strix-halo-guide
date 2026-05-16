# llama.cpp Latest Master Vulkan Break-100 Test - 2026-05-16

Goal: test whether latest upstream master after b9179 can push Qwen3-Coder 30B-A3B Q4_K_S over 100 t/s on Strix Halo.

Upstream commit: `0253fb21f595246f54c192fe8332f34173be251b`
Build number reported by llama-bench: b9187

Host benchmark noise was temporarily paused while T3 stayed running.

## Result

| Run | Repeats | pp512 | tg128 | Read |
|-----|--------:|------:|------:|------|
| [`master0253-q4ks-t15-r5.csv`](master0253-q4ks-t15-r5.csv) | r5 | 1385.67 | 99.08 | Close, but still below 100. |
| [`master0253-q4ks-t15-r20.csv`](master0253-q4ks-t15-r20.csv) | r20 | 1341.77 | 98.64 | Longer confirmation fell back below 99. |

Conclusion: latest master b9187 did not produce a stable 100 t/s direct `llama-bench` path for Qwen3-Coder Q4_K_S. The merged MTP support is still interesting for real server/speculative decoding tests, but it does not change the direct non-speculative `llama-bench` headline.
