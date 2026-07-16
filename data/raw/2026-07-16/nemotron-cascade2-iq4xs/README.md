# Nemotron Cascade 2 30B-A3B IQ4_XS Scout

Date: 2026-07-16

System: Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S, 128 GB
unified memory.

This scout checks whether the current Nemotron Cascade 2 model family has a
practical direct GGUF route on one Strix Halo system. It is a load, speed, and
small correctness check rather than a broad quality evaluation.

## Reproducibility Pin

- runtime: official `llama.cpp` b10034, commit `505b1ed15`
- backend: Vulkan/RADV, full GPU offload
- model: `nvidia_Nemotron-Cascade-2-30B-A3B-IQ4_XS.gguf`
- quant source: `unsloth/Nemotron-Cascade-2-30B-A3B-GGUF`
- quant source revision: `931b595fc71b7ca14fb9d935af011f69f7c0434c`
- model SHA-256: `871a80bfd682289f2efa1b4fdee899576b5a768681f2b2ad74a15b59af6a510e`

## Result

| Test | Result |
| --- | ---: |
| `pp512` | 1325.31 t/s |
| `tg128` | **78.95 t/s** |
| reasoning smoke | correct: 9 sheep remain |
| forced no-think smoke | correct: 9 sheep remain |

The IQ4_XS artifact occupies about 18.17 GB and loads cleanly through the
current upstream Vulkan runtime. Both small answer checks completed at about
78.7 t/s. The no-think prefix did not suppress the model's visible reasoning,
so this run does not claim a reliable no-think mode.

This is a useful current-model route, but it is not a replacement for a proper
quality evaluation and not a new overall speed headline.

## Evidence

- [`llama-bench.csv`](llama-bench.csv): direct benchmark result
- [`thinking-output.txt`](thinking-output.txt): reasoning smoke output
- [`instruct-output.txt`](instruct-output.txt): forced no-think smoke output
- [`run-scout.sh`](run-scout.sh): exact reproducible runner
- [`host-snapshot.txt`](host-snapshot.txt): host and Vulkan context
- [`model.sha256`](model.sha256): exact model identity
- [`upstream-model-card.md`](upstream-model-card.md) and
  [`quant-card.md`](quant-card.md): source metadata captured at test time

An initial harness attempt omitted `--single-turn`, causing interactive
`llama-cli` to continue printing empty prompts after the correct answer. The
published runner includes `--single-turn --simple-io`; this was a harness I/O
error, not a model or backend failure.
