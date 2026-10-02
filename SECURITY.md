# Security Policy

## Official Source

The canonical repository for this guide is:

```text
https://github.com/hogeheer499-commits/strix-halo-guide
```

The canonical website is `https://strixhaloguide.com/`.

This project publishes documentation, shell scripts, benchmark data, charts,
and source archives. It does not publish Windows installers, `.exe` files,
binary `.zip` packages, browser extensions, or model weights.

GitHub-generated source archives for tagged releases are expected. Extra binary
download assets are not part of this project unless they are explicitly
documented in this repository by the maintainer.

**Lookalike repositories and websites (checked 2026-09-25):** copies can use
this guide's name. At least one unrelated repository with the same name (plus a
GitHub Pages copy) links a `.zip` bundle and tells Windows users to run an
`.exe`. None of them is part of this project. Do not download or run files from
anywhere except the canonical repository. This guide does not ship `.exe` files
or binary `.zip` packages; the setup route is the reviewed shell script from the
canonical repository.

## What To Report

Please report:

- repos, websites, or packages that claim to be the official source for this guide;
- executable downloads or ZIP bundles promoted under this guide's name;
- modified setup commands that point away from this repository without saying so;
- benchmark tables copied from this guide while changing the hardware, model,
  quant, or backend provenance.

If the report does not include private credentials or sensitive logs, open a
GitHub issue here:

```text
https://github.com/hogeheer499-commits/strix-halo-guide/issues
```

Do not paste passwords, API keys, private SSH keys, or private model URLs into
public issues. If a public report needs redaction, describe the issue without
the secret and state that private details are available.

### Vulnerabilities In `setup.sh` Or Other Scripts

Report security issues in `setup.sh` or other scripts privately, not in a public
issue: use GitHub private vulnerability reporting on this repository (Security
tab, "Report a vulnerability") if it is enabled, or email
`hogeheer499@gmail.com`. Include the affected file and commit, and wait for a
response before publishing details.

## Verification

Before running commands from any Strix Halo guide, check that URLs point to:

```text
github.com/hogeheer499-commits/strix-halo-guide
raw.githubusercontent.com/hogeheer499-commits/strix-halo-guide
strixhaloguide.com
```

Third-party forks and mirrors may be useful, but they are not validated by this
project and should be treated as unofficial.

## Security Status Of Pinned Components

