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

## Share Responsibly

Please do not brigade, coordinate upvotes, or require anyone to share this repo as a condition of contributing. Sharing is useful only when it adds evidence or helps another owner reproduce a result.

If you are a contributor sharing your own result:

- disclose that your row is a community reproduction or follow-up
- lead with your hardware, backend, model, command, and raw output
- link to the repo only when the guide or data is directly relevant
- invite corrections and failed/slower runs
- follow the target platform's self-promotion rules

Good framing:

```text
I reproduced one Strix Halo local LLM benchmark on my own system and posted the raw output. Here is where it matched or differed from the guide.
```

Avoid:

```text
Please upvote/star this repo.
```

```text
Everyone should post this link.
```

## One-Line Summary

Measured Strix Halo local LLM guide for Ryzen AI MAX+ 395 / Radeon 8060S / 96-128GB unified memory: setup, model choices, direct 100.0 t/s 30B-class Qwen MoE evidence, 170.0 t/s LFM2.5 small-MoE evidence, 18.4 t/s Nemotron 3 Super 120B direct GGUF capacity evidence, 98.5 t/s Qwen3-Coder speed-first, 81.3 t/s Qwen3.6 speed-first, 55.6 t/s gpt-oss-120b, 128K context, MTP speculative decoding at 101.1 t/s on Qwen3.6 and 102.7-110.0 t/s on Gemma 4 26B-A4B QAT including a 107.4 t/s T3-only repeat, CSVs, raw logs, reproducibility notes, community validation across Corsair, GMKtec, MS-S1-Max, and Nimo systems, command-flag sensitivity notes, Windows LM Studio evidence, tuned thermal/power-policy evidence, Nimo large-model serving evidence, and first wall-power efficiency rows.

## Short Share Text

I could not find one complete, copyable Strix Halo local LLM guide, so I made one with measured configs, raw CSVs/logs, and caveats.

Highlights:

- Qwen3-Coder 30B-A3B: 96.76 t/s direct llama.cpp Vulkan/RADV on current b9049; previous b9010 peak was 97.24 t/s.
- Qwen3-30B-A3B-Instruct-2507 IQ4_XS: 100.04 t/s direct llama.cpp Vulkan/RADV on b9467. This is a separate general-instruct Qwen route, not the Qwen3-Coder headline.
- LFM2.5 8B-A1B Q4_K_M: 168.96 t/s in pp512/tg128 and 170.02 t/s generation-only in the 2026-06-05 latest/int-dot check. This is a small active-parameter MoE speed row, not a 30B-class replacement.
- Nemotron 3 Super 120B-A12B UD-IQ4_XS: 18.43 t/s direct llama.cpp Vulkan/RADV in the 2026-06-05 latest/int-dot check. This is a 120B-class GGUF capacity/current-model row, not a speed headline.
- Qwen3-Coder 30B-A3B Q4_K_S: 98.51 t/s direct llama.cpp Vulkan/RADV speed-first row on b9179.
- Qwen3.6 35B-A3B: 62.56 t/s direct llama.cpp Vulkan/RADV on current b9049.
- Qwen3.6 35B-A3B Q4_0: 81.30 t/s direct llama.cpp Vulkan/RADV as a speed-first quant row.
- Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn: 101.16 t/s best local Beelink average over six `llama-server` prompts on b9360, with repeated t16 runs around 101.1 t/s; first GMKtec community reproduction reached 93.29 t/s on b9235. Best local prompt was 117.53 t/s. This is speculative server evidence, not a direct `llama-bench` headline.
- Gemma 4 26B-A4B QAT with matched MTP head: 73.96 t/s no-spec server baseline, 102.69 t/s cold repeat, 107.42 t/s T3-only repeat, 110.00 t/s best repeat on ac4cddeb0. This is current-model server/speculative evidence, not a direct `llama-bench` headline.
- gpt-oss-120b MXFP4: 55.57 t/s direct llama.cpp Vulkan/RADV on current b9049.
- Qwen3.6 through Ollama 0.23.1 API: 50.51 t/s warm average.
- 128K context tested on Qwen3.6 without truncation.
- Independent community validation: three Corsair AI Workstation 300 systems measured 93.55-95.50 t/s Qwen3-Coder, a GMKtec EVO-X2 96GB native Ubuntu run reproduced the guide's Qwen3.6 row within -0.8% pp512 and -1.7% tg128, the same GMKtec class added Qwen3-Coder b9235 follow-up rows and reproduced the MTP route at 93.29 t/s average, a Windows MS-S1-Max report added LM Studio serving evidence, and a tuned Reddit GMKtec report reached about 99.9-100.0 t/s on Qwen3-Coder `Q4_K_S` with thermal/power-policy qualifiers.
- Community wall-power context: Qwen3-Coder around 150 W / 1.6 J/token, Qwen3.6 around 148 W / 2.0 J/token, gpt-oss-120b around 174 W / 3.1 J/token, and Qwen3-Coder-Next around 137 W / 3.4 J/token during sustained generation.
- Includes setup steps, backend choices, raw data, charts, and reproducibility notes.

Repo: https://github.com/hogeheer499-commits/strix-halo-guide

Corrections, other Strix Halo results, and failed experiments are welcome.

## Reddit / Forum Post

Title options:

- I benchmarked local LLMs on AMD Strix Halo 128GB: direct 100 t/s Qwen 30B MoE, 55.6 t/s gpt-oss-120b, 128K context
- Strix Halo local LLM guide with raw CSVs/logs: what works, what does not, and what to run
- AMD Ryzen AI MAX+ 395 local LLM guide: Ollama, llama.cpp, Vulkan/RADV, ROCm, 128K context

Post:

```text
I could not find one complete, copyable guide for running local LLMs on AMD Strix Halo / Ryzen AI MAX+ 395, so I made one:

https://github.com/hogeheer499-commits/strix-halo-guide

This is measured primarily on a Beelink GTR9 Pro with Ryzen AI MAX+ 395, Radeon 8060S, and 128GB unified memory.

Headline results:
- Qwen3-30B-A3B-Instruct-2507 IQ4_XS: 100.04 t/s direct llama.cpp Vulkan/RADV on b9467. Separate general-instruct Qwen route; not a Qwen3-Coder replacement.
- LFM2.5 8B-A1B Q4_K_M: 170.02 t/s generation-only and 168.96 tg128 in the pp512/tg128 latest/int-dot check. Small-MoE speed row; not a 30B-class capability replacement.
- Nemotron 3 Super 120B-A12B UD-IQ4_XS: 18.43 t/s direct `llama-bench` on one 128GB Strix Halo. Current-model capacity proof; not a speed row.
- Qwen3-Coder 30B-A3B Q4_K_S: 98.51 t/s direct llama.cpp Vulkan/RADV speed-first row on b9179
- Qwen3-Coder 30B-A3B UD-Q4_K_XL: 96.76 t/s direct llama.cpp Vulkan/RADV on current b9049
- Qwen3.6 35B-A3B UD-Q4_K_M: 62.56 t/s direct llama.cpp Vulkan/RADV on current b9049
- Qwen3.6 35B-A3B Q4_0: 81.30 t/s direct llama.cpp Vulkan/RADV as a speed-first quant row
- Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn: 101.16 t/s best local average over six llama-server prompts on b9360; repeated t16 runs around 101.1 t/s; 93.29 t/s in the first GMKtec community reproduction on b9235; best local prompt 117.53 t/s, scoped as speculative server evidence
- Gemma 4 26B-A4B QAT matched-head MTP: 102.69 t/s cold repeat, 107.42 t/s T3-only repeat, and 110.00 t/s best repeat on ac4cddeb0, scoped as speculative server evidence
- gpt-oss-120b MXFP4 split GGUF: 55.57 t/s direct llama.cpp Vulkan/RADV on current b9049
- Qwen3.6 35B-A3B through Ollama 0.23.1 API: 50.51 t/s warm average
- Qwen3.6 128K filled-context decode completed at 32.23 t/s without truncation
- Server/concurrency testing included: Vulkan/RADV wins at 1-4 parallel requests; Lemonade ROCm wins aggregate throughput at 8-16 in the measured Qwen3.6 sweep
- HIP/Vulkan crossover testing included: HIP can win prompt processing while Vulkan still wins token generation in local Qwen rows
- Independent community validation included: three Corsair AI Workstation 300 systems measured 93.55-95.50 t/s Qwen3-Coder, a GMKtec EVO-X2 96GB native Ubuntu run reproduced the Qwen3.6 row within -0.8% pp512 and -1.7% tg128, a GMKtec Qwen3-Coder b9235 follow-up added full pp/tg portability evidence, a GMKtec MTP rerun reached 93.29 t/s average, a Windows MS-S1-Max report added LM Studio serving evidence, and a tuned Reddit GMKtec report touched 100.0 t/s with clear thermal/power-policy caveats
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

Highlights: 100.04 t/s direct Qwen3-30B-A3B-Instruct-2507 IQ4_XS, 170.02 t/s generation-only LFM2.5 small-MoE scout, 18.43 t/s Nemotron 3 Super 120B direct GGUF capacity scout, 98.51 t/s Qwen3-Coder speed-first direct llama.cpp Vulkan/RADV, 96.76 t/s balanced Qwen3-Coder direct row on b9049, 101.16 t/s local Qwen3.6 MTP server average on b9360, 102.69 cold / 107.42 T3-only / 110.00 best-repeat t/s Gemma 4 26B-A4B QAT matched-head MTP server route on ac4cddeb0, 93.29 t/s GMKtec community MTP reproduction on b9235, 55.57 t/s gpt-oss-120b MXFP4, 128K context tested, server shootout included, N=3 Corsair validation at 93.55-95.50 t/s, GMKtec EVO-X2 native Ubuntu Qwen3.6 validation within 2%, GMKtec Qwen3-Coder b9235 follow-up data, Windows MS-S1-Max LM Studio evidence, a tuned Reddit GMKtec 99.9-100.0 t/s Qwen3-Coder report, community wall-power rows, a community 3-node USB4 llama.cpp RPC matrix, and USB4 latency tuning data.
```

## Partner / Reviewer Sharing Snippet

```text
Independent AMD Strix Halo / Ryzen AI MAX+ local-AI guide:
https://github.com/hogeheer499-commits/strix-halo-guide

The useful angle for AMD, OEMs, reviewers, and developer-relations teams is adoption friction: the repo turns scattered setup choices and benchmark claims into reproducible public evidence with raw logs, CSVs, charts, caveats, and community validation.

Partner brief:
https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/ONE_PAGE_BRIEF.md
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
