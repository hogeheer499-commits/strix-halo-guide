# AMD Strix Halo System Evidence Matrix

This matrix summarizes the public system-level evidence represented in the
Strix Halo Guide. It is designed for buyers, reviewers, contributors, and OEM
engineering teams that need to see what has actually been measured, what kind
of evidence exists, and what still needs independent validation.

The count is **12 owner systems or independent sources**, not 12 unique product
models and not 12 directly comparable benchmark systems. First-party Beelink
measurements remain separate from community reports. Direct `llama-bench`,
server/API, MTP/speculative, capacity, power, thermal, RPC, NPU, and failure
evidence are not blended into one score.

Machine-readable summary: [`data/system_evidence_matrix.csv`](data/system_evidence_matrix.csv)

## Coverage Matrix

| Evidence source | Count | Evidence class | OS / route represented | Public coverage | Main evidence | Most useful next validation |
|---|---:|---|---|---|---|---|
| Beelink GTR9 Pro, primary guide system | 1 | First-party retail system | Ubuntu 24.04; Vulkan/RADV; Ollama; direct and server `llama.cpp`; ROCm controls | Setup, direct/API/server benchmarks, capacity, power, concurrency, failures, restart/reboot checks | [`README.md`](README.md), [`data/raw/`](data/raw/), [`data/headline_claims.csv`](data/headline_claims.csv) | A second current Beelink firmware/configuration tested with the same buyer-path and sustained-load protocol |
| Corsair AI Workstation 300 fleet | 3 | Community-reported owner systems | Fedora; Vulkan/RADV and ROCm; USB4 RPC | Cross-box variance, direct benchmarks, wall power, RPC, USB4, 310B-class prompt capacity, thermal/SCLK and fan-reset evidence | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`THERMAL_STABILITY.md`](THERMAL_STABILITY.md), [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md) | Vendor-confirmed BIOS, EC/fan-control, and current-firmware guidance followed by the same bounded thermal protocol |
| GMKtec EVO-X2, native contributor system | 1 | Community-reported owner system | Native Ubuntu; Vulkan/RADV; 96GB | Qwen3.6 and Qwen3-Coder portability, exact MTP reproduction, setup metadata | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`native evidence`](data/raw/2026-05-14/community-gmktec-native-issue16/) | Current firmware and a matched buyer-path rerun against the primary Beelink setup |
| GMKtec EVO-X2, tuned external report | 1 | Independently sourced community report | Vulkan/RADV; tuned thermal and power policy | Qwen3-Coder speed-shape evidence with explicit cooling and policy qualifiers | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`provenance note`](data/raw/2026-06-02/community-reddit-look-qwen-coder/) | Raw repeated-run bundle and an untuned stock control on the same unit |
| Minisforum MS-S1-Max | 1 | Community-reported owner system | Windows 11; LM Studio | Windows serving path, long-context configuration, hardware telemetry | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`raw report`](data/raw/2026-06-02/community-windows-lmstudio-issue3/) | Current driver/firmware repeat plus a matched short-context and sustained-load buyer-path run |
| Nimo AI Mini PC | 1 | Community-reported owner system | Ubuntu; Vulkan/RADV and ROCm/Lemonade | Large-model serving, MTP, StepFun/Qwen routes, Gemma QAT, thermal context | [`COMMUNITY_NIMO.md`](COMMUNITY_NIMO.md), [`structured rows`](data/community_nimo_issue4.csv) | Current software-stack repeat with exact model hashes and a normalized buyer workload |
| Beelink GTR9 Pro, second owner stack | 1 | Community-reported owner system | CachyOS; ROCm/ZenDNN and Vulkan controls | Cross-backend prompt/decode evidence, long-prompt result, NPU/IOMMU context, negative VMM/rocWMMA routes | [`BACKEND_CROSSOVER.md`](BACKEND_CROSSOVER.md), [`raw report`](data/raw/2026-06-12/community-devoidfury-cachyos-rocm-zendnn/) | Same-model current-build A/B with normalized commands and full correctness metadata |
| Beelink GTR9 Pro, third independent unit (Reddit) | 1 | Community-reported owner system | Ubuntu 24.04; Vulkan/RADV | First independent reproduction of the first-party Qwen3.6 ~62-63 t/s figure (62.65 tg128); `-ub > -b` silent-clamp finding (+28.9% pp512 corrected); measured stock-Mesa-to-kisak 26.1.7 uplift (+16.9% pp512) | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`raw note`](data/raw/2026-08-21/community-reddit-ornery-ub-clamp/) | Build number, kernel, BIOS UMA, and raw llama-bench output via a benchmark-report issue |
| GMKtec EVO-X2, ciru-ai artifact | 1 | External public evidence package | NixOS; IOMMU on; NPU sidecar; ROCmFP4 | Sanitized benchmark exports, tuned low-bit routes, quality rows, NPU contention evidence | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`compact metrics`](data/community_ciru_evox2_metrics.csv), [source artifact](https://github.com/ciru-ai/strix-halo-evo-x2-evidence) | Reproduction of selected profiles on a second OEM plus stable packaged runner/model manifests |
| Minix Elite ER939 Ai | 1 | Community-reported owner system | Ubuntu; Ollama | Beginner-path Ollama report on another retail chassis | [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), [`raw report`](data/raw/2026-06-24/community-minix-er939-ollama-issue27/) | Exact Vulkan ICD, model digest, command/script, warm/cold repeats, and current firmware metadata |

## What This Matrix Can And Cannot Answer

It can answer:

- whether a setup or behavior has transferred beyond the primary Beelink;
- which operating systems, runtimes, and advanced paths have public evidence;
- where same-SKU variance, power, thermals, RPC, or NPU behavior has been measured;
- which vendor or community input would remove the next buyer uncertainty.

It cannot answer:

- which OEM is universally fastest or best;
- whether unlike backends, quants, prompts, and contexts are directly comparable;
- whether a community report is equivalent to a controlled first-party run;
- whether untested firmware or hardware revisions behave the same way.

For individual rows and caveats, use [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md).
For the shortest measured recommendations, use
[`BEST_KNOWN_PROFILES.md`](BEST_KNOWN_PROFILES.md). For exact public headline
provenance, use [`data/headline_claims.csv`](data/headline_claims.csv).

## Contribute A Missing Validation

The most useful contribution is not necessarily a record speed. A stock-system
reproduction, BIOS or firmware correction, failed route, power/thermal trace,
or exact model/runtime manifest can remove more buyer uncertainty than a tuned
headline. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the requested metadata.
