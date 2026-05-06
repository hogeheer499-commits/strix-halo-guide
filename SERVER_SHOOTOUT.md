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
| Coding assistant or local scripts | `llama-server` Vulkan/RADV | best measured Qwen3.6 path at 1-4 parallel requests | measured |
| Multiple local tools/users | Lemonade `llamacpp-rocm` b1259 | best measured Qwen3.6 aggregate throughput at 8-16 parallel requests | measured |
| vLLM/API appliance | kyuz0 or Lemonade vLLM ROCm container | serving-oriented stack with batching and production APIs | small smoke test only; throughput pending |
| Long-context research | follow the long-context section, do not assume one backend wins | backend choice changes after 32K context | partially measured |
| Image/video generation | kyuz0 ComfyUI toolboxes | separate ROCm container path for diffusion/video workloads | outside this LLM server shootout |

The practical split is now clear for Qwen3.6 35B-A3B UD-Q4_K_M: use Vulkan/RADV `llama-server` for single-user and small parallel workloads, and use Lemonade `llamacpp-rocm` b1259 when the box is serving many simultaneous local requests. The open question is whether current vLLM/ROCm builds are better for agent-serving, batching, tool APIs, or long-running server workloads.

## What Counts As A Server

A server is anything that exposes a model to other tools through an HTTP API.

| Server | What it is good for | Main tradeoff |
|--------|---------------------|---------------|
| Ollama | easy setup, model pulling, local chat, Open WebUI | lower short-context speed than direct `llama-server` in current tests |
| `llama-server` Vulkan/RADV | fastest measured Qwen3.6 path at 1-4 parallel requests | manual model files and flags |
| `llama-server` ROCm/Lemonade | strongest measured Qwen3.6 aggregate throughput at 8-16 parallel requests | packaged build, more setup than Vulkan |
| kyuz0 vLLM toolbox | isolated Strix Halo vLLM container path | heavier stack, throughput still unmeasured here |
| Lemonade `vllm-rocm` | portable gfx1151 vLLM build | candidate, not yet measured here |
| Experimental AWQ/DFlash repos | bleeding-edge vLLM experiments | not canonical until reproduced locally |

## Shootout Matrix

The canonical data file is `data/server_shootout.csv`.

Current measured/pending summary:

| Server | Backend | Model | Concurrency | Result | Verdict |
|--------|---------|-------|-------------|--------|---------|
| `llama-server` | Vulkan/RADV | Qwen3.6 35B-A3B UD-Q4_K_M | 1-16 sweep | 58.80 to 189.72 aggregate t/s | best low-concurrency path |
| `llama-server` | Vulkan/RADV | Qwen3-Coder 30B-A3B UD-Q4_K_XL | 8 | 173.16 aggregate t/s, 0.382 s mean TTFT | best measured coding API point |
| Ollama | Vulkan/RADV | Qwen3.6 35B-A3B Q4_K_M | 1 | 50.51 t/s controlled API warm average | easiest useful path |
| kyuz0 vLLM toolbox | ROCm/TheRock | Qwen3-0.6B | 1 | OpenAI-compatible smoke test passed | serving works, throughput not proven |
| Lemonade `llamacpp-rocm` b1259 | ROCm 7.13 | Qwen3.6 35B-A3B UD-Q4_K_M | 1-16 sweep | 48.62 to 207.81 aggregate t/s | best high-concurrency path |
| Lemonade `vllm-rocm` 0.20.1 gfx1151 | ROCm 7.12 | pending | pending | candidate | needs measured comparison |

## Qwen3.6 Full Sweep

Measured 2026-05-05 on the Beelink GTR9 Pro with the normal workstation baseline recorded. Each row is a 5-rep streaming `/v1/completions` run, 128 generated tokens per request, 4096 context tokens per slot, and 0 throughput errors.

| Parallel requests | Vulkan/RADV aggregate t/s | Vulkan p95 ITL | Lemonade ROCm aggregate t/s | Lemonade p95 ITL | Read |
|------------------:|--------------------------:|---------------:|----------------------------:|-----------------:|------|
| 1 | 58.80 | 16.2 ms | 48.62 | 20.0 ms | Vulkan wins for single-user chat/scripts |
| 2 | 96.08 | 19.8 ms | 82.19 | 23.6 ms | Vulkan still wins |
| 4 | 138.83 | 27.4 ms | 127.03 | 30.4 ms | Vulkan still wins |
| 8 | 170.87 | 45.2 ms | 177.17 | 43.5 ms | Lemonade starts winning aggregate and ITL |
| 16 | 189.72 | 81.9 ms | 207.81 | 74.3 ms | Lemonade is the high-concurrency winner |

