# Nimo Gemma 4 QAT Follow-Up

Community-submitted follow-up from boxwrench in issue #4.

- Source issue: https://github.com/hogeheer499-commits/strix-halo-guide/issues/4
- Source comment: https://github.com/hogeheer499-commits/strix-halo-guide/issues/4#issuecomment-4639263658
- Attachment copied here: `GEMMA4-QAT-NUMBERS.md`
- Date received: 2026-06-06
- Status: community-reported evidence

## What This Adds

This follow-up adds Gemma 4 QAT Q4_0 rows for 12B, 26B-A4B, and 31B on a Strix Halo APU / Nimo AI Mini PC context. It is valuable because it separates three issues that are easy to mix together:

- plain QAT main-model speed
- matched versus mismatched MTP assistant-head behavior
- single-stream MTP gains versus multi-slot serving limitations

## Scope

These rows are not first-party Beelink headline claims and are not direct replacements for the guide's `llama-bench` headline rows. They are community serving/tooling evidence for Gemma 4 QAT and Atomic TurboQuant MTP paths.

Important caveats from the submitted attachment:

- MTP rows require an Atomic `llama.cpp` TurboQuant fork with `gemma4_assistant` support.
- Stock `llama.cpp` b9360 does not load Gemma 4 MTP heads.
- Current Atomic Gemma 4 MTP path crashes at `PARALLEL=2`, so MTP rows are `PARALLEL=1`.
- Plain Gemma 4 26B-A4B QAT still wins the submitted 2-slot aggregate row at 90.9 tok/s.
- No thermal throttle was reported in the submitted rows.

Use `GEMMA4-QAT-NUMBERS.md` as the source of truth for detailed numbers and caveats.
