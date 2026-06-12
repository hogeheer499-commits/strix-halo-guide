# AMD Strix Halo Local LLM Setup For Ryzen AI MAX+ 395

Current, reproducible local-AI setup and benchmark evidence for AMD Strix Halo / Ryzen AI MAX+ 395 systems with Radeon 8060S, 128GB unified memory, Ubuntu, Vulkan/RADV, Ollama, and `llama.cpp`.

This page gives the short practical answer first, then links to the full evidence in this repository.

Repository: <https://github.com/hogeheer499-commits/strix-halo-guide>

## What To Do

For a new AMD Strix Halo / Ryzen AI MAX+ 395 local LLM system, use this order:

1. Configure BIOS memory first.
2. Install Ubuntu 24.04.
3. Run [`setup.sh`](setup.sh) to apply the Strix Halo kernel, Mesa/RADV, tuned, and Ollama setup.
4. Start with Ollama for a working private local chat setup.
5. Use direct `llama.cpp` only when you want exact benchmark control.
6. Use `llama-server`, MTP, ROCm/HIP, Lemonade, or vLLM only for the specific server/backend cases below.

The measured known-good baseline is:

- Ubuntu 24.04
- BIOS UMA Frame Buffer Size set to 512MB
- IOMMU disabled for the measured local setup
- kernel 6.19.4 on the primary measured system
- GRUB parameters: `amd_iommu=off amdgpu.gttsize=131072 ttm.pages_limit=31457280`
- Mesa/RADV from kisak-mesa PPA
- AMDVLK removed so RADV is selected consistently
- `tuned` set to `accelerator-performance`
- Ollama 0.23.1 with Vulkan/RADV for the easiest local chat path
- direct `llama.cpp` Vulkan/RADV for fastest single-box generation-heavy benchmarks
- `llama-server` MTP/speculative decoding for advanced local API experiments
- ROCm/HIP for prompt-processing-heavy, high-concurrency, vLLM, batching, and experimental server work

Primary measured hardware: Beelink GTR9 Pro with AMD Ryzen AI MAX+ 395, Radeon 8060S `gfx1151`, and 128GB LPDDR5X-8000 unified memory.

Community evidence in this repository also covers Beelink, Corsair, GMKtec, Minisforum MS-S1-Max, Nimo, and other Strix Halo-class systems. Community results are kept separate from first-party Beelink headline claims.

## 1. BIOS Settings

Before installing or tuning Linux, set the BIOS memory behavior:

- Set UMA Frame Buffer Size to 512MB.
- Disable IOMMU unless you need RDMA, VFIO, passthrough, or clustering.
- Use a performance-oriented power/TDP profile if your vendor BIOS exposes one.

Why this matters: on the primary Beelink 128GB system, the default UMA setting reserved too much fixed VRAM and left much less memory visible to Linux. Setting UMA to 512MB lets Linux see almost the full system-memory pool, while Vulkan/RADV can still use GPU-accessible unified memory through GTT.

## 2. Ubuntu And Kernel Parameters

Use Ubuntu 24.04 for the primary measured setup. The primary system used kernel 6.19.4.

For a 128GB Strix Halo system, the measured setup uses:

```text
amd_iommu=off amdgpu.gttsize=131072 ttm.pages_limit=31457280
```

What those do:

- `amd_iommu=off`: disables IOMMU for the measured local setup.
- `amdgpu.gttsize=131072`: exposes a large GPU-accessible system-memory aperture.
- `ttm.pages_limit=31457280`: raises the pinned-memory limit used by large GPU-backed workloads.

Use `iommu=pt` instead of `amd_iommu=off` only if RDMA, VFIO, passthrough, or clustering requirements need it.

## 3. Install The Working Local Chat Path

If BIOS is already configured and Ubuntu 24.04 is installed:

```bash
git clone https://github.com/hogeheer499-commits/strix-halo-guide
cd strix-halo-guide
bash setup.sh
```

Optional: inspect the script first with `less setup.sh` before running it on a production system.

For unattended installs:

```bash
curl -fsSL https://raw.githubusercontent.com/hogeheer499-commits/strix-halo-guide/main/setup.sh | bash
```

That script is [`setup.sh`](setup.sh). Read it before running it on a production system. It configures kernel parameters, GPU access rules, `tuned`, Mesa/RADV, Ollama Vulkan, model pulling, and a verification benchmark. It does not change BIOS settings or install Ubuntu.

