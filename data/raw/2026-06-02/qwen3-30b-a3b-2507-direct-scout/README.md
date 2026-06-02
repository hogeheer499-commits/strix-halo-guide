# Qwen3 30B-A3B Instruct 2507 Direct Scout

Purpose: test whether the newer `Qwen3-30B-A3B-Instruct-2507` 30B-A3B speed-shape can replace or challenge the older Qwen3-Coder 30B `Q4_K_S` direct speed headline.

Host notes:

- Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S.
- Workspace-critical services were kept running.
- Nonessential user-interface noise was partially cleaned where safe.
- Some background services remained active, so treat this as a strong real-workstation direct result rather than a fully isolated cold-boot lab run.

Models:

```text
byteshape/Qwen3-30B-A3B-Instruct-2507-GGUF
Qwen3-30B-A3B-Instruct-2507-Q4_K_S-3.61bpw.gguf
Qwen3-30B-A3B-Instruct-2507-IQ4_XS-3.63bpw.gguf
```

Build:

```text
llama.cpp 1fd5f4803 / b9467
Vulkan/RADV
```

Device line:

```text
Radeon 8060S Graphics (RADV_STRIX_HALO), int dot: 0, matrix cores: KHR_coopmat
```

Results:

| Model / quant | Shape | Result | Read |
| --- | ---: | --- |
| `Q4_K_S-3.61bpw` | `pp512/tg128`, r5 | 1272.62 pp512 / 94.80 tg128 | Fast, but below the 98.51 t/s Qwen3-Coder 30B `Q4_K_S` headline. |
| `Q4_K_S-3.61bpw` | `pp512/tg128`, r20 | 1272.56 pp512 / 94.37 tg128 | Confirms this quant is a stable near-miss, not a replacement headline. |
| `Q4_K_S-3.61bpw` | `-p 0 -n 128`, r10 | 94.85 tg128 | Generation-only shape also stays below 98.51 t/s. |
| `IQ4_XS-3.63bpw` | `pp512/tg128`, r5 | 1418.53 pp512 / 99.80 tg128 | Scout crossed the old 98.51 t/s direct headline. |
| `IQ4_XS-3.63bpw` | `pp512/tg128`, r20 | 1418.23 pp512 / 100.58 tg128 | Confirmed direct 100+ t/s route on this b9467 stack. |
| `IQ4_XS-3.63bpw` | `-p 0 -n 128`, r20 | 100.40 tg128 | Generation-only shape also remains above 100 t/s. |
| `IQ4_XS-3.63bpw` | `pp512/tg128`, r50 | 1416.03 pp512 / 100.04 tg128 | Longest confirmation in this scout; remains above 100 t/s direct. |

Interpretation:

- The 30B-A3B speed-shape hypothesis is directionally right: this model is in the same high-throughput class.
- The `Q4_K_S` file did not beat the old direct headline, but the similar-size `IQ4_XS` file did.
- This is a direct `llama-bench` result, not MTP/server/speculative decoding.
- Treat as a new candidate headline only after deciding how to frame the model date/popularity caveat: `Qwen3-30B-A3B-Instruct-2507` is adjacent to, not clearly newer than, the existing Qwen3-Coder 30B headline.
