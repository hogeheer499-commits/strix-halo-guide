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
- `community_nimo_issue4.csv`: selected structured rows from boxwrench's Nimo AI Mini PC issue #4 bundle, including Qwen 3.6, Qwen3-Coder-Next, Qwen 122B, StepFun, Gemma 4 QAT/MTP assistant-head rows, DFlash, and thermal-context references. These are community serving/eval rows, not first-party direct `llama-bench` headlines.
- `community_ciru_evox2_metrics.csv`: compact public metric subset from ciru-ai's external GMKtec EVO-X2 / NixOS / IOMMU-on / NPU-aware evidence artifact. The full sanitized CSV/SQLite source stays in [`ciru-ai/strix-halo-evo-x2-evidence`](https://github.com/ciru-ai/strix-halo-evo-x2-evidence). These are community NPU, ROCmFP4, served/API, and quality-eval rows, not first-party Beelink direct `llama-bench` headlines.
- `raw/2026-06-21/rocmfpx-chadrock-ace-saber-repro-attempt/`: earlier first-party Beelink corrected-route attempt for ciru-ai's CHADROCK ACE/SABER ROCmFPX / ROCmFP4 MTP path. The route loaded and served locally, but this first attempt missed the official helper-runner shape and did not reproduce the high-acceptance band.
- `raw/2026-06-24/community-minix-er939-ollama-issue27/`: Minix Elite ER939 Ai community report from issue #27. This adds Ubuntu 26.04 / kernel 7.0.0-22 / Mesa 26.1.3 / Ollama 0.30.10 buyer-path evidence for `qwen3.6:35b-a3b`; metadata is incomplete, so it is not a speed headline.
- `community_power.csv`: community-reported whole-system wall-power and energy-per-token rows. These are useful external validation and tokens-per-watt baselines, but are not local headline claims.
- `beelink_power_telemetry.csv`: local Beelink amdgpu `PPT` telemetry rows. These are useful same-machine power/load context, but they are not wall-power rows.
- `community_rpc.csv`: community-reported multi-node `llama.cpp` RPC rows over USB4 Ethernet. These are advanced capacity/scaling results and are not single-machine headline claims.
- `community_rpc_server.csv`: community-reported `llama-server` TTFT and generation-rate rows for single-box and RPC serving.
- `community_rpc_failures.csv`: community-reported RPC failure rows, including allocator/capacity failure interpretation.
- `community_rpc_model_hashes.csv`: community-reported model source and SHA256 provenance for RPC rows.
- `community_usb4_latency.csv`: community-reported USB4 latency tuning rows for Strix Halo clusters. These are advanced cluster-tuning results and are not relevant to the default single-machine setup.
- `community_usb4_idle_power.csv`: community-reported idle-power measurements for the USB4 `pm_qos` tuning step.
- `benchmarks.csv`: existing short-context and backend benchmark rows already published in the guide.
- `mtp_speculative.csv`: local and community `llama-server` MTP speculative-decoding rows for Qwen3.6 MTP GGUFs and Gemma 4 QAT matched-head routes, including official 35B Q8_0, local 35B Q4_K_M requant, 35B IQ4_XS-Q8nextn, the GMKtec exact-model reproduction, the b9360 100+ t/s MTP rerun, Gemma 4 26B-A4B QAT 102.7 cold / 107.4 T3-only / 110.0 best-repeat t/s server evidence, and official 27B Q8_0/NVFP4 negative-speed tests.
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
- `raw/2026-05-19/community-gmktec-qwen-coder-issue17/`: raw generation-only and pp512/tg128 Qwen3-Coder UD-Q4_K_XL b9235 rows from mottledMantis' GMKtec EVO-X2.
- `raw/2026-05-19/community-gmktec-mtp-issue18/`: Qwen3.6 MTP IQ4_XS-Q8nextn b9235 community reproduction from mottledMantis' GMKtec EVO-X2.
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
- `raw/2026-05-26/latest-llamacpp-b9334/`: latest llama.cpp b9334 / Mesa 26.1.1 spot check. Direct Qwen3-Coder did not beat the current direct headlines, but Qwen3.6 MTP IQ4_XS-Q8nextn improved to a 98.57 t/s six-prompt average with a 116.75 t/s best prompt.
- `raw/2026-05-27/latest-llamacpp-b9360/`: latest llama.cpp b9360 / Mesa 26.1.1 spot check. Direct Qwen3-Coder did not beat the current direct headlines, but Qwen3.6 MTP IQ4_XS-Q8nextn reached a repeat-confirmed 101.1 t/s six-prompt average with `draft-n=2`, `--poll 100`, and `-ub 1024`.
- `raw/2026-06-01/latest-llamacpp-de6f727-safe-clean/`: latest llama.cpp `de6f727aa` / Mesa 26.1.1 spot check. Direct Qwen3-Coder Q4_K_S measured 95.55 t/s tg128 with `mmap=0`, so it did not beat the current b9179 98.51 t/s direct headline.
- `raw/2026-06-01/qwen36-27b-mtp-latest-de6f727/`: latest llama.cpp `de6f727aa` / Mesa 26.1.1 sanity rerun for official Qwen3.6 27B MTP Q8_0. Baseline was 7.61 t/s and `draft-n=3` was 14.69 t/s, confirming this dense Q8 route is useful negative/control evidence rather than a speed path.
- `raw/2026-06-02/reddit-look-int-dot-reproduction/`: exact local reproduction attempt for a Reddit-reported GMKtec Qwen3-Coder 100 t/s command on llama.cpp `1fd5f4803`, plus a Qwen3.6 27B direct follow-up. The default Beelink build path stayed at 96.38-96.72 t/s with `int dot: 0`; a follow-up `glslc v2026.1` build enabled `int dot: 1` but still measured only 95.27-95.91 t/s in the completed checks. Qwen3.6 27B direct measured 7.70 t/s tg128.
- `raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/`: Qwen3-30B-A3B-Instruct-2507 scout on llama.cpp b9467 / Mesa 26.1.1. The `Q4_K_S` quant stayed below the Qwen3-Coder 98.51 t/s headline, but `IQ4_XS` reached 100.58 t/s r20 and 100.04 t/s r50 direct `llama-bench`, making it the first local direct 100+ t/s 30B-class Qwen row. Treat it as a separate general-instruct Qwen route, not as a Qwen3-Coder replacement.
- `raw/2026-06-02/high-power-policy-test/`: short local Beelink follow-up for a community high-power policy / thermal tuning report. GPU `high` plus CPU EPP `performance` improved this short b9467 Qwen3-Coder Q4_K_S run from 95.18 to 96.37 t/s tg128, but it did not reproduce the external 100 t/s GMKtec result and is advanced tuning context only.
- `raw/2026-06-02/community-windows-lmstudio-issue3/`: imported Windows / LM Studio / MS-S1-Max community report from issue #3, including the benchmark script, CSV output, and hardware telemetry. This is serving/API evidence, not a native Linux `llama-bench` comparison.
- `raw/2026-06-02/community-reddit-look-qwen-coder/`: provenance note for Look_Over_There's Reddit GMKtec EVO-X2 tuned Qwen3-Coder `Q4_K_S` report, including the reported 99.9-100.0 t/s result, thermal repaste/pad qualifier, and high-power policy caveat.
- `raw/2026-06-03/community-nimo-issue4/`: imported Nimo AI Mini PC community bundle from issue #4, including system metadata, reproducibility notes, manifest, raw benchmark rows, thermal telemetry, StepFun, Qwen 122B MTP, and Qwen3-Coder-Next follow-up notes. Summarized in `../COMMUNITY_NIMO.md` and `community_nimo_issue4.csv`.
- `raw/2026-06-06/community-nimo-gemma4-qat-issue4/`: Nimo AI Mini PC issue #4 follow-up for Gemma 4 QAT Q4_0 on 12B, 26B-A4B, and 31B, including plain Vulkan baselines, non-QAT MTP heads, matched QAT MTP heads, acceptance rates, power notes, and the original `PARALLEL=2` MTP crash caveat. Atomic PR #26 later fixed that crash upstream; fresh post-merge 2-slot numbers are still needed.
- `raw/2026-06-03/minimax-m27-ud-iq4xs-local-smoke/`: large-model feasibility scout showing MiniMax M2.7 `UD-IQ4_XS` can load and generate locally on one 128GB Strix Halo system. This is capacity/adoption evidence, not a speed headline.
- `raw/2026-06-03/deepseek-v4-flash-q2k-download-attempt/`: DeepSeek V4 Flash `Q2_K` download attempt. The run produced no benchmark claim; it documents 100GB+ model distribution/resume friction.
- `raw/2026-06-03/large-model-feasibility-scan/`: triage notes for large current-model targets such as Kimi K2.6, MiniMax M2.7/M3, DeepSeek V4 Flash, and GLM-5.1. This is adoption-friction evidence, not benchmark output.
- `raw/2026-06-03/qwen3-coder-iq4xs-direct-scout/`: Qwen3-Coder 30B-A3B `IQ4_XS` direct scout. It measured 90.44 t/s tg128 and is a negative/control row showing that `IQ4_XS` alone does not replace the Qwen3-Coder Q4_K_S headline.
- `raw/2026-06-03/qwen3-30b-a3b-neo-max-iq4xs-direct-scout/`: alternate Qwen3 30B-A3B NEO-MAX `IQ4_XS` direct scout. It measured 87.39 t/s tg128 and shows the 2507 100 t/s route does not generalize to every 30B-A3B IQ4_XS file.
- `raw/2026-06-03/qwen35-35b-a3b-iq4xs-direct-scout/`: Qwen3.5 35B-A3B `IQ4_XS` direct scout. It measured 75.22 t/s tg128 and is a current/larger-Qwen comparator, not a speed headline.
- `raw/2026-06-04/latest-model-viral-scan/`: triage notes for fast-moving current model targets, including Gemma 4, LFM2.5, Qwen3.5/Qwen3.6, Kimi, MiniMax, DeepSeek, and Nemotron. Do not treat this note as a benchmark claim unless a linked raw benchmark exists.
- `raw/2026-06-04/gemma-4-12b-it-direct-scout/`: current-model scout for Gemma 4 12B IT `IQ4_XS` and `Q4_K_M` on direct `llama-bench` Vulkan/RADV.
- `raw/2026-06-04/lfm25-8b-a1b-q4km-direct-scout/`: current-model scout for LFM2.5 8B-A1B `Q4_K_M`, useful as a small-MoE speed/currentness comparison.
- `raw/2026-06-04/nemotron-3-nano-30b-a3b-iq4xs-direct-scout/`: Nemotron 3 Nano 30B-A3B `IQ4_XS` direct `llama-bench` scout after the Nemotron 3 Ultra release. This is the practical single-box NVIDIA Nemotron route found in this scan, not a Nemotron 3 Ultra benchmark.
- `raw/2026-06-04/nemotron-3-super-120b-a12b-udiq4xs-direct-scout/`: Nemotron 3 Super 120B-A12B `UD-IQ4_XS` direct `llama-bench` scout. This is a direct 120B-class GGUF capacity/current-model route, not a speed headline.
- `raw/2026-06-04/qwen35-9b-q4km-direct-comparator/`: Qwen3.5 9B `Q4_K_M` comparator for current Gemma/Qwen discussion. Useful context, not a newest-Qwen headline.
- `raw/2026-06-05/model-update-scan/`: latest model/runtime search and dry-run size notes for fast-moving model targets, including Nemotron Ultra/Super, LFM2.5, DeepSeek, Kimi, GLM, and Gemma. These are triage notes unless paired with a raw benchmark directory.
- `raw/2026-06-05/latest-llamacpp-intdot-regression/`: latest/int-dot practical scout for LFM2.5 8B-A1B, Nemotron Nano 30B-A3B, Nemotron Super 120B-A12B, Qwen3-30B-A3B-Instruct-2507, and Qwen3-Coder UD-Q4_K_XL. This adds LFM2.5 small-MoE speed evidence and Nemotron Super capacity evidence; it does not replace the older Qwen3-Coder headline.
- `raw/2026-06-05/deepseek-v4-flash-0xsero-load-failure/`: DeepSeek V4 Flash 0xSero/Spark-Mini smoke attempts. A smaller local file existed, but current local `llama-bench` smoke attempts failed to load it. This is loadability/setup-friction evidence, not a performance claim.
- `raw/2026-06-07/latest-llamacpp-b9544-regression/`: latest `llama.cpp` b9544 Vulkan/RADV regression control for Qwen3-30B-A3B-Instruct-2507, Qwen3-Coder UD-Q4_K_XL, LFM2.5, and Nemotron Super. The sentinel rows showed no b9544 regression.
- `raw/2026-06-07/qwen3-coder-q4ks-b9544-refresh/`: exact SHA-matched Qwen3-Coder 30B-A3B `Q4_K_S` speed-first file redownloaded and rerun on b9544. It reproduced around 98 t/s but did not beat the older b9179 strict-clean 98.51 t/s headline.
- `raw/2026-06-11/latest-llamacpp-ac4cddeb-vulkan-clean/`: latest `llama.cpp` ac4cddeb0 Vulkan/RADV direct controls for Qwen3-30B-A3B-Instruct-2507, Qwen3-Coder Q4_K_S, LFM2.5, Gemma 4 12B/26B QAT, Nemotron Super, Qwen3.6 27B NVFP4, plus DeepSeek V4 Flash Spark-Mini load-failure evidence.
- `raw/2026-06-11/gemma4-26b-qat-mtp-sixprompt-ac4cddeb/`: first-party Gemma 4 26B-A4B QAT `llama-server` six-prompt route with no-spec baseline, matched MTP head, sweep rows, and a 110.00 t/s best repeat. Server/speculative evidence, not direct `llama-bench`.
- `raw/2026-06-12/gemma4-26b-qat-mtp-cold-repeat-ac4cddeb/`: cold repeat of the Gemma 4 26B-A4B QAT matched-head MTP route after stopping nonessential local docflock/VM workload while leaving T3 and Hermes untouched. It measured 102.69 t/s across six prompts.
- `raw/2026-06-12/gemma4-26b-qat-mtp-t3-only-repeat-ac4cddeb/`: T3-only repeat of the same Gemma 4 26B-A4B QAT matched-head MTP route after stopping Hermes, Ollama, RustDesk, docflock/ffmpeg, VM, and browser-class noise. It measured 107.42 t/s across six prompts and explains the gap between the 102.69 t/s cold repeat and 110.00 t/s best repeat.
- `raw/2026-06-12/community-devoidfury-cachyos-rocm-zendnn/`: community Beelink GTR9 Pro CachyOS / ROCm 7.2.4 / ZenDNN backend-crossover report from devoidfury. Qwen3.6 27B MTP `UD-Q6_K_XL` measured 303.20 pp5000 on ROCm versus 155.89 pp5000 on Vulkan, while decode stayed around 8 t/s; VMM and `GGML_HIP_ROCWMMA_FATTN` caveats are preserved.
- `raw/2026-06-14/community-ciru-evox2-nixos-npu-rocmfp4/`: provenance note for ciru-ai's external GMKtec EVO-X2 / NixOS / IOMMU-on / NPU-aware evidence artifact. The full source artifact remains in [`ciru-ai/strix-halo-evo-x2-evidence`](https://github.com/ciru-ai/strix-halo-evo-x2-evidence); this guide imports a compact metric subset in `community_ciru_evox2_metrics.csv`.
- `raw/2026-06-24/community-minix-er939-ollama-issue27/`: provenance note for papagenic's Minix Elite ER939 Ai Ollama 0.30.10 issue #27 report. It is buyer-path evidence for Ubuntu 26.04 / kernel 7.0 / Mesa 26.1.3 on another chassis, not direct `llama-bench` headline evidence.
- `raw/2026-06-21/rocmfp4-crown-halo-dynamic-mtp-smoke/`: first-party Beelink smoke for `jcbtc/qwen3.6-35b-a3b-crown-halo-mtp-dynamic` through the `charlie12345/rocmfp4-llama` HIP-only Distrobox build. The route loads and serves with native MTP, but the local smoke does not reproduce ciru-ai's higher community dynamic-MTP speed band.
- `raw/2026-06-21/rocmfpx-chadrock-ace-saber-helper-repro/`: successful first-party Beelink helper-route repro for ciru-ai's CHADROCK ACE/SABER ROCmFPX / ROCmFP4 MTP path. The pinned `ciru-ai/ROCmFPX` helper runner and CHADROCK model reproduced 139.93-140.40 t/s gen512 on a 3946-token high-acceptance prompt, with gen2048 at 127.77 t/s. Server/speculative evidence, not direct `llama-bench`.
- `raw/2026-06-21/nemotron-3-nano-omni-mxfp4-b9747-smoke/`: first-party Beelink direct `llama-bench` smoke for `unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-GGUF` `MXFP4_MOE` on the official `llama.cpp` b9747 Vulkan binary. It measured 1277.60 pp512 / 56.56 tg128. Useful current NVIDIA Omni/FP4 support evidence, not a speed headline.
- `raw/2026-06-02/modern-model-clean-followup/`: modern-model follow-up after Reddit feedback. Qwen3-Coder-Next 80B-A3B IQ4_XS measured 61.91 t/s tg128 and 738.98 t/s pp512 on b9467. A Qwen3.6 MTP b9360 repeat averaged 97.08 t/s across six prompts, with code prompts above 105 t/s; useful nuance for the experimental server/speculative route, not a new direct headline.
- `raw/2026-06-02/qwen3-coder-next-iq4xs/`: earlier modern Qwen3-Coder-Next 80B-A3B IQ4_XS Vulkan/RADV row. It measured 61.68 t/s tg128 and 735.72 t/s pp512, useful for current-model context but superseded by the b9467 repeat in `raw/2026-06-02/modern-model-clean-followup/`.

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