Checked 2026-09-30 (previous check 2026-09-25); the Open WebUI count was redone on
2026-10-02. This lists published advisories for runtimes the guide pins, qualified or
plans to test. It is not a full audit.
The guide has not tested any exploit, and "not tested here" below means exactly
that. Sources are the projects' own advisory lists and issue trackers, the
[NVD](https://nvd.nist.gov/) and AMD
[Product Security](https://www.amd.com/en/resources/product-security.html)
bulletins. Practical guidance built on this list is in
[`SECURE_LOCAL_AI.md`](SECURE_LOCAL_AI.md).

### Open WebUI

- **47 published advisories include the pinned 0.10.2 image (counted 2026-10-02).**
  Method: the count of published advisories whose affected-version range includes
  0.10.2, taken from Open WebUI's GitHub security advisories
  ([advisory list](https://github.com/open-webui/open-webui/security/advisories),
  read through the repository advisories API with `state=published`, checked
  2026-10-02). Of 165 published advisories, 47
  include 0.10.2: 15 rated high, 31 medium and 1 low, none critical. The newest
  advisory in the list was published on 2026-09-28. This counts advisories as
  published, not separate weaknesses. It does not say which of them can be used against
  a single-user, loopback-only setup: that was not assessed here, and no advisory was
  tested here.
- **Two groups.** 13 of the 47 (3 high, 10 medium) belong to the batch of 19 advisories
  published on 2026-09-27 and 2026-09-28; all 19 list 0.11.4 (released 2026-09-21) as
  the patched version. The other 34 (12 high, 21 medium, 1 low) were published between
  2026-08-02 and 2026-09-09 and list 0.11.0 or 0.11.1 as the patched version.
  CVE-2026-70491 (0.10.2 and earlier, fixed in 0.11.0; checked 2026-09-25) is one of the
  34. The digest-pinned 0.10.2 image in the README is in the affected range of all 47.
- **[GHSA-vpq8-f445-hcq7](https://github.com/open-webui/open-webui/security/advisories/GHSA-vpq8-f445-hcq7)**
  (high, CVSS 8.1, affects 0.7.0 up to but excluding 0.11.4): the community-stats
  message listener does not check `event.origin`. According to the advisory, any
  website visited by a signed-in user can obtain that user's session token, and
  no attacker account is needed. The advisory names community sharing
  (`ENABLE_COMMUNITY_SHARING`, enabled by default) as a precondition and says
  deployments with it disabled are not affected. The attack runs in the user's own
  browser, so binding the server to loopback does not appear to prevent it (our
  reading of the advisory, not tested here).
- **With default settings, `ENABLE_COMMUNITY_SHARING=False` does not change an existing data volume.** In Open WebUI's
  source (`backend/open_webui/models/config.py`, tags v0.10.2 and v0.11.4, read
  2026-10-02) the start-up step that stores default values says "Existing DB values
  take precedence over defaults", and the setting is stored as
  `ui.enable_community_sharing` (`backend/open_webui/config.py`; the variable defaults
  to on). A data volume on which Open WebUI has already started therefore keeps its
  stored value and, with default settings, ignores the variable. In the same source,
  `ENABLE_PERSISTENT_CONFIG=False` makes Open WebUI use the environment values and not
  store admin changes (read in the source, not tested here). For an existing volume with default
  settings, turn community sharing
  off in the admin settings: in the v0.10.2 source the General tab of the admin
  settings has an "Enable Community Sharing" switch
  (`src/lib/components/admin/Settings/General.svelte`). Neither the variable nor the
  switch was tested here; the menu path comes from the source, not from clicking through
  it.
- **One version rule.** The digest-pinned 0.10.2 image is the only Open WebUI version
  qualified here ([`RUNTIME_QUALIFICATION_2026-09-19.md`](RUNTIME_QUALIFICATION_2026-09-19.md)).
  A patched release (0.11.4 or later) is not qualified here; the row with `priority` 40
  ("Patched Open WebUI qualification and advisory recheck") in
  [`data/current_test_queue.csv`](data/current_test_queue.csv) tracks it. Releases
  0.11.1 to 0.11.3 are not patched releases: the affected ranges of all 19 advisories
  in the batch include 0.11.3 (for example GHSA-f9xp-mfmq-x6cg, high, 0.11.1 to
  0.11.3), and on 2026-10-02 no published advisory listed 0.11.4 as affected. If you
  upgrade anyway, pin the new image by digest (not a moving tag), rerun the acceptance
  checks of the September 19 qualification and report the result.
- **If you stay on the pin,** keep it bound to loopback, turn community sharing off as
  described above and do not create accounts for untrusted users. These steps reduce
  exposure. They do not make the pinned image a patched one.

### Ollama

- **CVE-2026-85180** (SSRF through cross-host redirects when pulling tensor
  layers): NVD status "Awaiting Analysis" (last modified 2026-09-10, checked
  2026-09-30). The linked VulnCheck advisory lists Ollama 0.30.0 through 0.33.2 as
  affected. That range includes the `setup.sh` fresh-install default 0.31.2, the
  Qwen3.8 route on 0.32.13 and the qualified existing 0.32.15 service.
  [ollama#17041](https://github.com/ollama/ollama/issues/17041) was still open on
  2026-09-30. NVD, VulnCheck and Ollama name no fixed release.
- **Redirect changes in 0.34.2 and 0.34.3:** Ollama PRs
  [#18512](https://github.com/ollama/ollama/pull/18512) (merged 2026-09-17,
  tightens redirect handling for registry requests in `x/transfer/download.go`,
  the file NVD points to; v0.34.2 is its merge commit) and
  [#18533](https://github.com/ollama/ollama/pull/18533) (merged 2026-09-19,
  cross-host redirects only among allowlisted hosts; in v0.34.3) change the code
  path of this CVE. Neither Ollama, NVD nor VulnCheck names them as the fix for this CVE, so this
  guide does not call CVE-2026-85180 fixed in any version.
- **0.31.2 is the lower bound for two further CVEs:** CVE-2026-102697 (NVD:
  0.14.0 up to but excluding 0.31.2; the experimental agent mode's Bash approval
  can be bypassed by control operators appended to an approved command, reachable
  through prompt injection) and CVE-2026-86289 (NVD: up to 0.31.1; integer
  overflow in the GGUF v1 string decoder, addressed in 0.31.2-rc1). At NVD the
  first is "Awaiting Analysis" and the second "Deferred" (checked 2026-09-30).
- **Cloud features:** Ollama's FAQ documents a local-only mode,
  `OLLAMA_NO_CLOUD=1` (or `disable_ollama_cloud` in `~/.ollama/server.json`),
  which turns off cloud models and web search
  ([FAQ](https://docs.ollama.com/faq), checked 2026-09-30). Documented, not tested
  here; `setup.sh` does not set it.

### Other runtimes the guide tests or plans to test

- **vLLM:** CVE-2026-90553 (NVD, "Analyzed": vLLM before 0.28.0, remote code
  execution through a processor loader that ignores `trust_remote_code`) and
  [GHSA-25q3-v2hm-8vpf](https://github.com/vllm-project/vllm/security/advisories/GHSA-25q3-v2hm-8vpf)
  (high, before 0.28.0, a negative token id can stop the engine). The vLLM build
  recorded in [`VLLM_BASELINE.md`](VLLM_BASELINE.md) (0.19.2rc1.dev113) is in that
  range. Newer vLLM has not been qualified here.
- **SGLang:** CVE-2026-86793 (NVD, 9.8 critical, status "Deferred"):
  unauthenticated pickle deserialization through `/update_weights_from_tensor`
  when no auth keys are configured; NVD names no versions. The hardening PRs
  [#39858](https://github.com/sgl-project/sglang/pull/39858) (merged 2026-09-17)
  and [#40259](https://github.com/sgl-project/sglang/pull/40259) (merged
  2026-09-19) are not part of the 0.5.20 release (GitHub's compare view shows
  that the v0.5.20 tag contains neither commit, checked 2026-09-30). Run SGLang
  only on loopback, with auth keys, and without that endpoint reachable (not tested
  here).
- **llama.cpp RPC:** upstream describes the RPC backend as a fragile,
  insecure proof of concept. CVE-2026-86317 (NVD, "Deferred": llama.cpp up to
  0.4.0, a remote reachable assertion in `rpc_server::deserialize_tensor`; the
  upstream issue was closed as inactive). A source reading of v0.5.0 on 2026-09-30
  showed no dimension check in that function (not tested).
  [GHSA-j8rj-fmpv-wcxw](https://github.com/ggml-org/llama.cpp/security/advisories/GHSA-j8rj-fmpv-wcxw)
  (CVE-2026-34159, critical, CVSS 9.8, published 2026-03-26, checked 2026-10-02) is titled
  "Unauthenticated RCE via GRAPH_COMPUTE buffer=0 bypass in llama.cpp RPC backend". The
  advisory says no authentication is required, only TCP access to the RPC server port
  (default 50052), to run commands as the server's user. It lists llama.cpp
  `<= b7991` as affected and names no patched version. It also says the RPC backend must
  be enabled at build time and defaults to localhost. The builds this guide currently
  uses (v0.4.1 and v0.5.0 = b11146) are newer than b7991, but the advisory names no patched version, so newer does not
  by itself mean fixed. This guide has not compared current builds with the advisory's
  description and has not tested them; whether they are affected is to verify. Use
  RPC only over a direct point-to-point link, never on a LAN or tailnet address; see
  [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md).
- **AMD's clustering playbooks** ([`amd/playbooks`](https://github.com/amd/playbooks),
  read 2026-09-30) start `rpc-server` and `llama-server` with `--host 0.0.0.0`,
  and the RCCL playbook starts a Ray head on port 6379, serves vLLM on `0.0.0.0`
  (port 7000) without an API key and connects Open WebUI with authentication set to
  none. The Ray documentation says that anyone who can reach the Ray dashboard,
  jobs or client ports can execute arbitrary code, and that
  token authentication (Ray 2.52.0 and later) does not replace network isolation
  ([Ray security](https://docs.ray.io/en/latest/ray-security/index.html)). Not tested
  here.
- **AMD-SB-6033 (RCCL, CVSS 7.7):** a compromised peer or an attacker on the same
  network may execute code in the RCCL process. AMD lists ROCm 7.14 (2026-07-15)
  as the mitigation and names only Instinct accelerators; whether a Ryzen AI Max
  system is affected is not stated. The bulletin gives CVE-2026-43598 in its
  description and CVE-2026-54974 in its product table (checked 2026-09-30).
- **AMD-SB-6034 (CVE-2026-43603, CVSS 6.9):** a local user can crash the kernel
  through a NULL pointer dereference in the AMD GPU Linux driver. AMD lists the
  Ryzen AI Max 300 series with "Radeon Software for Linux 26.13" (2026-07-20) as
  the mitigation; AMD gives no status for distribution kernels. Relevant to boxes
  shared with local users (checked 2026-09-30, not tested here).

### Text from another conversation

- **llama.cpp [#27148](https://github.com/ggml-org/llama.cpp/issues/27148)**
  (open since 2026-08-15, label "stale", checked 2026-09-30): with the default
  `--cache-ram` (8192 MiB) and `--cache-idle-slots` (on), `llama-server` can place
  an unrelated, finished conversation into the slot for a new request, so the
  model answers the wrong conversation while `cached_tokens` shows 0. Reporters
  reproduced it on Strix Halo (ROCm, `gfx1151`), including router mode with a
  single user. Their mitigation is `--cache-ram 0 --no-cache-idle-slots`; with
  several parallel slots they report needing both. A fix
  ([#27624](https://github.com/ggml-org/llama.cpp/pull/27624)) was open on
  2026-09-30. Not reproduced here; whether Vulkan builds or Ollama are affected is
  unknown.
- **Ollama [#18528](https://github.com/ollama/ollama/issues/18528) and llama.cpp
  [#29092](https://github.com/ggml-org/llama.cpp/issues/29092)** (open, reported
  2026-09-18): the ROCm `llama-server` bundled with Ollama 0.32.14 and 0.34.1
  emits earlier requests' text in later responses with Qwen3.6-35B-A3B and
  Qwen3.8-27B. A commenter on #29092 reports no leak with self-built master (HIP
  and Vulkan) in a three-request probe. The guide's Ollama setup runs Vulkan with
  HIP devices hidden; this guide has not reproduced the leak on either backend.
- **Preprint, not on Strix Halo:** the preprint
  [arXiv 2609.18526](https://arxiv.org/abs/2609.18526) (2026-09-16, not peer
  reviewed) tested llama.cpp commit 388d39f3e, LM Studio 0.4.21 and Ollama 0.20.5
  on an NVIDIA GPU. It reports that with `--slot-save-path` one client with a
  valid API key could restore another client's saved conversation (200 of 200
  trials), that a shared prompt-prefix cache gives a timing signal measurable over
  a WAN, that prompts stay readable in process memory, that LM Studio logs prompts
  in plain text with `logSensitiveData` enabled (no such traces with it
  disabled), and that Ollama left no prompt traces and made no outbound traffic in
  205 sessions. Claims of a third party; none reproduced here.

### Firmware

AMD ties fixes for the Ryzen AI Max 300 series to `StrixHaloPI-FP11` versions
that the system vendor must include in a BIOS; each bulletin says to ask the OEM
for the BIOS update. Checked 2026-09-30:

| AMD bulletin | Subject | Fixed in `StrixHaloPI-FP11` |
|---|---|---|
| [AMD-SB-4013](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-4013.html) | Client processor vulnerabilities, February 2026 | 1.0.0.1 (2025-03-20), 1.0.0.1c (2025-08-18) |
| [AMD-SB-7055](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-7055.html) | RDSEED failure on "Zen 5" | 1.0.0.2a (2025-11-25) |
| [AMD-SB-4017](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-4017.html) | Client processor vulnerabilities, May 2026 | 1.0.0.2a (2025-11-25); 1.0.0.2b (2025-12-29, listed under "Ryzen AI MAX") |
| [AMD-SB-7064](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-7064.html) | TPM reference code errata | 1.0.0.2c (fTPM only), 1.0.0.2d (Pluton, 2026-08-09) |

Update route according to the sources:

- **Framework Desktop:** BIOS 3.06 (2026-08-03) lists AMD PI 1.0.0.2c and six
  security fixes; Framework publishes it to LVFS for `fwupd`
  ([release page](https://resources.frame.work/downloads/desktop/amd-ryzen-ai-max-300/3.06/)).
- **HP Z2 Mini G1a and ZBook Ultra G1a:** listed on LVFS (Z2 Mini G1a system
  update 1.2.2.0). Which AMD PI that BIOS contains: to verify in HP's release notes.
- **Beelink, GMKtec, Minisforum, Bosgame, ASUS ROG Flow Z13:** searches on
  [LVFS](https://fwupd.org/lvfs/search) found no listing on 2026-09-30. LVFS device
  pages sit behind a bot check, so this is not proof. Use the vendor's BIOS
  downloads and release notes, and ask the vendor which AMD PI a BIOS contains.

The BIOS version and AMD PI of this guide's first-party test system are not
recorded for the published runs ([`REPRODUCIBILITY.md`](REPRODUCIBILITY.md)).

### What to do until fixed releases are qualified

- Keep Ollama on its loopback default (`127.0.0.1:11434`); do not expose an
  unauthenticated Ollama listener to a LAN, a tailnet or the internet.
- Pull models only from registries you trust.
- Open WebUI: the qualified image is the digest-pinned 0.10.2, which 47 published
  advisories include (see above); a patched release (0.11.4 or later) is not qualified
  here. Either way keep it bound to loopback, turn community sharing off (in the admin
  settings on an existing volume; from source, not clicked through here) and do not create accounts for untrusted users. If you
  upgrade, pin by digest, rerun the acceptance checks and report the result.
- Do not share one `llama-server` between people or agents of different trust
  without the cache settings above, and avoid `--slot-save-path` on shared servers.
- Keep `rpc-server`, Ray and vLLM off the LAN; see
  [`SECURE_LOCAL_AI.md`](SECURE_LOCAL_AI.md#clusters).
- Before pasting a community recipe, check its bind addresses (`0.0.0.0`), passwords
  stored in scripts, container privileges (`seccomp=unconfined`, `label=disable`,
  `SYS_PTRACE`, `--ipc=host`) and any closed binary that gets `/dev/kfd`; see the
  [recipe checklist](SECURE_LOCAL_AI.md#community-recipes-checklist) and
  [containers](SECURE_LOCAL_AI.md#containers-and-closed-binaries). The container
  commands in the README come from a third party's instructions, use moving tags and
  share your home directory.
- SSH: key login, `PasswordAuthentication no`, a firewall, an IPv6 check and a VPN or
  `ssh -L` tunnel instead of an open port. Check the effective settings with
  `sudo sshd -T` and `sudo ufw status numbered`, because a drop-in file or an existing
  broader firewall rule can undo your change; see [SSH](SECURE_LOCAL_AI.md#ssh).
- RAG and agents: treat documents, web pages and repository files as data, not
  instructions (OWASP LLM01:2025); see [RAG and agents](SECURE_LOCAL_AI.md#rag-and-agents).

Found an error or a missing advisory? See [What To Report](#what-to-report).