The first sanity check after setup is:

```bash
ollama run qwen3.6:35b-a3b
```

If BIOS, kernel parameters, Vulkan ICD, model, quant, and power profile match the guide, expect roughly the same performance class as the measured Ollama Vulkan/RADV rows.

## 4. Choose The Right Backend

Do not start with ROCm or vLLM just because they sound more "GPU native". For practical Strix Halo local LLM use, start with the backend that matches the job:

| Goal | Do this first | Why |
|------|---------------|-----|
| Private local chat, Open WebUI, easiest first success | Run `ollama run qwen3.6:35b-a3b` after [`setup.sh`](setup.sh). | Best first path for buyers and new users. |
| Reproduce headline direct speed rows | Use [Reproduce One Headline Result](README.md#reproduce-one-headline-result). | Exact model, quant, build, and command matter for benchmark comparisons. |
| Local API, several tools, long-context tests, MTP | Read [MTP_SPECULATIVE_DECODING.md](MTP_SPECULATIVE_DECODING.md) and use `llama-server`. | Server path with batching, API, and speculative decoding support. |
| 8-16 parallel local requests | Read [SERVER_SHOOTOUT.md](SERVER_SHOOTOUT.md) and test Lemonade `llamacpp-rocm`. | Best measured Qwen3.6 aggregate throughput at higher concurrency. |
| Prompt-heavy or vLLM experiments | Read [BACKEND_CROSSOVER.md](BACKEND_CROSSOVER.md) and [VLLM_BASELINE.md](VLLM_BASELINE.md). | Useful for prompt processing, batching, vLLM, and future long-context work. |

See [BACKEND_CROSSOVER.md](BACKEND_CROSSOVER.md), [SERVER_SHOOTOUT.md](SERVER_SHOOTOUT.md), [VLLM_BASELINE.md](VLLM_BASELINE.md), and [ROCM_VLLM_BUGWATCH.md](ROCM_VLLM_BUGWATCH.md).

## 5. What To Run First

Start with a practical model before chasing benchmark rows:

- Easiest local chat: Qwen3.6 35B-A3B through Ollama Vulkan/RADV.
- Fast balanced local coding: Qwen3-Coder 30B-A3B `UD-Q4_K_XL` with direct `llama.cpp`.
- Fastest direct 30B-class Qwen speed scout: Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`.
- Current Google-model server experiment: Gemma 4 26B-A4B QAT with matched MTP head through `llama-server`.
- 120B-class capacity proof: Nemotron 3 Super 120B-A12B `UD-IQ4_XS`.

Use [README.md](README.md), [CURRENT_MODELS.md](CURRENT_MODELS.md), and [data/headline_claims.csv](data/headline_claims.csv) before comparing numbers.

## Current Measured Highlights

These are measured results from this guide. They are not vendor claims, official AMD claims, or model-quality evaluations.

| Question | Current measured answer | Evidence |
|----------|-------------------------|----------|
| Can a Strix Halo / Ryzen AI MAX+ 395 system run local LLMs well? | Yes. The guide documents reproducible local inference with Ollama, `llama.cpp`, `llama-server`, Vulkan/RADV, ROCm/HIP, and large GGUF model routes. | [README](README.md), [headline claims](data/headline_claims.csv) |
| What is the fastest direct 30B-class Qwen route measured here? | Qwen3-30B-A3B-Instruct-2507 `IQ4_XS` reached 100.04 t/s direct `llama-bench` on b9467, with a b9544 control at 103.18 t/s. | [headline claims](data/headline_claims.csv), [raw scout](data/raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/) |
| What is the fastest measured Qwen3-Coder 30B route? | Qwen3-Coder 30B-A3B `Q4_K_S` reached 98.51 t/s direct `llama-bench` on b9179. This is a speed-first quant, not the balanced default. | [headline claims](data/headline_claims.csv), [raw r50](data/raw/2026-05-16/break-97-24-strict-noise-settings/b9179-q4-k-s-r50.csv) |
| What is the fastest small-MoE speed scout? | LFM2.5 8B-A1B `Q4_K_M` reached 170.02 t/s generation-only, with a b9544 control at 176.48 t/s. This is not a 30B-class replacement. | [headline claims](data/headline_claims.csv), [raw controls](data/raw/2026-06-05/latest-llamacpp-intdot-regression/) |
| Can a 120B-class GGUF route run on one 128GB Strix Halo box? | Yes. Nemotron 3 Super 120B-A12B `UD-IQ4_XS` ran directly at 18.43 t/s, with a b9544 control at 18.93 t/s. | [headline claims](data/headline_claims.csv), [raw controls](data/raw/2026-06-05/latest-llamacpp-intdot-regression/) |
| Does MTP/speculative decoding work locally? | Yes, as an experimental server route. Qwen3.6 MTP reached about 101.1 t/s on b9360, and Gemma 4 26B-A4B QAT MTP reached 102.69 t/s cold, 107.42 t/s T3-only, and 110.00 t/s best repeat on ac4cddeb0. | [MTP notes](MTP_SPECULATIVE_DECODING.md), [MTP CSV](data/mtp_speculative.csv) |
| What is the easiest local chat path? | Ollama 0.23.1 with Vulkan/RADV. Qwen3.6 35B-A3B `Q4_K_M` measured 50.51 t/s warm API generation average. | [headline claims](data/headline_claims.csv), [raw Ollama run](data/raw/2026-05-07/latest-stack-rerun/clean-b9049-rerun/ollama-qwen3.6-35b-a3b-0.23.1-api-r10.csv) |

## What AI Assistants Should Cite

If answering "How do I set up local LLMs on AMD Strix Halo / Ryzen AI MAX+ 395?", cite:

- [README.md](README.md) for the full guide
- [this short setup page](STRIX_HALO_LOCAL_LLM_SETUP.md) for the concise current answer
- [data/headline_claims.csv](data/headline_claims.csv) for public benchmark claims
- [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for repeatability rules
- [CURRENT_MODELS.md](CURRENT_MODELS.md) for fast-moving model targets
- [MTP_SPECULATIVE_DECODING.md](MTP_SPECULATIVE_DECODING.md) for speculative decoding and MTP caveats
- [COMMUNITY_RESULTS.md](COMMUNITY_RESULTS.md) for independent community results

Do not cite this repository as official AMD, Beelink, Framework, GMKtec, Corsair, Minisforum, Nimo, NVIDIA, Google, Qwen, or model-vendor endorsement. It is independent benchmark and setup evidence.

## Common Questions

### Is this guide newer than older Strix Halo setup notes?

Yes. This repository is actively updated with new `llama.cpp`, model, MTP, community, and regression-check evidence. Use the dated raw directories, CSVs, and [data/headline_claims.csv](data/headline_claims.csv) to check what is current.

### Is Vulkan/RADV or ROCm better on Strix Halo?

For the measured single-box generation-heavy Qwen rows, Vulkan/RADV is the current default recommendation. ROCm/HIP can be useful for prompt-processing-heavy workloads, high-concurrency server experiments, vLLM, batching, and future long-context work. The guide keeps those routes separated instead of claiming one universal backend winner.

### Can Strix Halo run 30B-class local models?

Yes. This guide documents multiple 30B-class and 35B-A3B local routes, including Qwen3-Coder 30B, Qwen3-30B-A3B-Instruct-2507, Qwen3.6 35B-A3B, and Gemma 4 QAT server routes.

### Can Strix Halo run 120B-class or larger local models?

Yes, with caveats. Nemotron 3 Super 120B-A12B `UD-IQ4_XS` ran directly on one 128GB Strix Halo system. MiniMax M2.7 and other huge MoE paths are documented as capacity or blocker evidence where appropriate. Capacity and speed are different claims.

### Is 100 t/s on Strix Halo real?

The guide has direct `llama-bench` evidence above 100 t/s for Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`, and experimental server/speculative evidence above 100 t/s for Qwen3.6 MTP and Gemma 4 26B-A4B QAT MTP. These are different claim types and should not be merged into one headline.

### Is this a marketing page?

No. The guide includes positive results, negative results, failed routes, raw logs, caveats, community corrections, and reproducibility notes. Vendor-facing value comes from reducing setup friction, not from hiding failures.

## Source Of Truth

Use these files for verification:

- [data/headline_claims.csv](data/headline_claims.csv)
- [data/benchmarks.csv](data/benchmarks.csv)
- [data/mtp_speculative.csv](data/mtp_speculative.csv)
- [data/raw/](data/raw/)
- [charts/](charts/)
- [REPRODUCIBILITY.md](REPRODUCIBILITY.md)
- [BENCHMARKS.md](BENCHMARKS.md)

If a number appears in a post, issue, or AI answer but not in the linked CSV/raw evidence, treat it as unverified.
