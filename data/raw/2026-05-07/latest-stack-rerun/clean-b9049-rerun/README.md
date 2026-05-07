# Clean Latest-Stack Rerun

Date: 2026-05-07

Purpose: rerun the public short-context headline checks after updating the local
llama.cpp worktree to b9049 and Ollama to 0.23.1, without changing the kernel,
Mesa/RADV stack, BIOS setup, or model files.

## Host State

- System: Beelink GTR9 Pro, Ryzen AI MAX+ 395, Radeon 8060S / RADV STRIX_HALO.
- Kernel: `6.19.4-061904-generic`.
- Mesa/RADV: Mesa 26.0.6 from kisak-mesa PPA.
- Power profile: `accelerator-performance`.
- One lightweight maintainer workstation dependency stayed running by design.
- Non-essential remote, meeting, and screen-share services were paused for the
  benchmark window and restored afterward.

See:

- `host-state-before.txt`
- `host-state-after-llamacpp.txt`
- `host-state-after-ollama.txt`
- `restore-manifest.txt`
- `ollama-update.log`

## Results

| Tool | Build | Model | Workload | Result |
|------|-------|-------|----------|--------|
| llama-bench Vulkan/RADV | b9049 `2496f9c14` | Qwen3-Coder 30B-A3B UD-Q4_K_XL | pp512 / tg128, `-r 20` | 1396.66 pp512, 96.15 tg128 |
| llama-bench Vulkan/RADV | b9049 `2496f9c14` | Qwen3.6 35B-A3B UD-Q4_K_M | pp512 / tg128, `-r 20` | 1059.45 pp512, 62.56 tg128 |
| Ollama Vulkan/RADV | 0.23.1 | Qwen3.6 35B-A3B Q4_K_M | `/api/generate`, 10 warm runs | 158.03 prompt eval, 50.51 generation |

## Takeaway

The latest-stack rerun does not materially change the public conclusions:

- Direct llama.cpp Vulkan/RADV remains the fastest short-context path.
- Current b9049 direct numbers round to 63-96 t/s for the two headline MoE
  models tested here.
- The previous b9010 Qwen3-Coder peak of 97.24 t/s remains valid historical
  evidence, but b9049 measured 96.15 t/s in this clean rerun.
- Ollama 0.23.1 matches the earlier 0.21.2 Qwen3.6 API speed within noise.
