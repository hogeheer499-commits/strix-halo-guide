# Benchmark Results - Current Snapshot

This file is the compact benchmark source-of-truth for numbers already published in the README. It reconciles historical and current measurements so old ROCm, driver, serving, and long-context notes do not contradict the current guide.

## Current System Snapshot

Latest measured host audit on 2026-07-16:

| Component | Current State |
|-----------|---------------|
| System | Beelink GTR9 Pro |
| CPU | AMD Ryzen AI MAX+ 395, 16C/32T |
| GPU | Radeon 8060S, gfx1151, RADV STRIX_HALO |
| RAM | 124GiB OS-visible unified memory |
| Kernel | 6.19.4-061904-generic |
| Mesa RADV | 26.1.4, kisak-mesa PPA |
| Ollama | 0.31.2 installed service; 0.31.1/0.31.2/0.32.0 isolated comparison; isolated 0.32.3 qualification |
| AMDVLK | Removed |
| linux-firmware | 20240318.git3b128b60-0ubuntu2.27 |
| GPU clock | 2900 MHz selected during measured runs |
| July 16 measured power state | Desktop `performance`; AMDGPU DPM `high`; nonessential desktop processes paused for the controlled sentinel campaigns |

Historical benchmark runs below were measured on 2026-03-20, 2026-03-21, and 2026-04-26 with `tuned accelerator-performance` active. The 2026-05-07 latest-stack rerun confirms `tuned accelerator-performance` active, Mesa RADV 26.0.6, AMDVLK absent, linux-firmware safe, GPU clock at 2900 MHz, llama.cpp b9049, and Ollama 0.23.1. The 2026-05-16 spot check tested llama.cpp b9172 and an isolated Ollama 0.24.0 binary without changing the installed Ollama service. The 2026-05-26 spot check used Mesa RADV 26.1.1 and llama.cpp b9334. The 2026-05-27 spot check used the same Mesa/RADV stack and llama.cpp b9360. The 2026-05-31 spot check tested latest llama.cpp b9442 for the direct Qwen3-Coder speed-first path and found no new headline. The 2026-06-01 spot check updated the same latest-stack worktree to `de6f727aa` and again found no new Qwen3-Coder headline. The 2026-06-02 b9467 scout found a separate Qwen3-30B-A3B-Instruct-2507 IQ4_XS direct route above 100 t/s. The 2026-06-05 latest/int-dot scout added LFM2.5 small-MoE speed evidence and Nemotron 3 Super 120B-class direct GGUF capacity evidence. The 2026-06-07 b9544 regression control showed no regression on the Vulkan/RADV sentinel rows and redownloaded the exact Qwen3-Coder `Q4_K_S` speed-first file for a current-build control. The 2026-06-11 ac4cddeb0 controls kept the direct Qwen3-30B route above 100 t/s, kept LFM2.5 in the 170 t/s class, kept Nemotron Super directly runnable, added Gemma 4 12B/26B QAT direct rows, and documented Qwen3.6 27B NVFP4 as a negative speed route. The 2026-06-11/12 Gemma 4 26B-A4B QAT matched-head MTP runs are server/speculative rows and are summarized in [`MTP_SPECULATIVE_DECODING.md`](MTP_SPECULATIVE_DECODING.md), not merged into direct `llama-bench` claims. The 2026-07-13 b9979 campaign is a separate aggregate-concurrency track: it validates an opt-in AMD/RADV density gate on 30B 128-expert/top-8 and 80B 512-expert/top-10 models and is summarized in [`MOE_CONCURRENCY.md`](MOE_CONCURRENCY.md), not merged into direct single-stream headlines. On 2026-07-16, an official b10034 Vulkan sentinel confirmed that the stock 8-to-9 sequence cliff still exists on both model shapes; a controlled Ollama 0.31.1/0.31.2/0.32.0 comparison found no material version regression; and current Nemotron, AgentWorld, Omni, Audex, and CHADROCK routes were rechecked. The same campaign reproduced Step 3.7 Flash as a separate 198B agent/MTP capacity route with 4K/16K/48K served rows, native tool calling, and 256K allocation, then replaced the old DeepSeek V4 ordinary-GGUF blocker with a direct 284.33B load/basic-correctness pass. Those dated results are summarized below and in [`CURRENT_MODELS.md`](CURRENT_MODELS.md).

## 2026-07-16 Current Runtime And Model Sentinel

These rows answer three practical questions: whether the multi-user Vulkan cliff still exists, whether the current Ollama version is slower, and which recent local-AI model routes are genuinely runnable on one 128 GB Strix Halo system. Direct, server/speculative, text-only, and multimodal results remain separate.

| Route | Result | Practical read |
| --- | ---: | --- |
| Official llama.cpp b10034, Qwen3-Coder 30B-A3B, stock Vulkan np8 to np9 | 232.69 to 145.79 aggregate t/s | The 8-to-9 cliff persists: -37.34%. |
| Official llama.cpp b10034, Qwen3-Next 80B-A3B, stock Vulkan np8 to np9 | 144.61 to 98.78 aggregate t/s | A second MoE shape confirms the cliff: -31.69%. |
| Ollama 0.31.1 / 0.31.2 / 0.32.0, same cache and prompt | 72.55 / 73.19 / 73.20 t/s | No material version regression in this controlled check. The installed buyer path remains 0.31.2 until a normal package upgrade and host reboot are tested. |
| CHADROCK ACE/SABER ROCmFPX MTP, exact 3946-token reference shape | 141.37 t/s mean, 100% draft acceptance | Highest repeat-confirmed server/speculative profile here, but prompt-shape sensitive and not a direct `llama-bench` result. |
| Step 3.7 Flash 198B-A11B ROCmFPX Q3 plus Q8 MTP draft | 23.84 t/s 4K no-spec; 34.50 t/s 4K MTP; 33.83 t/s 16K MTP | 44.68% MTP uplift on the matched 4K server baseline. Native tool call and 256K allocation also passed; server/capacity evidence, not direct `llama-bench`. |
| DeepSeek V4 Flash 284B `UD-IQ2_XXS`, b10034 | 155.64 pp512 / 13.27 tg128 | Pinned 90.86GB ordinary GGUF loaded, generated, and answered a deterministic check correctly. Low-bit current capacity evidence, not a speed or broad quality recommendation. |
| ROCm 7.14 / PyTorch 2.11 / vLLM, Qwen3-0.6B FP16, hipBLASLt on versus off | +40.50% / +38.96% / +41.54% aggregate throughput at concurrency 8/9/16 | Reproduces AMD's Ryzen AI batch-8+ workaround in an isolated official image. Small-model server A/B; no direct GGUF or practical 27B/35B claim. |
| Official `llama.cpp` b10046 ROCm/HIP, Qwen3-0.6B Q8_0 | 4666.05 pp512 / 208.73 tg128; 120,124 MiB free UMA detected | Historical small-model allocation sentinel. It logged `ROCm_Host` buffers, but open issue #26209/PR #25863 means it did not qualify long-context, multimodal, multi-slot, or practical-model correctness. |
| Nemotron 3 Nano Omni 30B-A3B MXFP4, b10034 | 64.26 tg128 | Exact-artifact runtime improvement versus the earlier 56.56 t/s b9747 row. |
| Nemotron Cascade 2 30B-A3B IQ4_XS | 78.95 tg128 | Current NVIDIA-branded direct text route with small correctness checks. |
| Qwen AgentWorld 35B-A3B IQ4_XS | 65.65 tg128 | Runnable agent/environment route with a 128K Q8 KV allocation smoke. |
| Nemotron 3 Nano Omni NVFP4 plus F16 projector | 53.21 tg128 plus image OCR smoke | Experimental multimodal route; OCR smoke is not a broad vision or audio quality claim. |
| Audex text GGUF MXFP4 | 60.73 tg128 | Portable text route only. Full audio requires a separate runtime, and the model license is NVIDIA OneWay Noncommercial. |

