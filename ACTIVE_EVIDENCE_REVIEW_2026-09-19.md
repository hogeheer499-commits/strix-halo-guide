# Active-evidence review — September 19, 2026

This review covers **active recommendation surfaces**, their source boundaries
and consistency. It is not a remeasurement date for historical benchmarks and
not a claim that every archived log was reread or every upstream issue retested.

## Reviewed surfaces and decisions

| Claim category / consumers | Review and resulting boundary |
|---|---|
| README Quick Start, installer/manual setup, FAQ and troubleshooting; `STRIX_HALO_LOCAL_LLM_SETUP.md`; `docs/amd-strix-halo-setup.md` | Read active guidance and installer behavior. Preserve 128GB-only automation scope, legacy-configuration holds, optional power policy, native-gfx1151/HSA distinction and fresh-install qualification caveat. Historical kernel/driver snapshots are not current host requirements. |
| `CURRENT_MODELS.md`, `BEST_KNOWN_PROFILES.md`, profile CSV and model hub | Separate historical speed profiles, current available releases and scoped functional qualification. Qwen3.6 text is not Qwen2.5-VL vision. Available 0.34.2 was not promoted without official Qwen3.8 and normal upgrade/reboot acceptance. |
| `QWEN38_STRIX_HALO.md`, Qwen page and route matrix | Historical official Ollama 0.32.13, external patched-HIP 96GB GMKtec, MTP/DFlash and unqualified leads remain separate. The 50,059-token pass and recoverable 56,051-token failure are exact-stack evidence, not universal context limits. New candidate Qwen3.8 remains open. |
| `ROCM_VLLM_BUGWATCH.md`, active test queue and troubleshooting | Released v0.4.1 CLI contract and bounded HIP correctness controls now have local evidence. Retain historical failures, unresolved large-memory accounting and model-specific limits. Older dated release/issue sections are not silently re-dated. |
| `data/headline_claims.csv`, `BENCHMARKS.md`, `REPRODUCIBILITY.md`, README/site headline consumers | Checked claim identity, model/quant, direct versus API/server/speculative categories and linked structured/raw provenance. No new headline performance claim. AgentWorld's disputed retained-run rate is withheld in active summaries rather than choosing a new number without provenance. Historical raw numbers remain unchanged. |
| README buyer guidance, buyer page and new storefront snapshot | New primary-store observations separate SKU, RAM/SSD, region/currency, available variant versus dispatch, and complete system versus board/laptop. Old prices, delivery banners and unavailable exact quotes are not promoted. No unmatched best-value/support ranking. |
| `SYSTEM_EVIDENCE_MATRIX.md`, system CSV and coverage consumers | Preserve 10 described owner systems + 3 independently attributed external sources. Coverage is not 13 matched reproductions. GMKtec community/external evidence is not a first-party current-retail-SKU test. |
| `PARTNERSHIP.md`, `ONE_PAGE_BRIEF.md`, `SERVICES.md`, vendor summary and disclosure | Independent technical outcomes and service scopes, no invented sales/conversion/support reduction. Account-specific affiliate terms unresolved; no links activated, no new vendor relationship implied. Existing service prices are not hardware-storefront prices. |
| Canonical builder's home/evidence/partners templates; setup/buyer/models/Qwen/troubleshooting/services sources; public-state metadata | Same existing builder/deployment route. Synchronize scoped results, revision and review date without redesign, new infrastructure, endorsements or private logs. Deployment verification is separate from content review. |

## New evidence considered

- [Existing-user and isolated runtime qualification](RUNTIME_QUALIFICATION_2026-09-19.md):
  exact-output tests, genuine tool execution, pinned client, service/process
  restart, LAN reachability, direct/server split and historical/released HIP controls.
- [September 19 storefront snapshot](BUYER_SNAPSHOT_2026-09-19.md): primary
  seller observations, unresolved selected quotes and public program context.
- Existing structured claims, linked campaign summaries and relevant retained
  results were used to preserve their measurement scope. Full private campaign
  captures remain private; public summaries do not expose account operations.

## What this date does not certify

No fresh install, new full-host reboot, broad quality evaluation, wall-power
campaign, exact-SKU GMKtec reproduction or general HIP/Qwen3.8 capacity test was
performed. Historical raw archives, old storefront snapshots, external traffic
statistics and every model-card listing were not remeasured or wholesale
recaptured. Their individual dates, negative results and caveats remain.

`evidence_reviewed = 2026-09-19` means this active-surface/source-scope review.
It does not turn the June/July/August measurements into September results or
the deployment timestamp into a hardware evidence date. Future reviews should
revisit changed high-risk claims and stale dated offers; publication alone must
never refresh this field.
