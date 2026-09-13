"""Offline fixtures: extract only configuration functions, never run setup.sh."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / 'setup.sh').read_text()
FUNCTIONS = SOURCE.split('# BEGIN OLLAMA CONFIGURATION FUNCTIONS', 1)[1].split('\n', 1)[1].split('# END OLLAMA CONFIGURATION FUNCTIONS', 1)[0]


class ConfigurationTests(unittest.TestCase):
    def run_fixture(self, environment='', files='', unsets='', existing=None, fail=''):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            custom = directory / 'override.conf'
            custom.write_text('[Service]\nEnvironment="OLLAMA_MODELS=/custom models"\nMemoryMax=90G\n# OLLAMA_VULKAN=0\n')
            target = directory / '60-strix-halo-guide.conf'
            if existing is not None:
                target.write_text(existing)
            # systemctl's merged output is the contract under test; this mock
            # deliberately models later drop-ins overriding the guide values.
            prelude = r'''
err() { echo "$1" >&2; }
log() { echo "$1"; }
sudo() { "$@"; }
systemctl() {
    if [ "$1" = "$FAIL" ]; then return 1; fi
    case "$1" in
      daemon-reload|restart) return 0 ;;
      show)
        case "$4" in
          Environment)
            if [ -f "$FIXTURE_DIR/60-strix-halo-guide.conf" ]; then
                sed -n 's/^Environment=//p' "$FIXTURE_DIR/60-strix-halo-guide.conf" | tr '\n' ' '
            fi
            printf '%s\n' "$EXISTING_ENV" ;;
          EnvironmentFiles) printf '%s\n' "$EXISTING_FILES" ;;
          UnsetEnvironment) printf '%s\n' "$EXISTING_UNSETS" ;;
        esac ;;
    esac
}
'''
            env = dict(os.environ, FIXTURE_DIR=str(directory), EXISTING_ENV=environment,
                       EXISTING_FILES=files, EXISTING_UNSETS=unsets, FAIL=fail)
            # Conditional invocation ensures failure propagation doesn't rely
            # on bash errexit, which is disabled in conditional function calls.
            command = prelude + FUNCTIONS + '\nif configure_ollama "$FIXTURE_DIR"; then configure_ollama "$FIXTURE_DIR"; else exit 1; fi\n'
            result = subprocess.run(['bash', '-c', command], env=env, text=True, capture_output=True)
            self.assertIn('MemoryMax=90G', custom.read_text())
            self.assertIn('OLLAMA_MODELS=/custom models', custom.read_text())
            return result, target.read_text() if target.exists() else None

    def test_missing_and_commented_settings_preserved_and_rerun(self):
        result, content = self.run_fixture(environment='OLLAMA_MODELS="/custom models"')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('OLLAMA_VULKAN=1', content)

    def test_conflicting_later_dropin(self):
        result, content = self.run_fixture(environment='OLLAMA_VULKAN=0')
        self.assertNotEqual(result.returncode, 0)
        self.assertIsNone(content)

    def test_file_and_unset_contracts_require_review(self):
        for options in ({'files': '/etc/ollama.env'}, {'unsets': 'OLLAMA_VULKAN'}):
            with self.subTest(options=options):
                result, content = self.run_fixture(**options)
                self.assertNotEqual(result.returncode, 0)
                self.assertIsNone(content)

    def test_existing_owned_filename_not_overwritten(self):
        result, content = self.run_fixture(existing='# custom content\n')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(content, '# custom content\n')

    def test_failed_service_operations_are_failures(self):
        for operation in ('daemon-reload', 'restart'):
            with self.subTest(operation=operation):
                result, _ = self.run_fixture(fail=operation)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('environment matches', result.stdout)


if __name__ == '__main__':
    unittest.main()
