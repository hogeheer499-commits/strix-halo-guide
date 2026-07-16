# Controlled Ollama 0.31.1 / 0.31.2 / 0.32.0 Comparison

Date: 2026-07-16

System: Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S, 128 GB unified memory.

This run isolates the Ollama runtime version from service configuration. All
three versions used the same user-local port, model cache, Vulkan/RADV
environment, Qwen3.6 artifact, prompt, context, batch size, and single parallel
slot. The installed 0.31.2 system service remained unchanged and idle on port
11434.

## Controlled Environment

- model: `qwen3.6:35b-a3b` Q4_K_M, digest `07d35212591fc27746f0a317c975a6d68754fb38e9053d82e25f06057af28522`
- API: `/api/generate`, one cold plus nine warm requests per version
- request: 25 prompt tokens, 128 generated tokens, temperature zero, 2048 context
- `OLLAMA_NUM_PARALLEL=1`
- `OLLAMA_NUM_BATCH=512`
- `OLLAMA_VULKAN=1`
- `OLLAMA_IGPU_ENABLE=1`
- `HIP_VISIBLE_DEVICES=-1`
- `OLLAMA_FLASH_ATTENTION=1`
- explicit RADV ICD

Binary and release-archive hashes, host state, and the idle system-service state
are in [`host-snapshot.txt`](host-snapshot.txt).

## Result

| Ollama server | Cold generation | Warm mean | Warm range | Warm SD | Warm prompt mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0.31.1 | 71.41 t/s | 72.55 t/s | 72.36-72.66 | 0.12 | 876.92 t/s |
| 0.31.2 | 72.85 t/s | 73.19 t/s | 73.04-73.28 | 0.09 | 878.20 t/s |
| 0.32.0 | 72.87 t/s | 73.20 t/s | 72.84-73.40 | 0.20 | 886.00 t/s |

Under identical local-server conditions, 0.31.1, 0.31.2, and 0.32.0 are in the
same Qwen3.6 generation-performance class. The earlier normal-service 0.31.2
result of 60.57 t/s remains valid for that measured service run, but this
comparison shows it was not sufficient evidence of a version-wide 0.31.2
regression.

Ollama 0.32.0 fully offloaded Qwen3.6 (42/42 layers) to the Radeon 8060S. It
also passed a Qwen2.5-VL 7B vision smoke before and after a local-server process
restart: 29/29 language-model layers and the vision encoder used Vulkan, and
the model correctly read the guide title and 140.4 t/s number from the
repository social preview. A corrected post-restart Qwen request with thinking
disabled returned exactly `restart pass`.

This proves local-binary compatibility, iGPU offload, vision, and process
restart behavior. It does not claim a system-wide 0.32.0 package upgrade or
full-host reboot pass; the installed system service was deliberately not
changed during this controlled comparison.

## Evidence

- [`summary.json`](summary.json): repeat-aware version summary
- `0.3*.1-qwen-api-r10.csv`: per-request throughput and duration rows
- `0.3*.1-qwen-r*.json`: complete API responses
- `0.3*.1-server.log`: runtime, GPU discovery, offload, and request logs
- `0.3*.1-api-version.json`: server-reported versions
- `0.3*.1-ps.json`: model placement after the speed run
- [`0.32.0-vision-before-restart.json`](0.32.0-vision-before-restart.json)
- [`0.32.0-vision-after-restart.json`](0.32.0-vision-after-restart.json)
- [`0.32.0-qwen-after-restart-visible.json`](0.32.0-qwen-after-restart-visible.json)
- `0.3*.1-telemetry.csv` and matching `*.summary.json` files
- [`run-controlled-compare.py`](run-controlled-compare.py): exact harness

The initial post-restart request used a 16-token thinking budget and ended
before emitting a visible response. It is retained as
`0.32.0-qwen-after-restart.json`; the corrected visible-response check is the
one used for the restart conclusion.

The telemetry PPT field is `amdgpu` package telemetry, not measured wall power.
