import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SETUP = (ROOT / 'setup.sh').read_text()


class SetupOutcomeTests(unittest.TestCase):
    def test_generated_smoke_helper_matches_source(self):
        embedded = SETUP.split("tee \"$SMOKE_HELPER\" > /dev/null << 'SCRIPT'\n", 1)[1].split('\nSCRIPT', 1)[0]
        self.assertEqual(embedded + '\n', (ROOT / 'scripts/ollama_smoke.sh').read_text())

    def test_serialization_and_http_response_failures(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            curl = directory / 'curl'
            curl.write_text('#!/usr/bin/env python3\nimport os,sys\nfrom pathlib import Path\nPath(os.environ["CAPTURE"]).write_text(sys.stdin.read())\nprint(os.environ["RESPONSE"])\nsys.exit(int(os.environ.get("CURL_STATUS","0")))\n')
            curl.chmod(0o755)
            response = {'done': True, 'response': 'Useful text', 'prompt_eval_count': 5,
                        'prompt_eval_duration': 100, 'eval_count': 2, 'eval_duration': 200, 'total_duration': 400}
            env = dict(os.environ, PATH=str(directory) + os.pathsep + os.environ['PATH'],
                       CAPTURE=str(directory / 'request.json'), RESPONSE=json.dumps(response), PYTHONOPTIMIZE='1')
            prompt = 'Quoted "text"\nand a backslash \\ plus $literal'
            command = ['bash', str(ROOT / 'scripts/ollama_smoke.sh'), 'model"name', prompt]
            result = subprocess.run(command, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads((directory / 'request.json').read_text())
            self.assertEqual(payload['prompt'], prompt)
            self.assertEqual(payload['model'], 'model"name')
            for invalid in ('not json', '{}', json.dumps(dict(response, done=False)), json.dumps(dict(response, response=''))):
                result = subprocess.run(command, env=dict(env, RESPONSE=invalid), capture_output=True)
                self.assertNotEqual(result.returncode, 0)
            result = subprocess.run(command, env=dict(env, CURL_STATUS='22'), capture_output=True)
            self.assertNotEqual(result.returncode, 0)

    def test_grub_missing_conflicting_and_pending_rerun(self):
        block = SETUP.split('GRUB_FILE=', 1)[1].split('# Modprobe configuration', 1)[0]
        block = 'GRUB_FILE=' + block
        block = block.replace('/etc/default/grub', '${FIXTURE_DIR}/grub').replace('/proc/cmdline', '${FIXTURE_DIR}/cmdline')
        prelude = 'set -euo pipefail\nREBOOT_REQUIRED=0\nlog() { :; }; info() { :; }; warn() { :; }; err() { echo "$1" >&2; }; sudo() { "$@"; }; update-grub() { :; }\n'
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            env = dict(os.environ, FIXTURE_DIR=temporary)
            grub = directory / 'grub'
            grub.write_text('# keep this comment\nGRUB_TIMEOUT=5\n')
            (directory / 'cmdline').write_text('quiet splash\n')
            command = ['bash', '-c', prelude + block + '\necho "$REBOOT_REQUIRED"']
            for _ in range(2):
                result = subprocess.run(command, env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.strip(), '1')
            self.assertEqual(grub.read_text().count('GRUB_CMDLINE_LINUX_DEFAULT='), 1)
            self.assertIn('GRUB_TIMEOUT=5', grub.read_text())
            grub.write_text('GRUB_CMDLINE_LINUX_DEFAULT="quiet amdgpu.gttsize=1"\n')
            result = subprocess.run(command, env=env, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('gttsize=1', grub.read_text())

    def test_readiness_exhaustion_cannot_continue(self):
        block = SETUP.split('OLLAMA_READY=0', 1)[1].split('# Pull recommended model', 1)[0]
        command = 'set -euo pipefail\nerr() { :; }; log() { :; }; sleep() { :; }; curl() { printf "{}"; }; OLLAMA_READY=0' + block
        result = subprocess.run(['bash', '-c', command], capture_output=True)
        self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
