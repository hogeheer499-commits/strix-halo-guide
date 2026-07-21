# Benchmark Charts

These SVG charts are generated from the structured CSV files in `data/`.

Regenerate them after changing benchmark data:

```bash
python3 scripts/generate_charts.py
```

## Files

- `multi_user_aggregate.svg`: aggregate `llama-server` throughput across `-np 1/2/4/8/16`.
- `long_context_prompt.svg`: local RADV prompt-processing scaling from 4K to 64K.
- `filled_kv_decode.svg`: decode speed after 32K/64K/128K filled KV cache.
- `kv_cache_tradeoff.svg`: Qwen3.6 q8_0/q4_0 KV-cache tradeoff relative to f16.
- `real_vs_synthetic.svg`: 64K real documentation corpus versus synthetic repeated-token prompt.
- `backend_spot_check.svg`: May 2026 Vulkan RADV versus ROCm HIP short-context tg spot check.
- `backend_crossover_prefill.svg`: HIP versus Vulkan prompt-processing spot check at pp16384.
- `backend_crossover_generation.svg`: HIP versus Vulkan token-generation spot check at tg128.
- `moe_density_gate_30b.svg`: Qwen3-Coder 30B aggregate decode across concurrency 1-64 for b9979 stock/density/dense16 Vulkan and Lemonade ROCm.
- `moe_density_gate_80b.svg`: Qwen3-Next 80B version of the same concurrency crossover.
- `community_corsair_sclk_throughput.svg`: Fail-Safe's strict three-system
  Corsair prompt/generation throughput sweep across 2200-2600 MHz SCLK caps.
- `community_corsair_sclk_thermal.svg`: the same campaign's 30-minute socket
  power and worst edge-temperature tradeoff, including bounded stock controls.

The SVGs are publishable summaries. The CSVs and raw logs remain the source of truth.