Raw evidence: [`data/raw/2026-07-16/`](data/raw/2026-07-16/). The structured concurrency sentinel is in [`data/moe_density_gate_summary.csv`](data/moe_density_gate_summary.csv); direct rows, including the historical b10046 HIP allocation sentinel, are in [`data/benchmarks.csv`](data/benchmarks.csv); server/speculative rows are in [`data/mtp_speculative.csv`](data/mtp_speculative.csv); and the ROCm 7.14 vLLM A/B is in [`data/rocm_714_hipblaslt_ab.csv`](data/rocm_714_hipblaslt_ab.csv).

## Top-Line Model Results

| Model | Backend / Build | Quant | pp512 | tg128 | Notes |
|-------|-----------------|-------|-------|-------|-------|
| LFM2.5 8B-A1B | Vulkan RADV, llama.cpp ac4cddeb0 | Q4_K_M | 3364 | **171.17** | 2026-06-11 latest upstream control; remains a small-MoE speed row, not a 30B-class replacement |
| Qwen3-30B-A3B-Instruct-2507 | Vulkan RADV, llama.cpp ac4cddeb0 | IQ4_XS | 1431 | **100.38** | 2026-06-11 latest upstream control; keeps the separate direct 30B-class Qwen route above 100 t/s |
| Gemma 4 26B-A4B IT QAT | Vulkan RADV, llama.cpp ac4cddeb0 | UD-Q4_K_XL | 1432 | **74.80** | 2026-06-11 direct current Google-model baseline; paired with the separate matched-head MTP server route |
| Nemotron 3 Super 120B-A12B | Vulkan RADV, llama.cpp ac4cddeb0 | UD-IQ4_XS | 296 | **18.24** | 2026-06-11 latest upstream control; 120B-class direct GGUF capacity route still runs on one 128GB Strix Halo system |
| LFM2.5 8B-A1B | Vulkan RADV, llama.cpp b9544 | Q4_K_M | 3398 | **176.48** | 2026-06-07 latest b9544 control; small-MoE speed row, not a 30B-class replacement |
| Qwen3-30B-A3B-Instruct-2507 | Vulkan RADV, llama.cpp b9544 | IQ4_XS | 1438 | **103.18** | 2026-06-07 latest b9544 control; confirms the separate direct 30B-class Qwen route remains above 100 t/s |
| Qwen3-30B-A3B-Instruct-2507 | Vulkan RADV, llama.cpp b9467 | IQ4_XS | 1416 | **100.04** | First local direct `llama-bench` row above 100 t/s; separate general-instruct Qwen route, not the Qwen3-Coder headline |
| Nemotron 3 Super 120B-A12B | Vulkan RADV, llama.cpp b9544 | UD-IQ4_XS | 297 | **18.93** | 2026-06-07 latest b9544 control for the 120B-class direct GGUF capacity route |
| LFM2.5 8B-A1B | Vulkan RADV, llama.cpp 2016bf2 | Q4_K_M | 3415 | **168.96** | 2026-06-05 latest/int-dot small-MoE scout; generation-only p0/n128 reached 170.02 t/s |
| Nemotron 3 Super 120B-A12B | Vulkan RADV, llama.cpp 2016bf2 | UD-IQ4_XS | 295 | **18.43** | 2026-06-05 direct 120B-class GGUF capacity/current-model proof, not a speed result |
| Nemotron 3 Nano 30B-A3B | Vulkan RADV, llama.cpp 2016bf2 | IQ4_XS | 1312 | **75.97** | Practical NVIDIA 30B-class route from the 2026-06-05 latest/int-dot scout |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9179 | Q4_K_S | 1396 | **98.51** | 2026-05-16 strict-clean r50 speed-first quant confirmation |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9544 | Q4_K_S | 1406 | 98.02 | 2026-06-07 exact SHA-matched speed-first control; generation-only p0/n128 measured 98.49 t/s; no new headline versus b9179 |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9544 | UD-Q4_K_XL | 1400 | 97.08 | 2026-06-07 balanced-UD control; stays in the 96-97 t/s class |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp 2016bf2 | UD-Q4_K_XL | n/a | 92.84 | 2026-06-05 generation-only latest/int-dot check; below the older balanced b9049 96-97 t/s row |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9453-7 | Q4_K_S | 1384 | 95.55 | Latest direct rerun; no new headline versus b9179 |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9442 | Q4_K_S | 1376 | 93.85 | Latest direct rerun; no new headline versus b9179 |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9360 | Q4_K_S | 1409 | 97.23 | Latest direct rerun; better than b9334 but no new direct headline |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9334 | Q4_K_S | 1401 | 96.27 | Latest direct rerun; no new headline versus b9179 |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9049 | UD-Q4_K_XL | 1321 | **96.76** | Max-performance guide-flags r20 confirmation; balanced UD default |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9360 | UD-Q4_K_XL | 1399 | 92.60 | Latest direct balanced-UD rerun; no new headline |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9334 | UD-Q4_K_XL | 1402 | 94.15 | Latest direct balanced-UD rerun; no new headline |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9179 | Q4_K_S | 1387 | **97.22** | Earlier 2026-05-16 speed-first quant sweep before strict host-state fix |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9010 | UD-Q4_K_XL | 1346 | **97.24** | Previous May peak |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b8460 | UD-Q4_K_XL | 1342 | **87.11** | Previous coding MoE headline |
| Qwen3.6 35B-A3B | Vulkan RADV, llama.cpp b9049 | Q4_0 | 1244 | **81.30** | Fastest measured speed-first quant; lower-quality tradeoff |
| Qwen3.6 35B-A3B | Vulkan RADV, llama.cpp b9049 | Q4_K_M | 1106 | **76.94** | Fast balanced Strix quant candidate |
| Qwen3.6 35B-A3B | Vulkan RADV, llama.cpp b9049 | UD-Q4_K_M | 1059 | **62.56** | Clean latest-stack rerun |
| Qwen3.6 35B-A3B | Vulkan RADV, llama.cpp b9010 | UD-Q4_K_M | 1109 | **63.06** | Previous May UD rerun |
| Qwen3.6 35B-A3B | Vulkan RADV, llama.cpp b8460 | Q4_K_M | 1064 | **63.76** | Recommended all-rounder |
| Qwen3.5 35B-A3B | Vulkan RADV, llama.cpp b8460 | Q4_K_M | 1080 | **64.85** | Used for backend/build comparison |
| gpt-oss-120b | Vulkan RADV, llama.cpp b9049 | MXFP4 MoE | 727 | **55.57** | 117B-parameter open-weight MoE loaded from split GGUF |
| Qwen3-Next 80B-A3B | Vulkan RADV, llama.cpp b9172 | UD-Q4_K_XL | 752 | **59.06** | Latest-stack r20 confirmation; best current 80B Qwen-family path |
| Qwen3-Next 80B-A3B | Vulkan RADV, llama.cpp b8933 | UD-Q4_K_XL | 657 | **54.92** | 80B MoE, 256K context capable |
| Gemma 4 26B-A4B | Vulkan RADV, llama.cpp b8933 | UD-Q4_K_M | 1142 | **48.46** | Slower than Qwen MoE at similar active params |
| Llama 4 Scout 109B | Vulkan RADV, llama.cpp b8933 | Q4_K_M | 331 | **18.32** | 109B params on one mini PC |
| Llama 3.1 70B | Ollama Vulkan RADV | Q4_K_M | 22-80 | **4.7-4.9** | Dense 70B, bandwidth-bound |
| Qwen3 0.6B | Vulkan RADV, llama.cpp | Q8_0 | 13112 | **266** | Small-model speed ceiling |

## 2026-06-02 Qwen3-30B-A3B-Instruct-2507 Direct Scout

Measured on the same Beelink GTR9 Pro with llama.cpp b9467 / `1fd5f4803`, Vulkan/RADV, and Mesa 26.1.1. Raw data lives under [`data/raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/`](data/raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/).

