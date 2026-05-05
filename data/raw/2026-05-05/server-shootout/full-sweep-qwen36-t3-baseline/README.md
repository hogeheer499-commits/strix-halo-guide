# 2026-05-05 Server Shootout Full Sweep: Qwen3.6 T3 Baseline

Status: measured-local full sweep.

This run keeps T3 Code and the T3 proxies running because they are part of the
protected workstation baseline. The hygiene check reported 0 blockers and 0
warnings before and after the full run.

## Protocol

| Item | Value |
|------|-------|
| System | Beelink GTR9 Pro |
| Model | `/home/hoge-heer/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` |
| API | OpenAI-compatible `/v1/completions` streaming |
| Prompt | `scripts/benchmark_openai_server.py` default prompt |
| Tokens per request | 128 |
| Reps | 5 measured reps plus warmup |
| Parallel sweep | 1, 2, 4, 8, 16 |
| Context | 4096 tokens per slot |
| T3 Code | running, protected workstation baseline |
| RustDesk | stopped |
| Ollama | stopped |
| Docker containers | none running |
| Zoom VM | paused |
| tuned | `accelerator-performance` active |

For each concurrency point, the server was restarted with matching `-np` and
`-c = 4096 * np`.

## Results

| Server | Backend | Parallel | Aggregate t/s | Mean TTFT | p95 TTFT | p95 ITL | Errors |
|--------|---------|---------:|--------------:|----------:|---------:|--------:|-------:|
| `llama-server` | Vulkan/RADV | 1 | 58.80 | 0.115 s | 0.115 s | 16.2 ms | 0 |
| `llama-server` | Vulkan/RADV | 2 | 96.08 | 0.156 s | 0.156 s | 19.8 ms | 0 |
| `llama-server` | Vulkan/RADV | 4 | 138.83 | 0.206 s | 0.207 s | 27.4 ms | 0 |
| `llama-server` | Vulkan/RADV | 8 | 170.87 | 0.254 s | 0.255 s | 45.2 ms | 0 |
| `llama-server` | Vulkan/RADV | 16 | 189.72 | 0.399 s | 0.400 s | 81.9 ms | 0 |
| Lemonade `llamacpp-rocm` | ROCm/gfx1151 | 1 | 48.62 | 0.097 s | 0.097 s | 20.0 ms | 0 |
| Lemonade `llamacpp-rocm` | ROCm/gfx1151 | 2 | 82.19 | 0.127 s | 0.132 s | 23.6 ms | 0 |
| Lemonade `llamacpp-rocm` | ROCm/gfx1151 | 4 | 127.03 | 0.172 s | 0.175 s | 30.4 ms | 0 |
| Lemonade `llamacpp-rocm` | ROCm/gfx1151 | 8 | 177.17 | 0.271 s | 0.284 s | 43.5 ms | 0 |
| Lemonade `llamacpp-rocm` | ROCm/gfx1151 | 16 | 207.81 | 0.460 s | 0.475 s | 74.3 ms | 0 |

## Interpretation

Vulkan/RADV is the better default for single-user and small parallel loads.
Lemonade ROCm b1259 becomes the better llama.cpp serving path once the workload
reaches 8-16 simultaneous local requests.

## Files

- `summary.csv`
- `cleanliness-after-all.txt`
- `vulkan-radv/`
- `lemonade-b1259-rocm/`
