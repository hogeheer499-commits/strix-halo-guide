# Strix Halo Local LLM FAQ


## Is The Guide Claiming 100 t/s Direct?

No.

The current direct Qwen3-Coder rows are:

- 98.51 t/s Q4_K_S speed-first quant via direct `llama-bench`
- 96.76 t/s UD-Q4_K_XL balanced quant via direct `llama-bench`

The about 101.1 t/s Qwen3.6 result is a separate `llama-server` MTP/speculative decoding route. It is not the direct `llama-bench` headline.

## Should I Use ROCm Or Vulkan/RADV?

Start with Vulkan/RADV for the measured GGUF generation-heavy path. Test ROCm/HIP for prompt-heavy work, server experiments, vLLM/gfx1151 work, and capacity/RPC cases.

## Does This Apply To Framework Desktop?

Not automatically. Framework Desktop uses the same Strix Halo class, but exact performance needs measured rows with matching commands and setup details. Framework reproductions are especially useful.

## Does This Run 120B Models?

The guide includes a gpt-oss-120b MXFP4 split GGUF row at 55.57 t/s direct llama.cpp Vulkan/RADV on the measured Beelink setup. This is performance evidence, not a model-quality evaluation.

## What Results Are Most Useful?

- direct `llama-bench` CSV rows
- Ollama API rows with request details
- server concurrency rows
- long-context filled-KV rows
- power readings
- failed setup reports
- Windows versus Linux comparisons on the same machine

## Where Should I Submit Results?

- Benchmark report: https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=benchmark-report.md
- Power report: https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=power-report.md
- Discussion: https://github.com/hogeheer499-commits/strix-halo-guide/discussions
