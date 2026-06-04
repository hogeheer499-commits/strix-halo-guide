# Latest Model Viral Scan

Purpose: triage newly discussed/open local models for Strix Halo benchmark and post value.

This is a research/triage note. Do not treat entries here as benchmark claims unless a linked raw benchmark exists.

## Priority Read

| Target | Current status | Strix Halo post value | Next action |
| --- | --- | --- | --- |
| Gemma 4 12B IT | Officially announced 2026-06-03; GGUFs available from `ggml-org` and `unsloth`. | High. New Google model, laptop/unified-memory framing, multimodal/audio/vision/MTP claims. | Tested locally; see `../gemma-4-12b-it-direct-scout/`. |
| Qwen3.6 | Newer and more relevant than Qwen3.5 for current Strix Halo posts. | High, but already partly covered by existing guide rows for 35B-A3B, 27B, and MTP. | Use existing guide evidence first; only add new Qwen3.6 tests if they answer a new model/source/quant question. |
| Qwen3.5-9B | Active community comparison target, but not the newest Qwen line. | Medium. Useful if replying to Gemma 4 12B vs Qwen3.5-9B Reddit discussions. Weak as a standalone "latest model" headline. | Optional comparator only. `Q4_K_M` was tested locally; see `../qwen35-9b-q4km-direct-comparator/`. |
| LFM2.5-8B-A1B | Tested after Gemma. | High for speed/currentness, lower for broad name recognition than Google/Qwen/Kimi. | Use as the fast "new small MoE" result; see `../lfm25-8b-a1b-q4km-direct-scout/`. |
| Kimi K3 | No concrete HF/GGUF target found during this scan. | Watch item only. | Do not claim it exists locally until official/model-hub artifacts are found. |
| Kimi K2.6 | Real and very high-viral-value, but public GGUF routes are huge. | High concept value, low single-box practicality without external storage/runtime plan. | Keep as a capacity/runtime story, not a quick direct benchmark. |
| MiniMax M3 | Officially announced/watch target, but local weights/GGUF were not found in the previous scan. | High if weights appear. | Watch for actual artifacts before benchmark planning. |

## Model-Hub Checks

Gemma 4 12B:

```text
google/gemma-4-12B-it
unsloth/gemma-4-12b-it-GGUF
ggml-org/gemma-4-12B-it-GGUF
```

Notable scan facts:

- `unsloth/gemma-4-12b-it-GGUF` exposed 12B IT GGUF quants including `Q4_K_M` and `IQ4_XS`.
- `ggml-org/gemma-4-12B-it-GGUF` exposed `Q4_K_M`, `Q8_0`, and BF16 GGUF routes.
- Google describes Gemma 4 12B as a laptop-ready 12B model with unified multimodal architecture, 16 GB VRAM/unified-memory target, Apache 2.0 license, and MTP drafters.

Qwen:

```text
unsloth/Qwen3.6-35B-A3B-GGUF
unsloth/Qwen3.6-35B-A3B-MTP-GGUF
unsloth/Qwen3.6-27B-GGUF
unsloth/Qwen3.6-27B-MTP-GGUF
unsloth/Qwen3.5-9B-GGUF
```

Notable scan facts:

- `Qwen3.6` is the better "new Qwen" family for current-model framing.
- A clean official-like small `Qwen3.6-9B/12B` route was not found as the main obvious target in this scan; visible 9B/12B hits were mostly community/distill/uncensored variants.
- `Qwen3.5-9B` remains useful only because current Reddit discussion compares it directly to Gemma 4 12B.

Kimi:

```text
unsloth/Kimi-K2.6-GGUF
bartowski/moonshotai_Kimi-K2.6-GGUF
0xSero/Kimi-K2.6-519B-NVFP4
```

Notable scan facts:

- No concrete `Kimi K3` HF/GGUF target was found.
- Kimi K2.6 GGUF routes are too large for a quick single-box internal-disk run.
- Kimi social speed claims should be kept separate from direct `llama-bench` GGUF/RADV claims unless reproduced with matching evidence.

LFM:

```text
LiquidAI/LFM2.5-8B-A1B-GGUF
unsloth/LFM2.5-8B-A1B-GGUF
```

Notable scan facts:

- Practical GGUF sizes are in the same range as small Gemma/Qwen tests.
- The `LiquidAI/LFM2.5-8B-A1B-GGUF` `Q4_K_M` route was tested locally and reached 139.30 t/s generation-only on direct `llama-bench`.
- This is a strong speed/currentness result, but should be framed as an 8B.A1B small-MoE result rather than compared directly against 30B-class Qwen rows.

## Post Framing

Strongest current post hooks:

1. "Google's new Gemma 4 12B runs locally on Strix Halo, but Qwen MoE remains much faster for text generation."
2. "LFM2.5 8B-A1B hits 139 t/s locally on Strix Halo: new small-MoE speed looks very different from large-model capability."
3. "Current-model reality check: newest/local-interest models are not automatically faster than the older Qwen 30B speed headline."
4. "Strix Halo's value is not only 100 t/s; it is being able to test current 5-35GB-class models quickly and keep 100GB+ MoE experiments possible."

Avoid:

- Calling Qwen3.5-9B a newest-model result.
- Treating Kimi K3 as released/benchmarkable without artifacts.
- Turning Gemma 4 12B into a speed headline.
- Mixing MTP/server/social runtime claims with direct `llama-bench` results.

Sources:

- Google Gemma 4 12B announcement: <https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12b/>
- Strix Halo setup discussion: <https://www.reddit.com/r/StrixHalo/comments/1tv41uh/strix_halo_ryzen_ai_max_395_128gb_owners_whats/>
- Gemma 4 12B vs Qwen3.5-9B discussion: <https://www.reddit.com/r/LocalLLaMA/comments/1tw0lua/gemma412bit_vs_qwen359b_on_shared_benchmarks_qwen/>
