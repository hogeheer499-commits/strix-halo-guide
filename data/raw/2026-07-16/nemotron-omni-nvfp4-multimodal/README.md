# Nemotron 3 Nano Omni NVFP4 Multimodal Scout

Date: 2026-07-16

System: Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S, 128 GB
unified memory.

This scout tests both the language GGUF and the separate vision projector. It
is the first first-party run in this guide that validates the current Nemotron
Omni route as multimodal rather than only benchmarking its language model.

## Reproducibility Pin

- runtime: official `llama.cpp` b10034, commit `505b1ed15`
- backend: Vulkan/RADV, full GPU offload
- model: `nemotron-3-30b-NVFP4.gguf`
- projector: `mmproj-nemotron-3-30b-f16.gguf`
- quant source: `FreedomAISVR/Nemotron-3-30B-Nano-Omni-NVFP4-GGUF`
- quant source revision: `478af95c5ec29613dfa0bd28b5f47249ac9e2391`
- model SHA-256: `d29e2f057c71cab73581e1a79e54064921d06f5a3ee7c3798d0d00fd6adbca1e`
- projector SHA-256: `acea9c11e2150a1690b5a65e04081c11f48fafc30da8c4d8344ae1fa1baa5b68`

## Result

| Test | Result |
| --- | ---: |
| `pp512` | 1143.91 t/s |
| `tg128` | **53.21 t/s** |
| image OCR smoke | pass: `STRIX 395` |

The 19.25 GB NVFP4 language model and 1.59 GB F16 projector load cleanly with
the experimental `llama-mtmd-cli`. The model correctly read the large black
text `STRIX 395` from the generated PNG while both the language model and
projector used the current Vulkan path.

The existing MXFP4 language-only artifact measured 64.26 t/s on the same
b10034 runtime, so NVFP4 is not the faster language route in this comparison.
Its value is a working image-capable path. This small OCR check does not prove
audio/video quality, broad vision accuracy, or production readiness of the
experimental multimodal CLI.

## Evidence

- [`llama-bench.csv`](llama-bench.csv): direct language benchmark
- [`vision-test.png`](vision-test.png): generated OCR input
- [`vision-output.txt`](vision-output.txt): complete multimodal response
- [`vision-stderr.txt`](vision-stderr.txt): projector initialization and image encoding
- [`run-scout.sh`](run-scout.sh): exact runner
- [`host-snapshot.txt`](host-snapshot.txt): host and Vulkan context
- [`model.sha256`](model.sha256) and [`mmproj.sha256`](mmproj.sha256): exact artifact identities
- [`quant-card.md`](quant-card.md): source metadata captured at test time

This is first-party multimodal compatibility evidence, not a replacement for
the direct Qwen speed headlines or the beginner Ollama buyer path.
