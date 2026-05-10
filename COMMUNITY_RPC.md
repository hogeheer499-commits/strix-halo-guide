# Community RPC Results

These results are community-reported by [Fail-Safe](https://github.com/Fail-Safe) in [issue #12](https://github.com/hogeheer499-commits/strix-halo-guide/issues/12). They are kept separate from this guide's single-machine headline claims.

Structured data:

- structured summary: [`data/community_rpc.csv`](data/community_rpc.csv)
- server/TTFT rows: [`data/community_rpc_server.csv`](data/community_rpc_server.csv)
- failure rows: [`data/community_rpc_failures.csv`](data/community_rpc_failures.csv)
- model hashes: [`data/community_rpc_model_hashes.csv`](data/community_rpc_model_hashes.csv)
- raw imported attachment, including the contributor's combined `llama-bench` CSV: [`data/raw/2026-05-09/community-rpc-issue12/`](data/raw/2026-05-09/community-rpc-issue12/)
- raw follow-up failure snippets: [`data/raw/2026-05-10/community-rpc-followup-issue12/`](data/raw/2026-05-10/community-rpc-followup-issue12/)

## Why This Matters

The main guide answers: what can one Strix Halo AI PC do?

This report answers a different practical question:

> If you own multiple Strix Halo boxes, when does `llama.cpp` RPC over USB4 Ethernet help, and when does RPC overhead dominate?

That is rare evidence. It includes a three-machine setup, 1-node / 2-node / 3-node comparisons, two backends, three model sizes, raw CSVs, commands, topology, and failure modes.

## Contributor Credit

Fail-Safe provided:

- three Corsair AI Workstation 300 systems, all Ryzen AI MAX+ 395 / Radeon 8060S / 128GB
- a direct USB4 `thunderbolt-net` triangle mesh between the three boxes
- matched software across the fleet: Fedora 43, kernel 7.0-rc6, Mesa RADV 25.3.6, kyuz0 Vulkan/RADV and ROCm 7.2 containers
- raw `llama-bench -o csv` outputs for 14 successful cells
- clear negative results for failed cells
- exact model sources and SHA256 hashes
- `llama-server` TTFT and streaming generation measurements for 1-node versus 2-node RPC
- practical interpretation of what this means for owners of more than one Strix Halo machine

## Setup

| Item | Reported setup |
|------|----------------|
| Systems | 3x Corsair AI Workstation 300 |
| APU | Ryzen AI MAX+ 395 / Radeon 8060S |
| Memory | 128GB per system |
| OS/kernel | Fedora 43, kernel `7.0.0-0.rc6.49.fc45.x86_64` |
| Vulkan stack | Mesa RADV 25.3.6, kyuz0 `vulkan-radv` container |
| ROCm stack | kyuz0 `rocm-7.2` container |
| Network | USB4 `thunderbolt-net` triangle mesh, 20 Gbps per link, MTU 9000, sub-ms peer latency |
| Workload | `llama-bench -fa 1 -ngl 999 -mmp 0 -p 512 -n 128 -o csv` |

Backend build caveat: the Vulkan and ROCm containers used different llama.cpp builds. Within-backend RPC overhead comparisons are still useful; absolute Vulkan-vs-ROCm comparisons should be read with that caveat.

## USB4 Latency Tuning Follow-Up

Fail-Safe also measured a tuning follow-up in [issue #13](https://github.com/hogeheer499-commits/strix-halo-guide/issues/13) on the same Qwen3-Coder Vulkan/RADV 2-node RPC cell.

Practical result: applying `pm_qos_resume_latency_us=100` on each CPU of each USB4 cluster node reduced ping RTT from about 600-700 us to about 134 us and improved the measured 2-node tg128 row from 75.27 t/s to 76.79 t/s, about +2.0%. See [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md) and [`data/community_usb4_latency.csv`](data/community_usb4_latency.csv).

## Main Takeaways

1. If the model fits on one Strix Halo box, run it on one box for raw single-stream throughput.
2. RPC overhead is real, especially for token generation.
3. Larger models amortize the RPC cost better, but did not make RPC faster than one node when the model already fit locally.
4. For models that do not fit on one box, ROCm RPC can make the model usable.
5. For the 140.8 GB MiniMax-M2.7 test, 2-node ROCm was faster than 3-node ROCm.
6. Vulkan/RADV remains the simple single-box default for generation-heavy Strix Halo use, but it is not a universal answer for huge multi-node models or allocator edge cases.

## Fits-On-One Model: Qwen3-Coder 30B

Model: Qwen3-Coder-30B-A3B UD-Q4_K_XL, 17.7 GB.

| Backend | Nodes | pp512 t/s | tg128 t/s | tg change vs 1 node |
|---------|-------|-----------|-----------|---------------------|
| Vulkan/RADV | 1 | 1391.60 | 95.00 | baseline |
| Vulkan/RADV | 2 | 1352.21 | 75.68 | -20.34% |
| Vulkan/RADV | 3 | 1304.21 | 66.44 | -30.06% |
| ROCm 7.2 | 1 | 1285.12 | 73.97 | baseline |
| ROCm 7.2 | 2 | 1242.45 | 57.92 | -21.70% |
| ROCm 7.2 | 3 | 1203.50 | 49.42 | -33.19% |

Interpretation: sharding a small model that already fits on one box is a throughput loss. This supports a simple beginner rule: use one Strix Halo machine if the model fits.

## Larger Fits-On-One Model: Qwen3-Coder-Next 80B

Model: Qwen3-Coder-Next UD-Q8_K_XL, 86.3 GB.

| Backend | Nodes | pp512 t/s | tg128 t/s | tg change vs 1 node |
|---------|-------|-----------|-----------|---------------------|
| Vulkan/RADV | 1 | 709.75 | 40.11 | baseline |
| Vulkan/RADV | 2 | 690.51 | 34.52 | -13.93% |
| Vulkan/RADV | 3 | 679.93 | 29.43 | -26.63% |
| ROCm 7.2 | 1 | 735.17 | 36.94 | baseline |
| ROCm 7.2 | 2 | 725.77 | 31.32 | -15.20% |
| ROCm 7.2 | 3 | 712.04 | 28.36 | -23.21% |

Interpretation: the 2-node RPC penalty is smaller on the larger model, so the overhead is partly amortized. It still does not beat the one-node path for a model that already fits. ROCm also beat Vulkan on pp512 in this specific large-Q8 prompt-processing row, while Vulkan still won tg128.

## Forced-Sharding Model: MiniMax-M2.7 230B

Model: MiniMax-M2.7 UD-Q4_K_XL, 140.8 GB.

| Backend | Nodes | Result | pp512 t/s | tg128 t/s |
|---------|-------|--------|-----------|-----------|
| Vulkan/RADV | 1 | failed to load | n/a | n/a |
| Vulkan/RADV | 2 | failed to load | n/a | n/a |
| Vulkan/RADV | 3 | skipped | n/a | n/a |
| ROCm 7.2 | 1 | failed to load | n/a | n/a |
| ROCm 7.2 | 2 | worked | 238.62 | 21.41 |
| ROCm 7.2 | 3 | worked | 236.28 | 19.74 |

Interpretation: when sharding is required, use the smallest node count that fits. The third node reduced tg128 by 7.80% compared with 2-node ROCm.

The Vulkan/RADV failure is also useful. The report hit a single allocation failure around 792 MiB even in the 2-node RPC case. That suggests layer sharding does not rescue a tensor-level Vulkan allocation limit. ROCm handled the same MiniMax path.

## Failure Provenance

Fail-Safe followed up with the stderr details for the failed MiniMax cells.

| Backend | Nodes | Failure | Why it matters |
|---------|-------|---------|----------------|
| Vulkan/RADV | 1 | `radv/amdgpu` failed to allocate `830472192` bytes, about 792 MiB, in GTT (`domains: 4`). | This is not simple total-GTT exhaustion; it points to a per-buffer allocation ceiling or contiguous-allocation issue. |
| Vulkan/RADV RPC | 2 | RPC follower hit the same 830472192-byte allocation failure, then the leader saw the remote server crash/disconnect. | Layer sharding does not split individual tensor allocations, so RPC cannot rescue this RADV failure mode. |
| ROCm 7.2 | 1 | Generic model-load failure. | Distinct from Vulkan: ROCm 2-node and 3-node worked, so ROCm 1-node appears to be a true capacity failure for the 140.8 GB model. |

Structured rows: [`data/community_rpc_failures.csv`](data/community_rpc_failures.csv). Raw stderr snippets: [`data/raw/2026-05-10/community-rpc-followup-issue12/`](data/raw/2026-05-10/community-rpc-followup-issue12/).

## Model Provenance

The RPC matrix used Unsloth Dynamic GGUFs:

| Model | Source repo | Quant | Files |
|-------|-------------|-------|-------|
| Qwen3-Coder-30B-A3B-Instruct | `unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF` | UD-Q4_K_XL | 1 GGUF |
| Qwen3-Coder-Next | `unsloth/Qwen3-Coder-Next-GGUF` | UD-Q8_K_XL | 3 shards |
| MiniMax-M2.7 | `unsloth/MiniMax-M2.7-GGUF` | UD-Q4_K_XL | 4 shards |

SHA256 rows: [`data/community_rpc_model_hashes.csv`](data/community_rpc_model_hashes.csv).

## API Serving And TTFT

Fail-Safe also ran the Qwen3-Coder 30B UD-Q4_K_XL path through `llama-server` instead of `llama-bench`, using `/completion` streaming, `cache_prompt: false`, `temperature: 0`, an 83-token prompt, 128 generated tokens, 2 warmups discarded, and 5 measured requests.

| Setup | TTFT mean | Total time mean | Streaming gen rate | Compared with `llama-bench` |
|-------|-----------|-----------------|--------------------|------------------------------|
| 1-node Vulkan/RADV | 201.4 ms | 1584.9 ms | 92.52 t/s | 2.6% below 95.0 t/s `llama-bench` |
| 2-node Vulkan/RADV RPC | 300.8 ms | 2143.1 ms | 69.51 t/s | 8.2% below 75.7 t/s `llama-bench` |

This turns the RPC result from a synthetic benchmark into practical serving evidence:

- single-box `llama-server` overhead is small enough for normal chat/tool use
- RPC adds about 100 ms TTFT on this short prompt
- TTFT variance is much higher under RPC: about 2 ms stdev on 1-node versus about 19 ms on 2-node
- for interactive UX, single-box Strix Halo is the cleaner path when the model fits; RPC remains mainly a capacity tool

Structured rows: [`data/community_rpc_server.csv`](data/community_rpc_server.csv).

## Practical Recommendation

For most Strix Halo users:

- one box plus Vulkan/RADV remains the first path to try for chat, coding, and generation-heavy GGUF inference
- do not use RPC for a model that already fits unless you have a specific reason to trade single-stream speed for multi-node experimentation
- for huge models that exceed one box, try ROCm RPC with the smallest number of nodes that fits
- keep RPC results in community/advanced docs unless they are reproduced locally and scoped clearly

## Source

- GitHub issue: [#12](https://github.com/hogeheer499-commits/strix-halo-guide/issues/12)
- Raw attachment imported here: [`data/raw/2026-05-09/community-rpc-issue12/`](data/raw/2026-05-09/community-rpc-issue12/)
- Structured summary CSV: [`data/community_rpc.csv`](data/community_rpc.csv)
- Server/TTFT CSV: [`data/community_rpc_server.csv`](data/community_rpc_server.csv)
- Failure CSV: [`data/community_rpc_failures.csv`](data/community_rpc_failures.csv)
- Model-hash CSV: [`data/community_rpc_model_hashes.csv`](data/community_rpc_model_hashes.csv)
- Raw follow-up failure snippets: [`data/raw/2026-05-10/community-rpc-followup-issue12/`](data/raw/2026-05-10/community-rpc-followup-issue12/)
- Contributor raw combined CSV: [`data/raw/2026-05-09/community-rpc-issue12/csv-combined-rpc-bench.csv`](data/raw/2026-05-09/community-rpc-issue12/csv-combined-rpc-bench.csv)
