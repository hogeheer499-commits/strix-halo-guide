# Qwen3-Coder-Next IQ4_XS Vulkan/RADV

Local Beelink GTR9 Pro follow-up for the Reddit criticism that the 98.51 t/s Qwen3-Coder 30B headline uses an older model.

## Result

- Date: 2026-06-02
- System: Beelink GTR9 Pro, Ryzen AI MAX+ 395, Radeon 8060S, 128GB unified memory
- Backend: llama.cpp Vulkan/RADV
- Build: b8275a8ac
- Model: Qwen3-Coder-Next IQ4_XS GGUF from `unsloth/Qwen3-Coder-Next-GGUF`
- Size: 39.74 GiB
- Command shape: `-fa on -ngl 999 -mmp 0 -b 2048 -ub 512 -p 512,0 -n 0,128 -r 5`

Measured result:

- pp512: 735.72 t/s
- tg128: 61.68 t/s

## Interpretation

This is a modern coding-model row and useful evidence for people who want current Qwen coding models on Strix Halo. It does not replace the 98.51 t/s Qwen3-Coder 30B speed-first headline; it answers a different question: how fast a newer 80B-total / 3B-active Qwen3-Coder-Next GGUF runs locally on the Beelink.
