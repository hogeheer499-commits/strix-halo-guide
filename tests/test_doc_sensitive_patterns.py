"""Public-doc privacy patterns: maintainer paths, hostnames and LAN dumps."""
import unittest

from test_measurement_contracts import load

validator = load('validate_repo')


def hits(text):
    return [name for name, pattern in validator.DOC_SENSITIVE_PATTERNS.items() if pattern.search(text)]


class DocSensitivePatternTests(unittest.TestCase):
    def test_private_host_details_are_flagged(self):
        # Fixtures are assembled at run time so this file passes the scan itself.
        for text in ('loaded from /home/' + 'hoge-heer/models', 'host example-GTR' + '-Pro booted',
                     'proxy at 192.' + '168.1.20:3773', '== Listening ' + 'Ports =='):
            with self.subTest(text=text):
                self.assertTrue(hits(text))

    def test_public_versions_and_placeholders_pass(self):
        for text in ('~/models/qwen.gguf', 'Beelink GTR9 Pro', 'ROCm 10.0.0', 'Mesa 26.1.7',
                     'Ollama 0.31.2', 'http://127.0.0.1:11434'):
            with self.subTest(text=text):
                self.assertEqual(hits(text), [])


if __name__ == '__main__':
    unittest.main()
