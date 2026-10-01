# Securing A Local AI Box

Checked 2026-09-30. This is a checklist for a Strix Halo local-AI box (Ollama, `llama.cpp`, Open
WebUI, containers) built from public documentation, advisories and issue threads. It is not a
security audit or a guarantee. The guide has not tested any exploit or attack described here, and
"not tested here" marks what no one has checked on this guide's hardware. Dated advisories for the
pinned components are in [`SECURITY.md`](SECURITY.md#security-status-of-pinned-components).

## The Short Version

1. Keep model servers on loopback. Ollama's local API needs no authentication (Ollama docs, checked
   2026-09-30), so the network is the only barrier.
2. Do not rely on ufw alone: ports published by Docker bypass it, and Tailscale accepts tailnet
   traffic early (both documented below). Test from a second device.
3. Open WebUI: the advisories list 0.11.4 as the patched version (not qualified here); turn community
   sharing off (GHSA-vpq8-f445-hcq7).
4. A shared `llama-server` can answer with another conversation's text (llama.cpp#27148). The
   reporters' mitigation is `--cache-ram 0 --no-cache-idle-slots` (not tested here).
5. Treat documents, web pages and repository files as data, never as instructions (OWASP
   LLM01:2025).
6. Before pasting a community recipe, check its bind addresses, passwords, container privileges and
   binaries.
7. `rpc-server` and Ray have no safe LAN mode: use a direct link only.
8. SSH: key login, `PasswordAuthentication no`, a firewall, and a VPN or `ssh -L`.
9. AMD firmware fixes reach a BIOS only when the system vendor ships them: check your update route.
10. "Local" is not automatically "private": cloud model tags, logs, caches and tools can move data
    off the box.

## Network Exposure

