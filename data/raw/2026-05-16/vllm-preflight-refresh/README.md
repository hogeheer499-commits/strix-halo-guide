# vLLM Preflight Refresh - 2026-05-16

This directory records a lightweight refresh of the existing `vllm-gfx1151` container.

Container:

- `vllm-gfx1151`
- Image: `docker.io/kyuz0/vllm-therock-gfx1151:stable`

Result:

- Container starts.
- GPU visibility through ROCm SMI still shows Radeon 8060S / gfx1151.
- Container versions:
  - vLLM `0.19.2rc1.dev113+g6aa057c9d.d20260422.rocm713`
  - PyTorch `2.13.0a0+rocm7.13.0a20260422`
  - Triton `3.7.0+git6aa07328.rocm7.13.0a20260422`

Existing local performance evidence:

- The 2026-05-07 AWQ smoke test for Qwen3.6-35B-A3B AWQ4 measured about 24.8-25.0 aggregate t/s at `np=1`.
- That proves the route can serve, but it does not compete with the current llama.cpp Vulkan/RADV single-user generation rows.

Interpretation:

- Keep plain vLLM AWQ as experimental server evidence.
- Do not promote vLLM as a faster default path until DFlash or another serving-specific workload is reproduced locally.
