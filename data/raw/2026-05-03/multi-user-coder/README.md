# 2026-05-03 Qwen3-Coder Multi-User llama-server Benchmark

Purpose: measure the fast coding model as a local API service under concurrent requests.

## Preflight

| Item | Value |
|------|-------|
| System | Beelink GTR9 Pro |
| CPU/GPU | AMD Ryzen AI MAX+ 395 / Radeon 8060S |
| Kernel | 6.19.4-061904-generic |
| Vulkan driver | Mesa RADV 26.0.6, kisak-mesa PPA |
| llama.cpp | b9010 / `d05fe1d7d` |
| Model | `Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf` |
| tuned profile | `accelerator-performance` |
| GPU clock | 2900 MHz selected |

## Method

Same harness as the Qwen3.6 multi-user run:

- Fresh `llama-server` per `-np` value.
- `-np 1/2/4/8/16`.
- Continuous batching enabled.
- About 4096 context tokens per slot.
- 1 warmup request, then 3 measured repetitions.
- `np` concurrent streaming `/completion` requests per repetition.
- 128 generated tokens per request.
- Prompt cache disabled.

## Results

| `-np` | Concurrent Requests | Aggregate tg | Avg per Request | Mean TTFT | Mean ITL | Errors |
|-------|---------------------|--------------|-----------------|-----------|----------|--------|
| 1 | 1 | 90.20 t/s | 90.20 t/s | 0.079 s | 10.6 ms | 0 |
| 2 | 2 | 121.65 t/s | 60.83 t/s | 0.133 s | 15.5 ms | 0 |
| 4 | 4 | 157.41 t/s | 39.36 t/s | 0.207 s | 24.0 ms | 0 |
| 8 | 8 | 173.16 t/s | 21.65 t/s | 0.382 s | 43.5 ms | 0 |
| 16 | 16 | 129.56 t/s | 8.10 t/s | 0.571 s | 119.9 ms | 0 |

## Verdict

`-np 8` is the practical peak for Qwen3-Coder serving on this stack: **173 t/s aggregate** with ~0.38 s TTFT. Unlike Qwen3.6, `-np 16` is not just a plateau; it regresses to 130 t/s aggregate and should be avoided for throughput-focused coding workloads.
