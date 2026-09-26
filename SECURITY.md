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

**Lookalike repositories (checked 2026-09-25):** at least one unrelated
repository with the same name, `GetNyrex/strix-halo-guide` (plus a GitHub Pages
copy), links a `.zip` bundle and tells Windows users to run an `.exe`. It is not
part of this project. Do not download or run its files. This guide never ships
`.exe` or `.zip` installers; the setup route is the reviewed shell script from
the canonical repository.

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

Checked 2026-09-25. This lists published advisories for runtimes the guide pins
or qualified; it is not a full audit, and the guide has not tested any exploit.

- **Ollama:** CVE-2026-85180 (SSRF through cross-host redirects when pulling
  tensor layers) lists Ollama 0.30.0 through 0.33.2 as affected. That range
  includes the `setup.sh` fresh-install default 0.31.2, the Qwen3.8 route on
  0.32.13 and the qualified existing 0.32.15 service. The linked
  [ollama#17041](https://github.com/ollama/ollama/issues/17041) was still open
  and no fixed release was named as of 2026-09-25.
- **Open WebUI:** CVE-2026-70491 affects Open WebUI 0.10.2 and earlier, which
  includes the digest-pinned 0.10.2 image in the README. Further advisories
  fixed in 0.11.0 and 0.11.1 also cover 0.10.2; many of them require an
  authenticated non-admin user. A patched release has not yet been qualified
  here (queued in [`data/current_test_queue.csv`](data/current_test_queue.csv)).

Until fixed releases are qualified:

- keep Ollama on its loopback default (`127.0.0.1:11434`); do not expose an
  unauthenticated Ollama listener to a LAN or the internet;
- pull models only from registries you trust;
- keep Open WebUI bound to loopback and do not create accounts for untrusted
  users.
