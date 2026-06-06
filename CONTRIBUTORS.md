# Contributors

This guide is maintained as an evidence-first Strix Halo local AI reference. Community reports are credited separately from the primary Beelink headline claims so readers can tell which results were measured locally and which results validate portability across other systems.

## Community Benchmark Contributors

### [Fail-Safe](https://github.com/Fail-Safe)

Fail-Safe materially expanded the guide's evidence base with a Corsair AI Workstation 300 Strix Halo fleet:

- independent Qwen3-Coder Vulkan/RADV reproduction on Fedora 43, kernel 7.0-rc6, Mesa RADV 25.3.6, and kyuz0 containers
- second-session reproducibility for the same Qwen3-Coder row
- N=3 same-SKU cross-box variance across three Corsair AI Workstation 300 systems
- whole-system wall-power and energy-per-token telemetry across Qwen3-Coder, Qwen3.6, gpt-oss-120b, and Qwen3-Coder-Next
- Qwen3.6 Q4_0 and Q4_K_M community quant comparison
- 3-node USB4 `llama.cpp` RPC matrix across Vulkan/RADV and ROCm
- MiniMax-M2.7 ROCm RPC capacity result and Vulkan/RADV allocation failure evidence
- model source and SHA256 provenance for RPC models
- `llama-server` TTFT and streaming generation-rate comparison for 1-node versus 2-node RPC
- USB4 latency tuning, MTU comparison, `pm_qos` idle-power measurement, and experimental thunderbolt throttle patch notes
- Qwen3.6 GGUF source/build follow-up showing source effects, build effects, and guide-flag effects separately

Relevant docs:

- [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md)
- [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md)
- [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md)
- [`data/community_results.csv`](data/community_results.csv)
- [`data/community_power.csv`](data/community_power.csv)
- [`data/community_rpc.csv`](data/community_rpc.csv)
- [`data/community_rpc_server.csv`](data/community_rpc_server.csv)
- [`data/community_rpc_failures.csv`](data/community_rpc_failures.csv)
- [`data/community_rpc_model_hashes.csv`](data/community_rpc_model_hashes.csv)
- [`data/community_usb4_latency.csv`](data/community_usb4_latency.csv)
- [`data/community_usb4_idle_power.csv`](data/community_usb4_idle_power.csv)

### [mottledMantis](https://github.com/mottledMantis)

mottledMantis added the second major independent community validation path, this time on GMKtec EVO-X2:

- first GMKtec EVO-X2 native Ubuntu Vulkan/RADV reproduction for the guide's Qwen3.6 UD-Q4_K_M row
- 96GB LPDDR5X-8000 system, Ubuntu 26.04, kernel 7.0.0-15, Mesa RADV 26.0.3, and llama.cpp b9156
- native result landed within -0.8% pp512 and -1.7% tg128 of the guide's Beelink Qwen3.6 b9049 row
- confirmed the result was stable without `tuned`; an `accelerator-performance` rerun stayed in the same performance class
- contributed the first GMKtec EVO-X2 Qwen3-Coder UD-Q4_K_XL rows on llama.cpp b9235, including both generation-only and full `pp512/tg128` follow-up data
- helped document Qwen3-Coder command-shape sensitivity by providing a full run with different batch, flash-attention, and mmap settings from the Beelink headline row
- independently reproduced the guide's exact Qwen3.6 MTP IQ4_XS-Q8nextn route on GMKtec, reaching 93.29 t/s average with `draft-n=2`
- contributed a WSL2/HIP ROCm 7.2 baseline for the same GMKtec EVO-X2, useful for Windows/WSL2 users even though it is not an apples-to-apples native Vulkan comparison
- provided raw CSV attachments for the native Vulkan/RADV run and detailed setup metadata for BIOS UMA, IOMMU mode, kernel, Mesa, model SHA, build, command, and limitations

Relevant docs:

- [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md)
- [`data/community_results.csv`](data/community_results.csv)
- [`data/raw/2026-05-13/community-gmktec-wsl2-issue15/`](data/raw/2026-05-13/community-gmktec-wsl2-issue15/)
- [`data/raw/2026-05-14/community-gmktec-native-issue16/`](data/raw/2026-05-14/community-gmktec-native-issue16/)
- [`data/raw/2026-05-19/community-gmktec-qwen-coder-issue17/`](data/raw/2026-05-19/community-gmktec-qwen-coder-issue17/)
- [`data/raw/2026-05-19/community-gmktec-mtp-issue18/`](data/raw/2026-05-19/community-gmktec-mtp-issue18/)

