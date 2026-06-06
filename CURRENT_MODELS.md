# Current Model Triage

This page tracks fast-moving local-model targets that are useful for Strix Halo / Ryzen AI MAX+ 395 buyers, reviewers, and benchmark contributors.

It is not a leaderboard. The goal is to separate three questions that often get mixed together:

- Is the model current and interesting?
- Does it run locally on one 128 GB Strix Halo system?
- Is it fast, or is its value mainly capability, memory capacity, multimodality, or setup friction?

Measured rows below are first-party Beelink GTR9 Pro direct `llama-bench` Vulkan/RADV scouts unless stated otherwise. Normal workstation services were left running, so treat these as practical workstation scouts rather than cold/clean headline rows.

## Best Current Headline Rows

| Question | Best current row | Why it matters |
| --- | --- | --- |
| Fastest direct 30B-class Qwen MoE | Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`: 100.04 t/s direct `llama-bench` on b9467 | Shows a direct 30B-class Qwen route can cross 100 t/s on Strix Halo. Keep separate from the Qwen3-Coder headline and balanced-default rows. |
| Fastest current small-MoE scout | LFM2.5 8B-A1B `Q4_K_M`: 170.02 t/s generation-only and 168.96 tg128 in the latest/int-dot pp512/tg128 check | Shows how fast newer small active-parameter MoE routes can be. This is not a 30B-class capability replacement. |
| Largest current direct GGUF capacity route | Nemotron 3 Super 120B-A12B `UD-IQ4_XS`: 18.43 tg128 direct `llama-bench` on one 128 GB Strix Halo system | Proves a 120B-class MoE GGUF route can run directly on one box; value is capacity/currentness, not raw speed. |

## June 2026 Scout Results

| Model | Quant | Size class | Result | Read |
| --- | --- | ---: | ---: | --- |
| LFM2.5 8B-A1B | `Q4_K_M` | 5.1 GB / 8B.A1B | 3414.61 pp512 / 168.96 tg128; 170.02 tg128 generation-only on the 2026-06-05 int-dot rerun | Fastest new small-MoE result in this scout. Strong speed/currentness hook, but not a 30B-class capability comparison. |
| Nemotron 3 Nano 30B-A3B | `IQ4_XS` | 18.2 GB / 31B.A3.5B MoE | 1312.47 pp512 / 75.97 tg128 on the 2026-06-05 int-dot rerun | Practical NVIDIA Nemotron route for one Strix Halo system after the Nemotron 3 Ultra release. |
| Nemotron 3 Super 120B-A12B | `UD-IQ4_XS` | 64.5 GB / 120B.A12B MoE | 294.99 pp512 / 18.43 tg128 on the 2026-06-05 int-dot rerun | Missing middle Nemotron route: much larger than Nano, directly runnable as GGUF on one Strix Halo, but not a speed result. |
| Qwen3-Coder 30B-A3B | `IQ4_XS` | 16.4 GB / 30B.A3B | 1372.27 pp512 / 90.44 tg128; 90.72 tg128 generation-only | Negative/control row: `IQ4_XS` alone did not beat the older Qwen3-Coder Q4_K_S 98.51 t/s headline. |
| Qwen3 30B-A3B NEO-MAX | `IQ4_XS` | 16.4 GB / 30B.A3B | 1396.05 pp512 / 87.39 tg128; 87.77 tg128 generation-only | Alternate 30B-A3B control row; the 2507 100 t/s result does not generalize to every 30B-A3B IQ4_XS file. |
| Qwen3.5 35B-A3B | `IQ4_XS` | 19.7 GB / 35B.A3B | 1170.27 pp512 / 75.22 tg128; 75.53 tg128 generation-only | Current/larger Qwen comparator; newer or larger is not automatically faster. |
| Qwen3.5 9B | `Q4_K_M` | 5.7 GB / 9B dense | 1015.35 pp512 / 34.49 tg128; 34.34 tg128 generation-only | Useful comparator for current Gemma-vs-Qwen discussion. Not the newest Qwen family. |
| Gemma 4 12B IT | `IQ4_XS` | 6.4 GB / 12B | 680.17 pp512 / 25.74 tg128; 25.77 tg128 generation-only | New Google model runs locally. Use for current-model/multimodal coverage, not speed. |
| Gemma 4 12B IT | `Q4_K_M` | 7.4 GB / 12B | 684.92 pp512 / 24.42 tg128; 24.42 tg128 generation-only | Balanced Gemma route. Slower than Qwen3.5 9B and much slower than Qwen 30B-class MoE speed rows. |
| MiniMax M2.7 | `UD-IQ4_XS` | 108.4 GB / 230B.A10B MoE | 101.00 pp512 / 28.27 tg128; 28.60 tg128 generation-only | Large-model feasibility proof: 230B-class MoE runs locally on one Strix Halo. Not a speed result. |
| DeepSeek V4 Flash | `Q2_K` / 0xSero Spark-Mini targets | 103.3 GB original target; 52.6 GB local Spark-Mini file | Original route download-blocked; later smaller 0xSero/Spark-Mini local file still failed to load in `llama-bench` smoke attempts | Strong setup-friction evidence. Do not list as pass, speed result, or hardware limit without a successful load. |
| Nemotron 3 Ultra 550B-A55B | GGUF dry-run / BF16 / NVFP4 targets | 188.0 GB smallest scanned GGUF route; 1.1 TB BF16 / 352.4 GB NVFP4 | Artifact scan only | GGUF artifacts now exist, but the smallest scanned route is still too large for a practical one-box 128 GB Strix Halo internal-disk benchmark. |

Raw evidence:

- Gemma 4 12B: [`data/raw/2026-06-04/gemma-4-12b-it-direct-scout/`](data/raw/2026-06-04/gemma-4-12b-it-direct-scout/)
- Nimo Gemma 4 QAT/MTP follow-up: [`data/raw/2026-06-06/community-nimo-gemma4-qat-issue4/`](data/raw/2026-06-06/community-nimo-gemma4-qat-issue4/)
- Qwen3.5 9B comparator: [`data/raw/2026-06-04/qwen35-9b-q4km-direct-comparator/`](data/raw/2026-06-04/qwen35-9b-q4km-direct-comparator/)
- LFM2.5 8B-A1B: [`data/raw/2026-06-04/lfm25-8b-a1b-q4km-direct-scout/`](data/raw/2026-06-04/lfm25-8b-a1b-q4km-direct-scout/)
- Nemotron 3 Nano 30B-A3B: [`data/raw/2026-06-04/nemotron-3-nano-30b-a3b-iq4xs-direct-scout/`](data/raw/2026-06-04/nemotron-3-nano-30b-a3b-iq4xs-direct-scout/)
- Nemotron 3 Super 120B-A12B: [`data/raw/2026-06-04/nemotron-3-super-120b-a12b-udiq4xs-direct-scout/`](data/raw/2026-06-04/nemotron-3-super-120b-a12b-udiq4xs-direct-scout/)
- 2026-06-05 latest/int-dot rerun for LFM2.5, Nemotron Nano, Nemotron Super, Qwen3-30B-A3B-Instruct-2507, and Qwen3-Coder UD: [`data/raw/2026-06-05/latest-llamacpp-intdot-regression/`](data/raw/2026-06-05/latest-llamacpp-intdot-regression/)
- Qwen3-Coder IQ4_XS control: [`data/raw/2026-06-03/qwen3-coder-iq4xs-direct-scout/`](data/raw/2026-06-03/qwen3-coder-iq4xs-direct-scout/)
- Qwen3 30B-A3B NEO-MAX IQ4_XS control: [`data/raw/2026-06-03/qwen3-30b-a3b-neo-max-iq4xs-direct-scout/`](data/raw/2026-06-03/qwen3-30b-a3b-neo-max-iq4xs-direct-scout/)
- Qwen3.5 35B-A3B IQ4_XS control: [`data/raw/2026-06-03/qwen35-35b-a3b-iq4xs-direct-scout/`](data/raw/2026-06-03/qwen35-35b-a3b-iq4xs-direct-scout/)
- MiniMax M2.7: [`data/raw/2026-06-03/minimax-m27-ud-iq4xs-local-smoke/`](data/raw/2026-06-03/minimax-m27-ud-iq4xs-local-smoke/)
- DeepSeek V4 Flash attempt: [`data/raw/2026-06-03/deepseek-v4-flash-q2k-download-attempt/`](data/raw/2026-06-03/deepseek-v4-flash-q2k-download-attempt/)
- DeepSeek V4 Flash 0xSero/Spark-Mini load failure: [`data/raw/2026-06-05/deepseek-v4-flash-0xsero-load-failure/`](data/raw/2026-06-05/deepseek-v4-flash-0xsero-load-failure/)
- Large-model feasibility scan: [`data/raw/2026-06-03/large-model-feasibility-scan/`](data/raw/2026-06-03/large-model-feasibility-scan/)
- Triage notes: [`data/raw/2026-06-04/latest-model-viral-scan/`](data/raw/2026-06-04/latest-model-viral-scan/), [`data/raw/2026-06-05/model-update-scan/`](data/raw/2026-06-05/model-update-scan/)

## Related Controls Already Covered Elsewhere

These rows are useful for context, but they are not promoted as new headline claims:

| Route | Result | Why it stays secondary |
| --- | ---: | --- |
| Qwen3-Coder-Next 80B-A3B `IQ4_XS` direct | 61.91 tg128 / 738.98 pp512 | Modern coding-model row for currentness. It is useful, but not a speed replacement for the 30B Qwen rows. |
| Qwen3.6 35B-A3B MTP repeat | 97.08 t/s six-prompt mean; 106.24 t/s max | Confirms code prompts can cross 100 t/s, but broad repeat average did not reproduce the earlier 101.1 t/s run. Keep as server/speculative evidence. |
| Qwen3-Coder 30B high-power policy check | 95.18 tg128 auto policy, 96.37 tg128 high policy | Shows power policy can help this Beelink run, but did not reproduce the tuned external GMKtec 100 t/s report. |
| Qwen3.6 27B dense Q8 control | 7.70 tg128 direct follow-up | Useful response to model requests, but this dense Q8 route is not a speed candidate versus the 35B-A3B MoE paths. |

Raw evidence:

- Qwen3-Coder-Next and MTP repeat: [`data/raw/2026-06-02/modern-model-clean-followup/`](data/raw/2026-06-02/modern-model-clean-followup/)
- High-power policy check: [`data/raw/2026-06-02/high-power-policy-test/`](data/raw/2026-06-02/high-power-policy-test/)
- Qwen3.6 27B dense follow-up: [`data/raw/2026-06-02/reddit-look-int-dot-reproduction/`](data/raw/2026-06-02/reddit-look-int-dot-reproduction/)

## What This Means

### Speed

For text generation speed, model architecture dominates. LFM2.5 8B-A1B is much faster than Gemma 4 12B in this scout because it is a small active-parameter MoE route. This does not mean it replaces larger coding or reasoning models.

The existing Qwen 30B-class rows remain the stronger 30B speed story:

- Qwen3-Coder 30B-A3B `Q4_K_S`: 98.51 t/s direct first-party Beelink headline.
- Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`: 100.04 t/s direct first-party scout on b9467; 99.10 t/s generation-only on the 2026-06-05 latest/int-dot rerun.

