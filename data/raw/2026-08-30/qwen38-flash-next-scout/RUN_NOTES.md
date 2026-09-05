# Qwen3.8-Flash-Next UD-IQ4_XS scout — 2026-08-30 (COMPLETE)

First first-party measurement of Qwen/Qwen3.8-Flash-Next (released
~2026-08-26; 125B / 6B active MoE plus publisher-listed 51B n-gram embeddings
and 4B MTP; the tested GGUF reports about 177B parameters; license **qwen-community-1.0, not
Apache 2.0**) on this Beelink GTR9 Pro. Artifact:
unsloth/Qwen3.8-Flash-Next-GGUF UD-IQ4_XS, 3 shards, ~93.7GB total
(hashes in ../artifact-sha256.txt). Downloaded 2026-08-30.

Stack, power protocol, deviations, and background load: identical to
../b10687-vulkan-sentinel/RUN_NOTES.md (same session, kernel 7.0.0-30,
b10687 `c841aee` Vulkan/RADV, performance profile, DPM auto).

## Results (llama-bench -fa 1 -ngl 999 -p 512 -n 128 -r 10 -o csv)

| Metric | Value |
|---|---|
| pp512 | 394.73 ± 3.63 t/s |
| tg128 | 27.16 ± 0.08 t/s |

## Correctness smoke

`llama-cli -ngl 999 -fa on --temp 0 -n 48 -st` with prompt "Answer with only
the number: what is 7*8?" produced a thinking block and the correct answer
`56` (qwen38-flash-next-correctness-smoke.txt). NOTE: the first smoke attempt
failed on rc=1 because `-no-cnv` no longer exists on b10687 (`-st` replaces
it); the successful rerun happened AFTER the power profile was restored, so
its reported 26.6 generation t/s is anecdotal context only — cite the r10
llama-bench row, not the smoke, for speed.

## Claim class

Single-quant, single-build scout on 10 repeats. Fit: ~94GB artifact loads and
runs on the 128GB machine with normal context. No long-context, tool,
vision, server, or quality claims. License caveat must travel with any
recommendation.
