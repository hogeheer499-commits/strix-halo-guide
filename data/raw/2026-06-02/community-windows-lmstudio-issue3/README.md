# Windows LM Studio Community Report - Issue #3

Source: https://github.com/hogeheer499-commits/strix-halo-guide/issues/3#issuecomment-4602020775

Contributor: `bennos1911`

System:

- Minisforum MS-S1-Max
- AMD Ryzen AI MAX+ 395 / Radeon 8060S
- 128GB memory, with AMD Adrenalin Variable Graphics Memory configured to 96GB GPU memory and about 31.6GB OS-usable system memory
- Windows 11 Pro 25H2 build 26200.8457
- AMD chipset 8.05.04.516
- AMD Adrenalin 26.5.2

Benchmark shape:

- LM Studio 0.4.15 build 2
- Vulkan llama.cpp v2.18.0
- `Qwen3.6-35B-A3B-Q4_K_M.gguf`
- `n_parallel=4`
- `n_ctx=262144`
- `kv_unified=true`
- benchmark script executed from WSL2 Ubuntu while the LM Studio GPU work runs on the Windows host
- command reported by contributor:

```bash
python3 lm_studio_bench_amd.py --model qwen/qwen3.6-35b-a3b --num-runs 15 --max-tokens 512
```

Reported summary:

- 45 total runs across three prompts
- average latency 3.700s, P50 2.541s
- average script throughput 89.49 tok/s, median 78.53 tok/s

Interpretation:

- This is the first Windows / LM Studio / Ryzen AI MAX+ 395 community report imported into the guide.
- It is useful buyer-friction evidence because many Strix Halo users start on Windows and want to know whether a Windows local-AI path works.
- It is not an apples-to-apples Linux `llama-bench` comparison. The guide's direct headline rows use native Linux Vulkan/RADV `llama-bench`; this report uses an LM Studio API benchmark with multiple prompt lengths, `n_parallel=4`, 262K context, and 512-token generations.
- The overall 89.49 tok/s script average includes very short prompts. The long 512-token prompt rows in the imported CSV are around 69-70 tok/s.

Imported artifacts:

- `lm_studio_bench_amd.py`: contributor benchmark script
- `lm_studio_bench_wsl.csv`: run CSV from the contributor
- `Hardware.20260602-210603.csv`: hardware telemetry CSV from the contributor

