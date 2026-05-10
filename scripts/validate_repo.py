#!/usr/bin/env python3
"""Repository consistency checks for the Strix Halo guide.

These checks intentionally stay lightweight: they validate the evidence/index
structure without running benchmarks or requiring local models.
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

EXTERNAL_PREFIXES = (
    "#",
    "http://",
    "https://",
    "mailto:",
    "tel:",
)

SENSITIVE_PATTERNS = {
    "github token": re.compile(r"(?:gho|ghp|ghs|ghu|ghr)_[A-Za-z0-9_]{20,}"),
    "github fine-grained token": re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    "libvirt master key path": re.compile(r"master-key\.aes"),
    "private VM MAC from raw host-state": re.compile(r"52:54:00:78:91:06"),
    "raw websocket remote address": re.compile(r"remoteAddress"),
    "local Zoom profile path": re.compile(r"/home/hoge-heer/\.zoom"),
    "local DocFlock process path": re.compile(r"docflock-sharer"),
}

SENSITIVE_SCAN_ALLOWLIST = {
    "scripts/validate_repo.py",
}

FORBIDDEN_TEXT = {
    "README.md": [
        "default-quality",
        "#rocm-hip----now-working-on-kernel-6194",
        "#llama-bench-direct----latest-llamacpp",
        "#ollama-vulkan-radv-ollama-0212",
        "Use ROCm RPC with the smallest node count that fits.",
        "Vulkan/RADV still wins measured generation;",
    ],
}


def tracked_files() -> list[Path]:
    out = subprocess.check_output(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
    )
    return [ROOT / line for line in out.splitlines() if line.strip()]


def github_slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text


def check_readme_anchors(errors: list[str]) -> None:
    text = README.read_text(encoding="utf-8")
    anchors: list[str] = []
    counts: dict[str, int] = {}

    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not match:
            continue
        base = github_slug(match.group(2))
        count = counts.get(base, 0)
        counts[base] = count + 1
        anchors.append(base if count == 0 else f"{base}-{count}")

    anchor_set = set(anchors)
    for match in re.finditer(r"\[[^\]]+\]\((#[^)]+)\)", text):
        anchor = urllib.parse.unquote(match.group(1)[1:])
        if anchor not in anchor_set:
            errors.append(f"README.md has missing internal anchor: #{anchor}")


def normalized_link_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    target = target.split("#", 1)[0]
    return urllib.parse.unquote(target)


def check_markdown_local_links(files: list[Path], errors: list[str]) -> None:
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in pattern.finditer(text):
            raw = match.group(1).strip()
            if not raw or raw.startswith(EXTERNAL_PREFIXES):
                continue
            target = normalized_link_target(raw)
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                rel_path = path.relative_to(ROOT)
                errors.append(f"{rel_path}: missing local link target {raw}")


def check_csv_widths(files: list[Path], errors: list[str]) -> None:
    for path in files:
        if path.suffix.lower() != ".csv":
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.reader(handle))
        if not rows:
            errors.append(f"{path.relative_to(ROOT)} is empty")
            continue
        widths = sorted({len(row) for row in rows})
        if len(widths) != 1:
            errors.append(
                f"{path.relative_to(ROOT)} has inconsistent CSV column counts: {widths}"
            )


def check_headline_claim_paths(errors: list[str]) -> None:
    path = ROOT / "data" / "headline_claims.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            claim_id = row.get("id", "<unknown>")
            for column in ("structured_csv", "raw_evidence", "chart"):
                value = (row.get(column) or "").strip()
                if not value or value == "n/a":
                    continue
                if value.startswith(("http://", "https://")):
                    continue
                if not (ROOT / value).exists():
                    errors.append(
                        f"data/headline_claims.csv row {claim_id}: missing {column} path {value}"
                    )


def check_forbidden_text(files: list[Path], errors: list[str]) -> None:
    for rel_name, phrases in FORBIDDEN_TEXT.items():
        path = ROOT / rel_name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for phrase in phrases:
            if phrase in text:
                errors.append(f"{rel_name} contains forbidden stale phrase: {phrase}")

    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        if rel in SENSITIVE_SCAN_ALLOWLIST:
            continue
        if path.is_dir():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except UnicodeDecodeError:
            continue
        for name, pattern in SENSITIVE_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{rel} contains {name}")


def main() -> int:
    errors: list[str] = []
    files = tracked_files()

    check_readme_anchors(errors)
    check_markdown_local_links(files, errors)
    check_csv_widths(files, errors)
    check_headline_claim_paths(errors)
    check_forbidden_text(files, errors)

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository validation passed.")
    print(f"Checked {len(files)} tracked files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