| Route | Result | Read |
|-------|--------|------|
| Qwen3-30B-A3B-Instruct-2507 `Q4_K_S`, `pp512/tg128`, r20 | 94.37 tg128, 1272.56 pp512 | Fast, but below the Qwen3-Coder 98.51 t/s direct headline. |
| Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`, `pp512/tg128`, r20 | 100.58 tg128, 1418.23 pp512 | First confirmed local direct 100+ t/s row in this scout. |
| Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`, `-p 0 -n 128`, r20 | 100.40 tg128 | Generation-only shape also stayed above 100 t/s. |
| Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`, `pp512/tg128`, r50 | 100.04 tg128, 1416.03 pp512 | Longest confirmation; used for the headline claim index. |

Takeaway: this is the first local direct `llama-bench` row above 100 t/s on Strix Halo, but it is a separate general-instruct Qwen3 route. Keep it distinct from the Qwen3-Coder 30B 98.51 t/s speed-first headline, the balanced Qwen3-Coder UD row, and the Qwen3.6 MTP server/speculative route.

## 2026-06-05 Latest/Int-Dot Current-Model Scout

Measured on the same Beelink GTR9 Pro with a newer local `llama.cpp` build whose Vulkan device line reports `int dot: 1`. Raw data lives under [`data/raw/2026-06-05/latest-llamacpp-intdot-regression/`](data/raw/2026-06-05/latest-llamacpp-intdot-regression/).

| Route | Result | Read |
|-------|--------|------|
| LFM2.5 8B-A1B `Q4_K_M`, pp512/tg128 r5 | 168.96 tg128, 3414.61 pp512 | Fastest current small-MoE scout here. Useful speed/currentness hook, but not a 30B-class capability replacement. |
| LFM2.5 8B-A1B `Q4_K_M`, `-p 0 -n 128`, r20 | 170.02 tg128 | Generation-only confirmation for the small-MoE speed row. |
| Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`, pp512/tg128 r3 | 98.32 tg128, 1447.43 pp512 | Still close to the earlier 100.04 t/s row, but this latest/int-dot check did not replace it. |
| Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`, `-p 0 -n 128`, r20 | 99.10 tg128 | Generation-only latest/int-dot check, below the earlier b9467 100.04 t/s r50 headline. |
| Nemotron 3 Nano 30B-A3B `IQ4_XS`, pp512/tg128 r5 | 75.97 tg128, 1312.47 pp512 | Practical NVIDIA 30B-class direct route. |
| Nemotron 3 Super 120B-A12B `UD-IQ4_XS`, pp512/tg128 r3 | 18.43 tg128, 294.99 pp512 | Direct 120B-class MoE GGUF capacity/current-model proof on one 128GB Strix Halo system. |
| Qwen3-Coder 30B-A3B `UD-Q4_K_XL`, `-p 0 -n 128`, r20 | 92.84 tg128 | Useful negative/control row; below the older b9049 96-97 t/s balanced row. |

Takeaway: the 2026-06-05 check improves the current-model map rather than replacing the Qwen3-Coder headline. LFM2.5 is the small-MoE speed winner, Nemotron Super is the 120B-class direct capacity route, and Qwen3-Coder still keeps its older b9179 speed-first and b9049 balanced rows.

## 2026-06-07 Latest b9544 Regression Control

Measured on the same Beelink GTR9 Pro with llama.cpp b9544 / `98d5e8ba8`, Vulkan/RADV, Mesa 26.1.2, and explicit `-dev Vulkan0`. Raw data lives under [`data/raw/2026-06-07/latest-llamacpp-b9544-regression/`](data/raw/2026-06-07/latest-llamacpp-b9544-regression/).

| Route | Result | Read |
|-------|--------|------|
| Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`, pp512/tg128 r10 | 103.18 tg128, 1438.10 pp512 | Latest b9544 keeps the separate 30B-class Qwen route above 100 t/s. |
| Qwen3-Coder 30B-A3B `Q4_K_S`, pp512/tg128 r50 | 98.02 tg128, 1406.45 pp512 | Exact SHA-matched speed-first file rerun on b9544. This is close to the b9179 98.51 t/s headline but does not beat it. |
| Qwen3-Coder 30B-A3B `Q4_K_S`, `-p 0 -n 128`, r20 | 98.49 tg128 | Generation-only control for the community-style p0 shape; still not a stable first-party 100 t/s Qwen3-Coder row. |
| Qwen3-Coder 30B-A3B `UD-Q4_K_XL`, pp512/tg128 r5 | 97.08 tg128, 1399.98 pp512 | Balanced coding control stays in the 96-97 t/s class. |
| LFM2.5 8B-A1B `Q4_K_M`, pp512/tg128 r10 | 176.48 tg128, 3398.36 pp512 | Latest b9544 does not regress the small-MoE speed route. |
| Nemotron 3 Super 120B-A12B `UD-IQ4_XS`, pp512/tg128 r3 | 18.93 tg128, 297.14 pp512 | Latest b9544 does not regress the 120B-class direct GGUF capacity route. |

Takeaway: users do not need to pin away from b9544 for these Vulkan/RADV sentinel rows. The exact Qwen3-Coder `Q4_K_S` file now reproduces around 98 t/s on b9544, but the direct first-party Qwen3-Coder headline remains the older strict-clean b9179 98.51 t/s r50 row.

## 2026-06-01 Latest de6f727 Direct Spot Check

Measured on the same Beelink GTR9 Pro after a clean pass that preserved workspace-critical services and paused nonessential benchmark noise where safe. Raw data lives under [`data/raw/2026-06-01/latest-llamacpp-de6f727-safe-clean/`](data/raw/2026-06-01/latest-llamacpp-de6f727-safe-clean/).

| Route | Result | Read |
|-------|--------|------|
| llama.cpp `de6f727aa` (`b9453-7`), Qwen3-Coder 30B Q4_K_S direct `llama-bench`, `mmap=0` | 95.55 tg128, 1384.30 pp512 | Latest upstream did not beat the existing b9179 98.51 t/s speed-first headline. |
| Same run with default `mmap=1` | 94.20 tg128, 1371.77 pp512 | Slightly slower in this check; kept as raw evidence only. |

Takeaway: latest `de6f727aa` did not create a new direct Qwen3-Coder headline. The direct speed-first headline remains the older strict-clean b9179 r50 row at 98.51 t/s.

## 2026-05-31 Latest b9442 Direct Spot Check

Measured on the same Beelink GTR9 Pro after a safe-clean pass that preserved workspace-critical services. Raw data lives under [`data/raw/2026-05-31/`](data/raw/2026-05-31/).

| Route | Result | Read |
|-------|--------|------|
| llama.cpp b9442, Qwen3-Coder 30B Q4_K_S direct `llama-bench` | 93.85 tg128, 1376.37 pp512 | Latest upstream did not beat the existing b9179 98.51 t/s speed-first headline. |
| Same-state b9360 Qwen3-Coder 30B Q4_K_S control | 95.35 tg128, 1384.21 pp512 | Same host state also stayed below the earlier b9360 97.23 t/s r20 row, so do not promote this as a regression claim without more repeats. |
| Same-state b9187 Qwen3-Coder 30B Q4_K_S `-t 15` control | 95.09 tg128, 1388.21 pp512 | Older near-99 scout route did not reproduce a higher result in this short control run. |

Takeaway: latest b9442 did not create a new direct Qwen3-Coder headline. These are useful negative/control rows only; the direct speed-first headline remains the older strict-clean b9179 r50 row at 98.51 t/s.

## 2026-05-27 Latest b9360 Spot Check

Measured on the same Beelink GTR9 Pro after pausing benchmark noise while leaving the normal workspace dependency running. Raw data lives under [`data/raw/2026-05-27/latest-llamacpp-b9360/`](data/raw/2026-05-27/latest-llamacpp-b9360/).

