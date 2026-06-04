# Qwen3.5 9B Q4_K_M Direct Comparator

Purpose: provide a direct local comparator for current Gemma 4 12B vs Qwen3.5 9B community discussion.

This is not a newest-model headline. It is a comparison/control row because Qwen3.5 9B is being discussed publicly against Gemma 4 12B.

Host notes:

- Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S.
- normal workstation services were left running.
- This was a real-workstation scout, not a cold/clean isolated run.

Model:

```text
unsloth/Qwen3.5-9B-GGUF
Qwen3.5-9B-Q4_K_M.gguf
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
| `pp512/tg128`, r5 | 1015.35 pp512 / 34.49 tg128 | Same direct benchmark shape as Gemma 4 12B scout. |
| `-p 0 -n 128`, r10 | 34.34 tg128 | Generation-only confirmation. |

Interpretation:

- Qwen3.5 9B `Q4_K_M` is faster than the Gemma 4 12B IT text-only rows measured on the same stack.
- This does not make Qwen3.5 9B the better current-model headline. It is an older Qwen-family comparator and should be framed as a community-discussion control.
- For newest-Qwen framing, prefer Qwen3.6 rows already present in the guide.
- This is direct `llama-bench`, not server/API/MTP/speculative decoding.

Source:

- <https://huggingface.co/unsloth/Qwen3.5-9B-GGUF>
