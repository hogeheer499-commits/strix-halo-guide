# 2026-05-03 Multi-User llama-server Benchmark

Purpose: measure whether the Strix Halo box can serve multiple concurrent local requests, not just one single-user `llama-bench` stream.

## Preflight

| Item | Value |
|------|-------|
| System | Beelink GTR9 Pro |
| CPU/GPU | AMD Ryzen AI MAX+ 395 / Radeon 8060S |
| Kernel | 6.19.4-061904-generic |
| Vulkan driver | Mesa RADV 26.0.6, kisak-mesa PPA |
| llama.cpp | b9010 / `d05fe1d7d` |
| Model | `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` |
| tuned profile | `accelerator-performance` |
| GPU clock | 2900 MHz selected |

## Method

Each run started a fresh `llama-server` with continuous batching enabled. The server used `-np` values of 1, 2, 4, 8, and 16. Total context was scaled so each slot had about 4096 tokens available.

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
~/llama-cpp-latest/build-vulkan/bin/llama-server \
  -m ~/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf \
  -fa on -ngl 999 --no-mmap \
  -c <4096 * np> -np <np> -cb \
  -b 2048 -ub 512 --no-cache-prompt \
  --host 127.0.0.1 --port <port> --metrics --slots
```

For each `-np` level:

- 1 warmup request.
- 3 measured repetitions.
- `np` concurrent streaming `/completion` requests per repetition.
- 128 generated tokens per request.
- `temperature=0`, `top_k=1`, `ignore_eos=true`, prompt cache disabled.

## Results

| `-np` | Concurrent Requests | Aggregate tg | Avg per Request | Mean TTFT | Mean ITL | Errors |
|-------|---------------------|--------------|-----------------|-----------|----------|--------|
| 1 | 1 | 59.21 t/s | 59.21 t/s | 0.117 s | 16.1 ms | 0 |
| 2 | 2 | 92.21 t/s | 46.11 t/s | 0.198 s | 20.3 ms | 0 |
| 4 | 4 | 130.81 t/s | 32.71 t/s | 0.237 s | 29.0 ms | 0 |
| 8 | 8 | 161.98 t/s | 20.25 t/s | 0.307 s | 47.4 ms | 0 |
| 16 | 16 | 165.98 t/s | 10.38 t/s | 0.547 s | 92.9 ms | 0 |

## Verdict

Continuous batching is highly effective up to about `-np 8`: aggregate generation rises from 59.2 t/s to 162.0 t/s while TTFT stays around 0.3 s. `-np 16` does not materially improve total throughput, but it proves the box can keep 16 simultaneous 128-token streams alive with no errors and sub-second TTFT.

Use `-np 8` as the current practical sweet spot for a local Qwen3.6 API service. Use `-np 16` only when fairness across many low-rate clients matters more than per-user speed.

Raw files:

- `qwen3.6-35b-ud-llama-server-multi-user-summary.csv`
- `qwen3.6-35b-ud-llama-server-multi-user-detail.csv`
- `llama-server-np*.log`
