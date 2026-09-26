# Active-evidence review — September 26, 2026

This review covers **active recommendation surfaces** after an independent audit
(checked 2026-09-25). It is not a remeasurement date: no new hardware
measurement was taken, and historical results keep their own dates.

## What changed on active surfaces

| Surface | Decision |
|---|---|
| Qwen3.8 Ollama route (README, QWEN38 page, profiles, headline CSVs, models hub) | Numbers unchanged; relabelled as an Ollama API result with Ollama-default MTP drafting (`draft_num_predict 4`). Requires Ollama 0.32.12+. A matched no-draft control is queued. |
| Beginner `qwen3.6:35b-a3b` row | Tied to its measured manifest; the tag now resolves to an MTP build that is not yet measured (queued). |
| Setup (`setup.sh`, setup pages, troubleshooting) | OS guard, 128GB-class upper bound, unpinned-`main` disclosure, firmware check on `linux-firmware-amd-graphics`, identical recorded boot profile, undo section. Fresh-install qualification remains open. |
| Security (`SECURITY.md`) | Dated advisories for pinned Ollama and Open WebUI versions, lookalike-repository warning, canonical site, private reporting route. |
| Upstream snapshot, models hub, test queue | Dated 2026-09-25 availability; availability does not upgrade measurements. |
| Buyer page and vendor pages | Announced PRO 400-series hardware marked unmeasured; dated Apple/NVIDIA/EU context; per-OEM coverage; dated star snapshot; private-first contact route. |

## What this date does not certify

No fresh install, reboot, new benchmark, wall-power or noise measurement, and
no remeasurement of historical archives. Summary-only figures in
`RUNTIME_QUALIFICATION_2026-09-19.md` remain summary-only.