Raw data: `data/raw/2026-05-05/server-shootout/full-sweep-qwen36-workstation-baseline/`.

Repeat validation after workstation connection work:

| Server | Parallel | Baseline aggregate t/s | Repeat aggregate t/s | Delta |
|--------|---------:|-----------------------:|---------------------:|------:|
| `llama-server` Vulkan/RADV | 1 | 58.80 | 59.56 | +1.3% |
| `llama-server` Vulkan/RADV | 2 | 96.08 | 97.34 | +1.3% |
| `llama-server` Vulkan/RADV | 4 | 138.83 | 138.12 | -0.5% |
| `llama-server` Vulkan/RADV | 8 | 170.87 | 172.96 | +1.2% |
| `llama-server` Vulkan/RADV | 16 | 189.72 | 190.77 | +0.6% |
| Lemonade `llamacpp-rocm` | 1 | 48.62 | 51.40 | +5.7% |
| Lemonade `llamacpp-rocm` | 2 | 82.19 | 84.72 | +3.1% |
| Lemonade `llamacpp-rocm` | 4 | 127.03 | 125.75 | -1.0% |
| Lemonade `llamacpp-rocm` | 8 | 177.17 | 181.95 | +2.7% |
| Lemonade `llamacpp-rocm` | 16 | 207.81 | 212.38 | +2.2% |

The repeat did not change the recommendation: Vulkan/RADV remains better at
1-4 parallel requests, and Lemonade ROCm remains better at 8-16.

## Smoke Runs

These runs validate the workflow and server behavior, but they are not headline benchmark claims.

| Date | Server | Model | Condition | Result |
|------|--------|-------|-----------|--------|
| 2026-05-05 | `llama-server` Vulkan/RADV | Qwen3.6 35B-A3B UD-Q4_K_M | Normal workstation baseline recorded, VM paused | OpenAI-compatible `/v1/completions` at `-np 8`: 173.36 aggregate t/s, 0 errors; feature probe returned HTTP 200 for models, completions, chat, streaming chat, and tools schema |
| 2026-05-05 | Lemonade `llamacpp-rocm` b1259 | Qwen3.6 35B-A3B UD-Q4_K_M | Normal workstation baseline recorded, VM paused | OpenAI-compatible `/v1/completions` at `-np 8`: 176.43 aggregate t/s, 0 errors; feature probe returned HTTP 200 for models, completions, chat, streaming chat, and tools schema |

## Benchmark Protocol

Keep this boring and reproducible.

0. Confirm the system is clean enough:

```bash
scripts/check_benchmark_cleanliness.sh
```

This script is read-only. It does not stop local services or mutate benchmark state. On the maintainer workstation it also reports protected local workflow dependencies; third-party replicators should record equivalent background state rather than treating those services as part of the public benchmark requirement. Maintainer-only guardrails live in [`MAINTAINER_NOTES.md`](MAINTAINER_NOTES.md).

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
- Do not run publishable numbers while remote desktop streaming, video calls, unrelated VMs, or unrelated local AI services are active.
- Record any required local workflow services separately from the benchmark server under test.
- Treat external vLLM/DFlash claims as leads until reproduced locally.
- Do not publish tokens-per-watt until power telemetry is validated.
- Keep failed starts, OOMs, compile hangs, and missing endpoints in the notes. Failure cases are part of the value.

## Next Run Order

1. Done: current `llama-server` Vulkan/RADV baseline through the new feature probe.
2. Done: Lemonade `llamacpp-rocm` b1259 with the same model/concurrency shape.
3. Done: full sweep for the two best llama.cpp paths with the workstation baseline recorded.
4. Test kyuz0 vLLM stable with a supported AWQ model.
5. Test Lemonade `vllm-rocm` gfx1151 if it can serve the same or a clearly comparable model.
6. Only then evaluate experimental AWQ/DFlash repos, clearly labeled as advanced.
