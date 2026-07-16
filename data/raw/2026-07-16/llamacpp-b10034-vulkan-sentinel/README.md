# llama.cpp b10034 Vulkan MoE Concurrency Sentinel

Date: 2026-07-16

System: Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S, 128 GB unified memory.

This latest-release sentinel checks whether the sharp 8-to-9 parallel-sequence
throughput cliff documented in [`MOE_CONCURRENCY.md`](../../../../MOE_CONCURRENCY.md)
still exists in the official `llama.cpp` b10034 Ubuntu Vulkan build. It reuses
the same two local model artifacts and command shape as the controlled b9979
campaign.

## Source And Models

- upstream release: `llama.cpp` b10034
- source commit: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
- official release-asset SHA-256: `cec255e083eb5617a08f1923c0b043a391a53b5d09d573675f697a8053008d73`
- Qwen3-Coder 30B-A3B `UD-Q4_K_XL`: SHA-256 `2841aa314d916434860cfb8990347528dcdfe5c350dbcb9d1461dbee88ff2533`
- Qwen3-Next 80B-A3B `UD-Q4_K_XL`: SHA-256 `49e554f954afbfc9f627b8be236adf16c1e51d8e5ecaa0e65ac8ede4e2c41a56`

The exact binary hash, host state, driver, and model sizes are preserved in
[`host-snapshot.txt`](host-snapshot.txt).

## Command Shape

```bash
llama-batched-bench \
  -m MODEL.gguf \
  -c 65536 -ngl 999 -fa on \
  -ctk q4_0 -ctv q4_0 --no-mmap \
  -npp 512 -ntg 128 -npl 8,9 \
  --output-format jsonl
```

Each model was measured three times. The wrapper waits for a sub-50 C start,
records one-second sysfs telemetry, and aborts at 95 C.

## Result

| Model | np8 decode mean | np9 decode mean | 8-to-9 change | Read |
| --- | ---: | ---: | ---: | --- |
| Qwen3-Coder 30B-A3B | 232.69 t/s | 145.79 t/s | -37.34% | Cliff persists. |
| Qwen3-Next 80B-A3B | 144.61 t/s | 98.78 t/s | -31.69% | Cliff persists. |

The three np9 repeats were tightly grouped: 145.61-145.94 t/s for the 30B
model and 98.49-99.22 t/s for the 80B model. Prompt-processing throughput did
not show a matching collapse.

This is a latest-runtime regression sentinel, not a new positive speed
headline. It shows that b10034 has not removed the concurrency cliff. The
separate b9979 campaign remains the source for the opt-in AMD/RADV density-gate
comparison and correctness checks.

## Evidence

- [`summary.csv`](summary.csv): parsed prompt, decode, and combined throughput
- `qwen*-stock-r*.jsonl`: complete benchmark output per repeat
- `qwen*-stock-r*.stderr.txt`: command metadata and backend initialization
- `qwen*-stock-r*.telemetry.csv`: one-second temperature, PPT, clock, and utilization telemetry
- [`telemetry-summary.json`](telemetry-summary.json): aggregate telemetry scope and values
- [`run-b10034-sentinel.sh`](run-b10034-sentinel.sh): exact benchmark wrapper
- [`host-snapshot.txt`](host-snapshot.txt): host, binary, model, driver, and process state

`amdgpu` `power1_average` is package telemetry, not measured wall power.
