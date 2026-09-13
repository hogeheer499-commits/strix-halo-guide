import json
import unittest
from unittest.mock import patch

from test_measurement_contracts import load

authority = load('audit_authority_surface')
validator = load('validate_repo')


class PublicValidationTests(unittest.TestCase):
    def network(self, bad_qwen=False):
        state = json.loads((authority.ROOT / 'data/public_state.json').read_text())
        common = ('Strix Halo Qwen3.8 partner Affiliate commission does not determine '
                  f"{state['coverage']['systems_or_sources']} systems or independent sources "
                  f"{state['coverage']['community_benchmark_contributors']} credited community benchmark contributors "
                  + state['evidence_reviewed_human'] + ' 20.42 50,059 261,130 ')

        def fetch(url):
            if 'api.github.com' in url:
                return 200, url, json.dumps({'homepage': authority.PROJECT_URL})
            if url.endswith('sitemap.xml'):
                # Content-modified date deliberately differs from evidence-review date.
                return 200, url, ('2026-09-05 ' + authority.PROJECT_URL +
                                 authority.PROJECT_SETUP_URL + authority.PROJECT_PARTNERS_URL +
                                 authority.PROJECT_QWEN_URL)
            canonical = url.replace(authority.PAGES_URL, authority.PROJECT_URL)
            body = common
            if url == authority.PAGES_QWEN_URL and bad_qwen:
                canonical, body = authority.PAGES_QWEN_URL, 'wrong content'
            return 200, url, body + f'<link href="{canonical}" rel="canonical">'

        with patch.object(authority, 'fetch', side_effect=fetch), patch.object(
                authority, 'fetch_no_redirect', return_value=(301, '', authority.PROJECT_URL, '')):
            return authority.network_checks()[0]

    def test_canonical_mirror_and_independent_sitemap_date(self):
        checks = self.network()
        for name in ('github-pages-qwen', 'project-home', 'project-partners', 'project-sitemap'):
            self.assertEqual([c.status for c in checks if c.name == name], ['PASS'])

    def test_missing_content_does_not_skip_wrong_canonical(self):
        checks = [c for c in self.network(True) if c.name == 'github-pages-qwen']
        self.assertEqual(len(checks), 2)
        self.assertTrue(any('markers' in c.detail for c in checks))
        self.assertTrue(any('canonical' in c.detail for c in checks))
        self.assertTrue(all(c.status == 'WARN' for c in checks))

    def test_affiliate_declared_state_and_required_fields(self):
        row = dict(link_id='fixture', status='active', vendor='vendor', product='product',
                   region='US', relationship='affiliate', public_destination='https://example.invalid',
                   last_checked='2026-09-13', disclosure_location='VENDOR_DISCLOSURE.md', notes='')
        errors = []
        validator.check_affiliate_rows([row], True, errors)
        self.assertEqual(errors, [])
        for rows, present in (([row], False), ([], True), ([row, row], True),
                              ([dict(row, disclosure_location='')], True),
                              ([dict(row, status='unknown')], False)):
            errors = []
            validator.check_affiliate_rows(rows, present, errors)
            self.assertTrue(errors)
