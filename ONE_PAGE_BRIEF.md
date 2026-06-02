# Strix Halo Local-AI Guide: Partner Brief

Independent, reproducible setup and benchmark evidence for AMD Strix Halo / Ryzen AI MAX+ 395 local-AI systems.

## Problem

High-end local-AI hardware can be technically strong but commercially under-leveraged if buyers cannot easily reproduce good results. Strix Halo buyers must navigate BIOS settings, OS choice, Vulkan/RADV, ROCm, Ollama, `llama.cpp`, vLLM, model formats, quantization, context settings, power behavior, and benchmark claims before they can trust the purchase.

## Proof Already Available

The repo already includes a technical proof layer:

- Setup and workflow guide: [`README.md`](README.md).
- Current benchmark snapshot: [`BENCHMARKS.md`](BENCHMARKS.md).
- Reproducibility notes: [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).
- Headline claim index: [`data/headline_claims.csv`](data/headline_claims.csv).
- Structured CSV data and raw artifacts: [`data/`](data/README.md), [`data/raw/`](data/raw/).
- Charts: [`charts/`](charts/README.md).
- Community validation: [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md), [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md).
- Backend/server caveats: [`SERVER_SHOOTOUT.md`](SERVER_SHOOTOUT.md), [`BACKEND_CROSSOVER.md`](BACKEND_CROSSOVER.md), [`VLLM_BASELINE.md`](VLLM_BASELINE.md), [`ROCM_VLLM_BUGWATCH.md`](ROCM_VLLM_BUGWATCH.md).

## Commercial Value

This project turns scattered setup knowledge into public evidence and practical buyer confidence. It helps developers and buyers understand what AMD Strix Halo local-AI hardware can do, which setup path to try first, what remains experimental, and where more vendor support would remove friction.

For vendors and developer-relations teams, that means fewer adoption barriers, clearer buyer guidance, more credible reviews, and better signals about software or firmware gaps.

## Collaboration Ask

I can produce independent, reproducible, public technical evidence that reduces adoption friction and helps buyers understand the value and limits of your hardware.

Useful collaboration can include technical contacts, review or loaner systems, early BIOS/firmware/software access, scoped benchmark campaign sponsorship, affiliate relationships, or engineering feedback.

## Example Deliverables

- Reproducible setup guide for a named system.
- Benchmark report with raw logs, CSVs, charts, and caveats.
- Buyer-focused known-good configuration notes.
- Cross-OEM reproduction report.
- Windows versus Linux comparison.
- Power and efficiency report.
- ROCm/vLLM/NPU blocker or progress report.
- Disclosure-compliant public writeup.

## Disclosure And Independence

No paid-positive reviews. No hidden influence. No unsupported marketing claims. Sponsored, loaned, gifted, affiliate, or early-access work must be disclosed clearly. Vendors may correct factual errors, but benchmark conclusions remain independent.

## Contact

For collaboration inquiries, open a GitHub issue or contact the maintainer through the GitHub profile.

Direct email / LinkedIn: TODO before outreach.
