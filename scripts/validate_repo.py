#!/usr/bin/env python3
"""Repository consistency checks for the Strix Halo guide.

These checks intentionally stay lightweight: they validate the evidence/index
structure without running benchmarks or requiring local models.
"""

from __future__ import annotations

import ast
import csv
import json
import re
import struct
import subprocess
import sys
import urllib.parse
from datetime import date
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
    "private GitHub analytics path": re.compile(r"github-traction-snapshot"),
    "private GitHub unique-traffic metric": re.compile(
        r"unique repository visitors|unique cloners|unique_views_14d|unique_cloners_14d",
        re.IGNORECASE,
    ),
    "private GitHub referrer/path artifact": re.compile(
        r"(?:referrers|popular_paths)\.json",
        re.IGNORECASE,
    ),
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


def check_system_evidence_matrix(errors: list[str]) -> None:
    """Keep the public cross-OEM count and its source paths auditable."""
    csv_path = ROOT / "data" / "system_evidence_matrix.csv"
    markdown_path = ROOT / "SYSTEM_EVIDENCE_MATRIX.md"
    required_columns = (
        "evidence_source",
        "count",
        "evidence_class",
        "system",
        "identity_basis",
        "os_or_route",
        "coverage",
        "main_evidence",
        "most_useful_next_validation",
    )
    allowed_classes = {
        "first-party-retail",
        "community-reported-owner",
        "independently-sourced-report",
        "external-public-package",
    }

    for path in (csv_path, markdown_path):
        if not path.exists():
            errors.append(f"missing system evidence matrix file: {path.relative_to(ROOT)}")
    if not csv_path.exists() or not markdown_path.exists():
        return

    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != required_columns:
            errors.append(
                "data/system_evidence_matrix.csv has unexpected columns: "
                f"{reader.fieldnames}"
            )
            return
        rows = list(reader)

    if not rows:
        errors.append("data/system_evidence_matrix.csv has no evidence rows")
        return

    total = 0
    owner_systems = 0
    independent_sources = 0
    seen_sources: set[str] = set()
    for line_number, row in enumerate(rows, start=2):
        source = row["evidence_source"].strip()
        if not source:
            errors.append(f"data/system_evidence_matrix.csv line {line_number}: empty evidence_source")
        elif source in seen_sources:
            errors.append(
                f"data/system_evidence_matrix.csv line {line_number}: duplicate evidence_source {source}"
            )
        seen_sources.add(source)

        try:
            count = int(row["count"])
        except ValueError:
            errors.append(
                f"data/system_evidence_matrix.csv line {line_number}: count is not an integer"
            )
            continue
        if count < 1:
            errors.append(
                f"data/system_evidence_matrix.csv line {line_number}: count must be positive"
            )
        total += count

        evidence_class = row["evidence_class"].strip()
        if evidence_class not in allowed_classes:
            errors.append(
                "data/system_evidence_matrix.csv line "
                f"{line_number}: unsupported evidence_class {evidence_class}"
            )
        elif evidence_class in {"first-party-retail", "community-reported-owner"}:
            owner_systems += count
        else:
            independent_sources += count

        identity_basis = row["identity_basis"].strip()
        if not identity_basis:
            errors.append(
                "data/system_evidence_matrix.csv line "
                f"{line_number}: empty identity_basis"
            )

        evidence_path = row["main_evidence"].strip()
        if not evidence_path:
            errors.append(
                f"data/system_evidence_matrix.csv line {line_number}: empty main_evidence"
            )
        elif evidence_path.startswith(("http://", "https://")):
            pass
        elif not (ROOT / evidence_path).exists():
            errors.append(
                "data/system_evidence_matrix.csv line "
                f"{line_number}: missing main_evidence path {evidence_path}"
            )

    public_references = {
        "README.md": (
            f"Evidence Coverage: {total} Systems Or Independent Sources",
            f"{total}_systems%2Fsources",
            f"{owner_systems} described owner systems plus {independent_sources} independently attributable",
            "SYSTEM_EVIDENCE_MATRIX.md",
            "data/system_evidence_matrix.csv",
        ),
        "SYSTEM_EVIDENCE_MATRIX.md": (
            f"**{total} owner systems or independent sources**",
            f"**{owner_systems} described owner",
            f"plus {independent_sources} independently attributable",
            "data/system_evidence_matrix.csv",
        ),
        "data/README.md": (
            "system_evidence_matrix.csv",
            f"{owner_systems} described owner systems and {independent_sources} independently attributable",
        ),
        "docs/index.md": (f"covers {total} Strix Halo-class systems",),
        "ONE_PAGE_BRIEF.md": (
            f"**{total} Strix Halo-class systems or independent sources**",
            f"{owner_systems} described owner",
            f"plus {independent_sources} independently attributable",
        ),
        "docs/llms.txt": (
            "SYSTEM_EVIDENCE_MATRIX.md",
            "data/system_evidence_matrix.csv",
        ),
    }
    for rel_name, fragments in public_references.items():
        path = ROOT / rel_name
        if not path.exists():
            errors.append(f"missing matrix reference file: {rel_name}")
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment not in text:
                errors.append(f"{rel_name} missing system matrix reference: {fragment}")


