# DeepSeek V4 Flash 0xSero / Spark-Mini Load Failure

Purpose: follow up the earlier DeepSeek V4 Flash download-blocked attempt with a smaller 0xSero / Spark-Mini GGUF route.

Outcome: local file existed and `llama-bench` smoke attempts were run, but the model did not load. No benchmark result was produced.

Host / backend notes:

- Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S.
- Vulkan/RADV Strix Halo path.
- Device lines were captured with both `int dot: 0` and `int dot: 1` build paths.
- Normal workstation context; this was a practical smoke/load check, not a cold benchmark campaign.

Target model:

```text
DeepSeek-V4-Flash-Spark-Mini-Q2-REAP-ds4.gguf
```

Local file:

```text
52,593,532,000 bytes
```

The repository stores the small `.sha256` sidecar in `model.sha256`, but does not store the model file itself.

Attempted smoke shape:

```text
llama-bench -p 0 -n 32 -r 1
```

Observed failure:

```text
llama_bench: error: failed to load model '/home/hoge-heer/benchmark-models/deepseek-v4-flash-162b-0xsero/DeepSeek-V4-Flash-Spark-Mini-Q2-REAP-ds4.gguf'
```

Captured files:

- `devices.txt`: Vulkan/RADV device discovery with `int dot: 1`.
- `smoke-p0-tg32-r1.stderr.txt`: `int dot: 1` load failure.
- `smoke-intdot-b2016bf2-p0-tg32-r1.stderr.txt`: second `int dot: 1` load failure on the latest/int-dot build path.
- `smoke-latest-p0-tg32-r1.stderr.txt`: `int dot: 0` load failure on a latest path.
- `smoke-fresh-p0-tg32-r1.stderr.txt`: fresh build load failure.
- `smoke-llamacpp-c723-p0-tg32-r1.stderr.txt`: environment failure from a HIP-linked `llama-bench` binary missing `libhipblas.so.3`; do not treat this as a model/runtime result.
- CSV files contain headers only because no run completed.

Interpretation:

- This is stronger friction evidence than the earlier 103GB single-file download attempt: a smaller local route was present, but current local `llama.cpp` smoke attempts still failed before benchmarking.
- Do not list DeepSeek V4 Flash as a pass, speed result, or Strix Halo capability claim from this attempt.
- The useful buyer/vendor lesson is that artifact availability is not enough. GGUF compatibility, runtime support, backend build, and reproducible loadability still matter.
