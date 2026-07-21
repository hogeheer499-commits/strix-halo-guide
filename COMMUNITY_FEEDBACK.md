# Community Feedback Loop

This guide treats community feedback as part of the evidence process, not only as promotion or traffic.

Technical readers often reject benchmark posts that feel too polished, promotional, or unsupported, even when the underlying measurements are real. That is useful feedback for this project: adoption friction is not only setup friction. It is also trust friction.

## What Trust Friction Looks Like

For local-AI hardware, buyers and developers are skeptical of:

- headline numbers without raw logs or commands
- model names without exact artifact and quant details
- server/speculative/API results mixed with direct `llama-bench` rows
- large-model claims that skip download size, sharding, backend, or memory limits
- marketing-style language around community results
- reposted benchmark summaries that do not preserve caveats

The guide should answer that skepticism with raw evidence, not with louder claims.

## How Feedback Changes The Guide

Community pushback should improve the public docs when it identifies a real gap.

The 2026-06-04 Nemotron discussion is a concrete example. The first framing compared Nemotron 3 Ultra with the already-tested Nano route, but skipped Nemotron 3 Super. That was a valid technical correction. Super 120B-A12B was then tested the same day and added as a direct Strix Halo GGUF route:

- `unsloth/NVIDIA-Nemotron-3-Super-120B-A12B-GGUF`
- `UD-IQ4_XS`
- `llama.cpp` Vulkan/RADV
- Ryzen AI MAX+ 395 / Radeon 8060S / 128 GB unified memory
- initial 2026-06-04 correction run, `pp512/tg128`, r3: 292.51 pp512 / 17.94 tg128
- initial 2026-06-04 correction run, `p0/tg128`, r3: 17.73 t/s generation-only
- 2026-06-05 latest/int-dot rerun, `pp512/tg128`, r3: 294.99 pp512 / 18.43 tg128

Raw evidence:
[`data/raw/2026-06-04/nemotron-3-super-120b-a12b-udiq4xs-direct-scout/`](data/raw/2026-06-04/nemotron-3-super-120b-a12b-udiq4xs-direct-scout/)
and
[`data/raw/2026-06-05/latest-llamacpp-intdot-regression/`](data/raw/2026-06-05/latest-llamacpp-intdot-regression/).

The corrected Nemotron map is:

- Ultra 550B-A55B: watchlist for one-box 128 GB Strix Halo until a practical local route exists.
- Super 120B-A12B: runnable middle route for capacity/current-model testing.
- Nano 30B-A3B: faster smaller route.

The 2026-07 Corsair thermal/SCLK report is a second example. The initial report associated sustained hard locks with stock clock behavior. Fail-Safe then supplied a strict three-system sweep, bounded stock controls, raw telemetry, and an analyzer. Historical journals subsequently showed that two systems had booted without the out-of-tree `ec_su_axb35` fan-control module after a kernel update, leaving dependent services failed.

The guide therefore does not call 2400 MHz a universal fix. It records it as the best conservative tradeoff measured on that fleet, keeps the root cause unresolved, adds a concrete post-update fan-service check, and tracks the resulting upstream fan-reset patch. See [`THERMAL_STABILITY.md`](THERMAL_STABILITY.md). The correction is more valuable to buyers and vendors than defending the first hypothesis would have been.

## Writing Rules From This Feedback

- Put artifact, quant, backend, and command context before broad interpretation.
- Link raw data as evidence, not as a call to action.
- Avoid asking for stars or promotion inside technical benchmark posts.
- Use plain engineering language instead of marketing language.
- Preserve corrections and negative results.
- Keep first-party, community, server/API, MTP/speculative, RPC, power, Windows, Linux, ROCm, and Vulkan/RADV claims separated.

## Vendor Value

This feedback loop is commercially useful because it exposes buyer trust friction in public. Vendors do not only need higher benchmark numbers; they need credible setup paths that technical buyers believe.

The guide's role is to turn skepticism into dated, reproducible evidence:

- what artifact exists
- what quant fits
- what backend runs
- what speed was measured
- what failed or remained watchlist-only
- what community correction changed the docs

That is the value proposition: independent public evidence that makes Strix Halo local-AI hardware easier to evaluate, trust, buy, support, and review.
