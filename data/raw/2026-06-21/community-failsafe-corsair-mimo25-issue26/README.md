# Fail-Safe Corsair MiMo V2.5 Issue #26

Source: <https://github.com/hogeheer499-commits/strix-halo-guide/issues/26>

Contributor: Fail-Safe

This raw directory preserves the imported summary for Fail-Safe's Corsair AI Workstation 300 `ai-2` MiMo-V2.5 `UD-IQ2_M` report. Keep it as community capacity and telemetry evidence, not as a first-party headline claim.

## System

- Device: Corsair AI Workstation 300
- CPU/GPU: AMD Ryzen AI MAX+ 395 / Radeon 8060S
- Memory: 124 GiB visible, 128GB class
- BIOS UMA: 512MB, inferred from the report and visible memory state
- IOMMU: off via `amd_iommu=off`
- OS: Fedora Linux 44 Server Edition
- Kernel: `7.0.12-201.fc44.x86_64`
- Mesa: `Mesa 25.3.6` inside the Vulkan container
- Vulkan ICD: RADV
- ROCm: host `rocminfo` runtime `1.18`; ROCm container tag `rocm-7.2`
- Ollama: not installed / not used
- `tuned`: not available on this host

## Benchmark

- Model: `MiMo-V2.5-UD-IQ2_M`
- Model source: local mirror under `/data/models/UD-IQ2_M/`; original source repo and model hash were not captured in the run
- GGUF path: `/data/models/UD-IQ2_M/MiMo-V2.5-UD-IQ2_M-00001-of-00003.gguf`
- Backend: direct `llama-bench` Vulkan/RADV
- Container/tool: `docker.io/kyuz0/amd-strix-halo-toolboxes:vulkan-radv`
- Build: `build_commit=32eddaf2e`, `build_number=9712`
- Command shape: `-fa 1 -ngl 999 -mmp 0 -b 2048 -ub 512 -p 512 -n 128 -r 20 -o csv`

The pasted CSV row has `n_prompt=512` and `n_gen=0`, so the imported structured result is a prompt-processing row only:

- `pp512`: 30.650898 t/s
- `tg128`: not captured in the pasted CSV row
- model size: 96,552,297,984 bytes
- model params: 309,766,601,088
- model type: `mimo2 310B.A15B IQ2_M - 2.7 bpw`

See [`llama-bench-mimo25-udiq2m.csv`](llama-bench-mimo25-udiq2m.csv) for the imported CSV row.

## Telemetry Summary

Fail-Safe also included live telemetry sampled during the run. The full per-sample telemetry CSV remains in issue #26; the compact imported summary is in [`telemetry-summary.csv`](telemetry-summary.csv).

| Metric | Low | High | Mean |
| --- | ---: | ---: | ---: |
| Home Assistant wall power | 29.7 W | 162.4 W | 114.14 W |
| GPU edge temperature | 40.0 C | 75.0 C | 59.76 C |
| GPU socket power | 14.098 W | 104.021 W | 70.92 W |

Clock observations from the report:

- `pp_dpm_sclk` moved through `600MHz`, `1100MHz`, `1771-2399MHz`, and finished at `2400MHz *` in the sampled window.
- `pp_dpm_mclk` stayed at `1000MHz *` in the sampled window.
- `pp_od_clk_voltage` reported `SCLK: 600MHz 2900MHz`.

## Guide Interpretation

This is useful Corsair community capacity evidence for a 310B-total / 15B-active MoE GGUF route on a single 128GB-class Strix Halo system. It is not a speed headline because generation throughput was not captured in the pasted CSV row, and model source/hash were not captured.

