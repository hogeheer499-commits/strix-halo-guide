# MiniMax M2.7 UD-IQ4_XS Local Smoke

Purpose: test whether a large current MoE model can load and generate locally on one Strix Halo / Ryzen AI MAX+ 395 system.

This is a feasibility/adoption test, not a speed-record attempt.

Host notes:

- Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S.
- normal workstation services were left running.
- This was a real-workstation scout, not a cold/clean isolated run.
- Disk was tight after download; no additional large-model downloads were started for this run.

Model:

```text
unsloth/MiniMax-M2.7-GGUF
UD-IQ4_XS/MiniMax-M2.7-UD-IQ4_XS-00001-of-00004.gguf
```

Observed by `llama-bench`:

```text
minimax-m2 230B.A10B IQ4_XS - 4.25 bpw
model_size: 108405492736
model_n_params: 228689764864
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

Commands:

```bash
llama-bench \
  -m /home/hoge-heer/benchmark-models/minimax-m27-ud-iq4xs/UD-IQ4_XS/MiniMax-M2.7-UD-IQ4_XS-00001-of-00004.gguf \
  -fa 1 -ngl 999 -mmp 0 -b 512 -ub 128 \
  -p 0 -n 32 -r 1 -o csv

llama-bench \
  -m /home/hoge-heer/benchmark-models/minimax-m27-ud-iq4xs/UD-IQ4_XS/MiniMax-M2.7-UD-IQ4_XS-00001-of-00004.gguf \
  -fa 1 -ngl 999 -mmp 0 -b 512 -ub 128 \
  -p 0 -n 128 -r 3 -o csv

llama-bench \
  -m /home/hoge-heer/benchmark-models/minimax-m27-ud-iq4xs/UD-IQ4_XS/MiniMax-M2.7-UD-IQ4_XS-00001-of-00004.gguf \
  -fa 1 -ngl 999 -mmp 0 -b 512 -ub 128 \
  -p 512 -n 128 -r 3 -o csv
```

Results:

| Shape | Result | Read |
| --- | ---: | --- |
| `-p 0 -n 32`, r1 | 28.07 tg32 | Smoke/load proof. |
| `-p 0 -n 128`, r3 | 28.60 tg128 | Stable generation-only check. |
| `pp512/tg128`, r3 | 101.00 pp512 / 28.27 tg128 | Standard direct `llama-bench` shape. |

Interpretation:

- MiniMax M2.7 `UD-IQ4_XS` loads and generates locally on one Strix Halo system via Vulkan/RADV.
- This is valuable as an adoption proof for 128 GB unified memory: a 230B-parameter, 10B-active MoE model can run locally.
- It is not a replacement for the Qwen direct speed headline. Generation is around 28 t/s in this route, not near 98.5-100 t/s.
- This is direct `llama-bench`, not MTP/server/speculative decoding.
- The result should be framed as "large current MoE model fits and runs locally", not "fastest local model".

Source:

- <https://huggingface.co/unsloth/MiniMax-M2.7-GGUF>
