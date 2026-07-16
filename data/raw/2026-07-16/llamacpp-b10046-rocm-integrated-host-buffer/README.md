# llama.cpp b10046 HIP Integrated-Host-Buffer Reproduction

Status: measured local compatibility pass on 2026-07-16.

This run checks the HIP integrated-GPU host-buffer fix merged through
`llama.cpp` PR #24233. The upstream change restores the `integrated` device
property for HIP builds so AMD APUs can use host-backed buffers instead of
being treated like discrete GPUs.

## Pinned Inputs

- system: Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S (`gfx1151`)
- release: official `llama.cpp` b10046, commit `32e789fdf`
- asset: `llama-b10046-bin-ubuntu-rocm-7.2-x64.tar.gz`
- asset SHA256: `79f1575e1ba58a1d1063af1ee7bd7dede2a332ff11552a4211254d5a961a4e97`
- backend: ROCm/HIP
- runtime libraries: existing Ollama ROCm 7.2 bundle at
  `/usr/local/lib/ollama/rocm_v7_2`
- model: local Qwen3-0.6B Q8_0 GGUF, 798,801,920 bytes
- host overrides: no `HSA_OVERRIDE_GFX_VERSION`; no `HSA_ENABLE_SDMA`

The release binary did not find its HIP/rocBLAS dependencies through the
default loader path on this host. Setting only the library path made it work:

```bash
export LD_LIBRARY_PATH=/usr/local/lib/ollama/rocm_v7_2
unset HSA_OVERRIDE_GFX_VERSION HSA_ENABLE_SDMA
```

That is a packaging/setup note for this binary and host, not evidence that the
backend itself failed.

## Compatibility Result

The official binary detected one `gfx1151` ROCm device with 122,880 MiB total
memory and reported 120,124 MiB free. It also printed:

```text
ggml_backend_cuda_get_available_uma_memory: final available_memory_kb: 123007692
```

A CPU-heavy smoke with only one layer offloaded logged actual `ROCm_Host`
allocations:

- 604.14 MiB model buffer
- 0.58 MiB output buffer
- 70.01 MiB compute buffer

This directly reproduces the intended integrated-host-buffer behavior on the
measured Strix Halo system.

## Direct Sentinel

`llama-bench` command shape:

```text
-m Qwen_Qwen3-0.6B-Q8_0.gguf -ngl 999 -mmp 0 -p 512 -n 128 -r 3 -o csv
```

| Test | Mean | Standard deviation |
| --- | ---: | ---: |
| pp512 | 4666.05 t/s | 521.24 |
| tg128 | 208.73 t/s | 0.51 |

The direct number is a small-model runtime sentinel, not a speed headline or a
comparison against Vulkan. The important result is correct full-UMA discovery
and real `ROCm_Host` allocation without a gfx-version override.

## Practical Read

Official b10046 is the first release checked here that includes the merged HIP
integrated-device fix. It is promising compatibility evidence for ROCm/HIP
`llama.cpp` on Strix Halo, but it does not replace Vulkan/RADV as the guide's
beginner path. A practical 27B/35B model and a fully self-contained runtime
package remain useful follow-ups before recommending this as the normal buyer
route.

## Evidence Map

- `list-devices-with-ollama-libs.txt`: device and full-UMA discovery
- `bench.csv` and `bench-stderr.log`: direct small-model sentinel
- `cpu-heavy-rocm-host-smoke.txt`: one-GPU-layer generation smoke
- `cpu-heavy-verbose-stdout.txt`: verbose smoke output
- `cpu-heavy-verbose-stderr.txt`: exact `ROCm_Host` model/output/compute buffers
- `list-devices.txt`: initial missing-library result before setting the loader path

Upstream references:

- <https://github.com/ggml-org/llama.cpp/releases/tag/b10046>
- <https://github.com/ggml-org/llama.cpp/pull/24233>
