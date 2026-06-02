# Performance Notes

This file keeps narrow performance conclusions that are useful for repeat testing, but too detailed for the first README screen.

## Direct 98.51 t/s Reproduction Status

The current direct `llama-bench` speed-first headline remains Qwen3-Coder 30B-A3B `Q4_K_S` at **98.51 t/s** on llama.cpp b9179, Vulkan/RADV, measured on 2026-05-16.

That result came from a strict host state:

- Mesa/RADV 26.0.6 from the then-current kisak Mesa stack.
- llama.cpp b9179 `b81c2cdd7`.
- Qwen3-Coder 30B-A3B `Q4_K_S`.
- `-fa 1`, `-mmp 0`, `-b 2048`, `-ub 512`, `-t 16`, `--poll 50`, `-ngl 999`.
- `tuned accelerator-performance` active and `power-profiles-daemon` inactive.
- CPU governors and EPP set to `performance`.
- GPU fixed high with 2900 MHz selected.
- RustDesk, Firefox, Zoom VM, and ffmpeg paused; T3 kept running and guarded.

Raw evidence:

- [`data/raw/2026-05-16/break-97-24-strict-noise-settings/b9179-q4-k-s-r50.csv`](data/raw/2026-05-16/break-97-24-strict-noise-settings/b9179-q4-k-s-r50.csv)
- [`data/raw/2026-05-16/break-97-24-strict-noise-settings/host-state-r50.txt`](data/raw/2026-05-16/break-97-24-strict-noise-settings/host-state-r50.txt)

## 2026-06-01 Reproduction Attempts

A 2026-06-01 rerun first landed around 92-93 t/s because it accidentally used `flash_attn=0`. That is not comparable to the original headline, which used `flash_attn=1`.

After correcting to `flash_attn=1`, the same b9179 Qwen3-Coder `Q4_K_S` path on the current Mesa/RADV 26.1.1 stack measured about **95.1 t/s** with the original flags. The latest `de6f727aa` build measured about **95.6 t/s** on the same path. These were local control runs and did not replace the public headline.

An isolated source-built Mesa 26.0.6 RADV test was also run without system downgrades. `vulkaninfo` confirmed `Mesa 26.0.6 (git-0e095aab43)`, but the best controlled r20 rerun was **96.84 t/s**, not 98.51 t/s.

Interpretation:

- Mesa/RADV version and exact driver stack matter.
- Source-built Mesa 26.0.6 is not identical to the old kisak Mesa 26.0.6 binary stack.
- The 98.51 t/s row remains valid as recorded evidence, but it should be treated as a strict-stack speed-first result, not a casual “always reproduce this” number.
- Do not change the headline unless a newer repeated run beats 98.51 t/s with raw CSV, host state, model hash, and exact command.

## Qwen3.6 27B MTP Q8_0 Status

The official Qwen3.6 27B MTP `Q8_0` GGUF is useful evidence because it answers a natural question: “Should I use the dense 27B route instead of the 35B-A3B MoE route on Strix Halo?”

Current answer: not for speed.

Measured server results:

- llama.cpp b9235, Mesa/RADV 26.0.6: **7.74 t/s** without MTP, **14.59 t/s** best MTP average.
- llama.cpp `de6f727aa`, Mesa/RADV 26.1.1: **7.61 t/s** without MTP, **14.69 t/s** with `draft-n=3`.
- llama.cpp `1fd5f4803` / b9467, Mesa/RADV 26.1.1: **7.70 t/s** direct `llama-bench` tg128 follow-up.

Raw evidence:

- [`data/raw/2026-05-19/qwen36-27b-mtp-q8-llamacpp-9235/`](data/raw/2026-05-19/qwen36-27b-mtp-q8-llamacpp-9235/)
- [`data/raw/2026-06-01/qwen36-27b-mtp-latest-de6f727/`](data/raw/2026-06-01/qwen36-27b-mtp-latest-de6f727/)
- [`data/raw/2026-06-02/reddit-look-int-dot-reproduction/`](data/raw/2026-06-02/reddit-look-int-dot-reproduction/)

Interpretation:

- MTP nearly doubles the dense 27B Q8 route, but the route remains much slower than the 35B-A3B MoE paths.
- For a practical Strix Halo local-AI setup, Qwen3.6 35B-A3B GGUFs remain the better Qwen3.6 speed path in this guide.
- Keep the 27B result as a negative/control row, not as a headline.

## Vulkan Integer-Dot And 100 t/s Reproduction Status

A Reddit follow-up reported about 99.84-100.00 t/s on Qwen3-Coder 30B-A3B `Q4_K_S` using llama.cpp `1fd5f4803` / b9467 and simple command shapes:

```bash
llama-bench -fa 1 -n 128 -m Qwen3-Coder-30B-A3B-Instruct-Q4_K_S.gguf
llama-bench -fa 1 -n 128 -p 0 -m Qwen3-Coder-30B-A3B-Instruct-Q4_K_S.gguf
```

Local Beelink reproduction on the same source commit:

- default command: **1392.09 t/s pp512**, **96.38 t/s tg128**
- ten `-p 0` runs: **96.72 t/s best**, **96.51 t/s average**, **95.99 t/s minimum**
- local Vulkan device line: `int dot: 0`

The Reddit-reported GMKtec output showed `int dot: 1`. That matters because llama.cpp's Vulkan backend has integer-dot shader paths for quantized matmul. If the device and shader compiler expose that path, decode can be faster on Q4-style workloads.

The confusing part is that this Beelink's `vulkaninfo` reports `VK_KHR_shader_integer_dot_product` and `shaderIntegerDotProduct = true`, but the host Ubuntu `glslc` package used during CMake reports `GL_EXT_integer_dot_product not supported by glslc`. In practice, the hardware/driver capability is visible, but the current host shader-compiler path does not let this llama.cpp build enable the integer-dot shaders.

Interpretation:

- The Reddit result is plausible and valuable, but this guide has not reproduced it on the Beelink yet.
- The next clean route is not another random benchmark sweep; it is an isolated shader-toolchain test that enables `GL_EXT_integer_dot_product` without polluting the host.
- Do not change the Beelink direct headline unless a repeated local run beats 98.51 t/s with raw output, host state, model hash, exact command, and `int dot: 1`/toolchain metadata.

Raw evidence:

- [`data/raw/2026-06-02/reddit-look-int-dot-reproduction/`](data/raw/2026-06-02/reddit-look-int-dot-reproduction/)
