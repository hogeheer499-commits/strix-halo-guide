# 2026-05-05 Server Shootout Smoke: llama-server Qwen3.6 np8

Status: smoke-test / workflow validation.

This run records the normal workstation background state. Treat the numbers as
useful workflow evidence; the smoke-test label is because this is a short 3-rep
validation run, not a full sweep.

## Preflight

| Item | Value |
|------|-------|
| System | Beelink GTR9 Pro |
| Kernel | 6.19.4-061904-generic |
| Vulkan driver | Mesa RADV 26.0.6, kisak-mesa PPA |
| llama.cpp | b9010 / `d05fe1d7d` |
| Server | `llama-server` Vulkan/RADV |
| Model | `/home/hoge-heer/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` |
| Port | `127.0.0.1:18080` |
| Parallel slots | 8 |
| Context | 32768 total, 4096 per slot |
| Workflow services | normal workstation baseline recorded |
| RustDesk | stopped |
| Ollama | stopped |
| Docker containers | stopped |
| Zoom VM | paused |
| tuned | `accelerator-performance` active |

Note: the raw `cleanliness-*.txt` logs record exact workstation background
state. They are preserved as captured rather than rewritten.

## Server Command

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
/home/hoge-heer/llama-cpp-latest/build-vulkan/bin/llama-server \
  -m /home/hoge-heer/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf \
  -fa on -ngl 999 --no-mmap \
  -c 32768 -np 8 -cb \
  -b 2048 -ub 512 --no-cache-prompt \
  --host 127.0.0.1 --port 18080 --metrics --slots
```

## Feature Probe

Command:

```bash
python3 scripts/check_openai_server_features.py \
  --url http://127.0.0.1:18080 \
  --model Qwen3.6-35B-A3B-UD-Q4_K_M.gguf \
  --output data/raw/2026-05-05/server-shootout/llama-server-qwen36-np8-workstation-baseline/features.json
```

Observed:

- `/v1/models`: HTTP 200
- `/v1/completions`: HTTP 200
- `/v1/chat/completions`: HTTP 200
- streaming chat: HTTP 200
- `/v1/chat/completions` with tools schema: HTTP 200
- tool schema was accepted, but the model did not emit a tool call for this prompt

## Throughput

Command:

```bash
python3 scripts/benchmark_openai_server.py \
  --url http://127.0.0.1:18080 \
  --model Qwen3.6-35B-A3B-UD-Q4_K_M.gguf \
  --np 8 \
  --tokens 128 \
  --reps 3 \
  --detail data/raw/2026-05-05/server-shootout/llama-server-qwen36-np8-workstation-baseline/detail-np8.csv \
  --summary data/raw/2026-05-05/server-shootout/llama-server-qwen36-np8-workstation-baseline/summary-np8.csv
```

Summary across 3 measured reps:

| Metric | Value |
|--------|------:|
| Aggregate throughput mean | 173.36 t/s |
| Aggregate throughput min | 173.19 t/s |
| Aggregate throughput max | 173.57 t/s |
| Mean per-request throughput | 22.64 t/s |
| Mean TTFT | 0.252 s |
| Mean p95 TTFT | 0.252 s |
| Mean ITL | 44.5 ms |
| Mean p95 ITL | 44.5 ms |
| Errors | 0 |

## Files

- `cleanliness-before.txt`
- `cleanliness-after.txt`
- `llama-server.log`
- `models.json`
- `features.json`
- `features.txt`
- `benchmark-np8.txt`
- `detail-np8.csv`
- `summary-np8.csv`
