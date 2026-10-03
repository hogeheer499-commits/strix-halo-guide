# Redaction note — 2026-09-26

Maintainer host details were redacted from text files under `data/raw/` after
capture: the maintainer's home directory became `~`, the host name `<host>`,
private LAN addresses `<lan-ip>`, and listening-port and top-process sections
were reduced to benchmark-runtime lines with a one-line redaction marker.
Benchmark numbers, commands, model filenames (relative to `~`), kernel, Mesa,
runtime builds, firmware and power fields were not changed. Files listed in
`SHA256SUMS` manifests were left untouched. Git history before this commit
keeps the original captures.

## Follow-up — 2026-10-03

The two 2026-09-26 bundles `strict-clean-headline-b11146` and
`64gb-tier-30b-candidates-b11146` kept their desktop process and VM listings.
Desktop application names in those host snapshots, the run log, the run script and the READMEs were replaced by
categories (`web-browser`, `video-call-app`, `video-call-app-helper`,
`coding-app`, VM name `vm-1`); counts, order, kernel, Mesa, runtime and power
fields were not changed, so the evidence that the host was not fully idle is
kept. The maintainer's account name in file-owner columns of raw listings
became `<user>`. Files listed in `SHA256SUMS` manifests were left untouched.
Git history before this commit keeps the original captures.