Keep those separate from small-model speed results.

### Currentness

Gemma 4 12B is the strongest current-model brand hook in this scout. The practical result is not "Gemma is fastest"; it is "a newly released Google local model runs on Strix Halo, and the guide can show exactly how it compares."

The Nimo community follow-up adds a second Gemma 4 lesson for QAT/server users: matched QAT MTP assistant heads can materially improve single-stream decode and acceptance on Gemma 4 12B, 26B-A4B, and 31B QAT Q4_0 rows, but the current Atomic TurboQuant path is still an advanced server route with a `PARALLEL=2` caveat. Keep this separate from first-party direct `llama-bench` rows.

Qwen3.5 9B is useful only as a community-discussion comparator. For current Qwen framing, prefer the existing Qwen3.6 rows in this guide.

### Capacity

MiniMax M2.7 is the best current evidence that 128 GB unified memory changes what a mini PC can attempt. A 108 GB GGUF route loaded and generated locally. That is valuable for buyers even though it is not fast.

DeepSeek V4 Flash shows a different adoption blocker: one route was blocked by 100GB+ download/resume friction, while a later smaller 0xSero/Spark-Mini local file still failed during `llama-bench` load. That is not a hardware speed result, but it is valuable adoption-friction evidence.

Nemotron 3 Ultra shows the same pattern at a larger scale. The new Ultra release is important, and a GGUF route was found in the 2026-06-05 follow-up scan. The smallest scanned Ultra GGUF route was still about 188 GB, so it remains a watchlist/external-storage/multi-node target rather than a practical one-box 128 GB Strix Halo benchmark. The practical NVIDIA family map is now: Ultra as watchlist, Super 120B-A12B as the larger direct GGUF capacity route, and Nano 30B-A3B as the faster practical route.

