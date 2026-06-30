# Minix Elite ER939 Ai Ollama 0.30.10 Community Report

Source: [`hogeheer499-commits/strix-halo-guide#27`](https://github.com/hogeheer499-commits/strix-halo-guide/issues/27)

Contributor: [`papagenic`](https://github.com/papagenic)

Status: community-reported buyer-path evidence. This is not a first-party Beelink headline claim and not a direct `llama-bench` comparison.

## Reported System

- Device: Minix Elite ER939 Ai
- CPU/GPU: template field was not filled in the issue; treat this as a reported Strix Halo-class system row, not a fully verified CPU/GPU metadata row
- RAM: `128GI` as reported
- BIOS UMA setting: 1G
- IOMMU setting: disabled
- OS: Ubuntu 26.04 LTS
- Kernel: 7.0.0-22-generic
- Mesa: Mesa 26.1.3, kisak-mesa PPA
- ROCm: `1.1` as reported
- Ollama: 0.30.10
- tuned profile: `accelerator-performance`
- Vulkan ICD: template field left as `RADV / AMDVLK / other`; not confirmed

## Reported Benchmark

- Model: `qwen3.6:35b-a3b`
- Model source: Ollama
- Command: `./bench-ollama.sh`
- Timestamp: 2026-06-24T12:00:13Z
- Prompt eval: 97.4 t/s over 14 tokens
- Generation: 30.5 t/s over 206 tokens
- Total time: 16.74s

## Interpretation

This is useful as the first Minix Elite ER939 Ai owner report and as an Ollama 0.30.10 / Ubuntu 26.04 / kernel 7.0.0-22 buyer-path signal. It shows another Strix Halo-class owner running the Qwen3.6 35B-A3B Ollama route with a modern kernel and Mesa stack.

It should not be treated as a speed headline or a regression against the guide's older Ollama rows yet. The report is a one-shot script result with a very short prompt-eval phase, 206 generated tokens, no raw CSV attachment yet, and incomplete backend/Vulkan ICD/repeat metadata.

The useful follow-up would be:

- exact `bench-ollama.sh`
- `ollama --version`
- `ollama ps` while the model is loaded
- `vulkaninfo --summary`
- Ollama service log line showing backend/device selection
- 5-10 warm repeats with the same script
- a direct `llama-bench -o csv` row if the contributor wants an apples-to-apples comparison later
