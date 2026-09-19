#!/usr/bin/env python3
"""Audit public discovery surfaces without scraping search-result rankings.

Local failures are errors. Network checks are warnings by default because a
temporary remote outage must not break normal repository validation. Use
--strict-network when a missing public surface should fail the command.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_URL = "https://github.com/hogeheer499-commits/strix-halo-guide"
PAGES_URL = "https://hogeheer499-commits.github.io/strix-halo-guide/"
PROJECT_URL = "https://strixhaloguide.com/"
PROJECT_SETUP_URL = "https://strixhaloguide.com/amd-strix-halo-setup/"
PROJECT_PARTNERS_URL = "https://strixhaloguide.com/partners/"
PROJECT_QWEN_URL = "https://strixhaloguide.com/qwen38-strix-halo/"
PAGES_SETUP_URL = f"{PAGES_URL}amd-strix-halo-setup/"
PAGES_QWEN_URL = f"{PAGES_URL}qwen38-strix-halo/"
PROJECT_BUYER_URL = f"{PROJECT_URL}best-strix-halo-mini-pc/"
PROJECT_MODELS_URL = f"{PROJECT_URL}strix-halo-models/"
PROJECT_TROUBLESHOOTING_URL = f"{PROJECT_URL}troubleshooting/"
# This is the actual disclosure destination linked by the partner page,
# not a guessed /disclosure/ route on the canonical site.
DISCLOSURE_URL = "https://raw.githubusercontent.com/hogeheer499-commits/strix-halo-guide/main/VENDOR_DISCLOSURE.md"


def freshness_checks(as_of: dt.date | None = None) -> list[Check]:
    """Report staleness without preventing network checks or report writing."""
    target = "data/public_state.json"
    try:
        state = json.loads((ROOT / target).read_text(encoding="utf-8"))
        reviewed = dt.date.fromisoformat(state["evidence_reviewed"])
        maximum = int(state["freshness_max_age_days"])
        if maximum < 0:
            raise ValueError("freshness_max_age_days must be nonnegative")
        today = as_of or dt.datetime.now(dt.timezone.utc).date()
        age = (today - reviewed).days
    except (OSError, ValueError, TypeError, KeyError) as exc:
        return [Check("evidence-freshness", target, "ERROR", f"invalid state: {exc}")]
    if age < 0:
        status, detail = "ERROR", "evidence review is in the future"
    elif age > maximum:
        status, detail = "ERROR", f"evidence review is stale: {age} days old; maximum {maximum}"
    else:
        status, detail = "PASS", f"evidence review age {age} days; maximum {maximum}"
    return [Check("evidence-freshness", target, status, f"as of {today}: {detail}")]


def publication_checks(url: str, body: str, state: dict) -> list[Check]:
    """Revision is a deployment signal, not proof of every prose claim."""
    expected = state.get("publication", {}).get("expected_content_revision")
    if not expected:
        return [Check("publication-revision", url, "WARN", "no expected content revision configured")]
    # Accept either attribute order and tolerate markup/spacing differences.
    tags = re.findall(r"<meta\b[^>]*>", body, re.I)
    revision = None
    for tag in tags:
        attrs = dict((k.lower(), html.unescape(v)) for k, _, v in
                     re.findall(r'''([\w-]+)\s*=\s*(["'])(.*?)\2''', tag))
        if attrs.get("name", "").lower() == "guide-content-revision":
            revision = attrs.get("content")
    status = "PASS" if revision == expected else "WARN"
    checks = [Check("publication-revision", url, status,
                    f"content revision {revision!r}; expected {expected!r}; not a hardware qualification date")]
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    text = re.sub(r"\s+", " ", text).lower()
    # Targeted regressions supplement the revision check; absence is NOT a
    # general semantic pass. Do not use these patterns on historical archives.
    stale = []
    if url == PROJECT_BUYER_URL:
        for phrase in ("cheapest 128gb", "best ecosystem/support", "192gb pro 495"):
            # A transparent withdrawal is not an active buying recommendation.
            paragraphs = [html.unescape(re.sub(r"<[^>]+>", " ", p)).lower()
                          for p in re.split(r"</(?:p|tr|li|h[1-6])>", body, flags=re.I)]
            if any(phrase in re.sub(r"\s+", " ", p) and "withdrawn" not in p for p in paragraphs):
                stale.append(phrase)
    if re.search(r"always (?:use|disable).{0,30}(?:mmap|tuned)", text):
        stale.append("universal load/power advice")
    if stale:
        checks.append(Check("publication-guidance", url, "WARN",
                            "review potentially stale active wording in context: " + ", ".join(stale)))
    return checks


@dataclass
class Check:
    name: str
    target: str
    status: str
    detail: str


def local_checks() -> list[Check]:
    checks: list[Check] = []
    required = {
        "README.md": (
            "Strix Halo Guide: AMD Ryzen AI MAX+ 395 Local LLM Setup & Benchmarks",
            "SYSTEM_EVIDENCE_MATRIX.md",
            REPOSITORY_URL,
            PROJECT_URL,
        ),
        "docs/_config.yml": (
            'title: "Strix Halo Guide"',
            'url: "https://hogeheer499-commits.github.io"',
            'baseurl: "/strix-halo-guide"',
        ),
        "docs/index.md": (
            "Strix Halo",
            "cross-OEM system evidence matrix",
            REPOSITORY_URL,
            f'canonical_url: "{PROJECT_URL}"',
            "sitemap: false",
        ),
        "docs/amd-strix-halo-setup.md": (
            f'canonical_url: "{PROJECT_SETUP_URL}"',
            "sitemap: false",
        ),
        "docs/_layouts/default.html": (
            PROJECT_URL,
            "AMD Strix Halo Guide",
        ),
        "SHARE.md": (
            "Canonical web guide:",
            PROJECT_URL,
        ),
        "docs/llms.txt": (
            REPOSITORY_URL,
            "SYSTEM_EVIDENCE_MATRIX.md",
            "data/system_evidence_matrix.csv",
        ),
    }
    for rel_name, fragments in required.items():
        path = ROOT / rel_name
        if not path.exists():
            checks.append(Check("local-file", rel_name, "ERROR", "file is missing"))
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        missing = [fragment for fragment in fragments if fragment not in text]
        if missing:
            checks.append(
                Check("local-content", rel_name, "ERROR", f"missing: {', '.join(missing)}")
            )
        else:
            checks.append(Check("local-content", rel_name, "PASS", "required discovery fields present"))
    return checks


def fetch(url: str) -> tuple[int, str, str]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "strix-halo-guide-authority-audit/1.0"},
    )
    with urllib.request.urlopen(request, timeout=25) as response:
        body = response.read(4_000_000).decode("utf-8", errors="replace")
        return response.status, response.geturl(), body


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        return None


def fetch_no_redirect(url: str) -> tuple[int, str, str | None, str]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "strix-halo-guide-authority-audit/1.0"},
    )
    opener = urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(request, timeout=25) as response:
            body = response.read(4_000_000).decode("utf-8", errors="replace")
            return response.status, response.geturl(), response.headers.get("Location"), body
    except urllib.error.HTTPError as exc:
        body = exc.read(4_000_000).decode("utf-8", errors="replace")
        return exc.code, exc.geturl(), exc.headers.get("Location"), body


def canonical_from_html(body: str) -> str | None:
    match = re.search(
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)',
        body,
        flags=re.IGNORECASE,
    )
    if not match:
        match = re.search(
            r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']',
            body,
            flags=re.IGNORECASE,
        )
    return match.group(1) if match else None


def network_checks() -> tuple[list[Check], dict[str, int]]:
    checks: list[Check] = []
    metrics: dict[str, int] = {}
    state = json.loads((ROOT / "data" / "public_state.json").read_text(encoding="utf-8"))
    reviewed = state["evidence_reviewed_human"]
    systems = state["coverage"]["systems_or_sources"]
    contributors = state["coverage"]["community_benchmark_contributors"]
    surfaces = (
        ("repository", REPOSITORY_URL, ("AMD Strix Halo",), None),
        ("github-pages-home", PAGES_URL, ("Strix Halo",), PROJECT_URL),
        ("github-pages-setup", PAGES_SETUP_URL, ("AMD Strix Halo Setup",), PROJECT_SETUP_URL),
        ("github-pages-qwen", PAGES_QWEN_URL, ("Qwen3.8",), PROJECT_QWEN_URL),
        (
            "project-home",
            PROJECT_URL,
            (
                "Strix Halo",
                "Qwen3.8",
                f"{systems} systems or independent sources",
                f"{contributors} (?:credited community )?benchmark contributors",
                reviewed,
            ),
            PROJECT_URL,
        ),
        (
            "project-setup",
            PROJECT_SETUP_URL,
            ("AMD Strix Halo", "Qwen3.8", reviewed),
            PROJECT_SETUP_URL,
        ),
        (
            "project-partners",
            PROJECT_PARTNERS_URL,
            (
                "partner",
                f"{systems} systems(?: or independent sources)?",
                "Affiliate commission (?:does not determine|never determines)",
            ),
            PROJECT_PARTNERS_URL,
        ),
        (
            "project-qwen",
            PROJECT_QWEN_URL,
            ("Qwen3.8", "20.42", "50,059", "261,130", reviewed),
            PROJECT_QWEN_URL,
        ),
        ("project-buyer", PROJECT_BUYER_URL, ("Strix Halo", "128GB"), PROJECT_BUYER_URL),
        ("project-models", PROJECT_MODELS_URL, ("Strix Halo", "model"), PROJECT_MODELS_URL),
        ("project-troubleshooting", PROJECT_TROUBLESHOOTING_URL,
         ("Strix Halo", "troubleshooting"), PROJECT_TROUBLESHOOTING_URL),
        ("project-disclosure", DISCLOSURE_URL,
         ("Vendor Disclosure Policy", "Affiliate links", "Negative results stay"), None),
    )
    for name, url, markers, expected_canonical in surfaces:
        try:
            status, final_url, body = fetch(url)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            checks.append(Check(name, url, "WARN", f"fetch failed: {exc}"))
            continue
        if status != 200:
            checks.append(Check(name, url, "WARN", f"HTTP {status}; final URL {final_url}"))
            continue
        visible = html.unescape(re.sub(r"<[^>]+>", " ", body))
        visible = re.sub(r"\s+", " ", visible)
        missing_markers = [marker for marker in markers if not re.search(marker, visible, re.I)]
        if missing_markers:
            checks.append(
                Check(
                    name,
                    url,
                    "WARN",
                    "HTTP 200 but markers are missing: " + ", ".join(missing_markers),
                )
            )
        if url.startswith(PROJECT_URL):
            checks.extend(publication_checks(url, body, state))
        canonical = canonical_from_html(body) if expected_canonical else None
        if expected_canonical and canonical != expected_canonical:
            checks.append(
                Check(name, url, "WARN", f"canonical {canonical!r}; expected {expected_canonical!r}")
            )
            continue
        if not missing_markers:
            checks.append(Check(name, url, "PASS", f"HTTP 200; final URL {final_url}"))

    redirect_checks = (
        ("http-to-https-apex", "http://strixhaloguide.com/", PROJECT_URL),
        ("www-to-apex", "https://www.strixhaloguide.com/", PROJECT_URL),
    )
    for name, url, expected_location in redirect_checks:
        try:
            status, _, location, _ = fetch_no_redirect(url)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            checks.append(Check(name, url, "WARN", f"fetch failed: {exc}"))
            continue
        if status == 301 and location == expected_location:
            checks.append(Check(name, url, "PASS", f"HTTP 301 to {location}"))
        else:
            checks.append(
                Check(
                    name,
                    url,
                    "WARN",
                    f"HTTP {status}, location {location!r}; expected HTTP 301 to {expected_location}",
                )
            )

    support_files = (
        (
            "project-robots",
            f"{PROJECT_URL}robots.txt",
            ("User-agent: *", "Allow: /", f"Sitemap: {PROJECT_URL}sitemap.xml"),
        ),
        (
            "project-sitemap",
            f"{PROJECT_URL}sitemap.xml",
            # Sitemap lastmod is content modification, not benchmark review date.
            (PROJECT_URL, PROJECT_SETUP_URL, PROJECT_PARTNERS_URL, PROJECT_QWEN_URL),
        ),
        (
            "project-llms",
            f"{PROJECT_URL}llms.txt",
            (PROJECT_URL, PROJECT_SETUP_URL, PROJECT_QWEN_URL, REPOSITORY_URL),
        ),
    )
    for name, url, markers in support_files:
        try:
            status, final_url, body = fetch(url)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            checks.append(Check(name, url, "WARN", f"fetch failed: {exc}"))
            continue
        missing_markers = [marker for marker in markers if marker not in body]
        if status == 200 and not missing_markers:
            checks.append(Check(name, url, "PASS", f"HTTP 200; final URL {final_url}"))
        else:
            checks.append(
                Check(
                    name,
                    url,
                    "WARN",
                    f"HTTP {status}; missing: {', '.join(missing_markers)}",
                )
            )

    backlinks = (
        (
            "awesome-llm-apps-contextual-link",
            "https://raw.githubusercontent.com/Shubhamsaboo/awesome-llm-apps/main/advanced_llm_apps/llm_apps_with_memory_tutorials/local_chatgpt_with_memory/README.md",
        ),
        (
            "awesome-opensource-ai-resource-link",
            "https://raw.githubusercontent.com/alvinreal/awesome-opensource-ai/main/README.md",
        ),
        (
            "strixhalo-homelab-resource-link",
            "https://raw.githubusercontent.com/deseven/strixhalo-homelab/main/AI/AI_Capabilities_Overview.md",
        ),
    )
    for name, url in backlinks:
        try:
            status, _, body = fetch(url)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            checks.append(Check(name, url, "WARN", f"fetch failed: {exc}"))
            continue
        if status == 200 and REPOSITORY_URL in body:
            checks.append(Check(name, url, "PASS", "canonical repository link is present"))
        else:
            checks.append(Check(name, url, "WARN", "canonical repository link was not found"))

    api_url = "https://api.github.com/repos/hogeheer499-commits/strix-halo-guide"
    try:
        status, _, body = fetch(api_url)
        data = json.loads(body)
        if status == 200:
            metrics = {
                "github_stars": int(data.get("stargazers_count", 0)),
                "github_forks": int(data.get("forks_count", 0)),
                "github_open_issues": int(data.get("open_issues_count", 0)),
            }
            checks.append(Check("github-public-metrics", api_url, "PASS", json.dumps(metrics, sort_keys=True)))
            homepage = data.get("homepage")
            if homepage == PROJECT_URL:
                checks.append(Check("github-project-homepage", api_url, "PASS", homepage))
            else:
                checks.append(
                    Check(
                        "github-project-homepage",
                        api_url,
                        "WARN",
                        f"homepage {homepage!r}; expected {PROJECT_URL}",
                    )
                )
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
        checks.append(Check("github-public-metrics", api_url, "WARN", f"fetch failed: {exc}"))
    return checks, metrics


def write_json(path: Path, generated_at: str, checks: list[Check], metrics: dict[str, int]) -> None:
    payload = {
        "generated_at": generated_at,
        "note": "SERP positions are intentionally not scraped; use Search Console for query trends.",
        "metrics": metrics,
        "checks": [asdict(check) for check in checks],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_markdown(path: Path, generated_at: str, checks: list[Check], metrics: dict[str, int]) -> None:
    lines = [
        "# Strix Halo Guide Authority Audit",
        "",
        f"Generated: `{generated_at}`",
        "",
        "Search-result positions are intentionally not scraped. Automated markers/revisions do not certify all page claims. Review warnings in context.",
        "",
    ]
    if metrics:
        lines.extend(
            [
                "## Public GitHub Snapshot",
                "",
                f"- Stars: **{metrics.get('github_stars', 0)}**",
                f"- Forks: **{metrics.get('github_forks', 0)}**",
                f"- Open issues and pull requests: **{metrics.get('github_open_issues', 0)}**",
                "",
            ]
        )
    lines.extend(["## Checks", "", "| Status | Check | Target | Detail |", "|---|---|---|---|"])
    for check in checks:
        detail = check.detail.replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {check.status} | {check.name} | {check.target} | {detail} |")
    warning_count = sum(check.status == "WARN" for check in checks)
    error_count = sum(check.status == "ERROR" for check in checks)
    lines.extend(["", "## Recommended Review", ""])
    if error_count:
        lines.append(
            f"- Fix the **{error_count} local error(s)** before publishing new discovery or vendor claims."
        )
    if warning_count:
        lines.append(
            f"- Inspect the **{warning_count} network warning(s)**. Recheck before editing content; temporary remote failures are possible."
        )
    if not error_count and not warning_count:
        lines.append(
            "- Configured automated checks passed; untested claims and hardware/client qualification remain outside this report."
        )
    lines.extend(
        [
            "- Treat a contextual link as durable only while it remains on the upstream default branch.",
            "- Add new public claims only through the repository evidence and validation process.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--network", action="store_true", help="check public sites and known backlinks")
    parser.add_argument("--strict-network", action="store_true", help="treat network warnings as failures")
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--markdown-out", type=Path)
    parser.add_argument("--as-of", type=dt.date.fromisoformat,
                        help="simulate the freshness date only (YYYY-MM-DD); never changes review dates")
    args = parser.parse_args()

    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    checks = local_checks() + freshness_checks(args.as_of)
    metrics: dict[str, int] = {}
    if args.network:
        try:
            remote_checks, metrics = network_checks()
            checks.extend(remote_checks)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            checks.append(Check("network-audit", PROJECT_URL, "ERROR", f"could not complete: {exc}"))

    for check in checks:
        print(f"[{check.status}] {check.name}: {check.target} - {check.detail}")
    if args.json_out:
        write_json(args.json_out, generated_at, checks, metrics)
    if args.markdown_out:
        write_markdown(args.markdown_out, generated_at, checks, metrics)

    if any(check.status == "ERROR" for check in checks):
        return 1
    if args.strict_network and any(check.status == "WARN" for check in checks):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
