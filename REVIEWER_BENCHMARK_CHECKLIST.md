# Reviewer Benchmark Checklist For Strix Halo Local LLM Testing


## Purpose

This checklist helps reviewers, bloggers, and YouTubers produce comparable Strix Halo local LLM results instead of one-off screenshots.

## Minimum Metadata

- exact device
- Ryzen AI MAX SKU
- memory size
- BIOS UMA setting
- IOMMU setting
- OS and kernel
- Mesa/RADV, AMDVLK, or ROCm version
- tool and build commit
- model name, source, quant, filename, and hash if available
- command
- raw output
- power profile
- thermals/cooling if relevant

## Keep Workloads Separate

Do not mix:

- direct `llama-bench`
- Ollama API generation
- `llama-server`
- MTP/speculative decoding
- server concurrency
- long-context filled-KV decode
- ROCm/HIP versus Vulkan/RADV comparisons
- community rows

## Suggested First Commands

Start with a direct `llama-bench` row because it is easiest to compare.

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
llama-bench \
  -m /path/to/model.gguf \
  -fa 1 -ngl 999 -mmp 0 -p 0 -n 128 -r 20 -o csv
```

Then add an API/server row only if the request shape is fully described.

## Good Review Framing

```text
This result is one Strix Halo system, one backend, one model file, one quant, and one command. It should be compared only against matching rows.
```

## Link Targets

- `README.md`
- `REPRODUCIBILITY.md`
- `data/headline_claims.csv`
- `COMMUNITY_RESULTS.md`
- benchmark issue template
- power issue template
