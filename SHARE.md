# Share Pack

Use this file when sharing the guide on Reddit, Hacker News, Discord, forums, or with other Strix Halo owners.

Canonical link:

```text
https://github.com/hogeheer499-commits/strix-halo-guide
```

Social preview image in this repo:

```text
social-preview.png
```

## One-Line Summary

Measured Strix Halo local LLM guide for Ryzen AI MAX+ 395 / Radeon 8060S / 96-128GB unified memory: setup, model choices, 63-97 t/s current direct Qwen MoE results, 81.3 t/s Qwen3.6 speed-first, 55.6 t/s gpt-oss-120b, 128K context, MTP speculative decoding at 92-93 t/s broad average, CSVs, raw logs, reproducibility notes, community validation across Corsair and GMKtec systems, command-flag sensitivity notes, and first wall-power efficiency rows.

## Short Share Text

I could not find one complete, copyable Strix Halo local LLM guide, so I made one with measured configs, raw CSVs/logs, and caveats.

Highlights:

- Qwen3-Coder 30B-A3B: 96.76 t/s direct llama.cpp Vulkan/RADV on current b9049; previous b9010 peak was 97.24 t/s.
- Qwen3.6 35B-A3B: 62.56 t/s direct llama.cpp Vulkan/RADV on current b9049.
- Qwen3.6 35B-A3B Q4_0: 81.30 t/s direct llama.cpp Vulkan/RADV as a speed-first quant row.
- Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn: 92.30 t/s local Beelink average over six `llama-server` prompts; first GMKtec community reproduction reached 93.29 t/s. Best local prompt was 110.61 t/s. This is speculative server evidence, not a broad 100 t/s claim.
- gpt-oss-120b MXFP4: 55.57 t/s direct llama.cpp Vulkan/RADV on current b9049.
- Qwen3.6 through Ollama 0.23.1 API: 50.51 t/s warm average.
- 128K context tested on Qwen3.6 without truncation.
- Independent community validation: three Corsair AI Workstation 300 systems measured 93.55-95.50 t/s Qwen3-Coder, a GMKtec EVO-X2 96GB native Ubuntu run reproduced the guide's Qwen3.6 row within -0.8% pp512 and -1.7% tg128, the same GMKtec class added Qwen3-Coder b9235 follow-up rows, and it reproduced the MTP route at 93.29 t/s average.
- Community wall-power context: Qwen3-Coder around 150 W / 1.6 J/token, Qwen3.6 around 148 W / 2.0 J/token, gpt-oss-120b around 174 W / 3.1 J/token, and Qwen3-Coder-Next around 137 W / 3.4 J/token during sustained generation.
- Includes setup steps, backend choices, raw data, charts, and reproducibility notes.

Repo: https://github.com/hogeheer499-commits/strix-halo-guide

Corrections, other Strix Halo results, and failed experiments are welcome.

## Reddit / Forum Post

Title options:

- I benchmarked local LLMs on AMD Strix Halo 128GB: 97 t/s Qwen3-Coder, 55.6 t/s gpt-oss-120b, 128K context
- Strix Halo local LLM guide with raw CSVs/logs: what works, what does not, and what to run
- AMD Ryzen AI MAX+ 395 local LLM guide: Ollama, llama.cpp, Vulkan/RADV, ROCm, 128K context

Post:

```text
I could not find one complete, copyable guide for running local LLMs on AMD Strix Halo / Ryzen AI MAX+ 395, so I made one:

https://github.com/hogeheer499-commits/strix-halo-guide

This is measured primarily on a Beelink GTR9 Pro with Ryzen AI MAX+ 395, Radeon 8060S, and 128GB unified memory.

Headline results:
- Qwen3-Coder 30B-A3B UD-Q4_K_XL: 96.76 t/s direct llama.cpp Vulkan/RADV on current b9049
- Qwen3.6 35B-A3B UD-Q4_K_M: 62.56 t/s direct llama.cpp Vulkan/RADV on current b9049
- Qwen3.6 35B-A3B Q4_0: 81.30 t/s direct llama.cpp Vulkan/RADV as a speed-first quant row
- Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn: 92.30 t/s local average over six llama-server prompts; 93.29 t/s in the first GMKtec community reproduction; best local prompt 110.61 t/s, scoped as speculative server evidence
- gpt-oss-120b MXFP4 split GGUF: 55.57 t/s direct llama.cpp Vulkan/RADV on current b9049
- Qwen3.6 35B-A3B through Ollama 0.23.1 API: 50.51 t/s warm average
- Qwen3.6 128K filled-context decode completed at 32.23 t/s without truncation
- Server/concurrency testing included: Vulkan/RADV wins at 1-4 parallel requests; Lemonade ROCm wins aggregate throughput at 8-16 in the measured Qwen3.6 sweep
- HIP/Vulkan crossover testing included: HIP can win prompt processing while Vulkan still wins token generation in local Qwen rows
- Independent community validation included: three Corsair AI Workstation 300 systems measured 93.55-95.50 t/s Qwen3-Coder, a GMKtec EVO-X2 96GB native Ubuntu run reproduced the Qwen3.6 row within -0.8% pp512 and -1.7% tg128, a GMKtec Qwen3-Coder b9235 follow-up added full pp/tg portability evidence, and a GMKtec MTP rerun reached 93.29 t/s average
- Wall-power context included: community measurements around 150 W / 1.6 J/token for Qwen3-Coder, 174 W / 3.1 J/token for gpt-oss-120b, and additional Qwen3.6 / Qwen3-Coder-Next rows

The guide includes:
- BIOS / Ubuntu / Mesa / Vulkan setup
- Ollama, llama.cpp, ROCm, Lemonade, and vLLM notes
- backend and model recommendations by use case
- CSVs, raw logs, charts, and reproducibility notes
- caveats for BIOS/kernel/Mesa/ROCm/model/context/backend differences

I am looking for corrections and more Strix Halo results from Framework, GMKtec, HP ZBook, Beelink, and other Ryzen AI MAX systems.
Wall-power / smart-plug / UPS power data is especially useful because it turns raw t/s into practical tokens-per-watt context.
```

## Hacker News Style Post

Title options:

- Show HN: Strix Halo local LLM guide with raw benchmarks and reproducible setup
- Show HN: Running local LLMs on AMD Strix Halo 128GB, with CSV-backed benchmarks

Post:

```text
I made a Strix Halo local LLM guide after finding that the useful information was scattered across repos, issues, forum posts, and benchmark snippets.

It covers a measured Ubuntu setup for Ryzen AI MAX+ 395 / Radeon 8060S / 128GB unified memory, with Ollama, llama.cpp Vulkan/RADV, ROCm notes, server/concurrency testing, long-context tests, and raw benchmark evidence.

I tried to keep claims bounded: the main numbers are from one primary Beelink GTR9 Pro, each headline points to CSVs/raw logs/charts or notes, and community reproductions are kept in a separate results table.

Repo: https://github.com/hogeheer499-commits/strix-halo-guide
```

## Discord / Slack Message

```text
Strix Halo local LLM guide with measured setup + raw benchmark evidence:
https://github.com/hogeheer499-commits/strix-halo-guide

Highlights: 96.76 t/s Qwen3-Coder direct llama.cpp Vulkan/RADV on current b9049, 92.30 t/s local Qwen3.6 MTP server average plus 93.29 t/s GMKtec community MTP reproduction, 55.57 t/s gpt-oss-120b MXFP4, 128K context tested, server shootout included, N=3 Corsair validation at 93.55-95.50 t/s, GMKtec EVO-X2 native Ubuntu Qwen3.6 validation within 2%, GMKtec Qwen3-Coder b9235 follow-up data, community wall-power rows, a community 3-node USB4 llama.cpp RPC matrix, and USB4 latency tuning data.
```

## Links To Include

- README: https://github.com/hogeheer499-commits/strix-halo-guide
- Reproducibility: https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/REPRODUCIBILITY.md
- Server shootout: https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/SERVER_SHOOTOUT.md
- Headline claim index: https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv
- Community results: https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/COMMUNITY_RESULTS.md
- Power baseline: https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/POWER_BASELINE.md
- Community RPC results: https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/COMMUNITY_RPC.md
- USB4 cluster tuning: https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/USB4_CLUSTER_TUNING.md
- Raw data map: https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/README.md

## What To Ask For

- Benchmark results from other Strix Halo systems.
- Corrections to setup steps.
- Failed experiments and regressions.
- New model/backend combinations to test.
- Windows versus Linux comparisons, if measured on the same machine.
- Wall-power or UPS/smart-plug efficiency rows with raw readings.
