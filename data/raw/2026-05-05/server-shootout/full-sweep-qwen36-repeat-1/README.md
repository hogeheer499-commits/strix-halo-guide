# 2026-05-05 Server Shootout Repeat: Qwen3.6 Workstation Baseline

Status: repeat validation run.

This rerun checks whether the normal workstation background state materially
changed the previous full-sweep result.

## Protocol

Same protocol as `../full-sweep-qwen36-workstation-baseline/`:

- Qwen3.6 35B-A3B UD-Q4_K_M
- OpenAI-compatible streaming `/v1/completions`
- 128 generated tokens per request
- 5 measured reps plus warmup
- parallel requests: 1, 2, 4, 8, 16
- 4096 context tokens per slot
- normal workstation baseline recorded

The hygiene check reported 0 blockers and 0 warnings before and after the rerun.

## Delta From Previous Full Sweep

| Server | Backend | Parallel | Previous t/s | Repeat t/s | Delta | Repeat p95 ITL |
|--------|---------|---------:|-------------:|-----------:|------:|---------------:|
| `llama-server` | Vulkan/RADV | 1 | 58.80 | 59.56 | +1.3% | 16.0 ms |
| `llama-server` | Vulkan/RADV | 2 | 96.08 | 97.34 | +1.3% | 19.5 ms |
| `llama-server` | Vulkan/RADV | 4 | 138.83 | 138.12 | -0.5% | 27.4 ms |
| `llama-server` | Vulkan/RADV | 8 | 170.87 | 172.96 | +1.2% | 44.6 ms |
| `llama-server` | Vulkan/RADV | 16 | 189.72 | 190.77 | +0.6% | 81.2 ms |
| Lemonade `llamacpp-rocm` | ROCm/gfx1151 | 1 | 48.62 | 51.40 | +5.7% | 18.9 ms |
| Lemonade `llamacpp-rocm` | ROCm/gfx1151 | 2 | 82.19 | 84.72 | +3.1% | 22.9 ms |
| Lemonade `llamacpp-rocm` | ROCm/gfx1151 | 4 | 127.03 | 125.75 | -1.0% | 30.6 ms |
| Lemonade `llamacpp-rocm` | ROCm/gfx1151 | 8 | 177.17 | 181.95 | +2.7% | 42.4 ms |
| Lemonade `llamacpp-rocm` | ROCm/gfx1151 | 16 | 207.81 | 212.38 | +2.2% | 72.6 ms |

## Interpretation

The rerun does not change the recommendation. Vulkan/RADV remains better for
1-4 parallel requests. Lemonade ROCm b1259 remains better for 8-16 parallel
requests.

The changes are consistent with normal run-to-run variance and do not invalidate
the earlier split.

## Files

- `summary.csv`
- `cleanliness-before-all.txt`
- `cleanliness-after-all.txt`
- `cleanliness-after-all-confirm.txt`
- `vulkan-radv/`
- `lemonade-b1259-rocm/`
