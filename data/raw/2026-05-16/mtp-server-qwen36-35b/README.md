# Qwen3.6 MTP llama-server Sweep

Date: 2026-05-16.

Purpose: test whether merged `llama.cpp` MTP speculative decoding can produce a practical Strix Halo server-speed win, and whether it can honestly break 100 t/s.

## Host And Build

- System: Beelink GTR9 Pro
- CPU/GPU: AMD Ryzen AI MAX+ 395 / Radeon 8060S
- Kernel: 6.19.4-061904-generic
- Mesa/RADV: 26.0.6
- Backend: Vulkan/RADV
- Tool: `llama-server`
- llama.cpp: b9187 / `0253fb21f595246f54c192fe8332f34173be251b`

## Models

Official MTP GGUF:

- Source: `ggml-org/Qwen3.6-35B-A3B-MTP-GGUF`
- File: `Qwen3.6-35B-A3B-MTP-Q8_0.gguf`
- Size: 37,801,096,544 bytes
- SHA256: `5f24078b0ec9186811834fe229edd71c6cd1e861d6586137d08510ef648126ce`

Local requant:

- File: `Qwen3.6-35B-A3B-MTP-Q4_K_M.gguf`
- Created locally with `llama-quantize --allow-requantize`
- Size: 21,712,409,952 bytes
- SHA256: `be11d472527e5013290b09c1afc12694a326a4184eb97cf58fff579a671dddc3`

## Prompt Harness

Six practical prompts were sent to `/completion` with:

- `n_predict: 192`
- `temperature: 0`
- `top_k: 1`
- `cache_prompt: false`
- `stream: false`

The harness records `timings.predicted_per_second` from `llama-server`.

## Main Results

| Run | Mean t/s | Min t/s | Max t/s | Read |
|-----|---------:|--------:|--------:|------|
| Q8_0 baseline, no MTP | 56.198 | 53.346 | 69.441 | Heavy official model baseline. |
| Q8_0 MTP `draft-n=2` | 67.041 | 60.814 | 75.553 | Best Q8 average; useful but too heavy. |
| Q4_K_M baseline, no MTP | 74.132 | 72.546 | 74.561 | Local requant baseline. |
| Q4_K_M MTP `draft-n=2` | 87.534 | 82.178 | 95.681 | Best practical average in this sweep. |
| Q4_K_M MTP `draft-n=3`, `-t 16`, `--poll 10` | 83.128-84.194 | 70.247-70.563 | 99.859-100.740 | Repeatable single-prompt 100 t/s, not a broad average claim. |

## Conclusion

MTP is a real speedup for the Qwen3.6 MTP server path on Strix Halo. The best broad result was about 87.5 t/s average across six prompts. The tuned `draft-n=3` route repeated a 100 t/s single-prompt result three times out of four, with a best observed prompt of 100.740 t/s.

This does not replace the direct non-speculative 98.51 t/s Qwen3-Coder `llama-bench` headline. Treat it as an advanced server/speculative-decoding result.
