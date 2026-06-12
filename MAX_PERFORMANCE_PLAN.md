# Strix Halo Max Performance Plan

Status: active planning track, started 2026-05-07.

Goal: test the Beelink GTR9 Pro / Ryzen AI MAX+ 395 as far as is practical for local LLM inference, without turning the guide into unbounded hype. The public claim should be: we tested the important software, driver, quant, model, context, and serving routes, and here is the best setup by workload.

## Current Truth

The old broad claim "RADV wins on everything" should not be used.

Current measured recommendation:

- Beginner summary: use RADV for the normal Vulkan path, do not install AMDVLK, and only test ROCm/HIP when you specifically care about long prompts, RAG ingest, server batching, or vLLM.
- RADV wins the Vulkan-driver comparison. Use RADV, not AMDVLK.
- Vulkan/RADV remains the best measured local default for short-context generation, chat, coding, and direct `llama-server` work.
- ROCm/HIP can win prompt-processing-heavy work. The local crossover spot check showed HIP ahead at pp16384, while Vulkan stayed ahead at tg128.
- Lemonade ROCm is still relevant for aggregate server throughput at higher Qwen3.6 concurrency.
- MTP speculative decoding is now measured as a separate `llama-server` route. It can improve practical server generation and reached a repeat-confirmed 101.1 t/s six-prompt average on Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn with b9360. A newer Gemma 4 26B-A4B QAT matched-head route reached 102.7 t/s cold / 107.4 t/s T3-only / 110.0 t/s best-repeat on ac4cddeb0. These do not replace direct `llama-bench` headlines.
- Plain vLLM/AWQ serves locally but is not competitive for single-user generation without DFlash or another serving-specific win.
- Lucebox DFlash/PFlash is now the highest-upside experimental decode/prefill route, but local reproduction is blocked until an isolated ROCm/HIP dev toolchain with `hipcc` and rocWMMA is available.
- FastFlowLM/NPU is visible at the kernel level on this Beelink (`amdxdna` + `/dev/accel/accel0`), but XRT/FastFlowLM user-space is not installed yet.

Current fastest local headline:

- Current balanced direct path: Qwen3-Coder 30B-A3B UD-Q4_K_XL at 96.76 t/s on llama.cpp b9049, Vulkan/RADV.
- Historical balanced peak: Qwen3-Coder 30B-A3B UD-Q4_K_XL at 97.24 t/s on b9010.
- New speed-first peak: Qwen3-Coder 30B-A3B Q4_K_S at 98.51 t/s r50 on llama.cpp b9179, Vulkan/RADV, after fixing the `tuned` versus `power-profiles-daemon` conflict and pausing benchmark noise.
- Treat 98.51 t/s as the current measured speed-first Qwen3-Coder peak, not a 100 t/s result and not the default balanced-quality recommendation.
- Separate direct 100 t/s row: Qwen3-30B-A3B-Instruct-2507 IQ4_XS reached 100.04 t/s r50 on llama.cpp b9467, Vulkan/RADV. Treat it as a separate general-instruct Qwen route, not as a Qwen3-Coder replacement.
- Additional Qwen3-Coder break-100 route testing reached 99.11 t/s in an r5 scout and 98.96 t/s in an r20 confirmation, but still did not produce a stable Qwen3-Coder 100 t/s result.
- Current fastest measured Qwen3.6 path: Q4_0 at 81.30 t/s on llama.cpp b9049, Vulkan/RADV. Label this as speed-first, not the default all-round quality recommendation.
- Current measured MTP server routes: Qwen3.6 IQ4_XS-Q8nextn reached 101.16 t/s best local Beelink six-prompt average on b9360 with `draft-n=2`, `--poll 100`, and `-ub 1024`; Gemma 4 26B-A4B QAT with a matched MTP head reached 102.69 t/s cold repeat, 107.42 t/s T3-only repeat, and 110.00 t/s best repeat on ac4cddeb0. The best community broad Qwen3.6 MTP average is 93.29 t/s on GMKtec EVO-X2 with b9235.

## 2026-05-07 Campaign Results

Detailed results: [`MAX_PERFORMANCE_RESULTS_2026-05-07.md`](MAX_PERFORMANCE_RESULTS_2026-05-07.md). Structured summary: [`data/max_performance_campaign.csv`](data/max_performance_campaign.csv).

