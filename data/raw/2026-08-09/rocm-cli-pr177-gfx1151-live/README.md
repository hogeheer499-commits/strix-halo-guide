# AMD rocm-cli PR #177 Strix Halo Live Qualification

First-party Beelink GTR9 Pro packaging qualification from 2026-08-09. This
tests ROCm `rocm-cli` PR #177 at commit
`8236118df07ce5720c35887cd2ceab204b4ea2c6`, which upgrades the delegated
Radeon Lemonade environment to 11.5.1.

## Result

- A fresh isolated root installed the Lemonade 11.5.1 engine and served the
  official `Qwen3-0.6B-GGUF` profile on Radeon 8060S without the released
  0.1.0 flattening/symlink workaround.
- The managed service reached `ready`, exposed an OpenAI-compatible local
  endpoint, returned 128 completion tokens, and stopped cleanly.
- The service log confirms the ROCm backend and Radeon 8060S. The single smoke
  request measured 865.77 prompt t/s and 259.48 decode t/s.
- This tiny-model number proves the managed path is live; it is not a buyer
  performance recommendation or a comparison with the guide's larger models.

## Remaining Friction Found

1. If `XDG_RUNTIME_DIR` points to a path that does not yet exist, engine setup
   fails. Creating the directory with mode 0700 makes the install proceed.
2. An absolute local GGUF path was treated as a registry/model identifier and
   returned a 404. The official named profile worked.
3. Upgrading an existing 10.10 isolated root installed 11.5.1 and removed the
   old packaging workaround, but the saved `preferred_env_id` and one CLI
   summary still showed 10.10 while the launched service manifest recorded
   11.5.1.

These are actionable packaging/UX caveats. They do not invalidate the fresh
11.5.1 success.

## Evidence Map

- `pr177-serve-official-11470.txt`: resolved plan and ready managed service.
- `pr177-services-after-serve.txt`, `service-manifest.json`, `pr177-stop.txt`:
  lifecycle proof.
- `pr177-external-response.json`: external OpenAI-compatible response.
- `service-readable.log`: device, backend, loading, and timing evidence.
- `config.json`, `audit-events.jsonl`, `cli-lifecycle.log`: isolated CLI state.
- `source-commit.txt`, `host-and-cli.txt`, `files.sha256`: provenance.
