# Strix Halo ROCm Versus Vulkan/RADV For Local LLMs


## Short Version

For the measured generation-heavy GGUF Qwen rows in this guide, Vulkan/RADV is currently the fastest practical path. ROCm/HIP still matters for prompt-heavy tests, server experiments, vLLM work, capacity/RPC cases, and future gfx1151 support.

Do not reduce this to "Vulkan good, ROCm bad." The answer changes by workload.

## Decision Table

| Workload | Start With | Why |
|----------|------------|-----|
| Easy local chat | Ollama Vulkan/RADV | Simple model pulling and useful measured API row. |
| Fast single-user GGUF generation | `llama.cpp` Vulkan/RADV | Fastest measured direct Qwen generation rows. |
| Low-concurrency local API | `llama-server` Vulkan/RADV | Best measured 1-4 parallel Qwen3.6 server path. |
| Higher concurrency server sweep | Lemonade `llamacpp-rocm` | Won aggregate throughput at 8-16 in measured Qwen3.6 sweep. |
| Prompt-heavy ingestion | Test ROCm/HIP | HIP won prompt-processing-heavy rows in the same-source matrix. |
| vLLM/gfx1151 experiments | ROCm stack | Experimental; do not claim guide-proven throughput yet. |
| Capacity/RPC cases | ROCm RPC when needed | Useful when the model does not fit on one box. |

## Evidence To Link

- `BACKEND_CROSSOVER.md`
- `SERVER_SHOOTOUT.md`
- `ROCM_VLLM_BUGWATCH.md`
- `data/max_performance_campaign.csv`
- `data/server_shootout.csv`
- `data/headline_claims.csv`

## Comment-Safe Framing

```text
In this guide's measured Strix Halo GGUF generation rows, Vulkan/RADV won the current Qwen token-generation path. ROCm/HIP is still relevant for prompt-heavy work, serving, vLLM/gfx1151 experiments, and capacity cases. The exact model, quant, command, context, and backend decide the answer.
```

## What Is Not Proven

- A polished vLLM throughput win on a comparable 35B Strix Halo path.
- DFlash throughput on a comparable local workload.
- A universal ROCm versus Vulkan rule across all models.
- Windows versus Linux parity on the same machine.
