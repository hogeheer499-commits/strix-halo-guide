# Post-Migration Smoke Test - 2026-05-16

This directory proves that the storage migration did not break the benchmark model path.

After the old Windows partition was converted to ext4 and mounted at `/home/hoge-heer/models`, two Vulkan/RADV `llama-bench` smoke tests loaded models from that unchanged path:

- `Qwen_Qwen3-0.6B-Q8_0.gguf`
- `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`

These are smoke tests, not headline benchmark rows.

Result:

- Qwen3 0.6B loaded and ran from `/home/hoge-heer/models`.
- Qwen3.6 35B loaded and ran from `/home/hoge-heer/models`.
- The Qwen3.6 smoke row measured 61.02 tg32, matching the expected performance class for this short validation run.
