# Qwen3.8 27B on AMD Strix Halo: What Works, What Is Fast, and What Is Actually Verified

**Evidence reviewed:** August 30, 2026.

Qwen3.8 27B is a practical dense multimodal model on AMD Strix Halo / Ryzen AI
MAX+ 395 with Radeon 8060S and 96GB/128GB unified memory. The difficult part is
no longer whether it runs. The difficult part is choosing between a simple
official route, a reproducible stock runtime, long-context correctness, and
much faster experimental speculative-decoding stacks without comparing unlike
results.

This page separates those routes. It is not a single-number leaderboard.

## Short Answer

- **Start with the official Ollama artifact** if you want the least complicated
  chat, image, tool-call, and thinking route already measured by this guide.
- **Use direct stock `llama.cpp` as the reproducibility control** before testing
  MTP, DFlash, ROCmFP4, custom quants, or performance forks.
- **Treat 52-65 t/s posts as advanced reproduction targets**, not as proof that
  every Qwen3.8 setup reaches that speed.
- **Choose the backend around context behavior as well as decode speed.** Current
  community evidence reports a fast Vulkan lane for shorter/growing context and
  a slower ROCm lane that behaves better for deep or cold prompt ingestion.
- **Do not generalize one local failure into a hardware limit.** This guide's
  Ollama/RADV route passed exact retrieval through 50,059 prompt tokens and hit
  a recoverable device loss at 56,051, while separate corrected GMKtec evidence
  reached 261,130 evaluated tokens.

## Current Route Matrix

| Route | Evidence class | What it shows | What it does not show |
| --- | --- | --- | --- |
| Official `qwen3.8:27b` through Ollama 0.32.13 / Vulkan-RADV | **First-party measured** on Beelink GTR9 Pro 128GB | 292.49 prompt t/s and 20.42 generation t/s over nine warm repeats; image, tools, thinking, and exact retrieval through 50,059 prompt tokens passed | Not direct `llama-bench`; not broad quality; not 262K validation |
| Corrected Kyanite Labs GMKtec route | **External public package** on GMKtec EVO-X2 96GB | 13/13 retrieval cases including 261,130 evaluated tokens; 6/6 image pilot; small MTP/no-spec A/B | Patched/reverted HIP build and different quant/system; not a beginner default |
| Stock b10503 Q8_0 MTP report | **Community-reported** Strix Halo laptop | Reported 7.3 to 22.4 t/s matched MTP uplift | Raw package has not been imported into this guide; not first-party |
| Tuned Vulkan + ROCmFP4 + DFlash2 route | **Community-reported advanced route** | About 52 t/s on code and 31 t/s on prose in the detailed public report; exposes context/prefill tradeoffs | Different fork, quant, drafter, prompt, and request shape from the Ollama route |
| Adaptive-speculation 65 t/s report | **Unverified current lead** | A promising fork-level speed target and a request for independent validation | Matching Qwen3.8 FP4 DFlash sidecar was unpublished when checked; not reproducible end to end yet |
| PieBru Q6 quality-first route | **External public package** | Committed setup/evidence policy and a reported roughly 17-21 t/s sustained Q6 route | Different quality/speed objective; not evidence that Q6 should match FP4/Q4 speed |

The machine-readable version is
[`data/qwen38_route_matrix.csv`](data/qwen38_route_matrix.csv). First-party raw
evidence is under
[`data/raw/2026-08-15/qwen38-27b-ollama-03213-vulkan-radv/`](data/raw/2026-08-15/qwen38-27b-ollama-03213-vulkan-radv/).
The external/runtime provenance review is under
[`data/raw/2026-08-25/qwen38-community-runtime-update/`](data/raw/2026-08-25/qwen38-community-runtime-update/).

## Easiest Measured Route

The tested official model is `qwen3.8:27b`, a 17.7GB-decimal `Q4_K_M`
artifact reporting 27.3B dense parameters and a 262,144-token model context
limit. On the measured Ollama 0.32.13 system service:

```bash
ollama run qwen3.8:27b
```

Keep the Strix Halo service environment documented in the main guide,
including `OLLAMA_VULKAN=1` and `OLLAMA_IGPU_ENABLE=1`. The current Ollama 0.33.2
package is a test target, not an automatic inheritance of the 0.32.13
results. The normal 0.31.2 service remains the guide's full-reboot-qualified
general beginner baseline until the controlled upgrade matrix passes.

## Why 20, 22, 31, 52, and 65 t/s Can All Be Honest

Those numbers can differ without contradicting each other because at least
eight variables change:

1. official Ollama artifact versus a custom GGUF;
2. Q8/Q6/Q4/ROCmFP4 or another custom quant;
3. Ollama API versus direct `llama.cpp` versus `llama-server`;
4. stock runtime versus a pinned performance fork;
5. no speculation versus MTP versus DFlash2 or adaptive speculation;
6. code, prose, repetition-heavy, or agent/tool prompts;
7. cold prompt ingestion versus cached turn-by-turn context growth;
8. generated-token count, context depth, acceptance rate, and host state.

A useful result records all eight. A screenshot with only “tokens per second”
does not establish a portable buyer recommendation.

## Matched Benchmark Ladder Still Needed

The highest-value next local campaign is not another isolated peak. It is a
matched ladder on the same host and pinned model artifact:

1. stock b10687 Vulkan, no speculation;
2. stock b10687 Vulkan, native MTP;
3. stock b10687 versus PR #25863 on HIP for exact-output correctness;
4. a published ROCmFP4 route with no-spec and MTP controls;
5. a fully published DFlash/adaptive route only after target and sidecar hashes
   are available.

Each lane should use code and prose prompts, 4K/16K/50K context, 200- and
512-token generation, exact-output/correctness controls, acceptance metrics,
model hashes, memory, versions, and raw logs. Vision, tools, and multi-slot
checks remain separate from text speed.

The live queue is [`data/current_test_queue.csv`](data/current_test_queue.csv).

## Buyer Decision

| If you want | Start here |
| --- | --- |
| The simplest current official multimodal route | Ollama 0.32.13 evidence plus `qwen3.8:27b`; wait for the 0.33.2 qualification before transferring the measurements |
| Auditable direct performance | Stock `llama.cpp` control with a pinned GGUF and exact command |
| Maximum short-context experimental speed | Reproduce the published fork, quant, and drafter as one inseparable profile |
| Deep or cold context | Prefer the route with demonstrated prompt-ingestion behavior and exact retrieval, not the highest short decode number |
| Production agent use | Add tool-schema size, native/compatible API shapes, restart, output correctness, and real task quality before choosing |

## Current Alerts

- `llama.cpp` issue [#26209](https://github.com/ggml-org/llama.cpp/issues/26209)
  reports silent repeated/garbled output on Strix Halo HIP after integrated
  `ROCm_Host` compute buffers were enabled. Candidate PR
  [#25863](https://github.com/ggml-org/llama.cpp/pull/25863) needs a matched
  local correctness A/B before stock HIP becomes general guidance.
- Ollama issue [#17906](https://github.com/ollama/ollama/issues/17906) reports
  an Anthropic-compatible Qwen3.8 `xhigh` mapping failure on 0.32.13 and
  0.32.15; native `/api/chat` worked in that report. This guide has not yet
  reproduced the compatibility failure.
- `llama.cpp` issue [#27615](https://github.com/ggml-org/llama.cpp/issues/27615)
  reports a Qwen3.8 slowdown with a very large tool schema. Treat agent
  workloads as a separate qualification surface.

## Public Sources And Scope

- Official model: <https://huggingface.co/Qwen/Qwen3.8-27B>
- Official Ollama artifact: <https://ollama.com/library/qwen3.8:27b>
- Kyanite Labs corrected long-context package: <https://github.com/KyaniteLabs/qwen38-27b-strix-halo>
- Stock b10503/Q8 community matrix: <https://www.reddit.com/r/StrixHalo/comments/1vsstxm/qwen3827b_benchmarks_on_strix_halo_q8_0_mtp_21_ts/>
- Detailed 52 t/s/context discussion: <https://www.reddit.com/r/StrixHalo/comments/1vwm4p3/qwen38_27b_new_record_on_strix_halo_52_tokens_per/>
- Adaptive 65 t/s validation request: <https://www.reddit.com/r/StrixHalo/comments/1vxx51g/qwen38_27b_65_ts_decode_try_it_out/>
- PieBru evidence repository: <https://github.com/PieBru/Qwen-3.8-27B_Strix-Halo_gfx1151>

Community and external results remain separate from first-party Beelink
measurements. No source above implies AMD, Qwen, Beelink, GMKtec, or other OEM
endorsement of this guide.

## Commercial And Affiliate Disclosure

This guide contains no affiliate links as of August 30, 2026. If affiliate
links are added later, each will be labeled near the link and recorded in
[`data/affiliate_link_registry.csv`](data/affiliate_link_registry.csv).
Affiliate availability or commission will not determine benchmark inclusion,
ranking, negative-result retention, or conclusions. See
[`VENDOR_DISCLOSURE.md`](VENDOR_DISCLOSURE.md).

If this page saved you testing time, useful support is a GitHub star, a
correction, or a reproducible result from another Strix Halo system.