def check_public_state(errors: list[str]) -> None:
    """Keep current public entry surfaces synchronized to one dated state file."""
    state_path = ROOT / "data" / "public_state.json"
    if not state_path.exists():
        errors.append("missing public freshness state: data/public_state.json")
        return

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"data/public_state.json is invalid: {exc}")
        return

    required_top_level = (
        "schema_version",
        "evidence_reviewed",
        "evidence_reviewed_human",
        "freshness_max_age_days",
        "release",
        "runtime",
        "qwen38",
        "coverage",
        "public_project_snapshot",
        "affiliate_status",
    )
    for key in required_top_level:
        if key not in state:
            errors.append(f"data/public_state.json missing key: {key}")
    if any(key not in state for key in required_top_level):
        return

    try:
        reviewed = date.fromisoformat(state["evidence_reviewed"])
        max_age = int(state["freshness_max_age_days"])
    except (TypeError, ValueError) as exc:
        errors.append(f"data/public_state.json has invalid freshness values: {exc}")
        return
    age = (date.today() - reviewed).days
    if age < 0:
        errors.append("data/public_state.json evidence_reviewed is in the future")
    elif age > max_age:
        errors.append(
            "public evidence state is stale: "
            f"{age} days old, maximum is {max_age} days"
        )

    runtime = state["runtime"]
    coverage = state["coverage"]
    public_project = state["public_project_snapshot"]
    reviewed_human = state["evidence_reviewed_human"]
    affiliate_checked = date.fromisoformat(state["affiliate_status"]["checked"])
    affiliate_checked_human = (
        f"{affiliate_checked.strftime('%B')} {affiliate_checked.day}, {affiliate_checked.year}"
    )
    if coverage.get("owner_systems", 0) + coverage.get("independent_sources", 0) != coverage.get(
        "systems_or_sources"
    ):
        errors.append(
            "data/public_state.json coverage split does not add up to systems_or_sources"
        )
    required_fragments = {
        "README.md": (
            "QWEN38_STRIX_HALO.md",
            f"{coverage['systems_or_sources']} systems or independent sources",
            "data/public_state.json",
            "strix-halo-models/",
        ),
        "QWEN38_STRIX_HALO.md": (
            f"**Evidence reviewed:** {reviewed_human}",
            f"Ollama {runtime['ollama_current_checked']}",
            "data/qwen38_route_matrix.csv",
            "data/affiliate_link_registry.csv",
        ),
        "STRIX_HALO_LOCAL_LLM_SETUP.md": (
            f"**Evidence reviewed:** {reviewed_human}",
            "QWEN38_STRIX_HALO.md",
            f"Ollama {runtime['ollama_current_checked']}",
        ),
        "TRACTION.md": (
            f"Repository-stat snapshot date: {public_project['date']}",
            f"| Stars | {public_project['stars']} |",
            f"| Forks | {public_project['forks']} |",
        ),
        "ONE_PAGE_BRIEF.md": (
            f"{public_project['stars']} stars",
            f"{public_project['forks']} forks",
            public_project["date"],
        ),
        "PARTNERSHIP.md": (
            f"{public_project['stars']} GitHub stars",
            f"{public_project['forks']} forks",
            public_project["date"],
        ),
        "SHARE.md": (
            "Qwen3.8",
            f"Ollama {runtime['ollama_current_checked']}",
            f"no affiliate links as of {affiliate_checked_human}",
            f"Public benchmark evidence covers {coverage['systems_or_sources']} owner systems or independent sources",
            f"{coverage['owner_systems']} described owner systems plus {coverage['independent_sources']} independently attributable external sources",
            f"{coverage['community_benchmark_contributors']} credited community benchmark contributors",
        ),
        "CONTRIBUTORS.md": (
            f"credits **{coverage['community_benchmark_contributors']}** community benchmark contributors",
            f"**{coverage['systems_or_sources']} owner systems or independent sources**",
        ),
        "BEST_KNOWN_PROFILES.md": (
            f"**Profiles reviewed:** {reviewed_human}",
            "data/best_known_profiles.csv",
        ),
        "BENCHMARKS.md": (
            f"**Benchmarks reviewed:** {reviewed_human}",
            "data/benchmarks.csv",
        ),
        "REPRODUCIBILITY.md": (
            f"**Checklist reviewed:** {reviewed_human}",
            "data/headline_claims.csv",
        ),
        "docs/index.md": (
            f"**Evidence reviewed:** {reviewed_human}",
            f"Ollama {runtime['ollama_current_checked']}",
            "qwen38-strix-halo/",
            "troubleshooting/",
            "strix-halo-models/",
        ),
        "docs/amd-strix-halo-setup.md": (
            f"**Setup reviewed:** {reviewed_human}",
            "qwen38-strix-halo/",
            "troubleshooting/",
            "strix-halo-models/",
            "https://strixhaloguide.com/amd-strix-halo-setup/",
        ),
        "docs/best-strix-halo-mini-pc.md": (
            f"**Evidence reviewed:** {reviewed_human}",
            f"no affiliate links as of {affiliate_checked_human}",
            "data/affiliate_link_registry.csv",
        ),
        "docs/qwen38-strix-halo.md": (
            f"**Evidence reviewed:** {reviewed_human}",
            f"no affiliate links as of {affiliate_checked_human}",
            f"Ollama {runtime['ollama_current_checked']}",
            "data/qwen38_route_matrix.csv",
        ),
        "docs/troubleshooting.md": (
            f"**Evidence reviewed:** {reviewed_human}",
            f"no affiliate links as of {affiliate_checked_human}",
            "OLLAMA_IGPU_ENABLE=1",
            "linux-firmware-20251125",
            "llama.cpp/issues/26209",
            "llama.cpp/pull/25863",
        ),
        "docs/models.md": (
            f"**Evidence reviewed:** {reviewed_human}",
            f"no affiliate links as of {affiliate_checked_human}",
            "Measured On This Machine",
            "Verified To Exist, Not Measured Here (2026-08-29 Check)",
            "data/current_test_queue.csv",
        ),
        "docs/llms.txt": (
            "qwen38-strix-halo/",
            "troubleshooting/",
            "strix-halo-models/",
            "QWEN38_STRIX_HALO.md",
            "data/qwen38_route_matrix.csv",
        ),
        "VENDOR_DISCLOSURE.md": (
            "data/affiliate_link_registry.csv",
            "Affiliate commission does not determine",
        ),
    }
    for rel_name, fragments in required_fragments.items():
        path = ROOT / rel_name
        if not path.exists():
            errors.append(f"missing synchronized public surface: {rel_name}")
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment not in text:
                errors.append(f"{rel_name} missing public-state fragment: {fragment}")

    registry_path = ROOT / "data" / "affiliate_link_registry.csv"
    if not registry_path.exists():
        errors.append("missing affiliate registry: data/affiliate_link_registry.csv")
    else:
        with registry_path.open(newline="", encoding="utf-8") as handle:
            header = next(csv.reader(handle), [])
        expected = [
            "link_id",
            "status",
            "vendor",
            "product",
            "region",
            "relationship",
            "public_destination",
            "last_checked",
            "disclosure_location",
            "notes",
        ]
        if header != expected:
            errors.append(
                "data/affiliate_link_registry.csv has unexpected columns: "
                f"{header}"
            )


