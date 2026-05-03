# vLLM Container Baseline

This file records the clean vLLM setup state. It is not a benchmark result.

## 2026-05-03 Preflight

Status: clean container setup and small-model smoke test completed.

Container:

- Name: `vllm-gfx1151`
- Runtime: rootless Podman via Distrobox
- Image: `docker.io/kyuz0/vllm-therock-gfx1151:stable`
- Image ID: `4723cfafb369`
- Image size: 30.5 GB
- Container home: `/home/hoge-heer/distrobox/vllm-gfx1151`

Host/GPU visibility from inside the container:

- Host kernel driver reported by `rocm-smi`: `6.19.4-061904-generic`
- GPU: Radeon 8060S Graphics
- GFX version: `gfx1151`

Container software:

- OS: Fedora Linux 43 container image
- ROCm used by PyTorch: `7.13.26154`
- vLLM: `0.19.2rc1.dev113+g6aa057c9d.d20260422`
- vLLM git sha: `6aa057c9d`
- PyTorch: `2.13.0a0+rocm7.13.0a20260422`
- Triton: `3.7.0+git6aa07328.rocm7.13.0a20260422`
- Python: `3.12.13`

Relevant environment:

```bash
VLLM_TARGET_DEVICE=rocm
VLLM_USE_TRITON_AWQ=1
VLLM_DISABLE_COMPILE_CACHE=1
ROCBLAS_USE_HIPBLASLT=1
PYTORCH_ROCM_ARCH=gfx1151
HIP_ARCHITECTURES=gfx1151
TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
```

Smoke command:

```bash
podman exec --user hoge-heer vllm-gfx1151 bash -lc '
  cd "$HOME" &&
  VLLM_DISABLE_COMPILE_CACHE=1 vllm serve Qwen/Qwen3-0.6B \
    --host 127.0.0.1 \
    --port 18001 \
    --max-model-len 2048 \
    --max-num-seqs 1 \
    --gpu-memory-utilization 0.20 \
    --dtype auto \
    --attention-backend TRITON_ATTN \
    --enforce-eager
'
```

Smoke result:

- `GET /health`: HTTP 200
- `GET /v1/models`: returned `Qwen/Qwen3-0.6B` with `max_model_len=2048`
- `POST /v1/chat/completions`: HTTP 200
- `GET /metrics`: vLLM metrics exposed
- First run downloaded a 1.40 GiB safetensors checkpoint
- Model load reported 1.2 GiB memory and 22.86 s load time
- KV cache reported 22.43 GiB available and 210,016 tokens

Interpretation:

- vLLM is now installed and verified in a clean isolated container.
- This proves serving works on gfx1151 with the stable kyuz0 image.
- This does not prove useful throughput for the guide yet. The next benchmark must use the same model/quant/concurrency framing as the existing `llama-server` data.

Next controlled vLLM benchmark:

1. Use the `:stable` container first; only test `:latest` after the stable baseline.
2. Start with `cyankiwi/Qwen3.6-35B-A3B-AWQ-4bit` or another model explicitly supported by the toolbox.
3. Run concurrency 1, 2, 4, 8, 16.
4. Capture TTFT, p50/p95 latency, aggregate throughput, memory, startup/warmup time, and exact serve flags.
5. Compare against `llama-server` only when model, quant, context, token count, and concurrency are defensible.
