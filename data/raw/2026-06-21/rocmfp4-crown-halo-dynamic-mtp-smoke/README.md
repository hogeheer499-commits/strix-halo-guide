# ROCmFP4 Crown Halo Dynamic MTP Smoke

Date: 2026-06-21

Purpose: test whether the current `jcbtc/qwen3.6-35b-a3b-crown-halo-mtp-dynamic` ROCmFP4/MTP artifact can be loaded and served on the guide's Beelink GTR9 Pro / Ryzen AI MAX+ 395 system.

This is not a direct `llama-bench` headline result and not a reproduction of ciru-ai's highest community numbers. It is first-party loadability and server/API smoke evidence for the advanced ROCmFP4 / CHADROCK lane.

## Route

- Model repo: `jcbtc/qwen3.6-35b-a3b-crown-halo-mtp-dynamic`
- Model file: `Qwen3.6-35B-A3B-HaloStrix-Dyn-MTP-v7.gguf`
- Model size: about 21.0 GiB
- Model sha256: `342e3ee059792dbcba016dc3274a2de73a2372c0ea300a8e56aa615190f58ba9`
- mmproj file: `mmproj-F16.mmproj`
- mmproj sha256: `8971ee4f331ff0a4c609374f32984b3d4e6dc086c0aa35f1d637fad1829e887f`
- Runtime tree: `charlie12345/rocmfp4-llama`
- Runtime commit: `4795079b0`
- Build used here: HIP-only Distrobox build through the existing `vllm-gfx1151` / TheRock-style container
- Device: `ROCm0` / Radeon 8060S Graphics

The host Ubuntu environment did not have the ROCm SDK libraries in the normal shell path. The route was run through `distrobox enter vllm-gfx1151 -- bash -lc ...`, where `/opt/rocm/lib` and the gfx1151 ROCm libraries are available.

## Results

| Run | API | Context | Spec | Result | Read |
| --- | --- | ---: | --- | ---: | --- |
| Short prompt | `llama-cli` | 4096 | `draft-mtp`, `n-max 4`, f16 main/draft KV | 133.6 pp / 72.2 gen t/s | Works; faster than no-spec on this prompt. |
| Short prompt no-spec | `llama-cli` | 4096 | none | 235.7 pp / 52.4 gen t/s | Baseline for the short prompt. |
| Long structured prompt | `llama-cli` | 16384 | `draft-mtp`, `n-max 4`, f16 main/draft KV | 1071.9 pp / 51.1 gen t/s | Long prompt runs, but MTP gain is small in this local HIP-only path. |
| Long structured prompt no-spec | `llama-cli` | 16384 | none | 1334.9 pp / 49.9 gen t/s | Baseline for the long prompt. |
| Short prompt | `llama-server`, `-sm none`, `--no-mmap` | 16384 | `draft-mtp`, `n-max 4`, f16 main/draft KV | 55.33 pred t/s, 71/160 draft tokens accepted | Server/OpenAI-compatible API smoke. |
| Long structured prompt | `llama-server`, `-sm none`, `--no-mmap` | 16384 | `draft-mtp`, `n-max 4`, f16 main/draft KV | 57.61 pred t/s, 168/344 draft tokens accepted | Best long server row in this smoke. |
| Short prompt | `llama-server`, `-sm row`, mmap | 16384 | `draft-mtp`, `n-max 4`, f16 main/draft KV | 60.66 pred t/s, 76/152 draft tokens accepted | Slightly better short server variant. |
| Long structured prompt | `llama-server`, `-sm row`, mmap | 16384 | `draft-mtp`, `n-max 4`, f16 main/draft KV | 52.01 pred t/s, 159/384 draft tokens accepted | Did not beat the `-sm none` / `--no-mmap` long row. |

An attempted 8192-context long prompt was rejected cleanly because the request had 8587 prompt tokens. This is useful setup evidence: the long prompt needs a larger context setting.

## Interpretation

This route is valuable because it proves the dynamic Crown Halo GGUF can load and run with native MTP on the guide's Beelink system through the ROCmFP4 fork. It also exposes the current reproduction gap:

- ciru-ai's latest community update reports much higher dynamic-MTP decode/acceptance behavior on their stack.
- This first-party Beelink smoke did not reproduce that speed band.
- The most likely differences are runtime profile, Vulkan versus HIP-only ROCm path, dynamic runner policy, host/container stack, prompt shape, or exact patched runner state.

For guide purposes, this should be treated as:

- first-party ROCmFP4 loadability evidence
- first-party server/API smoke evidence
- a useful advanced-lane blocker/repro target
- not a new public speed headline
- not a replacement for the default `setup.sh` / Ollama / Vulkan-RADV beginner path

## Files

- `host-and-model-snapshot.txt`: host, repo, runtime commit, file size, and hashes
- `container-runtime-snapshot.txt`: container runtime and device snapshot
- `command-*.sh`: exact local commands used
- `llama-cli-*.stdout.log`: CLI raw output
- `llama-server-*.log`: server raw logs
- `server-*.response.json`: OpenAI-compatible API response and timing metadata
- `hf-card-README.txt`: copied Hugging Face model card text at test time
- `hf-recipe-halo-mtp-dyn-v7.md`: copied model recipe
- `hf-model-profile.env`: copied model profile
- `hf-serve-script.sh`: copied model serving script
