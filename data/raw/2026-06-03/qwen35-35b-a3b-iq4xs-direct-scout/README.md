# Qwen3.5 35B-A3B IQ4_XS Direct Scout

Purpose: test whether a newer, popular Qwen 35B-A3B route can approach or beat the older Qwen3-Coder 30B 98.51 t/s direct speed headline.

Host notes:

- Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S.
- T3 and Hermes were kept running.
- This was a real-workstation scout, not a cold/clean isolated run.

Model:

```text
bartowski/Qwen_Qwen3.5-35B-A3B-GGUF
Qwen_Qwen3.5-35B-A3B-IQ4_XS.gguf
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
| `pp512/tg128`, r5 | 1170.27 pp512 / 75.22 tg128 | Modern Qwen 35B-A3B route, but far below the 98.51 t/s direct speed headline. |
| `-p 0 -n 128`, r10 | 75.53 tg128 | Generation-only check confirms it is not a speed replacement. |

Interpretation:

- This is a useful modern-model negative/control result.
- Newer or larger Qwen MoE routes do not automatically inherit the 30B-A3B 98-100 t/s speed shape.
- This is direct `llama-bench`, not MTP/server/speculative decoding.
