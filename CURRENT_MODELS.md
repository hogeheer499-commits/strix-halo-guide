# Current Model Triage

This page tracks fast-moving local-model targets that are useful for Strix Halo / Ryzen AI MAX+ 395 buyers, reviewers, and benchmark contributors.

It is not a leaderboard. The goal is to separate three questions that often get mixed together:

- Is the model current and interesting?
- Does it run locally on one 128 GB Strix Halo system?
- Is it fast, or is its value mainly capability, memory capacity, multimodality, or setup friction?

Measured rows below are first-party Beelink GTR9 Pro direct `llama-bench` Vulkan/RADV scouts unless stated otherwise. normal workstation services were left running, so treat these as practical workstation scouts rather than cold/clean headline rows.

## June 2026 Scout Results

| Model | Quant | Size class | Result | Read |
| --- | --- | ---: | ---: | --- |
| LFM2.5 8B-A1B | `Q4_K_M` | 5.1 GB / 8B.A1B | 1772.48 pp512 / 135.82 tg128; 139.30 tg128 generation-only | Fastest new small-MoE result in this scout. Strong speed/currentness hook, but not a 30B-class capability comparison. |
| Nemotron 3 Nano 30B-A3B | `IQ4_XS` | 18.2 GB / 31B.A3.5B MoE | 619.00 pp512 / 65.45 tg128; 66.60 tg128 generation-only | Practical NVIDIA Nemotron route for one Strix Halo system after the Nemotron 3 Ultra release. |
| Qwen3.5 9B | `Q4_K_M` | 5.7 GB / 9B dense | 1015.35 pp512 / 34.49 tg128; 34.34 tg128 generation-only | Useful comparator for current Gemma-vs-Qwen discussion. Not the newest Qwen family. |
| Gemma 4 12B IT | `IQ4_XS` | 6.4 GB / 12B | 680.17 pp512 / 25.74 tg128; 25.77 tg128 generation-only | New Google model runs locally. Use for current-model/multimodal coverage, not speed. |
| Gemma 4 12B IT | `Q4_K_M` | 7.4 GB / 12B | 684.92 pp512 / 24.42 tg128; 24.42 tg128 generation-only | Balanced Gemma route. Slower than Qwen3.5 9B and much slower than Qwen 30B-class MoE speed rows. |
| MiniMax M2.7 | `UD-IQ4_XS` | 108.4 GB / 230B.A10B MoE | 101.00 pp512 / 28.27 tg128; 28.60 tg128 generation-only | Large-model feasibility proof: 230B-class MoE runs locally on one Strix Halo. Not a speed result. |
| DeepSeek V4 Flash | `Q2_K` target | 103.3 GB target | Download attempt only; partial reached about 53 GiB | Distribution/download friction blocked this attempt before benchmarking. Do not list as pass or fail. |
| Nemotron 3 Ultra 550B-A55B | BF16 / NVFP4 targets | 1.1 TB BF16 / 352.4 GB NVFP4 | Artifact scan only | Major release, but not a direct one-box 128 GB Strix Halo GGUF/`llama.cpp` target yet. |

Raw evidence:

- Gemma 4 12B: [`data/raw/2026-06-04/gemma-4-12b-it-direct-scout/`](data/raw/2026-06-04/gemma-4-12b-it-direct-scout/)
- Qwen3.5 9B comparator: [`data/raw/2026-06-04/qwen35-9b-q4km-direct-comparator/`](data/raw/2026-06-04/qwen35-9b-q4km-direct-comparator/)
- LFM2.5 8B-A1B: [`data/raw/2026-06-04/lfm25-8b-a1b-q4km-direct-scout/`](data/raw/2026-06-04/lfm25-8b-a1b-q4km-direct-scout/)
- Nemotron 3 Nano 30B-A3B: [`data/raw/2026-06-04/nemotron-3-nano-30b-a3b-iq4xs-direct-scout/`](data/raw/2026-06-04/nemotron-3-nano-30b-a3b-iq4xs-direct-scout/)
- MiniMax M2.7: [`data/raw/2026-06-03/minimax-m27-ud-iq4xs-local-smoke/`](data/raw/2026-06-03/minimax-m27-ud-iq4xs-local-smoke/)
- DeepSeek V4 Flash attempt: [`data/raw/2026-06-03/deepseek-v4-flash-q2k-download-attempt/`](data/raw/2026-06-03/deepseek-v4-flash-q2k-download-attempt/)
- Triage notes: [`data/raw/2026-06-04/latest-model-viral-scan/`](data/raw/2026-06-04/latest-model-viral-scan/)

