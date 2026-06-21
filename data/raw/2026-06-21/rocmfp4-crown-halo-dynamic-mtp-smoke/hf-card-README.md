---
license: apache-2.0
base_model: unsloth/Qwen3.6-35B-A3B-MTP-GGUF
base_model_relation: quantized
library_name: llama.cpp
tags:
  - gguf
  - qwen
  - qwen3.6
  - qwen35moe
  - 35b
  - 35b-a3b
  - 3b-active
  - model-size-35b-a3b
  - mtp
  - llama.cpp
  - quantized
  - moe
  - mixture-of-experts
  - strix-halo
  - vulkan
  - vision
  - multimodal
  - image-text-to-text
language:
  - en
pipeline_tag: image-text-to-text
---

# Qwen3.6 35B A3B Crown Halo Dynamic MTP v7 GGUF

![Strix Halo local serving](assets/strixhalo.png)

Crown Dynamic MTP v7 is a custom mixed-precision GGUF quantization of `unsloth/Qwen3.6-35B-A3B-MTP-GGUF`, tuned for local AMD Strix Halo serving with `llama.cpp` native MTP speculative decoding.

This is not a generic cloud inference recipe. It is a Strix Halo owner profile: single-user, high-context, Vulkan, native MTP, split mode none, flash attention, vision projector support, and polling settings chosen for this machine class.

## File

| file | size | sha256 |
|---|---:|---|
| `Qwen3.6-35B-A3B-HaloStrix-Dyn-MTP-v7.gguf` | 21.03 GiB | `342e3ee059792dbcba016dc3274a2de73a2372c0ea300a8e56aa615190f58ba9` |
| `mmproj-F16.mmproj` | 858 MB | `8971ee4f331ff0a4c609374f32984b3d4e6dc086c0aa35f1d637fad1829e887f` |

`mmproj-F16.mmproj` is the Qwen3.6 35B A3B GGUF-format vision projector. It is stored with a `.mmproj` repo extension so Hugging Face's GGUF parser keeps the main card focused on the 35B language model rather than the smaller projector.

## Technical Metadata

Hugging Face may round the parsed GGUF tensor count to `36B` in its automatic badge. This release is the Qwen3.6 `35B-A3B` MoE family: about 35B-class total parameters with roughly 3B active parameters per token.

| Field | Value |
| --- | --- |
| model size | `35B-A3B` MoE |
| total parameters | `35B` class |
| active parameters | `~3B` class |
| architecture | `qwen35moe` |
| GGUF size label | `35B-A3B` |
| direct upstream GGUF | `unsloth/Qwen3.6-35B-A3B-MTP-GGUF` |
| base family | `Qwen/Qwen3.6-35B-A3B` |
| local runtime format | mixed-precision Vulkan GGUF |
| vision projector | `mmproj-F16.mmproj` |

## What This Is

Crown v7 is not a renamed upstream quant. It uses a custom mixed-precision tensor recipe:

- `MXFP4` on blocks 0-27 routed expert gate/up tensors
- `Q4_K_M` fallback on blocks 28-35 routed expert gate/up tensors
- `Q5_K` on blocks 36-39 routed expert gate/up tensors
- `Q5_K` / `Q6_K` for routed down experts
- `Q8_0` for attention, shared experts, token embeddings, output, and selected MTP tensors

The full recipe is included in `recipes/halo-mtp-dyn-v7.md` and `recipes/halo-mtp-dyn-v7.tensor-types.txt`.

## Strix Halo Serving Profile

Reference profile:

- AMD Ryzen AI MAX / Radeon 8060S Strix Halo class machine
- Vulkan `llama.cpp` build with Qwen MTP support
- 128 GB unified memory
- single-slot serving because MTP is the constraint
- 131072 context
- split mode none
- flash attention enabled
- native MTP speculative decoding
- Qwen3.6 35B A3B vision projector enabled

Primary Strix/MTP/vision showcase command:

```bash
llama-server \
  -m Qwen3.6-35B-A3B-HaloStrix-Dyn-MTP-v7.gguf \
  --alias crown-dynamic-mtp \
  --host 127.0.0.1 \
  --port 18181 \
  --jinja \
  -c 131072 \
  --reasoning off \
  --reasoning-format none \
  --reasoning-budget -1 \
  --no-context-shift \
  -sm none \
  -ngl 999 \
  -fa on \
  -b 2048 \
  -ub 512 \
  -t 16 \
  -ctk f16 \
  -ctv f16 \
  --spec-draft-type-k f16 \
  --spec-draft-type-v f16 \
  --parallel 1 \
  --metrics \
  --mmproj mmproj-F16.mmproj \
  --spec-type mtp \
  --spec-draft-n-max 4 \
  --poll 100 \
  --poll-batch 1 \
  --spec-draft-poll 1 \
  --spec-draft-poll-batch 1 \
  --temp 0.6 \
  --min-p 0.0 \
  --top-p 0.95 \
  --top-k 20 \
  --repeat-penalty 1.0
```

