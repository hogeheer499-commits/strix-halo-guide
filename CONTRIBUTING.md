# Contributing

This guide is strongest when results come from more than one Strix Halo machine. Reports from Beelink, GMKtec, Corsair, Framework, HP ZBook, and other Ryzen AI MAX systems help readers know which setup choices are portable and which are machine-specific.

## Best Ways To Help

1. Share a benchmark from your own Strix Halo system.
2. Share wall-power or board-power measurements for an existing benchmark row.
3. Report a failed setup, slower result, crash, or regression.
4. Request a model/backend combination that would help real users choose what to run.
5. Open a PR that adds structured data, raw logs, docs fixes, or reproducibility improvements.
6. Share your own reproduction publicly if it would help other owners, while following the rules of the platform where you post.

Slower results are useful. Failed results are useful. Contradictions are useful if the setup details are complete.

## Sharing Your Results

Sharing is optional. It is never required for contributing to this repo, and contributors should not ask for upvotes, coordinate voting, or post the same text across many communities.

If you share a reproduction on Reddit, Hacker News, Discord, forums, blogs, or social media:

- post as yourself and disclose any connection to this repo
- lead with your own hardware, command, and result
- include raw CSV/logs or a GitHub issue/PR with the evidence
- keep community-reported rows separate from local Beelink headline claims
- link to the repo only when it is directly relevant to the discussion
- invite corrections and slower/failed reproductions
- avoid titles that imply a universal result across all Strix Halo systems

Useful places to share independent reproductions:

- Reddit r/LocalLLaMA, when the post is a real benchmark or setup report and follows subreddit rules
- Framework Community, especially for Framework Desktop rows
- Level1Techs and ServeTheHome forums for hardware, power, cooling, and server-use discussions
- Hacker News only for polished, evidence-first writeups

Suggested phrasing:

```text
I reproduced/checked one row from the Strix Halo local LLM guide on my own system. Here are my hardware, command, raw output, and where it matched or differed.
```

Do not frame sharing as marketing. The useful contribution is the measurement, not the link.

## High-Value Reports Wanted

These are currently the most valuable community contributions:

- Native Linux Vulkan/RADV results from Framework Desktop, GMKtec EVO-X2, HP ZBook, Beelink, and other Ryzen AI MAX systems.
- Same-model reproduction of the guide's Qwen3-Coder and Qwen3.6 rows.
- Windows native, WSL2/HIP, and Windows-vs-Linux comparisons on the same machine.
- Wall-power, smart-plug, UPS, or validated board-power measurements with idle and load readings.
- Long-context, RAG/prefill-heavy, server concurrency, and multi-user API workloads.
- ROCm/HIP, Lemonade, vLLM, DFlash/AWQ, NPU, or other backend experiments.
- Negative results: crashes, OOMs, driver failures, slower backends, and setup steps that did not work.

## Issue Templates

Use the template that best matches your contribution:

- [Benchmark report](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=benchmark-report.md): measured tokens/sec results.
- [Power / efficiency report](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=power-report.md): wall power, board power, UPS, smart-plug, or validated telemetry.
- [Model or backend request](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=model-request.md): a model, quant, backend, or serving route worth testing.
- [Bug report](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=bug-report.md): wrong commands, broken links, stale claims, or setup failures.
- [Suggestion](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=suggestion.md): guide structure, explanation, reproducibility, or usability improvements.
- [Impersonation or unsafe download report](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=impersonation-report.md): unofficial mirrors, installers, or repos using this guide's name.

Use [Discussions](https://github.com/hogeheer499-commits/strix-halo-guide/discussions) for early notes, setup questions, and comparison ideas that are not ready for a clean issue yet.

## Benchmark Metadata

Include enough detail for someone else to understand why your result matches or differs from the guide:

- device and memory size
- CPU/GPU name
- BIOS UMA setting
- IOMMU setting
- OS and kernel
- Mesa/RADV, AMDVLK, ROCm, Ollama, or container version
- backend and tool build/commit
- model name, source, quant, file name, and hash if available
- context length, prompt tokens, generated tokens, repeats, and concurrency
- exact command
- raw output, CSV, logs, screenshots, or attachments
- power profile, clocks, thermals, and background load if known

For `llama.cpp` rows, raw `llama-bench -o csv` output is ideal. For server/API rows, include request shape, prompt, generated token count, concurrency, TTFT if measured, and whether streaming was enabled.

## Power Metadata

For power reports, please include:

- meter/tool used and whether it measures wall power, board power, or APU/GPU telemetry
- sample interval and whether readings are event-based or polled
- idle baseline before and after the run
- sustained generation power window
- prompt-processing peak or sustained power window if measured
- tokens/J and J/token if calculated
- raw readings or exported CSV if possible
- cooling/fan profile, ambient temperature, and attached displays/peripherals if known

Do not mix APU `PPT` telemetry with wall-power claims. If the source is `amdgpu` PPT, label it as PPT, not total system power.

## How Data Is Used

Community rows are credited and kept separate from local Beelink headline claims unless they are explicitly promoted with clear scope. This keeps the guide useful without pretending every result came from the same machine.

Useful community reports may be added to:

- [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md)
- [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md)
- [`USB4_CLUSTER_TUNING.md`](USB4_CLUSTER_TUNING.md)
- [`data/community_results.csv`](data/community_results.csv)
- [`data/community_power.csv`](data/community_power.csv)
- raw provenance folders under [`data/raw/`](data/raw/)
- [`CONTRIBUTORS.md`](CONTRIBUTORS.md)

Headline claims require structured data, raw evidence, version details, and clear caveats. If a result is community-reported, it stays labeled that way.

## Pull Requests

PRs are welcome, especially for structured CSV additions, raw-data imports, reproducibility fixes, and documentation cleanup.

Before opening a PR:

1. Keep changes scoped to one topic.
2. Add raw evidence or source links for benchmark changes.
3. Credit community contributors and link to the original issue/comment/source.
4. Run the validator:

```bash
python3 scripts/validate_repo.py
```

If you cannot run the validator, say so in the PR.

## Style Guidelines

- Write in English.
- Keep claims bounded to the measured setup.
- Include dates and version numbers.
- Prefer clear commands and raw evidence over broad claims.
- Use `> blockquotes` for warnings and important caveats.
- Do not add binary downloads, model weights, installers, or unofficial executables.
- Do not paste API keys, tokens, private SSH keys, passwords, or private model URLs.
- When referencing community work, credit the author and link to the source.

## Contributor Credit

Benchmark reports in issues are welcome and will be credited when incorporated. PRs are even better for future datasets because GitHub also records commit-level contribution.

For repo safety, direct write access is not needed for benchmark contributions. Long-running contributors can start with issue triage, reproducibility review, or PR review before any broader access is considered.

## Code of Conduct

Be respectful and evidence-focused. The goal is to make local AI on Strix Halo easier to reproduce for everyone.
