# Outreach Templates

These templates are meant to be edited before sending. Keep the claims tied to the repo and avoid inventing traction, sponsors, endorsements, or buyer impact.

Public project home:

```text
https://strixhaloguide.com/
```

Vendor and reviewer overview:

```text
https://strixhaloguide.com/partners/
```

Canonical technical evidence:

```text
https://github.com/hogeheer499-commits/strix-halo-guide
```

## AMD Developer Relations / Ryzen AI / ROCm Email

Subject: Independent Strix Halo local-AI guide with reproducible benchmark evidence

```text
Hello [name/team],

I maintain an independent AMD Strix Halo / Ryzen AI MAX+ 395 local-AI setup and benchmark guide:

https://strixhaloguide.com/

The project is primarily technical: setup steps, backend guidance, benchmark reports, raw logs, CSVs, charts, reproducibility notes, and community validation. The commercial value is that it reduces buyer and developer friction around AMD local-AI hardware. Buyers are interested in the hardware, but the setup path across BIOS settings, Linux/Windows, Vulkan/RADV, ROCm, Ollama, llama.cpp, vLLM, model formats, and quantization can be difficult to trust.

I can produce independent, reproducible, public technical evidence that reduces adoption friction and helps buyers understand the value and limits of the hardware.

Useful collaboration could be early technical context, firmware/software guidance, ROCm/Ryzen AI contacts, review hardware, or sponsorship for a specific benchmark campaign. Results would remain independent and disclosed; this is not paid-positive coverage.

If this is better routed to another AMD Developer Relations, Ryzen AI, ROCm, or AI-PC contact, could you point me to the right person?

Best,
[name]
GitHub: https://github.com/hogeheer499-commits
Email: hogeheer499@gmail.com
```

## AMD Follow-Up After Accepted `llama.cpp` Contribution

Use this as a reply to the original email so the earlier context stays in the
same thread. If a new subject is required, use:

```text
llama.cpp contributor: reproducible Ryzen AI Halo field evidence
```

```text
Hi AMD AI Developer Program team,

A quick, relevant update since my earlier project submission: a small fix I submitted to llama.cpp has now been reviewed and merged upstream.

https://github.com/ggml-org/llama.cpp/pull/25643

It is preset/router maintenance, not a Strix Halo performance patch. The reason I am sharing it is that it shows the guide is not only collecting downstream benchmark results. When a reproducible software issue is clear enough, I can take it through implementation, focused validation, upstream review, and merge.

The full verified contribution record is here:
https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/UPSTREAM_CONTRIBUTIONS.md

The short project and collaboration overview is here:
https://strixhaloguide.com/partners/

I would still appreciate help routing the Strix Halo guide and the AMD/RADV evidence to the right Ryzen AI, RADV/Vulkan, ROCm, or project-showcase contact. The goal remains practical: reduce setup and buying friction by turning real-system findings into public guidance and, where appropriate, upstream improvements.

Best,
Jesse van Dijk
hogeheer499-commits
Strix Halo guide maintainer
```

## Beelink Product Marketing Email

Subject: Independent Beelink GTR9 Pro local-AI evidence and setup-friction feedback

```text
Hello [name/team],

I maintain an independent Strix Halo local-AI guide that currently uses a Beelink GTR9 Pro as the primary measured system:

https://strixhaloguide.com/

The guide is evidence-backed rather than promotional: it documents setup, backend choices, raw benchmark artifacts, charts, reproducibility notes, and caveats. It helps buyers understand how to get useful local-AI workloads running instead of piecing together scattered BIOS, OS, driver, backend, and model advice.

The repo reached 239 GitHub stars in a small hardware/software niche as of the 2026-07-25 GitHub API snapshot, but the more important value is practical: it reduces adoption friction for buyers and reviewers. A strong AI PC is easier to evaluate, trust, recommend, and purchase when buyers can reproduce a known-good setup and understand the limits.

The project is not only downstream documentation. I also have accepted
upstream contributions in `llama.cpp` and other AI infrastructure, so
reproducible software findings can become tested guidance or narrowly scoped
upstream work. Verification:
https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/UPSTREAM_CONTRIBUTIONS.md

Because the Beelink GTR9 Pro is the primary measured system, Beelink feedback would be especially useful on:

- recommended BIOS / UMA / IOMMU settings for local AI
- current firmware and board-revision guidance
- any known local-AI setup notes for Linux/Vulkan/RADV/Ollama/llama.cpp
- technical corrections to the current Beelink setup notes
- possible review/loaner access or a scoped benchmark campaign for future validation

All vendor involvement would be disclosed, and results would remain independent, including negative findings if they are accurate.

Would you be open to discussing this, or routing me to the right product/technical contact?

Best,
[name]
GitHub: https://github.com/hogeheer499-commits
Email: hogeheer499@gmail.com
```

## Beelink Follow-Up After Accepted `llama.cpp` Contribution

Send this as a reply to the first Beelink message. If it cannot remain in the
same thread, use:

```text
llama.cpp contributor: reducing GTR9 Pro local-AI buyer friction
```