## Good Post Hooks

- "LFM2.5 8B-A1B at 170 t/s generation-only on Strix Halo: new small-MoE models are a different speed class."
- "Google Gemma 4 12B runs locally on Strix Halo, but Qwen/LFM are faster for text-only generation."
- "Current model reality check: newest does not automatically mean fastest."
- "A 230B-class MiniMax MoE runs locally on one 128 GB Strix Halo system, but speed and capacity are different wins."
- "NVIDIA Nemotron 3 Ultra just dropped; on one 128 GB Strix Halo, Super 120B-A12B is the runnable middle route and Nano 30B-A3B is the faster route."
- "Nemotron 3 Super 120B-A12B runs directly on Strix Halo: 295.0 pp512 / 18.4 tg128 via `llama.cpp` Vulkan/RADV."
- "The hidden local-AI friction is not just GPU speed. It is model format, quant choice, download size, backend support, and reproducible commands."

## Guide Value To Add

The most useful public addition is not another single headline number. It is a repeatable "current model triage" workflow:

1. Check whether the model has official or credible GGUF artifacts.
2. Record artifact size, architecture, context length, and quant options before downloading.
3. Run one balanced quant and one speed/footprint quant when available.
4. Keep speed rows, large-model load proofs, MTP/server rows, and download-blocked attempts separate.
5. Explain what buyer uncertainty the result removes: speed, currentness, capacity, setup path, or distribution friction.

