# Strix Halo Server Shootout

Status: active benchmark track, started 2026-05-05.

This track answers a practical question:

> How should I use a Strix Halo local AI PC, and which local server should run each job?

Single-user `llama-bench` numbers are useful, but they do not tell you whether the box feels good as a daily AI service. A local AI PC is useful when it can serve chat, coding tools, agents, document search, and background jobs through stable APIs.

## Current Answer

As of the May 2026 baseline:

| Use case | Start with | Why | Status |
|----------|------------|-----|--------|
| Beginner local chat | Ollama Vulkan/RADV | easiest model management and setup | measured single-user baseline |
| Open WebUI private chat/docs | Ollama first, then `llama-server` if you need speed | lowest friction, OpenAI-compatible clients work | measured Ollama baseline; RAG not yet benchmarked |
| Coding assistant or local scripts | `llama-server` Vulkan/RADV | fastest measured local OpenAI-compatible path today | measured |
| Multiple local tools/users | `llama-server --parallel 8` Vulkan/RADV | best measured throughput/latency balance so far | measured |
| vLLM/API appliance | kyuz0 or Lemonade vLLM ROCm container | serving-oriented stack with batching and production APIs | small smoke test only; throughput pending |
| Long-context research | follow the long-context section, do not assume one backend wins | backend choice changes after 32K context | partially measured |
| Image/video generation | kyuz0 ComfyUI toolboxes | separate ROCm container path for diffusion/video workloads | outside this LLM server shootout |

The current measured winner for a local text API is still `llama-server` on Vulkan/RADV, especially at `--parallel 8`. The open question is whether current vLLM/ROCm builds are better for agent-serving, batching, tool APIs, or long-running server workloads.

## What Counts As A Server

A server is anything that exposes a model to other tools through an HTTP API.

| Server | What it is good for | Main tradeoff |
|--------|---------------------|---------------|
| Ollama | easy setup, model pulling, local chat, Open WebUI | lower short-context speed than direct `llama-server` in current tests |
| `llama-server` Vulkan/RADV | fastest measured local OpenAI-compatible llama.cpp path | manual model files and flags |
| `llama-server` ROCm/Lemonade | packaged ROCm llama.cpp builds for gfx1151 | needs controlled local benchmark on this machine |
| kyuz0 vLLM toolbox | isolated Strix Halo vLLM container path | heavier stack, throughput still unmeasured here |
| Lemonade `vllm-rocm` | portable gfx1151 vLLM build | candidate, not yet measured here |
| Experimental AWQ/DFlash repos | bleeding-edge vLLM experiments | not canonical until reproduced locally |

## Shootout Matrix

The canonical data file is `data/server_shootout.csv`.

Current measured/pending summary:

| Server | Backend | Model | Concurrency | Result | Verdict |
|--------|---------|-------|-------------|--------|---------|
| `llama-server` | Vulkan/RADV | Qwen3.6 35B-A3B UD-Q4_K_M | 8 | 161.98 aggregate t/s, 0.307 s mean TTFT | best measured general local API point |
| `llama-server` | Vulkan/RADV | Qwen3-Coder 30B-A3B UD-Q4_K_XL | 8 | 173.16 aggregate t/s, 0.382 s mean TTFT | best measured coding API point |
| Ollama | Vulkan/RADV | Qwen3.6 35B-A3B Q4_K_M | 1 | 50.51 t/s controlled API warm average | easiest useful path |
| kyuz0 vLLM toolbox | ROCm/TheRock | Qwen3-0.6B | 1 | OpenAI-compatible smoke test passed | serving works, throughput not proven |
| Lemonade `llamacpp-rocm` b1259 | ROCm 7.13 | pending | pending | candidate | needs measured comparison |
| Lemonade `vllm-rocm` 0.20.1 gfx1151 | ROCm 7.12 | pending | pending | candidate | needs measured comparison |

## Benchmark Protocol

Keep this boring and reproducible.

0. Confirm the system is clean enough:

```bash
scripts/check_benchmark_cleanliness.sh
```

This script is read-only. It does not stop RustDesk, T3, Docker, Ollama, or VMs. It only reports whether the system is clean enough for publishable measurements.

1. Record host state:
   - kernel
   - Mesa/RADV or ROCm version
   - `tuned-adm active`
   - GPU clock
   - container image/tag if applicable
   - model name, quant, hash/path
2. Start the server with exact flags.
3. Run a feature probe:

```bash
python3 scripts/check_openai_server_features.py \
  --url http://127.0.0.1:8080 \
  --model MODEL_NAME \
  --output data/raw/DATE/SERVER/features.json
```

4. Run the streaming throughput harness:

```bash
python3 scripts/benchmark_openai_server.py \
  --url http://127.0.0.1:8080 \
  --model MODEL_NAME \
  --np 8 \
  --tokens 128 \
  --reps 3 \
  --detail data/raw/DATE/SERVER/detail-np8.csv \
  --summary data/raw/DATE/SERVER/summary-np8.csv
```

5. Sweep concurrency:
   - 1
   - 2
   - 4
   - 8
   - 16
6. Store raw logs and CSV summaries.
7. Add only defensible rows to `data/server_shootout.csv`.

## Required Metrics

Minimum publishable row:

- server and backend
- exact build or image tag
- model and quant
- context limit
- endpoint tested
- concurrency
- tokens per request
- aggregate tokens/sec
- mean and p95 TTFT
- p95 inter-token latency
- error count
- setup friction
- limitations

Do not compare two rows as "faster" unless model, quant, prompt, endpoint, token count, context, and concurrency are close enough to be meaningful.

## Feature Probes

Throughput is not enough for a useful local AI PC. Each server should also be tested for:

| Feature | Why it matters |
|---------|----------------|
| `/v1/models` | clients can discover models |
| `/v1/completions` | simple scripts and benchmark harness |
| `/v1/chat/completions` | OpenAI-style chat clients |
| streaming chat | interactive latency |
| tool/function calling | agents and coding workflows |
| long-running stability | daily local server use |
| metrics endpoint | monitoring and debugging |

Tool calling is model-dependent, so failures must be described carefully. A server can support tool-call syntax while a model still chooses not to call a tool.

## Validity Rules

- Do not install vLLM, PyTorch, ROCm, or TheRock packages into the host Python environment.
- Test stable container/builds before nightly/latest builds.
- Do not run publishable numbers while RustDesk, T3 Code, Zoom, unrelated VMs, or unrelated local AI services are active.
- Treat external vLLM/DFlash claims as leads until reproduced locally.
- Do not publish tokens-per-watt until power telemetry is validated.
- Keep failed starts, OOMs, compile hangs, and missing endpoints in the notes. Failure cases are part of the value.

## Next Run Order

1. Re-run the current `llama-server` Vulkan/RADV baseline through the new feature probe.
2. Test Lemonade `llamacpp-rocm` b1259 with the same model/concurrency shape.
3. Test kyuz0 vLLM stable with a supported AWQ model.
4. Test Lemonade `vllm-rocm` gfx1151 if it can serve the same or a clearly comparable model.
5. Only then evaluate experimental AWQ/DFlash repos, clearly labeled as advanced.
