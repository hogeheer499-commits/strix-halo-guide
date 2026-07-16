# ROCm 7.14 Ryzen AI hipBLASLt A/B

Status: measured locally on 2026-07-16.

This isolated campaign checks the ROCm 7.14 release-note workaround for lower
than expected FP16 vLLM throughput on Ryzen AI MAX / MAX+ at batch 8 and above.
It did not alter the host ROCm stack or the existing `vllm-gfx1151`
Distrobox.

## Pinned Inputs

- system: Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S (`gfx1151`)
- image: `rocm/vllm:rocm7.14.0_rdna_ubuntu24.04_py3.14_pytorch_2.11.0_vllm_0.23.0`
- manifest digest: `sha256:5b0389109bb2db9346d3f0f971c4c99eba7e5e72cfa57e9a2a9b4ac67477771d`
- container PyTorch: `2.11.0+rocm7.14.0`
- container HIP: `7.14.60850`
- container vLLM: `0.23.1.dev1+g9ddef7117.d20260715`
- model: existing local `Qwen/Qwen3-0.6B` safetensors snapshot
- dtype: FP16
- generated tokens per request: 256
- repeats: 3 per condition
- comparison: `TORCH_BLAS_PREFER_HIPBLASLT=0` versus `1`
- concurrency: 1, 4, 8, 9, and 16

The generic official `rdna` image initialized successfully on this `gfx1151`
system. That is a compatibility result for this pinned image, not proof that
every generic ROCm image supports every Strix Halo configuration.

## Results

| Concurrency | hipBLASLt off | hipBLASLt on | Difference |
| ---: | ---: | ---: | ---: |
| 1 | 143.38 t/s | 143.53 t/s | +0.10% |
| 4 | 471.97 t/s | 468.34 t/s | -0.77% |
| 8 | 480.98 t/s | 675.79 t/s | +40.50% |
| 9 | 540.67 t/s | 751.33 t/s | +38.96% |
| 16 | 896.83 t/s | 1269.40 t/s | +41.54% |

All 30 measured benchmark invocations completed without request errors. At
concurrency 16, mean inter-token latency fell from 17.67 ms to 12.45 ms with
hipBLASLt enabled. The result matches the scope of AMD's release note: no
material single-request gain, but a large recovery at batch/concurrency 8 and
above in this FP16 vLLM workload.

## Interpretation

Use `TORCH_BLAS_PREFER_HIPBLASLT=1` for this pinned ROCm 7.14 / PyTorch 2.11
FP16 vLLM server shape when serving eight or more concurrent requests. Do not
generalize it to Vulkan, GGUF, direct `llama-bench`, quantized models, or all
ROCm workloads. At concurrency 4 it was slightly slower, so operators should
still A/B their actual model and request shape.

The telemetry files cover each complete mode rather than matched per-
concurrency windows. They preserve edge temperature, amdgpu PPT, SCLK, and GPU
busy data, but they are not sufficient for a wall-power efficiency claim.

## Evidence Map

- `summary.csv` and `summary.json`: processed A/B means and latency fields
- `hipblaslt-*/np*-summary.csv`: per-repeat benchmark summaries
- `hipblaslt-*/np*-detail.csv`: per-request data
- `hipblaslt-*/np*-stdout.jsonl`: benchmark stdout records
- `hipblaslt-*/server.log`: vLLM server logs
- `hipblaslt-*/telemetry.csv`: host amdgpu telemetry
- `hipblaslt-*/container-versions.json`: exact runtime versions
- `image-inspect.json`: pinned image metadata
- `model-sha256.txt`: local model-file hashes
- `run-context.txt`: host and run context
- `run-isolated-ab.sh`: exact isolated runner