This helps buyers and vendors because it turns "can this AI PC run the latest models?" into dated, reproducible evidence instead of scattered social screenshots.

The Nemotron 3 Super row is also an example of the community feedback loop documented in [`COMMUNITY_FEEDBACK.md`](COMMUNITY_FEEDBACK.md): a public correction identified a missing route, and the guide added a measured result instead of leaving the original framing unchanged.

## Highest-Value Next Tests

These are prioritized for buyer/vendor guide value, not social-media hooks:

| Priority | Test | Why it adds guide value |
| ---: | --- | --- |
| 1 | `llama.cpp` latest-release regression check on the Qwen3-Coder 30B headline, Qwen3-30B-A3B-Instruct-2507, Nemotron Super, and LFM2.5 rows | Shows whether users should update or pin their `llama.cpp` build. Recent releases are moving quickly, so this directly reduces setup uncertainty. |
| 2 | Ollama 0.30.x Windows/Linux sanity check for one default chat model and one 30B-class MoE | Ollama is the easiest buyer path. Version drift matters more to typical users than another raw `llama-bench` row. |
| 3 | Nemotron Super quant comparison: `UD-IQ2_M` or `UD-Q2_K_XL` versus current `UD-IQ4_XS` if storage permits | Answers whether lower quants make 120B-class Nemotron meaningfully faster or more practical on one Strix Halo box. |
| 4 | DeepSeek V4 Flash runtime/loadability follow-up on a smaller route | The 0xSero/Spark-Mini file existed locally but did not load in current smoke attempts. Next value comes from identifying whether this is GGUF compatibility, runtime support, or build/backend mismatch. |
| 5 | External-storage feasibility plan for Ultra/Kimi/GLM class routes | These are not current one-box internal-disk targets. A clean external NVMe plan would answer whether 128 GB unified memory can at least smoke/load the smallest extreme routes. |

## Watch List

| Target | Status |
| --- | --- |
| Qwen3.6 new quants/sources | Already important in the guide. Add only if a new source answers a new question. |
| Kimi K2.6 | Very high viral value, but direct GGUF routes are currently too large for quick single-box internal-disk testing. |
| Kimi K3 | No concrete local artifact found during the 2026-06-04 scan. Treat as watch item, not benchmarkable evidence. |
| MiniMax M3 | Watch for actual local weights/GGUF artifacts before claiming a benchmark path. |
| DeepSeek V4 Flash | Original 103GB route was download-blocked; smaller 0xSero/Spark-Mini route reached local load attempts but failed before benchmarking. Watch for compatible GGUF/runtime fixes before claiming performance. |
| Nemotron 3 Ultra 550B-A55B | GGUF route found in the 2026-06-05 scan, but the smallest scanned route is about 188 GB. Watch for smaller practical artifacts or test only with external storage / multi-node planning. |
| Nemotron 3 Super 120B-A12B | Tested with `UD-IQ4_XS`. Add lower/higher quant comparisons only if they answer a specific buyer question. |

## Sources

- Google Gemma 4 12B announcement: <https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12b/>
- Gemma 4 12B GGUF: <https://huggingface.co/ggml-org/gemma-4-12B-it-GGUF>
- Gemma 4 12B GGUF: <https://huggingface.co/unsloth/gemma-4-12b-it-GGUF>
- LFM2.5 8B-A1B GGUF: <https://huggingface.co/LiquidAI/LFM2.5-8B-A1B-GGUF>
- Qwen3.5 9B GGUF: <https://huggingface.co/unsloth/Qwen3.5-9B-GGUF>
- Nemotron 3 Nano 30B-A3B GGUF: <https://huggingface.co/unsloth/Nemotron-3-Nano-30B-A3B-GGUF>
- Nemotron 3 Super 120B-A12B GGUF: <https://huggingface.co/unsloth/NVIDIA-Nemotron-3-Super-120B-A12B-GGUF>
- Nemotron 3 Ultra 550B-A55B GGUF: <https://huggingface.co/unsloth/NVIDIA-Nemotron-3-Ultra-550B-A55B-GGUF>
- Nemotron 3 Ultra BF16: <https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16>
- Nemotron 3 Ultra NVFP4: <https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-NVFP4>
