---
license: other
language:
- en
library_name: gguf
tags:
- gguf
- nemotron
- nemotron-3
- nvidia
- nvfp4
- mamba2
- hybrid
- moe
base_model: nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16
pipeline_tag: text-generation
inference: false
quantized_by: FreedomAISVR
---

# Nemotron-3-30B-Nano-Omni NVFP4 GGUF

NVFP4 (E4M3) quantization of [nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16](https://huggingface.co/nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16), NVIDIA's 30B MoE (~3B active) reasoning model with Mamba2-SSM hybrid architecture.

### Why Is This File Bigger Than Expected?

This model uses a **Mamba2-Transformer hybrid MoE architecture** — 23 out of 52 layers are Mamba2 state-space model (SSM) layers. The CUDA kernels that run Mamba2 SSM operations (`SSM_SCAN`, `SSM_CONV`) **require F32 inputs** and will reject quantized weight tensors entirely.

When SSM weight tensors are quantized, the CUDA backend falls back to CPU for those layers. Since 44% of the model is Mamba2, this significantly impacts performance.

### The Workaround (Hybrid Quantization)

The 46 SSM weight tensors (`ssm_in.weight`, `ssm_out.weight` across 23 Mamba2 blocks) are stored in **F16** instead of the quantized format. Everything else stays at the original quantization.

### This Is a Bandaid, Not a Fix

This hybrid approach is a **temporary workaround** until llama.cpp adds quantized support to CUDA SSM kernels (`SSM_SCAN`, `SSM_CONV`). The kernels are currently hardcoded to F32 (`ssm_conv_f32`, `ssm_scan_f32` in the CUDA backend).



## Files

| Filename | Type | Size | Description |
|---|---|---|---|
| `nemotron-3-30b-NVFP4.gguf` | Hybrid NVFP4+F16 | ~18.4 GB | Main model weights (~4.88 BPW effective) |
| `mmproj-nemotron-3-30b-f16.gguf` | F16 | ~1.5 GB | SigLIP vision encoder |

## Architecture

- **52 layers**: 23 Mamba2 (SSM) + 23 MoE FFN (128 experts, top-6) + 6 attention
- **MoE**: 128 routed experts + 1 shared expert, top-6 routing
- **Vision**: SigLIP ViT (30 blocks, 1280 hidden)
- **Context**: 262K tokens

## Usage

```bash
llama-server -m nemotron-3-30b-NVFP4.gguf --mmproj mmproj-nemotron-3-30b-f16.gguf --host 0.0.0.0 --port 8080 -ngl 99
```

## Credits
- Original model: [NVIDIA](https://huggingface.co/nvidia)
- Quantization: [FreedomAISVR](https://huggingface.co/FreedomAISVR)
