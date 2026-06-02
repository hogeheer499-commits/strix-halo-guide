# Reddit GMKtec Qwen3-Coder Tuned Report

Source: https://www.reddit.com/r/StrixHalo/comments/1tu78x5/qwen3coder_30b_at_985_ts_on_strix_halo_has_anyone/

Contributor: `Look_Over_There`

System:

- GMKtec EVO-X2
- AMD Ryzen AI MAX+ 395 / Radeon 8060S
- RAM, OS, kernel, and Mesa versions were not reported in the captured comment thread
- Vulkan device line reported `RADV_STRIX_HALO`

Benchmark shape:

```bash
llama-bench -fa 1 -n 128 -p 0 -m ./Qwen3-Coder-30B-A3B-Instruct-Q4_K_S.gguf
```

Reported tool/build:

- llama.cpp build `1fd5f4803 (9467)`
- Vulkan/RADV
- Qwen3-Coder 30B-A3B Instruct `Q4_K_S`

Reported result:

- Most `-p 0 -n 128` runs were around 99.90 t/s.
- Best observed run reached a clean 100.0 t/s after about 10 runs.

Contributor qualifier:

- The contributor re-applied the heatsink with high-quality thermal paste and reseated stock thermal pads on the memory chips.
- They reported CPU/GPU temperatures about 15-20C lower than the original factory state.
- They also used a Linux high-power policy script:

```bash
for card in /sys/class/drm/card*/device/power_dpm_force_performance_level; do
    echo high | sudo tee "$card"
done
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/energy_performance_preference
```

Interpretation:

- This is valuable external tuned-performance evidence from another Strix Halo chassis.
- It should not be mixed into the guide's first-party Beelink headline number.
- It suggests that thermals, factory heatsink/pad quality, power policy, and exact toolchain/driver state can matter for the last few percent of Qwen3-Coder short-context generation speed.
- Local Beelink follow-up with the same b9467 command did not reproduce 100 t/s. It measured 96.38-96.72 t/s on the default build path and 95.27-95.91 t/s on an `int dot: 1` `glslc v2026.1` build. A separate local high-power policy test improved one short b9467 Qwen3-Coder run from 95.18 to 96.37 t/s, but still did not reach 100 t/s.

Related local follow-ups:

- [`../reddit-look-int-dot-reproduction/`](../reddit-look-int-dot-reproduction/)
- [`../high-power-policy-test/`](../high-power-policy-test/)

