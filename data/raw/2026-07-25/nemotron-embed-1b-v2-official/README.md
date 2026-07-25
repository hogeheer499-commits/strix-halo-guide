# NVIDIA Llama Nemotron Embed 1B v2 Local Retrieval Check

First-party Beelink GTR9 Pro result from 2026-07-25.

## Result

The official `nvidia/llama-nemotron-embed-1b-v2` Sentence Transformers route
loaded and ran locally on the CPU without CUDA or an NVIDIA GPU.

For the query:

```text
Which BIOS setting lets Linux access unified memory on Strix Halo?
```

the model produced these cosine similarities:

- relevant Strix Halo UMA/GTT passage: `0.410610586`
- unrelated weather passage: `0.030947512`
- positive-minus-negative margin: `0.379663080`

The output dimension was 2048. A fresh offline process produced the exact
same metrics and vector SHA-256:
`029923917cf3c4e94151555919869a2db9f94e02274f2c738b03e04eb7427e79`.

On the cached repeat:

- model load: 0.611462 seconds
- query plus two documents encoded: 0.091301 seconds
- total process wall time: 3.71 seconds
- maximum resident memory: 2,728,268 KiB

This is a small semantic-retrieval functionality and determinism check. It is
not a BEIR, MIRACL, MLQA, or long-document retrieval benchmark.

## Exact Route

- Model: `nvidia/llama-nemotron-embed-1b-v2`
- Hugging Face revision:
  `113abe4acafa848e77ead9c0623205e511932348`
- Model file: `model.safetensors` (2,471,644,736 bytes)
- Model SHA-256:
  `45f8440682a89ac577cc8d53b1bb345804772adb7b34e0573562e2fca4e62b0d`
- Runtime device: CPU
- Python: 3.12.3
- PyTorch: 2.13.0+cpu
- Transformers: 5.14.1
- Sentence Transformers: 5.6.1
- CPU threads: 16

The two small model-provided Python files were inspected before enabling
`trust_remote_code=True`. They import PyTorch and Transformers model
components and do not contain network, shell, subprocess, `eval`, or `exec`
calls.

## Reproduce

The exact deterministic test is in `run_embedding_check.py`.

```bash
python3 -m venv /path/to/nemotron-embed-venv
/path/to/nemotron-embed-venv/bin/pip install \
  torch --index-url https://download.pytorch.org/whl/cpu
/path/to/nemotron-embed-venv/bin/pip install sentence-transformers

HF_HUB_OFFLINE=1 \
  /path/to/nemotron-embed-venv/bin/python run_embedding_check.py
```

Omit `HF_HUB_OFFLINE=1` for the first run so the pinned model revision can be
downloaded.

## Files

- `run_embedding_check.py`: exact test implementation.
- `first-run.log`: first model download/load and result.
- `restart-run.log`: cached fresh-process offline repeat.
