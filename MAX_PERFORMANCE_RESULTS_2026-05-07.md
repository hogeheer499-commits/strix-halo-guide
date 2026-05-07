# Max Performance Campaign - 2026-05-07

This page records the overnight Beelink GTR9 Pro max-performance campaign. It is the audit-friendly version of "did we leave obvious speed on the table?"

Structured summary: [`data/max_performance_campaign.csv`](data/max_performance_campaign.csv). Raw logs: [`data/raw/2026-05-07/max-performance-campaign/`](data/raw/2026-05-07/max-performance-campaign/).

## Short Answer

The guide is no longer just a 63-97 t/s claim.

Current practical read:

- Use Vulkan/RADV first for normal chat, coding, Ollama, and `llama-server`.
- Qwen3-Coder still tops out around 96-97 t/s on the current measured Vulkan path; no stable 100 t/s result was found.
- Qwen3.6 has a new speed-first path: Q4_0 reached 81.30 t/s, versus about 63 t/s for the older UD-Q4_K_M default row.
- HIP is still not the short-generation winner, but the same-source b9049 matrix confirms it can win prompt processing.
- gpt-oss-120b is stronger than the first local check: 55.57 t/s tg128 and prompt processing through 65K tokens.
- Plain vLLM AWQ without the gated DFlash drafter works, but it is not competitive with llama.cpp Vulkan on generation speed.

## Best New Numbers

| Workload | Best Local Result | Raw Evidence | Recommendation |
|----------|------------------:|--------------|----------------|
| Qwen3.6 speed-first generation | 81.30 t/s tg128, 1243.51 pp512 | [`q4-0 r20`](data/raw/2026-05-07/max-performance-campaign/benchmarks/qwen36-top-confirm-r20/q4-0-ub2048.csv) | Good for speed-first users; label as lower-quality Q4_0 quant. |
| Qwen3.6 balanced Strix quant | 76.94 t/s tg128, 1105.78 pp512 | [`Q4_K_M r20`](data/raw/2026-05-07/max-performance-campaign/benchmarks/qwen36-top-confirm-r20/q4-k-m-ub1024.csv) | Candidate replacement for the old UD row after a quality sanity check. |
| Qwen3-Coder current ceiling | 96.76 t/s tg128 | [`guide flags r20`](data/raw/2026-05-07/max-performance-campaign/benchmarks/qwen3-coder-top-confirm-r20/guide.csv) | Keep 96-97 t/s as the honest current ceiling. |
| gpt-oss-120b current Vulkan path | 55.57 t/s tg128, 726.99 pp512 | [`long-context sweep`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/) | Strong 120B local proof point; still not a quality eval. |
| Same-source HIP/Vulkan split | HIP wins pp16384; Vulkan wins tg128 | [`same-build matrix`](data/raw/2026-05-07/max-performance-campaign/benchmarks/same-build-hip-vulkan-b9049/) | Beginner rule stays RADV; advanced users test HIP for RAG/prefill. |

## Negative Results Worth Keeping

| Route | Result | Why It Matters |
|-------|--------|----------------|
| vLLM AWQ without DFlash | About 25 t/s at `np=1` | Works as an API smoke test, but not a speed route yet. |
| hec DFlash exact route | Blocked by gated `z-lab/Qwen3.6-27B-DFlash` access | Do not imply the guide reproduced DFlash until access and local results exist. |
| lhl rocWMMA tuned branch | Built, but failed to load current Qwen3.6 GGUFs | Useful lead, not publishable local speed evidence yet. |
| llama.cpp speculative sanity | Terminated after runaway CLI output | Keep out of headline claims until a controlled harness is added. |
| AMDVLK retest | Not run; no AMDVLK ICD is installed | Current clean system only exposes RADV for AMD Vulkan. |
| Thermals/power | Not run; no validated local sensor output | Do not publish tokens-per-watt or sustained-clock claims yet. |

## What This Changes In The Guide

The README should stay beginner-friendly:

- "Use RADV for Vulkan" remains the simple rule.
- "HIP can win prompt processing" is the advanced caveat.
- Qwen3.6 should show two choices: a default/balanced path and a speed-first Q4_0 path.
- The public headline can mention 63-97 t/s for current direct Qwen MoE, but the Qwen3.6 81.30 t/s row must be labeled speed-first.
- The gpt-oss-120b headline should move from 50.6 t/s to 55.6 t/s.

## Remaining Useful Work

The next truly valuable tests are not more random flag sweeps. They are:

- Quality sanity for the faster Qwen3.6 Strix quants, especially Q4_0 versus Q4_K_M/IQ4_NL.
- A controlled `llama-server` API run for Qwen3.6 Q4_0 and Q4_K_M, because users care about API speed, not only `llama-bench`.
- A real vLLM DFlash reproduction if gated access is granted.
- Sustained performance only after reliable temperature/power telemetry is available.
