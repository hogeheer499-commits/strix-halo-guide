# Qwen3-Coder Q4_K_S llama-server ngram Sweep

Date: 2026-05-17.

Purpose: check whether the 98.51 t/s direct Qwen3-Coder Q4_K_S route can become a broad 100 t/s practical `llama-server` route with ngram speculative decoding.

## Host And Build

- System: Beelink GTR9 Pro
- CPU/GPU: AMD Ryzen AI MAX+ 395 / Radeon 8060S
- Kernel: 6.19.4-061904-generic
- Backend: Vulkan/RADV
- Tool: `llama-server`
- llama.cpp: b9187 / `0253fb21f595246f54c192fe8332f34173be251b`

## Model

- File: `Qwen3-Coder-30B-A3B-Instruct-Q4_K_S.gguf`
- Local path: `/home/hoge-heer/benchmark-models/qwen3-coder-break100/Qwen3-Coder-30B-A3B-Instruct-Q4_K_S.gguf`

## Main Results

| Run | Mean t/s | Min t/s | Max t/s | Read |
|-----|---------:|--------:|--------:|------|
| Baseline server, no speculation | 93.715 | 93.436 | 93.877 | Lower than the direct `llama-bench` 98.51 t/s row. |
| `ngram-cache` | 93.221 | 92.989 | 93.535 | No win. |
| `ngram-map-k` | 94.594 | 89.383 | 104.712 | Better max, not broad 100. |
| `ngram-map-k4v` | 95.209 | 92.757 | 104.724 | Best average in this sweep. |
| `ngram-simple` | 94.671 | 92.162 | 103.303 | Useful but behind `ngram-map-k4v`. |

## Conclusion

ngram speculative decoding helps some Qwen3-Coder server prompts, but it did not create a broad 100 t/s practical server result. The direct `llama-bench` 98.51 t/s Q4_K_S row remains the stronger speed-first coding headline.
