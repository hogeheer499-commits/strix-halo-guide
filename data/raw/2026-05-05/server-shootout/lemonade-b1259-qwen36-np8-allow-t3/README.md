# 2026-05-05 Server Shootout Smoke: Lemonade llamacpp-rocm b1259 Qwen3.6 np8

Status: smoke-test / workflow validation.

This run kept T3 Code running because T3 is a protected workflow dependency on
this workstation. Treat the numbers as useful workflow evidence; the smoke-test
label is because this is a short 3-rep validation run, not a full sweep.

## Preflight

| Item | Value |
|------|-------|
| System | Beelink GTR9 Pro |
| Kernel | 6.19.4-061904-generic |
| ROCm backend | Lemonade `llamacpp-rocm` b1259 for gfx1151 |
| llama.cpp | `e77056f` |
| ROCm build | 7.13.0a20260421 |
| Server | `llama-server` ROCm |
| Model | `/home/hoge-heer/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` |
| Port | `127.0.0.1:18081` |
| Parallel slots | 8 |
| Context | 32768 total, 4096 per slot |
| T3 Code | running, protected workstation baseline |
| RustDesk | stopped |
| Ollama | stopped |
| Docker containers | stopped |
| Zoom VM | paused |
| tuned | `accelerator-performance` active |

Note: the raw `cleanliness-*.txt` logs were captured before the hygiene script
renamed `ALLOW_T3=1` to the current protected T3 baseline policy. The condition
is the same: T3 stayed on and was recorded as expected background state.

## Tool Setup

Download:

```text
https://github.com/lemonade-sdk/llamacpp-rocm/releases/download/b1259/llama-b1259-ubuntu-rocm-gfx1151-x64.zip
```

Local path:

```text
/home/hoge-heer/strix-halo-bench-tools/lemonade-llamacpp-rocm-b1259-gfx1151/extracted
```

Archive SHA256:

```text
0f1a9f764ea89088f6202f62b615c6bf5a8132de88e13ab8f909316c0c22e6e7
```

Tiny preflight:

```bash
LD_LIBRARY_PATH=$TOOL \
HSA_OVERRIDE_GFX_VERSION=11.5.1 \
HIP_VISIBLE_DEVICES=0 \
ROCBLAS_USE_HIPBLASLT=1 \
$TOOL/llama-bench \
  -m /home/hoge-heer/models/Qwen_Qwen3-0.6B-Q8_0.gguf \
  -ngl 999 -fa 1 -mmp 0 -p 32 -n 16 -r 1
```

Observed tiny preflight:

- prompt processing: 1932.32 t/s
- token generation: 206.08 t/s

## Server Command

```bash
TOOL=/home/hoge-heer/strix-halo-bench-tools/lemonade-llamacpp-rocm-b1259-gfx1151/extracted

LD_LIBRARY_PATH=$TOOL \
HSA_OVERRIDE_GFX_VERSION=11.5.1 \
HIP_VISIBLE_DEVICES=0 \
ROCBLAS_USE_HIPBLASLT=1 \
$TOOL/llama-server \
  -m /home/hoge-heer/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf \
  -fa on -ngl 999 --no-mmap \
  -c 32768 -np 8 -cb \
  -b 2048 -ub 512 --no-cache-prompt \
  --host 127.0.0.1 --port 18081 --metrics --slots
```

## Feature Probe

Command:

```bash
python3 scripts/check_openai_server_features.py \
  --url http://127.0.0.1:18081 \
  --model Qwen3.6-35B-A3B-UD-Q4_K_M.gguf \
  --output data/raw/2026-05-05/server-shootout/lemonade-b1259-qwen36-np8-allow-t3/features.json
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
  --url http://127.0.0.1:18081 \
  --model Qwen3.6-35B-A3B-UD-Q4_K_M.gguf \
  --np 8 \
  --tokens 128 \
  --reps 3 \
  --detail data/raw/2026-05-05/server-shootout/lemonade-b1259-qwen36-np8-allow-t3/detail-np8.csv \
  --summary data/raw/2026-05-05/server-shootout/lemonade-b1259-qwen36-np8-allow-t3/summary-np8.csv
```

Summary across 3 measured reps:

| Metric | Value |
|--------|------:|
| Aggregate throughput mean | 176.43 t/s |
| Aggregate throughput min | 169.71 t/s |
| Aggregate throughput max | 183.11 t/s |
| Mean per-request throughput | 23.14 t/s |
| Mean TTFT | 0.269 s |
| Mean p95 TTFT | 0.279 s |
| Mean ITL | 43.6 ms |
| Mean p95 ITL | 43.7 ms |
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
