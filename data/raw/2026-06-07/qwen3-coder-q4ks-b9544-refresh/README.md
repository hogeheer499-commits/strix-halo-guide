# Qwen3-Coder Q4_K_S b9544 Refresh - 2026-06-07

Purpose: rerun the exact Qwen3-Coder 30B-A3B `Q4_K_S` speed-first file used by the older 98.51 t/s Beelink headline on current `llama.cpp` b9544.

This is a control row, not a new headline. It answers whether the latest b9544 build plus the exact old model artifact beats the older b9179 strict-clean 98.51 t/s result.

## Artifact

- Source repo: `unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF`
- File: `Qwen3-Coder-30B-A3B-Instruct-Q4_K_S.gguf`
- Size: `17456012448` bytes
- SHA256: `56a7d00783419bcb0ae566253c371bcb3678261bb79881a553539f5679864db4`
- This SHA256 matches the file recorded in `data/raw/2026-05-16/qwen3-coder-break100-master/model-sha256.txt`.

## Build And Host

- System: Beelink GTR9 Pro
- APU: AMD Ryzen AI MAX+ 395 / Radeon 8060S
- Memory: 128GB unified memory
- Backend: Vulkan/RADV
- Mesa: 26.1.2 kisak
- llama.cpp: b9544 / `98d5e8ba8`
- Device: explicit `-dev Vulkan0`
- One workspace-critical service was left running. Remote desktop, local AI serving, VM, and media/backend services were paused for the benchmark window. Long-running background containers were left running.

## Results

| Shape | Raw CSV | Result | Read |
| --- | --- | ---: | --- |
| pp512/tg128 r10 | [`qwen3-coder-q4ks-b9544-p512-n128-r10.csv`](qwen3-coder-q4ks-b9544-p512-n128-r10.csv) | 98.36 tg128 / 1405.50 pp512 | Short confirmation. |
| pp512/tg128 r50 | [`qwen3-coder-q4ks-b9544-p512-n128-r50.csv`](qwen3-coder-q4ks-b9544-p512-n128-r50.csv) | 98.02 tg128 / 1406.45 pp512 | Best comparison to the older b9179 r50 headline. |
| p0/tg128 r20 | [`qwen3-coder-q4ks-b9544-p0-n128-r20.csv`](qwen3-coder-q4ks-b9544-p0-n128-r20.csv) | 98.49 tg128 | Generation-only control for community-style `-p 0` runs. |

## Interpretation

- b9544 reproduces the Qwen3-Coder `Q4_K_S` speed-first path around 98 t/s.
- It does not beat the older b9179 strict-clean first-party headline at 98.51 t/s.
- It does not create a first-party 100 t/s Qwen3-Coder claim.
- The separate Qwen3-30B-A3B-Instruct-2507 `IQ4_XS` route remains the first-party direct 100+ t/s 30B-class Qwen row.
