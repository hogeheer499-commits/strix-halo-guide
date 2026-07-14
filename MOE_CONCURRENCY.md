# AMD MoE Concurrency: Density-Gate Evidence

Status: measured first-party evidence on 2026-07-13; the Vulkan changes remain experimental and opt-in.

This page answers a practical server question:

> Why can aggregate decode throughput fall when a ninth concurrent MoE sequence is added on Strix Halo, and which backend or dispatch policy should a buyer use?

The short answer is that this is a fixable Vulkan dispatch problem, not a Strix Halo memory-capacity limit. Official `llama.cpp` b9979 still uses fixed eight-column thresholds. An AMD/RADV density gate removes most of the 8-to-9 cliff on both tested MoE shapes without changing concurrency 1-8. A separate dense threshold of 16 helps most at concurrency 9-12, but regresses the 30B and 80B rows at concurrency 16 versus the density gate alone, so it is not a universal default.

Do not compare these aggregate server numbers with direct single-stream `llama-bench` headlines. At concurrency 9, nine sequences contribute to the reported aggregate decode rate.

## What Was Tested

Hardware and workload:

- Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S, 128 GB unified memory
- Ubuntu 24.04, Mesa/RADV, `accelerator-performance`, explicit high GPU DPM during each measured run
- official `llama.cpp` b9979 source commit `4114ba18b208c2e9c1689a8316d410e649309dbc`
- `llama-batched-bench`, pp512/tg128 per sequence, Q4_0 KV, 65,536-token context
- each controlled run cooled below 50 C before measurement
- five repeats for 30B at concurrency 8/9/12/16; three repeats for 80B and Lemonade ROCm

Models:

| Model | Quant | Expert shape | Why it is here |
| --- | --- | --- | --- |
| Qwen3-Coder 30B-A3B | `UD-Q4_K_XL` | 128 experts, top-8 | Practical current coding route and a second expert shape. |
| Qwen3-Next 80B-A3B | `UD-Q4_K_XL` | 512 experts, top-10 | Matches the many-expert/top-10 topology at the center of upstream issue #25356, although it is not the exact artifact named there. |

Dispatch modes:

| Route | Meaning |
| --- | --- |
| Vulkan stock | Unmodified b9979 runtime behavior; fixed eight-token MMV thresholds. |
| Vulkan density | Opt-in `n_tokens * n_experts_used <= 2 * n_expert`, capped at 64 tokens. |
| Vulkan density + dense16 | Same expert density gate plus a separate ordinary dense MMV threshold of 16. |
| Lemonade ROCm | Existing optimized Lemonade `llamacpp-rocm` b1259 comparator; not a same-commit backend build. |

The patch is disabled by default. It is activated only with `GGML_VK_DENSITY_GATE=1`; dense16 additionally requires `GGML_VK_MMV_MAX_COLS=16`. This prevents the known NVIDIA-Vulkan regression from becoming a default behavior.

## Controlled Repeat Results

Aggregate decode tokens/s, mean with standard deviation in parentheses:

### Qwen3-Coder 30B-A3B

| Concurrency | Vulkan stock | Vulkan density | Density + dense16 | Lemonade ROCm |
| ---: | ---: | ---: | ---: | ---: |
| 8 | 228.18 (0.04) | 228.36 (0.21) | 228.11 (0.08) | 191.78 (0.38) |
| 9 | 147.19 (0.09) | 210.07 (0.08) | **234.12 (0.58)** | 200.89 (0.49) |
| 12 | 177.02 (0.08) | 236.70 (0.05) | **246.13 (0.76)** | 240.79 (1.10) |
| 16 | 212.66 (0.06) | 266.07 (0.17) | 227.20 (0.11) | **287.64 (0.84)** |

At concurrency 9, density improves stock by **42.7%** and density+dense16 by **59.1%**. The stock 8-to-9 drop is 35.5%; density reduces it to 8.0%, while density+dense16 removes it on this model. At concurrency 16, however, density alone is substantially better than dense16.

### Qwen3-Next 80B-A3B

| Concurrency | Vulkan stock | Vulkan density | Density + dense16 | Lemonade ROCm |
| ---: | ---: | ---: | ---: | ---: |
| 8 | 144.88 (0.24) | 145.02 (0.57) | 144.76 (0.35) | 112.19 (0.37) |
| 9 | 100.15 (0.13) | 125.48 (0.11) | **142.72 (0.30)** | 116.90 (0.36) |
| 12 | 113.26 (0.06) | 138.46 (0.24) | **144.97 (0.38)** | 130.50 (0.36) |
| 16 | 126.61 (0.12) | **150.82 (0.21)** | 131.08 (0.10) | 143.32 (0.39) |

