# Nemotron 3 Super 120B-A12B UD-IQ4_XS Direct Scout

Purpose: answer the Nemotron family gap after the Nemotron 3 Ultra release and the Nano 30B-A3B scout.

This is not a Nemotron 3 Ultra 550B benchmark. Ultra BF16/NVFP4 artifacts are too large for one 128 GB Strix Halo system and were not found as a direct GGUF/`llama.cpp` route during the scan. Nemotron 3 Super is the practical middle target between Ultra and Nano.

Host notes:

- Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S.
- normal workstation services were left running.
- This was a real-workstation scout, not a cold/clean isolated run.

Model:

```text
unsloth/NVIDIA-Nemotron-3-Super-120B-A12B-GGUF
UD-IQ4_XS/NVIDIA-Nemotron-3-Super-120B-A12B-UD-IQ4_XS-00001-of-00003.gguf
```

Observed by `llama-bench`:

```text
nemotron_h_moe 120B.A12B IQ4_XS - 4.25 bpw
model_size: 64476770304
model_n_params: 120668707840
```

Downloaded GGUF shards:

```text
00001-of-00003: 7.9 MB
00002-of-00003: 49.6 GB
00003-of-00003: 14.9 GB
```

Build:

```text
llama.cpp 1fd5f4803713 / b9453-14-g1fd5f4803
Vulkan/RADV
```

Device line:

```text
Radeon 8060S Graphics (RADV_STRIX_HALO), int dot: 1, matrix cores: KHR_coopmat
```

Results:

| Shape | Result | Read |
| --- | ---: | --- |
| `-p 0 -n 32`, r1 | 17.07 tg32 | Smoke/load proof. |
| `pp512/tg128`, r3 | 292.51 pp512 / 17.94 tg128 | Standard direct `llama-bench` scout shape. |
| `-p 0 -n 128`, r3 | 17.73 tg128 | Generation-only confirmation. |

Interpretation:

- Nemotron 3 Super 120B-A12B `UD-IQ4_XS` runs directly on Strix Halo via `llama.cpp` Vulkan/RADV.
- This is the practical missing middle between Nemotron 3 Ultra and Nemotron 3 Nano.
- The value is capacity/current-model feasibility, not speed.
- This is direct `llama-bench`, not server/API/MTP/speculative decoding.

Source:

- <https://huggingface.co/unsloth/NVIDIA-Nemotron-3-Super-120B-A12B-GGUF>
