# Qwen3-Coder 30B-A3B IQ4_XS Direct Scout

Purpose: test whether a popular `IQ4_XS` GGUF for the existing Qwen3-Coder 30B-A3B family can beat or replace the older direct 98.51 t/s `Q4_K_S` headline.

Host notes:

- Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S.
- T3 and Hermes were kept running.
- This was a real-workstation scout, not a cold/clean isolated run.

Model:

```text
unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF
Qwen3-Coder-30B-A3B-Instruct-IQ4_XS.gguf
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
| `pp512/tg128`, r5 | 1372.27 pp512 / 90.44 tg128 | Fast prompt processing, but clearly below the 98.51 t/s direct headline. |
| `-p 0 -n 128`, r10 | 90.72 tg128 | Generation-only check confirms this route is not a speed replacement. |

Interpretation:

- This route is a useful negative/control result.
- `IQ4_XS` alone is not enough to reproduce the 100+ t/s shape seen with `Qwen3-30B-A3B-Instruct-2507-IQ4_XS`.
- This is direct `llama-bench`, not MTP/server/speculative decoding.
