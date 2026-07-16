# Qwen AgentWorld 35B-A3B IQ4_XS Scout

Date: 2026-07-16

System: Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S, 128 GB
unified memory.

This scout tests Qwen AgentWorld as a language world model for local agent
environment simulation. It is not evaluated here as a general-purpose chat or
coding assistant.

## Reproducibility Pin

- runtime: official `llama.cpp` b10034, commit `505b1ed15`
- backend: Vulkan/RADV, full GPU offload
- model: `Qwen-AgentWorld-35B-A3B-UD-IQ4_XS.gguf`
- quant source: `unsloth/Qwen-AgentWorld-35B-A3B-GGUF`
- quant source revision: `3a305abf5cfd119ee999dfe929c433746edd8d63`
- model SHA-256: `ff4201b0c163950dc96aeaca033398543a1d62513ddc1c4030f9b94823764e06`

## Result

| Test | Result |
| --- | ---: |
| `pp512` | 1182.77 t/s |
| `tg128` | **65.65 t/s** |
| terminal-world smoke | correctly predicted `agentworld-ok` |
| 128K Q8 KV allocation | pass |

The 17.77 GB language-only GGUF loads cleanly on the current Vulkan runtime.
Using the official terminal-environment framing, the model correctly predicted
the output of `echo agentworld-ok`. A separate `-c 131072` Q8 KV run also
loaded and generated successfully; this is a context-allocation smoke, not a
filled-128K quality or retrieval benchmark.

AgentWorld visibly reasons before emitting the simulated observation. The
world-model use case and its prompt format matter, so its 65.65 t/s direct row
should not be presented as a replacement for the guide's ordinary assistant or
coding routes.

## Evidence

- [`llama-bench.csv`](llama-bench.csv): direct benchmark result
- [`terminal-smoke-output.txt`](terminal-smoke-output.txt): terminal simulation
- [`context-128k-output.txt`](context-128k-output.txt): 128K allocation output
- [`context-128k-stderr.txt`](context-128k-stderr.txt): elapsed time and memory metadata
- [`run-scout.sh`](run-scout.sh): exact reproducible runner
- [`host-snapshot.txt`](host-snapshot.txt): host and Vulkan context
- [`model.sha256`](model.sha256): exact model identity
- [`upstream-model-card.md`](upstream-model-card.md) and
  [`quant-card.md`](quant-card.md): source metadata captured at test time