| Route | Status | Result |
|-------|--------|--------|
| Qwen3.6 quant sweep | done | Q4_0 reached 81.30 t/s; Q4_K_M reached 76.94 t/s; old UD row remains 62.56 t/s. |
| Same-source HIP vs Vulkan | done | HIP wins prompt processing at pp16384; Vulkan wins tg128. |
| Qwen3-Coder max-speed sweep | done | No stable Qwen3-Coder 100 t/s result; strict-clean speed-first ceiling is now 98.51 t/s; balanced UD remains 96-97 t/s. |
| Qwen3-30B-A3B-Instruct-2507 scout | done | IQ4_XS reached 100.04 t/s r50 direct `llama-bench` on b9467; separate general-instruct Qwen route, not a Qwen3-Coder replacement. |
| gpt-oss-120b long-context sweep | done | 55.57 t/s tg128 and prompt processing through 65K tokens. |
| Tuned rocWMMA path | attempted | lhl branch built, but failed to load current Qwen3.6 GGUFs. |
| vLLM AWQ/DFlash | partially blocked | Plain AWQ smoke works at about 25 t/s; exact DFlash route blocked by gated drafter access. |
| MTP speculative decoding | done | `llama-server` MTP works. The b9360 rerun reached a repeat-confirmed 101.1 t/s local six-prompt average with Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn; Gemma 4 26B-A4B QAT reached 102.7 t/s cold / 107.4 t/s T3-only / 110.0 t/s best-repeat with a matched MTP head; GMKtec community reproduction reached 93.29 t/s on b9235 for the Qwen3.6 route. |

## 2026-05-16 Follow-Up

Raw evidence:

- [`data/raw/2026-05-16/post-migration-smoke/`](data/raw/2026-05-16/post-migration-smoke/)
- [`data/raw/2026-05-16/beelink-power-telemetry/`](data/raw/2026-05-16/beelink-power-telemetry/)
- [`data/raw/2026-05-16/lucebox-dflash-preflight/`](data/raw/2026-05-16/lucebox-dflash-preflight/)
- [`data/raw/2026-05-16/npu-fastflowlm-preflight/`](data/raw/2026-05-16/npu-fastflowlm-preflight/)
- [`data/raw/2026-05-16/vllm-preflight-refresh/`](data/raw/2026-05-16/vllm-preflight-refresh/)
- [`data/raw/2026-05-16/qwen3-coder-break100-master/`](data/raw/2026-05-16/qwen3-coder-break100-master/)
- [`data/raw/2026-05-16/break-100-routes/`](data/raw/2026-05-16/break-100-routes/)
- [`data/raw/2026-05-16/break-100-routes-strict2/`](data/raw/2026-05-16/break-100-routes-strict2/)
- [`data/raw/2026-05-16/break-100-amdvlk-isolated/`](data/raw/2026-05-16/break-100-amdvlk-isolated/)
- [`data/raw/2026-05-16/break-100-pr22970-vulkan/`](data/raw/2026-05-16/break-100-pr22970-vulkan/)
- [`data/raw/2026-05-16/break-100-master-0253-vulkan/`](data/raw/2026-05-16/break-100-master-0253-vulkan/)
- [`data/raw/2026-05-16/mtp-server-qwen36-35b/`](data/raw/2026-05-16/mtp-server-qwen36-35b/)
- [`data/raw/2026-05-17/mtp-iq4xs-q8nextn/`](data/raw/2026-05-17/mtp-iq4xs-q8nextn/)
- [`data/raw/2026-05-17/qwen3-coder-q4ks-server-ngram/`](data/raw/2026-05-17/qwen3-coder-q4ks-server-ngram/)

Findings:

