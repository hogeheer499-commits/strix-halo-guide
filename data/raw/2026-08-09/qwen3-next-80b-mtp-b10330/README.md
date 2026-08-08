# Qwen3-Next 80B-A3B MTP backend qualification on llama.cpp b10330

This evidence package compares direct generation with the new Qwen3-Next
MTP-only sidecar on one Beelink GTR9 Pro / Ryzen AI MAX+ 395. The same main
model, sidecar, prompts, seeds, context size, and output length were used for
the Vulkan and HIP controls.

This is a real-world qualification run, not a strict-clean headline run. Zoom,
the `ubuntu-zoom` VM, DocRemote/ffmpeg, and RustDesk remained active and are
recorded in `host-snapshot-before.txt`.

## Exact artifacts

- llama.cpp: b10330, commit `687e7789271ec1276e3470f158428e11a4f80b6f`
- Main model: `Qwen3-Next-80B-A3B-Instruct-UD-Q4_K_XL.gguf`
- MTP sidecar: `Qwen3-Next-80B-A3B-Instruct-MTP-ONLY-Q4_K_M.gguf`
- Main and sidecar hashes: `model-sha256.txt`
- Vulkan build: official b10330 source, Vulkan/RADV
- HIP build: official b10330 source, ROCm 7.14 gfx1151 package
- HIP unified-memory environment override: unset

## Result

| Backend / policy | Short decode | 3k-prompt decode | Draft acceptance | Result |
|---|---:|---:|---:|---|
| Vulkan direct | 61.33 t/s | 59.16 t/s | n/a | coherent baseline |
| Vulkan MTP, n=2 / p=0.60 | 7.81 t/s | 7.99 t/s | 100% | correct but much slower |
| Vulkan MTP, n=4 / p=0.00 | 12.37 t/s | 12.58 t/s | 95.8-99.0% | correct but 78.7-79.8% slower than direct |
| HIP direct | 51.34 t/s | 50.21 t/s | n/a | coherent baseline |
| HIP MTP, n=4 / p=0.00 | 83.52 t/s | 83.60 t/s | 97.4-99.0% | 62.7-66.5% faster than direct |

All 18 Vulkan responses and all 12 HIP responses produced the same output hash
for a given deterministic prompt. The MTP routes therefore preserved the
observed output while changing throughput.

## Interpretation

- MTP support alone is not evidence of a speedup. On this exact b10330 Vulkan
  route the sidecar is a severe regression despite high acceptance.
- The official gfx1151 HIP route turns the same MTP sidecar into a useful
  acceleration path and is the better measured backend for Qwen3-Next MTP here.
- The HIP result is a strong practical scout, but it is not promoted as a
  strict-clean headline until it is repeated under controlled background
  conditions.
- Do not add `GGML_CUDA_ENABLE_UNIFIED_MEMORY=1` to this profile. Separate
  b10330 evidence in the adjacent ROCm qualification package found reproducible
  corrupt output on this real Qwen model with that override enabled.

## Reproduce

Run `run-repro.py` for the Vulkan matrix. Run `run-hip-control.py` with the
ROCm 7.14 libraries on `LD_LIBRARY_PATH` for the HIP control. Exact generated
server commands, requests, responses, logs, rows, and summaries are stored in
this directory.