| Route | Result | Read |
|-------|--------|------|
| llama.cpp b9360, Qwen3-Coder 30B Q4_K_S direct `llama-bench` | 97.23 tg128, 1408.59 pp512 | Better than b9334 direct, but still below the b9179 98.51 t/s strict-clean row. |
| llama.cpp b9360, Qwen3-Coder 30B UD-Q4_K_XL direct `llama-bench` | 92.60 tg128, 1398.69 pp512 | No new balanced headline; below the b9049/b9010 96-97 t/s rows. |
| llama.cpp b9360, Qwen3.6 35B MTP IQ4_XS-Q8nextn, no MTP | 74.88 t/s average over six prompts | Current no-speculative server baseline. |
| llama.cpp b9360, Qwen3.6 35B MTP IQ4_XS-Q8nextn, `draft-n=2`, `-ub 512` | 99.56 t/s best default-ubatch average; best prompt 108.28 t/s | Very close to 100 t/s, but still below it without the ubatch change. |
| llama.cpp b9360, Qwen3.6 35B MTP IQ4_XS-Q8nextn, `draft-n=2`, `-ub 1024` | **101.16 t/s** best six-prompt average; t16 repeats **101.15 / 101.10 / 101.06 t/s** | First repeated local broad 100+ t/s MTP server route. |
| llama.cpp b9360, Qwen3.6 35B MTP IQ4_XS-Q8nextn, `draft-n=3`, `-ub 1024` | 99.83 t/s average; best prompt 117.53 t/s | Higher single-prompt peak, lower broad average than draft-n=2. |

Takeaway: latest b9360 did not improve the direct Qwen3-Coder headline, but it did create the first repeat-confirmed local MTP server route above 100 t/s across the six-prompt harness. Keep these categories separate: direct `llama-bench` remains 98.51 t/s speed-first / 96-97 t/s balanced, while MTP is now about 101.1 t/s as an advanced server/speculative route.

## 2026-05-26 Latest b9334 Spot Check

Measured on the same Beelink GTR9 Pro after pausing benchmark noise while leaving the normal workspace dependency running. Raw data lives under [`data/raw/2026-05-26/latest-llamacpp-b9334/`](data/raw/2026-05-26/latest-llamacpp-b9334/).

| Route | Result | Read |
|-------|--------|------|
| llama.cpp b9334, Qwen3-Coder 30B Q4_K_S direct `llama-bench` | 96.27 tg128, 1401.20 pp512 | No new direct headline; slower than the b9179 98.51 t/s strict-clean row. |
| llama.cpp b9334, Qwen3-Coder 30B UD-Q4_K_XL direct `llama-bench` | 94.15 tg128, 1402.17 pp512 | No new balanced headline; below the b9049/b9010 96-97 t/s rows. |
| Same-state b9179 Qwen3-Coder Q4_K_S control | 97.61 tg128, 1409.36 pp512 | Confirms b9334 itself did not improve direct generation in this check. |
| llama.cpp b9334, Qwen3.6 35B MTP IQ4_XS-Q8nextn, no MTP | 74.39 t/s average over six prompts | Current no-speculative server baseline. |
| llama.cpp b9334, Qwen3.6 35B MTP IQ4_XS-Q8nextn, `draft-n=2` | 96.14 t/s average; best prompt 107.24 t/s | Strong improvement over b9235 draft-n=2. |
| llama.cpp b9334, Qwen3.6 35B MTP IQ4_XS-Q8nextn, `draft-n=3` | **98.57 t/s** best six-prompt average; best prompt **116.75 t/s** | Former best local MTP route before the b9360 `-ub 1024` rerun. |
| llama.cpp b9334, Qwen3.6 35B MTP IQ4_XS-Q8nextn, `draft-n=4` | 87.89 t/s average | Higher draft depth hurt average stability. |
| llama.cpp b9334, synthetic512/ignore-EOS MTP variant | 93.93 t/s average | Synthetic prompt variant did not improve the broad average. |

Takeaway: latest b9334 did not improve the direct Qwen3-Coder headline, but it materially improved the experimental MTP server path. It was later superseded by the b9360 MTP rerun at about 101.1 t/s. Keep these categories separate: direct `llama-bench` remains 98.51 t/s speed-first / 96-97 t/s balanced.

## 2026-05-16 Latest-Stack Spot Check

Measured on the same Beelink GTR9 Pro after pausing non-essential GUI/noise processes while leaving the normal workspace session active. Raw data lives under [`data/raw/2026-05-16/`](data/raw/2026-05-16/).

| Route | Result | Read |
|-------|--------|------|
| llama.cpp b9172, Qwen3-Coder 30B UD-Q4_K_XL | 94.43-95.05 tg128 depending on batch flags | No new balanced-UD headline; b9049/b9010 remain faster at about 96-97 t/s. |
| llama.cpp b9172, Qwen3.6 UD-Q4_K_M | 61.52 tg128 | No new headline; current b9049/b9010 rows remain stronger. |
| llama.cpp b9172, Qwen3.6 Q4_0 | 79.14 tg128 | No new headline; current b9049 Q4_0 row remains 81.30 t/s. |
| llama.cpp b9172, Qwen3-Next 80B UD-Q4_K_XL | **59.06 tg128**, 751.70 pp512 | New best 80B Qwen-family row; replaces the old 54.92 t/s b8933 headline for this model. |
| llama.cpp b9172, gpt-oss-120b MXFP4 | 54.69 tg128, 718.61 pp512 | No new headline; b9049 remains slightly better at 55.57 t/s. |
| Ollama 0.24.0 isolated binary, Qwen3.6 API | 49.05 t/s warm generation average | No speedup versus the same-prompt Ollama 0.23.1 control at 49.09 t/s. |
| llama.cpp b9179, Qwen3-Coder 30B Q4_K_S/Q4_0/IQ4_NL/Q4_K_M sweep | Initial best row: Q4_K_S at **97.22 tg128**, 1387.22 pp512 | Useful negative result: current master plus smaller Qwen3-Coder quants did not produce a stable 100 t/s path. Raw data: [`qwen3-coder-break100-master`](data/raw/2026-05-16/qwen3-coder-break100-master/). |
| llama.cpp b9179, Qwen3-Coder 30B Q4_K_S strict-clean confirmation | **98.51 tg128 r50**, 1396.11 pp512 | New speed-first peak after fixing the `tuned`/`power-profiles-daemon` conflict and pausing nonessential GUI/video/media noise. Raw data: [`break-97-24-strict-noise-settings`](data/raw/2026-05-16/break-97-24-strict-noise-settings/). |
| llama.cpp b9467, Qwen3-Coder-Next 80B-A3B IQ4_XS | 61.91 tg128, 738.98 pp512 | Modern Qwen coding-model row repeated after Reddit feedback. It is useful current-model evidence but not a replacement for the Qwen3-Coder 30B speed-first headline. Raw data: [`modern-model-clean-followup`](data/raw/2026-06-02/modern-model-clean-followup/). |
| llama.cpp b9187, Qwen3.6 35B MTP IQ4_XS-Q8nextn server route | **90.80 t/s average** over six prompts with `draft-n=2`; best prompt **110.61 t/s** with `draft-n=3`, `-t 16`, `--poll 10` | Previous MTP route and former single-prompt peak, but not a replacement for the direct non-speculative headline or a broad 100 t/s average. Raw data: [`mtp-iq4xs-q8nextn`](data/raw/2026-05-17/mtp-iq4xs-q8nextn/), summary: [`MTP_SPECULATIVE_DECODING.md`](MTP_SPECULATIVE_DECODING.md). |
| llama.cpp b9235, Qwen3.6 35B MTP IQ4_XS-Q8nextn server route | **92.30 t/s average** over six prompts with `draft-n=3`; best prompt **109.21 t/s** | Former local MTP best, later superseded by b9334 at 98.57 t/s and b9360 at about 101.1 t/s. Raw data: [`mtp-35b-iq4xs-llamacpp-9235`](data/raw/2026-05-19/mtp-35b-iq4xs-llamacpp-9235/). |
| Community GMKtec EVO-X2, llama.cpp b9235, Qwen3-Coder 30B UD-Q4_K_XL | 92.11 tg128 generation-only; 1157.29 pp512 / 91.40 tg128 in the full follow-up | Useful portability evidence for the GMKtec/latest-stack path. Not an apples-to-apples replacement for the Beelink headline because the full follow-up used `-b 512 -ub 512`, `flash_attn=0`, and `use_mmap=1`. Raw data: [`community-gmktec-qwen-coder-issue17`](data/raw/2026-05-19/community-gmktec-qwen-coder-issue17/). |
| Community GMKtec EVO-X2, llama.cpp b9235, Qwen3.6 35B MTP IQ4_XS-Q8nextn | **93.29 t/s average** over six prompts with `draft-n=2`; `draft-n=3` reached 93.01 t/s average and 175.97 t/s best prompt | First independent exact-model MTP reproduction. It slightly exceeds the local Beelink b9235 average, but still does not create a broad 100 t/s average claim. Raw data: [`community-gmktec-mtp-issue18`](data/raw/2026-05-19/community-gmktec-mtp-issue18/). |
| Community GMKtec EVO-X2, llama.cpp b9235, Gemma 4 26B-A4B IT UD-Q4_K_M | **1209.08 pp512 / 53.02 tg128** direct `llama-bench` | Second-OEM stock Gemma control. Decode is in the same practical band as the first-party b9851/b9859 55.45/54.18 t/s rows, but different build, Mesa, mmap, host state, and model bytes/hash make it portability evidence rather than a hardware comparison. Raw data: [`community-gmktec-gemma4-issue4`](data/raw/2026-08-18/community-gmktec-gemma4-issue4/). |
| llama.cpp b9235, official Qwen3.6 27B MTP Q8_0 | 7.74 t/s baseline; **14.59 t/s** best MTP average | Useful negative result: MTP nearly doubled the official 27B Q8_0 route, but this dense/heavy path is much slower than the 35B-A3B MoE routes and is not a speed candidate. Raw data: [`qwen36-27b-mtp-q8-llamacpp-9235`](data/raw/2026-05-19/qwen36-27b-mtp-q8-llamacpp-9235/). |

