# Security Policy

## Official Source

The canonical repository for this guide is:

```text
https://github.com/hogeheer499-commits/strix-halo-guide
```

This project publishes documentation, shell scripts, benchmark data, charts,
and source archives. It does not publish Windows installers, `.exe` files,
binary `.zip` packages, browser extensions, or model weights.

GitHub-generated source archives for tagged releases are expected. Extra binary
download assets are not part of this project unless they are explicitly
documented in this repository by the maintainer.

## What To Report

Please report:

- repos, websites, or packages that claim to be the official source for this guide;
- executable downloads or ZIP bundles promoted under this guide's name;
- modified setup commands that point away from this repository without saying so;
- benchmark tables copied from this guide while changing the hardware, model,
  quant, or backend provenance;
- security issues in `setup.sh` or other scripts in this repository.

If the report does not include private credentials or sensitive logs, open a
GitHub issue here:

```text
https://github.com/hogeheer499-commits/strix-halo-guide/issues
```

Do not paste passwords, API keys, private SSH keys, or private model URLs into
public issues. If a public report needs redaction, describe the issue without
the secret and state that private details are available.

## Verification

Before running commands from any Strix Halo guide, check that URLs point to:

```text
github.com/hogeheer499-commits/strix-halo-guide
raw.githubusercontent.com/hogeheer499-commits/strix-halo-guide
```

Third-party forks and mirrors may be useful, but they are not validated by this
project and should be treated as unofficial.
