# Active-evidence review — October 1, 2026

This review covers **active recommendation surfaces** after a review of those
surfaces (sources checked 2026-09-30). It is not a remeasurement date: no new hardware
measurement was taken, and historical results keep their own dates. The reviews
of [2026-09-19](ACTIVE_EVIDENCE_REVIEW_2026-09-19.md) and
[2026-09-26](ACTIVE_EVIDENCE_REVIEW_2026-09-26.md) are unchanged and keep their
original wording.

## What changed on active surfaces

| Surface | Decision |
|---|---|
| Qwen3.8 Ollama route (README, [QWEN38 page](QWEN38_STRIX_HALO.md) and web mirror, profiles, headline CSVs, route matrix, share text, test queue) | The "matched no-draft control is queued" wording was replaced by the measured result of 2026-09-26: 12.89 t/s without drafting versus 22.71 t/s with default MTP on Ollama 0.32.15 ([raw data](data/raw/2026-09-26/qwen38-27b-ollama-03215-mtp-vs-nodraft/)). The 20.42 t/s result stays an Ollama-default MTP result on 0.32.13. An artifact is identified by its model-blob digest next to the manifest ID. |
| MTP and benchmark data ([`data/mtp_speculative.csv`](data/mtp_speculative.csv), [`data/benchmarks.csv`](data/benchmarks.csv)) | Ollama API rows added from the raw bundles; `data/benchmarks.csv` gained `speculation` and `evidence_class` columns. Rows whose speculation setting is not documented say `unknown`. |
| Labels and 30B-class scout | The b11146 re-check is named a controlled re-check (not a fully idle host); "latest control" labels carry dates; routine scout rows for three 30B-class models are in [`CURRENT_MODELS.md`](CURRENT_MODELS.md). |
| Upstream state ([`data/public_state.json`](data/public_state.json), [bugwatch recheck](ROCM_VLLM_BUGWATCH.md#2026-09-30-upstream-recheck), [test queue](data/current_test_queue.csv), [raw-folder index](data/README.md)) | One field per question for Ollama and llama.cpp: latest stable Ollama 0.34.4 (checked 2026-09-30; GitHub listed 0.35.0 as the latest release on 2026-10-01, unqualified here; 0.34.2 labelled previous), llama.cpp b11265 as availability and b11146 as the latest local measurement. The recheck lists the Ollama 0.35 releases, llama.cpp changes, Lemonade, security bulletins and new test targets; availability does not upgrade any measurement. |
| Security ([`SECURITY.md`](SECURITY.md), new [`SECURE_LOCAL_AI.md`](SECURE_LOCAL_AI.md), setup commands, RPC, USB4 and Unsloth pages, [troubleshooting](docs/troubleshooting.md)) | Dated advisory status for the pinned components; a checklist for network exposure, shared servers, community recipes, containers, clusters, SSH, RAG and agents, and firmware, with public sources and a "what we did not test" section. Commands that gained flags or steps say where the flag comes from and that it is not tested here. |
| Setup pages | Links to the security pages; memory-limit, CPU-model, kernel and NPU notes with dates; no change to the qualified install path. |
| Buyer pages ([web comparison](docs/best-strix-halo-mini-pc.md), [snapshot](BUYER_SNAPSHOT_2026-10-01.md), [CSV](data/buyer_price_snapshot_2026-09-30.csv), [use cases](BUYER_USE_CASES.md)) | Storefront observations of 2026-09-30 with country, currency and tax status per row; the first Ryzen AI Max PRO 495 (192GB) listings, none measured here; a 128GB-or-192GB section; European buying notes with seller terms as the store pages state them; per-vendor BIOS update routes. Earlier snapshots stay historical. |
| Model hub and new pages ([`docs/models.md`](docs/models.md), [`ENGINES.md`](ENGINES.md), [`WINDOWS_START.md`](WINDOWS_START.md), [`LAPTOPS_AND_HOMELAB.md`](LAPTOPS_AND_HOMELAB.md)) | Third-party capability scores are shown next to fit on one box and labelled as such; engines, Windows and laptop/homelab pages collect community and vendor sources and say what this guide did not verify. A coding-speed row is no longer described as a coding-quality ranking. |
| Vendor pages ([partnership scope](PARTNERSHIP.md), [one-page brief](ONE_PAGE_BRIEF.md), [proof summary](VENDOR_PROOF_SUMMARY.md), [disclosure](VENDOR_DISCLOSURE.md), [traction](TRACTION.md)) | Dated scope and version lines; a record of the corrections of 2026-09-26; [How We Work With Vendors](VENDOR_DISCLOSURE.md#how-we-work-with-vendors) (correction route, negative results stay); a dated list of where the data is reused. |
| Contributor surface (README section [Reuse And Citing The Numbers](README.md#reuse-and-citing-the-numbers), [`CONTRIBUTING.md`](CONTRIBUTING.md), issue and pull-request templates, CI workflows) | Headlines are listed with the qualification that must travel with them; the templates ask for memory speed, visible RAM and GTT size; the tests are documented as needing Linux or WSL; the benchmark-cleanliness script no longer writes listening-port or process dumps. |

## What this date does not certify

- No fresh install, reboot or new benchmark, and no remeasurement of historical
  archives. Summary-only figures in `RUNTIME_QUALIFICATION_2026-09-19.md` remain
  summary-only.
- No own measurement of wall power or noise. Electricity examples are
  assumptions or third-party idle figures, not measurements of this guide's
  hardware.
- Prices, stock and versions are observations of 2026-09-30 (storefronts) and
  2026-09-30 (upstream availability). They are seller listings, not delivered
  checkout quotes, and they can change. After that check, GitHub's
  latest-release endpoint returned Ollama 0.35.0 on 2026-10-01; nothing else in
  the upstream recheck was repeated.
- Claims of third parties (community benchmark reports, forum and issue threads,
  vendor statements, press reviews, published advisories and bulletins) were read
  and dated, not reproduced here.
- The findings about HP, Framework and GMKtec pages are what the stores' pages
  showed on the observation date, not a statement about the companies; terms and
  prices can change.
- Security steps marked "not tested here" have not been tested on this guide's
  hardware.
- Ryzen AI Max PRO 495 / 192GB systems, Windows routes, community engines and
  the new test-queue rows are not measured or qualified here.