Takeaway: upgrading blindly is not always faster. b9172 is worthwhile for Qwen3-Next 80B on this machine. Current master b9179 plus the Qwen3-Coder Q4_K_S speed-first quant can beat the old 97.24 t/s peak under a strict benchmark host state, but still did not produce a reliable Qwen3-Coder direct non-speculative 100 t/s result. The GMKtec Qwen3-Coder follow-up reinforces that command flags such as batch size, flash attention, and mmap must be preserved when comparing rows. MTP on b9187/b9235/b9334/b9360 can exceed 100 t/s on favorable server prompts, and b9360 plus `-ub 1024` now gives a repeat-confirmed local six-prompt average around 101.1 t/s. Keep direct `llama-bench`, server batching, and speculative decoding claims separate.

## MTP Speculative Decoding

Measured with `llama-server` Vulkan/RADV, six `/completion` prompts, `n_predict=192`, `temperature=0`, `top_k=1`, and prompt cache disabled per request. Structured data: [`data/mtp_speculative.csv`](data/mtp_speculative.csv). Raw data: [`data/raw/2026-05-16/mtp-server-qwen36-35b/`](data/raw/2026-05-16/mtp-server-qwen36-35b/), [`data/raw/2026-05-17/mtp-iq4xs-q8nextn/`](data/raw/2026-05-17/mtp-iq4xs-q8nextn/), [`data/raw/2026-05-19/`](data/raw/2026-05-19/), [`data/raw/2026-05-26/latest-llamacpp-b9334/`](data/raw/2026-05-26/latest-llamacpp-b9334/), [`data/raw/2026-05-27/latest-llamacpp-b9360/`](data/raw/2026-05-27/latest-llamacpp-b9360/), [`data/raw/2026-06-01/qwen36-27b-mtp-latest-de6f727/`](data/raw/2026-06-01/qwen36-27b-mtp-latest-de6f727/), [`data/raw/2026-06-11/gemma4-26b-qat-mtp-sixprompt-ac4cddeb/`](data/raw/2026-06-11/gemma4-26b-qat-mtp-sixprompt-ac4cddeb/), [`data/raw/2026-06-12/gemma4-26b-qat-mtp-cold-repeat-ac4cddeb/`](data/raw/2026-06-12/gemma4-26b-qat-mtp-cold-repeat-ac4cddeb/), and [`data/raw/2026-06-12/gemma4-26b-qat-mtp-t3-only-repeat-ac4cddeb/`](data/raw/2026-06-12/gemma4-26b-qat-mtp-t3-only-repeat-ac4cddeb/).

| Route | Mean t/s | Min-Max | Read |
|-------|---------:|--------:|------|
| Official Qwen3.6 35B MTP Q8_0, no MTP | 56.20 | 53.35-69.44 | Heavy baseline. |
| Official Qwen3.6 35B MTP Q8_0, `draft-n=2` | 67.04 | 60.81-75.55 | Best 35B Q8 average; about +19%. |
| Local Qwen3.6 MTP Q4_K_M requant, no MTP | 74.13 | 72.55-74.56 | Faster baseline from reduced model weight. |
| Local Qwen3.6 MTP Q4_K_M requant, `draft-n=2` | 87.53 | 82.18-95.68 | Best Q4_K_M average; about +18% over the Q4_K_M no-MTP server baseline. |
| Local Qwen3.6 MTP Q4_K_M requant, `draft-n=3`, `-t 16`, `--poll 10` | 83.13-84.19 repeats | best prompt 99.86-100.74 | Repeatable single-prompt 100 t/s result, but lower broad average. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, no MTP | 72.44 | 72.12-72.62 | Published small MTP quant baseline. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, `draft-n=2`, `-t 16`, `--poll 50` | 90.80 | 83.23-100.37 | Previous best broad MTP average before the b9235 rerun. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, `draft-n=3`, `-t 16`, `--poll 10` | 90.27 | 73.81-110.61 | Former single-prompt peak, but not a broad 100 t/s average. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9235, no MTP | 74.54 | 74.36-74.86 | Latest-stack baseline rerun. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9235, `draft-n=2`, `-t 16`, `--poll 50` | 91.88 | 80.40-100.67 | Latest-stack MTP rerun, stronger than the b9187 draft-n=2 average. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9235, `draft-n=3`, `-t 16`, `--poll 10` | 92.30 | 76.57-109.21 | Former best local Beelink broad MTP average. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9334, no MTP | 74.39 | 70.77-75.14 | Latest no-speculative baseline. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9334, `draft-n=2`, `-t 16`, `--poll 50` | 96.14 | 86.58-107.24 | Latest-stack MTP improvement. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9334, `draft-n=3`, `-t 16`, `--poll 100` | **98.57** | 81.94-116.22 | Former best local Beelink broad MTP average before the b9360 `-ub 1024` rerun. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9334, `draft-n=3`, `-t 16`, `--poll 10` | 98.52 | 82.24-116.75 | Best b9334 single-prompt peak. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9360, no MTP | 74.88 | 74.82-74.97 | Latest no-speculative baseline. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9360, `draft-n=2`, `-t 16`, `--poll 100`, `-ub 512` | 99.56 | 86.91-108.28 | Very close, but still below broad 100 t/s. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9360, `draft-n=2`, `-t 16`, `--poll 100`, `-ub 1024` | **101.15** | 88.36-109.87 | First repeated local broad 100+ t/s MTP route; t16 repeats were 101.15 / 101.10 / 101.06. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9360, `draft-n=2`, `-t 12`, `--poll 100`, `-ub 1024` | **101.16** | 88.29-109.71 | Highest single six-prompt average in this b9360 sweep, essentially tied with t16. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9360, `draft-n=3`, `-t 16`, `--poll 100`, `-ub 1024` | 99.83 | 83.28-117.53 | Higher prompt peak, lower broad average than draft-n=2. |
| Gemma 4 26B-A4B QAT, ac4cddeb0, no MTP | 73.96 | 73.63-74.13 | No-speculative server baseline for the matched-head route; separate from direct `llama-bench`. |
| Gemma 4 26B-A4B QAT + matched MTP head, ac4cddeb0, `draft-n=2` | **106.88** | 92.91-119.08 | First local six-prompt Gemma MTP pass; about +44% versus no-spec baseline. |
| Gemma 4 26B-A4B QAT + matched MTP head, ac4cddeb0, `draft-n=3` repeat | **110.00** | 93.57-127.33 | Best repeat-confirmed Gemma MTP average; server/speculative route, not direct `llama-bench`. |
| Gemma 4 26B-A4B QAT + matched MTP head, ac4cddeb0, cold repeat | **102.69** | 86.76-118.77 | Cold repeat after stopping nonessential local workload while leaving T3 and Hermes untouched. |
| Gemma 4 26B-A4B QAT + matched MTP head, ac4cddeb0, T3-only repeat | **107.42** | 91.30-124.71 | Repeat after stopping Hermes/Ollama/RustDesk/docflock/VM/browser-class noise while leaving T3 running. |
| Community GMKtec Qwen3.6 MTP IQ4_XS-Q8nextn, b9235, `draft-n=2`, `-t 16`, `--poll 50` | **93.29** | 71.79-161.54 | First independent exact-model reproduction; best community broad average so far. |
| Community GMKtec Qwen3.6 MTP IQ4_XS-Q8nextn, b9235, `draft-n=3`, `-t 16`, `--poll 50` | 93.01 | 68.28-175.97 | Higher prompt peak, slightly lower broad average than `draft-n=2`. |
| Official Qwen3.6 27B MTP Q8_0, b9235, no MTP | 7.74 | 7.74-7.75 | Heavy dense route; not a speed candidate. |
| Official Qwen3.6 27B MTP Q8_0, b9235, best MTP | 14.59 | 12.70-16.56 | MTP helps, but this route remains far slower than the 35B-A3B MoE path. |
| Official Qwen3.6 27B MTP Q8_0, `de6f727aa`, no MTP | 7.61 | 7.59-7.62 | Latest-stack sanity rerun; still a heavy dense route. |
| Official Qwen3.6 27B MTP Q8_0, `de6f727aa`, `draft-n=3` | 14.69 | 12.87-16.53 | Confirms the negative/control conclusion: MTP helps, but this route is not competitive with 35B-A3B MoE speed. |