The exact public Strix profile is included as `model-profiles/qwen3.6-35b-a3b-crown-halo-mtp-dynamic.env`, and the serving script is included as `scripts/serve_halo_mtp_dyn_v7.sh`.

For text-only use, you may omit `--mmproj`. For image input, keep `mmproj-F16.mmproj` next to the main GGUF and pass it with `--mmproj`.

### KV Cache Choice

Use `f16` target KV and `f16` draft KV with `b2048/u512`.

Older local comparison rows included `q8_0/q8_0` KV, but that is not the public Strix Halo recommendation for this release. The benchmark story and serving recipe are centered on the `f16/f16` MTP profile.

## Where It Shines On Strix Halo

The point of this release is native MTP behavior under compatible `llama.cpp` serving. It shines when the MTP head gets accepted at a high rate, especially structured or repetitive long-decode workloads.

On structured 4k-token prompt / 256-token generation tests:

| setting | workload | generation tok/s | MTP acceptance | accepted / drafted |
|---|---|---:|---:|---:|
| MTP depth 4, b2048/u512, f16 KV | JSON | 105.79 | 97.6% | 203 / 208 |
| MTP depth 4, b2048/u512, f16 KV | code | 106.13 | 99.5% | 203 / 204 |
| MTP depth 4, b2048/u512, f16 KV | chat | 104.67 | 97.6% | 203 / 208 |
| MTP depth 4, b2048/u512, f16 KV | tool-call JSON | 104.97 | 97.6% | 203 / 208 |
| MTP depth 2, b2048/u512, f16 KV | JSON | 91.08 | 100.0% | 170 / 170 |
| MTP depth 2, b2048/u512, f16 KV | code | 90.59 | 100.0% | 170 / 170 |
| MTP depth 2, b2048/u512, f16 KV | chat | 90.07 | 100.0% | 170 / 170 |
| MTP depth 2, b2048/u512, f16 KV | tool-call JSON | 90.60 | 100.0% | 170 / 170 |

Best observed structured-decode slice: **MTP depth 4**, roughly **105-106 tok/s** with **97-99% draft-token acceptance**.

A separate context sweep found a strong mid-context decode row:

| context | setting | prompt tokens | generated | generation tok/s | MTP acceptance |
|---|---|---:|---:|---:|---:|
| 32k | MTP depth 4 | 20,263 | 128 | 79.58 | 86.0% |
| 32k | MTP depth 2 | 20,263 | 128 | 59.74 | 66.1% |

## Vision Smoke Test

Vision was validated locally on June 15, 2026 with the normal Crown Dynamic profile, the `mmproj-F16` projector, and native MTP enabled. Test image:

`/srv/desktop-data/cirudata/ciruoutfit.png`

Prompt:

> Look at this image. In one short sentence, name the dominant hair color and the object covering the character's ear.

Response:

> The dominant hair color is green, and the object covering the character's ear is a cybernetic headset.

The OpenAI-compatible llama.cpp response included MTP draft timing fields: `draft_n=24` and `draft_n_accepted=19`.

## Strix Owner Notes

- `--parallel 1` is intentional. MTP is the constraint, and this profile is for single-user local serving.
- `-c 131072` is intentional. This release is focused on high-context Strix Halo use.
- Use `--spec-type mtp`; plain GGUF loading will not show the behavior this model was built for.
- Use the polling settings from the profile: `--poll 100`, `--poll-batch 1`, `--spec-draft-poll 1`, and `--spec-draft-poll-batch 1`.
- `b2048/u512` is the recommended Strix MTP default from the acceptance matrix; larger `b8192/u512` did not improve acceptance and added latency.
- `f16/f16` KV is the recommended MTP setting for Strix Halo.
- Use `--mmproj mmproj-F16.mmproj` for image input. Omit it only for text-only serving.

## Important Benchmark Caveat

This is not a universal "always faster" GGUF.

In ordinary non-speculative `llama-bench`, Crown v7 looks similar to other strong Qwen3.6 35B A3B quants. The point of this release is the MTP behavior under compatible Strix Halo `llama.cpp` serving, not raw no-speculative token generation.

Local context-sweep testing showed:

- MTP helped most on structured/repetitive decode workloads with high draft acceptance.
- MTP depth 4 was the strongest tested setting for structured decode.
- Very long active contexts, especially around 64k, did not show an end-to-end MTP win on this Vulkan host.
- If you run this as a normal GGUF without MTP support, expect a strong Q4-size mixed quant, not the accelerated MTP profile.

## Provenance

Base/source repo: `unsloth/Qwen3.6-35B-A3B-MTP-GGUF`

Quantization recipe used BF16 split GGUF shards and `imatrix_unsloth.gguf_file` from the upstream Unsloth release.

Recipe checksums:

- `recipes/halo-mtp-dyn-v7.md`: `9b56f075cbd5cc225c28ae7022c6c0e04beafeec6fa275f50aef4c0d1d2f46cc`
- `recipes/halo-mtp-dyn-v7.tensor-types.txt`: `d827103057fb485db6c4e7116bdb3658a50b48a79c915431f18188bb647d2375`
