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

Measured Strix Halo local LLM guide for Ryzen AI MAX+ 395 / Radeon 8060S / 128GB unified memory: setup, model choices, 63-97 t/s direct MoE results, 50.5 t/s Ollama, 128K context, CSVs, raw logs, and reproducibility notes.

## Short Share Text

I could not find one complete, copyable Strix Halo local LLM guide, so I made one with measured configs, raw CSVs/logs, and caveats.

Highlights:

- Qwen3-Coder 30B-A3B: 97.24 t/s direct llama.cpp Vulkan/RADV.
- Qwen3.6 35B-A3B: 63.06 t/s direct llama.cpp Vulkan/RADV.
- Qwen3.6 through Ollama API: 50.51 t/s warm average.
- 128K context tested on Qwen3.6 without truncation.
- Includes setup steps, backend choices, raw data, charts, and reproducibility notes.

Repo: https://github.com/hogeheer499-commits/strix-halo-guide

Corrections, other Strix Halo results, and failed experiments are welcome.

## Reddit / Forum Post

Title options:

- I benchmarked local LLMs on AMD Strix Halo 128GB: 97 t/s Qwen3-Coder, 50 t/s Ollama, 128K context
- Strix Halo local LLM guide with raw CSVs/logs: what works, what does not, and what to run
- AMD Ryzen AI MAX+ 395 local LLM guide: Ollama, llama.cpp, Vulkan/RADV, ROCm, 128K context

Post:

```text
I could not find one complete, copyable guide for running local LLMs on AMD Strix Halo / Ryzen AI MAX+ 395, so I made one:

https://github.com/hogeheer499-commits/strix-halo-guide

This is measured primarily on a Beelink GTR9 Pro with Ryzen AI MAX+ 395, Radeon 8060S, and 128GB unified memory.

Headline results:
- Qwen3-Coder 30B-A3B UD-Q4_K_XL: 97.24 t/s direct llama.cpp Vulkan/RADV
- Qwen3.6 35B-A3B UD-Q4_K_M: 63.06 t/s direct llama.cpp Vulkan/RADV
- Qwen3.6 35B-A3B through Ollama API: 50.51 t/s warm average
- Qwen3.6 128K filled-context decode completed at 32.23 t/s without truncation
- Server/concurrency testing included: Vulkan/RADV wins at 1-4 parallel requests; Lemonade ROCm wins aggregate throughput at 8-16 in the measured Qwen3.6 sweep

The guide includes:
- BIOS / Ubuntu / Mesa / Vulkan setup
- Ollama, llama.cpp, ROCm, Lemonade, and vLLM notes
- backend and model recommendations by use case
- CSVs, raw logs, charts, and reproducibility notes
- caveats for BIOS/kernel/Mesa/ROCm/model/context/backend differences

I am looking for corrections and more Strix Halo results from Framework, GMKtec, HP ZBook, Beelink, and other Ryzen AI MAX systems.
```

## Hacker News Style Post

Title options:

- Show HN: Strix Halo local LLM guide with raw benchmarks and reproducible setup
- Show HN: Running local LLMs on AMD Strix Halo 128GB, with CSV-backed benchmarks

Post:

```text
I made a Strix Halo local LLM guide after finding that the useful information was scattered across repos, issues, forum posts, and benchmark snippets.

It covers a measured Ubuntu setup for Ryzen AI MAX+ 395 / Radeon 8060S / 128GB unified memory, with Ollama, llama.cpp Vulkan/RADV, ROCm notes, server/concurrency testing, long-context tests, and raw benchmark evidence.

I tried to keep claims bounded: the main numbers are from one primary Beelink GTR9 Pro, and each headline points to CSVs/raw logs/charts or notes.

Repo: https://github.com/hogeheer499-commits/strix-halo-guide
```

## Discord / Slack Message

```text
Strix Halo local LLM guide with measured setup + raw benchmark evidence:
https://github.com/hogeheer499-commits/strix-halo-guide

Highlights: 97.24 t/s Qwen3-Coder direct llama.cpp Vulkan/RADV, 50.51 t/s Qwen3.6 via Ollama, 128K context tested, server shootout included.
```

## Links To Include

- README: https://github.com/hogeheer499-commits/strix-halo-guide
- Reproducibility: https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/REPRODUCIBILITY.md
- Server shootout: https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/SERVER_SHOOTOUT.md
- Headline claim index: https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv
- Raw data map: https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/README.md

## What To Ask For

- Benchmark results from other Strix Halo systems.
- Corrections to setup steps.
- Failed experiments and regressions.
- New model/backend combinations to test.
- Windows versus Linux comparisons, if measured on the same machine.
