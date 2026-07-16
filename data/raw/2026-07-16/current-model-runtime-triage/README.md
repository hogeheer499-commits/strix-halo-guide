# Current Model And Runtime Triage

Date: 2026-07-16

This is the campaign-time triage snapshot. Later on the same day, official
`llama.cpp` b10046 was released and its HIP integrated-host-buffer fix was
reproduced separately. Use [`CURRENT_MODELS.md`](../../../../CURRENT_MODELS.md)
and [`data/current_test_queue.csv`](../../../current_test_queue.csv) for the
current release map and next-test priorities.

This note preserves the runtime decisions behind the July 16 test queue. A
blocked row is not a hardware failure: it means the available artifact needs a
different runtime, more storage, or a non-default software stack before a fair
Strix Halo benchmark is possible.

## Runtime Releases

- `llama.cpp` b10034, commit `505b1ed15ca80e2a19f12ff4ac365e40fb374053`,
  is the measured Vulkan/RADV release in this update.
- b10037, commit `56d6e9dde2c684cebbc11e1f705da4286cb535f2`, was
  published while the campaign was running. Its three commits after b10034
  touch CUDA, OpenCL, and quantization tooling, not the measured Vulkan runtime
  path. They do not justify rerunning the unchanged Vulkan sentinel.
- Ollama 0.32.0 is measured in the controlled 0.31.1/0.31.2/0.32.0 comparison.
- ROCm 7.14.0 is the latest observed official ROCm release. It includes a
  Ryzen AI MAX / MAX+ inference note for some FP16 vLLM workloads at batch 8+
  and recommends `TORCH_BLAS_PREFER_HIPBLASLT=1` with PyTorch earlier than
  2.14. This becomes an isolated container A/B target; the campaign does not
  replace the working host graphics stack merely for version parity.

## Model Runtime Decisions

### Nemotron Labs Puzzle 75B-A9B

Status: blocked on mainline runtime support; no model download attempted.

The community GGUF repository explicitly requires still-open `llama.cpp` PR
[#25444](https://github.com/ggml-org/llama.cpp/pull/25444) and was converted
with a pinned PR build. On this date the PR was open at head commit
`b566325c837881cf01895b05d66aeb249b17131c`. Official b10034 does not contain
the `nemotron_h_puzzle` model architecture. Downloading a 37-48 GiB quant for
the stock runtime would therefore be predictable waste rather than a fair
loadability test.

### DeepSeek V4 Flash

Status: one stock-runtime route is now viable; the smaller REAP route remains
runtime-specific.

General DeepSeek V4 support merged through `llama.cpp` PR
[#24162](https://github.com/ggml-org/llama.cpp/pull/24162) on 2026-06-29
(merge commit `8c146a8366304c871efc26057cc90370ccf58dad`). The current
`unsloth/DeepSeek-V4-Flash-GGUF` `UD-IQ2_XXS` artifact is the practical
stock-runtime candidate for one 128 GB system. A pinned dry-run at revision
`e3aa0d6a5fa4f820d9e132ac1fd1d01e1b2b49e0` reports three shards totaling
90.9 GB. The earlier `antirez` repository is no longer available and must not
remain in the test queue. The approximately 46.98 GiB REAP artifact is
not interchangeable: it uses the separate `ds4-compact-v1` / reaped runtime
path and should stay out of stock `llama.cpp` recommendations.

### Nemotron Labs Audex 30B-A3B

Status: text-only GGUF is testable; complete audio remains a separate
HF/vLLM-sidecar workflow.

The community release provides ordinary text-only GGUFs for `llama.cpp` and
separate full-vocabulary audio GGUFs. The audio encoder, vocoder, speech
decoder, enhancement VAE, and NVIDIA inference scripts live in an additional
approximately 7.67 GB sidecar. The release explicitly states that `llama.cpp`
does not package the complete Audex audio pipeline as one all-in-one GGUF
runtime. A text benchmark must not be presented as proof of local audio QA,
audio generation, or speech-to-speech support on AMD.

License note: Audex uses the NVIDIA OneWay Noncommercial license. It is useful
as technical support evidence, but it is not an uncomplicated commercial
vendor-workflow recommendation.

### Kimi K2.7 Code And Other Frontier-Size Routes

Status: external-storage / multi-system lane.

Kimi K2.7 Code remains a roughly 595 GB NVFP4-class artifact for an
approximately 1T-total / 32B-active model. GLM-5.2, MiniMax-M3, Hy3, and
Nemotron Ultra candidates also exceed the useful internal-disk budget or need
specialized serving stacks. These remain important ecosystem watch targets,
but "downloadable" is not the same as a practical one-box 128 GB route.

### Other July 15-16 NVIDIA Releases

Status: scanned; no first-party Strix Halo benchmark scheduled.

- `nvidia/Lyra-2.0` is a WAN-14B-based single-image-to-3D research pipeline
  documented for H100/GB200-class NVIDIA systems, not a local LLM route.
- `nvidia/Nemotron-3-Embed-1B-NVFP4` is a useful retrieval model, but the
  released NVFP4 checkpoint is explicitly documented for vLLM on NVIDIA
  hardware. The BF16 model is the portable Transformers route.
- `nvidia/Gemma-4-31B-IT-NVFP4` is an NVIDIA ModelOpt/vLLM checkpoint. The
  guide already has direct and matched-head Gemma 4 GGUF evidence that is more
  actionable for the current Vulkan/RADV buyer path.

These releases may become relevant when AMD-capable GGUF or ROCm artifacts
exist. Downloading the vendor-specific checkpoints now would not answer a new
buyer question.

## Buyer And Vendor Read

This triage removes two recurring sources of adoption friction:

1. buyers can distinguish a model that does not fit from a model that merely
   lacks current runtime support;
2. vendors and runtime developers get a concrete next dependency instead of a
   vague "it failed on AMD" report.

Only locally measured routes are promoted into the benchmark CSVs and
best-known profiles. Blocked routes remain visible in the test queue so they
can be retested when their prerequisite changes.
