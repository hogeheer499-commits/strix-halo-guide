# Scoped maintenance review — November 8, 2026

This review covers five things: the new RAM choice card, a correction of
conflicting setup-status statements, selected upstream states, three 192GB
store listings and service/contact information. Sources were read on November 8
(UTC); content integration and checks continued on November 9 in
Europe/Amsterdam. It is not a new benchmark, a complete security audit or a
broad evidence review. **The October 1 evidence-review date
and its 21-day freshness limit remain unchanged.** Historical measurements,
runtime pins and raw evidence keep their original dates.

## Reader-facing changes

- [The model hub](docs/models.md#what-can-i-run-with-my-ram) now opens with a task and model to try for 32GB, 64GB, 96GB, 128GB and 192GB. The 128GB Qwen retrieval test is first-party evidence; the new MiMo, Bolt and Super VL rows are untested candidates. The 96GB row points to community evidence and claims no special capacity benefit.
- [README](README.md) and [the buyer guide](docs/best-strix-halo-mini-pc.md) link to that card. Published file-size bands are not RAM budgets. The dated 126.21GB MiMo listing is about 117.54GiB of weights; that number alone establishes neither fit nor impossibility on 128GB.
- [The setup page](docs/amd-strix-halo-setup.md), [local chat route](LOCAL_CHAT_START.md), [troubleshooting](docs/troubleshooting.md) and [security status](SECURITY.md#open-webui) now keep three things apart: the limited October 15 WebUI test, the later advisory, and the acceptance checks that are still open.
- [The GPU troubleshooting section](docs/troubleshooting.md#is-it-running-on-the-gpu) documents `python3 scripts/check_local_ai.py report`, implemented alongside this content candidate. It selects the starter tag and reports allocation only; a CPU or mixed result can be a complete report, but it is not a GPU pass. Fixture checks establish script behavior, not real hardware acceptance.
- [Current models](CURRENT_MODELS.md), [bugwatch](ROCM_VLLM_BUGWATCH.md#november-8-2026-scoped-recheck) and [engines](ENGINES.md) separate newly available releases from locally qualified versions.
- [Services](SERVICES.md) records the fixed Setup Rescue scope: one machine, up to 90 minutes, a working path or documented blocker; €229 excluding VAT for the first three customers, then €299 excluding VAT. The applicable rate is confirmed before work starts; no remaining-place count is claimed. `SERVICES.md` states the supplier: Strix Halo Guide is a project of Kleine Koe (JVD Netwerk), and services are offered and invoiced by JVD Netwerk. Service, intake and partner contacts in `SERVICES.md`, `SERVICE_INTAKE.md`, `ONE_PAGE_BRIEF.md` and `PARTNERSHIP.md` use `info@strixhaloguide.com`.
- `.github/FUNDING.yml` no longer enables an inactive GitHub Sponsors entry. A read-only account check returned `hasSponsorsListing: false`; no account feature was activated.

## Evidence and primary sources

| Source read | Supported observation | Boundary |
| --- | --- | --- |
| [August 15 Qwen context results](data/raw/2026-08-15/qwen38-27b-ollama-03213-vulkan-radv/qualification/context_results.csv) | Qwen3.8-27B Q4_K_M, Ollama 0.32.13, Vulkan/RADV, default MTP: exact retrieval through 50,059 prompt tokens on the 128GB system | No new run, general task-quality verdict or other-RAM qualification; preserve the larger failing prompt. |
| [MiMo Ollama manifest](https://registry.ollama.ai/v2/library/mimo-v2.6/manifests/9b) | `llamacpp`/GGUF Q4_K_M; 5,629,105,568-byte model and 921,705,024-byte projector; blob identities recorded on the model page | Mutable tag, not a 32GB RAM or task measurement. |
| [Bolt pinned tree](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-24GB-GGUF/tree/e0fecb69cb3e5e4c5e8a056fa2aec98c78e91246) | 22,018,326,528-byte model + 1,733,692,736-byte projector | Publisher's “24GB” target, not an AMD measurement. |
| [Super VL pinned tree](https://huggingface.co/ggml-org/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-GGUF/tree/99144d1d7a318f045f1412a85bbb807f3c8a17a0) | Q4_0 71,933,775,840 bytes; Q8_0 128,472,993,760 bytes = 119.65GiB; BF16 projector 1,733,696,768 bytes separately | Q4 plus projector exceeds 64GiB; smaller quants are not excluded. Q8 on 128GB is very tight and untested, not proved impossible. Optional MTP heads are extra. |
| [Ollama 0.40.15](https://github.com/ollama/ollama/releases/tag/v0.40.15), [0.40.13](https://github.com/ollama/ollama/releases/tag/v0.40.13), [llama.cpp v0.9.0](https://github.com/ggml-org/llama.cpp/releases/tag/v0.9.0) | Published November 3, October 28 and November 4 respectively; MiMo support and LFM3 Linux/Windows support are release-note observations | No upgrade, runtime/default change or performance claim. |
| [#26209 Regression after c7d8722: infinite "/" tokens](https://github.com/ggml-org/llama.cpp/issues/26209), [#28211 HIP/ROCm wrong logits beyond n_ubatch](https://github.com/ggml-org/llama.cpp/issues/28211), [#31196 Vulkan Q8_0 weight reuse for 9–16 columns](https://github.com/ggml-org/llama.cpp/pull/31196) | Respectively closed as not planned on October 16, open, and open/unmerged | Closure is not a verified fix; proposed code is not a released or measured improvement. |
| [October 15 isolated acceptance](data/raw/2026-10-15/ollama-0312-webui-0114-isolated-acceptance/README.md) | New data, first admin/login, visible answer, closed signup, anonymous rejection, loopback listeners and UI/runtime restart passed | Docker installation, exact default-port/named-volume command, fresh native installation, host reboot, restore and second-device checks remain open. |
| [WebUI GHSA-3vvh-g22g-jq6r](https://github.com/open-webui/open-webui/security/advisories/GHSA-3vvh-g22g-jq6r) | Affects >=0.7.0,<0.12.2, including 0.11.4; fix listed as 0.12.2. Requires enabled channels, a channel webhook, member write access and knowledge of the webhook ID | No exploit or mitigation test performed; the ID is not a secret. Disabled channels or no webhooks are unaffected according to this advisory. No blanket security qualification or blind upgrade. |
| [Framework announcement](https://frame.work/blog/192gb-framework-desktop-open-for-pre-order/), [NL store link](https://frame.work/nl/en/products/desktop-diy-amd-aimax300/configuration/new), [GMKtec EU](https://de.gmktec.com/en/products/gmktec-evo-x5-pro-ai-max-495), [Minisforum EU](https://minisforumpc.eu/products/minisforum-ms-s1-max-p495) | The buyer page records the pre-order and starting price, the estimated dispatch and the conflicting stock labels separately | Direct store fetches were partly rate-limited; public web text supplied the scoped listing observations. No checkout, complete delivered quote or buyer receipt was verified. Framework's 192GB configurator could not be read reliably. |

## Validation and publication limits

The repository validator and the local link/anchor checks are part of reviewing
this content candidate; they are not hardware tests. The known freshness
failure must remain visible until a real broad review is completed. `data/public_state.json`
records only content/maintenance, scoped availability and local publication
status changes; qualification and measurement fields are unchanged.

No guide or site publication, release,
account activation, runtime installation, model download or host change is
established by this review. The canonical site requires its own integration,
build and authorized publication. The report mode's real-host check stopped at
the listener guard before API access; no successful real GPU/CPU report or fresh
runtime, boot or recovery qualification is established by its synthetic fixtures.
