# DeepSeek V4 Flash UD-IQ2_XXS Direct Scout

Status: measured local pass.

This run answers whether the current ordinary GGUF route for DeepSeek V4
Flash loads and generates on one 128GB Strix Halo system after general
`deepseek_v4` support landed in `llama.cpp`.

## Pinned Inputs

- source: `unsloth/DeepSeek-V4-Flash-GGUF`
- source revision: `e3aa0d6a5fa4f820d9e132ac1fd1d01e1b2b49e0`
- quant: `UD-IQ2_XXS`, three GGUF shards
- artifact size: 90.86 GB / 84.62 GiB
- parameters reported by `llama-bench`: 284,334,567,511
- runtime: official `llama.cpp` b10034, commit `505b1ed15`
- backend: Vulkan/RADV on Radeon 8060S
- host: Beelink GTR9 Pro, Ryzen AI MAX+ 395, 128GB
- kernel: `6.19.4-061904-generic`
- Mesa: 26.1.4 kisak-mesa RADV

The exact source revision, local shard hashes, runtime version, device list,
host snapshot, and commands are stored beside this file.

## Direct Result

`llama-bench` command shape:

```text
-ngl 999 -fa on -mmp 0 -p 512 -n 128 -r 3 -o csv
```

| Test | Mean | Standard deviation |
| --- | ---: | ---: |
| pp512 | 155.6407 t/s | 0.2587 |
| tg128 | 13.2683 t/s | 0.0077 |

The model loaded completely and the deterministic smoke answered `9` to the
12-minus-3 check. It emitted a visible thinking block before the final answer
despite the instruction to answer with only the number, so this is a load,
generation, and basic-correctness pass rather than an instruction-following or
quality evaluation.

## Practical Read

This replaces the previous ordinary-GGUF download/runtime blocker with a
current direct capacity result. It shows that a 90.9GB, 284.33B-parameter
DeepSeek V4 Flash artifact can run on one 128GB Strix Halo box through the
normal Vulkan/RADV `llama.cpp` path.

It is not a speed recommendation. The low-bit `UD-IQ2_XXS` quant has an
important quality tradeoff, and 13.27 t/s is much slower than the guide's
30B-class or small-MoE speed routes. The separate 46.98GiB REAP artifact still
requires its specialized ds4 runtime and is not validated by this result.

## Evidence Map

- `download.txt`: completed three-shard download
- `source-revision.txt`: pinned source and revision
- `model-shards.sha256`: exact local GGUF hashes
- `llama-version.txt` and `llama-devices.txt`: runtime and GPU identity
- `host-snapshot.txt`: dated host, memory, disk, and Vulkan/RADV state
- `bench-command.txt`, `llama-bench.csv`, `llama-bench.stderr.txt`: direct benchmark
- `smoke-command.txt`, `smoke-output.txt`, `smoke-stderr.txt`: correctness smoke
- `download-and-run.sh`, `run-scout.sh`: reproducible harness
