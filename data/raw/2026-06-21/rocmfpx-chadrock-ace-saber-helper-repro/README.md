# ROCmFPX CHADROCK ACE/SABER Helper Repro

First-party Beelink GTR9 Pro reproduction of ciru-ai's corrected ROCmFPX /
CHADROCK ACE/SABER MTP route.

This run matters because the earlier local attempt loaded the model but did not
use the official helper runner path. The corrected run used the pinned
`ciru-ai/ROCmFPX` helper script with `--spec-draft-poll 1` and
`--spec-draft-poll-batch 1`, plus the CHADROCK ACE/SABER model.

## Result

Best local gen512 repeats on a 3946-token synthetic prompt:

| Run | Decode | Prompt | Draft accepted |
| --- | ---: | ---: | ---: |
| repeat 1 | 140.40 tok/s | 1071.04 tok/s | 408 / 408 |
| repeat 2 | 139.93 tok/s | 1067.52 tok/s | 408 / 408 |
| repeat 3 | 114.95 tok/s | 1048.90 tok/s | 386 / 467 |

The local gen2048 check on the same 3946-token prompt reached 127.77 tok/s
with 1595 / 1753 draft tokens accepted.

Interpretation: the high-speed CHADROCK path is real and reproduced locally,
but it is acceptance-sensitive. The guide should present this as an advanced
ROCmFPX/MTP route, not as a default beginner path and not as a direct
`llama-bench` result.

## Runner

- Source: `ciru-ai/ROCmFPX`
- Runner commit: see `runner_commit.txt`
- Binary: `build-strix-rocmfp4/bin/llama-server`
- Model: `Qwen3.6-35B-A3B-NSC-ACE-SABER-MTP-F16-to-ROCmFP4-STRIX_LEAN.gguf`
- Model hash: see `model.sha256`

## Server Shape

The run used the official helper path from `scripts/run-rocmfpx-mtp-server.sh`
with:

```text
DEVICE=Vulkan0
SPEC_DRAFT_DEVICE=Vulkan0
CTX_SIZE=32768
BATCH_SIZE=2048
UBATCH_SIZE=512
CACHE_TYPE_K=f16
CACHE_TYPE_V=f16
CACHE_TYPE_K_DRAFT=f16
CACHE_TYPE_V_DRAFT=f16
SPEC_DRAFT_N_MAX=4
SPEC_DRAFT_N_MIN=0
SPEC_DRAFT_P_MIN=0.25
SPEC_DRAFT_P_SPLIT=0.10
NO_MMPROJ=1
STRICT_BENCH=1
```

Requests used `/completion` with:

```json
{
  "n_predict": 512,
  "temperature": 0,
  "ignore_eos": true,
  "cache_prompt": false,
  "speculative.n_max": 4,
  "speculative.n_min": 0,
  "speculative.p_min": 0.25
}
```

## Files

- `server.log`: full server log with timing and draft acceptance lines.
- `repeat_summary.json`: compact gen512 repeat summary.
- `initial_sweep_summary.json`: earlier prompt/profile sweep in the same helper run.
- `helper_repeat*_prompt3946_p025_gen512.*.json`: request/response pairs for the
  three gen512 repeats.
- `helper_prompt3946_p025_gen2048.*.json`: gen2048 request/response pair.
- `prompt_3946_exactish.txt`: synthetic 3946-token prompt used for the repeat.
- `post_run_services.txt`: user-service status after cleanup.
