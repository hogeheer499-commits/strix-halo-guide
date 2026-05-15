# 2026-05-16 isolated Ollama 0.24.0 API check

Purpose: test the latest Ollama binary without replacing the installed 0.23.1 service.

Setup:

- Isolated server on `127.0.0.1:11435`
- Shared existing model store
- `OLLAMA_VULKAN=1`
- `HIP_VISIBLE_DEVICES=-1`
- `OLLAMA_FLASH_ATTENTION=1`
- `OLLAMA_CONTEXT_LENGTH=65536`
- `OLLAMA_NUM_BATCH=512`
- `OLLAMA_NUM_PARALLEL=1`

Result for `qwen3.6:35b-a3b`, 10 warm `/api/generate` runs:

| Version | Prompt tokens | Prompt eval | Warm generation | Read |
|---------|--------------:|------------:|----------------:|------|
| 0.24.0 isolated | 25 | 187.66 t/s | 49.05 t/s | No speedup. |
| 0.23.1 installed control | 25 | 188.29 t/s | 49.09 t/s | Same-prompt control. |

The isolated 0.24.0 server was stopped after the test.
