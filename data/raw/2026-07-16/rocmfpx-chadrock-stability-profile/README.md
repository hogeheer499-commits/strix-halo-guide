# ROCmFPX CHADROCK Prompt-Shape Stability Profile

Date: 2026-07-16

System: Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S, 128 GB unified memory.

This follow-up profiles the previously reproduced 140 t/s CHADROCK route
across multiple prompt shapes. It uses the pinned ROCmFPX runner and the exact
ACE/SABER target-plus-MTP artifact instead of treating the 3946-token result as
a universal server speed.

## Reproducibility Pin

- ROCmFPX commit: `deaa996dab90b3ca6dd3ae5d453bedfcd983012d`
- runner version: `17 (deaa996)`
- runner SHA-256: `7ad01144ed7a9f2c46cccd64c780ea7c2793e50d256d1d5e2e702aeb25138b75`
- model: `Qwen3.6-35B-A3B-NSC-ACE-SABER-MTP-F16-to-ROCmFP4-STRIX_LEAN.gguf`
- model SHA-256: `6a635d1d8ac4af8f2c4ca6ff528bc6bad9b3a6d45e8630ef6e5728f04898eeed`

The server ran through the `vllm-gfx1151` Distrobox with the pinned ROCmFPX
libraries. Both target and draft used Vulkan device 0. The server used a 32K
context, F16 KV, batch 2048, micro-batch 512, and strict speculative decoding.
Each request explicitly used `n_max=4`, `n_min=0`, and `p_min=0.25`.

## Result

| Prompt profile | Prompt tokens | Decode mean | Range | Draft acceptance mean |
| --- | ---: | ---: | ---: | ---: |
| Approx. 1K | 984 | 78.00 t/s | 75.36-80.67 | 41.93% |
| Reference 4K | 3,946 | **141.37 t/s** | **140.84-141.79** | **100.00%** |
| Approx. 8K | 7,893 | 83.85 t/s | 79.31-86.14 | 51.28% |
| Approx. 16K | 15,787 | 107.23 t/s | 78.46-123.18 | 83.64% |

All rows use three repeats, temperature zero, 512 requested output tokens,
`ignore_eos=true`, and prompt caching disabled. The 3946-token reference shape
is a repeat-confirmed 141.37 t/s advanced-server result. It is not evidence
that arbitrary 4K prompts, longer contexts, or ordinary chats will run at that
speed.

The useful finding is the relationship between MTP acceptance and served
decode: prompt length alone does not predict throughput. The exact generated
token pattern can make the draft head highly predictable, so operators should
measure their real workload rather than copy one headline number.

## Evidence

- [`profile-summary.json`](profile-summary.json): repeat-aware profile summary
- [`profile-rows.json`](profile-rows.json): all per-request timing and acceptance rows
- [`run-profile.py`](run-profile.py): exact request harness
- [`prompt_3946_reference.txt`](prompt_3946_reference.txt): reference prompt
- `*.request.json` and `*.response.json`: complete request/response pairs
- [`server.log`](server.log): complete server initialization and timing log
- [`telemetry.csv`](telemetry.csv) and [`telemetry-summary.json`](telemetry-summary.json)
- [`runner-commit.txt`](runner-commit.txt), [`llama-server.sha256`](llama-server.sha256), and [`model.sha256`](model.sha256)

This is an experimental ROCmFPX/CHADROCK server/MTP route, not direct
`llama-bench`, not an Ollama result, and not the beginner default. The sysfs
PPT values are package telemetry rather than wall-power measurements.
