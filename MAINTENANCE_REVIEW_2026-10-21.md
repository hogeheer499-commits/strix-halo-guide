# Scoped maintenance review — October 21, 2026

This is a focused update of the beginner route, saved-output corrections and the
primary sources listed below. It is not a complete upstream/model/hardware audit,
a fresh installation, a new benchmark or a general security qualification.
The broad evidence-review date remains October 1, 2026; this update does not
reset its 21-day freshness check. Individual measurements keep their own dates.

## What changed

- The README starts with one complete beginner route: installation, a visible
  answer, a known-answer check, GPU/listener checks and optional browser chat.
  The existing October 14 VM and October 15 GPU/browser component records are
  included with their limits. The revised route still lacks end-to-end fresh
  native Strix Halo installation, recovery and full-host reboot acceptance.
- The Gemma 4 26B QAT speculative server profile is removed from practical
  recommendations after six saved coding outputs failed their tasks. Historical
  speed/raw evidence stays intact. This does not identify an MTP-only cause or
  judge the whole model family; see the [saved-output review](BEST_KNOWN_PROFILES.md#historical-throughput-sampled-coding-outputs-failed).
- The existing vLLM raw-version correction, merged K2 Horizon PR status and
  setup-mirror link correction are retained from the October 14 patch.

## Primary-source checks on October 21

| Source | Observation and consequence |
|---|---|
| [Ollama latest release](https://github.com/ollama/ollama/releases/tag/v0.40.7), published October 18 | Stable 0.40.7 is available, not qualified here. Its renderer/parser/template-source reporting helps record model identity. The fresh-install pin and historical measurements are unchanged. |
| [Ollama 0.40.7 scheduling source](https://github.com/ollama/ollama/blob/v0.40.7/server/routes.go) | The automatic compatibility-migration call remains commented out. Earlier 0.40.2 stores still need backup/identity/rollback review. |
| [Ollama 0.40.8-rc0](https://github.com/ollama/ollama/releases/tag/v0.40.8-rc0), published October 21 | Prerelease Flint notes explicitly say macOS support only and other GPU support later. No Strix Halo recommendation or AMD performance claim follows. |
| [Open WebUI advisory GHSA-3vvh-g22g-jq6r](https://github.com/open-webui/open-webui/security/advisories/GHSA-3vvh-g22g-jq6r), published October 18 | Channel webhook impersonation affects >=0.7.0,<0.12.2, including the component-tested 0.11.4 pin; patched in 0.12.2. The advisory requires enabled channels, a channel webhook and a member with write access; it says disabled channels or no channel webhooks are not affected. Keep those features off for this local single-user candidate. This mitigation is advisory guidance, not a new local test. |
| [Open WebUI 0.12.3](https://github.com/open-webui/open-webui/releases/tag/v0.12.3), published October 16 | Newer stable release observed; this guide has not qualified its install, migration or restore. No silent change to the tested digest. |
| [Ollama issue #17041](https://github.com/ollama/ollama/issues/17041) | Still open. This check does not establish a fixed release for CVE-2026-85180. Historical affected-range warnings stay. |
| [K2 Horizon PR #29535](https://github.com/ggml-org/llama.cpp/pull/29535) | Merged October 6, rechecked; no containing-release or local load qualification established. |
| [AMD Halo product page](https://www.amd.com/en/products/processors/desktops/ryzen/ryzen-ai-halo.html) and [October 12 introduction](https://www.amd.com/en/blogs/2026/meet-the-next-amd-ryzen-ai-halo.html) | AMD presents its own PRO 495/192GB platform. Vendor model-fit/performance statements are not this guide's measurements, an EU SKU or proof of delivery. |
| [GMKtec EU EVO-X5 Pro 495 listing](https://de.gmktec.com/en/products/gmktec-evo-x5-pro-ai-max-495) | Orders placed by October 15: expected dispatch at end of October. Orders from October 16: expected dispatch November 20–30. The seller explicitly distinguishes dispatch from delivery; no Dutch delivery or 192GB speed claim follows. |

The two requested Open WebUI advisory pages returned the same 100 records.
They were deduplicated; no complete-feed count or exhaustive security clearance
is claimed. The identified October 18 advisory was read at its individual URL.
Other firmware, runtimes, model releases, prices, community questions and OEM
SKUs were not comprehensively rechecked. Existing dated observations are not
promoted to current facts by this update.

## Publication and remaining acceptance

This review describes a local candidate. A guide commit/push, mirror publication,
release and canonical site deployment each retain their own approval and
verification steps. The canonical builder requires a clean guide commit; a dirty
candidate is not represented as an attributable production bundle.
