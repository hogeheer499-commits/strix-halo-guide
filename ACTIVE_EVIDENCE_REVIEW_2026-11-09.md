# Active-evidence review — November 9, 2026

This is a new review of **active recommendation surfaces**, following the
[October 1 broad review](ACTIVE_EVIDENCE_REVIEW_2026-10-01.md) and the
[November 8 scoped maintenance review](MAINTENANCE_REVIEW_2026-11-08.md).
Public sources below were read again on **2026-11-09**. No hardware measurement,
installation, runtime upgrade or reboot was performed. Earlier reviews and
measurements keep their original dates.

The main changes are newly published security reports affecting older runtime
pins, refreshed upstream availability, and explicit limits on buyer and
third-party context that could not be renewed. No newly qualified runtime,
model or system replaces the measured routes.

## What changed on active surfaces

| Surface | Review and decision |
| --- | --- |
| README and Qwen route, including web mirrors, profiles, benchmarks, reproducibility and share text | Reconciled current review/availability labels with `data/public_state.json`. Kept the measured 0.32.13 Qwen route, 0.32.15 matched MTP/no-draft control, manifest/blob identities, context failure, output caveats and 0.31.2 historical reboot baseline. No measured CSV or headline number changed. README structure is unchanged. |
| [Model hub](docs/models.md), [current models](CURRENT_MODELS.md), [engines](ENGINES.md) | Read the RAM/task card against the linked August 15 retrieval record and publisher manifest/pinned trees. MiMo model/projector digests and sizes and Bolt/Super VL sizes still match the November 8 observations. File size remains distinct from usable RAM and task acceptance. September capability scores are explicitly stale; older engine comparisons and vendor claims retain their own dates. No new quality, fit or engine qualification. |
| [Upstream state](ROCM_VLLM_BUGWATCH.md#november-9-2026-broad-recheck), [state record](data/public_state.json), [queue](data/current_test_queue.csv) | Official feeds: Ollama 0.40.15, llama.cpp semantic v0.9.0 and numbered prerelease b12211, Lemonade v2026.45.3, WebUI 0.13.3, rocm-cli stable v0.2.1, vLLM stable 0.32.0 plus 0.33.0rc3 candidate, SGLang 0.5.23. ROCm/ROCm's latest repository release remains 7.14.0 while AMD's current Core SDK notes describe 10.1.0; those are separate release states. Mesa's official notes list 26.2.6 (October 28). Availability does not upgrade qualification. |
| [Security](SECURITY.md#november-9-2026-recheck), [start route](LOCAL_CHAT_START.md), setup and troubleshooting | Re-read repository advisories, NVD keyword results/named records, AMD RCCL/driver bulletins and upstream PR states. Added newly published Ollama pull-API path traversal/SSRF and llama.cpp parser, GGUF, sampler, Pocket-TTS and RPC reports, with affected ranges and limits. Repeated WebUI 0.11.4 channel-webhook conditions, unresolved tensor-redirect and cache-leak reports. AMD corrected its old AMD-SB-6033 product-table CVE mismatch October 6. Functional acceptance is not security clearance. Profiles now point to October 15's limited WebUI 0.11.4 component check instead of calling historical 0.10.2 the only qualified image. |
| [Buyer page](docs/best-strix-halo-mini-pc.md), README buying context, dated snapshots | Framework returned 403; selected Beelink, GMKtec and Minisforum EU pages returned 429: stock, prices and dispatch claims are **not rechecked**. Corsair US CS-9080003-NA was readable and said out of stock; its comparison card prices CS-9080002-NA, so the exact-SKU price remains unresolved. Kept the September 30 broad snapshot and November 8 three-listing observations dated, adding the access warning beside active buyer guidance. No checkout/delivered quote. |
| [Partnership](PARTNERSHIP.md), [brief](ONE_PAGE_BRIEF.md), [proof](VENDOR_PROOF_SUMMARY.md), [disclosure](VENDOR_DISCLOSURE.md), [traction](TRACTION.md) | Read all five against existing technical scope/corrections and the repository API: **371 stars / 27 forks**, November 9. Updated the three copies and state record. Corrected the proof page's obsolete snapshot link and clarified that later HIP-report closure as not planned is not a fix. Affiliate registry remains header-only; a URL-pattern scan of active Markdown/data found no affiliate tracking destinations. Historical relationship, contributor/coverage and reuse observations are not newly recertified. No new commercial outcome or endorsement. |

## What this date does not certify

- No fresh install, full-host reboot, runtime replacement, restore, model
  download, benchmark, wall-power/noise measurement or task-quality test.
  Historical functional acceptance and raw measurements remain dated evidence.
- No blanket security clearance. NVD keyword searches and repository feeds have
  different coverage. WebUI pagination repeated IDs; a global affected-version
  query returned zero despite a directly readable advisory including 0.11.4.
  A complete current advisory census was not possible. The October 2 count is
  historical. No exploit was run. CERT.PL's CVE-2026-103663 page returned 403;
  the report is attributed to the NVD record.
- No new broad price snapshot. `storefront_observed` remains 2026-09-30: one
  readable exact-SKU page does not renew the market comparison. November 8's
  192GB text is not a November 9 confirmation. Order, dispatch and delivery
  remain separate questions.
- No comprehensive renewal of September capability leaderboards, their model
  availability cells, community-engine claims, external listings/reuse,
  firmware/BIOS, Windows/NPU routes or historical news. They remain dated
  context, not current rankings or a claim that nothing changed.
- No 32/64/96/192GB setup profile or new OEM qualification. RAM-card candidates
  remain untested; capacity arithmetic is not a completed task.
- No private relationship verification, attributable sales, conversion,
  support-cost reduction or endorsement. Public counts and an empty registry
  establish only what was inspected in this repository.
- No deployment is established by this report. The canonical site requires its
  own build, authorized deploy and full live verification. Repository CI is
  separate from runtime/hardware qualification.

## Sources read November 9, 2026

| Primary source | What was read / access limit |
| --- | --- |
| [Ollama](https://api.github.com/repos/ollama/ollama/releases), [llama.cpp](https://api.github.com/repos/ggml-org/llama.cpp/releases), [Lemonade](https://api.github.com/repos/lemonade-sdk/lemonade/releases), [ROCm](https://api.github.com/repos/ROCm/ROCm/releases), [WebUI](https://api.github.com/repos/open-webui/open-webui/releases) | Official repository feeds/latest endpoints using the GitHub API; semantic and numbered releases separated. |
| [rocm-cli](https://api.github.com/repos/ROCm/rocm-cli/releases), [vLLM](https://api.github.com/repos/vllm-project/vllm/releases), [SGLang](https://api.github.com/repos/sgl-project/sglang/releases), [AMD Core SDK](https://rocm.docs.amd.com/en/latest/about/release-notes.html), [Mesa 26.2.6](https://docs.mesa3d.org/relnotes/26.2.6.html) | Release metadata/official documentation, not local acceptance. Mesa was read on its official documentation site, not an unofficial GitHub mirror. |
| [NVD API](https://services.nvd.nist.gov/rest/json/cves/2.0), [named CVEs and upstream PRs](SECURITY.md#november-9-2026-recheck) | Keyword queries `Ollama`, `llama.cpp`, `Open WebUI`, `ROCm`, 2,000-record page limit, all returned matches within one response (46/50/180/4); plus named records and linked PR states. Not an exhaustive dependency audit; unrelated matches excluded from pin discussion. |
| [Ollama advisories](https://github.com/ollama/ollama/security/advisories), [llama.cpp](https://github.com/ggml-org/llama.cpp/security/advisories), [WebUI](https://github.com/open-webui/open-webui/security/advisories), [ROCm](https://github.com/ROCm/ROCm/security/advisories), [named WebUI advisory](https://github.com/open-webui/open-webui/security/advisories/GHSA-3vvh-g22g-jq6r) | Repository advisory APIs: 13 llama.cpp entries, zero Ollama/ROCm entries, incomplete WebUI pagination. Zero entries is not absence of vulnerabilities. Named WebUI range/preconditions re-read directly. |
| [AMD-SB-6033](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-6033.html), [AMD-SB-6034](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-6034.html) | RCCL CVE correction and driver mitigation/product scope, no BIOS/distribution-kernel qualification. |
| [HIP #26209](https://github.com/ggml-org/llama.cpp/issues/26209), [#28211](https://github.com/ggml-org/llama.cpp/issues/28211), [Vulkan PR #31196](https://github.com/ggml-org/llama.cpp/pull/31196), [Ollama #17041](https://github.com/ollama/ollama/issues/17041), [cache #27148](https://github.com/ggml-org/llama.cpp/issues/27148), [PR #27624](https://github.com/ggml-org/llama.cpp/pull/27624), [Ollama #18528](https://github.com/ollama/ollama/issues/18528), [#29092](https://github.com/ggml-org/llama.cpp/issues/29092) | Current issue/merge state via repository APIs; no issue reproduced. Closure as not planned is not proof of a fix. |
| [MiMo manifest](https://registry.ollama.ai/v2/library/mimo-v2.6/manifests/9b), [Bolt pinned tree](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-24GB-GGUF/tree/e0fecb69cb3e5e4c5e8a056fa2aec98c78e91246), [Super VL pinned tree](https://huggingface.co/ggml-org/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-GGUF/tree/99144d1d7a318f045f1412a85bbb807f3c8a17a0) | Layers/digests and HF API file sizes compared with the RAM card; no download or run. |
| [Framework announcement](https://frame.work/blog/192gb-framework-desktop-open-for-pre-order/), [NL configurator](https://frame.work/nl/en/products/desktop-diy-amd-aimax300/configuration/new) | HTTP 403, not rechecked. |
| [Beelink EU](https://eu.bee-link.com/products/beelink-gtr9-pro-amd-ryzen-ai-max-395), [GMKtec EVO-X2 EU](https://de.gmktec.com/en/products/gmktec-evo-x2-amd-ryzen%E2%84%A2-ai-max-395-mini-pc-1), [EVO-X5 Pro EU](https://de.gmktec.com/en/products/gmktec-evo-x5-pro-ai-max-495), [Minisforum MS-S1 MAX EU](https://minisforumpc.eu/products/minisforum-ms-s1-max-mini-pc), [MAX-P495 EU](https://minisforumpc.eu/products/minisforum-ms-s1-max-p495) | HTTP 429, not rechecked; no rate-limit bypass or inferred stock/price. |
| [Corsair CS-9080003-NA](https://www.corsair.com/us/en/p/gaming-computers/cs-9080003-na/corsair-ai-workstation-300-amd-ryzen-ai-max-395-processor-amd-radeon-8060s-igpu-up-to-96gb-vram-128gb-lpddr5x-memory-4tb-2tb-2tb-m2-ssd-win11-home-cs-9080003-na) | HTTP 200: exact SKU/out-of-stock text readable; comparison SKU price not reused. |
| [Repository metadata](https://api.github.com/repos/hogeheer499-commits/strix-halo-guide), [registry](data/affiliate_link_registry.csv), [claim index](data/headline_claims.csv), [profiles](data/best_known_profiles.csv), [August 15 context results](data/raw/2026-08-15/qwen38-27b-ollama-03213-vulkan-radv/qualification/context_results.csv) | Public counts, link/relationship surface and existing evidence behind active recommendations; no private analytics or new hardware test. |
