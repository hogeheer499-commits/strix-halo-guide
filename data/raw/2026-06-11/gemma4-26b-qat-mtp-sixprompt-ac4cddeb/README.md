# Gemma 4 26B-A4B QAT MTP six-prompt route

First-party Beelink GTR9 Pro `llama-server` route on `llama.cpp` ac4cddeb0 build 9592 with Vulkan/RADV.

This is server/speculative decoding evidence, not a direct `llama-bench` result.

Main model:

- `gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf`

Draft model:

- `MTP/gemma-4-26B-A4B-it-Q4_0-MTP.gguf`

Best tested flags:

```bash
-ngl 999 -fa on --no-mmap --cache-ram 0 \
-c 4096 -np 1 -b 2048 -ub 512 --poll 50 \
--spec-type draft-mtp --spec-draft-n-max 3
```

| Run | Mean | Range | Acceptance | Notes |
| --- | ---: | ---: | ---: | --- |
| no-spec baseline | 73.96 t/s | 73.63-74.13 | n/a | Same six prompts, no speculative decoding. |
| MTP draft-n=2 | 106.88 t/s | 92.91-119.08 | 0.7385 | First matched-head pass. |
| MTP draft-n=3 sweep | 109.98 t/s | 93.62-126.39 | 0.6817 | Best sweep setting before repeat. |
| MTP draft-n=3 repeat | 110.00 t/s | 93.57-127.33 | 0.6817 | Best repeat-confirmed average. |

Use the 110.00 t/s row as a best-repeat server result, not as a cold-clean guarantee or direct benchmark.
