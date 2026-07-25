# Qwen3-ASR 0.6B Official GGUF Local Audio Check

First-party Beelink GTR9 Pro result from 2026-07-25.

## Result

- The `llama.cpp`-documented `ggml-org/Qwen3-ASR-0.6B-GGUF` route loaded
  and ran locally with `llama-mtmd-cli` b10107 on Vulkan/RADV.
- It identified the language as English and transcribed the known ALSA test
  sample as `Front, center.`
- A fresh process using the cached model produced the exact same transcript.
- The transcript-line SHA-256 was
  `cc74763233d68fe0bb7d60bd451e2013f4434d6bb5f9d4a30076ac0b8c933cd2`
  on both runs.
- The cached restart completed in 1.13 seconds wall time with 930,416 KiB
  maximum resident memory.

This is a local functionality and reproducibility check on one short clean
English sample. It is not a word-error-rate benchmark. The current
`llama.cpp` audio path also warns that audio support is experimental and may
have reduced quality.

## Exact Inputs

- Source: `ggml-org/Qwen3-ASR-0.6B-GGUF`
- Hugging Face revision:
  `928ab958557df9aa2ef1c93e0e83c7ad0933fae2`
- Text model: `Qwen3-ASR-0.6B-Q8_0.gguf` (804,749,248 bytes)
- Text-model SHA-256:
  `bca259818b50ca7c4c05e9bdb35a5dc04fa039653a6d6f3f0f331f96f6aa1971`
- Projector: `mmproj-Qwen3-ASR-0.6B-Q8_0.gguf` (214,392,480 bytes)
- Projector SHA-256:
  `41a342b5e4c514e968cb756de6cd1b7be39eff43c44c57a2ef5fc6522e36603d`
- Runtime: `llama-mtmd-cli` b10107 (`c0bc8591e`)
- Runtime SHA-256:
  `f423fd6e9eafef9d545634bda0beb3bd250d5a29122aa2e7cd8067d87d0bde1b`
- Audio: `/usr/share/sounds/alsa/Front_Center.wav`
- Audio SHA-256:
  `0d61518bcd3f13b0c709a5298e939caf698b80d31d71d50475365ee0e5536cc9`
- Audio format: mono, 48 kHz, signed 16-bit PCM
- Backend: Vulkan/RADV

## Command

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
llama-mtmd-cli \
  -hf ggml-org/Qwen3-ASR-0.6B-GGUF \
  --audio /usr/share/sounds/alsa/Front_Center.wav \
  -p 'Transcribe this audio exactly. Return only the spoken words.' \
  -ngl 999 \
  -fa on \
  -c 8192 \
  -n 96 \
  --temp 0 \
  --seed 42
```

## Files

- `first-run.log`: first download/load and transcript.
- `restart-run.log`: cached fresh-process repeat plus `/usr/bin/time -v`
  telemetry.
