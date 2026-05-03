# 2026-05-03 Real-Corpus Filled-KV Decode

Purpose: repeat the 64K filled-KV decode test with a real prompt assembled from this guide's documentation files instead of a synthetic repeated-token prompt.

## Method

The prompt was built from local guide files:

- `README.md`
- `BENCHMARKS.md`
- `RESEARCH.md`
- `TEST_PLAN.md`
- `SMOKE_TESTS.md`
- `data/README.md`

Each model used `llama-server`, Vulkan RADV, f16 KV cache, prompt cache disabled, `n_predict=128`, `temperature=0`, and `top_k=1`. Each row is the average of two requests.

## Results

| Model | Tokens Evaluated | Prompt Eval | Decode After Fill | Wall Time | Truncated |
|-------|------------------|-------------|-------------------|-----------|-----------|
| Qwen3.6 35B-A3B | 65,120 | 706.21 t/s | 40.84 t/s | 95.41 s | no |
| Qwen3-Next 80B-A3B | 63,507 | 504.53 t/s | 37.75 t/s | 129.40 s | no |

## Synthetic vs Real-Corpus

| Model | Prompt Type | Tokens | Prompt Eval | Decode After Fill | Wall Time |
|-------|-------------|--------|-------------|-------------------|-----------|
| Qwen3.6 35B-A3B | synthetic repeated token | 65,533 | 931.89 t/s | 41.44 t/s | 73.52 s |
| Qwen3.6 35B-A3B | real guide corpus | 65,120 | 706.21 t/s | 40.84 t/s | 95.41 s |
| Qwen3-Next 80B-A3B | synthetic repeated token | 65,532 | 753.26 t/s | 38.18 t/s | 90.45 s |
| Qwen3-Next 80B-A3B | real guide corpus | 63,507 | 504.53 t/s | 37.75 t/s | 129.40 s |

## Verdict

Synthetic repeated-token prompts are optimistic for prompt-ingest speed. Real documentation text slowed prompt processing by about 24% on Qwen3.6 and 33% on Qwen3-Next 80B. Decode speed after the cache was filled stayed almost unchanged.

Use the synthetic rows for controlled backend/cache comparisons. Use the real-corpus rows for user-facing expectations on large documents and codebases.
