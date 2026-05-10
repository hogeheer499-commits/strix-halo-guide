# Contributors

This guide is maintained as an evidence-first Strix Halo local AI reference. Community reports are credited separately from the primary Beelink headline claims so readers can tell which results were measured locally and which results validate portability across other systems.

## Community Benchmark Contributors

### [Fail-Safe](https://github.com/Fail-Safe)

Fail-Safe materially expanded the guide's evidence base with a Corsair AI Workstation 300 Strix Halo fleet:

- independent Qwen3-Coder Vulkan/RADV reproduction on Fedora 43, kernel 7.0-rc6, Mesa RADV 25.3.6, and kyuz0 containers
- second-session reproducibility for the same Qwen3-Coder row
- N=3 same-SKU cross-box variance across three Corsair AI Workstation 300 systems
- whole-system wall-power and energy-per-token telemetry
- Qwen3.6 Q4_0 and Q4_K_M community quant comparison
- 3-node USB4 `llama.cpp` RPC matrix across Vulkan/RADV and ROCm
- MiniMax-M2.7 ROCm RPC capacity result and Vulkan/RADV allocation failure evidence
- model source and SHA256 provenance for RPC models
- `llama-server` TTFT and streaming generation-rate comparison for 1-node versus 2-node RPC
- USB4 latency tuning, MTU comparison, `pm_qos` idle-power measurement, and experimental thunderbolt throttle patch notes

Relevant docs:

- [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md)
- [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md)
- [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md)
- [`data/community_results.csv`](data/community_results.csv)
- [`data/community_rpc.csv`](data/community_rpc.csv)
- [`data/community_rpc_server.csv`](data/community_rpc_server.csv)
- [`data/community_rpc_failures.csv`](data/community_rpc_failures.csv)
- [`data/community_rpc_model_hashes.csv`](data/community_rpc_model_hashes.csv)
- [`data/community_usb4_latency.csv`](data/community_usb4_latency.csv)
- [`data/community_usb4_idle_power.csv`](data/community_usb4_idle_power.csv)

## How To Get Contributor Credit

Benchmark reports in issues are welcome and will be credited when incorporated. Pull requests are even better for future datasets because GitHub will automatically attach commit-level contributor credit after merge.

For repo safety, direct write access is not needed for benchmark contributions. The preferred path is:

1. Open an issue with data, raw logs, commands, and setup details.
2. Open a PR for structured CSV/doc updates if convenient.
3. Maintainer reviews and merges, preserving attribution.

If a community contributor becomes a long-running maintainer, start with issue triage or PR review workflows before considering write access.
