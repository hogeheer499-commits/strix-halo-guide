# Benchmark Data

This directory contains structured benchmark data used by the guide.

The README remains the human-facing guide. These files are the machine-readable source for future charts, dashboards, comparisons, and social images.

Generated SVG summaries live in `../charts/`. Regenerate them after changing CSV data:

```bash
python3 scripts/generate_charts.py
```

## Files

- `headline_claims.csv`: machine-readable map from public README headline claims to structured CSVs, raw evidence, charts, and notes.
- `community_results.csv`: benchmark reports from other Strix Halo systems. These rows are useful external validation but are kept separate from public headline claims.
- `community_power.csv`: community-reported whole-system wall-power and energy-per-token rows. These are useful external validation and tokens-per-watt baselines, but are not local headline claims.
- `beelink_power_telemetry.csv`: local Beelink amdgpu `PPT` telemetry rows. These are useful same-machine power/load context, but they are not wall-power rows.
- `community_rpc.csv`: community-reported multi-node `llama.cpp` RPC rows over USB4 Ethernet. These are advanced capacity/scaling results and are not single-machine headline claims.
- `community_rpc_server.csv`: community-reported `llama-server` TTFT and generation-rate rows for single-box and RPC serving.
- `community_rpc_failures.csv`: community-reported RPC failure rows, including allocator/capacity failure interpretation.
- `community_rpc_model_hashes.csv`: community-reported model source and SHA256 provenance for RPC rows.
- `community_usb4_latency.csv`: community-reported USB4 latency tuning rows for Strix Halo clusters. These are advanced cluster-tuning results and are not relevant to the default single-machine setup.
- `community_usb4_idle_power.csv`: community-reported idle-power measurements for the USB4 `pm_qos` tuning step.
- `benchmarks.csv`: existing short-context and backend benchmark rows already published in the guide.
- `mtp_speculative.csv`: local `llama-server` MTP speculative-decoding rows for Qwen3.6 MTP GGUFs, including official 35B Q8_0, local 35B Q4_K_M requant, 35B IQ4_XS-Q8nextn, and official 27B Q8_0 negative-speed tests.
- `max_performance_campaign.csv`: 2026-05-07 "push the Beelink further" campaign summary, including quant sweeps, same-source HIP/Vulkan, gpt-oss long-context, vLLM AWQ smoke, and negative results.
- `multi_user.csv`: controlled `llama-server` concurrency results with aggregate throughput, per-request throughput, TTFT, and ITL.
- `server_shootout.csv`: practical local-AI-server comparison rows across Ollama, `llama-server`, ROCm builds, and vLLM candidates.
- `backend_crossover.csv`: local HIP versus Vulkan spot-check rows for prompt-processing and token-generation workload split.
- `long_context.csv`: long-context reference measurements.
- `filled_kv_decode.csv`: controlled `llama-server` requests measuring decode after a 32K/64K prompt, including KV-cache type comparisons.
- `smoke_tests.csv`: short validation runs that prove the current stack is healthy before larger benchmark campaigns.
- `raw/`: raw command output for controlled benchmark runs used by current claims.
- `../SMOKE_TESTS.md`: human-readable smoke-test notes and verdicts.
- `../charts/`: generated SVG charts derived from the CSV files.

## Raw Community Artifacts

