# Qwen3-TTS 1.7B llama.cpp Vulkan/RADV Smoke

First-party Beelink GTR9 Pro functionality and restart check from 2026-08-09.
This validates the newly merged Qwen3-TTS route in `llama.cpp` b10330 and then
uses Qwen3-ASR to check the generated speech. It is not a voice-quality or
multilingual benchmark.

## Result

- The official Qwen3-TTS 1.7B Q4_K_M target plus Q8_0 projector loaded on
  Vulkan/RADV and generated a valid 24 kHz mono PCM WAV.
- First run: 50 frames, 4.00 seconds of audio, 1.38 seconds reported model
  processing after load/download (`2.90x` real time).
- Fresh cached process: 52 frames, 4.16 seconds of audio, 1.27 seconds
  reported model processing (`3.27x` real time), 2.95 seconds wall time.
- The two WAV files are not byte-identical. This is a repeatable functionality
  check, not a deterministic-audio claim.
- Qwen3-ASR 0.6B transcribed the cached-repeat output as:
  `Strix Halo can run local text-to-speech with Llama.CPP.`

The prompted text was `Strix Halo can run local text to speech with
llama.cpp.` The back-transcription therefore preserves the intended content.

## Exact Route

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
llama-tts \
  -hf ggml-org/Qwen3-TTS-12Hz-1.7B-Base-GGUF:Q4_K_M \
  -p 'Strix Halo can run local text to speech with llama.cpp.' \
  --tts-lang en \
  -ngl 999 \
  --seed 42 \
  --temp 0 \
  --output repeat.wav
```

The ASR back-check reused the guide's documented official
`ggml-org/Qwen3-ASR-0.6B-GGUF` route.

## Versions And Caveats

- System: Beelink GTR9 Pro, Ryzen AI MAX+ 395, Radeon 8060S, 128 GB
- Kernel: 7.0.0-28-generic
- Mesa/RADV: 26.1.6
- `llama.cpp`: b10330 commit
  `687e7789271ec1276e3470f158428e11a4f80b6f`
- TTS source revision: `ca27d74bc954b73dadab5b71ca265d87fc861a7c`
- ASR source revision: `928ab958557df9aa2ef1c93e0e83c7ad0933fae2`
- Background state: normal low-load workstation services remained active; see
  `host-snapshot.txt`.

The Vulkan warmup reports unsupported `PAD_REFLECT_1D` projector operations,
warns that performance may be suboptimal, and labels audio support
experimental with possible reduced quality. Keep this as an experimental
local speech route until broader language, voice, quality, and long-run tests
exist.

## Files

- `first-run.log`, `first.wav`: download/load pass and first output.
- `repeat-run.log`, `repeat.wav`: fresh cached-process repeat.
- `asr-backcheck.log`: independent content back-transcription.
- `model-metadata.txt`, `sha256.txt`: exact artifact revisions, sizes, and
  hashes.
- `runtime-version.txt`, `host-snapshot.txt`: runtime and host context.
