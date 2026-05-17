# Community Power Telemetry From Issue #6

Source issue: <https://github.com/hogeheer499-commits/strix-halo-guide/issues/6>

Status: community-reported whole-system wall-power telemetry. These rows are useful for tokens-per-watt context, but they are not local Beelink wall-power headline claims.

Contributor: [Fail-Safe](https://github.com/Fail-Safe)

System: Corsair AI Workstation 300 Strix Halo systems with Ryzen AI MAX+ 395 / Radeon 8060S / 128GB LPDDR5X.

Measurement method:

- Zigbee smart plugs.
- Home Assistant WebSocket capture.
- Plug `state_changed` events merged with periodic `get_states` polls every 5 seconds.
- Idle baseline captured around the benchmark windows.
- Sustained token-generation rows use longer `-n 1024` runs so the plug has enough time to report stable load.
- Prompt-processing rows use `-p 16384 -n 0 -r 10` to create a longer sustained compute-bound phase.

Structured rows imported into [`data/community_power.csv`](../../../community_power.csv):

| Source | Box | Model | pp peak wall W | tg sustained wall W | tg throughput | tg wall J/token | Notes |
|--------|-----|-------|---------------:|--------------------:|--------------:|----------------:|-------|
| [Qwen3.6 comment](https://github.com/hogeheer499-commits/strix-halo-guide/issues/6#issuecomment-4414228987) | ai-2 | Qwen3.6 35B-A3B Q4_0 | 203.0 | 148.0 | 75.41 t/s tg1024 | 1.96 | pp peak time-weighted across 157 sec; tg held 130 sec across 26 polls. |
| [gpt-oss comment](https://github.com/hogeheer499-commits/strix-halo-guide/issues/6#issuecomment-4414323665) | ai-1 | gpt-oss-120b MXFP4 | 259.4 | 173.6 | 55.90 t/s tg1024 | 3.10 | pp peak time-weighted across 294 sec with 16 elevated events; tg held 124 sec across 25 polls. |
| [Qwen3-Coder-Next comment](https://github.com/hogeheer499-commits/strix-halo-guide/issues/6#issuecomment-4414411995) | ai-2 | Qwen3-Coder-Next 80B-A3B Q8_0 | 211.9 | 137.4 | 39.98 t/s tg1024 | 3.44 | pp peak time-weighted across 271 sec; tg held 256 sec across 51 polls. |

Existing earlier Qwen3-Coder rows from issue #10 remain in [`data/community_power.csv`](../../../community_power.csv):

- Qwen3-Coder 30B-A3B UD-Q4_K_XL, about 150 W sustained generation and about 1.59 J/token on ai-2.

Practical interpretation:

- Qwen3-Coder remains the best measured community energy-per-generated-token row in this set.
- gpt-oss-120b is much less efficient per generated token than Qwen3-Coder on this wall-power sample.
- Qwen3-Coder-Next Q8_0 shows that disk size and parameter count alone do not predict wall power; throughput and actual bandwidth/kernel intensity matter.
- The Beelink still needs its own wall-meter run before this guide should publish Beelink tokens-per-watt headline claims.