At concurrency 9, density improves stock by **25.3%** and density+dense16 by **42.5%**. The stock 8-to-9 drop is 30.9%; density+dense16 reduces it to 1.4%. This independently confirms the issue on a 512-expert/top-10 model.

Charts:

- [`charts/moe_density_gate_30b.svg`](charts/moe_density_gate_30b.svg)
- [`charts/moe_density_gate_80b.svg`](charts/moe_density_gate_80b.svg)

## Practical Decision Table

| Workload | Start with | Reason |
| --- | --- | --- |
| One interactive user or up to eight parallel sequences | Stock Vulkan/RADV | The gate does not materially improve concurrency 1-8. Keep the simplest supported path. |
| Fixed concurrency around 9-12 and willing to run an experimental build | Density+dense16 | Best measured 9-12 aggregate throughput on both tested models. Do not generalize it to concurrency 16. |
| Variable concurrency around 9-16 | Density gate alone | Safer experimental compromise; large gains over stock without the dense16 regression at 16. |
| 30B service at 16 or more parallel sequences | Compare density Vulkan with Lemonade ROCm | ROCm wins this 30B matrix from concurrency 16 and remains strongest through most high-concurrency rows. |
| 80B service through concurrency 64 | Density Vulkan | This particular 80B model remained faster on tuned Vulkan than the older Lemonade b1259 comparator. |
| Beginner local chat | Ollama/Vulkan buyer path | This experiment is advanced server tuning, not a replacement for the setup script or beginner path. |

This is exactly why the guide should not say "ROCm always wins batching" or "Vulkan is always faster." The crossover depends on model topology and target concurrency.

## Correctness And Thermal Controls

- stock, density, and density+dense16 each passed **790/790** Vulkan `MUL_MAT_ID` backend tests
- stock and density+dense16 each passed **956/956** ordinary Vulkan `MUL_MAT` backend tests
- fixed-prompt, temperature-zero model output was text-identical across all three Vulkan modes
- controlled 30B repeats peaked at 86 C stock, 86 C density, 87 C density+dense16, and 79 C ROCm
- controlled 80B repeats peaked at 82 C stock, 80 C density, 81 C density+dense16, and 85 C ROCm

The telemetry field named PPT is `amdgpu` sysfs APU/GPU package telemetry. It is not wall power, so this page does not make wall-energy or efficiency claims.

## Vendor And Engineering Value

The important product conclusion is not merely that one benchmark became faster:

> A multi-user throughput bottleneck on Strix Halo can be reproduced, scoped to Vulkan dispatch behavior, corrected without harming low concurrency in the measured AMD routes, and translated into workload-specific buyer guidance.

That gives OEMs and AMD a concrete engineering question instead of a vague performance complaint. Useful next validation would be:

- a second Strix Halo system with firmware, fan profile, and chassis metadata
- AMD/RADV engineering review of a vendor-conditioned or runtime-tuned dispatch policy
- grouped/segmented `mul_mat_id` shader work that fills cooperative-matrix tiles instead of selecting between two incomplete paths
- same-commit Vulkan/HIP comparison to replace the older Lemonade comparator

Upstream issue: [`ggml-org/llama.cpp#25356`](https://github.com/ggml-org/llama.cpp/issues/25356).

## Evidence

- machine-readable detail: [`data/moe_density_gate.csv`](data/moe_density_gate.csv)
- repeat-aware summary: [`data/moe_density_gate_summary.csv`](data/moe_density_gate_summary.csv)
- raw logs, telemetry, patch, commands, correctness output, and host snapshot: [`data/raw/2026-07-13/llamacpp-b9979-amd-density-gate/`](data/raw/2026-07-13/llamacpp-b9979-amd-density-gate/)

Related practical pages:

- beginner setup: [`README.md#quick-start-6-steps`](README.md#quick-start-6-steps)
- workload recommendations: [`BEST_KNOWN_PROFILES.md`](BEST_KNOWN_PROFILES.md)
- current runtime and model status: [`CURRENT_MODELS.md`](CURRENT_MODELS.md)
