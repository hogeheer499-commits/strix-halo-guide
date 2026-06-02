# Maintainer Notes

This public file is intentionally limited to repository-maintenance guidance that is safe to publish. Machine-specific workflow, local service names, ports, account operations, credentials, and private maintainer procedures belong in ignored local notes such as `CONTEXT.md` or files under `local-scratch/`.

## Public Maintenance Scope

`strix-halo-guide` is an evidence-backed AMD Strix Halo / Ryzen AI MAX+ 395 local-AI setup and benchmark guide. The public docs should stay technical-first, reproducible, and independent.

When maintaining public documentation:

- Keep buyer/developer setup value primary.
- Keep vendor/partner/sponsor positioning secondary and evidence-based.
- Link benchmark claims to raw data, CSVs, charts, or `data/headline_claims.csv` where possible.
- Keep first-party results separate from community results.
- Keep direct `llama-bench` results separate from server/API/MTP/speculative/concurrency results.
- Preserve negative results, caveats, failed routes, and reproducibility risks.
- Do not invent benchmark numbers, traffic, sponsors, testimonials, contact names, endorsements, or sales impact.

## Recommended Public Context

For a new documentation pass, read:

1. `AGENTS.md`
2. `README.md`
3. `BENCHMARKS.md`
4. `REPRODUCIBILITY.md`
5. `data/README.md`
6. `COMMUNITY_RESULTS.md`
7. `SERVER_SHOOTOUT.md`
8. `BACKEND_CROSSOVER.md`
9. `ROCM_VLLM_BUGWATCH.md`
10. `SPONSOR_ROADMAP.md`

For local workstation continuity, use ignored local notes rather than public Markdown.

## Raw Evidence Hygiene

Before committing raw host-state or benchmark-environment captures, redact anything that is not needed to reproduce the benchmark:

- full process lists and unrelated command lines
- local home-directory paths that are not needed for reproduction
- local service health JSON
- VM UUIDs, MAC addresses, secret paths, browser profile paths, or private tokens

Keep benchmark-relevant facts such as timestamp, kernel, memory, tuned profile, driver, GPU device string, tool commit, model hash, exact command, and raw benchmark output.

## Validation

Run the lightweight repo checks before publishing docs or data updates:

```bash
python3 scripts/validate_repo.py
```

GitHub Actions runs the same validation on `main` pushes and pull requests.

## Community And Support Strategy

Keep community activity real and technical:

- Thank contributors clearly and credit their systems/results.
- Ask for exact next useful data: hardware, BIOS, kernel, Mesa/ROCm, backend, model, command, CSV/raw logs, power method, and failure notes.
- Leave open issues open only when they represent real unanswered benchmark questions.
- Treat slower, failed, or contradictory reports as useful evidence, not a branding problem.

Support, sponsorship, loaned hardware, affiliate links, or early-access software must not change benchmark conclusions. Disclose vendor involvement clearly and preserve independent findings.
