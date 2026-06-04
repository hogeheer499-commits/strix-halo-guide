# Gemma 4 12B IT Direct Scout

Purpose: test Google's new Gemma 4 12B IT GGUF route on one Strix Halo / Ryzen AI MAX+ 395 system.

This is a current-model relevance test, not a speed-record attempt.

Host notes:

- Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S.
- normal workstation services were left running.
- This was a real-workstation scout, not a cold/clean isolated run.

Model sources:

```text
ggml-org/gemma-4-12B-it-GGUF
gemma-4-12B-it-Q4_K_M.gguf

unsloth/gemma-4-12b-it-GGUF
gemma-4-12b-it-IQ4_XS.gguf
```

Build:

```text
llama.cpp 1fd5f4803713 / b9453-14-g1fd5f4803
Vulkan/RADV
```

Device line:

```text
Radeon 8060S Graphics (RADV_STRIX_HALO), int dot: 0, matrix cores: KHR_coopmat
```

Results:

| Model / quant | Shape | Result | Read |
| --- | --- | ---: | --- |
| Gemma 4 12B IT `Q4_K_M` | `pp512/tg128`, r5 | 684.92 pp512 / 24.42 tg128 | Balanced GGUF route. |
| Gemma 4 12B IT `Q4_K_M` | `-p 0 -n 128`, r10 | 24.42 tg128 | Generation-only confirmation. |
| Gemma 4 12B IT `IQ4_XS` | `pp512/tg128`, r5 | 680.17 pp512 / 25.74 tg128 | Smaller/speed-leaning route. |
| Gemma 4 12B IT `IQ4_XS` | `-p 0 -n 128`, r10 | 25.77 tg128 | Generation-only confirmation. |

Interpretation:

- Gemma 4 12B IT works directly with `llama-bench` on Strix Halo Vulkan/RADV.
- The useful public framing is current-model coverage: Google's newly released local multimodal model runs locally on Strix Halo.
- It is not a speed challenger for Qwen MoE rows. Generation is around 24-26 t/s in this direct route, far below the 98.5-100 t/s Qwen 30B-class speed rows.
- `IQ4_XS` is only modestly faster than `Q4_K_M` here.
- This is direct `llama-bench`, not server/API/MTP/speculative decoding.

Source checks:

- Google announcement: <https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12b/>
- GGUF source: <https://huggingface.co/ggml-org/gemma-4-12B-it-GGUF>
- GGUF source: <https://huggingface.co/unsloth/gemma-4-12b-it-GGUF>
