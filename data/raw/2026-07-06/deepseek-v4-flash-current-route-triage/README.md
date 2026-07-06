# DeepSeek V4 Flash Current Route Triage

Date: 2026-07-06

Purpose: re-check current DeepSeek V4 Flash artifact routes before spending another large download/test cycle.

This is not a benchmark pass/fail. It is a distribution and runtime-route triage note.

## Routes Checked

| Route | Observed status | Read |
| --- | --- | --- |
| `unsloth/DeepSeek-V4-Flash-GGUF` | New GGUF route with `UD-Q4_K_XL` and `UD-Q8_K_XL` shards. Model card says Q8 is 162GB and only about 6GB bigger than Q4, so Q4 is still roughly 156GB. | Interesting, but too large for a quick one-box internal-disk smoke test here. |
| `ilintar/DeepSeek-V4-Flash-GGUF` | `IQ2_M` shard set totals about 92.8 GiB by HEAD metadata. | Best ordinary-GGUF size candidate found in this scan, but the download was too slow to complete during this pass. |
| `sleepyeldrazi/deepseek-v4-flash-reap-k128-Q2-GGUF` | Model card reports 46.98 GiB. | Smaller, but requires the `eouya2/ds4-for-reaped` / compact ds4 runtime route rather than the guide's normal `llama.cpp` path. |

## Local Download Attempt

Attempted route:

```text
ilintar/DeepSeek-V4-Flash-GGUF
include: iq2m/*.gguf
```

The download was stopped before a usable model was available. Visible progress was roughly 0.5GB after several minutes, the partial directory was about 2.9GB when stopped, and the partial files were removed after the stop. No load test or benchmark was run.

## Interpretation

- DeepSeek V4 Flash remains a high-interest watchlist item because the model is current and recognizable.
- The current practical blocker is still artifact/runtime friction, not a measured Strix Halo speed or capacity failure.
- The next clean test should use either external storage / a longer download window for the 92.8 GiB `IQ2_M` GGUF route, or a separate ds4 runtime lane for the 46.98 GiB REAP route.
- Do not list this as a local pass until a full artifact loads and produces a measured row.
