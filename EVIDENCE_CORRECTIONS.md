# Curator Notes On Preserved Evidence

Reviewed September 13, 2026. These notes correct or qualify authored interpretation
while retaining original contributor submissions, model-card snapshots, filenames
and raw measurements. They do not claim new hardware validation.

## Ollama 0.32.3 Response-Hash Match

The [July 25 buyer qualification](data/raw/2026-07-25/ollama-0.32.3-buyer-qualification/)
states that all nine measured response hashes matched between Ollama 0.31.2 and
0.32.3. Seven of those nine visible responses are empty strings because the
256-token limit was reached before visible output, so the match mostly compares
empty responses. The bundle README now carries this qualification (September 26,
2026). The decode means (73.20 and 73.13 t/s) are unchanged.

## May 26 Control Build

The [control CSV](data/raw/2026-05-26/latest-llamacpp-b9334/control-b9179-qwen3-coder-q4-k-s-r20.csv)
records build **9172**, commit `1348f67c5`, despite `b9179` in its filename and
the bundle's summary. Its 97.61 tg128 / 1409.36 pp512 observation is unchanged.

## AgentWorld Retained-Run Disagreement

The [AgentWorld campaign](data/raw/2026-07-16/agentworld-iq4xs/)
authored summary reports 1182.77 pp / 65.65 tg, while its retained
`llama-bench.csv` reports 1184.175398 pp / 66.085646 tg. Those are not silently
substituted for one another; provenance of the exact authored-summary run remains
pending. A matching model name/size alone cannot resolve that disagreement.

## Nimo StepFun Denominators

The [StepFun MTP submission](data/raw/2026-06-03/community-nimo-issue4/STEPFUN-MTP-NUMBERS.md)
compares 26.0 tok/s with a **20.4** tok/s control: +27.45%. The adjacent 22.28
tok/s row in the guide is a separate result, not that denominator. The recorded
103.4→82.4 seconds is **20.31% less time**, or **25.49% higher reciprocal-time
rate**, not the imported 20.8% wording. Four of five versus five of five is a
20 percentage-point change in a small reported check; it does not isolate a
causal model-quality improvement.

## Qwen3.8 Community Elapsed Time

The [August 25 scope note](data/raw/2026-08-25/qwen38-community-runtime-update/README.md)
retains the original “18% lower elapsed time” wording. The actual 17.8→15.1
seconds is **15.17% less time**, or **17.88% higher reciprocal-time rate**, for
that three-prompt, 200-output-token comparison. The recorded times are unchanged.

## Nimo Gemma QAT Profiles And Topology

The [Gemma QAT submission](data/raw/2026-06-06/community-nimo-gemma4-qat-issue4/GEMMA4-QAT-NUMBERS.md)
changes KV precision: the 12B/26B plain controls use F16 KV and MTP uses Q8 KV;
31B plain uses Q8 KV and MTP uses F16 KV. Context settings also differ in the
recorded profiles. These are deployment-profile comparisons, not isolated MTP
toggles. “Matched QAT head” describes head compatibility, not all-variable matching.

The same source labels aggregate rows “2-slot” while recording a
`PARALLEL=1`-only MTP constraint. The original commands/process/request topology
needed to reconcile those statements is not retained here. Preserve the reported
rates as topology-unresolved; do not invent a two-server/router explanation.
A merged concurrency fix does not retroactively resolve these historical rows.

## Nimo Metadata And Thermal Limits

The submitted [Qwen 122B tuning](data/raw/2026-06-03/community-nimo-issue4/QWEN122B-MTP-TUNING-NUMBERS.md)
and [Coder-Next](data/raw/2026-06-03/community-nimo-issue4/QWEN3-CODER-NEXT-NUMBERS.md)
metadata includes a `qwen2` architecture label that is unverified for those exact
GGUFs. An upstream Hugging Face class name is not a substitute for inspecting
the actual GGUF `general.architecture` field.

The [supplemental thermal note](data/raw/2026-06-03/community-nimo-issue4/THERMAL-TELEMETRY-NIMO.md)
uses another OS-stack description but does not establish a separate physical
machine. Instrument, sampling and run alignment are incomplete. Its power,
noise and temperature values remain contributor reports, not verified wall-meter
measurements or proof of a power-limited rather than thermal mechanism.

## Captured NVIDIA Model Cards

The [NVFP4 quantization card](data/raw/2026-07-16/nemotron-omni-nvfp4-multimodal/quant-card.md)
mislabels the element format: NVFP4 uses **E2M1** elements with **E4M3** block
scales, per [NVIDIA's format explanation](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/).
This metadata correction does not change the measured model-load result.

The [Cascade 2 model-card example](data/raw/2026-07-16/nemotron-cascade2-iq4xs/upstream-model-card.md)
describes 1M context but configures `--max-model-len 262144`. That example is
configured for 262,144 tokens; this does not disprove the architecture's advertised
capacity or qualify a local 1M-token run.

## Qwen3 30B-A3B 2507 Table Rendering

The [June 2 direct scout](data/raw/2026-06-02/qwen3-30b-a3b-2507-direct-scout/README.md)
has four data columns but only three delimiter cells. The original capture is
preserved. This curator rendering supplies the missing delimiter without changing
values; the 98.51 t/s comparison is the **historical headline at that run**, not
the current best result.

| Model / quant | Shape | Result | Read |
| --- | --- | --- | --- |
| `Q4_K_S-3.61bpw` | `pp512/tg128`, r5 | 1272.62 pp512 / 94.80 tg128 | Below the then-current 98.51 t/s Qwen3-Coder headline |
| `Q4_K_S-3.61bpw` | `pp512/tg128`, r20 | 1272.56 pp512 / 94.37 tg128 | Near-miss confirmation |
| `Q4_K_S-3.61bpw` | `-p 0 -n 128`, r10 | 94.85 tg128 | Generation-only below the then-current headline |
| `IQ4_XS-3.63bpw` | `pp512/tg128`, r5 | 1418.53 pp512 / 99.80 tg128 | Crossed the old headline |
| `IQ4_XS-3.63bpw` | `pp512/tg128`, r20 | 1418.23 pp512 / 100.58 tg128 | Direct 100+ on this b9467 stack |
| `IQ4_XS-3.63bpw` | `-p 0 -n 128`, r20 | 100.40 tg128 | Generation-only confirmation |
| `IQ4_XS-3.63bpw` | `pp512/tg128`, r50 | 1416.03 pp512 / 100.04 tg128 | Longest confirmation in this scout |
