# Nemotron 3 Nano 30B-A3B IQ4_XS Direct Scout

Purpose: provide a practical NVIDIA Nemotron local benchmark route after the Nemotron 3 Ultra release.

This is not a Nemotron 3 Ultra 550B benchmark. Ultra BF16/NVFP4 artifacts are too large for one 128 GB Strix Halo system and were not found as a direct GGUF/`llama.cpp` route during the scan.

Host notes:

- Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S.
- normal workstation services were left running.
- This was a real-workstation scout, not a cold/clean isolated run.

Model:

```text
unsloth/Nemotron-3-Nano-30B-A3B-GGUF
Nemotron-3-Nano-30B-A3B-IQ4_XS.gguf
```

Observed by `llama-bench`:

```text
nemotron_h_moe 31B.A3.5B IQ4_XS - 4.25 bpw
model_size: 18161059584
model_n_params: 31577940288
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
| `-p 0 -n 32`, r1 | 66.06 tg32 | Smoke/load proof. |
| `pp512/tg128`, r5 | 619.00 pp512 / 65.45 tg128 | Standard direct `llama-bench` shape. |
| `-p 0 -n 128`, r10 | 66.60 tg128 | Generation-only confirmation. |

Interpretation:

- Nemotron 3 Nano 30B-A3B `IQ4_XS` runs directly on Strix Halo via `llama.cpp` Vulkan/RADV.
- This is the practical NVIDIA Nemotron route for one 128 GB Strix Halo system today.
- It is not the same as the newly released Nemotron 3 Ultra 550B-A55B.
- The right public framing is: Ultra is a major release, but Nano 30B-A3B is the direct local Strix Halo benchmark target.
- This is direct `llama-bench`, not server/API/MTP/speculative decoding.

Source:

- <https://huggingface.co/unsloth/Nemotron-3-Nano-30B-A3B-GGUF>
