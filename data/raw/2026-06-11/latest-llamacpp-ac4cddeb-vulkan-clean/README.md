# 2026-06-11 latest llama.cpp ac4cddeb0 Vulkan/RADV controls

First-party Beelink GTR9 Pro controls on `llama.cpp` ac4cddeb0 build 9592 with Vulkan/RADV and explicit `Vulkan0`.

These are direct `llama-bench` rows unless noted otherwise. They are latest-stack controls, not a replacement for the older strict-clean Qwen3-Coder b9179 headline.

| Model | Quant | Result | Read |
| --- | --- | ---: | --- |
| Qwen3-30B-A3B-Instruct-2507 | `IQ4_XS` | 1430.65 pp512 / 100.38 tg128 | Direct 30B-class Qwen route still above 100 t/s. |
| Qwen3-Coder 30B-A3B | `Q4_K_S` | 1395.99 pp512 / 94.20 tg128 | Latest-stack control below the older 98.51 t/s strict-clean headline. |
| LFM2.5 8B-A1B | `Q4_K_M` | 3363.94 pp512 / 171.17 tg128 | Small-MoE speed route still in the 170 t/s class. |
| Gemma 4 12B IT QAT | `UD-Q4_K_XL` | 816.32 pp512 / 29.34 tg128 | Current Google QAT direct row. |
| Gemma 4 26B-A4B IT QAT | `UD-Q4_K_XL` | 1431.96 pp512 / 74.80 tg128 | Direct baseline for the Gemma MTP server route. |
| Nemotron 3 Super 120B-A12B | `UD-IQ4_XS` | 296.26 pp512 / 18.24 tg128 | 120B-class capacity route still direct-runnable. |
| Qwen3.6 27B MTP NVFP4 v3 | `NVFP4` | 373.97 pp512 / 13.17 tg128 | Newer artifact runs, but remains a negative speed route. |
| DeepSeek V4 Flash Spark-Mini | `Q2-REAP` | failed to load | Loadability/setup-friction evidence, not a performance result. |

Server smoke logs in this directory are exploratory single-prompt checks. The six-prompt Gemma MTP route is stored separately in `../gemma4-26b-qat-mtp-sixprompt-ac4cddeb/`.
