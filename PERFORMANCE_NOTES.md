# Performance Notes

This file keeps narrow performance conclusions that are useful for repeat testing, but too detailed for the first README screen.

## Qwen3-Coder Direct 98.51 t/s Reproduction Status

The current Qwen3-Coder direct `llama-bench` speed-first headline remains Qwen3-Coder 30B-A3B `Q4_K_S` at **98.51 t/s** on llama.cpp b9179, Vulkan/RADV, measured on 2026-05-16.

That result came from a strict host state:

- Mesa/RADV 26.0.6 from the then-current kisak Mesa stack.
- llama.cpp b9179 `b81c2cdd7`.
- Qwen3-Coder 30B-A3B `Q4_K_S`.
- `-fa 1`, `-mmp 0`, `-b 2048`, `-ub 512`, `-t 16`, `--poll 50`, `-ngl 999`.
- `tuned accelerator-performance` active and `power-profiles-daemon` inactive.
- CPU governors and EPP set to `performance`.
- GPU fixed high with 2900 MHz selected.
- Nonessential GUI, remote-access, video, and media noise was paused where safe; workspace-critical services were preserved.

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

## Qwen3-30B-A3B-Instruct-2507 Direct 100 t/s Status

A 2026-06-02 scout found a separate local direct `llama-bench` route above 100 t/s:

- Model: Qwen3-30B-A3B-Instruct-2507.
- Quant: `IQ4_XS-3.63bpw`.
- Build: llama.cpp `1fd5f4803` / b9467.
- Backend: Vulkan/RADV, Mesa 26.1.1.
- Result: **100.04 t/s** tg128 and **1416.03 t/s** pp512 on the r50 confirmation.
- Shorter confirmation: **100.58 t/s** tg128 on r20.
- Generation-only shape: **100.40 t/s** with `-p 0 -n 128 -r 20`.

The same model family with `Q4_K_S-3.61bpw` did not beat the Qwen3-Coder 98.51 t/s row:

- `Q4_K_S` r20: **94.37 t/s** tg128.
- `Q4_K_S` generation-only: **94.85 t/s** tg128.

Raw evidence:

- [`data/raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/qwen3-30b-2507-iq4xs-b9467-r50.csv`](data/raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/qwen3-30b-2507-iq4xs-b9467-r50.csv)
- [`data/raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/model-iq4xs.sha256`](data/raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/model-iq4xs.sha256)
- [`data/raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/README.md`](data/raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/README.md)

Interpretation:

- This is the first local direct `llama-bench` row above 100 t/s in the guide.
- It should be framed as "multiple 30B-class Qwen MoE routes around 98.5-100 t/s, with raw logs."
- It should not replace the Qwen3-Coder 30B headline, because it is a different general-instruct model and a different quant.
- It is not MTP, server/speculative decoding, or a multi-user aggregate result.

## 2026-06-05 Current-Model / Int-Dot Scout Status

A 2026-06-05 scout reran selected current-model rows on a newer local `llama.cpp` build where the Vulkan device line reported `int dot: 1`.

Key results:

