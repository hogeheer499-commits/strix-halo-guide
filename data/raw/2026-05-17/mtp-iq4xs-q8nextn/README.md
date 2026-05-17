# Qwen3.6 MTP IQ4_XS-Q8nextn Sweep

Date: 2026-05-17.

Purpose: test whether the `localweights` Qwen3.6 35B MTP quant with Q8 next-token heads improves the practical `llama-server` MTP route on Strix Halo, and whether it can honestly produce a broad 100 t/s result.

## Host And Build

- System: Beelink GTR9 Pro
- CPU/GPU: AMD Ryzen AI MAX+ 395 / Radeon 8060S
- Kernel: 6.19.4-061904-generic
- Backend: Vulkan/RADV
- Tool: `llama-server`
- llama.cpp: b9187 / `0253fb21f595246f54c192fe8332f34173be251b`

## Model

- Source: `localweights/Qwen3.6-35B-A3B-MTP-IQ4_XS-Q8nextn-GGUF`
- File: `Qwen3.6-35B-A3B-MTP-IQ4_XS-Q8nextn.gguf`
- Size: 19,393,459,552 bytes
- SHA256: `4d2349305663bc59bacab26d8eba8ed1218de84b8d1f0456208037e13efa9a98`

## Prompt Harness

Six practical prompts were sent to `/completion` with:

- `n_predict: 192` unless the filename starts with `long512` or `synthetic512`
- `temperature: 0`
- `top_k: 1`
- `cache_prompt: false`
- `stream: false`

The harness records `timings.predicted_per_second` from `llama-server`. Each run also has a sysfs telemetry CSV with GPU edge temperature, CPU Tctl, amdgpu PPT, GPU busy, and selected clocks.

## Main Results

| Run | Mean t/s | Min t/s | Max t/s | Read |
|-----|---------:|--------:|--------:|------|
| Baseline, no MTP | 72.436 | 72.118 | 72.616 | Similar to the local Q4_K_M MTP baseline. |
| MTP `draft-n=2`, `-t 16`, `--poll 50` repeat 3 | 90.804 | 83.227 | 100.373 | Best broad six-prompt average in this sweep. |
| MTP `draft-n=3`, `-t 16`, `--poll 10` | 90.271 | 73.809 | 110.612 | Fastest single prompt, but less stable. |
| Long natural generation, `n_predict=512`, best run | 89.399 | 72.564 | 109.494 | Longer generation did not raise the broad average. |
| Synthetic no-EOS 512-token run, best run | 87.676 | 67.978 | 106.962 | Synthetic no-EOS did not help. |

## Thermal / Power Read

The best broad run (`mtp-draft2-t16-p50-repeat3`) stayed cool:

- GPU edge average/max: 59.789 C / 65.000 C
- CPU Tctl average/max: 65.957 C / 70.500 C
- amdgpu PPT average/max: 100.812 W / 119.092 W

This does not look thermal-throttled. Cooling is probably not the missing 10% for a broad 100 t/s MTP average.

## Conclusion

This quant is better than the local Q4_K_M requant for MTP server work. It raises the best six-prompt average from about 87.5 t/s to about 90.8 t/s and raises the best prompt from 100.74 t/s to 110.61 t/s.

It still does not justify the broad claim "Qwen3.6 runs 100 t/s on Strix Halo." The honest claim is: Qwen3.6 MTP can exceed 100 t/s on favorable server prompts, while the best measured six-prompt average on this Beelink is about 90.8 t/s.
