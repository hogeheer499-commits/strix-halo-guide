# qwen3.6:35b-a3b beginner tag: old manifest versus current MTP manifest (2026-09-26)

**Question:** the README beginner row (~60 t/s, 2026-07-10) was measured on the
tag's earlier manifest `07d35212591f`. Since about 2026-08-24 the tag resolves
to an MTP build. What does a new user get today, and how much comes from MTP?

**Setup:** Beelink GTR9 Pro, kernel 7.0.0-31, Ollama 0.32.15 system service
(Vulkan/RADV). All three arms use the same harness as the Qwen3.8 route
(`benchmark.sh`: temperature 0, seed 42, 128 output tokens, 4096 context,
cold run plus nine warm repeats). This harness differs from the 2026-07-10
beginner-path harness, so compare the arms with each other, not with ~60 t/s.

| Arm | Tag (ID) | Draft parameter | Runner launch |
|---|---|---|---|
| old-07d352 | earlier manifest, kept as `qwen3.6:35b-a3b-measured-07d352` (`07d35212591f`) | none | no `--spec-type` |
| current-mtp | `qwen3.6:35b-a3b` (`096fdbd02fe6`) | `draft_num_predict 2` | `--spec-type draft-mtp`, `spec-draft-n-max 2` |
| current-nodraft | same blob with `PARAMETER draft_num_predict 0` (`Modelfile.current-nodraft`) | 0 | no `--spec-type` |

**Result (warm mean over nine repeats, min-max):**

| Arm | Generation t/s | Prompt t/s |
|---|---|---|
| old-07d352 | 70.25 (69.71-70.47) | 1127.82 |
| current-mtp | 74.51 (69.18-76.78) | 1067.71 |
| current-nodraft | 70.35 (69.59-71.04) | 987.05 |

**Scope and caveats:** routine measurement with a known background workload
(see `../qwen38-27b-ollama-03215-mtp-vs-nodraft/host-context.txt`). Draft
acceptance was not captured. With MTP the generated text varied between
repeats; without drafting it was identical across repeats.

**Conclusion:** on this workload the current MTP build gives a small gain
(about 6 percent) over the same blob without drafting, which matches the
earlier manifest. The beginner row's performance class still holds.
