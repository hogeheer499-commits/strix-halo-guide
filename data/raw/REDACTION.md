# Redaction note — 2026-09-26

Maintainer host details were redacted from text files under `data/raw/` after
capture: the maintainer's home directory became `~`, the host name `<host>`,
private LAN addresses `<lan-ip>`, and listening-port and top-process sections
were reduced to benchmark-runtime lines with a one-line redaction marker.
Benchmark numbers, commands, model filenames (relative to `~`), kernel, Mesa,
runtime builds, firmware and power fields were not changed. Files listed in
`SHA256SUMS` manifests were left untouched. Git history before this commit
keeps the original captures.