- `raw/2026-05-07/community-qwen-coder-issue10/`: provenance note mapping the original Qwen3-Coder issue #10 comments to structured community CSV rows.
- `raw/2026-05-09/community-qwen36-issue10/`: raw Qwen3.6 Q4_0/Q4_K_M community rows from issue #10.
- `raw/2026-05-10/community-qwen36-source-build-issue10/`: summary and provenance for Fail-Safe's Qwen3.6 source/build/quant follow-up from issue #10.
- `raw/2026-05-10/community-power-issue6/`: provenance note for Fail-Safe's issue #6 wall-power rows covering Qwen3.6, gpt-oss-120b, and Qwen3-Coder-Next.
- `raw/2026-05-09/community-rpc-issue12/`: raw RPC matrix CSVs from issue #12.
- `raw/2026-05-10/community-rpc-followup-issue12/`: raw MiniMax failure snippets from issue #12.
- `raw/2026-05-10/community-usb4-tuning-issue13/`: raw USB4 tuning CSVs plus the experimental thunderbolt patch and Makefile from issue #13.
- `raw/2026-05-13/community-gmktec-wsl2-issue15/`: issue-comment provenance and TG512 raw CSV row for mottledMantis' GMKtec EVO-X2 WSL2/HIP baseline.
- `raw/2026-05-14/community-gmktec-native-issue16/`: raw native Ubuntu Vulkan/RADV CSV attachments for mottledMantis' GMKtec EVO-X2 reproduction.
- `raw/2026-05-16/latest-stack-b9172/`: local llama.cpp b9172 rerun; Qwen3-Next 80B improved to 59.06 t/s while Qwen3-Coder, Qwen3.6, and gpt-oss did not improve.
- `raw/2026-05-16/ollama-0.24.0-api/`: isolated Ollama 0.24.0 API check plus same-prompt 0.23.1 control; no speedup found.
- `raw/2026-05-16/lemonade-rocm-b1259-spotcheck/`: Qwen3-Next 80B ROCm spot check; HIP won pp512, Vulkan/RADV won tg128.
- `raw/2026-05-16/post-migration-smoke/`: confirms the Windows-partition-to-model-partition migration did not break `/home/hoge-heer/models`.
- `raw/2026-05-16/beelink-power-telemetry/`: local amdgpu `PPT` telemetry during idle, Qwen3-Coder, and Qwen3.6 runs.
- `raw/2026-05-16/lucebox-dflash-preflight/`: Lucebox DFlash/PFlash clone and CMake HIP preflight; blocked locally by missing host ROCm dev toolchain.
- `raw/2026-05-16/npu-fastflowlm-preflight/`: non-invasive NPU visibility check; `amdxdna` and `/dev/accel/accel0` exist, but XRT/FastFlowLM are not installed.
- `raw/2026-05-16/vllm-preflight-refresh/`: refreshed kyuz0 vLLM container version/GPU visibility check.
- `raw/2026-05-16/mtp-server-qwen36-35b/`: `llama-server` MTP speculative-decoding sweep; Qwen3.6 MTP Q4_K_M averaged 87.53 t/s with `draft-n=2`, and repeated a 100.74 t/s best-prompt result with `draft-n=3`.
- `raw/2026-05-17/mtp-iq4xs-q8nextn/`: `llama-server` MTP speculative-decoding sweep with the IQ4_XS-Q8nextn quant; best six-prompt average was 90.80 t/s and best prompt was 110.61 t/s.
- `raw/2026-05-17/qwen3-coder-q4ks-server-ngram/`: Qwen3-Coder Q4_K_S `llama-server` ngram speculative-decoding check; best average was 95.21 t/s, below broad 100 t/s.
- `raw/2026-05-19/mtp-35b-iq4xs-llamacpp-9235/`: latest llama.cpp b9235 MTP rerun with Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn; best six-prompt average was 92.30 t/s and best prompt was 109.21 t/s.
- `raw/2026-05-19/qwen36-27b-mtp-q8-llamacpp-9235/`: official Qwen3.6 27B MTP Q8_0 test; MTP improved 7.74 t/s baseline to 14.59 t/s, but it is not a speed/headline route.

## Status Values

- `measured-local`: measured on this guide's Beelink GTR9 Pro and suitable for current claims.
- `community-reported`: reported by another Strix Halo user through an issue, discussion, or PR; useful validation, but not a headline claim unless explicitly promoted with scope.
- `historical-local`: measured locally in an older stack state; useful context, not the current headline.
- `external-reference`: measured by another source and cited for comparison.
- `smoke-test`: short validation run, not a full benchmark campaign.
- `candidate-not-measured`: tracked candidate for the next campaign; no local performance claim yet.
- `failed-local`: local attempt failed; retained as a negative result so the guide does not imply unsupported combinations work.
- `measured-local-ppt`: measured on this guide's Beelink using amdgpu `PPT` telemetry. This is not wall power.

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

For server shootout rows, also include:

- API surface and endpoint tested
- streaming status
- tool-calling status
- setup friction
- best-fit use case
- limitations

If any of those are unknown, leave the cell blank rather than guessing.

## Headline Claim Rows

Every row in `headline_claims.csv` should point to evidence that already exists
in this repository. Do not add a new headline row until the supporting CSV, raw
evidence path, and chart or explicit `n/a` chart value are known.