def check_duplicate_dict_literal_keys(errors: list[str]) -> None:
    """Fail when a literal key would silently replace an earlier dict entry."""
    path = Path(__file__)
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError) as exc:
        errors.append(f"cannot inspect scripts/validate_repo.py dict literals: {exc}")
        return

    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        seen: dict[object, int] = {}
        for key_node in node.keys:
            if key_node is None:
                continue
            try:
                key = ast.literal_eval(key_node)
                hash(key)
            except (ValueError, TypeError, SyntaxError):
                continue
            if key in seen:
                errors.append(
                    "scripts/validate_repo.py has duplicate dict literal key "
                    f"{key!r} on lines {seen[key]} and {key_node.lineno}"
                )
            else:
                seen[key] = key_node.lineno


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


def png_dimensions(path: Path) -> tuple[int, int] | None:
    """Read PNG dimensions without adding an image-library CI dependency."""
    try:
        with path.open("rb") as handle:
            header = handle.read(24)
    except OSError:
        return None
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", header[16:24])


def check_pages_seo(errors: list[str]) -> None:
    config_path = ROOT / "docs" / "_config.yml"
    index_path = ROOT / "docs" / "index.md"
    layout_path = ROOT / "docs" / "_layouts" / "default.html"
    preview_path = ROOT / "social-preview.png"
    pages_preview_path = ROOT / "docs" / "assets" / "social-preview.png"
    favicon_path = ROOT / "docs" / "assets" / "favicon.png"
    root_qwen_preview_path = ROOT / "qwen38-route-preview.png"
    qwen_preview_path = ROOT / "docs" / "assets" / "qwen38-route-preview.png"

    required_files = (
        config_path,
        index_path,
        layout_path,
        preview_path,
        pages_preview_path,
        favicon_path,
        root_qwen_preview_path,
        qwen_preview_path,
    )
    for path in required_files:
        if not path.exists():
            errors.append(f"missing Pages SEO file: {path.relative_to(ROOT)}")
    if any(not path.exists() for path in required_files):
        return

    config = config_path.read_text(encoding="utf-8")
    index = index_path.read_text(encoding="utf-8")
    layout = layout_path.read_text(encoding="utf-8")

    required_config = (
        'title: "Strix Halo Guide"',
        'url: "https://hogeheer499-commits.github.io"',
        'baseurl: "/strix-halo-guide"',
        "jekyll-seo-tag",
        "jekyll-sitemap",
        'logo: "/assets/favicon.png"',
    )
    for fragment in required_config:
        if fragment not in config:
            errors.append(f"docs/_config.yml missing SEO setting: {fragment}")

    required_index = (
        'permalink: /',
        'canonical_url: "https://strixhaloguide.com/"',
        'sitemap: false',
        'date: "',
        'type: "TechArticle"',
        'date_modified: "',
        'https://hogeheer499-commits.github.io/strix-halo-guide/assets/social-preview.png',
        "**Evidence reviewed:**",
    )
    for fragment in required_index:
        if fragment not in index:
            errors.append(f"docs/index.md missing SEO field or visible evidence: {fragment}")

    required_layout = (
        "{% seo %}",
        "https://strixhaloguide.com/",
        "AMD Strix Halo Guide",
        "google-site-verification",
        "rel=\"icon\"",
        "rel=\"apple-touch-icon\"",
        "article:modified_time",
        "id=\"main-content\"",
    )
    for fragment in required_layout:
        if fragment not in layout:
            errors.append(f"docs/_layouts/default.html missing SEO/accessibility markup: {fragment}")

    preview_size = png_dimensions(preview_path)
    pages_preview_size = png_dimensions(pages_preview_path)
    favicon_size = png_dimensions(favicon_path)
    if preview_size != (1280, 640):
        errors.append(f"social-preview.png must be 1280x640, found {preview_size}")
    if pages_preview_size != (1280, 640):
        errors.append(
            "docs/assets/social-preview.png must be 1280x640, "
            f"found {pages_preview_size}"
        )
    if favicon_size != (512, 512):
        errors.append(f"docs/assets/favicon.png must be 512x512, found {favicon_size}")
    qwen_preview_size = png_dimensions(qwen_preview_path)
    root_qwen_preview_size = png_dimensions(root_qwen_preview_path)
    if root_qwen_preview_size != (1280, 640):
        errors.append(
            "qwen38-route-preview.png must be 1280x640, "
            f"found {root_qwen_preview_size}"
        )
    if qwen_preview_size != (1280, 640):
        errors.append(
            "docs/assets/qwen38-route-preview.png must be 1280x640, "
            f"found {qwen_preview_size}"
        )
    if preview_path.read_bytes() != pages_preview_path.read_bytes():
        errors.append(
            "social-preview.png and docs/assets/social-preview.png differ; "
            "rerun python3 generate_preview.py"
        )
    if root_qwen_preview_path.read_bytes() != qwen_preview_path.read_bytes():
        errors.append(
            "qwen38-route-preview.png and docs/assets/qwen38-route-preview.png "
            "differ; rerun python3 generate_preview.py"
        )


def main() -> int:
    errors: list[str] = []
    files = tracked_files()

    check_readme_anchors(errors)
    check_markdown_local_links(files, errors)
    check_csv_widths(files, errors)
    check_headline_claim_paths(errors)
    check_system_evidence_matrix(errors)
    check_public_state(errors)
    check_duplicate_dict_literal_keys(errors)
    check_forbidden_text(files, errors)
    check_pages_seo(errors)

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
