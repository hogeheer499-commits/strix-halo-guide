# Nemotron 3 Nano Omni MXFP4 b9747 Smoke

Date: 2026-06-21

Purpose: quick first-party Beelink smoke test for a current NVIDIA Nemotron 3 Nano Omni GGUF route on the official `llama.cpp` b9747 Vulkan/RADV binary.

## Route

- Model repo: `unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-GGUF`
- File: `NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-MXFP4_MOE.gguf`
- Tool: official `llama-bench` b9747 release binary
- Build: `d6d899580` / build number `9747`
- Backend: Vulkan/RADV
- GPU line: `Radeon 8060S Graphics (RADV STRIX_HALO)`
- Kernel: `6.19.4-061904-generic`
- Mesa/RADV: Mesa `26.1.3` from kisak-mesa PPA

## Command

See [`command.txt`](command.txt).

```bash
/home/hoge-heer/benchmark-tools/llama-b9747/llama-b9747/llama-bench \
  --hf-repo unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-GGUF \
  --hf-file NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-MXFP4_MOE.gguf \
  -ngl 999 -fa on -p 512 -n 128 -r 3 -o csv
```

## Result

Structured output: [`llama-bench.csv`](llama-bench.csv)

| Test | Result |
| --- | ---: |
| pp512 | 1277.60 t/s |
| tg128 | 56.56 t/s |

## Interpretation

This is a useful current-model support row: the NVIDIA Nemotron 3 Nano Omni MXFP4 MoE GGUF loads and runs directly through `llama-bench` Vulkan/RADV on one 128GB Strix Halo system.

Do not treat this as a new speed headline. The older Nemotron 3 Nano IQ4_XS text route, Qwen 30B-class speed rows, LFM2.5 small-MoE row, and CHADROCK server/speculative row remain faster or more important for their respective claim categories.

