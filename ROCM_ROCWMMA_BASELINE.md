# ROCm and rocWMMA Baseline

This file records the current ROCm/rocWMMA readiness state. It is not a benchmark result.

## 2026-05-03 Probe

Status: no publishable local rocWMMA benchmark path yet.

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

- The local machine has ROCm HIP evidence, but not tuned rocWMMA evidence.
- Do not add local rocWMMA benchmark claims until a tuned branch/container is built and logged.
- Any upstream `GGML_HIP_ROCWMMA_FATTN=ON` run without lhl's tuning should be treated as an experiment/failure-mode check, not as a recommendation.

External tuned source:

- lhl's tuned source branch exists at `https://github.com/lhl/llama.cpp/tree/rocm-wmma-tune`.
- Latest observed branch head: `a45e1cd6e9f306a4708cb98912b2bd37e8b70fff`.
- lhl's `strix-halo-testing` repository includes `llama-cpp-fix-wmma/` and `llm-bench/` scripts for rocWMMA compatibility and analysis.

Required next build path:

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
