# Sponsor Roadmap

This roadmap turns missing tests and future work into fundable friction-removal projects. Each item is framed by the buyer uncertainty it removes and the public evidence it would create.

Status values:

- Existing evidence: evidence already exists, but follow-up may improve it.
- Needs hardware: cannot be completed well without a system, meter, or vendor access.
- Needs software access: blocked or limited by firmware, driver, ROCm, NPU, or toolchain availability.
- Needs repeat campaign: known path that needs controlled reruns on the current stack.
- Community welcome: useful if another Strix Halo owner can provide structured evidence.

| Priority | Test/project | Buyer uncertainty it removes | Why it matters to buyers | Why it matters to AMD/OEM/vendor | Hardware/software needed | Expected public deliverable | Status |
|----------|--------------|------------------------------|--------------------------|----------------------------------|--------------------------|----------------------------|--------|
| P0 | More Beelink validation | Does the documented setup still work after software updates? | Keeps known-good commands, versions, and expectations current. | Shows ongoing maintenance around a real retail system. | Existing Beelink GTR9 Pro, current Mesa, Ollama, `llama.cpp`, ROCm where relevant. | Updated smoke-test notes, benchmark deltas, raw logs, and CSVs. | Needs repeat campaign. |
| P0 | Wall-power measurement | What are real operating cost, heat, and efficiency under common local-AI workloads? | Helps buyers choose models/backends based on speed and efficiency, not only peak t/s. | Gives reviewers and OEMs credible efficiency evidence. | Reliable wall meter, smart plug, UPS export, or validated power tool; idle/load protocol. | Power/efficiency table, raw readings, chart, and caveats separating wall power from telemetry. | Needs hardware. |
| P1 | Framework Desktop validation | Do Beelink setup and performance assumptions transfer to Framework Desktop Strix Halo? | Helps buyers compare form factors and support paths. | Gives a major Strix Halo platform independent reproduction evidence. | Framework Desktop Strix Halo system or structured community report. | Framework validation section or community report with raw data. | Needs hardware / community welcome. |
| P1 | Other Strix Halo systems | Are results portable across GMKtec, Corsair, Minisforum, HP ZBook, and other Ryzen AI MAX systems? | Reduces the risk that the guide only applies to one box. | Helps vendors show where their platform matches, differs, or needs support. | Loaner/review systems or community reports with full metadata. | Cross-OEM community results, CSV updates, and caveats. | Existing community evidence; needs more hardware. |
| P1 | Buyer-focused known-good configuration testing | Which exact BIOS, OS, driver, backend, model, and quant path should a new buyer try first? | Converts scattered setup choices into a practical first-run path. | Reduces support friction and increases successful first impressions. | Current retail systems, public drivers, public firmware, common models. | Known-good configuration page with evidence links and failure notes. | Existing evidence; needs repeat campaign. |
| P2 | Windows native local-AI path versus Linux | Can buyers stay on Windows, or is native Linux the practical path? | Prevents buyers from choosing a painful OS path blindly. | Helps OEMs and developer-relations teams prioritize Windows, WSL2, driver, and setup work. | Same-machine Windows native, WSL2/HIP, and Linux test environments. | Windows-vs-Linux comparison doc with raw commands, versions, and caveats. | Needs hardware/software access; do not claim parity yet. |
| P2 | ROCm/vLLM improvements | Can Strix Halo serve OpenAI-compatible workloads reliably with modern ROCm/vLLM stacks? | Helps buyers decide whether the box can be a local API appliance. | Identifies software-stack gaps and engineering opportunities for ROCm, vLLM, and OEM support teams. | ROCm-compatible environment, known-good containers, current vLLM builds, guarded tests. | Updated [`VLLM_BASELINE.md`](VLLM_BASELINE.md), [`ROCM_VLLM_BUGWATCH.md`](ROCM_VLLM_BUGWATCH.md), logs, and serving benchmarks. | Existing baseline; needs software access and repeat campaign. |
| P2 | NPU / FastFlowLM / Ryzen AI software lane | Does the NPU help any realistic local-AI workflow on this hardware? | Clarifies whether buyers should care about NPU software today. | Helps AMD/Ryzen AI teams identify useful developer-facing proof and blockers. | XRT/FastFlowLM or equivalent user-space, public or early-access Ryzen AI software, test models. | NPU setup notes, smoke tests, failures, and any reproducible performance evidence. | Needs software access. |
| P3 | USB4 / multi-node / RPC scaling | When does clustering help, and when is one box faster? | Prevents buyers from buying multiple systems expecting automatic speedups. | Helps vendors frame multi-node use as capacity/scaling, not a simple headline t/s multiplier. | Multiple Strix Halo systems, USB4 network, reproducible RPC commands. | Expanded [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md), USB4 tuning notes, raw CSVs. | Existing community evidence; needs more hardware. |
| P3 | More community reproduction reports | Do independent users reproduce the setup across OS, kernel, Mesa, model, and chassis differences? | Increases trust and helps buyers calibrate expected variance. | Gives OEMs and reviewers real-world validation beyond one maintainer system. | Community contributors, issue templates, raw CSV/log attachments. | Updated [`COMMUNITY_RESULTS.md`](COMMUNITY_RESULTS.md), community CSVs, and contributor credits. | Community welcome. |
| P4 | Future Strix Halo successor comparison | How much better is the successor, and are setup steps preserved? | Helps buyers decide whether to buy now or wait. | Gives AMD/OEMs public evidence for generation-over-generation value. | Successor hardware, current Strix Halo baseline, matching models/backends. | Date-bound comparison report with raw evidence and no unsupported extrapolation. | TODO: future hardware. |

## Funding Logic

Each roadmap item is valuable because it removes a specific buyer uncertainty:

- setup uncertainty
- hardware portability uncertainty
- OS/backend uncertainty
- efficiency uncertainty
- software-stack maturity uncertainty
- multi-user or server-readiness uncertainty
- cross-OEM reproducibility uncertainty

That is the commercial leverage. Better public evidence makes AMD local-AI hardware easier to evaluate, easier to support, easier to review, and easier to buy.
