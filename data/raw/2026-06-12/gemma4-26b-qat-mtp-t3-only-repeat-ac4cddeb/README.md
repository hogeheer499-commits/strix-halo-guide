# Gemma 4 26B-A4B QAT MTP T3-only repeat

Repeat of the Gemma 4 26B-A4B QAT matched-head MTP route after stopping known nonessential local workload while leaving T3 running.

Host handling before the run:

- T3 was left running.
- Hermes was stopped temporarily.
- Railway was not touched; no Railway process was visible in the process scan.
- `docflock-backend.service`, its ffmpeg virtual-camera workload, Ollama, RustDesk, and the `ubuntu-zoom` VM were stopped before the run.
- Browser-like processes were allowed to be stopped if present.

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
| T3-only repeat | 107.42 t/s | 91.30-124.71 | 0.68167 | Six prompts, 192 predicted tokens each. |

This repeat explains the gap between the earlier 102.69 t/s cold repeat and the previous 110.00 t/s best repeat. The route did not change; the host workload did.

This is server/speculative evidence, not a direct `llama-bench` result.
