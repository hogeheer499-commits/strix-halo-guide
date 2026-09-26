# Existing-user runtime qualification — September 19, 2026

This is a scoped functional qualification on the existing Beelink GTR9 Pro
128GB Ryzen AI MAX+ 395 workstation, not a fresh installation, general model
quality benchmark, or replacement for the historical speed records.

## Decision

- **Existing service:** Ollama **0.32.15**, Vulkan/RADV, is qualified for the
  specific text, image, executed-tool and pinned browser checks below after a
  normal service restart. No full-host reboot was performed in this campaign.
- **Fresh-install baseline:** the historical reboot-qualified **0.31.2** pin
  remains. The revised installer has offline regression coverage, not a new
  clean-install hardware qualification. Do not downgrade a working existing
  installation merely to match the pin.
- **Ollama 0.34.2:** useful but **not the default**. The isolated candidate
  passed the available-model tests and process restart. Official Qwen3.8
  weights were absent; no large replacement download, normal package upgrade,
  candidate WebUI acceptance or full-reboot test was performed. Its Qwen3.8
  thinking/API compatibility remains open.
- **llama.cpp v0.4.1:** the pinned current CLI and the tested Qwen3-Coder
  Vulkan direct/server route work. HIP passed the bounded controls below;
  this does not qualify all models, large allocations or contexts.

## Host and artifacts

Kernel `7.0.0-31-generic`; Mesa `26.2.3~kisak1~n`; Radeon 8060S/gfx1151.
The pre-existing legacy boot/memory profile and background workloads were
retained. No kernel, driver, firmware, network policy or tuning changes were
made. These tests do not validate that legacy configuration as a new-install
recipe. They are not strict-clean performance measurements.

| Ollama tag | Manifest SHA-256 | Tested purpose |
|---|---|---|
| `qwen3.6:35b-a3b` | `07d35212591fc27746f0a317c975a6d68754fb38e9053d82e25f06057af28522` | Text, thinking and marker retrieval |
| `qwen2.5vl:7b` | `5ced39dfa4bac325dc183dd1e4febaa1c46b3ea28bce48896c8e69c1e79611cc` | Image fixture |
| `devstral-small-2:latest` | `24277f07f62db8f9cb68e9dfc679ea1818a7fbac47a50eff0a701d3f645b63c8` | Executed tool round-trip |

Model identifiers refer to the captured manifests, not a guarantee that future
pulls of these tags retrieve the same bytes. All three used Q4_K_M weights.

## Existing service and isolated candidate

| Acceptance | Expected and observed | 0.32.15 service | 0.34.2 isolated |
|---|---|---|---|
| Text, first and warm request | `17 + 25` → visible `42` | PASS after service restart | PASS before/after process restart |
| Image | Known [repository fixture](data/raw/2026-07-16/nemotron-omni-nvfp4-multimodal/vision-test.png) → `STRIX 395` | PASS with Qwen2.5-VL | PASS with Qwen2.5-VL |
| Genuine tool | Structured `lookup_fixture` call, actual deterministic harness execution, result returned to model, final `STRIX-LOCAL-7319` | PASS with Devstral | PASS with Devstral |
| Thinking | Visible correct answer, not reasoning-only output | PASS with Qwen3.6 | PASS with Qwen3.6 |
| Bounded retrieval | Exact inserted marker in a roughly 5K-token prompt | PASS | PASS |
| OpenAI-compatible chat | Visible `42` with Devstral | PASS | PASS |
| Missing model | HTTP 404, not a false successful answer | PASS | PASS |

The service's first text response became visible after **3.889s**, completed in
**3.920s**; the warm response became visible after **0.066s**, completed in
**0.099s**. These are one short acceptance request each, not throughput or
typical-user latency estimates. Model residency and cache state affect them.
**Summary-only:** these latency figures have no public CSV or raw artifact, so
per the guide's evidence rule they are unverified until a sanitized raw subset
is published.
GPU/backend evidence came from runtime logs and loaded-model state; HTTP 200
alone was never a pass. Full requests, streams, counters and memory snapshots
are retained in the private campaign bundle; this public summary does not
publish workstation/account operations or private logs.

Earlier **Qwen3.6 image and tool failures remain negative evidence**. Passing
Qwen2.5-VL and Devstral does not erase them. They are not automatically
regressions against historical vision tests that used different models.

