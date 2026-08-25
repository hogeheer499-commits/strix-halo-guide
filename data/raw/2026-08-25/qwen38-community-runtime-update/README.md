# Qwen3.8 Community And Runtime Update

Checked 2026-08-25. This note separates first-party measurements, external
community evidence, and open upstream reports.

## First-Party Baseline Retained

The guide's default measured Qwen3.8 route remains Ollama 0.32.13 on the
Beelink GTR9 Pro: 292.49 prompt t/s and 20.42 generation t/s over nine warm
API repeats, with image, tool-call, thinking, and exact-retrieval smokes passing
through 50,059 prompt tokens. A 56,051-token attempt caused a recoverable
Vulkan DeviceLost. See the
[`2026-08-15 raw evidence`](../../2026-08-15/qwen38-27b-ollama-03213-vulkan-radv/).

## External GMKtec Long-Context Evidence

Kyanite Labs published an MIT-licensed evidence repository and an official
`llama.cpp` discussion for Qwen3.8 27B on a GMKtec EVO-X2. The current system
correction says 96GB physical memory with a 64GB GTT carve; early table rows
that called it a 64GB-unified-memory system are stale. The route uses native
Ubuntu 24.04, kernel 6.17, ROCm 7.2.4, a Qwen3.8 27B `UD-Q4_K_XL` artifact,
and a patched/reverted b10435-era HIP build.

Useful scoped results from the public artifact:

- exact needle retrieval passed 13/13 cases at varied depths/seeds, including
  one exact match at 261,130 evaluated tokens in a 262,144-token allocation;
- the real-image battery passed 6/6 pilot screenshots;
- a three-prompt, four-way server A/B measured 15.1 seconds for MTP versus
  17.8 seconds with speculative decoding off for 200 generated tokens (about
  18% lower elapsed time on that exact workload); n-gram alone added no
  material benefit there;
- repetition-heavy count benchmarks produced much higher numbers than novel
  traffic, so those peaks are not general generation-speed claims.

This evidence shows that 262K-class retrieval can work on Strix Halo and makes
the local 56K DeviceLost stack-specific rather than a model or hardware ceiling.
It does not replace the beginner route: it uses a patched/unmerged HIP path, a
different quant, and a different system/runtime.

Sources:

- <https://github.com/KyaniteLabs/qwen38-27b-strix-halo>
- <https://github.com/ggml-org/llama.cpp/discussions/27154>

## Qwen3.8 MTP Community A/B

The public `qwen38-mtp` matrix requires paired A/B runs. A GMKtec/Windows
Vulkan submission reports `UD-Q4_K_XL`, 32K q8 KV, and the same b10437 server
configuration at 11.5 t/s median without speculation versus 23.7 t/s with
MTP `n=2` (+106%) across three runs of three prompts, with 78.2% reported draft
acceptance. No raw logs are attached to that pull request, so this remains a
community-reported lead, not a guide headline.

Sources:

- <https://github.com/sudoingX/qwen38-mtp>
- <https://github.com/sudoingX/qwen38-mtp/pull/9>

## Same-Day Performance Frontier: Leads, Not Headlines

Several public Qwen3.8 routes moved quickly after the official release. They
answer different questions and should not be collapsed into one leaderboard:

- a stock `llama.cpp` b10503 community A/B reports Q8_0 MTP moving from 7.3
  to 22.4 t/s on a 128GB Strix Halo laptop;
- a separately tuned Vulkan/ROCmFP4/DFlash2 route reports about 52 t/s on a
  coding prompt, about 31 t/s on prose, and a context-dependent crossover to
  ROCm for deep or cold prompt ingestion;
- a follow-up adaptive-speculation fork reports 65 t/s decode, but the author
  stated that the matching Qwen3.8 FP4 DFlash sidecar was not yet published at
  the time checked and explicitly requested independent confirmation;
- the PieBru evidence repository publishes a lower Q6 route with committed
  logs and a quality-first framing. It is useful precisely because its model,
  quant, prompt, power, and evidence policy differ from the speed-first rows.

These are valuable reproduction targets, not guide-owned performance claims.
The comparison must preserve model/quant, backend, runtime fork, speculation,
prompt type, context depth, cache behavior, generated-token count, and raw
artifacts. See the structured
[`Qwen3.8 route matrix`](../../../qwen38_route_matrix.csv) and the public
[`Qwen3.8 decision page`](../../../../QWEN38_STRIX_HALO.md).

Sources checked 2026-08-25:

- <https://www.reddit.com/r/StrixHalo/comments/1vsstxm/qwen3827b_benchmarks_on_strix_halo_q8_0_mtp_21_ts/>
- <https://www.reddit.com/r/StrixHalo/comments/1vwm4p3/qwen38_27b_new_record_on_strix_halo_52_tokens_per/>
- <https://www.reddit.com/r/StrixHalo/comments/1vxx51g/qwen38_27b_65_ts_decode_try_it_out/>
- <https://github.com/PieBru/Qwen-3.8-27B_Strix-Halo_gfx1151>

## Runtime Alerts

- Official `llama.cpp` v0.3.0 is the latest semantic release and b10622 the
  latest numbered build checked here; neither is locally qualified.
- Open issue #26209 reports silent repeated/garbled output on Strix Halo HIP
  after integrated `ROCm_Host` compute buffers were enabled. Open PR #25863
  avoids that direct compute-buffer path; multiple community controls report
  restored long-context and vision correctness. The b10622 source still marks
  the APU integrated and still accepts `ROCm_Host` buffers, so the guide's old
  b10046 small-model allocation smoke cannot be generalized to long-context,
  multimodal, or multi-slot correctness.
- Ollama 0.32.15 is the latest stable release checked. It is an unmeasured
  package target, not a replacement for the reboot-qualified 0.31.2 service or
  the measured Qwen3.8 0.32.13 route.
- Ollama issue #17906 reports that Anthropic-compatible `thinking: xhigh` is
  mapped to `high`, which the Qwen3.8 template rejects on 0.32.13 and 0.32.15;
  native `/api/chat` works in the report. This is not locally reproduced.
- Open issue #27615 reports a Qwen3.8 slowdown with a very large tool schema.
  It is not Strix-Halo-specific and remains an unconfirmed agent-workload test
  lead rather than a guide claim.

Sources:

- <https://github.com/ggml-org/llama.cpp/releases/tag/b10622>
- <https://github.com/ggml-org/llama.cpp/releases/tag/v0.3.0>
- <https://github.com/ggml-org/llama.cpp/issues/26209>
- <https://github.com/ggml-org/llama.cpp/pull/25863>
- <https://github.com/ollama/ollama/releases/tag/v0.32.15>
- <https://github.com/ollama/ollama/issues/17906>
- <https://github.com/ggml-org/llama.cpp/issues/27615>

## Next Controlled Test

Run stock b10622 versus PR #25863 on the same local Qwen3.8 artifact and host,
covering short text, 4K/16K nonce correctness, image input, multiple slots, and
long-context retrieval. Preserve model SHA256, exact source commit, commands,
outputs, kernel/Mesa/ROCm state, and failures before changing a public default.
