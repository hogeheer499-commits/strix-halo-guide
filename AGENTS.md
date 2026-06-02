# AGENTS.md

Operational instructions for Codex agents working in this repository.

## Core Project Lens

`strix-halo-guide` is primarily an evidence-backed AMD Strix Halo / Ryzen AI MAX+ 395 local-AI setup and benchmark guide.

The project now also has a vendor / partner / sponsor-facing direction: benchmark work should show how the guide reduces adoption friction for AMD Strix Halo / Ryzen AI MAX+ local-AI hardware.

When the user asks "is er nieuws?", "updates?", "wat moeten we testen?", or anything similar, evaluate updates through two layers:

1. Technical value:
   - new models
   - new `llama.cpp`, Ollama, ROCm, Mesa, vLLM, driver, BIOS, or tooling changes
   - benchmark regressions or improvements
   - new blockers, fixes, or reproducibility risks

2. Adoption / commercial value:
   - what buyer uncertainty does this remove?
   - what setup friction does this reduce?
   - what vendor/OEM/reviewer/product question does this answer?
   - what evidence would make someone more confident buying, recommending, supporting, or reviewing the hardware?
   - what missing hardware, firmware, driver support, vendor contact, or community data is needed to prove the next thing?

Higher t/s is useful, but it is not the only priority. Treat benchmarks as the proof layer and vendor/partner/sponsor docs as the leverage layer.

## Documentation Style

- Write in clear, professional English.
- Keep the repo primarily useful to developers, buyers, and benchmark contributors.
- Keep vendor-facing language credible, independent, and evidence-based.
- Prefer links to existing evidence over duplicating long benchmark sections.
- Use TODO placeholders for missing stats, contact details, quotes, traffic, sponsors, or evidence.
- Preserve negative results, caveats, and failed paths.
- Do not make the README feel like an advertisement.
- Keep machine-specific workflow, local services, ports, account operations, and private maintainer procedures out of public docs.

## Do-Not-Invent Rules

- Do not invent benchmark numbers.
- Do not invent sponsors, vendor relationships, traffic, sales impact, testimonials, quotes, or endorsements.
- Do not invent contact names, prices, issue activity, or GitHub stats.
- Do not imply official AMD, Beelink, Framework, GMKtec, Corsair, Minisforum, or OEM endorsement unless explicitly documented.
- Do not turn a planned test, external rumor, or experimental route into a proven recommendation.

## Benchmark Claim Rules

- Do not invent benchmark numbers.
- Inspect current repo files before quoting numbers.
- Keep direct `llama-bench` results separate from server/API/MTP/speculative/concurrency results.
- Keep first-party Beelink results separate from community results.
- Link claims to raw data, CSVs, charts, or `data/headline_claims.csv` where possible.
- Preserve negative results and caveats.
- Do not turn experimental routes into proven recommendations.
- Do not claim official AMD/OEM endorsement unless documented.
- Keep wall-power, board-power, amdgpu `PPT`, and inferred efficiency claims separate.
- Keep Windows, WSL2, native Linux, ROCm, Vulkan/RADV, vLLM, MTP, RPC, and NPU claims scoped to the exact evidence.

## Disclosure Rules

- Disclose sponsored, loaned, gifted, affiliate, or early-access work near the relevant results.
- Vendors may correct factual errors, but they do not get editorial control over benchmark conclusions.
- Negative results stay if they are accurate.
- Community results remain separated from first-party results unless clearly validated and labeled.
- Sponsored work funds friction-removal and better public evidence; it does not buy positive coverage.

## Link And Update Expectations

- Link buyer-facing claims to evidence where possible: raw logs, CSVs, charts, `data/headline_claims.csv`, or topic docs.
- If a referenced path changed, adapt to the current repo state instead of preserving stale links.
- Update related docs when adding a new public-facing evidence category.
- Do not add headline claims unless the supporting data, raw evidence, chart or `n/a`, and caveats are known.

## Commercial Thesis

The guide reduces a major adoption blocker for AMD Strix Halo / Ryzen AI MAX+ local-AI hardware: buyers struggle to know which setup path, backend, model format, quantization, driver, and benchmark claims are reliable.

The vendor-facing framing is:

```text
I can produce independent, reproducible, public technical evidence that reduces adoption friction and helps buyers understand the value of your hardware.
```

Do not frame this as entitlement to hardware. Frame partner support as access to hardware, firmware, drivers, technical context, and campaign funding that enables better public evidence.

## Verification Checklist

Before finishing documentation or benchmark-claim work:

- Inspect current repo files before quoting numbers.
- Check that new relative Markdown links resolve.
- Run `python3 scripts/validate_repo.py` when appropriate.
- Confirm no unsupported benchmark numbers were added.
- Confirm no invented sponsors, traffic, testimonials, quotes, or endorsements were added.
- Confirm TODO placeholders are clearly marked.
- Confirm first-party, community, server/API, MTP/speculative, ROCm/vLLM, power, NPU, RPC, and cross-OEM claims remain separated.
- Confirm vendor-facing docs preserve independence and disclosure language.
