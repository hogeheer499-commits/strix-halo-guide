# Accepted Upstream Contributions

This page records accepted upstream work by the maintainer of `strix-halo-guide`.
It is a verification page, not an endorsement claim: each entry links to the
upstream pull request, review history, tests, and merge record.

## Why This Matters

The guide depends on open-source runtimes and infrastructure such as
`llama.cpp`, local model servers, GGUF tooling, agent clients, and observability
components. Accepted upstream work shows that the maintainer does more than
collect downstream benchmark numbers:

- isolate a reproducible software problem;
- scope a change narrowly;
- add or run relevant validation;
- respond to upstream review;
- preserve compatibility and failure boundaries;
- turn findings into reviewable public work.

That makes the guide's setup and benchmark evidence more credible. It does not
make every guide claim correct by association; benchmark claims still require
their own raw evidence and reproduction path.

## Most Relevant To This Guide

| Project | Accepted contribution | Why it is relevant |
|---|---|---|
| `ggml-org/llama.cpp` | [`#25643 common: skip empty implicit default preset`](https://github.com/ggml-org/llama.cpp/pull/25643), merged 2026-07-25 | Fixes an INI preset/router edge case while preserving real default presets, named presets, and global settings. The PR includes a successful `llama-server` build, focused router-mode checks, and two upstream approvals. `llama.cpp` is a core runtime used throughout this guide. This is runtime-maintenance evidence, not a Strix Halo performance patch. |
| `mudler/LocalAI` | [`#10783 fix(ds4): bundle transitive runtime dependencies`](https://github.com/mudler/LocalAI/pull/10783), merged 2026-07-11 | Makes the DS4 backend package self-contained, validates packaged loader resolution, and prevents builder-host dependencies from hiding a broken release artifact. This is directly relevant to reliable local-AI packaging and deployment. |
| `vllm-project/vllm-gguf-plugin` | [`#86 document tested GGUF model coverage`](https://github.com/vllm-project/vllm-gguf-plugin/pull/86), merged 2026-07-20 | Documents model families and quantizations exercised by upstream generation tests while explicitly avoiding a false compatibility allowlist. This supports the same claim-hygiene approach used in this guide. |

## AI Agent And Local Endpoint Work

Four accepted Qwen Code changes cover local/single-slot agent scheduling,
provider behavior, model selection, and messaging integration:

| Contribution | Scope |
|---|---|
| [`QwenLM/qwen-code#7258`](https://github.com/QwenLM/qwen-code/pull/7258), merged 2026-07-22 | Prevents a single-slot local endpoint from being reoccupied by the main agent while a background subagent is waiting to run. |
| [`QwenLM/qwen-code#7522`](https://github.com/QwenLM/qwen-code/pull/7522), merged 2026-07-23 | Keeps ACP model selectors aligned with the active authentication route instead of advertising an unrelated discontinued OAuth model. |
| [`QwenLM/qwen-code#7612`](https://github.com/QwenLM/qwen-code/pull/7612), merged 2026-07-23 | Preserves Telegram forum-topic routing for command and agent replies, including concurrent topics. |
| [`QwenLM/qwen-code#7666`](https://github.com/QwenLM/qwen-code/pull/7666), merged 2026-07-25 | Adds configurable SSE rate-limit retry delays while preserving existing defaults, with focused tests and build/lint/type checks. |

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

## Honest Boundaries

- An accepted upstream contribution is not official endorsement of this guide.
- The `llama.cpp` contribution fixes preset/router behavior; it does not claim
  to enable Strix Halo or improve Strix Halo inference speed.
- Qwen Code, OpenTelemetry, NVIDIA AICR, LocalAI, and vLLM GGUF work should not
  be presented as AMD or OEM collaboration.
- Guide performance and compatibility claims remain supported by the linked
  CSVs, raw logs, charts, commands, and caveats for each specific run.

The maintainer's public GitHub contribution history is available at
[`hogeheer499-commits`](https://github.com/hogeheer499-commits). This page lists
the accepted upstream work most relevant to local AI, runtime reliability, and
evidence quality rather than treating raw activity volume as proof.
