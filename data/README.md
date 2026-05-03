# Benchmark Data

This directory contains structured benchmark data used by the guide.

The README remains the human-facing guide. These files are the machine-readable source for future charts, dashboards, comparisons, and social images.

Generated SVG summaries live in `../charts/`. Regenerate them after changing CSV data:

```bash
python3 scripts/generate_charts.py
```

## Files

- `benchmarks.csv`: existing short-context and backend benchmark rows already published in the guide.
- `multi_user.csv`: controlled `llama-server` concurrency results with aggregate throughput, per-request throughput, TTFT, and ITL.
- `long_context.csv`: long-context reference measurements.
- `filled_kv_decode.csv`: controlled `llama-server` requests measuring decode after a 32K/64K prompt, including KV-cache type comparisons.
- `smoke_tests.csv`: short validation runs that prove the current stack is healthy before larger benchmark campaigns.
- `raw/`: raw command output for controlled benchmark runs used by current claims.
- `../SMOKE_TESTS.md`: human-readable smoke-test notes and verdicts.
- `../charts/`: generated SVG charts derived from the CSV files.

## Status Values

- `measured-local`: measured on this guide's Beelink GTR9 Pro and suitable for current claims.
- `historical-local`: measured locally in an older stack state; useful context, not the current headline.
- `external-reference`: measured by another source and cited for comparison.
- `smoke-test`: short validation run, not a full benchmark campaign.

## Required Metadata for New Rows

Every new benchmark row should include:

- date
- system
- kernel
- Mesa/RADV or ROCm version
- backend and driver
- tool and build/commit where available
- model name
- quant
- prompt/context settings
- pp and/or tg result
- source command or source reference
- status

If any of those are unknown, leave the cell blank rather than guessing.
