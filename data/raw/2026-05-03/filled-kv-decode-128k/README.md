# 2026-05-03 Filled-KV Decode at 128K

Purpose: extend the filled-KV decode benchmark from 32K/64K to 128K with f16 KV cache.

## Preflight

| Item | Value |
|------|-------|
| System | Beelink GTR9 Pro |
| CPU/GPU | AMD Ryzen AI MAX+ 395 / Radeon 8060S |
| Kernel | 6.19.4-061904-generic |
| Vulkan driver | Mesa RADV 26.0.6, kisak-mesa PPA |
| llama.cpp | b9010 / `d05fe1d7d` |
| Backend | Vulkan RADV |
| Server | `llama-server` |
| KV cache | f16 |
| Prompt cache | disabled per request; server cache RAM set to 0 |

## Method

Each model was served with one slot, `ctx_size=132224`, `n_predict=128`, and a synthetic ~131K-token prompt. Each row is the average of two requests. No request truncated.

## Results

| Model | Prompt | KV | Prompt Eval | Decode After Fill | Wall Time | Truncated |
|-------|--------|----|-------------|-------------------|-----------|-----------|
| Qwen3.6 35B-A3B | 128K | f16 | 616.77 t/s | 32.23 t/s | 216.69 s | no |
| Qwen3-Next 80B-A3B | 128K | f16 | 497.79 t/s | 29.12 t/s | 268.54 s | no |

## Verdict

Both tested MoE models can complete a 128K prompt plus 128-token generation on the current Vulkan RADV stack without truncation. Qwen3.6 remains above 32 t/s after the 128K fill; Qwen3-Next 80B remains above 29 t/s. This makes the 128K local-document/codebase use case credible, with the caveat that prompt ingest takes several minutes on first turn.

Raw files:

- `filled-kv-decode-128k-summary.csv`
- `filled-kv-decode-128k-detail.csv`
- `*.log`
