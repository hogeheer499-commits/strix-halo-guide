# Qwen3 30B-A3B NEO-MAX IQ4_XS Direct Scout

Purpose: test whether an alternate imatrix-tuned Qwen3 30B-A3B `IQ4_XS` route can reproduce the 100+ t/s direct shape seen with `Qwen3-30B-A3B-Instruct-2507-IQ4_XS`.

Host notes:

- Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S.
- T3 and Hermes were kept running.
- This was a real-workstation scout, not a cold/clean isolated run.

Model:

```text
DavidAU/Qwen3-128k-30B-A3B-NEO-MAX-Imatrix-gguf
Qwen3-128k-30BA3B-NEO-MAX-PLUS-IQ4_XS.gguf
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
| `pp512/tg128`, r5 | 1396.05 pp512 / 87.39 tg128 | Good prompt processing, but decode is clearly below the 98.51 t/s direct headline. |
| `-p 0 -n 128`, r10 | 87.77 tg128 | Generation-only check confirms this route is not a speed replacement. |

Interpretation:

- This is a useful alternate-30B negative/control result.
- The direct 100+ t/s result from the 2507 `IQ4_XS` scout does not generalize to every 30B-A3B `IQ4_XS` file.
- This is direct `llama-bench`, not MTP/server/speculative decoding.
