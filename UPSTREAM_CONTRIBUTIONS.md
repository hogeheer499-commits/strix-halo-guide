# Accepted Upstream Contributions

This page records accepted upstream work by the maintainer of `strix-halo-guide`.
It is a verification page, not an endorsement claim: each entry links to the
upstream pull request, review history, tests, and merge record.

Snapshot: 2026-08-21. Merged pull requests listed: 17 across 12 external
projects, plus one contribution under active upstream review.

## Why This Matters

The guide depends on open-source runtimes and infrastructure such as
`llama.cpp`, AMD Lemonade, local model servers, GGUF tooling, agent clients,
official vendor SDKs, and observability components. Accepted upstream work
shows that the maintainer does more than collect downstream benchmark numbers:

- isolate a reproducible software problem;
- scope a change narrowly;
- add or run relevant validation;
- respond to upstream review;
- preserve compatibility and failure boundaries;
- turn findings into reviewable public work.

That makes the guide's setup and benchmark evidence more credible. It does not
make every guide claim correct by association; benchmark claims still require
their own raw evidence and reproduction path.

## Strix Halo And Local-Runtime Work (Most Relevant To This Guide)

| Project | Accepted contribution | Why it is relevant |
|---|---|---|
| `lemonade-sdk/lemonade` (AMD's local-AI server) | [`#3004 fix: honor custom backend binary environment variables`](https://github.com/lemonade-sdk/lemonade/pull/3004), merged 2026-08-11 | Makes backend configuration, runtime, and status behavior consistent when custom backend binaries are configured, with substantive reviewer feedback addressed. Lemonade is the ROCm runtime route used in this guide's concurrency and NPU evidence. |
| `AlexsJones/llmfit` | [`#842 fix: resolve generic AMD/ATI Strix Halo identity`](https://github.com/AlexsJones/llmfit/pull/842), merged 2026-08-09 | Fixes hardware identification for Strix Halo systems in a model-fit tool, so fit recommendations stop treating the Radeon 8060S as a generic AMD/ATI device. Directly about this platform. |
| `ggml-org/llama.cpp` | [`#25643 common: skip empty implicit default preset`](https://github.com/ggml-org/llama.cpp/pull/25643), merged 2026-07-25 | Fixes an INI preset/router edge case while preserving real default presets, named presets, and global settings. The PR includes a successful `llama-server` build, focused router-mode checks, and two upstream approvals. `llama.cpp` is a core runtime used throughout this guide. This is runtime-maintenance evidence, not a Strix Halo performance patch. |
| `mudler/LocalAI` | [`#10783 fix(ds4): bundle transitive runtime dependencies`](https://github.com/mudler/LocalAI/pull/10783), merged 2026-07-11 | Makes the DS4 backend package self-contained, validates packaged loader resolution, and prevents builder-host dependencies from hiding a broken release artifact. This is directly relevant to reliable local-AI packaging and deployment. |
| `vllm-project/vllm-gguf-plugin` | [`#86 document tested GGUF model coverage`](https://github.com/vllm-project/vllm-gguf-plugin/pull/86), merged 2026-07-20 | Documents model families and quantizations exercised by upstream generation tests while explicitly avoiding a false compatibility allowlist. This supports the same claim-hygiene approach used in this guide. |

## Official SDK And Inference-Infrastructure Work

| Project | Accepted contribution | Scope |
|---|---|---|
| `openai/openai-dotnet` (official OpenAI .NET SDK) | [`#1256 Add Responses reasoning context support`](https://github.com/openai/openai-dotnet/pull/1256), merged 2026-08-14 | Adds reasoning-context support through the full SDK chain: specification, generated models, serialization, public API, and tests. Two approvals; 1,578 tests passing. |
| `openai/openai-dotnet` | [`#1255 Fix conversation include query serialization`](https://github.com/openai/openai-dotnet/pull/1255), merged 2026-07-28 | Fixes query serialization for conversation `include` parameters in the official SDK. |
| `kubernetes-sigs/inference-perf` | [`#613 Let the finite timer stop zero-worker load generation`](https://github.com/kubernetes-sigs/inference-perf/pull/613), merged 2026-08-18 | Reproduces a real load-generation fault, adds a regression test, and passes the 435-test suite. Inference-perf is a Kubernetes SIG benchmarking tool for LLM serving, which is the same problem space as this guide's concurrency evidence. |

Precise wording for the SDK entries: two contributions merged into OpenAI's
official .NET SDK. This makes the maintainer a contributor to that SDK, not an
OpenAI employee or a contributor to ChatGPT itself.

## AI Agent And Local Endpoint Work

Four accepted Qwen Code changes cover local/single-slot agent scheduling,
provider behavior, model selection, and messaging integration:

| Contribution | Scope |
|---|---|
| [`QwenLM/qwen-code#7258`](https://github.com/QwenLM/qwen-code/pull/7258), merged 2026-07-22 | Prevents a single-slot local endpoint from being reoccupied by the main agent while a background subagent is waiting to run. |
| [`QwenLM/qwen-code#7522`](https://github.com/QwenLM/qwen-code/pull/7522), merged 2026-07-23 | Keeps ACP model selectors aligned with the active authentication route instead of advertising an unrelated discontinued OAuth model. |
| [`QwenLM/qwen-code#7612`](https://github.com/QwenLM/qwen-code/pull/7612), merged 2026-07-23 | Preserves Telegram forum-topic routing for command and agent replies, including concurrent topics. |
| [`QwenLM/qwen-code#7666`](https://github.com/QwenLM/qwen-code/pull/7666), merged 2026-07-25 | Adds configurable SSE rate-limit retry delays while preserving existing defaults, with focused tests and build/lint/type checks. |
| [`QwenLM/qwen-code#7661`](https://github.com/QwenLM/qwen-code/pull/7661), merged 2026-07-26 | Avoids sending required tool calls to DashScope thinking modes that reject them. |

These changes are broader AI-agent engineering evidence. They are not Strix
Halo benchmark claims.

## Evidence And Observability Work

| Project | Accepted contribution | Scope |
|---|---|---|
| `open-telemetry/opentelemetry-collector-contrib` | [`#49619 GenAI normalizer: opt-in schema URL overwrite`](https://github.com/open-telemetry/opentelemetry-collector-contrib/pull/49619), merged 2026-07-13 | Adds an opt-in configuration path, six directly involved schema tests, documentation, and changelog coverage without changing the default behavior. |
| `NVIDIA/aicr` | [`#1730 propagate CNCF evidence-section failures`](https://github.com/NVIDIA/aicr/pull/1730), merged 2026-07-13 | Makes failed evidence sections reach the collector and CLI result, records valid skips for absent optional prerequisites, and fails closed on missing or malformed verdicts. |

These contributions support the guide's broader evidence-engineering approach:
clear defaults, explicit failure states, reproducible validation, and public
source-of-truth links.

## Under Upstream Review (Not Counted As Merged)

| Project | Contribution | Status |
|---|---|---|
| `ROCm/aiter` | [`#4385`](https://github.com/ROCm/aiter/pull/4385) | Open. Public maintainer feedback confirms the technical direction; it is listed here as ongoing technical validation and is excluded from the merge count until merged. |

## External Adoption Of This Guide

These are not engineering contributions. They are public signals that other
maintainers chose to list this guide:

| Project | Accepted listing |
|---|---|
| `alvinreal/awesome-opensource-ai` | [`#671 Add AMD Strix Halo local LLM guide`](https://github.com/alvinreal/awesome-opensource-ai/pull/671), merged 2026-08-10 |
| `deseven/strixhalo-homelab` (strixhalo.wiki source) | [`#17 docs: add reproducible Strix Halo LLM guide`](https://github.com/deseven/strixhalo-homelab/pull/17), merged 2026-08-09 |
| `Shubhamsaboo/awesome-llm-apps` | [`#1075 docs: fix local ChatGPT setup paths`](https://github.com/Shubhamsaboo/awesome-llm-apps/pull/1075), merged 2026-08-09 (documentation fix) |

## Honest Boundaries

- An accepted upstream contribution is not official endorsement of this guide.
- The `llama.cpp` contribution fixes preset/router behavior; it does not claim
  to enable Strix Halo or improve Strix Halo inference speed.
- The Lemonade contribution is a configuration-consistency fix accepted by
  AMD's open-source Lemonade project; it is not an AMD partnership.
- OpenAI .NET SDK, Kubernetes SIG, Qwen Code, OpenTelemetry, NVIDIA AICR,
  LocalAI, and vLLM GGUF work should not be presented as AMD or OEM
  collaboration.
- Awesome-list and wiki listings are adoption signals, not technical review.
- Guide performance and compatibility claims remain supported by the linked
  CSVs, raw logs, charts, commands, and caveats for each specific run.

The maintainer's public GitHub contribution history is available at
[`hogeheer499-commits`](https://github.com/hogeheer499-commits). This page lists
the accepted upstream work most relevant to local AI, runtime reliability, and
evidence quality rather than treating raw activity volume as proof.
