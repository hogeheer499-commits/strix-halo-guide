# Inference Engines For Strix Halo (claims of third parties, checked 2026-09-30)

**The guide has not measured any of the community engines on this page.** The only routes with first-party rows are the `llama.cpp` and Ollama routes documented in [README.md](README.md), [BENCHMARKS.md](BENCHMARKS.md) and [SERVER_SHOOTOUT.md](SERVER_SHOOTOUT.md). Everything else below is what an engine's own README, its users or a vendor say. Facts that can change fast (versions, issue states, merge states) carry the date they were read; where a source was read again on 2026-10-01, that is stated.

Nothing here is a recommendation, a ranking or an endorsement. A listed engine is not a verified engine.

## How To Read A Headline Number

Headline speeds on this hardware are not comparable across engines unless the claim class matches. Check these before comparing:

| Claim class | What it means | Why it matters |
| --- | --- | --- |
| Short prompt | Prefill or decode measured on a short prompt (for example the guide's `llama-bench` pp512 / tg128). | Long contexts and real documents are slower; the guide's own real-corpus check slowed prompt ingest by 24-33% ([README.md](README.md), "Real-corpus 64K check"). |
| Repeating corpus | Decode measured on repetitive text, where a draft model is right almost every time. | Produces a ceiling, not a typical rate. One engine's own README says its peaks include repetitive output. |
| MTP or drafter | Speculative decoding with the model's own draft head or a separate drafter. | Changes the rate a lot: the guide's matched Ollama control for one model measured 12.89 t/s without MTP and 22.71 t/s with it (see below). In that run the generated text also differed between the two arms at temperature 0. Background: [MTP_SPECULATIVE_DECODING.md](MTP_SPECULATIVE_DECODING.md). |
| Power profile and IOMMU | The platform power profile, governor and `amd_iommu` setting during the run. | One third-party guide reports 21 to 24% higher prefill on one engine after moving from its stock setup (platform profile `balanced`, CPU governor `powersave`, IOMMU on, GPU power about 60 W) to the `performance` profile and governor, with GPU power rising to about 130 W; it reports a further gain after setting `amd_iommu=off` ([Level1Techs forum, read 2026-09-30](https://forum.level1techs.com/t/ryzen-ai-halo-halogen-server-testing-notes/257455), claim of a third party, not measured here). Always read the conditions a number was measured under. |

Mixing these classes is how a "5x faster" headline appears. The guide keeps direct `llama-bench`, server/API, MTP/speculative and concurrency results separate for the same reason.

## Engine Table

Verified here means: has this guide measured it? Licence and form are as stated by the project or by the GitHub API on the date shown; they are not legal advice.

| Engine | Licence and form | Source | Headline claim (as published) | Claim class | Verified here |
| --- | --- | --- | --- | --- | --- |
| `llama.cpp` (mainline) | Open source (MIT) | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | None on this page. The guide's own direct rows are in [BENCHMARKS.md](BENCHMARKS.md). | First-party, short prompt (`llama-bench` pp512 / tg128) | **Yes**, Vulkan/RADV and the scoped HIP routes, with dated rows. |
| Ollama | Open source (MIT) | [ollama/ollama](https://github.com/ollama/ollama) | None on this page. | First-party API rows | **Yes**, the Vulkan route, with dated rows. See "Ollama Compared With Other Servers" below. |
| `llama-server` Vulkan/RADV and Lemonade `llamacpp-rocm` | Open source (MIT for `llama.cpp`; Lemonade is Apache-2.0) | [Lemonade](https://github.com/lemonade-sdk/lemonade) | None on this page. | First-party concurrency sweep, Qwen3.6 35B-A3B, 2026-05-05 | **Yes, for that sweep only** ([SERVER_SHOOTOUT.md](SERVER_SHOOTOUT.md)); Lemonade releases after the measured build are unqualified. |
| vLLM | Open source (Apache-2.0) | [vllm-project/vllm](https://github.com/vllm-project/vllm) | None on this page. | First-party scoped experimental route | **Scoped only** ([VLLM_BASELINE.md](VLLM_BASELINE.md)); not a general qualification. |
| LM Studio | Desktop application; its public repository is a bug tracker only (GitHub description, 2026-10-01); licence terms not reviewed here | [lmstudio.ai](https://lmstudio.ai) | None on this page. | Community report only | **No.** One community Windows row exists in [COMMUNITY_RESULTS.md](COMMUNITY_RESULTS.md). Versions and issues: [WINDOWS_START.md](WINDOWS_START.md). |
| Unsloth Studio / Desktop | Repository is open source (Apache-2.0, GitHub API, 2026-10-01) | [unslothai/unsloth](https://github.com/unslothai/unsloth) | None on this page. | n/a | **No** for inference. A one-step fine-tune and export smoke exists ([UNSLOTH_STRIX_HALO.md](UNSLOTH_STRIX_HALO.md)). Users report garbage output on a HIP build; see the note below the table. |
| Gufo | Open source (MIT) | [gufo-org/gufo](https://github.com/gufo-org/gufo) | README, Qwen3.8 Flash-Next: 1,628.52 tok/s prompt processing and up to 59.41 tok/s generation for a single user with MTP; 157.22 tok/s aggregated over 8 concurrent requests. Qwen3.8 27B: 656.33 prompt and up to 70.56 generation (DFlash2, short-prompt workload). | MTP or drafter, short prompt, concurrency aggregate. The README says its peaks include repetitive output. A reply by the engine's makers in the Framework community thread ([thread](https://community.frame.work/t/gufo-the-all-in-one-strix-halo-inference-engine/85083), 2026-09-26) says the 59 tok/s figure is an extreme case: a prompt that asks the model to repeat one word, which drives drafter acceptance to 100% and gives a theoretical ceiling. | **No.** |
| Halogen Flash Server | **Closed binary** in a container image under the Peonist, LLC end-user licence agreement (v0.1, effective 2026-08-25); the repository holds deploy files, docs and tools, not the engine source (read 2026-09-30) | [peonist-ai/halogen-flash-server](https://github.com/peonist-ai/halogen-flash-server) | README, Qwen3.8 Flash-Next: 1,584 tok/s prefill (8,192-token prompt); 46.0 tok/s decode with the draft head at 32,768 tokens of context; 55.7 to 56.3 tok/s for a coding-agent turn with draft head plus prompt lookup. Measured by the maker on one reference machine at about 85 W sustained package power. | MTP or drafter plus prompt lookup, power profile (85 W reference), one model family. A forum guide ([Level1Techs, 2026-09-30](https://forum.level1techs.com/t/ryzen-ai-halo-halogen-server-testing-notes/257455)) reports 53.4 tok/s decode and about 1,770 tok/s prefill after power tuning and `amd_iommu=off`. A video marked as sponsored by AMD ([video](https://www.youtube.com/watch?v=Nm_zN6RQ_eE)) reports about 752 tok/s prefill and 41 tok/s generation at 32K. The three sets of numbers were not measured under the same conditions. | **No.** |
| Strix Llama and other `llama.cpp` forks | Forks; licences vary by repository | Community toolbox containers, for example [amd-strix-halo-toolboxes](https://github.com/kyuz0/amd-strix-halo-toolboxes) | Claims differ per fork and per post: MTP drafts, a custom ROCr, a custom scheduler. Examples recorded in [data/qwen38_route_matrix.csv](data/qwen38_route_matrix.csv) (2026-08-25). | Mostly MTP or drafter, short prompt | **No**, except the ROCmFPX route in [ROCMFP4_CHADROCK.md](ROCMFP4_CHADROCK.md). A fork-quant checklist is in [docs/models.md](docs/models.md). |
| EngramHalo | Fork of `llama.cpp` for one model; licence not reviewed | Described in a [Level1Techs thread](https://forum.level1techs.com/t/franken-strix-halo-2x-r9700s-128gb-strix-halo-unified-memory/254736) (2026-09-03) | Keeps the n-gram embedding table of Qwen3.8-Flash-Next in a CPU/SSD buffer instead of GTT; one post reports about 24 tok/s with it (claim of a third party). | Community report | **No.** |
| DwarfStar4 (`ds4`) | Separate project; licence not reviewed | [ds4](https://github.com/antirez/ds4) | Used in the vendor-published 192GB claim for DeepSeek V4.1 Flash described in [docs/models.md](docs/models.md). No headline recorded here. | Vendor-published claim | **No.** |
| Strix Halo toolboxes and AI Toolbox Cockpit | Container recipes and a launcher; no licence reported by the GitHub API (2026-10-01) | [amd-strix-halo-toolboxes](https://github.com/kyuz0/amd-strix-halo-toolboxes), [ai-toolbox-cockpit](https://github.com/kyuz0/ai-toolbox-cockpit) | None; these package other engines (`llama.cpp` Vulkan/ROCm, vLLM, ComfyUI, fine-tuning). An experimental Gufo ROCm 10.0 toolbox was added on 2026-09-26 and the Cockpit lists Gufo and Halogen Flash. | n/a | **No** individually. The README links the containers it uses. In a reply on the toolbox project's issue tracker the maintainer says container security is a concern and that Halogen gets extra isolation because it is closed source ([issue #135](https://github.com/kyuz0/amd-strix-halo-toolboxes/issues/135), reply of 2026-09-21, read 2026-09-30; the issue was opened as a security report and withdrawn by its reporter, so the quote is the maintainer's reply only). |
| hipfire | The GitHub API reports licence "other" (2026-10-01); not reviewed | [hipfire](https://github.com/warpfront/hipfire) | Repository description: a Rust inference engine for RDNA GPUs. No headline recorded here. | n/a | **No.** |
| Atlas | Open source (AGPL-3.0 per the GitHub API, 2026-10-01) | [Atlas](https://github.com/Atlas-Inf/atlas) | Repository description: a dependency-free inference engine; Strix Halo and GB10 listed as supported. Proposed as a Lemonade backend in [RFC #3643](https://github.com/lemonade-sdk/lemonade/discussions/3643) (2026-09-22). No headline recorded here. | n/a | **No.** |
| AMD `ggml-hrx` and `llamacpp-hrx` | AMD proposal for `llama.cpp` | [llama.cpp RFC #27219](https://github.com/ggml-org/llama.cpp/discussions/27219) (opened 2026-08-17; draft PR [#27218](https://github.com/ggml-org/llama.cpp/pull/27218)) | The RFC describes a native AMD backend built on HRX, a lighter subset of ROCm. The first contribution is limited to a minimal kernel library sufficient for one Qwen3-30B-A3B model. No speed claim is recorded here. Owners reported test runs on Strix Halo in the discussion (2026-09-15 and 2026-09-19). | n/a | **No.** |
| Lucebox | Separate project; licence not reviewed | [Maker post on X](https://x.com/pupposandro/status/2100220230383358150) (2026-09-16) | Maker claim: a ROCm engine plus the DSpark drafter at 41.9 tok/s at 8K context, and that ROCm now beats Vulkan on Strix Halo. | Maker claim, MTP or drafter | **No.** |
| Strata | Separate project; licence not reviewed | [Release post on X](https://x.com/coldniko/status/2105355519997431999) (2026-09-30; version number to verify, the post card was not readable without JavaScript) | Maker claim, not verified: prompts about 28% faster, 1M tokens of context, multi-GPU. | Maker claim | **No.** |
| hipEngine | Separate project; licence not reviewed | [hipEngine](https://github.com/shisa-ai/hipEngine) (repository created 2026-05-15) | No headline recorded here. | n/a | **No.** |

Notes on rows above:

- **Gufo.** Created 2026-08-11. GitHub releases read on 2026-10-01 run from v0.1.0 (2026-09-28) to v0.4.0 (2026-10-01), so a number read last week may describe a different build. Its README lists a Windows port and an RDMA variant for two Strix Halo machines as separate forks that are not merged into the main repository. The README quickstart publishes port 8080 and starts the server with `--host 0.0.0.0` in a container; bind to loopback unless you want LAN access. Issues about tool calls and sampling were open on 2026-09-30 and have changed state since; read the current tracker.
- **Halogen.** A repository titled "hgn-spec" describes itself as a clean-room specification of Halogen's HGN weight format ([repository](https://github.com/jtsylve/hgn-spec), created 2026-09-24; not reviewed here). The Halogen README states that, with its download option unset, the container opens no outbound connections; this is a statement by the vendor and was not checked. The Level1Techs guide linked above publishes port 8731 on all interfaces and sets `amd_iommu=off`; compare both with your network and with the [IOMMU policy in this guide](README.md#step-12-choose-the-iommu-policy).
- **Lemonade.** The stable release v2026.40.0 was published on 2026-09-30 17:46 UTC (GitHub releases). [RFC #3585](https://github.com/lemonade-sdk/lemonade/discussions/3585) (opened 2026-09-14) proposes OCI containers as Lemonade backends on Linux so that experimental engines such as Halogen, ROCmFPX and DwarfStar4 can be installed through Lemonade; the detailed specification is in [PR #3697](https://github.com/lemonade-sdk/lemonade/pull/3697), open on 2026-10-01.
- **Unsloth Studio.** Users report that on a HIP build the app sets `GGML_CUDA_ENABLE_UNIFIED_MEMORY=1`, which produces garbage output with large models on Strix Halo, and that setting `UNSLOTH_DISABLE_UNIFIED_MEMORY=1` avoids it ([Hugging Face discussion #30](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF/discussions/30), opened 2026-08-27). Unsloth replied on 2026-08-31 that it was most likely an AMD and `llama.cpp` specific problem and that a fix was in progress. Whether it is fixed was not checked. The same variable family is already tracked in [ROCM_VLLM_BUGWATCH.md](ROCM_VLLM_BUGWATCH.md).
- **Front-ends.** LM Studio, Lemonade, Unsloth Studio and Open WebUI are listed in this guide without ranking. Which one fits depends on whether you want a model manager, a chat UI or an API server; this guide has not compared them.

## Ollama Compared With Other Servers

**What users say (claims of third parties, not reproduced here).** Some users on community forums describe Ollama as slower than `llama-server` or a `llama.cpp` fork in their own tests and recommend `llama-server`, Unsloth Studio or Lemonade instead. A recurring complaint is that the right flags per model are not obvious. These are forum reports that cannot be linked from this page; they are not verified and carry no numbers here.

**What this guide measured.**

| Date | Route | Result | Scope |
| --- | --- | --- | --- |
| 2026-09-26 | Ollama 0.32.15, Qwen3.8 27B `qwen3.8:27b-q4_K_M`, no draft | 12.89 t/s generation, 384.66 prompt t/s | Vulkan/RADV, 4096-context API, 9 warm repeats, routine background load. |
| 2026-09-26 | Same service, `qwen3.8:27b-mtp-q4_K_M`, Ollama-default MTP (`draft_num_predict 4`) | 22.71 t/s generation, 360.01 prompt t/s | Same run and conditions. The output text differed from the no-draft arm at temperature 0 in the raw notes. |
| 2026-05-05 and 2026-05-07 | `llama-server` Vulkan/RADV (concurrency sweep, 2026-05-05) and Ollama 0.23.1 (API warm average, 2026-05-07), Qwen3.6 35B-A3B | 58.80 t/s aggregate at 1 request against 50.51 t/s | Different measurement shapes and old builds. Later controlled Ollama runs on the same model measured 72.55 to 73.20 t/s ([README.md](README.md), FAQ on Ollama and `llama.cpp`); see [SERVER_SHOOTOUT.md](SERVER_SHOOTOUT.md) for the caveats. |

Sources: [BENCHMARKS.md](BENCHMARKS.md), [raw bundle](data/raw/2026-09-26/qwen38-27b-ollama-03215-mtp-vs-nodraft/).

There is no same-model, same-shape `llama-server` row for Qwen3.8 27B in this guide yet, so the guide draws no conclusion about which server is faster for that model. The README keeps Ollama as the documented easy route because it has a qualified setup, service and restart path; that is a statement about setup effort and qualification, not about speed.

## Questions To Ask Before Running A Community Engine

1. **Open or closed?** Can you read the source and the build recipe? If it is a closed binary, who publishes it and under which terms?
2. **What does the process get access to?** A container started with `--device /dev/kfd` has direct GPU access. Options such as `--ipc=host`, `--security-opt seccomp=unconfined`, `SYS_PTRACE` or `--privileged` widen that. Read the run command line by line and prefer rootless containers.
3. **Where does it listen?** `--host 0.0.0.0` or `-p PORT:PORT` publishes the API on every interface. Bind to `127.0.0.1` unless you mean to share it, and use an API key if you do.
4. **Are secrets in the recipe?** Avoid putting a password in a wrapper script; use a `sudoers` rule or a `systemd` unit instead.
5. **Where do the weights come from?** Which repository and which revision (hash)? Custom tensor types can fail or produce garbage in mainline `llama.cpp`, Ollama or LM Studio. See the fork-quant checklist in [docs/models.md](docs/models.md).
6. **Is the version pinned?** Pin a tag, not `:latest`, and keep the previous image so you can roll back. Record the version next to any number you report.
7. **Does it hold up under real load?** Check long contexts, concurrent requests and tool calls on your own workload. A fast counter is not a correct answer; read the output.
8. **Is the headline your workload?** Match the claim class (table above): prompt length, repetitive text, MTP, power profile, IOMMU.
9. **Does it call out?** Check outbound connections with a firewall rule or `ss -tp` rather than relying on a README statement.
10. **Is the server shared?** Several users on one server raise separate problems; see [SECURE_LOCAL_AI.md](SECURE_LOCAL_AI.md).

## Related Pages

- [SERVER_SHOOTOUT.md](SERVER_SHOOTOUT.md): the guide's own server comparison and concurrency sweep.
- [docs/models.md](docs/models.md): models, fit tiers and the fork-quant checklist.
- [WINDOWS_START.md](WINDOWS_START.md): LM Studio and the Windows routes.
- [SECURE_LOCAL_AI.md](SECURE_LOCAL_AI.md): binding, containers, shared servers.

Last checked: 2026-09-30, with GitHub, Hugging Face and Lemonade statuses re-read on 2026-10-01.
