# Nemotron Labs Audex 30B-A3B Text-Only MXFP4 Scout

Date: 2026-07-16

System: Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S, 128 GB
unified memory.

This scout verifies the portable language-model portion of NVIDIA Audex. It
does not test or imply support for the complete audio pipeline.

## Reproducibility Pin

- runtime: official `llama.cpp` b10034, commit `505b1ed15`
- backend: Vulkan/RADV, full GPU offload
- model: `audex-30b-a3b-textonly-MXFP4_MOE.gguf`
- quant source: `LordNeel/Nemotron-Labs-Audex-30B-A3B-GGUF`
- quant source revision: `9b6a8d234a69affcdefc3639a2852c3b81e5c3d2`
- model SHA-256: `4ce4fd5cc8408b71f5b0f1c055d1fc20b87dd36db2449618f818e90b0c4f7477`

## Result

| Test | Result |
| --- | ---: |
| `pp512` | 1318.50 t/s |
| `tg128` | **60.73 t/s** |
| text correctness smoke | pass: `9` |

The 17.97 GB text-only MXFP4 artifact loads and generates cleanly on the
current Vulkan runtime. It answered the small sheep puzzle correctly and
identified itself as a text-only model.

The Audex release keeps audio encoder/vocoder assets and NVIDIA HF/vLLM
inference scripts in an additional approximately 7.67 GB sidecar. The source
card explicitly states that `llama.cpp` does not package the complete audio
pipeline as one all-in-one GGUF runtime. Therefore this result is language
support evidence only: it does not prove audio QA, audio generation, TTS, or
speech-to-speech on AMD.

Audex is released under the NVIDIA OneWay Noncommercial license. That limits
its usefulness for commercial buyer or vendor workflows even though the text
route is technically runnable.

## Evidence

- [`llama-bench.csv`](llama-bench.csv): direct language benchmark
- [`text-smoke-output.txt`](text-smoke-output.txt): complete correctness output
- [`run-scout.sh`](run-scout.sh): exact runner
- [`host-snapshot.txt`](host-snapshot.txt): host and Vulkan context
- [`model.sha256`](model.sha256): exact model identity

The first text-smoke command used a `llama-bench`-only `-mmp` option with
`llama-cli`. The corrected published runner removes that flag. This was a
harness error, not a model or backend failure.
