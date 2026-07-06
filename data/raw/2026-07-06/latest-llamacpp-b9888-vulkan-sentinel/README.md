# llama.cpp b9888 Vulkan Sentinel

Date: 2026-07-06

Purpose: check the latest official `llama.cpp` Ubuntu Vulkan release binary against the guide's Qwen3-Coder sentinel route without changing the headline claim boundary.

Hardware/software:

- Beelink GTR9 Pro
- AMD Ryzen AI MAX+ 395 / Radeon 8060S
- 128GB unified memory
- Ubuntu 24.04
- Kernel: recorded in `host-snapshot.txt`
- Mesa/RADV: recorded in `host-snapshot.txt`
- Tool: official `llama.cpp` b9888 Ubuntu Vulkan binary, build `cb295bf59`
- Device: explicit `-dev Vulkan0`

Command shape:

```bash
llama-bench \
  -m <model.gguf> \
  -dev Vulkan0 \
  -fa on \
  -ngl 999 \
  -mmp 0 \
  -b 2048 \
  -ub 512 \
  ...
```

Results:

| Model | Quant | Run | Result |
| --- | --- | --- | ---: |
| Qwen3-Coder 30B-A3B | `Q4_K_S` | `pp512/tg128 r50` | 1404.73 pp512 / 98.12 tg128 |
| Qwen3-Coder 30B-A3B | `Q4_K_S` | `p0/tg128 r50` | 98.59 t/s generation-only |
| Qwen3-Coder 30B-A3B | `UD-Q4_K_XL` | `pp512/tg128 r5` | 1410.82 pp512 / 96.53 tg128 |

Interpretation:

- b9888 works cleanly on the measured Vulkan/RADV path.
- It reproduces the Qwen3-Coder 98 t/s class.
- It does not replace the stronger b9851 `Q4_K_S` speed-first headline row at 100.99 t/s.
- Keep this as a latest-runtime sentinel, not as a new headline.

Raw files:

- `host-snapshot.txt`
- `llama-bench-devices.txt`
- `qwen3-coder-q4ks-b9888-faon-mmp0-p512-n128-r50.csv`
- `qwen3-coder-q4ks-b9888-faon-mmp0-p0-n128-r50.csv`
- `qwen3-coder-udq4kxl-b9888-faon-mmp0-r5.csv`