- LFM2.5 8B-A1B `Q4_K_M`: **168.96 t/s** tg128 with pp512/tg128, and **170.02 t/s** generation-only.
- Nemotron 3 Nano 30B-A3B `IQ4_XS`: **75.97 t/s** tg128.
- Nemotron 3 Super 120B-A12B `UD-IQ4_XS`: **18.43 t/s** tg128.
- Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`: **98.32 t/s** tg128 with pp512/tg128, and **99.10 t/s** generation-only.
- Qwen3-Coder 30B-A3B `UD-Q4_K_XL`: **92.84 t/s** generation-only.

Raw evidence:

- [`data/raw/2026-06-05/latest-llamacpp-intdot-regression/`](data/raw/2026-06-05/latest-llamacpp-intdot-regression/)

Interpretation:

- LFM2.5 is the guide's fastest current small-MoE scout, but it is not a 30B-class capability replacement.
- Nemotron 3 Super is a direct 120B-class GGUF capacity/current-model route, not a speed headline.
- The latest/int-dot Qwen3-Coder UD row did not beat the older balanced or speed-first Qwen3-Coder rows.
- The earlier Qwen3-30B-A3B-Instruct-2507 b9467 r50 row remains the strongest direct 30B-class Qwen result at 100.04 t/s.

## 2026-06-07 llama.cpp b9544 Regression Control

A 2026-06-07 control built `llama.cpp` b9544 / `98d5e8ba8` locally and reran the available direct Vulkan/RADV sentinel rows with explicit `-dev Vulkan0`.

Key results:

- Qwen3-30B-A3B-Instruct-2507 `IQ4_XS`: **103.18 t/s** tg128 and **1438.10 t/s** pp512, r10.
- Qwen3-Coder 30B-A3B `UD-Q4_K_XL`: **97.08 t/s** tg128 and **1399.98 t/s** pp512, r5.
- LFM2.5 8B-A1B `Q4_K_M`: **176.48 t/s** tg128 and **3398.36 t/s** pp512, r10.
- Nemotron 3 Super 120B-A12B `UD-IQ4_XS`: **18.93 t/s** tg128 and **297.14 t/s** pp512, r3.

Raw evidence:

- [`data/raw/2026-06-07/latest-llamacpp-b9544-regression/`](data/raw/2026-06-07/latest-llamacpp-b9544-regression/)

Interpretation:

- b9544 did not regress the available direct Vulkan/RADV sentinel rows.
- Qwen3-30B-A3B-Instruct-2507 remains a separate direct 30B-class Qwen route above 100 t/s.
- LFM2.5 remains a small active-parameter MoE speed row, not a 30B-class replacement.
- Nemotron Super remains a direct 120B-class capacity/current-model row.
- The exact Qwen3-Coder `Q4_K_S` speed-first file used for the older 98.51 t/s headline was not present locally, so that row was not rerun and should remain scoped to its original b9179 evidence.

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

Local Beelink reproduction on the same source commit with the normal Ubuntu `glslc 2023.8` build path:

- default command: **1392.09 t/s pp512**, **96.38 t/s tg128**
- ten `-p 0` runs: **96.72 t/s best**, **96.51 t/s average**, **95.99 t/s minimum**
- local Vulkan device line: `int dot: 0`

The Reddit-reported GMKtec output showed `int dot: 1`. That matters because llama.cpp's Vulkan backend has integer-dot shader paths for quantized matmul. If the device and shader compiler expose that path, decode can be faster on Q4-style workloads.

The confusing part is that this Beelink's `vulkaninfo` reports `VK_KHR_shader_integer_dot_product` and `shaderIntegerDotProduct = true`, but the host Ubuntu `glslc` package used during CMake reports `GL_EXT_integer_dot_product not supported by glslc`. In practice, the hardware/driver capability is visible, but the default host shader-compiler path does not let this llama.cpp build enable the integer-dot shaders.

Follow-up: a separate host/RADV build using a container-wrapped `glslc v2026.1` did enable `GL_EXT_integer_dot_product`, and `llama-bench --list-devices` then reported `int dot: 1` on the same Beelink. That did **not** improve the result on this stack:

- default command: **1392.68 t/s pp512**, **95.61 t/s tg128**
- three `-p 0` checks before stopping the long run: **95.27-95.91 t/s**
- local Vulkan device line: `int dot: 1`

Interpretation:

- The Reddit result is plausible and valuable, but this guide has not reproduced it on the Beelink yet.
- `int dot: 1` is not sufficient by itself on this Beelink/RADV stack; the exact shader compiler, driver, and generated shader behavior still matter.
- The next clean route is to compare the Reddit reporter's OS, Mesa/driver, `glslc`, and `llama.cpp` build metadata against this local `glslc v2026.1` attempt before promoting any 100 t/s conclusion.
- Do not change the Beelink direct headline unless a repeated local run beats 98.51 t/s with raw output, host state, model hash, exact command, and `int dot: 1`/toolchain metadata.

Raw evidence:

- [`data/raw/2026-06-02/reddit-look-int-dot-reproduction/`](data/raw/2026-06-02/reddit-look-int-dot-reproduction/)
- [`data/raw/2026-06-02/community-reddit-look-qwen-coder/`](data/raw/2026-06-02/community-reddit-look-qwen-coder/)

## High-Power Policy And Thermal Tuning Status

A community GMKtec EVO-X2 follow-up later reported two important tuning details behind a roughly 100 t/s Qwen3-Coder 30B `Q4_K_S` result:

- the heatsink was reapplied with higher-quality thermal paste;
- stock thermal pads on memory chips were reseated, reportedly lowering CPU/GPU temperatures by 15-20C;
- Linux GPU DPM was forced to `high`, and CPU EPP was forced to `performance`.

This is useful context, but it is not a default recommendation. The reporter also warned that the policy can add roughly 15-20 W to GPU power, can be workload-dependent, and can be risky if the stock thermal interface is poor.

A short local Beelink follow-up used llama.cpp `1fd5f4803`, Qwen3-Coder 30B-A3B `Q4_K_S`, Vulkan/RADV, and this command shape:

```bash
llama-bench -m Qwen3-Coder-30B-A3B-Instruct-Q4_K_S.gguf -fa 1 -ngl 999 -mmp 0 -b 2048 -ub 512 -p 512 -n 128 -r 5
```

Result:

| Policy | pp512 | tg128 |
| --- | ---: | ---: |
| GPU `auto`, CPU EPP still reported `performance` | 1216.82 +/- 68.76 t/s | 95.18 +/- 1.42 t/s |
| GPU `high`, CPU EPP `performance` | 1390.03 +/- 7.91 t/s | 96.37 +/- 0.29 t/s |

Local interpretation:

- The high-power policy helped this short local run, especially prompt processing stability.
- It did not reproduce the external 100 t/s GMKtec result on this Beelink.
- The external thermal rework may matter as much as, or more than, the software policy.
- Keep this labeled as advanced tuning context until repeated with temperature, clock, power, and before/after logs.

Raw local logs: [`data/raw/2026-06-02/high-power-policy-test/`](data/raw/2026-06-02/high-power-policy-test/). Community provenance note: [`data/raw/2026-06-02/community-reddit-look-qwen-coder/`](data/raw/2026-06-02/community-reddit-look-qwen-coder/).

## Modern-Model Anti-Cherry-Pick Follow-Up

Reddit feedback correctly pointed out that the direct 98.51 t/s Qwen3-Coder 30B row should not be framed as the newest-model claim. The current framing is:

- Qwen3-Coder 30B `Q4_K_S` remains the reproducible direct-speed baseline.
- Newer/current models are tracked separately for capability and buyer relevance.
- Experimental server/speculative rows stay separate from direct `llama-bench`.

A clean follow-up on llama.cpp `1fd5f4803` / b9467 measured Qwen3-Coder-Next 80B-A3B `IQ4_XS` at **738.98 t/s pp512** and **61.91 t/s tg128**. This confirms the modern coding-model row remains far below the older 30B speed-first row on raw decode speed, but is useful current-model context.

The same follow-up repeated the previous best Qwen3.6 MTP IQ4_XS-Q8nextn b9360 server route. This repeat averaged **97.08 t/s** across six prompts, with code prompts at **105.28-106.24 t/s** and general prompts at **87.35-95.79 t/s**. This reinforces the caveat: MTP can cross 100 t/s on favorable prompts and previously crossed 100 t/s as a six-prompt average, but it should remain labeled as an experimental server/speculative route, not a beginner/simple direct benchmark.

DFlash/PFlash preflight found local source trees and cached assets, but no DFlash/PFlash performance claim is made yet.

Raw evidence: [`data/raw/2026-06-02/modern-model-clean-followup/`](data/raw/2026-06-02/modern-model-clean-followup/).
