"""Targeted editorial regression guards, not a whole-guide fact checker."""
import csv
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def active_readme(text):
    before, sep, rest = text.partition("## Changelog")
    if sep:
        _, tail_sep, tail = rest.partition("## Next Useful Tests")
        return before + (tail_sep + tail if tail_sep else "")
    return text


def guidance_errors(text):
    text = active_readme(text)
    errors = []
    for pattern in (
        r"always (?:use|disable).{0,40}(?:mmap|on Strix Halo)",
        r"tuned[^\n]*(?:\+5[-–]8%|worth several percent)",
        r"PyTorch doesn't handle UMA correctly",
        r"\|[^\n]*\*\*llama-server\*\*[^\n]*\d+(?:\.\d+)? t/s",
        r"(?:against open|versus|vs\.?) PR #?25863",
        r"any (?:tool that supports OpenAI API|OpenAI-compatible client)",
    ):
        if re.search(pattern, text, re.I):
            errors.append(pattern)
    for block in re.findall(r"```bash\n(.*?)```", text, re.S):
        for line in block.splitlines():
            if re.search(r"^git clone .*github.com/ggml-org/llama.cpp", line):
                if "--branch v0.4.1 --depth 1" not in line:
                    errors.append("unpinned current llama.cpp clone")
        # Explicitly current candidates only: historical blocks keep old flags.
        if "v0.4.1" in block:
            if "./build-vulkan/" in block:
                errors.append("candidate executable directory differs from documented build")
            if re.search(r"(?:--no-mmap|--mmap|--mlock|--direct-io|-mmp)\b", block):
                errors.append("removed flag in v0.4.1 example")
            if re.search(r"-fa\s+(?!on\b|off\b|auto\b)", block):
                errors.append("invalid candidate Flash Attention value")
    return errors


class ActiveGuidanceTests(unittest.TestCase):
    def test_active_readme_contract(self):
        self.assertEqual(guidance_errors((ROOT / "README.md").read_text()), [])

    def test_negative_editorial_fixtures(self):
        for bad in (
            "always use on Strix Halo --no-mmap",
            "tuned accelerator-performance | **+5-8% overall**",
            "PyTorch doesn't handle UMA correctly",
            "| Speed | **llama-server** -- 101.0 t/s |",
            "stock b10687 versus PR #25863",
            "any OpenAI-compatible client",
            "```bash\ngit clone https://github.com/ggml-org/llama.cpp\n```",
            "```bash\n# v0.4.1\nllama-server --no-mmap -fa on\n```",
            "```bash\n# v0.4.1\nllama-server -fa --load-mode auto\n```",
            "```bash\n# v0.4.1\n./build-vulkan/bin/llama-server --load-mode auto\n```",
        ):
            with self.subTest(bad=bad):
                self.assertTrue(guidance_errors(bad))

    def test_historical_commands_are_not_rewritten(self):
        self.assertEqual(guidance_errors(
            "Historical b8460 reproduction:\n```bash\nllama-bench -mmp 0 -fa 1\n```\n"
            "## Changelog\nstock b10687 versus PR #25863\n"), [])

    def test_hip_queue_is_released_mitigation_not_closed_pr(self):
        with (ROOT / "data/current_test_queue.csv").open() as stream:
            rows = list(csv.reader(stream))
        hip = " ".join(rows[1])
        self.assertIn("b10687", hip)
        self.assertIn("v0.4.1", hip)
        self.assertIn("28604", hip)
        self.assertNotIn("25863", hip)
        for path in ("CURRENT_MODELS.md", "QWEN38_STRIX_HALO.md", "ROCM_VLLM_BUGWATCH.md",
                     "SYSTEM_EVIDENCE_MATRIX.md", "docs/troubleshooting.md"):
            text = (ROOT / path).read_text()
            self.assertNotRegex(text, r"(?:versus|against open) PR #25863")
            self.assertIn("28604", text)

    def test_scope_visible_before_installer(self):
        text = (ROOT / "README.md").read_text().split("## Setup Script", 1)[1]
        intro = text.split("```", 1)[0]
        self.assertIn("120GiB", intro)
        self.assertIn("hardware qualification", intro)
        self.assertIn("not a transactional installer", intro)

    def test_client_privacy_and_runtime_status(self):
        text = (ROOT / "README.md").read_text()
        self.assertIn("Cursor is not an offline-local guarantee", text)
        self.assertIn("reboot-qualified general baseline remains 0.31.2", text)
        self.assertIn("passed the scoped direct/server acceptance controls", text)
        self.assertNotIn("open-webui:main", active_readme(text))
        self.assertNotIn("**Recommendation tiers:**", active_readme(text))
        self.assertIn("not local-only", text)

    def test_closeout_claim_boundaries(self):
        runtime = (ROOT / "RUNTIME_QUALIFICATION_2026-09-19.md").read_text()
        for fragment in ("not the default", "Qwen2.5-VL", "Devstral",
                         "14,029", "not a maximum usable-memory",
                         "No full-host reboot", "not local-only"):
            self.assertIn(fragment, runtime)
        buyer = (ROOT / "BUYER_SNAPSHOT_2026-09-19.md").read_text()
        for fragment in ("128GB/2TB", "$3,649.99", "64GB/1TB",
                         "not a complete PC", "account-specific",
                         "no first-party exact-retail-SKU"):
            self.assertIn(fragment, buyer)
        self.assertEqual(len(list(csv.DictReader(
            (ROOT / "data/affiliate_link_registry.csv").read_text().splitlines()))), 0)