Takeaway: MTP is useful for server/speculative experiments and likely worth tracking as `llama.cpp` support matures. The local b9360 Qwen3.6 rerun raised the practical MTP range to about 101.1 t/s on the Beelink when `-ub 1024` is used. The Gemma 4 26B-A4B QAT matched-head route adds a current Google-model server example at 102.69-110.00 t/s depending on host workload. Do not write these as direct `llama-bench` results or as universal "all local LLMs run at 100+ t/s" claims. The GMKtec reproduction makes the earlier 92-93 t/s route more credible, and the official 27B Q8_0/NVFP4 MTP routes are useful negative speed results here.

## Qwen3.6 Quant Sweep

Measured 2026-05-07 with llama.cpp b9049 Vulkan/RADV on the Beelink GTR9 Pro. Raw data: [`data/raw/2026-05-07/max-performance-campaign/benchmarks/qwen36-top-confirm-r20/`](data/raw/2026-05-07/max-performance-campaign/benchmarks/qwen36-top-confirm-r20/).

| Quant | pp512 | tg128 | Use |
|-------|------:|------:|-----|
| Q4_0 | 1243.51 | **81.30** | Fastest measured Qwen3.6 row; speed-first, lower-quality tradeoff. |
| Q4_0 with q8 KV | 1229.97 | 79.90 | Slightly slower decode; q8 KV may be useful for some context/memory tradeoffs. |
| IQ4_NL | 1199.41 | 77.29 | Fast candidate; quality sanity needed before recommending broadly. |
| Q4_K_M | 1105.78 | 76.94 | Balanced Strix quant candidate; likely more practical than Q4_0 if quality matters. |
| UD-Q4_K_M | 1059.45 | 62.56 | Older default headline row from the clean latest-stack rerun. |

Takeaway: Qwen3.6 can be pushed well past the old 63 t/s row, but the guide should not hide the quant tradeoff. For beginners, keep "use Qwen3.6 Q4_K_M/UD-Q4_K_M as the all-rounder" and add "use Q4_0 when you want maximum speed and have accepted the quality tradeoff."

## gpt-oss-120b Local Check

Measured 2026-05-07 with llama.cpp b9049 Vulkan/RADV and the `ggml-org/gpt-oss-120b-GGUF` MXFP4 split GGUF. This is a performance/loadability check, not a quality evaluation.

Raw data:

- first load/speed check: [`data/raw/2026-05-07/gpt-oss-120b-local-attempt/`](data/raw/2026-05-07/gpt-oss-120b-local-attempt/)
- clean paused-system long-context rerun: [`data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/)

| Workload | Result | Raw CSV |
|----------|-------:|---------|
| pp512 | 726.99 t/s | [`long-context rerun`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-prefill-512-32768-r3.csv) |
| pp2048 | 728.60 t/s | [`long-context rerun`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-prefill-512-32768-r3.csv) |
| pp8192 | 678.59 t/s | [`long-context rerun`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-prefill-512-32768-r3.csv) |
| pp16384 | 605.21 t/s | [`long-context rerun`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-prefill-512-32768-r3.csv) |
| pp32768 | 478.25 t/s | [`long-context rerun`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-prefill-512-32768-r3.csv) |
| pp65536 | 293.73 t/s | [`pp65536 r1`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-pp65536-r1.csv) |
| tg128 | 55.57 t/s | [`tg128 r20`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-tg128-r20.csv) |

Takeaway: the 128GB Strix Halo setup can load and run a 117B-parameter open-weight MoE locally at about 55-56 t/s generation on the measured direct Vulkan path. The first tg32 attempt was correctly aborted by the benchmark guard when swap-free dropped under 2 GiB; after clearing swap with ample free RAM, tg32 and tg128 completed. The later paused-system rerun also proves prompt processing through 65K tokens, but the 65K row is one repeat.

## Ollama Vulkan

### Qwen3.6-35B-A3B, Ollama 0.23.1 and isolated 0.24.0, Vulkan RADV

| Prompt Tokens | Prompt Eval | Generation | Notes |
|---------------|-------------|------------|-------|
| 19 | 158 t/s | **50.5 t/s** | Controlled 2026-05-07 API warm average across 10 runs; matches 0.21.2 |
| 25 | 188 t/s | 49.1 t/s | 2026-05-16 same-prompt Ollama 0.23.1 control |
| 25 | 188 t/s | 49.1 t/s | 2026-05-16 isolated Ollama 0.24.0 check; no speedup |
| 20 | 163 t/s | 45.6 t/s | Older result, superseded by controlled API run |
| 22 | 174 t/s | 45.4 t/s | Older result, superseded by controlled API run |

### Historical March Ollama Results

These remain useful as historical data, but they are not the current headline numbers.

| Model | Prompt Tokens | pp (t/s) | tg (t/s) | Notes |
|-------|---------------|----------|----------|-------|
| Qwen3.5 35B-A3B, Ollama 0.20.4 | 14 | 121.3 | **48.0** | Mesa 26.0.2 era |
| Qwen3.5 35B-A3B, Ollama 0.20.4 | 23 | 182.3 | **47.5** | Mesa 26.0.2 era |
| Qwen3.5 35B-A3B, Ollama 0.20.4 | 122 | 456.7 | **47.4** | Mesa 26.0.2 era |
| Qwen3-Coder 30B-A3B Q8_0 | 12 | 118.3 | **51.4** | Ollama path |
| Qwen3-Coder-Next | 120 | 301.2 | **37.9** | Dense 51GB model |
| Qwen2.5-VL 7B | 23 | 81.7 | **21.4** | Vision-language model |

## 2026-07-13 b9979 AMD MoE Density-Gate Campaign

This is aggregate `llama-batched-bench` throughput, not direct single-stream `llama-bench` speed. Controlled repeats used pp512/tg128 per sequence, Q4_0 KV, a 65,536-token context, and a below-50 C start.

| Model | Route | np8 mean | np9 mean | np12 mean | np16 mean | Read |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Qwen3-Coder 30B-A3B | b9979 Vulkan stock | 228.18 | 147.19 | 177.02 | 212.66 | Fixed threshold creates a 35.5% 8-to-9 cliff. |
| Qwen3-Coder 30B-A3B | b9979 AMD/RADV density | 228.36 | 210.07 | 236.70 | 266.07 | Recovers 42.7% at np9 without changing np8 materially. |
| Qwen3-Coder 30B-A3B | density + dense16 | 228.11 | 234.12 | 246.13 | 227.20 | Best at np9-12, but worse than density alone at np16. |
| Qwen3-Coder 30B-A3B | Lemonade ROCm b1259 | 191.78 | 200.89 | 240.79 | 287.64 | Strongest tested 30B route at np16. |
| Qwen3-Next 80B-A3B | b9979 Vulkan stock | 144.88 | 100.15 | 113.26 | 126.61 | Repeats the cliff on 512 experts/top-10. |
| Qwen3-Next 80B-A3B | b9979 AMD/RADV density | 145.02 | 125.48 | 138.46 | 150.82 | Recovers 25.3% at np9; strongest tested 80B np16 route. |
| Qwen3-Next 80B-A3B | density + dense16 | 144.76 | 142.72 | 144.97 | 131.08 | Nearly removes the np9 cliff, but regresses versus density at np16. |
| Qwen3-Next 80B-A3B | Lemonade ROCm b1259 | 112.19 | 116.90 | 130.50 | 143.32 | Better than stock after np9, but behind tuned Vulkan in this model matrix. |

Source: [`data/moe_density_gate_summary.csv`](data/moe_density_gate_summary.csv), [`MOE_CONCURRENCY.md`](MOE_CONCURRENCY.md), and [`raw evidence`](data/raw/2026-07-13/llamacpp-b9979-amd-density-gate/).

## Multi-User llama-server

### Qwen3.6-35B-A3B UD-Q4_K_M, llama.cpp b9010, Vulkan RADV

This is a serving benchmark, not a single-user `llama-bench` headline. Each row is the average of 3 measured repetitions with streaming `/completion`, 128 generated tokens per request, prompt cache disabled, continuous batching enabled, and about 4096 context tokens per slot.

| `-np` | Concurrent Requests | Aggregate tg | Avg per Request | Mean TTFT | Mean ITL | Notes |
|-------|---------------------|--------------|-----------------|-----------|----------|-------|
| 1 | 1 | 59.21 t/s | 59.21 t/s | 0.117 s | 16.1 ms | Server/API path baseline |
| 2 | 2 | 92.21 t/s | 46.11 t/s | 0.198 s | 20.3 ms | Good scaling |
| 4 | 4 | 130.81 t/s | 32.71 t/s | 0.237 s | 29.0 ms | Strong batching gain |
| 8 | 8 | **161.98 t/s** | 20.25 t/s | 0.307 s | 47.4 ms | Practical sweet spot |
| 16 | 16 | 165.98 t/s | 10.38 t/s | 0.547 s | 92.9 ms | Throughput plateau |

Takeaway: continuous batching makes Strix Halo much more useful as a local API box than single-user numbers imply. `-np 8` gives about 2.7x the `-np 1` aggregate throughput while keeping TTFT near 0.3 seconds. `-np 16` is viable for many low-rate clients, but not faster overall.

### Qwen3-Coder 30B-A3B UD-Q4_K_XL, llama.cpp b9010, Vulkan RADV

| `-np` | Concurrent Requests | Aggregate tg | Avg per Request | Mean TTFT | Mean ITL | Notes |
|-------|---------------------|--------------|-----------------|-----------|----------|-------|
| 1 | 1 | 90.20 t/s | 90.20 t/s | 0.079 s | 10.6 ms | Server/API path baseline |
| 2 | 2 | 121.65 t/s | 60.83 t/s | 0.133 s | 15.5 ms | Good scaling |
| 4 | 4 | 157.41 t/s | 39.36 t/s | 0.207 s | 24.0 ms | Strong batching gain |
| 8 | 8 | **173.16 t/s** | 21.65 t/s | 0.382 s | 43.5 ms | Practical sweet spot |
| 16 | 16 | 129.56 t/s | 8.10 t/s | 0.571 s | 119.9 ms | Regression |

Takeaway: `-np 8` is the best measured setting for Qwen3-Coder serving. `-np 16` regresses, so avoid it for throughput-focused coding workloads.

## Long-Context Prompt Scaling

These rows measure prompt processing at the listed prompt lengths. They do not measure decode speed after a fully occupied KV cache.

| Model | Quant | 4K pp | 8K pp | 16K pp | 32K pp | 64K pp | tg128 row |
|-------|-------|-------|-------|--------|--------|--------|-----------|
| Qwen3.6 35B-A3B | UD-Q4_K_M | 1081.93 | 1089.48 | 1024.58 | 908.61 | 740.25 | 57.84 |
| Qwen3-Next 80B-A3B | UD-Q4_K_XL | 741.68 | 735.50 | 700.49 | 644.82 | 543.89 | 55.58 |

Takeaway: Qwen3.6 retains 68% of its 4K prompt-processing speed at 64K. Qwen3-Next 80B retains 73%, which is a strong result for a 46GB-on-disk 80B MoE model.

## Filled-KV Decode

These rows measure a full `llama-server` request: long prompt ingestion plus 128 generated tokens after the KV cache is filled. Prompt cache was disabled. Prompt content was synthetic and repetitive, so compare within this table rather than against arbitrary real-world documents.

| Model | Prompt | KV | Prompt Eval | Decode After Fill | Wall Time |
|-------|--------|----|-------------|-------------------|-----------|
| Qwen3.6 35B-A3B | 32K | f16 | 1216.64 t/s | 51.00 t/s | 29.50 s |
| Qwen3.6 35B-A3B | 32K | q8_0 | 1023.43 t/s | 54.59 t/s | 34.46 s |
| Qwen3.6 35B-A3B | 32K | q4_0 | 1048.70 t/s | 56.03 t/s | 33.58 s |
| Qwen3.6 35B-A3B | 64K | f16 | 931.89 t/s | 41.44 t/s | 73.52 s |
| Qwen3.6 35B-A3B | 64K | q8_0 | 731.22 t/s | 49.13 t/s | 92.33 s |
| Qwen3.6 35B-A3B | 64K | q4_0 | 750.04 t/s | 51.33 t/s | 89.97 s |
| Qwen3.6 35B-A3B | 128K | f16 | 616.77 t/s | 32.23 t/s | 216.69 s |
| Qwen3-Next 80B-A3B | 32K | f16 | 972.57 t/s | 46.17 t/s | 36.51 s |
| Qwen3-Next 80B-A3B | 64K | f16 | 753.26 t/s | 38.18 t/s | 90.45 s |
| Qwen3-Next 80B-A3B | 128K | f16 | 497.79 t/s | 29.12 t/s | 268.54 s |

Takeaway: q4_0/q8_0 KV cache improves Qwen3.6 decode speed after a filled context, but slows prompt ingestion enough that full first-turn wall time is worse than f16. Use f16 for first-turn long prompts; use q4_0/q8_0 only when memory pressure or long continued generation matters more than ingest speed. The 128K f16 rows completed without truncation.

### Real-Corpus 64K Check

| Model | Prompt Type | Tokens | Prompt Eval | Decode After Fill | Wall Time |
|-------|-------------|--------|-------------|-------------------|-----------|
| Qwen3.6 35B-A3B | synthetic repeated token | 65,533 | 931.89 t/s | 41.44 t/s | 73.52 s |
| Qwen3.6 35B-A3B | real guide corpus | 65,120 | 706.21 t/s | 40.84 t/s | 95.41 s |
| Qwen3-Next 80B-A3B | synthetic repeated token | 65,532 | 753.26 t/s | 38.18 t/s | 90.45 s |
| Qwen3-Next 80B-A3B | real guide corpus | 63,507 | 504.53 t/s | 37.75 t/s | 129.40 s |

Takeaway: synthetic repeated-token prompts are optimistic for prompt-ingest speed. Real guide/documentation text slowed prompt eval by 24-33%, while decode-after-fill barely changed.

## Backend and Build Comparison

### Qwen3.5-35B-A3B Q4_K_M

| Backend / Build | pp512 | tg128 | Takeaway |
|-----------------|-------|-------|----------|
| Ollama Vulkan RADV, bundled older llama.cpp | ~457 | 47.4 | Easy, but slower |
| Vulkan RADV, b8298 | 868 | 52.06 | Baseline kyuz0-era direct path |
| Vulkan RADV, b8460 | **1080** | **64.85** | Best short-context result |
| ROCm HIP, b8301, HSA fix | 1059 | 47.87 | Old self-compiled ROCm build |
| ROCm HIP, b8460, HSA fix | 1047 | 54.67 | ROCm improved, still slower tg than RADV |

### AMDVLK Correction

AMDVLK is not recommended. It was installed during earlier testing and its ICD file silently overrode RADV for some direct `llama-bench` commands. That caused false "RADV regression" conclusions. Corrected current state:

- RADV is the default Vulkan path and wins the measured generation-heavy GGUF rows used for this guide's beginner recommendation.
- ROCm/HIP is not a Vulkan driver and can win prompt-processing-heavy rows, so compare pp and tg separately instead of reducing every backend to one winner.
- AMDVLK should be uninstalled, not just ignored.
- Verify RADV in output: `(RADV STRIX_HALO) (radv)` and `shared memory: 65536`.
- AMDVLK output shows `(AMD open-source driver)` and `shared memory: 32768`.

## ROCm Status

The historical b8460/kernel 6.19.4 route was not "all broken." It worked when
both environment variables were set before running ROCm/HIP binaries:

```bash
export HSA_OVERRIDE_GFX_VERSION=11.5.1
export HSA_ENABLE_SDMA=0
```

| Build | Kernel | pp128 | pp512 | tg128 | Notes |
|-------|--------|-------|-------|-------|-------|
| b8460 | 6.19.4 | **547** | **1047** | **54.67** | Current fair ROCm comparison |
| b8301 | 6.19.4 | 542 | 1059 | 47.87 | Old build, HSA fix |
| b8301 | 6.18.14 | 488 | 996 | 48.80 | Previous reference |

ROCm remains relevant for batch processing, hipBLASLt, vLLM experiments, and long-context/rocWMMA work. For current generation-heavy MoE chat/coding rows, Vulkan RADV is faster on the measured data; for prompt-processing-heavy work, HIP can win and should be tested separately.

Current ROCm builds that detect `gfx1151` natively should run without a
global HSA architecture override. A stale host
`HSA_OVERRIDE_GFX_VERSION=11.0.0` was independently reproduced as a
Distrobox migration failure with current ROCm 7.2.4; removing it restored
native detection and inference. This does not change the environment recorded
for the historical rows above.

### 2026-05-03 ROCm HIP Spot Check

| Model | Quant | ROCm pp512 | ROCm tg128 | Vulkan Reference |
|-------|-------|------------|------------|------------------|
| Qwen3.6 35B-A3B | UD-Q4_K_M | 1186.19 | 52.69 | Vulkan b9010: 1108.93 pp, 63.06 tg |
| Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 1285.32 | 73.69 | Vulkan b9010: 1346.27 pp, 97.24 tg |

The local HIP build is b8460 and requires `LD_LIBRARY_PATH=/usr/local/lib/ollama/rocm` plus the HSA override. It emitted a missing `TensileLibrary_lazy_gfx1151.dat` warning, so treat this as a ROCm HIP baseline, not a tuned rocBLASLt/rocWMMA result.

### 2026-05-07 HIP vs Vulkan Crossover Spot Check

The new local spot check separates prompt processing from token generation. It is not a perfect same-build fairness claim: Vulkan rows use b9010, while HIP rows use the available local b8460 HIP build. The result is still useful because it matches the direction of the independent same-build Strix Halo study in [`nabe2030/hip-vs-vulkan-evo-x2`](https://github.com/nabe2030/hip-vs-vulkan-evo-x2).

Structured data: [`data/backend_crossover.csv`](data/backend_crossover.csv). Full notes: [`BACKEND_CROSSOVER.md`](BACKEND_CROSSOVER.md).

| Model | Vulkan pp16384 | HIP pp16384 | Prompt-processing read | Vulkan tg128 | HIP tg128 | Generation read |
|-------|---------------:|------------:|------------------------|-------------:|----------:|-----------------|
| Qwen3.6 35B-A3B UD-Q4_K_M | 1038.14 | **1295.38** | HIP +24.8% | **62.24** | 52.72 | Vulkan +18.1% |
| Qwen3-Coder 30B-A3B UD-Q4_K_XL | 564.68 | **756.16** | HIP +33.9% | **93.67** | 72.19 | Vulkan +29.8% |

Takeaway: keep Vulkan/RADV as the default for generation-heavy chat/coding and low-concurrency API use, but keep ROCm/HIP available for prompt-heavy experiments such as RAG ingestion, long prompts, summarization, and future vLLM/AWQ/DFlash work.

### 2026-05-16 Qwen3-Next 80B HIP vs Vulkan Spot Check

This spot check used the current b9172 Vulkan/RADV build against the existing Lemonade `llamacpp-rocm` b1259/gfx1151 bundle. It is a small r3/r20 comparison, not a final same-build backend shootout, but it is useful because it repeats the same workload split: HIP can help prefill, while Vulkan remains better for decode/generation.

Structured data: [`data/backend_crossover.csv`](data/backend_crossover.csv).

| Model | Vulkan pp512 | HIP pp512 | Prompt-processing read | Vulkan tg128 | HIP tg128 | Generation read |
|-------|-------------:|----------:|------------------------|-------------:|----------:|-----------------|
| Qwen3-Next 80B-A3B UD-Q4_K_XL | 751.70 | **800.38** | HIP +6.5% | **59.06** | 49.57 | Vulkan +19.1% |

Takeaway: do not phrase the guide as "RADV wins everything." For beginners, the practical rule is still simple: use Vulkan/RADV for chat, coding, and generation-heavy GGUF inference. Advanced users doing RAG ingest, long-prompt summarization, or server/batch experiments should test HIP/ROCm too.

Gemma 4 26B-A4B is a negative result on the local HIP path: Vulkan loaded and ran, but HIP b8460 failed to load the local GGUF. No local Gemma 4 HIP speed claim is made.

## Current Takeaways

1. Direct llama.cpp with Vulkan RADV is the fastest measured short-context path for Qwen MoE models.
2. Updating llama.cpp from b8298 to b8460 produced the largest improvement: +24% pp and +25% tg on Qwen3.5-35B-A3B.
3. AMDVLK caused false regression reports through ICD hijacking; keep it removed.
4. The dated b8460/kernel 6.19.4 ROCm rows used HSA overrides. Current native-`gfx1151` builds should be tested without a global override; HIP remains relevant for prompt processing.
5. Before any new benchmark campaign, keep `tuned accelerator-performance` active and log raw commands/results into a single dataset.
