# Ollama 0.31.1 Qwen3.6 Buyer-Path Sanity Check

Purpose: check the current Ollama buyer path without changing the system-wide
Ollama install.

This was run with a user-local Ollama 0.31.1 binary on `127.0.0.1:11435`,
using the existing `/usr/share/ollama/.ollama/models` cache. The system-wide
Ollama service remained at 0.23.1 on port `11434`.

## Environment

- Hardware: Beelink GTR9 Pro / Ryzen AI MAX+ 395 / Radeon 8060S
- OS: Ubuntu 24.04-class measured setup
- Backend: Ollama API with Vulkan/RADV
- Local binary: `/home/hoge-heer/benchmark-tools/ollama-0.31.1/bin/ollama`
- Model: `qwen3.6:35b-a3b`
- Key environment:
  - `OLLAMA_VULKAN=1`
  - `OLLAMA_IGPU_ENABLE=1`
  - `HIP_VISIBLE_DEVICES=-1`
  - `OLLAMA_FLASH_ATTENTION=1`
  - `OLLAMA_CONTEXT_LENGTH=65536`
  - `AMD_VULKAN_ICD=RADV`
  - `VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json`
  - `OLLAMA_NUM_BATCH=512`
  - `OLLAMA_NUM_PARALLEL=1`

Important: without `OLLAMA_IGPU_ENABLE=1`, Ollama 0.31.1 discovered
`Radeon 8060S Graphics (RADV STRIX_HALO)` but dropped the integrated GPU and
fell back to CPU in the local server startup log.

## Result

| Route | Result | Evidence |
| --- | ---: | --- |
| Ollama 0.31.1 local binary, `qwen3.6:35b-a3b`, warm API generation | 71.82 t/s mean; 71.62-72.05 t/s range | [`ollama-qwen36-35b-a3b-0311-api-r10.csv`](ollama-qwen36-35b-a3b-0311-api-r10.csv) |

This is a buyer-path API sanity check, not a direct `llama-bench` headline.
It is directly useful because Ollama is the easiest local chat route for new
Strix Halo buyers.

## Files

- [`host-snapshot.txt`](host-snapshot.txt)
- [`server-start.log`](server-start.log)
- [`server-full.log`](server-full.log)
- [`ollama-ps-after.txt`](ollama-ps-after.txt)
- [`ollama-qwen36-35b-a3b-0311-api-r10.csv`](ollama-qwen36-35b-a3b-0311-api-r10.csv)
- [`summary.txt`](summary.txt)
