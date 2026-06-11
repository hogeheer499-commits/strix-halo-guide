# Gemma 4 26B-A4B QAT MTP cold repeat

Cold repeat of the 2026-06-11 Gemma 4 26B-A4B QAT matched-head MTP route.

Host handling before the run:

- T3 was left running.
- Hermes was left untouched.
- Nonessential local docflock backend and `ubuntu-zoom` VM were stopped and restored after the run.
- Root Ollama service was idle and left untouched.

Route:

- `llama.cpp` ac4cddeb0 build 9592
- `llama-server` Vulkan/RADV
- main model: `gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf`
- draft model: `MTP/gemma-4-26B-A4B-it-Q4_0-MTP.gguf`
- `--spec-type draft-mtp --spec-draft-n-max 3`
- `-c 4096 -np 1 -b 2048 -ub 512 --poll 50`

Result:

| Run | Mean | Range | Acceptance | Notes |
| --- | ---: | ---: | ---: | --- |
| cold repeat | 102.69 t/s | 86.76-118.77 | 0.6817 | Six prompts, 192 predicted tokens each. |

This confirms the route remains in the 100+ t/s server class, but the lower cold repeat is the reason the public claim should be framed as `102.7 t/s cold / 110.0 t/s best-repeat`, not just `110 t/s`.
