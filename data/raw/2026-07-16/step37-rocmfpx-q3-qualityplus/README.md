# Step 3.7 Flash ROCmFPX Q3 QualityPlus Reproduction

First-party Beelink GTR9 Pro reproduction of a 198B-total, approximately 11B-active Step 3.7 Flash target plus its separate MTP draft on one 128GB Strix Halo system.

This is `llama-server` capacity, agent, and speculative-decoding evidence. It is not a direct `llama-bench` result and does not replace the direct Qwen speed headlines.

## Result

| Profile | Prompt tokens | Repeats | Decode | Prompt processing | Draft acceptance |
| --- | ---: | ---: | ---: | ---: | ---: |
| No-spec baseline | 4,109 | 3 | 23.84 t/s mean; 23.71-24.05 | 409.77 t/s mean | n/a |
| MTP | 4,109 | 3 | 34.50 t/s mean; 34.04-35.27 | 360.64 t/s mean | 100.00% |
| MTP | 16,401 | 3 | 33.83 t/s mean; 33.80-33.86 | 334.86 t/s mean | 99.61% |
| MTP | 49,175 | 1 | 28.06 t/s | 261.21 t/s | 97.56% |

The 4K MTP profile is 44.68% faster than the matched no-spec server baseline. The target and draft also allocated a full 262,144-token context, and the native tool-call smoke returned the requested `terminal` call with the exact `printf step37-ok` argument.

The 256K result is an allocation proof, not a filled-256K prompt or quality benchmark. The 48K row has one repeat and should be treated as a long-context scout rather than a repeat-confirmed headline.

## Pinned Sources

- Target: `jcbtc/Step-3.7-Flash-ROCmFPX-Q3-QualityPlus`
- Target revision: `fa311ca5a82bf82a2338151c4790e3f659abd88d`
- Draft: `notSnix/Step-3.7-Flash-MTP-Draft-GGUF`
- Draft revision: `c7bc8526b2b7004ce045112edebdf13a9eceb7eb`
- Runner: `ciru-ai/ROCmFPX` commit `221402af8574faf652b101b6afe225a3f329561f`
- Runner version: build 36 (`221402a`)
- Target footprint: 87.79 GB / 81.76 GiB
- Target plus draft and templates: 91.51 GB / 85.22 GiB

Hashes are stored in `target-shards.sha256`, `draft.sha256`, and `template.sha256`. Exact commands are stored in the `*.command.txt` files.

## Measured System

- Beelink GTR9 Pro
- AMD Ryzen AI MAX+ 395 / Radeon 8060S
- 128GB unified memory
- Ubuntu 24.04, kernel 6.19.4
- Mesa/RADV 26.1.4
- ROCmFPX target and draft served on `Vulkan0`
- Q8_0 KV cache, one server slot, flash attention

See `host-snapshot.txt` for the captured host, Vulkan, and HIP metadata.

## Evidence Map

- `summary.json`: per-profile aggregate results
- `rows.json`: every measured request and repeat
- `*.request.json` / `*.response.json`: exact API inputs and outputs
- `tool-smoke.response.json`: native tool-call output and timings
- `mtp-256k-allocation-proof.json`: reported 262,144-token context and target metadata
- `*.server.log`: server load, memory, and timing evidence
- `source-revisions.txt`: pinned model and runner revisions
- `download-and-run.sh` / `run-repro.py`: reproducible download and measurement harness

## Validation Note

An initial harness attempt revealed that terminating the outer container command could leave the inner server process alive. Those derived measurements were discarded before publication. The committed harness now kills any server already bound to the test port, uses a distinct alias for every profile, verifies the reported model ID before each request, and stops the child server explicitly. All results above come from the corrected rerun.

## Practical Read

The important buyer result is not only speed. A current 198B sparse agent model, separate MTP draft, useful long-context headroom, and native tool calling all fit on one 128GB Strix Halo box. The tradeoff is an advanced, pinned ROCmFPX path rather than the beginner Ollama/default-llama.cpp route.
