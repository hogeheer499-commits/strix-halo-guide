import io
import subprocess
from pathlib import Path
import unittest
from unittest.mock import Mock, patch
from test_measurement_contracts import load

guard = load('run_with_t3_guard')


class GuardTests(unittest.TestCase):
    def test_failed_http_cannot_pass_shell_health(self):
        source = (Path(__file__).resolve().parents[1] / 'scripts/check_benchmark_cleanliness.sh').read_text()
        function = source.split('check_json_ok() {', 1)[1].split('\n}\n', 1)[0]
        command = 'blocker() { echo BLOCK; }; info() { echo PASS; }; curl() { echo \'{"ok":true}\'; return 22; }; check_json_ok() {' + function + '\n}\ncheck_json_ok fixture fixture'
        result = subprocess.run(['bash', '-c', command], text=True, capture_output=True)
        self.assertIn('BLOCK', result.stdout)
        self.assertNotIn('PASS', result.stdout)
    def test_health_requires_json_true(self):
        for payload, expected in ((b'{"ok":true}', True), (b'<html>login</html>', False),
                                  (b'{"ok":"true"}', False), (b'{"ok":false}', False),
                                  (b'[]', False), (b'prefix {"ok":true}', False)):
            response = io.BytesIO(payload)
            response.status = 200
            with patch.object(guard.urllib.request, 'urlopen', return_value=response):
                self.assertEqual(guard.url_ok('http://fixture.invalid', 1), expected)
        self.assertEqual(guard.DEFAULT_URLS, [])

    def test_exception_and_normal_exit_cleanup(self):
        for failure in (RuntimeError('fixture exception'), None):
            process = Mock(pid=12345, returncode=0)
            process.poll.side_effect = [None] if failure else [0]
            with patch.object(guard.sys, 'argv', ['guard', '--', 'fixture']), \
                 patch.object(guard, 'guard_reason', side_effect=[None, failure] if failure else [None]), \
                 patch.object(guard.subprocess, 'Popen', return_value=process), \
                 patch.object(guard, 'terminate_process') as terminate, \
                 patch.object(guard, 'run_cleanup') as cleanup:
                if failure:
                    with self.assertRaises(RuntimeError):
                        guard.main()
                else:
                    self.assertEqual(guard.main(), 0)
                terminate.assert_called_once_with(process, 15.0)
                cleanup.assert_called_once_with([])

    def test_leader_exit_does_not_skip_group_kill(self):
        process = Mock(pid=12345)
        process.poll.return_value = 0
        with patch.object(guard.os, 'killpg') as kill:
            guard.terminate_process(process, 0)
        self.assertEqual(kill.call_args_list[0].args, (12345, guard.signal.SIGTERM))
        self.assertEqual(kill.call_args_list[-1].args, (12345, guard.signal.SIGKILL))
        process.wait.assert_called_once()


if __name__ == '__main__':
    unittest.main()
