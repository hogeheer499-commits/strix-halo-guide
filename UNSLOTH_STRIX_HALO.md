# Fine-Tune And Export A Local Model On Strix Halo

This is the measured Unsloth/ROCm path for training a small model on an AMD Ryzen AI MAX+ 395 / Radeon 8060S, exporting it to GGUF, and loading that GGUF locally with ROCm `llama.cpp`.

If you only want private chat, use the [README setup script](README.md#setup-script). Use this page when you specifically want to fine-tune or adapt a model.

## What This Route Proves

On the guide's retail 128GB Beelink GTR9 Pro, the pinned route completed:

```text
ROCm GPU detection
  -> one Unsloth SFT training step
  -> saved-checkpoint inference
  -> Q4_K_M GGUF export
  -> ROCm llama.cpp inference
  -> container restart
  -> inference from the host-persisted GGUF
```

The checkpoint returned `STRIX HALO TRAINING PASS`. The exported GGUF returned `STRIX HALO GGUF PASS`, and the copied artifact returned `STRIX HALO RESTART PASS` after the container was restarted.

This is a **functional end-to-end qualification** with a Qwen3 0.6B smoke model. It does not prove large-model training speed, useful fine-tuning quality, long-run stability, or a 249 t/s headline. See the [raw evidence](data/raw/2026-07-21/unsloth-rocm72-train-export-smoke/) for exact scope and versions.

## Before You Start

You need:

- a Strix Halo system with Linux and a recent kernel;
- `/dev/kfd` and `/dev/dri` available;
- Podman plus Distrobox;
- about 25GB for the container image, plus model, dataset, checkpoint, and export storage;
- the normal [Strix Halo memory setup](README.md#quick-start-6-steps).

This guide uses a community container derived from the AMD/Unsloth route. Review its [source and credits](https://github.com/Justin-Noel/amd-strix-halo-unsloth-toolboxes) before using it on a production machine. The image below is pinned to the exact digest qualified here.

## 1. Create The Pinned Container

```bash
distrobox create -n unsloth-rocm-7.2-guide \
  --image ghcr.io/justin-noel/amd-strix-halo-unsloth-toolboxes@sha256:8285eac06bf33398ad2605387e98d77eba30379cf690af755e238967ef238c3d \
  --additional-flags "--device /dev/dri --device /dev/kfd --group-add video --group-add render --security-opt seccomp=unconfined"

distrobox enter unsloth-rocm-7.2-guide
```

The pinned image is large: about 22.7GB uncompressed in this qualification.

## 2. Run The GPU Gate First

Inside the container:

```bash
/opt/unsloth/studio/unsloth_studio/bin/python -c \
  "import torch; print(torch.__version__, torch.version.hip); print(torch.cuda.get_device_name(0)); print(torch.tensor([1.0], device='cuda'))"
```

The qualified route printed:

```text
2.13.0+rocm7.2 7.2.53211
AMD Radeon 8060S
tensor([1.], device='cuda:0')
```

Stop here if the version is CPU-only, the Radeon device is missing, or the tensor command fails. Do not start a long training job until this gate passes.

## 3. Optional: Start The Web UI

Inside the container:

```bash
start-unsloth-studio
```

Open <http://localhost:8888>. The initial password is stored inside the container at:

```text
/opt/unsloth/studio/auth/.bootstrap_password
```

Check the health endpoint:

```bash
curl -s http://127.0.0.1:8888/api/health
```

`"chat_only": false` means the GPU training path loaded. The measured smoke used the CLI below so the exact operation could be preserved.

## 4. Run A Small Training Smoke

This deliberately performs only one SFT step. It verifies the path without pretending to produce a useful trained model.

```bash
/opt/unsloth/studio/unsloth_studio/bin/unsloth train \
  --model unsloth/Qwen3-0.6B-unsloth-bnb-4bit \
  --dataset yahma/alpaca-cleaned \
  --format-type alpaca \
  --training-type sft \
  --max-seq-length 256 \
  --load-in-4bit \
  --output-dir guide-qwen3-06b-smoke \
  --max-steps 1 \
  --batch-size 1 \
  --gradient-accumulation-steps 1 \
  --save-steps 1 \
  --lora-r 8 \
  --lora-alpha 16 \
  --no-enable-wandb
```

Important: keep `--output-dir` relative. Studio rejected an absolute path outside its managed output root. The result should appear under:

```text
/opt/unsloth/studio/outputs/guide-qwen3-06b-smoke
```

The measured one-step run completed at `global_step=1` with loss `2.6169`. That number is a workflow diagnostic, not a quality comparison.

## 5. Export The Result To GGUF

Run export from the writable Studio output directory:

```bash
cd /opt/unsloth/studio/outputs

/opt/unsloth/studio/unsloth_studio/bin/unsloth export \
  /opt/unsloth/studio/outputs/guide-qwen3-06b-smoke \
  /opt/unsloth/studio/outputs/guide-qwen3-06b-smoke-gguf \
  --format gguf \
  --quantization q4_k_m \
  --max-seq-length 256
```

Why the `cd` matters: the exporter writes a temporary BF16 GGUF in its current working directory. The first attempt failed with `PermissionError` from a non-writable directory. This workaround produced a 396,705,728-byte `Q4_K_M` GGUF.

## 6. Load The GGUF On The Radeon iGPU

```bash
/opt/unsloth/studio/llama.cpp/build/bin/llama-cli \
  --model /opt/unsloth/studio/outputs/guide-qwen3-06b-smoke-gguf/guide-qwen3-06b-smoke.Q4_K_M.gguf \
  --gpu-layers 999 --ctx-size 256 --no-mmap \
  --temp 0 --predict 64 \
  --prompt 'Reply with exactly: STRIX HALO GGUF PASS' \
  --no-display-prompt --single-turn --simple-io --reasoning off
```

Use `--single-turn --simple-io` for an automated smoke. Without those flags, `llama-cli` remains interactive and can keep generating prompt loops.

## 7. Preserve Your Work Outside The Container

Studio outputs live inside the container. Copy them into your mounted home directory before refreshing or deleting it:

```bash
mkdir -p "$HOME/unsloth-guide-artifacts-2026-07-21"

cp -a /opt/unsloth/studio/outputs/guide-qwen3-06b-smoke \
  "$HOME/unsloth-guide-artifacts-2026-07-21/"

cp -a /opt/unsloth/studio/outputs/guide-qwen3-06b-smoke-gguf \
  "$HOME/unsloth-guide-artifacts-2026-07-21/"
```

The measured host copies have these SHA-256 hashes:

```text
e2c6471fedf92223e6bd28ac296e720f1ab91cecb531bc91c7cfe03b52daff98  model.safetensors
f6cdf85982ce229982120d3ae5b93653fb16fa45d3205fbcbf3ce64cc0983612  guide-qwen3-06b-smoke.Q4_K_M.gguf
```

After a container restart, the copied GGUF loaded again and returned `STRIX HALO RESTART PASS`.

## Known Limits And Safety Notes

- This route uses an isolated community container. It is not an AMD endorsement of this repository.
- The official AMD article documents the broader Unsloth direction; this page records one independent retail-box reproduction.
- The one-step 0.6B run validates plumbing, not useful adaptation quality.
- Larger models need their own memory, training-time, thermal, checkpoint, and quality campaign.
- Container refresh removes Studio-side outputs. Copy valuable artifacts to the host first.
- The upstream container warns that running `unsloth studio update` without a visible GPU can replace the ROCm `llama.cpp` build with a CPU build.
- Do not add `HSA_OVERRIDE_GFX_VERSION` to this native `gfx1151` route.
- Review model, dataset, and container licenses before commercial use.

## Why This Matters

Inference-only numbers answer “how fast can this box run a model?” This workflow answers a second buyer and developer question: “can I adapt a model, export a portable artifact, and run it locally on the same machine?”

That is useful for private domain assistants, local prototypes, model experimentation, AMD developer workflows, and vendor/reviewer validation. The next valuable test is a real small dataset with held-out quality checks, not simply more steps on this smoke model.

## Evidence And Sources

- [Raw first-party evidence](data/raw/2026-07-21/unsloth-rocm72-train-export-smoke/)
- [Machine-readable best-known profiles](data/best_known_profiles.csv)
- [AMD's official Unsloth/Strix Halo article](https://www.amd.com/en/developer/resources/technical-articles/2026/train-and-run-models-on-amd-gpus-with-unsloth.html)
- [Qualified community container source](https://github.com/Justin-Noel/amd-strix-halo-unsloth-toolboxes)
- [Unsloth AMD installation documentation](https://unsloth.ai/docs/get-started/install/amd)