## Pinned browser route and privacy boundary

Open WebUI **0.10.2**, image
`ghcr.io/open-webui/open-webui@sha256:a26effeb220e132482bf7e0560b3404843e7bc40d23051144e062960df8df6b0`,
passed model discovery, visible Qwen3.6 response, controlled missing-model
behavior and client restart in the preceding scoped client campaign; discovery
and a visible response passed again after the service restart here.

The browser port was bound to loopback. The bridge container reached the
existing Ollama listener through the host gateway. **The Ollama listener was
reachable from a second LAN machine: this host was not local-only.** No
Internet reachability was established and no firewall/bind changes were made.
The local fixture used offline settings and disabled external OpenAI providers;
image provisioning itself required external distribution. This is not a
privacy guarantee for plugins, web search, RAG/embedding downloads or every
WebUI setting. A host-gateway alias cannot reach an exclusively loopback-bound
Ollama service by itself. Do not broaden an unauthenticated listener just to
copy this topology.

## llama.cpp and HIP correctness

Release `v0.4.1`, commit
`b29c606e28a01b1bc8c1351026a0fa6e616bf6c4`, built successfully for Vulkan
and for HIP. The HIP build used an already-cached isolated toolchain, HIP
`7.13.26154-92b7431876`, targeting `gfx1151`; no host ROCm installation changed.

Current CLI uses `--load-mode auto|none|mmap|mlock|mmap+mlock|dio` and
`-fa on|off|auto`. Do not copy removed `--mmap`, `--no-mmap` or old numeric
Flash Attention options into a current command.

The existing Qwen3-Coder 30B-A3B `UD-Q4_K_XL` artifact returned exact `42`
through direct CLI with both `auto` and `none`. The separate Vulkan server
passed arithmetic, **4,579-prompt-token** exact retrieval and two concurrent
distinct-marker requests. Total context allocation was 16,384 across two
slots; that is not proof of a filled 16K request.

With the same HIP toolchain and artifact, historical **b10687/c841aee** passed
short arithmetic but failed retrieval and both concurrent marker outputs.
Released **v0.4.1** passed these controls, including repeated runs. Both builds
passed the one-image Gemma 4 31B QAT Q4_0 + Q8_0-projector fixture (`STRIX 395`).
Thus this image did not discriminate the builds; do not label the old image
route broken from the text failures.

A further released-HIP check used 32,768 total context across two 16K slots:
exact retrieval passed at **14,029 evaluated prompt tokens**, with both
concurrent markers correct at 14,028/14,027 tokens. This is not a filled 32K
request or general long-document quality qualification.

The release contains [mitigation #28604](https://github.com/ggml-org/llama.cpp/pull/28604).
The A/B supports the released route, but many commits differ: it does not
attribute every change to that one patch or close
[issue #26209](https://github.com/ggml-org/llama.cpp/issues/26209).
GPU telemetry showed 49/49 layers offloaded, approximately 16,674MiB model
and 1,536MiB KV buffers for the Coder control. Reported HIP total/free memory
was internally inconsistent on UMA; it is **not a maximum usable-memory
measurement**. Large-model allocation and Qwen3.8 long-context qualification
remain separate.

A matched short direct benchmark control (pp128/tg32, three repeats, same
artifact/settings) showed no material change: about 599.70/94.60 t/s on the
old build and 602.01/94.95 t/s on the release. This is a non-headline sanity
control, not evidence of a general speed improvement. **Summary-only:** the
raw data for these figures is in the private campaign bundle, with no public
CSV or raw artifact, so treat them as unverified until a sanitized raw subset
is published. Direct benchmark,
server/API and speculative/MTP claims remain separate.

## Limits and next useful work

The small Qwen3 0.6B preliminary strict-format check returned `17 + 25 = 42`
rather than exactly `42`; retain that formatting failure. The practical Coder
control above passed. Build-time UI asset fetching was unavailable in the
network-disabled HIP build; the server API used the built fallback.

The highest-value missing work is official Qwen3.8 on the candidate, then a
normal service-upgrade/client/full-reboot acceptance campaign with rollback.
Do not infer fresh-install reliability, broad coding/vision quality, all-client
compatibility, maximum capacity, privacy or cross-OEM equivalence from these
smokes. SGLang/Lemonade were not retested: that would not change this scoped
single-user recommendation.
