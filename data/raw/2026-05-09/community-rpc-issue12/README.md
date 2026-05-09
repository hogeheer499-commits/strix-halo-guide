# strix-halo issue #12 RPC bench data

Raw data accompanying the comment posted on https://github.com/hogeheer499-commits/strix-halo-guide/issues/12.

## Files

- **`csv-combined-rpc-bench.csv`** — all 14 successful bench cells in a single CSV, with four extra columns prepended (`phase`, `model_label`, `backend_label`, `nodes`) so it can drop into `data/community_rpc.csv`-style ingestion. 28 rows = 14 cells × {pp512, tg128}.
- **`csv/`** — the 14 individual `llama-bench -o csv` outputs as written, one per cell. Filenames encode `<model>-<backend>-<nodes>n.csv`.

## Phase mapping

| Phase | Model                              | Quant      | Size    | Single-box fit? |
|-------|------------------------------------|------------|---------|-----------------|
| 1     | Qwen3-Coder-30B-A3B (qwen3moe)     | UD-Q4_K_XL | 17.7 GB | yes             |
| 2     | Qwen3-Coder-Next (qwen3next 80B.A3B) | UD-Q8_K_XL | 86.3 GB | yes             |
| 3     | MiniMax-M2.7 (230B.A10B)           | UD-Q4_K_XL | 140.8 GB| no              |

## Bench command

Same `llama-bench` invocation across every cell:

```
llama-bench -m <gguf> [--rpc <followers>] -fa 1 -ngl 999 -mmp 0 -p 512 -n 128 -r <r> -o csv
```

`-r 20` for Phases 1 & 2; `-r 5` for Phase 3 (each tg128 rep on the 140 GB model takes 12-14 s, so 20 reps × 4 cells was prohibitive).

## Cells not represented

Four Phase 3 cells failed to load and produced no bench rows:

- Phase 3 / Vulkan/RADV / 1n — `radv/amdgpu: Failed to allocate a buffer: 830472192 bytes` (792 MiB single-tensor)
- Phase 3 / Vulkan/RADV / 2n — same allocation failure, this time on the RPC follower
- Phase 3 / Vulkan/RADV / 3n — skipped, same root cause expected
- Phase 3 / ROCm 7.2 / 1n — out of memory (model size 140.8 GB > 124 GiB single-box GTT ceiling)

Failure-cell stderr available on request.

## Container builds

The two backends ship different llama.cpp builds:
- Vulkan/RADV image: `build_commit=1e5ad35d5`, `build_number=9093`
- ROCm 7.2 image: `build_commit=d6f303004`, `build_number=8738`

Within-backend RPC overhead numbers are unaffected. Absolute Vulkan-vs-ROCm comparisons carry that caveat.