- Storage migration did not break benchmark paths. Qwen3 0.6B and Qwen3.6 loaded from `/home/hoge-heer/models` and ran through Vulkan/RADV.
- Beelink amdgpu `PPT` telemetry is now captured for idle, Qwen3-Coder, and Qwen3.6. It is useful same-machine context, not wall power.
- Lucebox DFlash/PFlash cloned cleanly, but CMake HIP configuration failed because the host has no ROCm root / `hipcc` developer stack. Do not install that host-wide; use an isolated ROCm dev container/toolbox.
- NPU hardware is visible through `amdxdna` and `/dev/accel/accel0`, but XRT/FastFlowLM user-space is missing. The next NPU step is an isolated XRT/FastFlowLM install lane plus reboot/memlock validation.
- vLLM container versions and gfx1151 visibility were refreshed. Existing AWQ smoke remains about 25 t/s at `np=1`, which is useful serving evidence but not a default-speed win.
- Qwen3-Coder current-master break-100 sweep tested UD-Q4_K_XL plus Q4_0, Q4_K_S, IQ4_NL, and Q4_K_M. Q4_K_S was fastest in the first pass at 97.22 t/s r20; r5-only 97.7 t/s flag wins did not hold under r20 confirmation. No stable 100 t/s path found.
- A stricter follow-up found the missing host-state factor: `power-profiles-daemon` can stop/conflict with `tuned`. With `tuned accelerator-performance` active, `power-profiles-daemon` inactive, CPU/EPP on performance, GPU high, and RustDesk/Firefox/Zoom/ffmpeg paused, Qwen3-Coder Q4_K_S on b9179 confirmed 98.51 t/s r50. Raw data: [`data/raw/2026-05-16/break-97-24-strict-noise-settings/`](data/raw/2026-05-16/break-97-24-strict-noise-settings/).
- Follow-up break-100 routes tested threads, poll settings, batch/ubatch, CPU masks, no-host, mmap, direct I/O, KV q8/q4, Flash Attention off, no-op/no-KV variants, root RustDesk/qemu pausing, and temporary T3 renice while keeping T3 running. Best r5 scout was 99.11 t/s; best r20 confirmation was 98.96 t/s with 1382.12 pp512. No stable 100 t/s path found.
- Additional high-upside break-100 checks did not change the direct `llama-bench` conclusion. AMDVLK via kyuz0's isolated toolbox measured 93.28 t/s r5, llama.cpp PR #22970 measured 98.74 t/s r20, and latest upstream master b9187 measured 98.64 t/s r20.
- MTP was then tested as the separate route it actually is: `llama-server` speculative decoding. Official Qwen3.6 35B MTP Q8_0 improved from 56.20 to 67.04 t/s average with `draft-n=2`. A local Q4_K_M requant improved from 74.13 to 87.53 t/s average with `draft-n=2`. The published IQ4_XS-Q8nextn route later reached a repeat-confirmed 101.1 t/s local six-prompt average on b9360 with `draft-n=2`, `--poll 100`, and `-ub 1024`. Gemma 4 26B-A4B QAT with a matched MTP head later reached 102.69 t/s cold repeat, 107.42 t/s T3-only repeat, and 110.00 t/s best repeat on ac4cddeb0. These are server/speculative routes and remain separate from direct non-speculative `llama-bench` headlines. Official Qwen3.6 27B MTP Q8_0 and Qwen3.6 27B NVFP4 were also checked as negative speed routes. Raw data: [`data/raw/2026-05-16/mtp-server-qwen36-35b/`](data/raw/2026-05-16/mtp-server-qwen36-35b/), [`data/raw/2026-05-17/mtp-iq4xs-q8nextn/`](data/raw/2026-05-17/mtp-iq4xs-q8nextn/), [`data/raw/2026-05-19/mtp-35b-iq4xs-llamacpp-9235/`](data/raw/2026-05-19/mtp-35b-iq4xs-llamacpp-9235/), [`data/raw/2026-05-27/latest-llamacpp-b9360/`](data/raw/2026-05-27/latest-llamacpp-b9360/), [`data/raw/2026-06-01/qwen36-27b-mtp-latest-de6f727/`](data/raw/2026-06-01/qwen36-27b-mtp-latest-de6f727/), [`data/raw/2026-06-11/gemma4-26b-qat-mtp-sixprompt-ac4cddeb/`](data/raw/2026-06-11/gemma4-26b-qat-mtp-sixprompt-ac4cddeb/), [`data/raw/2026-06-12/gemma4-26b-qat-mtp-cold-repeat-ac4cddeb/`](data/raw/2026-06-12/gemma4-26b-qat-mtp-cold-repeat-ac4cddeb/), and [`data/raw/2026-06-12/gemma4-26b-qat-mtp-t3-only-repeat-ac4cddeb/`](data/raw/2026-06-12/gemma4-26b-qat-mtp-t3-only-repeat-ac4cddeb/), summary: [`MTP_SPECULATIVE_DECODING.md`](MTP_SPECULATIVE_DECODING.md).
- Qwen3-Coder Q4_K_S was also checked as a practical `llama-server` route with ngram speculative decoding. Baseline server average was 93.72 t/s; the best ngram route was `ngram-map-k4v` at 95.21 t/s average and 104.72 t/s best prompt. This did not create a broad 100 t/s coding-server claim. Raw data: [`data/raw/2026-05-17/qwen3-coder-q4ks-server-ngram/`](data/raw/2026-05-17/qwen3-coder-q4ks-server-ngram/).

