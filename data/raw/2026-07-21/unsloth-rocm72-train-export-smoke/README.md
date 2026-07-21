# Unsloth ROCm 7.2 Train -> Export -> Restart Smoke

Status: `measured-local` functional workflow qualification, not a training-performance or model-quality benchmark.

This run qualifies a complete small-model workflow on the guide's retail Beelink GTR9 Pro:

1. detect the Radeon 8060S through ROCm/PyTorch;
2. run one supervised fine-tuning step with Unsloth;
3. load the saved checkpoint and return an exact test string;
4. export the trained model to `Q4_K_M` GGUF;
5. load that GGUF with the bundled ROCm `llama.cpp`;
6. copy the artifacts outside the container, restart the container, and load the copied GGUF again.

The route passed all six stages. It is useful setup and compatibility evidence. The tiny Qwen3 0.6B smoke model, one training step, and practical background-load host state do **not** support a broad speed, quality, stability, or large-model fine-tuning claim.

## Pinned Environment

- Date: 2026-07-21
- System: Beelink GTR9 Pro, Ryzen AI MAX+ 395, Radeon 8060S, 128GB unified memory
- Host kernel: `6.19.4-061904-generic`
- Community container source commit: `3e82176d034e7d8357db457747d47144db9ff843`
- Image: `ghcr.io/justin-noel/amd-strix-halo-unsloth-toolboxes:rocm-7.2`
- Image digest: `sha256:8285eac06bf33398ad2605387e98d77eba30379cf690af755e238967ef238c3d`
- Image ID: `7d47153be1cac24305fe9d6b8390889918875ffb4ab9faa277cc77bc28f947c8`
- Image uncompressed size: `22674809043` bytes
- Model: `unsloth/Qwen3-0.6B-unsloth-bnb-4bit`
- Dataset: `yahma/alpaca-cleaned`
- Training: one SFT step, sequence length 256, batch 1, LoRA rank 8
- Export: `Q4_K_M` GGUF
- Bundled `llama.cpp`: b10043, commit `cbedbd493`

The run used the normal workstation state. T3, FFmpeg/DocRemote, Zoom, RustDesk, and an idle vLLM container remained present. This is appropriate for a functional workflow qualification, but not for a strict-clean performance headline.

## Results

- PyTorch: `2.13.0+rocm7.2`
- HIP runtime reported by PyTorch: `7.2.53211`
- GPU visible: `AMD Radeon 8060S`
- GPU tensor smoke: `4.0`
- Unsloth: `2026.7.3`
- Training: `global_step=1`, loss `2.6169`, 87 input tokens, runtime `2.3397` seconds
- Checkpoint inference: exact output `STRIX HALO TRAINING PASS`
- GGUF size: `396705728` bytes
- GGUF inference: exact output `STRIX HALO GGUF PASS`
- Restart/persisted-artifact inference: exact output `STRIX HALO RESTART PASS`
- Functional CLI timing before restart: about 1198 prompt t/s and 249.8 generation t/s
- Functional CLI timing after restart: about 1224.9 prompt t/s and 248.9 generation t/s

The timing rows are retained only as smoke diagnostics. They are not in `data/headline_claims.csv` and should not be compared with the guide's 30B-class rows.

## Friction Found

Two failures produced useful buyer guidance:

1. An absolute output path outside Studio's managed output root was rejected. Use a relative `--output-dir` so the run lands under `/opt/unsloth/studio/outputs`.
2. GGUF export first failed with `PermissionError` because the exporter writes a temporary BF16 GGUF in the current working directory. Run export from writable `/opt/unsloth/studio/outputs`.

Studio outputs live inside the container. Copy trained models and exports into the host home directory before refreshing or deleting the container.

## Evidence Files

- [`commands.txt`](commands.txt): exact qualification commands
- [`host.txt`](host.txt): host and background-state scope
- [`versions.txt`](versions.txt): pinned software and image identifiers
- [`trainer_state.json`](trainer_state.json): saved Trainer state from the one-step run
- [`artifact-hashes.txt`](artifact-hashes.txt): SHA-256 hashes for the merged checkpoint and GGUF
- [`results.txt`](results.txt): concise pass/fail and output record

The large checkpoint and GGUF are not committed to Git. They remain in the maintainer's host artifact directory.

## Sources

- [AMD: Train and Run Models on AMD GPUs with Unsloth](https://www.amd.com/en/developer/resources/technical-articles/2026/train-and-run-models-on-amd-gpus-with-unsloth.html)
- [Justin-Noel AMD Strix Halo Unsloth Toolboxes](https://github.com/Justin-Noel/amd-strix-halo-unsloth-toolboxes)
- [Unsloth AMD installation documentation](https://unsloth.ai/docs/get-started/install/amd)
