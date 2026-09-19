import datetime as dt
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_measurement_contracts import load

authority = load('audit_authority_surface')
validator = load('validate_repo')


class PublicValidationTests(unittest.TestCase):
    def network(self, bad_qwen=False, equivalent_wording=False):
        state = json.loads((authority.ROOT / 'data/public_state.json').read_text())
        common = ('AMD Strix Halo Qwen3.8 partner Affiliate commission does not determine '
                  f"{state['coverage']['systems_or_sources']} systems or independent sources "
                  f"{state['coverage']['community_benchmark_contributors']} credited community benchmark contributors "
                  + state['evidence_reviewed_human'] + ' 20.42 50,059 261,130 '
                  '128GB model troubleshooting Vendor Disclosure Policy Affiliate links Negative results stay ')

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
            if equivalent_wording:
                body = body.replace('credited community benchmark contributors', 'benchmark contributors')
                body = body.replace('Affiliate commission does not determine', 'Affiliate commission never determines')
            if url == authority.PAGES_QWEN_URL and bad_qwen:
                canonical, body = authority.PAGES_QWEN_URL, 'wrong content'
            return 200, url, (body + f'<link href="{canonical}" rel="canonical">'
                              '<meta content="' + state['publication']['expected_content_revision']
                              + '" name="guide-content-revision">')

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

    def test_all_decision_surfaces_are_monitored(self):
        checks = self.network()
        for name in ('project-home', 'project-setup', 'project-buyer', 'project-models',
                     'project-qwen', 'project-troubleshooting', 'project-partners', 'project-disclosure'):
            self.assertEqual([c.status for c in checks if c.name == name], ['PASS'])
        revisions = [c for c in checks if c.name == 'publication-revision']
        self.assertEqual(len(revisions), 7)  # disclosure is the linked repository policy
        self.assertTrue(all(c.status == 'PASS' for c in revisions))

    def test_equivalent_wording_does_not_trigger_marker_warnings(self):
        checks = self.network(equivalent_wording=True)
        for name in ('project-home', 'project-partners'):
            self.assertEqual([c.status for c in checks if c.name == name], ['PASS'])

    def test_revision_and_stale_claims_are_independent_of_http_success(self):
        state = {'publication': {'expected_content_revision': 'fixture'}}
        for body in ('', '<meta name="guide-content-revision" content="old">'):
            self.assertEqual(authority.publication_checks(authority.PROJECT_BUYER_URL, body, state)[0].status, 'WARN')
        body = ('<meta name="guide-content-revision" content="fixture">'
                '<p>Best ecosystem/support</p>')
        checks = authority.publication_checks(authority.PROJECT_BUYER_URL, body, state)
        self.assertEqual(checks[0].status, 'PASS')
        self.assertEqual(checks[1].status, 'WARN')

    def test_withdrawal_is_not_an_active_buyer_recommendation(self):
        state = {'publication': {'expected_content_revision': 'fixture'}}
        marker = '<meta name="guide-content-revision" content="fixture">'
        body = marker + '<p>Earlier Framework 192GB PRO 495 claims are withdrawn.</p>'
        self.assertEqual(len(authority.publication_checks(authority.PROJECT_BUYER_URL, body, state)), 1)
        body += '<p>Best ecosystem/support</p>'
        self.assertEqual(len(authority.publication_checks(authority.PROJECT_BUYER_URL, body, state)), 2)

    def test_freshness_boundary_without_changing_review_date(self):
        state = json.loads((authority.ROOT / 'data/public_state.json').read_text())
        reviewed = dt.date.fromisoformat(state['evidence_reviewed'])
        self.assertEqual(authority.freshness_checks(reviewed + dt.timedelta(days=21))[0].status, 'PASS')
        check = authority.freshness_checks(reviewed + dt.timedelta(days=22))[0]
        self.assertEqual(check.status, 'ERROR')
        self.assertIn('22 days', check.detail)
        self.assertEqual(authority.freshness_checks(reviewed - dt.timedelta(days=1))[0].status, 'ERROR')
        with patch.object(validator, 'date') as date:
            date.fromisoformat.side_effect = dt.date.fromisoformat
            date.today.return_value = reviewed + dt.timedelta(days=22)
            errors = []
            validator.check_public_state(errors)
        self.assertTrue(any('stale: 22 days' in e for e in errors))

    def test_stale_run_writes_both_reports_and_still_runs_network(self):
        with tempfile.TemporaryDirectory() as folder:
            md, js = Path(folder) / 'audit.md', Path(folder) / 'audit.json'
            state = json.loads((authority.ROOT / 'data/public_state.json').read_text())
            stale = dt.date.fromisoformat(state['evidence_reviewed']) + dt.timedelta(days=22)
            argv = ['audit', '--as-of', stale.isoformat(), '--network', '--markdown-out', str(md), '--json-out', str(js)]
            remote = authority.Check('remote-fixture', 'https://fixture.invalid', 'PASS', 'checked')
            with patch.object(authority.sys, 'argv', argv), patch.object(
                    authority, 'network_checks', return_value=([remote], {})) as network, patch('sys.stdout', new_callable=io.StringIO):
                self.assertEqual(authority.main(), 1)
                network.assert_called_once()
            self.assertIn('stale: 22 days', md.read_text())
            checks = json.loads(js.read_text())['checks']
            self.assertTrue(any(c['name'] == 'remote-fixture' for c in checks))
            self.assertTrue(any(c['status'] == 'ERROR' for c in checks))

    def test_workflow_does_not_skip_report_after_validation_failure(self):
        workflow = (authority.ROOT / '.github/workflows/authority-audit.yml').read_text()
        step = workflow.split('- name: Audit public authority surfaces', 1)[1].split('- name:', 1)[0]
        self.assertIn('if: ${{ !cancelled() }}', step)
        self.assertNotIn('continue-on-error', workflow)

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
