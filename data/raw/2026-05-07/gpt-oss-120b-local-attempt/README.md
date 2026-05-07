# gpt-oss-120b local attempt
2026-05-07T05:02:41+02:00
Repo: ggml-org/gpt-oss-120b-GGUF
Files: gpt-oss-120b-mxfp4-00001/00002/00003-of-00003.gguf
Purpose: local Strix Halo llama.cpp Vulkan benchmark attempt.

Result: loaded and benchmarked locally with llama.cpp b9049 Vulkan/RADV.

| Workload | Result | Raw CSV |
|----------|-------:|---------|
| pp512 | 725.03 t/s | `gpt-oss-120b-mxfp4-b9049-vulkan-pp512-r3.csv` |
| pp2048 | 707.29 t/s | `gpt-oss-120b-mxfp4-b9049-vulkan-pp2048-r3.csv` |
| tg32 | 51.02 t/s | `gpt-oss-120b-mxfp4-b9049-vulkan-tg32-r3.csv` |
| tg128 | 50.59 t/s | `gpt-oss-120b-mxfp4-b9049-vulkan-tg128-r3.csv` |

The first tg32 attempt was aborted by the benchmark guard because swap-free dipped below 2 GiB. Swap was cleared with enough free memory available, then tg32/tg128 completed while the protected workstation dependency stayed healthy. Treat this as performance evidence only, not a model-quality evaluation.
