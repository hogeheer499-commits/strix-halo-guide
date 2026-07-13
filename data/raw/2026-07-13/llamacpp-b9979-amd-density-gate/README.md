# llama.cpp b9979 AMD/RADV MoE Density-Gate Campaign

Date: 2026-07-13

System: Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S, 128 GB unified memory.

This directory preserves the first-party evidence behind [`MOE_CONCURRENCY.md`](../../../../MOE_CONCURRENCY.md). It compares official b9979 stock behavior, an opt-in AMD/RADV density gate, density plus an independently selectable dense MMV threshold of 16, and the existing Lemonade ROCm b1259 comparator.

## Source And Patch

- upstream release: `llama.cpp` b9979
- source commit: `4114ba18b208c2e9c1689a8316d410e649309dbc`
- patch: [`amd-radv-density-gate.patch`](amd-radv-density-gate.patch)
- default behavior remains stock
- `GGML_VK_DENSITY_GATE=1` enables `n_tokens * n_experts_used <= 2 * n_expert`, capped at 64 tokens
- `GGML_VK_MMV_MAX_COLS=16` separately selects dense16

The opt-in environment variable is deliberate. External issue data shows that applying this density policy to NVIDIA Vulkan can regress throughput.

## Models

- `Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf`: 128 experts, top-8
- `Qwen3-Next-80B-A3B-Instruct-UD-Q4_K_XL.gguf`: 512 experts, top-10

Exact SHA-256 hashes are in [`host-snapshot.txt`](host-snapshot.txt).

## Command Shape

```bash
llama-batched-bench \
  -m MODEL.gguf \
  -c 65536 -ngl 999 -fa on \
  -ctk q4_0 -ctv q4_0 --no-mmap \
  -npp 512 -ntg 128 \
  -npl 1,2,4,8,9,12,16,24,32,48,64 \
  --output-format jsonl
```

The long discovery sweep was split into thermally isolated blocks after an initial density attempt reached the 95 C safety threshold. Both aborted attempts remain in [`discovery/`](discovery/) as negative evidence. Controlled repeats started below 50 C and used explicit high GPU DPM only during measurement.

Exact wrappers:

- [`run-density-bench.sh`](run-density-bench.sh)
- [`run-density-campaign-root.sh`](run-density-campaign-root.sh)

## Correctness

The [`correctness/`](correctness/) directory contains:

- stock, density, and density+dense16 `MUL_MAT_ID`: 790/790 tests passed per mode
- stock and density+dense16 ordinary `MUL_MAT`: 956/956 tests passed per mode
- fixed-prompt, temperature-zero model-level outputs for all three modes

The generated sentence is text-identical across modes. Complete file hashes differ because current `llama-cli` writes timing lines into stdout.

## Data Map

- [`discovery/`](discovery/): concurrency 1-64 route sweeps and the preserved thermal aborts
- [`repeats30/`](repeats30/): five stock/density/dense16 repeats and three Lemonade ROCm repeats at concurrency 8/9/12/16
- [`repeats80/`](repeats80/): three repeats per route at concurrency 8/9/12/16
- every successful run has stdout, stderr, one-second telemetry, and a summary CSV
- [`../../../moe_density_gate.csv`](../../../moe_density_gate.csv): parsed detail rows
- [`../../../moe_density_gate_summary.csv`](../../../moe_density_gate_summary.csv): repeat-aware means and standard deviations

## Telemetry Caveat

`power1_average` is labeled PPT by the `amdgpu` hwmon interface. It is APU/GPU package telemetry, not measured wall power. Temperature is GPU edge temperature from the same sysfs interface.