```text
Hi Beelink team,

A short update since my earlier GTR9 Pro collaboration email: a fix I submitted to llama.cpp has now been reviewed and merged upstream.

https://github.com/ggml-org/llama.cpp/pull/25643

The change itself is preset/router maintenance, not a GTR9 Pro performance claim. What it adds to the collaboration case is practical engineering follow-through: I can reproduce software friction, document it for buyers, and where the scope is clear, take a fix through validation and upstream review.

The GTR9 Pro remains the primary system behind the guide. I would still like to connect with the right Beelink product or engineering contact about a better-validated “retail box to working local AI” buyer path, including BIOS/firmware guidance and possible access to a second Beelink configuration.

Project:
https://strixhaloguide.com/partners/

Canonical technical evidence:
https://github.com/hogeheer499-commits/strix-halo-guide

Verified upstream work:
https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/UPSTREAM_CONTRIBUTIONS.md

Best,
Jesse van Dijk
hogeheer499-commits
Strix Halo guide maintainer
```

## OEM / System Vendor Email

Preferred subject:

```text
llama.cpp contributor: reduce local-AI buyer friction for [system]
```

System-specific alternative:

```text
Tested local-AI buyer path for [vendor/system]
```

```text
Hello [name/team],

I maintain an independent AMD Strix Halo / Ryzen AI MAX+ local-AI setup and benchmark guide:

https://strixhaloguide.com/

The guide helps buyers and developers answer practical questions: which OS and backend to start with, which models are realistic, how Ollama compares with direct llama.cpp, what remains experimental in ROCm/vLLM, and what benchmark claims are backed by raw evidence.

I also have accepted upstream contributions in llama.cpp and other AI infrastructure. That matters for a hardware collaboration because findings do not have to stop at screenshots or downstream complaints: a well-scoped software issue can become reproducible buyer guidance and, where appropriate, reviewed upstream work.

https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/UPSTREAM_CONTRIBUTIONS.md

Canonical technical evidence:
https://github.com/hogeheer499-commits/strix-halo-guide

I am interested in validating [vendor/system] so buyers can see how it compares with existing Beelink, Corsair, and GMKtec evidence in the repo. This would reduce adoption friction for your hardware by turning setup and benchmark work into public, reproducible technical evidence.

Collaboration could be a technical contact, loaner/review unit, early firmware/software access, scoped benchmark campaign, or sponsored but independent technical report. Hardware or sponsorship would be disclosed clearly, and conclusions would remain independent.

Could you route me to the right product marketing, developer relations, or engineering contact?

Best,
[name]
GitHub: https://github.com/hogeheer499-commits
Email: hogeheer499@gmail.com
```

## Reviewer / Newsletter / YouTube Creator Message

Subject: Strix Halo buyer guide by a llama.cpp contributor

```text
Hello [name],

I maintain an independent Strix Halo / Ryzen AI MAX+ 395 local-AI guide:

https://strixhaloguide.com/

It may be useful background for your AI-PC or local-AI coverage because it focuses on reproducible setup, raw benchmark evidence, backend tradeoffs, and practical buyer questions rather than only headline speed claims.

The maintainer record now also includes accepted upstream work in llama.cpp and other AI infrastructure. The llama.cpp change is not a Strix Halo speed patch; its value is independent evidence that software findings can be reproduced, tested, reviewed, and merged rather than only reported downstream.

https://github.com/hogeheer499-commits/strix-halo-guide/blob/main/UPSTREAM_CONTRIBUTIONS.md

Canonical technical evidence:
https://github.com/hogeheer499-commits/strix-halo-guide

The main point: powerful local-AI hardware still has adoption friction when buyers cannot easily reproduce working setups. The guide documents a path through that friction with setup steps, benchmark data, raw logs, charts, community validation, and caveats.

If you cover Strix Halo systems, I would be interested in corrections, independent reproduction, or a link where the guide helps your audience understand setup and benchmark context. Results and vendor relationships remain independent and disclosed.

Best,
[name]
GitHub: https://github.com/hogeheer499-commits
Email: hogeheer499@gmail.com
```

## Short LinkedIn / DM Version

```text
Hi [name] - I maintain an independent AMD Strix Halo / Ryzen AI MAX+ local-AI setup and benchmark guide:

https://strixhaloguide.com/

It turns scattered setup and benchmark knowledge into reproducible public evidence: setup steps, backend guidance, raw logs/CSVs/charts, caveats, and community validation.

The commercial value is reduced adoption friction for AMD local-AI hardware. I can produce independent, reproducible, public technical evidence that helps buyers understand the value and limits of your hardware. Collaboration could be technical feedback, early firmware/software access, review hardware, or a scoped benchmark campaign, with disclosure and independent conclusions.

Could you point me to the right person?
```

## Follow-Up Email After No Response

Keep the existing email thread and subject. Do not send a generic bump when
there is a real technical update; use the AMD or Beelink contribution follow-up
above instead.

Generic subject:

```text
Re: Independent Strix Halo local-AI guide
```

```text
Hello [name],

Just following up on the Strix Halo local-AI guide:

https://github.com/hogeheer499-commits/strix-halo-guide

The short version is that the project reduces buyer/developer setup friction by turning Strix Halo local-AI setup and benchmark work into reproducible public evidence. I am looking for the right contact for technical feedback, hardware validation, early firmware/software context, or a scoped independent benchmark collaboration.

If this is not your area, could you route me to the right product, developer-relations, or engineering contact?

Best,
[name]
```

## Route-Me-To-The-Right-Person Message

```text
Hello [name],

I maintain an independent AMD Strix Halo / Ryzen AI MAX+ local-AI setup and benchmark guide:

https://strixhaloguide.com/

It produces reproducible public evidence that reduces buyer setup friction around local-AI hardware. I am trying to reach the right person for technical feedback, review hardware, early firmware/software context, or an independent benchmark collaboration.

Could you route me to the right product marketing, developer relations, or engineering contact?

Thanks,
[name]
```