## Route Details And Remaining Work

The highest-value routes below now include their 2026-05-07 campaign status. Keep the old pass conditions because they define what a future rerun must still capture.

### P0: Qwen3.6 Quant Sweep - Done

Why: this is the most likely route to a better immediately useful number for normal Strix Halo users. External Strix-optimized GGUFs report Qwen3.6 35B-A3B decode in the 70-76 t/s range for some quant variants, while this guide currently reports 62.56 t/s for the local UD-Q4 path.

Candidates:

- Plain Q4_K_M.
- Q4_0.
- IQ4_NL.
- Q5_K_M.
- Q6_K.
- Dynamic mixed quant from `0xSero/Qwen3.6-35B-A3B-GGUF-Strix`.

Pass condition:

- Same host, same current llama.cpp Vulkan/RADV build, same `-fa`, `-b`, `-ub`, `-ctk`, `-ctv`, `-ngl`, prompt size, and repeat count.
- Record model file, source repo, file size, hash, pp512, pp4096, tg128, and at least one real chat/API run.
- If a faster quant is lower quality, label it as "fastest measured quant", not "best model".

### P0: Same-Source HIP vs Vulkan - Done

Why: our first local crossover result was directionally useful but not a perfect same-build comparison. The 2026-05-07 campaign built Vulkan and HIP from the same b9049 source checkout. The HIP binary reports an unknown build id because the container did not trust the git directory, so call it same-source rather than perfect same-build.

Test matrix:

- Models: Qwen3.6 35B-A3B, Qwen3-Coder 30B-A3B, gpt-oss-120b if stable.
- Backends: Vulkan/RADV and HIP/ROCm from the same llama.cpp commit.
- Rows: pp512, pp2048, pp8192, pp16384, tg128, filled-context decode where practical.

Expected outcome:

- Vulkan remains the short-generation recommendation.
- HIP may win long-prompt prefill.
- The guide becomes stronger because it explains the split instead of pretending there is one universal winner.

### P1: Qwen3-Coder Max-Speed Sweep - Done

Why: this directly targets the 96-98.5 t/s Qwen3-Coder headline. The next useful question is whether the Beelink can cross 100 t/s on a still-useful coding model.

2026-05-17 update: current llama.cpp master b9179 and Unsloth Qwen3-Coder Q4_0/Q4_K_S/IQ4_NL/Q4_K_M quants were tested. Q4_K_S reached 97.22 t/s r20 in the first sweep. After fixing the `tuned`/`power-profiles-daemon` host-state conflict and pausing benchmark noise, Q4_K_S confirmed 98.51 t/s r50. A later Qwen3-Coder break-100 pass reached 99.11 t/s in r5 and 98.96 t/s in r20. AMDVLK isolated, PR #22970, and latest master b9187 also failed to produce a stable direct Qwen3-Coder 100 t/s path. A later 2026-06-02 scout did cross 100 t/s direct with Qwen3-30B-A3B-Instruct-2507 IQ4_XS, but that is a separate general-instruct model/quant route. Qwen3-Coder `llama-server` plus ngram speculation reached 95.21 t/s average, also below broad 100. MTP did produce a 110.61 t/s best-prompt `llama-server` result, but that is a separate speculative server claim, not this direct Qwen3-Coder `llama-bench` target.

Levers:

- llama.cpp b9049 or newer Vulkan/RADV.
- Batch and ubatch sweep: `-b/-ub 512`, `1024`, `2048`, maybe `4096` if memory and stability allow.
- KV cache variants: f16, q8_0, q4_0 where quality is acceptable.
- Quant variants if available: Q4_K_M, Q4_K_S, IQ4, Q5, UD-Q4_K_XL.
- `llama-bench` and `llama-server` API route, because user-visible speed can differ.

Pass condition:

- Any "over 100 t/s" claim needs raw logs, repeat count, exact model hash, and a note if the quant is lower quality than the current headline quant.

### P1: gpt-oss-120b Long-Context Sweep - Partly Done

Why: 120B on 128GB unified memory is the kind of result people share. The current guide proves it loads and generates around 55.57 t/s and can process prompts through 65K tokens, but filled-context decode and real-document wall time still need a cleaner API-style run.

Test rows:

- pp512, pp2048, pp8192, pp16384.
- tg128 at empty context.
- filled-context decode at 8K, 16K, 32K, and 64K if stable.
- Optional ROCm/HIP comparison only after the same-build gate is clean.

Pass condition:

- Label this as performance/loadability evidence, not model-quality evidence.

### P1: Tuned ROCm / rocWMMA Path

Why: this is the most credible route for HIP to become materially better on long-context or prefill-heavy rows. Current local HIP evidence is not tuned rocWMMA evidence.

Candidate route:

- Dedicated container/toolbox only.
- lhl `rocm-wmma-tune` branch or documented fix scripts.
- Build with `GGML_HIP=ON`, `AMDGPU_TARGETS=gfx1151`, `GGML_HIP_ROCWMMA_FATTN=ON`, and `GGML_HIP_MMQ_MFMA=ON`.

Pass condition:

- Build log, ROCm version, llama.cpp commit, flags, env vars, and raw output must be stored before publishing any result.
- If upstream rocWMMA regresses, publish it as a negative result.

### P2: vLLM AWQ/DFlash Reproduction

Why: this may not beat llama.cpp raw tg128, but it can be more useful for agent/server workloads: OpenAI-compatible endpoints, tool calls, vision, longer context, batching, and speculative serving.

Candidate source:

- `hec-ovi/vllm-awq4-qwen`, which reports Qwen 3.6 AWQ-INT4 plus DFlash on Strix Halo with ROCm/TheRock.

Pass condition:

- Container only, no host Python pollution.
- Capture startup time, warmup behavior, TTFT, p50/p95 latency, throughput, memory, endpoint compatibility, tool-call behavior, and failure modes.
- Compare against `llama-server` only when model, quant, prompt, context, concurrency, and output length are close enough.

Current local state:

- Plain Qwen3.6 AWQ4 vLLM smoke exists and measured about 25 t/s at `np=1`.
- The `vllm-gfx1151` container still starts and sees gfx1151.
- This route needs DFlash/speculative serving or a clear API-serving win before it belongs in the beginner recommendation.

### P2: Lucebox DFlash/PFlash Reproduction

Why: Lucebox is the clearest new route that might materially improve a real long-prompt + generation workload on Strix Halo. It targets Qwen3.5/Qwen3.6 27B DFlash/PFlash, not the same 30B/35B Vulkan headline workload.

Current local state:

- Repo clone and submodules succeeded at `6fe0d9a0a9b79855cc56967a60f6d35a5532cdd7`.
- HIP CMake preflight failed: no host ROCm root / `hipcc`.
- Required route: isolated ROCm/HIP dev container or toolbox, then target/draft model download inside that lane.

Pass condition:

- Build with `DFLASH27B_GPU_BACKEND=hip`, `DFLASH27B_HIP_ARCHITECTURES=gfx1151`, and documented rocWMMA settings.
- Compare Lucebox against llama.cpp HIP and Vulkan on the same target model and prompt shape.
- Publish as experimental until it has reproducible raw logs and an explanation for which workload it improves.

### P2: Speculative Decoding Check

Why: speculative decoding can improve generation in llama.cpp, but MoE models can also regress if draft verification activates too many experts. This is worth testing, but it is not safe to assume it helps.

Test rows:

- Baseline no speculation.
- llama.cpp n-gram cache.
- Small draft model where a compatible Qwen draft exists.
- Qwen3.6 and Qwen3-Coder separately.

Pass condition:

- Report accepted tokens, wall-clock t/s, model quality caveat, and whether the method helps real prompts, not only tiny synthetic prompts.

### P3: ROCm/TheRock Nightly vs Official ROCm

Why: many Strix Halo vLLM and HIP experiments use TheRock/nightly stacks before official gfx1151 support catches up.

Rule:

- Test in a container only.
- Do not replace the known-good host stack just to chase a nightly.

Pass condition:

- A nightly must beat the current result or unlock a new capability to be worth recommending.

### P3: Sustained Thermals and Power

Why: this does not raise peak t/s, but it proves whether the Beelink can hold performance during long local-AI sessions.

Test rows:

- 30-minute `llama-server` load.
- 30-minute long-context run.
- Optional wall-power/tokens-per-watt if telemetry is validated.

Pass condition:

- Record GPU clock, temperature, power source, fan mode, and whether speed drops over time.

## Lower-Value Or Risky Paths

- AMDVLK retesting is low value unless a specific new claim appears. AMDVLK is discontinued and has already caused ICD hijacking.
- BIOS UMA above 512MB is not expected to improve Vulkan inference. Test only if a specific ROCm/vLLM path requires it, and isolate the result.
- NPU LLM testing is not a max-performance path for the current 30B/35B/80B/120B GPU rows, but it is now a practical "should I use the NPU?" guide question because `amdxdna` and `/dev/accel/accel0` are visible locally.
- Full OS upgrade is not a first move for Vulkan performance. Ubuntu 24.04 with current kernel/Mesa already reaches the current measured peak.
- Windows testing is useful for completeness, but not likely to beat the current Linux/RADV headline.

## Recommended Campaign Order

1. Run the Qwen3.6 quant sweep.
2. Run same-build HIP vs Vulkan on current llama.cpp.
3. Run the Qwen3-Coder max-speed sweep.
4. Extend gpt-oss-120b into long-context rows.
5. Add sustained thermals and wall-power validation.
6. Attempt Lucebox DFlash/PFlash in an isolated ROCm dev lane.
7. Attempt FastFlowLM NPU in a separate XRT/FastFlowLM lane.
8. Attempt vLLM AWQ/DFlash only when DFlash or another server-specific win is available.

This order prioritizes likely useful wins first, then deeper experimental work.

## Claim Rules

- Public README language should put the action first and the caveat second. Example: "Use RADV for Vulkan. Advanced: HIP may win long-prompt prefill."
- "Best setup" must always mean "best setup for this workload".
- Every headline needs a date, backend, model, quant, command or script, CSV row, and raw log path.
- Faster lower-quality quants are allowed, but must be labeled as speed-first.
- External claims can guide tests, but they do not become local guide claims until reproduced on the Beelink.
- Negative results should stay in the guide when they prevent other users from wasting time.

## External Leads To Watch

- [`nabe2030/hip-vs-vulkan-evo-x2`](https://github.com/nabe2030/hip-vs-vulkan-evo-x2): independent HIP vs Vulkan Strix Halo comparison.
- [`lhl/strix-halo-testing`](https://github.com/lhl/strix-halo-testing): tuned ROCm/rocWMMA and long-context Strix Halo evidence.
- [`hec-ovi/vllm-awq4-qwen`](https://github.com/hec-ovi/vllm-awq4-qwen): Qwen 3.6 AWQ/DFlash vLLM path on Strix Halo.
- [`0xSero/Qwen3.6-35B-A3B-GGUF-Strix`](https://huggingface.co/0xSero/Qwen3.6-35B-A3B-GGUF-Strix): Strix-optimized Qwen3.6 GGUF quant variants.
- [`ggml-org/llama.cpp` speculative decoding docs](https://github.com/ggml-org/llama.cpp/blob/master/docs/speculative.md) and recent Vulkan/HIP changes.
- [ROCm](https://github.com/ROCm/ROCm/releases) and [vLLM](https://github.com/vllm-project/vllm/releases) release notes for gfx1151, AWQ, FP8 KV cache, and AMD backend changes.
