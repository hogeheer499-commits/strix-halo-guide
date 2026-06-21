---
license: apache-2.0
base_model: GestaltLabs/Qwen3.6-35B-A3B-NSC-ACE-SABER-GGUF-MTP
base_model_relation: quantized
language:
- en
library_name: llama.cpp
pipeline_tag: image-text-to-text
tags:
- qwen3.6
- qwen35moe
- 35b
- 35b-a3b
- 3b-active
- model-size-35b-a3b
- mixture-of-experts
- moe
- gguf
- mtp
- vision
- image-text-to-text
- llama.cpp
- rocm
- rocmfp4
- amd
- ryzen-ai-max-395
- strix-halo
- agentic-coding
- tool-calling
- nsc-ace
- saber
- ace-saber
---

![Chadrock 35B Ace Saber](assets/chadrock35b.png)

# New Chadrock v2 llama.cpp and config!

## Chadrock-35B Ace Saber ROCmFP4 MTP

Chadrock-35B Ace Saber is a ROCmFP4/MTP GGUF for AMD Ryzen AI Max+ 395 / Strix Halo systems. This release also includes a tested Qwen3.6 vision projector, so the same full Chadrock language GGUF can run image-text prompts when launched with `--mmproj`.

The model behavior comes from the Ace Saber build by **[@DJLougen](https://huggingface.co/GestaltLabs)**. The current speed numbers use the pinned Chadrock v2 ROCmFPX llama.cpp build from [`ciru-ai/ROCmFPX`](https://github.com/ciru-ai/ROCmFPX/tree/deaa996dab90b3ca6dd3ae5d453bedfcd983012d), with the request-level MTP controls described below.

This GGUF will **not run correctly with stock llama.cpp**. Use the pinned Chadrock v2 ROCmFPX runner because this file uses ROCmFP4 tensor types and MTP serving controls that upstream llama.cpp does not currently understand.

The model file is already provided here. You do **not** need to rebuild or quantize the model.

## Why This Mix

Ace Saber gives the model its coding, agentic, and tool-use behavior. Chadrock/ROCmFP4 gives it the speed profile needed to feel good locally on AMD unified-memory hardware.

The goal is not just another Qwen3.6 quant. The goal is:

- Ace Saber behavior from **@DJLougen**
- Qwen3.6 35B-A3B MoE efficiency
- MTP speculative decoding
- ROCmFP4 tensor-aware quantization
- high-throughput local serving on Ryzen AI Max+ 395 / Strix Halo

## Technical Metadata

Hugging Face may round the parsed GGUF tensor count to `36B` in its automatic badge. This release is the Qwen3.6 `35B-A3B` MoE family: about 35B-class total parameters with roughly 3B active parameters per token.

| Field | Value |
| --- | --- |
| model size | `35B-A3B` MoE |
| total parameters | `35B` class |
| active parameters | `~3B` class |
| architecture | `qwen35moe` |
| direct upstream GGUF | `GestaltLabs/Qwen3.6-35B-A3B-NSC-ACE-SABER-GGUF-MTP` |
| base family | `Qwen/Qwen3.6-35B-A3B` |
| local runtime format | ROCmFP4 Chadrock GGUF plus separate GGUF-format vision projector |

## Vision Support

Vision is provided by `mmproj-CHADROCK-35B-Ace-Saber-F32.mmproj`, a GGUF-format Qwen3VL projector converted from the restored Qwen3.6 visual tower sidecar in the upstream Ace Saber release.

This does **not** replace the language model and does **not** disable MTP. The validated command used the full Chadrock ROCmFP4 GGUF with native `--spec-type draft-mtp` enabled and added the projector with `--mmproj`.

Local validation used two generated images whose answers were not present in the prompt:

| Image gate | Expected | Result |
| --- | --- | --- |
| `gate_a.png` | `CIRU-742`, red square, blue circle | passed |
| `gate_b.png` | `HALO-319`, orange triangle, purple star | passed |

The same gate fails without a projector, so this is a real image-read check rather than a metadata-only claim.

## Chadrock v2 Speed

Best current text-only profile on AMD Ryzen AI Max+ 395 / Strix Halo: pinned Chadrock v2 ROCmFPX llama.cpp, Vulkan0 target plus Vulkan0 draft, f16/f16 target and draft KV, one slot, prompt cache disabled, no multimodal projector, deterministic decoding, and request policy `speculative.n_max=4`, `speculative.n_min=0`, `speculative.p_min=0.25`.

| Measurement | Prompt tokens | Generated tokens | Decode tok/s | Prefill tok/s | Total time | Draft accepted |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Chadrock v2 best, gen512 | `3,946` | `512` | `143.08` | `1072.34` | `7.26 s` | `408 / 408` |
| Chadrock v2 repeat, gen2048 | `3,946` | `2048` | `141.77` | `1064.16` | `18.16 s` | `1637 / 1637` |
| Same-run no-draft control, gen512 | `3,946` | `512` | `72.57` | `1064.49` | `10.77 s` | `0 / 0` |
| Same-run no-draft control, gen2048 | `3,946` | `2048` | `72.04` | `1067.18` | `32.13 s` | `0 / 0` |

Against the same-run no-draft control, the new Chadrock v2 MTP config is `1.97x` faster in decode at both gen512 and gen2048: `143.08` vs `72.57 tok/s`, and `141.77` vs `72.04 tok/s`.

Compared with the older Chadrock v1 card-speed profile (`~101.31 tok/s` aggregate HumanEval eval speed), the new best served text row is about `1.41x` faster (`+41.2%`). Compared with the older uncached Chadrock TG64 served row (`78.28 tok/s` server eval), the new gen2048 row is about `1.81x` faster (`+81.1%`). Those older rows are not identical prompts, so treat them as release-to-release runner evidence rather than a strict apples-to-apples benchmark pair.

The older 2026-06-07 HumanEval rerun is still useful as a quality guard: it generated `48,824` completion tokens across `164` tasks at `~101.31 tok/s` aggregate llama-server eval speed and produced the `155/164` base pass@1 and `148/164` HumanEval+ pass@1 result below.

## HumanEval

This model also posts an exceptional HumanEval result for a local GGUF run:

| Model / row | HumanEval base pass@1 | HumanEval+ pass@1 |
| --- | ---: | ---: |
| Chadrock-35B Ace Saber ROCmFP4, 32k Vulkan d2 rerun | `155/164 = 94.51%` | `148/164 = 90.24%` |
| earlier Chadrock-35B Ace Saber ROCmFP4 run | `157/164 = 95.73%` | `149/164 = 90.85%` |
| recorded stock Qwen3.6-27B UD-Q8_K_XL | `154/164 = 93.90%` | `149/164 = 90.85%` |

The fresh 32k rerun still beats the recorded stock 27B row on base HumanEval, while the older row remains one task higher on HumanEval+.

## BigCodeBench-Hard

The same tuned Chadrock Vulkan d2 family was also run on BigCodeBench-Hard-Instruct:

| Benchmark | Result |
| --- | ---: |
| BigCodeBench-Hard-Instruct pass@1 | `47/148 = 31.76%` |
| generation wall time | `799 s` |
| aggregate prompt speed | `~624.06 tok/s` |
| aggregate generation speed | `~100.12 tok/s` |

This is a harder instruction-coding benchmark than HumanEval and is included as a sanity check that the speed-tuned runtime still produces usable code under a broader task mix.

## Best Settings / Advanced Setup

For the pinned runner build, copy-paste build commands, request-level speculative controls, and the 35B/27B reproduction notes, use the advanced Ciru setup page:

**https://llm.ciru.ai/chadrock-rocmfpx/**

The current pinned score build is:

```text
ciru-ai/ROCmFPX tag: chadrock-rocmfp4-mtp-scores-20260621
commit: deaa996dab90b3ca6dd3ae5d453bedfcd983012d
```

For the fastest measured text-only ACE/SABER path on Strix Halo, use:

```text
backend: Vulkan0 target + Vulkan0 draft
context: 32768
batch / ubatch: 2048 / 512
target KV: f16 / f16
draft KV: f16 / f16
MTP: draft-mtp, n_max=4, n_min=0, p_min=0.25, p_split=0.10
serving: one slot, prompt cache disabled for benchmarks, --no-mmproj for text speed
sampler: temperature=0, top_p=0.95, top_k=20
```

That is the profile that produced `143.08 tok/s` at gen512 and repeated at
`141.77 tok/s` at gen2048 on the 3946-token text prompt. For image-text use,
remove `--no-mmproj` and add `--mmproj mmproj-CHADROCK-35B-Ace-Saber-F32.mmproj`;
the headline speed row above is text-only.

## Run With llama-server

Build the pinned Chadrock v2 ROCmFPX llama.cpp once, download this GGUF, then run this text-speed profile from the ROCmFPX checkout:

```bash
./build-strix-rocmfp4/bin/llama-server \
  -m /path/to/Qwen3.6-35B-A3B-NSC-ACE-SABER-MTP-F16-to-ROCmFP4-STRIX_LEAN.gguf \
  --alias chadrock-35b-ace-saber-rocmfp4-cap4 \
  --host 127.0.0.1 \
  --port 18180 \
  --jinja \
  -c 32768 \
  --reasoning off \
  --reasoning-format none \
  --reasoning-budget -1 \
  --no-context-shift \
  -dev Vulkan0 \
  -ngl 999 \
  -fa on \
  -b 2048 \
  -ub 512 \
  -t 16 \
  -tb 32 \
  -ctk f16 \
  -ctv f16 \
  --temp 0 \
  --top-p 0.95 \
  --top-k 20 \
  --seed 123 \
  --parallel 1 \
  --no-mmproj \
  --metrics \
  --no-webui \
  --no-cache-prompt \
  --cache-ram 0 \
  --slot-prompt-similarity 0.0 \
  --spec-type draft-mtp \
  --spec-draft-device Vulkan0 \
  --spec-draft-ngl all \
  --spec-draft-threads 16 \
  --spec-draft-threads-batch 32 \
  --spec-draft-type-k f16 \
  --spec-draft-type-v f16 \
  --spec-draft-n-max 4 \
  --spec-draft-n-min 0 \
  --spec-draft-p-min 0.25 \
  --spec-draft-p-split 0.10 \
  --no-spec-draft-backend-sampling \
  --spec-draft-poll 1 \
  --spec-draft-poll-batch 1
```

Use `--parallel 1` for MTP. Multi-slot serving changes the MTP behavior and is not the intended profile.
The benchmark table above used `-c 32768` and `--no-mmproj` for the fastest text row. For image-text use, remove `--no-mmproj` and add the projector:

```bash
--mmproj /path/to/mmproj-CHADROCK-35B-Ace-Saber-F32.mmproj
```
