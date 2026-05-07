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
- vLLM/AWQ/DFlash is promising for OpenAI-compatible agent serving, tool calls, vision, and long context, but this guide has not reproduced it locally yet.

Current fastest local headline:

- Current latest-stack direct path: Qwen3-Coder 30B-A3B at 96.15 t/s on llama.cpp b9049, Vulkan/RADV.
- Historical peak: Qwen3-Coder 30B-A3B at 97.24 t/s on b9010.
- Treat 96-97 t/s as the current stable ceiling for the measured Qwen3-Coder path until a new build, quant, or decode method beats it with raw logs.

## Highest-Value Open Tests

### P0: Qwen3.6 Quant Sweep

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

### P0: Same-Build HIP vs Vulkan

Why: our local crossover result is directionally useful but not a perfect same-build comparison. A clean same-commit b9049+ Vulkan/HIP build would make the backend recommendation much harder to argue against.

Test matrix:

- Models: Qwen3.6 35B-A3B, Qwen3-Coder 30B-A3B, gpt-oss-120b if stable.
- Backends: Vulkan/RADV and HIP/ROCm from the same llama.cpp commit.
- Rows: pp512, pp2048, pp8192, pp16384, tg128, filled-context decode where practical.

Expected outcome:

- Vulkan remains the short-generation recommendation.
- HIP may win long-prompt prefill.
- The guide becomes stronger because it explains the split instead of pretending there is one universal winner.

### P1: Qwen3-Coder Max-Speed Sweep

Why: this directly targets the 96-97 t/s headline. The next useful question is whether the Beelink can cross 100 t/s on a still-useful coding model.

Levers:

- llama.cpp b9049 or newer Vulkan/RADV.
- Batch and ubatch sweep: `-b/-ub 512`, `1024`, `2048`, maybe `4096` if memory and stability allow.
- KV cache variants: f16, q8_0, q4_0 where quality is acceptable.
- Quant variants if available: Q4_K_M, Q4_K_S, IQ4, Q5, UD-Q4_K_XL.
- `llama-bench` and `llama-server` API route, because user-visible speed can differ.

Pass condition:

- Any "over 100 t/s" claim needs raw logs, repeat count, exact model hash, and a note if the quant is lower quality than the current headline quant.

### P1: gpt-oss-120b Long-Context Sweep

Why: 120B on 128GB unified memory is the kind of result people share. The current guide proves it loads and generates around 50.59 t/s, but not how far context can be pushed before wall time becomes painful.

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
- NPU LLM testing is not a max-performance path for these models.
- Full OS upgrade is not a first move for Vulkan performance. Ubuntu 24.04 with current kernel/Mesa already reaches the current measured peak.
- Windows testing is useful for completeness, but not likely to beat the current Linux/RADV headline.

## Recommended Campaign Order

1. Run the Qwen3.6 quant sweep.
2. Run same-build HIP vs Vulkan on current llama.cpp.
3. Run the Qwen3-Coder max-speed sweep.
4. Extend gpt-oss-120b into long-context rows.
5. Attempt tuned ROCm/rocWMMA.
6. Attempt vLLM AWQ/DFlash reproduction.
7. Add sustained thermals/power validation.

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
