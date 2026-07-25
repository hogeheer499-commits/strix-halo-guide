# LFM2.5-VL 1.6B Official GGUF Local Vision Check

First-party Beelink GTR9 Pro result from 2026-07-25.

## Result

- The official `LiquidAI/LFM2.5-VL-1.6B-GGUF:Q4_0` route loaded and ran
  locally with `llama-mtmd-cli` b10107 on Vulkan/RADV.
- The model correctly read the largest title, AMD Strix Halo platform,
  `101.0 t/s`, `140.4 t/s`, and `128 GB` from `social-preview.png`.
- A fresh process using the cached model produced the exact same response.
- The response-line SHA-256 was
  `8db42bb5bd37801a44228df32975f98a943b1226803955a85d46149607041add`
  on both runs.
- The cached restart completed in 1.89 seconds wall time with 794,564 KiB
  maximum resident memory.

This is a local vision functionality and reproducibility check, not a
quality benchmark or a claim that this is the fastest vision model.

## Exact Inputs

- Source: `LiquidAI/LFM2.5-VL-1.6B-GGUF`
- Hugging Face revision:
  `0df8719db7180cedababc2bc589abfe5e8ebcd1f`
- Text model: `LFM2.5-VL-1.6B-Q4_0.gguf` (695,752,480 bytes)
- Projector: `mmproj-LFM2.5-VL-1.6b-Q8_0.gguf` (583,109,888 bytes)
- Runtime: `llama-mtmd-cli` b10107 (`c0bc8591e`)
- Runtime SHA-256:
  `f423fd6e9eafef9d545634bda0beb3bd250d5a29122aa2e7cd8067d87d0bde1b`
- Image: repository `social-preview.png`
- Backend: Vulkan/RADV

## Command

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
llama-mtmd-cli \
  -hf LiquidAI/LFM2.5-VL-1.6B-GGUF:Q4_0 \
  --image social-preview.png \
  -p 'Describe this image in one concise paragraph. Mention the largest title and the AMD hardware platform if readable.' \
  -ngl 999 \
  -fa on \
  -c 8192 \
  -n 192 \
  --temp 0 \
  --seed 42
```

## Files

- `first-run.log`: first successful load and response.
- `restart-run.log`: cached fresh-process repeat plus `/usr/bin/time -v`
  telemetry.

The earlier invalid `--load-mode read` invocation was corrected before the
repeat. Supported b10107 load modes are `none`, `mmap`, `mlock`, and `dio`.
