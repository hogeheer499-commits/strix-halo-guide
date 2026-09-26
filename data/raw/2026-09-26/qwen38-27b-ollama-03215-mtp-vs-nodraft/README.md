# Qwen3.8 27B Ollama: default MTP versus matched no-draft control (2026-09-26)

**Question:** how much of the published 2026-08-15 Qwen3.8 Ollama result
(20.42 generation t/s) comes from Ollama-default MTP drafting?

**Setup:** Beelink GTR9 Pro, kernel 7.0.0-31, Ollama 0.32.15 system service
(Vulkan/RADV), same prompt, options and nine-warm-repeat harness as
`data/raw/2026-08-15/qwen38-27b-ollama-03213-vulkan-radv/benchmark.sh`
(temperature 0, seed 42, 128 output tokens, 4096 context).
Both tags use the same model blob `f5f1dd8920d4`:

| Arm | Tag (ID) | Draft parameter | Runner launch |
|---|---|---|---|
| no-draft | `qwen3.8:27b-q4_K_M` (`25b843619e94`) | none | no `--spec-type` |
| mtp | `qwen3.8:27b-mtp-q4_K_M` (`22130167c4c2`, the 2026-08-15 artifact) | `draft_num_predict 4` | `--spec-type draft-mtp`, `spec-draft-n-max 4` |

**Result (warm mean over nine repeats, min-max):**

| Arm | Generation t/s | Prompt t/s |
|---|---|---|
| no-draft | 12.89 (12.87-12.90) | 384.66 |
| mtp | 22.71 (22.46-22.89) | 360.01 |

**Scope and caveats:** routine measurement, not strict-clean: a known
background workload (a VM, a remote-access agent and other light processes,
see `host-context.txt`) was running for both arms. Ollama 0.32.15, not the
0.32.13 of the original run. Each arm's output was identical across its own
warm repeats, but the two arms produced different text, so MTP output
equivalence at temperature 0 is not established here. Draft acceptance was
not captured.

**Conclusion:** the published Ollama Qwen3.8 route is an MTP result. On this
stack the same blob gives 12.89 generation t/s without drafting and 22.71 t/s
with Ollama-default MTP.
