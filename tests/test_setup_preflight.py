"""Offline fixtures for the setup.sh OS and RAM guards; never runs setup.sh."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SETUP = (ROOT / 'setup.sh').read_text()
BLOCK = SETUP.split('# BEGIN PREFLIGHT GUARDS', 1)[1].split('\n', 1)[1].split('# END PREFLIGHT GUARDS', 1)[0]
UBUNTU_2404 = 'ID=ubuntu\nVERSION_ID="24.04"\n'


class PreflightGuardTests(unittest.TestCase):
    def run_guard(self, os_release, ram_gb, allow=None):
        with tempfile.TemporaryDirectory() as temporary:
            release = Path(temporary) / 'os-release'
            release.write_text(os_release)
            block = BLOCK.replace('/etc/os-release', str(release))
            prelude = ('set -euo pipefail\n'
                       'warn() { echo "WARN $1"; }; err() { echo "ERR $1" >&2; }\n'
                       'free() { printf "              total\\nMem:  %s 1 1\\n" "$FIXTURE_RAM"; }\n')
            env = dict(os.environ, FIXTURE_RAM=str(ram_gb))
            env.pop('STRIX_HALO_ALLOW_UNQUALIFIED_OS', None)
            if allow is not None:
                env['STRIX_HALO_ALLOW_UNQUALIFIED_OS'] = allow
            return subprocess.run(['bash', '-c', prelude + block + '\necho PASSED'],
                                  env=env, capture_output=True, text=True)

    def test_recorded_ubuntu_and_128gb_class_passes(self):
        result = self.run_guard(UBUNTU_2404, 124)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('PASSED', result.stdout)
        self.assertNotIn('WARN', result.stdout)

    def test_unqualified_os_stops_without_override(self):
        for release in ('ID=ubuntu\nVERSION_ID="26.04"\n', 'ID=fedora\nVERSION_ID=43\n', ''):
            result = self.run_guard(release, 124)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('not qualified', result.stderr)

    def test_unqualified_os_override_warns(self):
        result = self.run_guard('ID=ubuntu\nVERSION_ID="26.04"\n', 124, allow='1')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('WARN', result.stdout)
        self.assertIn('PASSED', result.stdout)

    def test_ram_bounds(self):
        for ram in (61, 119, 137, 186):
            result = self.run_guard(UBUNTU_2404, ram)
            self.assertNotEqual(result.returncode, 0, ram)
            self.assertNotIn('PASSED', result.stdout)
        self.assertIn('192GB', self.run_guard(UBUNTU_2404, 186).stderr)
        for ram in (120, 136):
            self.assertEqual(self.run_guard(UBUNTU_2404, ram).returncode, 0, ram)

    def test_unreadable_ram_stops(self):
        result = self.run_guard(UBUNTU_2404, 'unknown')
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('PASSED', result.stdout)
        self.assertIn('Could not read visible RAM', result.stderr)

    def test_override_does_not_bypass_ram_upper_bound(self):
        result = self.run_guard(UBUNTU_2404, 186, allow='1')
        self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
