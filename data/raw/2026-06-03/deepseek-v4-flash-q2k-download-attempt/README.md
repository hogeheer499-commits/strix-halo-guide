# DeepSeek V4 Flash Q2_K Download Attempt

Purpose: test whether DeepSeek V4 Flash is practical to download and smoke-test locally on one Strix Halo / Ryzen AI MAX+ 395 system.

Outcome: download attempt only. No benchmark result was produced.

Host notes:

- Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S.
- normal workstation services were left running.
- This was a real-workstation attempt, not a cold/clean isolated run.
- MiniMax M2.7 local weights were removed after raw evidence was saved.
- One older Qwen3-Coder local model directory was removed to keep enough free space for this attempt.

Target model:

```text
Preyazz/DeepSeek-V4-Flash-GGUF
DeepSeek-V4-Flash-Q2_K.gguf
```

Dry-run size:

```text
DeepSeek-V4-Flash-Q2_K.gguf: 103.3G
```

Attempted commands:

```bash
HF_HUB_DISABLE_XET=1 hf download Preyazz/DeepSeek-V4-Flash-GGUF \
  --include 'DeepSeek-V4-Flash-Q2_K.gguf' \
  --local-dir /home/hoge-heer/benchmark-models/deepseek-v4-flash-q2k \
  --max-workers 1
```

Regular HF download failed because the file is too large for the non-Xet download path.

```bash
hf download Preyazz/DeepSeek-V4-Flash-GGUF \
  --include 'DeepSeek-V4-Flash-Q2_K.gguf' \
  --local-dir /home/hoge-heer/benchmark-models/deepseek-v4-flash-q2k \
  --max-workers 1
```

The Xet path downloaded a partial file to about 53 GiB, then stopped making progress.

```bash
HF_XET_HIGH_PERFORMANCE=1 HF_XET_NUM_CONCURRENT_RANGE_GETS=32 \
hf download Preyazz/DeepSeek-V4-Flash-GGUF \
  --include 'DeepSeek-V4-Flash-Q2_K.gguf' \
  --local-dir /home/hoge-heer/benchmark-models/deepseek-v4-flash-q2k \
  --max-workers 1
```

The high-performance Xet retry did not resume visible progress during the observation window. A later normal Xet retry also remained at the same partial size during the observation window.

Result:

| Item | Status |
| --- | --- |
| Local download | Partial only, about 53 GiB in HF cache. |
| Final GGUF file | Not present. |
| Load test | Not run. |
| `llama-bench` | Not run. |
| Performance claim | None. |

Interpretation:

- DeepSeek V4 Flash remains a high-interest large-model target, but this attempt hit download/distribution friction before any hardware benchmark could happen.
- This should not be listed as a Strix Halo pass or fail. It is a blocked download attempt.
- The partial file was left in place so a future `hf download` can potentially resume instead of starting from zero.
- Adoption read: for 100GB+ single-file GGUF routes, model distribution and resumability are part of the practical buyer friction, not just the hardware runtime.

Source:

- <https://huggingface.co/Preyazz/DeepSeek-V4-Flash-GGUF>
