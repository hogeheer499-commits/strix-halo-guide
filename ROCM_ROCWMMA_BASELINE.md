# ROCm and rocWMMA Baseline

This file records the current ROCm/rocWMMA readiness state. It is not a benchmark result.

> **Historical status (2026-08-30 review):** this page preserves the old probe
> and community evidence below. [`llama.cpp` PR #26046](https://github.com/ggml-org/llama.cpp/pull/26046),
> merged 2026-07-24, removed rocWMMA FlashAttention and made
> `GGML_HIP_ROCWMMA_FATTN` obsolete. Do not use the old build recipe as current
> guidance; current HIP builds use the newer MMA kernel.

## 2026-05-03 Probe

Historical result: no publishable local rocWMMA benchmark path was produced
before upstream removed the path in 2026.

Local host state:

- Full host ROCm SDK is not installed in `/opt/rocm`; `hipcc` is not available on the host.
- Ollama ships ROCm runtime libraries under `/usr/local/lib/ollama/rocm`, which is enough for existing HIP binary spot checks but not a clean build environment.
- The currently usable local HIP `llama-bench` path remains `/home/hoge-heer/llama-cpp-latest/build-hip/bin/llama-bench` with `LD_LIBRARY_PATH=/usr/local/lib/ollama/rocm`.

Existing local llama.cpp HIP builds:

| Path | Commit / state | ROCm/rocWMMA state |
|------|----------------|--------------------|
| `/home/hoge-heer/llama-cpp-latest/build-hip` | llama.cpp `d05fe1d7d` source tree; HIP binary used for May spot check | `GGML_HIP=ON`, `GGML_HIP_ROCWMMA_FATTN=OFF`, unroll flag present |
| `/home/hoge-heer/llama.cpp/build` | local fork branch `fix/hip-uma-detection` | `GGML_HIP=ON`, `GGML_HIP_ROCWMMA_FATTN=OFF` |
| `/home/hoge-heer/llama.cpp/build-opt` | local fork branch `fix/hip-uma-detection` | `GGML_HIP=ON`, `GGML_HIP_ROCWMMA_FATTN=OFF`, unroll flag present |
| `/home/hoge-heer/Desktop/llama-evidence-worktrees/master/build-rocm-evidence` | llama.cpp `a95a11e5b` evidence worktree | `GGML_HIP=ON`, `GGML_HIP_ROCWMMA_FATTN=OFF` |
| `/home/hoge-heer/Desktop/llama-evidence-worktrees/pr-20472/build-rocm-evidence` | llama.cpp `97ae46e46` evidence worktree | `GGML_HIP=ON`, `GGML_HIP_ROCWMMA_FATTN=OFF` |

Conclusion:

- The local machine has ROCm HIP evidence but did not produce a publishable tuned rocWMMA result before upstream removed that path.
- Do not turn the historical rocWMMA material into a current benchmark or build recommendation.
- Current upstream builds must omit the removed `GGML_HIP_ROCWMMA_FATTN` option.

Historical external tuned source:

- lhl's tuned source branch exists at `https://github.com/lhl/llama.cpp/tree/rocm-wmma-tune`.
- Latest observed branch head: `a45e1cd6e9f306a4708cb98912b2bd37e8b70fff`.
- lhl's `strix-halo-testing` repository includes `llama-cpp-fix-wmma/` and `llm-bench/` scripts for rocWMMA compatibility and analysis.

Historical build recipe (do not use with current upstream):

1. Create a separate container/toolbox for llama.cpp ROCm work. Do not build in the host Python/vLLM environment.
2. Clone `lhl/llama.cpp` at `rocm-wmma-tune` or apply the documented lhl fix scripts to a known llama.cpp commit.
3. Build with:

```bash
cmake -B build-rocwmma-tuned -S . \
  -DGGML_HIP=ON \
  -DAMDGPU_TARGETS=gfx1151 \
  -DGGML_HIP_ROCWMMA_FATTN=ON \
  -DGGML_HIP_MMQ_MFMA=ON \
  -DCMAKE_BUILD_TYPE=Release
cmake --build build-rocwmma-tuned -j$(nproc)
```

4. Record ROCm version, rocWMMA headers/library source, llama.cpp commit, compiler flags, `LD_LIBRARY_PATH`, `HSA_OVERRIDE_GFX_VERSION`, `HSA_ENABLE_SDMA`, `ROCBLAS_USE_HIPBLASLT`, and whether `TensileLibrary_lazy_gfx1151.dat` warnings appear.
5. Run a minimal sanity benchmark before long-context claims:

```bash
./build-rocwmma-tuned/bin/llama-bench \
  -m /path/to/model.gguf \
  -fa 1 -ngl 999 -mmp 0 \
  -p 512 -n 128
```

6. Only after sanity passes, compare long-context against the current Vulkan RADV filled-KV data at 32K/64K/128K.

## 2026-06-12 Community CachyOS / ROCm 7.2.4 Note

devoidfury reported a Beelink GTR9 Pro CachyOS stack with ROCm 7.2.4-1, local ZenDNN, and llama.cpp commit `1593d5684d077c07fc788e9527ec1bd52287de7f` plus small local MMQ/ZenDNN build tweaks.

The useful positive signal is backend crossover: on Qwen3.6 27B MTP `UD-Q6_K_XL`, ROCm + ZenDNN measured 303.20 pp5000 versus 155.89 pp5000 on Vulkan + ZenDNN, while decode stayed around 8 t/s on both backends.

The useful negative signal for this file:

- VMM: built, but crashed when loading any model.
- `GGML_HIP_ROCWMMA_FATTN`: still reported as a performance hit, with prompt-processing degrading faster than without it.

This remains historical negative evidence. Current ROCm/HIP is still useful to test for prompt-heavy rows, but the removed `GGML_HIP_ROCWMMA_FATTN` option is no longer an experiment or recommendation for current upstream builds.
