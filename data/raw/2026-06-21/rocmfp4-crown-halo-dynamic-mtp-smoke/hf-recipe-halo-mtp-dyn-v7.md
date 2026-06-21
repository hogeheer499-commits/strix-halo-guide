# halo-mtp-dyn-v7 Recipe

Source:
- `unsloth/Qwen3.6-35B-A3B-MTP-GGUF`
- BF16 split GGUF shards
- `imatrix_unsloth.gguf_file`

Intent:
- Speed-biased refinement after v6 beat Q4 on the PPL proxy but missed 2K generation by a tiny margin.
- Use `MXFP4` on blocks 0-27 routed expert gate/up tensors.
- Leave blocks 28-35 routed expert gate/up tensors at the Q4_K_M fallback.
- Promote blocks 36-39 routed expert gate/up tensors to `Q5_K`.
- Keep routed down experts at `Q5_K`/`Q6_K`, attention/shared/token/output tensors at `Q8_0`, and the MTP tail gate/up tensors at Q4 fallback.

Delta versus v6:
- Blocks 24-27 gate/up tensors: Q4_K_M fallback -> `MXFP4`.
