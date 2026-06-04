# LFM2.5 8B-A1B Q4_K_M Direct Scout

Purpose: test a recent practical small-MoE model on one Strix Halo / Ryzen AI MAX+ 395 system.

This is a current-model speed/coverage scout. It is not comparable to 30B-class Qwen MoE quality or capacity claims.

Host notes:

- Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S.
- normal workstation services were left running.
- This was a real-workstation scout, not a cold/clean isolated run.

Model:

```text
LiquidAI/LFM2.5-8B-A1B-GGUF
LFM2.5-8B-A1B-Q4_K_M.gguf
```

Observed by `llama-bench`:

```text
lfm2moe 8B.A1B Q4_K - Medium
model_size: 5147326208
model_n_params: 8467856832
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

| Shape | Result | Read |
| --- | ---: | --- |
| `pp512/tg128`, r5 | 1772.48 pp512 / 135.82 tg128 | Very fast small-MoE direct route. |
| `-p 0 -n 128`, r10 | 139.30 tg128 | Generation-only confirmation. |

Interpretation:

- LFM2.5 8B-A1B `Q4_K_M` runs very fast locally on Strix Halo via Vulkan/RADV.
- This is the strongest "new practical small model" speed result in this 2026-06-04 scan.
- It should be framed as a small-MoE speed/currentness result, not as a replacement for Qwen3-Coder 30B or larger current-model capability rows.
- This is direct `llama-bench`, not server/API/MTP/speculative decoding.

Source:

- <https://huggingface.co/LiquidAI/LFM2.5-8B-A1B-GGUF>