### [bennos1911](https://github.com/bennos1911)

bennos1911 added the first Windows / LM Studio / Ryzen AI MAX+ 395 community serving report:

- Minisforum MS-S1-Max with Ryzen AI MAX+ 395 / Radeon 8060S and 128GB memory
- Windows 11 Pro 25H2, AMD Adrenalin 26.5.2, and LM Studio 0.4.15 build 2
- Qwen3.6 35B-A3B Q4_K_M with 96GB AMD Adrenalin Variable Graphics Memory, `n_parallel=4`, and 262K context
- benchmark script, CSV output, and hardware telemetry attachments
- useful Windows-path evidence for beginners, kept separate from native Linux `llama-bench` headline claims

Relevant docs:

- [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md#windows-lm-studio-ms-s1-max-report)
- [`data/community_results.csv`](data/community_results.csv)
- [`data/raw/2026-06-02/community-windows-lmstudio-issue3/`](data/raw/2026-06-02/community-windows-lmstudio-issue3/)

### Look_Over_There

Look_Over_There added a Reddit community report showing a tuned GMKtec EVO-X2 can touch the round 100 t/s mark on the Qwen3-Coder 30B-A3B `Q4_K_S` short-context speed shape:

- GMKtec EVO-X2 with Radeon 8060S / Vulkan RADV `RADV_STRIX_HALO`
- llama.cpp b9467 `1fd5f4803`
- Qwen3-Coder 30B-A3B Instruct `Q4_K_S`
- `llama-bench -fa 1 -n 128 -p 0`
- most runs around 99.90 t/s, best observed 100.0 t/s after about 10 runs
- important qualifier: repasted heatsink, reseated memory thermal pads, reported 15-20C lower CPU/GPU temperatures, and used GPU `high` plus CPU EPP `performance`

Relevant docs:

- [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md#reddit-gmktec-evo-x2-tuned-100-ts-report)
- [`data/community_results.csv`](data/community_results.csv)
- [`data/raw/2026-06-02/community-reddit-look-qwen-coder/`](data/raw/2026-06-02/community-reddit-look-qwen-coder/)

### [boxwrench](https://github.com/boxwrench)

boxwrench added the first Nimo AI Mini PC community bundle:

- Nimo AI Mini PC with Ryzen AI MAX+ 395 / Radeon 8060S and 128GB unified memory
- Ubuntu 25.04, kernel 6.18.1, Mesa RADV 25.2.8, ROCm 7.1.1 baseline, 4GB UMA, and IOMMU enabled
- structured bundle with system metadata, reproducibility notes, manifest, raw benchmark rows, headline-style claim index, and supplemental thermal telemetry
- Qwen 3.6 35B, Qwen3-Coder-Next, Qwen 122B, StepFun Step-3.7-Flash, DFlash, GPT-OSS, and Gemma rows in the raw bundle
- Qwen 122B MTP tuning notes showing that `PMIN` pruning improved validation efficiency but reduced generation throughput
- StepFun MTP notes showing a server/speculative speedup in the contributor's harness
- Gemma 4 QAT Q4_0 follow-up across 12B, 26B-A4B, and 31B, including matched QAT MTP assistant-head rows and concurrency caveats
- compact-chassis thermal/power/noise context useful for buyers and vendors evaluating non-Beelink systems

Relevant docs:

- [`COMMUNITY_NIMO.md`](COMMUNITY_NIMO.md)
- [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md#nimo-ai-mini-pc-large-model-bundle)
- [`data/community_nimo_issue4.csv`](data/community_nimo_issue4.csv)
- [`data/raw/2026-06-03/community-nimo-issue4/`](data/raw/2026-06-03/community-nimo-issue4/)
- [`data/raw/2026-06-06/community-nimo-gemma4-qat-issue4/`](data/raw/2026-06-06/community-nimo-gemma4-qat-issue4/)

## How To Get Contributor Credit

Benchmark reports in issues are welcome and will be credited when incorporated. Pull requests are even better for future datasets because GitHub will automatically attach commit-level contributor credit after merge.

For repo safety, direct write access is not needed for benchmark contributions. The preferred path is:

1. Open an issue with data, raw logs, commands, and setup details.
2. Open a PR for structured CSV/doc updates if convenient.
3. Maintainer reviews and merges, preserving attribution.

If a community contributor becomes a long-running maintainer, start with issue triage or PR review workflows before considering write access.
