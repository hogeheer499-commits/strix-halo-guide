# ROCmFPX CHADROCK ACE/SABER Repro Attempt

Date: 2026-06-21

Purpose: test ciru-ai's corrected CHADROCK ROCmFPX / ROCmFP4 MTP route for the ACE/SABER 35B artifact on the guide's Beelink GTR9 Pro / Ryzen AI MAX+ 395 system.

This is not a direct `llama-bench` headline result. It is first-party reproduction evidence for an advanced `llama-server` / MTP route.

## Route

- Guide system: Beelink GTR9 Pro
- GPU: Radeon 8060S / RADV STRIX_HALO through `Vulkan0`
- Model repo: `jcbtc/chadrock-35b-ace-saber-rocmfp4-mtp`
- Model file: `Qwen3.6-35B-A3B-NSC-ACE-SABER-MTP-F16-to-ROCmFP4-STRIX_LEAN.gguf`
- Model sha256: `6a635d1d8ac4af8f2c4ca6ff528bc6bad9b3a6d45e8630ef6e5728f04898eeed`
- Runner repo: `ciru-ai/ROCmFPX`
- Runner commit: `deaa996dab90b3ca6dd3ae5d453bedfcd983012d`
- Binary: `llama-server`
- Runner version: `version: 17 (deaa996)`
- Build used here: host Vulkan-only build with `GGML_VULKAN=ON` and `GGML_HIP=OFF`

The Distrobox ROCm/HIP build path had HIP available, but it did not have Vulkan headers/libraries available for this runner build. The host had Vulkan/RADV available, so this repro attempt used a host Vulkan-only build.

## Results

| Run | Prompt | Spec | Result | Draft acceptance |
| --- | ---: | --- | ---: | ---: |
| Initial 3945-token repro | 3945 tokens | `n_max=4`, `p_min=0.25` | 883.73 prompt t/s / 73.64 predicted t/s | 315 / 677 |
| Cleaned repeat | 3945 tokens | `n_max=4`, `p_min=0.25` | 1051.53 prompt t/s / 81.82 predicted t/s | 315 / 677 |
| Cleaned no-draft control | 3945 tokens | no draft | 1121.61 prompt t/s / 75.61 predicted t/s | n/a |
| Cleaned `p_min=0.0` probe | 3945 tokens | `n_max=4`, `p_min=0.0` | 1121.87 prompt t/s / 72.49 predicted t/s | 301 / 834 |
| Short page-prompt smoke | 14 tokens | `n_max=4`, `p_min=0.25` | 101.65 prompt t/s / 86.69 predicted t/s | 332 / 656 |

The cleaned repeat paused the local VM, DocFlock, and Hermes services while keeping T3 running. Root-managed Ollama/RustDesk services were not stopped in this run. All paused services were restored after the benchmark.

## Interpretation

This route is valuable because it confirms that the corrected CHADROCK ACE/SABER artifact and pinned ROCmFPX runner can load and serve locally on the guide's Beelink/RADV path.

It did not reproduce ciru-ai's published high-speed 35B route yet. The largest mismatch is draft acceptance:

- this repro: `315 / 677` accepted on the 3945-token `p_min=0.25` run
- ciru-ai model-card row: `408 / 408` accepted for the comparable gen512 row

That makes the next useful follow-up very specific: obtain the exact prompt/payload, build/runtime details, and any runner-profile settings used for the published high-acceptance result.

Treat this as:

- successful first-party load/API/MTP evidence
- successful corrected-route smoke evidence
- a reproducible gap to investigate
- not a new public speed headline
- not a default beginner setup path

## Files

- `ciru_chadrock_rocmfpx_page.txt`: copied text from ciru-ai's reproduction page at test time
- `ciru_chadrock_rocmfpx_page.html`: copied HTML from ciru-ai's reproduction page at test time
- `hf_model_card_README.md`: copied Hugging Face model card at test time
- `runner_commit.txt`: runner commit used
- `llama_server_version.txt`: `llama-server` build/version output
- `model.sha256`: local model sha256
- `server.log`: initial server log
- `response_gen512.json`: initial 3945-token response JSON
- `request_gen512_stdout.txt`: parsed initial 3945-token timing output
- `response_short_page.json`: short prompt response JSON
- `request_short_page_stdout.txt`: parsed short prompt timing output
- `repeat_t3_only/`: cleaned-repeat server log, response JSONs, and parsed timing outputs
- `pre_stop_state.txt`, `t3_only_pre_state.txt`, `restore_state.txt`: service-state notes before and after the cleaned repeat
