---
name: Qwen3.8 Route Report
about: Reproduce or challenge a Qwen3.8 27B Strix Halo speed, context, vision, or MTP route
title: "[Qwen3.8] "
labels: benchmark
assignees: ''
---

Read the [Qwen3.8 route decision](https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/QWEN38_STRIX_HALO.md) first. Values from
different artifacts, runtimes, contexts, or speculative-decoding routes are not
directly comparable.

## Claim Being Tested

- **Source claim / link:**
- **What are you testing?** speed / context / image / tools / thinking / stability / other
- **Guide route being compared, if any:**

## System And Runtime

- **Device and memory:**
- **OS / kernel:**
- **Mesa / Vulkan driver or ROCm version:**
- **Runtime and exact version/commit:**
- **Backend:** Vulkan/RADV / ROCm/HIP / ROCmFP4 / DFlash / Ollama / other
- **BIOS UMA / IOMMU / power profile:**
- **Background workload:**

## Exact Artifacts

- **Main model repo, filename, quant, and hash:**
- **Projector filename and hash, if used:**
- **MTP/draft/sidecar repo, filename, quant, and hash, if used:**
- **Patch or fork commit, if used:**
- **License or redistribution constraint noticed:**

## Request Shape

- **Prompt/source text or reproducible generator:**
- **Evaluated prompt tokens:**
- **Requested/generated tokens:**
- **Context size:**
- **Batch / ubatch:**
- **Sampling / seed:**
- **Parallel slots or concurrency:**
- **Warmup and repeats:**

## Exact Command Or Request

```bash
paste the exact command or API request here
```

## Results And Output Check

- **Prompt processing:**
- **Generation/decode:**
- **Acceptance rate, if speculative:**
- **TTFT / elapsed time, if server/API:**
- **Did the output pass an exact or stated correctness check?**
- **Any crash, DeviceLost, fallback, truncation, or degraded output?**

```text
paste raw output or link logs/CSV here
```

## Interpretation

What does this reproduce, contradict, or leave unresolved? Slower and failed
routes are valuable. Do not describe one tuned route as universal Strix Halo
performance.