- **Bind address.** A native Ollama install binds `127.0.0.1:11434` by default
  ([FAQ](https://docs.ollama.com/faq), checked 2026-09-30). The official Docker image sets
  `OLLAMA_HOST=0.0.0.0:11434` ([Dockerfile](https://github.com/ollama/ollama/blob/main/Dockerfile),
  checked 2026-09-30).
- **No authentication.** The local Ollama API requires none; API keys apply to ollama.com
  ([docs](https://docs.ollama.com/api/authentication), checked 2026-09-30). Anyone who can reach the
  port can use the box and its models.
- **Open WebUI in Docker.** The README's bridge-network command needs a non-loopback Ollama
  listener, and widening the listener puts an API without authentication on the network. The README
  documents a host-network alternative that is untested here. Decide the bind address first, then
  add a firewall.
- **See what listens, then test from another device.** `sudo ss -ltnp` lists listeners; `0.0.0.0`,
  `*` and `[::]` are reachable from other machines unless a firewall stops them.
  `curl -m 5 http://<box-address>:11434/api/version` from another device should time out; a check on
  the box itself cannot see what a LAN or tailnet sees.
- **Docker and ufw.** Docker routes published ports through the nat table, before the INPUT chain
  that ufw uses, so ufw rules do not apply to them
  ([Docker docs](https://docs.docker.com/engine/network/packet-filtering-firewalls/), checked
  2026-09-30). Publish to loopback, as the README does: `-p 127.0.0.1:3000:8080`.
- **Tailscale and ufw.** In the default netfilter mode Tailscale's firewall rules accept traffic
  arriving on `tailscale0` early
  ([netfilter modes](https://tailscale.com/docs/reference/netfilter-modes), checked 2026-09-30). A
  request to prevent this has been open since 2024-04-13
  ([tailscale#11717](https://github.com/tailscale/tailscale/issues/11717)), and in `nodivert` mode a
  bug removes hand-placed `ts-input` rules at start-up
  ([tailscale#12185](https://github.com/tailscale/tailscale/issues/12185), open since 2024-05-18).
  Our reading: a ufw rule alone may not block the tailnet path. This guide has no published test of
  it, so run the cross-device check from a tailnet device. Tailscale's
  [access rules](https://tailscale.com/docs/features/access-control) are another layer (not tested
  here).
- **IPv6 and remote use.** If `ss` shows `[::]:<port>`, check IPv6 too; a rule written only for IPv4
  would not cover it (to verify on your system). For remote use, prefer an SSH tunnel to an open
  port; see [SSH](#ssh).
- **Cloud features.** Ollama cloud model tags and web search run on Ollama's service, not on your
  box ([cloud docs](https://docs.ollama.com/cloud), checked 2026-09-30). `OLLAMA_NO_CLOUD=1` turns
  them off ([FAQ](https://docs.ollama.com/faq)); documented, not tested here.

## Shared Servers

One box serving people or agents of different trust has more risks than a single-user box.
Everything below is a claim from a public source, not a result of this guide.

- **Open WebUI.** 19 advisories were published on 2026-09-27 and 2026-09-28, all patched in 0.11.4.
  GHSA-vpq8-f445-hcq7 lets any website a signed-in user visits obtain that user's session token when
  community sharing is enabled (the default). Set `ENABLE_COMMUNITY_SHARING=False` on a new
  container (not tested here) and do not create accounts for untrusted users. Details:
  [`SECURITY.md`](SECURITY.md#open-webui).
- **`llama-server` prompt cache.** With default settings an unrelated, finished conversation can be
  restored into a slot for a new request
  ([llama.cpp#27148](https://github.com/ggml-org/llama.cpp/issues/27148), open on 2026-09-30).
  Reporters reproduced it on Strix Halo (ROCm), once with a single user, and mitigate with
  `--cache-ram 0 --no-cache-idle-slots`. Not reproduced here; Vulkan and Ollama are unconfirmed.
- **Ollama's ROCm bundle.** Reports describe earlier requests' text appearing in later responses
  with the ROCm server bundled in Ollama 0.32.14 and 0.34.1
  ([ollama#18528](https://github.com/ollama/ollama/issues/18528),
  [llama.cpp#29092](https://github.com/ggml-org/llama.cpp/issues/29092)). The guide's Ollama setup
  uses Vulkan; this guide has not reproduced the leak.
- **Preprint** ([arXiv 2609.18526](https://arxiv.org/abs/2609.18526), 2026-09-16, not peer reviewed,
  tested on an NVIDIA GPU, not on Strix Halo): with `--slot-save-path`, a client with a valid API
  key restored another client's saved conversation in 200 of 200 trials; a shared prompt-prefix
  cache gave a timing signal; prompts stayed readable in process memory; LM Studio logged prompts in
  plain text while `logSensitiveData` was enabled. Practical reading: no `--slot-save-path` on a
  shared server, one instance per trust group, that LM Studio setting off (to verify in your
  version), no untrusted local users. AMD-SB-6034 also describes a kernel crash a local user can
  trigger ([`SECURITY.md`](SECURITY.md#other-runtimes-the-guide-tests-or-plans-to-test)).

## Community Recipes Checklist

Public recipes, scripts and forum guides are written for a working result. These patterns were seen
in public community recipes on 2026-09-30; none is linked here on purpose, because the point is the
pattern, not the author.

- **Bind addresses.** Look for `--host 0.0.0.0`, `-p 8000:8000` (all interfaces), `*_BIND=0.0.0.0`
  and `OLLAMA_HOST=0.0.0.0`. Prefer `127.0.0.1` or `-p 127.0.0.1:<port>:<port>`.
- **Passwords in scripts.** A sudo password in a wrapper script (for example through `sudo -S`) is
  readable by anyone who can read the file. Use a systemd unit, or a narrowly scoped sudoers rule
  you have reviewed.
- **Container privileges.** Check for `--security-opt seccomp=unconfined`, `label=disable`,
  `--cap-add SYS_PTRACE`, `--ipc=host`, `--network=host`, `--privileged` and `--group-add sudo`.
  Each removes a layer of isolation.
- **IOMMU.** Some recipes set `amd_iommu=off`. Besides the NPU and suspend limits this guide already
  documents, it turns off the IOMMU that the kernel's USB4 and Thunderbolt documentation names as
  the protection against DMA by connected devices
  ([kernel docs](https://docs.kernel.org/admin-guide/thunderbolt.html), checked 2026-09-30). Linux
  7.4's PerfOpt may narrow the speed gap; Phoronix measured 2 to 4% on Strix Halo
  ([review](https://www.phoronix.com/review/amd-perfopt), 2026-09-29, claim of a third party, not
  measured here). See the [setup page](https://strixhaloguide.com/amd-strix-halo-setup/).
- **Versions.** Pin an image digest or a release tag, and read a script before you run it.

## Containers And Closed Binaries

- **This guide's own commands.** The Distrobox/Podman commands in the README (Phase 7 and 8) use
  `--security-opt seccomp=unconfined`, and Step 7.2 adds `--group-add sudo`. The toolbox's own
  README documents the same flags
  ([amd-strix-halo-toolboxes](https://github.com/kyuz0/amd-strix-halo-toolboxes), checked
  2026-09-30). This guide has not tested whether the images work without them. The pinned Unsloth
  command in [`UNSLOTH_STRIX_HALO.md`](UNSLOTH_STRIX_HALO.md) uses an image digest but also
  `seccomp=unconfined`; the `:rocm-7.2` and `:stable` tags in the README commands are not digests.
  Record the digest of the image you ran (`podman image ls --digests`) and treat a rebuilt moving
  tag as a new, unreviewed artifact.
- **Home directory.** Distrobox documents that it integrates the container with the host and does
  not aim at isolation: the container has complete access to your home directory
  ([distrobox.it](https://distrobox.it/), checked 2026-09-30). `distrobox create --home <path>`
  selects a separate home
  ([create docs](https://github.com/89luca89/distrobox/blob/main/docs/usage/distrobox-create.md));
  not tested here with the guide's images.
- **Closed-source engines cannot be audited.** If you run an engine distributed as a binary, ask
  what it is allowed to access. A container with `/dev/kfd` and `/dev/dri` has direct GPU access,
  `--ipc=host` shares the host's IPC namespace, and the container may also see your files and
  network. Ask for the license terms, what network and file access the vendor documents, and how
  updates are delivered. This guide has not tested or reviewed any such engine.

## Clusters

- **`rpc-server`.** Upstream describes the RPC backend as a proof of concept and says: "Never run
  the RPC server on an open network or in a sensitive environment!"
  ([tools/rpc/README.md](https://github.com/ggml-org/llama.cpp/blob/master/tools/rpc/README.md),
  checked 2026-09-30). It has no authentication. CVE-2026-86317 (NVD, llama.cpp up to 0.4.0) is a
  remote crash through a malformed tensor. Bind it only to a direct point-to-point link such as the
  USB4 `thunderbolt-net` interface, never to a LAN or tailnet address. All nodes need the same build
  (RPC protocol 7 from v0.5.0).
- **AMD's playbooks.** The `clustering-rpc-server` playbook starts `rpc-server` and `llama-server`
  with `--host 0.0.0.0`. The `clustering-rccl` playbook starts a Ray head on port 6379, serves vLLM
  on `0.0.0.0` without an API key and connects Open WebUI with authentication set to none (both read 2026-09-30,
  [amd/playbooks](https://github.com/amd/playbooks)). The playbook text read on 2026-09-30 contains no exposure note (not exhaustively checked). If vLLM
  must listen beyond loopback, limit it to the cluster link and set an API key (`--api-key`). Not
  tested here.
- **Ray.** Ray's documentation says anyone who can reach the dashboard, jobs
  or client ports can execute arbitrary code, and that token authentication (Ray 2.52.0 and later)
  does not replace a controlled network
  ([Ray security](https://docs.ray.io/en/latest/ray-security/index.html), checked 2026-09-30). Keep
  6379 and 8265 off the LAN (8265 is the dashboard's default port,
  [Ray dashboard documentation](https://docs.ray.io/en/latest/cluster/configure-manage-dashboard.html),
  checked 2026-09-30). The playbook also sets `RAY_memory_monitor_refresh_ms=0`, which turns
  Ray's memory monitor off because host and GPU share one memory pool; what that costs when a model
  is too large is not tested here.
- **RCCL.** AMD-SB-6033 (checked 2026-09-30) lists ROCm 7.14 as the mitigation for a remote code
  execution risk between cluster peers; the bulletin names only Instinct accelerators, so whether
  Ryzen AI Max is affected is unknown.

## SSH

The README's Phase 10 installs `openssh-server` and `fail2ban` and disables root login. Passwords,
firewall and IPv6 are not covered there.

1. Create a key on your client (`ssh-keygen -t ed25519`) and install it with
   `ssh-copy-id <user>@<box>`. Confirm key login in a second terminal.
2. Then set `PasswordAuthentication no` in `/etc/ssh/sshd_config` and reload `ssh` while the first
   session stays open ([sshd_config](https://man.openbsd.org/sshd_config), checked 2026-09-30).
3. Allow port 22 only from your LAN or VPN
   (`sudo ufw allow from <lan-subnet> to any port 22 proto tcp`) and do not forward port 22 on your
   router. `fail2ban` reduces noise; it does not replace this.
4. Check IPv6: `ss -ltn 'sport = :22'` showing `[::]:22` means a global address may be reachable.
   Whether your router blocks inbound IPv6 is router-specific; test from outside your network.
5. For Open WebUI from another machine, tunnel instead of opening a port:
   `ssh -L 3000:127.0.0.1:3000 <user>@<box>`, then open `http://localhost:3000` on the client
   ([ssh](https://man.openbsd.org/ssh)).

Steps 1 to 5 are standard OpenSSH practice, not tested here on this guide's hardware.

## RAG And Agents

- **Documents are data.** Indirect prompt injection means content the model reads (documents, web
  pages, repository files, tool output) can carry instructions it may follow
  ([OWASP LLM01:2025](https://genai.owasp.org/llmrisk/llm01-prompt-injection/), checked 2026-09-30).
  OWASP says it is unclear whether fool-proof prevention exists, and lists measures that reduce
  the impact: least privilege, human approval for high-risk actions and separating untrusted
  content from the prompt (same page). This section summarises public sources; the guide has
  not tested these controls.
- **Do not load model-written images or links automatically.** A rendered image or link can carry
  data to a remote host in its URL (OWASP lists improper output handling as LLM05:2025,
  [Top 10 for LLM applications](https://genai.owasp.org/llm-top-10/)). Disable remote image loading
  in the chat front end where it allows it.
- **Sandbox agents without secrets.** Run coding and computer-use agents in a separate account or
  container without `~/.ssh`, tokens or cloud credentials.
- **A human approves actions.** Writing files, running shell commands and network calls should need
  your approval. Approval logic can have bugs: NVD lists CVE-2026-102697, a bypass of the Bash
  approval in Ollama's experimental agent mode through appended control operators, for versions
  0.14.0 up to but excluding 0.31.2 (checked 2026-09-30).

## Firmware

AMD publishes fixes as `StrixHaloPI-FP11` versions, and the system vendor decides when a BIOS
contains them. The bulletins, minimum versions and update routes per brand are in
[`SECURITY.md`](SECURITY.md#firmware).

- Find your BIOS version: `sudo dmidecode -s bios-version` and
  `sudo dmidecode -s bios-release-date`.
- On systems listed on LVFS, `fwupdmgr refresh --force`, `fwupdmgr get-updates` and
  `fwupdmgr update` apply the vendor's update
  ([Framework's instructions](https://resources.frame.work/downloads/desktop/amd-ryzen-ai-max-300/3.06/),
  checked 2026-09-30). Other brands use their own download pages.
- Ask the vendor which AMD PI a BIOS contains; a version number alone does not say.
- Before flashing, note your BIOS settings (UMA size, IOMMU) and find the vendor's recovery
  procedure. One open report (Framework's
  [issue #270](https://github.com/FrameworkComputer/SoftwareFirmwareIssueTracker/issues/270),
  2026-09-28, no replies, unverified) describes a desktop that did not restart after an `fwupdmgr`
  update on Ubuntu Server 26.04.

## What We Did Not Test

- No exploit, advisory or leak described on this page was reproduced on this guide's hardware; every
  claim above is from the cited public source.
- Open WebUI 0.11.4 and `ENABLE_COMMUNITY_SHARING=False`, `OLLAMA_NO_CLOUD=1`, and the
  `--cache-ram 0 --no-cache-idle-slots` flags are documented or reported by others, not qualified
  here.
- Tailscale and ufw interaction, IPv6 exposure, and the SSH steps have no published test in this
  guide.
- RPC, Ray, vLLM and RCCL cluster routes, and every closed-source engine, are untested.
- The preprint's findings were not repeated on Strix Halo.
- Firmware was not updated or inspected on the first-party test system; its BIOS version is not
  recorded for the published runs ([`REPRODUCIBILITY.md`](REPRODUCIBILITY.md)).
- This page is not legal advice and does not replace a review of your own network.

## Report A Problem

Found an error, a missing advisory or a broken source? Open a public issue as described in
[What To Report](SECURITY.md#what-to-report). Report a vulnerability in `setup.sh` or another script
privately, as described in [SECURITY.md](SECURITY.md#vulnerabilities-in-setupsh-or-other-scripts).
Do not paste passwords, keys or private logs into a public issue.
