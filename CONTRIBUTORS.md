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

## How To Get Contributor Credit

Benchmark reports in issues are welcome and will be credited when incorporated. Pull requests are even better for future datasets because GitHub will automatically attach commit-level contributor credit after merge.

For repo safety, direct write access is not needed for benchmark contributions. The preferred path is:

1. Open an issue with data, raw logs, commands, and setup details.
2. Open a PR for structured CSV/doc updates if convenient.
3. Maintainer reviews and merges, preserving attribution.

If a community contributor becomes a long-running maintainer, start with issue triage or PR review workflows before considering write access.