## What This Means

### Speed

For text generation speed, model architecture dominates. LFM2.5 8B-A1B is much faster than Gemma 4 12B in this scout because it is a small active-parameter MoE route. This does not mean it replaces larger coding or reasoning models.

The existing Qwen 30B-class rows remain the stronger 30B speed story:

- Qwen3-Coder 30B-A3B `Q4_K_S`: 98.51 t/s direct first-party Beelink headline.
- Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`: about 100 t/s direct first-party scout.

Keep those separate from small-model speed results.

### Currentness

Gemma 4 12B is the strongest current-model brand hook in this scout. The practical result is not "Gemma is fastest"; it is "a newly released Google local model runs on Strix Halo, and the guide can show exactly how it compares."

Qwen3.5 9B is useful only as a community-discussion comparator. For current Qwen framing, prefer the existing Qwen3.6 rows in this guide.

### Capacity

MiniMax M2.7 is the best current evidence that 128 GB unified memory changes what a mini PC can attempt. A 108 GB GGUF route loaded and generated locally. That is valuable for buyers even though it is not fast.

DeepSeek V4 Flash shows a different adoption blocker: a 100 GB single-file model can be blocked by download/resume friction before the hardware gets tested.

Nemotron 3 Ultra shows the same pattern at a larger scale. The new Ultra release is important, but the available BF16/NVFP4 artifacts are too large for one 128 GB Strix Halo system and were not found as a direct GGUF route during the 2026-06-04 scan. The practical NVIDIA route is Nemotron 3 Nano 30B-A3B GGUF.

## Good Post Hooks

- "LFM2.5 8B-A1B at 139 t/s on Strix Halo: new small-MoE models are a different speed class."
- "Google Gemma 4 12B runs locally on Strix Halo, but Qwen/LFM are faster for text-only generation."
- "Current model reality check: newest does not automatically mean fastest."
- "A 230B-class MiniMax MoE runs locally on one 128 GB Strix Halo system, but speed and capacity are different wins."
- "NVIDIA Nemotron 3 Ultra just dropped; the practical Strix Halo route today is Nemotron 3 Nano 30B-A3B at 66.6 t/s."
- "The hidden local-AI friction is not just GPU speed. It is model format, quant choice, download size, backend support, and reproducible commands."

## Guide Value To Add

The most useful public addition is not another single headline number. It is a repeatable "current model triage" workflow:

1. Check whether the model has official or credible GGUF artifacts.
2. Record artifact size, architecture, context length, and quant options before downloading.
3. Run one balanced quant and one speed/footprint quant when available.
4. Keep speed rows, large-model load proofs, MTP/server rows, and download-blocked attempts separate.
5. Explain what buyer uncertainty the result removes: speed, currentness, capacity, setup path, or distribution friction.

This helps buyers and vendors because it turns "can this AI PC run the latest models?" into dated, reproducible evidence instead of scattered social screenshots.

## Watch List

| Target | Status |
| --- | --- |
| Qwen3.6 new quants/sources | Already important in the guide. Add only if a new source answers a new question. |
| Kimi K2.6 | Very high viral value, but direct GGUF routes are currently too large for quick single-box internal-disk testing. |
| Kimi K3 | No concrete local artifact found during the 2026-06-04 scan. Treat as watch item, not benchmarkable evidence. |
| MiniMax M3 | Watch for actual local weights/GGUF artifacts before claiming a benchmark path. |
| DeepSeek V4 Flash | Resume or retry the existing partial download from a more stable network path. |
| Nemotron 3 Ultra 550B-A55B | Watch for GGUF or smaller practical artifacts. Current BF16/NVFP4 artifacts are too large for direct one-box Strix Halo testing. |

## Sources

- Google Gemma 4 12B announcement: <https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12b/>
- Gemma 4 12B GGUF: <https://huggingface.co/ggml-org/gemma-4-12B-it-GGUF>
- Gemma 4 12B GGUF: <https://huggingface.co/unsloth/gemma-4-12b-it-GGUF>
- LFM2.5 8B-A1B GGUF: <https://huggingface.co/LiquidAI/LFM2.5-8B-A1B-GGUF>
- Qwen3.5 9B GGUF: <https://huggingface.co/unsloth/Qwen3.5-9B-GGUF>
- Nemotron 3 Nano 30B-A3B GGUF: <https://huggingface.co/unsloth/Nemotron-3-Nano-30B-A3B-GGUF>
- Nemotron 3 Ultra BF16: <https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16>
- Nemotron 3 Ultra NVFP4: <https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-NVFP4>
