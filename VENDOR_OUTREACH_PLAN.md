# Vendor Outreach Plan

This plan keeps vendor outreach focused on adoption-friction evidence instead of generic sponsorship language.

## Positioning

Do not frame the repo as:

```text
I have 239 stars as of 2026-07-25, can I get hardware?
```

Frame it as:

```text
I maintain an independent Strix Halo local-AI setup and benchmark guide that reduces buyer setup friction with reproducible public evidence. I am looking for technical feedback, firmware/BIOS context, review or loaner access, or scoped collaboration to expand validated evidence across more systems.
```

The 239-star 2026-07-25 snapshot is useful as a small-niche demand signal, but the primary asset is the technical proof layer:

- reproducible setup steps
- known-good configurations
- known-bad paths
- raw logs and CSVs
- claim indexes
- community validation
- accepted upstream engineering with direct review and merge links
- separated direct, server, MTP, community, Windows, ROCm/vLLM, power, RPC, and failure evidence

## First-Wave Targets

| Priority | Target | Why now | Best first ask |
| ---: | --- | --- | --- |
| 1 | Beelink | Primary measured system is the GTR9 Pro. Existing first-party data makes this the cleanest first vendor. | BIOS/firmware/UMA/IOMMU guidance, factual setup corrections, technical contact, possible review/loaner or scoped follow-up campaign. |
| 2 | GMKtec | Community data already reproduced important rows on EVO-X2 and a tuned report touched 100 t/s. | Confirm platform guidance, invite official technical context, request review/loaner validation for 96GB/128GB variants. |
| 3 | Corsair | Three Corsair AI Workstation 300 systems already reproduced the Qwen3-Coder path and added wall-power/RPC data. | Technical validation and reviewer/DevRel contact; possible official context around power/cooling/workstation positioning. |
| 4 | Nimo | Community bundle added compact-chassis large-model/server evidence and Gemma QAT/MTP follow-up rows. | Setup metadata review, compact-chassis thermal/power context, possible direct validation. |
| 5 | Framework | Buyers want Framework Desktop rows; evidence is still missing locally. | Loaner/review access or community reproduction path; compare setup portability and buyer-first docs. |
| 6 | Minisforum | Windows LM Studio/MS-S1-Max community row exists, but native Linux same-shape validation is missing. | Windows/Linux setup context, native Linux reproduction, firmware/BIOS guidance. |
| 7 | AMD / ROCm / Ryzen AI DevRel | Software-stack maturity affects adoption across every OEM. | ROCm/vLLM/NPU/Ryzen AI technical contacts, driver notes, known blockers, and reproducibility feedback. |
| 8 | Reviewers / publications | The guide can serve as a background evidence pack for Strix Halo local-AI coverage. | Corrections, independent reproduction, links, or collaboration on a measured review workflow. |

## What To Ask For

Start with low-friction technical asks:

- "Can you confirm or correct the recommended BIOS/UMA/IOMMU settings?"
- "Is there a current firmware or board-revision note buyers should know?"
- "Do you have Linux/Vulkan/RADV/Ollama/llama.cpp setup guidance that should be reflected?"
- "Can you route me to a product, engineering, or developer-relations contact?"

Then ask for higher-leverage support:

- review or loaner unit
- early BIOS/firmware context where disclosure is allowed
- scoped benchmark campaign sponsorship
- hardware for cross-OEM reproduction
- wall-power measurement support
- Windows/Linux validation support

## Evidence Pack To Link

- Main guide: <https://github.com/hogeheer499-commits/strix-halo-guide>
- One-page brief: <https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/ONE_PAGE_BRIEF.md>
- Partnership overview: <https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/PARTNERSHIP.md>
- Traction and evidence: <https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/TRACTION.md>
- Accepted upstream contributions: <https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/UPSTREAM_CONTRIBUTIONS.md>
- Community results: <https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/COMMUNITY_RESULTS.md>
- Claim index: <https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/data/headline_claims.csv>
- Disclosure policy: <https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/VENDOR_DISCLOSURE.md>

## Outreach Rules

- Keep the first message short.
- Lead with buyer/setup friction, not self-promotion.
- Mention the dated 239-star snapshot once at most.
- Describe the `llama.cpp` merge accurately as accepted preset/router maintenance, not as a Strix Halo performance fix.
- Avoid claiming vendor endorsement.
- Avoid asking for free hardware as the main point.
- Always say results remain independent and disclosed.
- Ask for routing if the first contact is not the right person.

## Follow-Up Timing

- First follow-up: 5-7 business days after the first message.
- Second follow-up: 10-14 business days later only if the vendor is important.
- Stop after two unanswered follow-ups unless a new technical reason appears.

## Second-Wave Hook: Accepted Upstream Engineering

The accepted `llama.cpp` contribution is a legitimate new reason to contact or
follow up with vendors, AMD teams, and reviewers. Use the recognizable project
name to earn attention, then state the scope immediately:

```text
A fix I submitted to llama.cpp was reviewed and merged upstream. It is
preset/router maintenance, not a Strix Halo performance patch. Its relevance
here is engineering follow-through: reproducible software friction can become
tested buyer guidance or a narrowly scoped upstream change.
```

For existing AMD and Beelink outreach, reply in the original thread using the
specific follow-ups in [`OUTREACH_TEMPLATES.md`](OUTREACH_TEMPLATES.md).

For a new OEM or reviewer:

- include `llama.cpp` in the subject once;
- lead the body with buyer/setup friction, not personal status;
- link [`UPSTREAM_CONTRIBUTIONS.md`](UPSTREAM_CONTRIBUTIONS.md);
- ask for one concrete next step: technical routing, a second-system
  validation, firmware context, or review/loaner access;
- do not open a separate GitHub Discussion solely to announce contributor
  status.

The strongest vendor interpretation is not "the maintainer has a badge." It is
"this project can move from a reproducible field problem to public guidance and
reviewed upstream work."

## Success Criteria

Good outcomes are not only sponsorship:

- factual correction from a vendor
- BIOS/firmware guidance
- driver or ROCm contact
- review/loaner hardware
- community reproduction from a vendor system
- permission to quote technical guidance
- scoped campaign funding
- reviewer using the guide as background evidence

Any of these can make the guide more valuable than another 50 passive stars.
