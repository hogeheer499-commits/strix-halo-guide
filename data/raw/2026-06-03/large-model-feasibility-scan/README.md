# Large Model Feasibility Scan

Purpose: triage the highest-value viral/adoption targets before downloading very large model artifacts.

Host/storage context at scan time:

- Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S.
- About 98 GB free after the three Qwen direct scout downloads.
- T3 and Hermes must remain running.

## Findings

| Target | Status | Local-test read |
| --- | --- | --- |
| Kimi K2.6 | High viral value, currently storage/runtime blocked on this internal disk. | Public GGUF routes are hundreds of GB. `0xSero/Kimi-K2.6-519B-NVFP4` is about 309.6 GB of safetensors, which may explain the 110+ t/s social claim but is not a direct GGUF/RADV `llama-bench` route. |
| MiniMax M2.7 | Tested after cleanup. | `UD-IQ4_XS` downloaded and ran locally via direct `llama-bench`; see `../minimax-m27-ud-iq4xs-local-smoke/`. This is a large-model feasibility/adoption proof, not a speed-record route. |
| MiniMax M3 | Newly relevant watch target, but no local artifact found yet. | Official MiniMax blog positions M3 as open-weight with 1M context/native multimodality; the GitHub repo currently says "MiniMax M3 is Coming." No GGUF/weights were found via Hugging Face search during this scan. |
| DeepSeek V4 Flash | Download-blocked in this attempt. | `Preyazz/DeepSeek-V4-Flash-GGUF` has `Q2_K` at about 103.3 GB. The Xet download reached about 53 GiB partial, then stopped making visible progress during retries; see `../deepseek-v4-flash-q2k-download-attempt/`. No load or benchmark result exists. |
| GLM-5.1 | Interesting but currently storage-blocked for useful quants. | Unsloth GGUF starts around 205.5 GB; Bartowski starts around 158.2 GB. Not suitable before major cleanup/external storage. |

## Source Checks

- Kimi K2.6 public GGUF size scan: `unsloth/Kimi-K2.6-GGUF`, `bartowski/moonshotai_Kimi-K2.6-GGUF`.
- Kimi social-adjacent NVFP4 route: `0xSero/Kimi-K2.6-519B-NVFP4`, about 309.6 GB.
- MiniMax M2.7 GGUF size scan: `unsloth/MiniMax-M2.7-GGUF`, `bartowski/MiniMaxAI_MiniMax-M2.7-GGUF`.
- MiniMax M3 official page: <https://www.minimax.io/blog/minimax-m3>.
- MiniMax M3 GitHub page: <https://github.com/MiniMax-AI/MiniMax-M3>.
- DeepSeek V4 Flash GGUF size scan: `Preyazz/DeepSeek-V4-Flash-GGUF`, `nsparks/DeepSeek-V4-Flash-FP4-FP8-GGUF`.
- GLM-5.1 GGUF size scan: `unsloth/GLM-5.1-GGUF`, `bartowski/zai-org_GLM-5.1-GGUF`.

## Next Action

Before large-model downloads, remove or relocate no-longer-needed local model weights. Raw benchmark evidence is already stored separately in this repository and should remain.

Most relevant next practical tests:

1. Resume DeepSeek V4 Flash `Q2_K` from the partial HF cache, or retry from a faster/more stable network path.
2. Test another MiniMax M2.7 quant only if there is a quality/speed reason; `UD_IQ4_XS` already proves the large-model local route.
3. Kimi K2.6 NVFP4/GGUF only after a storage plan; treat any 110+ t/s result as a separate serving/runtime claim unless reproduced with comparable direct logs.
4. MiniMax M3 as soon as local weights or GGUF quants become available.
