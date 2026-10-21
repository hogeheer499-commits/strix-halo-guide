"""Offline setup-check fixtures; no host change, socket or model invocation."""
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_local_ai", ROOT / "scripts/check_local_ai.py")
check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check)
HEADER = "  sl local_address rem_address st tx_queue rx_queue\n"


def tcp(address="0100007F", port=11434, state="0A"):
    return (f"0: {address}:{port:04X} {'0' * len(address)}:0000 {state} "
            "00000000:00000000 00:00000000 00000000 1000 0 42\n")


def reply(answer="STRIX_CHECK=391", done=True, reason="stop"):
    return {"message": {"content": answer}, "done": done, "done_reason": reason}


class BootTests(unittest.TestCase):
    def run_boot(self, params=None, groups=(100, 101), effective=1000):
        with tempfile.TemporaryDirectory() as directory:
            cmdline = Path(directory) / "cmdline"
            cmdline.write_text("quiet " + " ".join(params or check.BOOT_PARAMETERS))
            with patch.object(check.os, "getgroups", return_value=list(groups)), \
                 patch.object(check.os, "getegid", return_value=effective), \
                 patch.object(check.grp, "getgrnam", side_effect=lambda name: SimpleNamespace(gr_gid={"render": 100, "video": 101}[name])), \
                 redirect_stdout(io.StringIO()) as output:
                try:
                    check.check_boot(cmdline)
                    return True, output.getvalue()
                except check.CheckFailed:
                    return False, output.getvalue()

    def test_exact_parameters_and_active_session_groups_pass(self):
        good, output = self.run_boot()
        self.assertTrue(good)
        self.assertEqual(output.count("OK "), 5)

    def test_missing_substring_conflicting_and_duplicate_parameters_stop(self):
        for params in (
            check.BOOT_PARAMETERS[1:],
            ("amdgpu.gttsize=1310720", *check.BOOT_PARAMETERS[1:]),
            (*check.BOOT_PARAMETERS, "amdgpu.gttsize=64"),
            (*check.BOOT_PARAMETERS, check.BOOT_PARAMETERS[0]),
        ):
            with self.subTest(params=params):
                good, output = self.run_boot(params)
                self.assertFalse(good)
                self.assertIn("MISSING amdgpu.gttsize=131072", output)

    def test_database_membership_does_not_replace_session_membership(self):
        good, output = self.run_boot(groups=(100,))
        self.assertFalse(good)
        self.assertIn("MISSING video in current session", output)

    def test_effective_primary_group_counts(self):
        self.assertTrue(self.run_boot(groups=(100,), effective=101)[0])

    def test_unreadable_cmdline_or_groups_stop(self):
        with patch.object(check.Path, "read_text", side_effect=PermissionError):
            with self.assertRaisesRegex(check.CheckFailed, "Cannot read"):
                check.check_boot()
        with patch.object(check.Path, "read_text", return_value="quiet"), \
             patch.object(check.os, "getgroups", side_effect=OSError):
            with self.assertRaisesRegex(check.CheckFailed, "Cannot read"):
                check.check_boot()


class ListenerTests(unittest.TestCase):
    def run_tables(self, ipv4, ipv6=HEADER):
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / name for name in ("tcp", "tcp6")]
            paths[0].write_text(ipv4)
            paths[1].write_text(ipv6)
            with redirect_stdout(io.StringIO()):
                check.check_listeners(paths)

    def test_exact_ipv4_loopback_passes(self):
        self.run_tables(HEADER + tcp())

    def test_any_broad_or_other_ipv4_listener_stops_even_with_loopback(self):
        for address in ("00000000", "0100000A", "0200007F"):
            with self.subTest(address=address):
                with self.assertRaisesRegex(check.CheckFailed, "non-profile"):
                    self.run_tables(HEADER + tcp() + tcp(address))

    def test_ipv6_unspecified_loopback_and_mapped_listeners_stop(self):
        for address in ("0" * 32, "0" * 24 + "01000000", "0000000000000000FFFF00000100007F"):
            with self.subTest(address=address):
                with self.assertRaisesRegex(check.CheckFailed, "non-profile"):
                    self.run_tables(HEADER + tcp(), HEADER + tcp(address))

    def test_other_ports_and_non_listening_connections_are_ignored(self):
        self.run_tables(HEADER + tcp() + tcp("00000000", port=3000),
                        HEADER + tcp("0" * 32, state="01"))

    def test_no_listener_stops(self):
        for table in (HEADER, HEADER + tcp(state="01")):
            with self.assertRaisesRegex(check.CheckFailed, "Service not ready"):
                self.run_tables(table)

    def test_missing_or_unreadable_either_table_stops(self):
        for reads in ([PermissionError()], [HEADER + tcp(), FileNotFoundError()]):
            with self.subTest(reads=reads), patch.object(check.Path, "read_text", side_effect=reads):
                with self.assertRaisesRegex(check.CheckFailed, "Cannot read both"):
                    check.check_listeners()

    def test_malformed_or_unknown_data_in_either_table_stops(self):
        for bad in ("", "garbage", HEADER + "0: broken", HEADER + tcp().replace("0A", "ZZ"),
                    HEADER + "0: 0100007F:2CAA 00000000:0000 0A\n",
                    HEADER + tcp(state="FF")):
            for tables in ((bad, HEADER), (HEADER + tcp(), bad)):
                with self.subTest(tables=tables):
                    with self.assertRaisesRegex(check.CheckFailed, "Cannot interpret"):
                        self.run_tables(*tables)

    def test_listener_failure_prevents_any_http_request(self):
        with patch.object(check, "check_listeners", side_effect=check.CheckFailed("unsafe listener")), \
             patch.object(check, "fetch_answer") as fetch, redirect_stdout(io.StringIO()) as output:
            self.assertEqual(check.main(["answer"]), 1)
            fetch.assert_not_called()
            self.assertIn("STOP:", output.getvalue())


class AnswerTests(unittest.TestCase):
    def run_answer(self, value=None, failure=None):
        with patch.object(check, "check_listeners"), \
             patch.object(check, "fetch_answer", return_value=value, side_effect=failure), \
             redirect_stdout(io.StringIO()) as output:
            code = check.main(["answer"])
            return code, output.getvalue()

    def test_known_answer_and_normal_completion_pass(self):
        code, output = self.run_answer(reply())
        self.assertEqual(code, 0)
        self.assertIn("Answer: STRIX_CHECK=391\nCompletion: True stop\nPASS\n", output)

    def test_missing_empty_repeated_wrong_and_abnormal_answers_stop(self):
        values = [None, [], {}, {"message": None}, {"message": {"content": 391}},
                  {"error": "model not found"}, {"error": "", **reply()},
                  reply(""), reply(" \n"), reply("STRIX_CHECK=391 STRIX_CHECK=391"),
                  reply("STRIX_CHECK=392"), reply(done=False), reply(done=1),
                  reply(reason="length"), reply(reason=None)]
        value = reply()
        del value["done"]
        values.append(value)
        value = reply()
        del value["done_reason"]
        values.append(value)
        for value in values:
            with self.subTest(value=value):
                code, output = self.run_answer(value)
                self.assertEqual(code, 1)
                self.assertIn("STOP:", output)
                self.assertNotIn("\nPASS", output)
                self.assertNotIn("Traceback", output)

    def test_operational_errors_are_readable_without_traceback(self):
        for failure in (TimeoutError(), ConnectionRefusedError(), OSError(),
                        check.http.client.RemoteDisconnected(), check.http.client.BadStatusLine("bad")):
            with self.subTest(failure=failure):
                code, output = self.run_answer(failure=failure)
                self.assertEqual(code, 1)
                self.assertIn('→ see "If A Step Fails"', output)
                self.assertNotIn("Traceback", output)

    def test_large_repeated_or_terminal_control_output_is_bounded(self):
        code, output = self.run_answer(reply("\x1b[31m\n" + "X" * 65000))
        self.assertEqual(code, 1)
        self.assertLess(len(output), 600)
        self.assertNotIn("\x1b", output)


class HttpTests(unittest.TestCase):
    def fetch(self, body=None, status=200, length=None, error=None):
        response = Mock(status=status)
        response.getheader.return_value = length
        response.read.return_value = json.dumps(reply()).encode() if body is None else body
        connection = Mock()
        connection.getresponse.return_value = response
        connection.getresponse.side_effect = error
        with patch.object(check.http.client, "HTTPConnection", return_value=connection) as factory:
            try:
                return check.fetch_answer(), factory, connection, response
            finally:
                connection.close.assert_called_once()

    def test_fixed_request_ignores_host_and_proxy_environment(self):
        with patch.dict(check.os.environ, {"OLLAMA_HOST": "https://untrusted.invalid:443",
                                          "HTTP_PROXY": "http://untrusted.invalid:1234",
                                          "ALL_PROXY": "socks5://untrusted.invalid:1234"}):
            value, factory, connection, response = self.fetch()
        self.assertEqual(value, reply())
        factory.assert_called_once_with("127.0.0.1", 11434, timeout=5)
        connection.connect.assert_called_once()
        connection.request.assert_called_once()
        method, target, body, headers = connection.request.call_args.args
        self.assertEqual((method, target), ("POST", "/api/chat"))
        self.assertEqual(json.loads(body), {
            "model": "qwen3.6:35b-a3b",
            "messages": [{"role": "user", "content":
                          "Compute 17 * 23. Reply with exactly this format and no other text: STRIX_CHECK=<integer>"}],
            "think": False,
            "stream": False,
            "options": {"num_ctx": 8192, "temperature": 0, "seed": 42, "num_predict": 96},
        })
        self.assertNotIn("391", json.loads(body)["messages"][0]["content"])
        self.assertEqual(headers, {"Content-Type": "application/json"})
        response.read.assert_called_once_with(check.MAX_RESPONSE_BYTES + 1)

    def test_http_error_and_redirect_do_not_follow_or_read_body(self):
        for status in (301, 302, 307, 400, 404, 500):
            with self.subTest(status=status):
                with self.assertRaisesRegex(check.CheckFailed, f"HTTP {status}"):
                    self.fetch(status=status)

    def test_oversized_and_invalid_declared_or_actual_response_stop(self):
        for options in ({"length": str(check.MAX_RESPONSE_BYTES + 1)},
                        {"length": "invalid"}, {"length": "-1"},
                        {"length": "9" * 5000}, {"length": "²"},
                        {"body": b"x" * (check.MAX_RESPONSE_BYTES + 1)}):
            with self.subTest(options=options):
                with self.assertRaisesRegex(check.CheckFailed, "64KiB"):
                    self.fetch(**options)

    def test_invalid_empty_and_non_unicode_json_stop(self):
        for body in (b"", b"not json", b"\xff"):
            with self.subTest(body=body[:20]):
                with self.assertRaisesRegex(check.CheckFailed, "invalid JSON"):
                    self.fetch(body=body)

    def test_json_recursion_failure_is_reported_without_runtime_depth_assumptions(self):
        with patch.object(check.json, "loads", side_effect=RecursionError):
            with self.assertRaisesRegex(check.CheckFailed, "invalid JSON"):
                self.fetch()

    def test_network_timeout_and_protocol_failure_close_connection(self):
        for error in (TimeoutError(), check.http.client.IncompleteRead(b"")):
            with self.subTest(error=error), self.assertRaises(type(error)):
                self.fetch(error=error)

    def test_connect_failure_closes_connection_without_sending_request(self):
        connection = Mock()
        connection.connect.side_effect = TimeoutError()
        with patch.object(check.http.client, "HTTPConnection", return_value=connection):
            with self.assertRaises(TimeoutError):
                check.fetch_answer()
        connection.request.assert_not_called()
        connection.close.assert_called_once()

    def test_total_alarm_raises_and_restores_handler(self):
        handlers=[]
        with patch.object(check.signal, "signal", side_effect=lambda _sig, handler: handlers.append(handler) or "previous"), \
             patch.object(check.signal, "setitimer") as timer:
            with self.assertRaises(TimeoutError):
                with check.request_deadline():
                    handlers[0](check.signal.SIGALRM, None)
        self.assertEqual(timer.call_args_list[0].args, (check.signal.ITIMER_REAL, 180))
        self.assertEqual(timer.call_args_list[-1].args, (check.signal.ITIMER_REAL, 0))
        self.assertEqual(handlers[-1], "previous")


class CommandTests(unittest.TestCase):
    def test_invalid_cli_stops_without_work(self):
        for args in ([], ["unknown"], ["answer", "--host", "example.invalid"]):
            with self.subTest(args=args), patch.object(check, "check_boot") as boot, \
                 patch.object(check, "check_answer") as answer, redirect_stdout(io.StringIO()) as output:
                self.assertEqual(check.main(args), 1)
                self.assertTrue(output.getvalue().startswith("STOP:"))
                boot.assert_not_called()
                answer.assert_not_called()

    def test_boot_success_and_failure_use_same_exit_contract(self):
        for failure, expected in ((None, 0), (check.CheckFailed("missing boot value"), 1)):
            with self.subTest(failure=failure), patch.object(check, "check_boot", side_effect=failure), \
                 redirect_stdout(io.StringIO()) as output:
                self.assertEqual(check.main(["boot"]), expected)
                self.assertTrue(output.getvalue().startswith("PASS" if expected == 0 else "STOP:"))


class DriftTests(unittest.TestCase):
    def test_model_and_exact_boot_parameters_match_setup_script(self):
        setup = (ROOT / "setup.sh").read_text()
        parameters = re.search(r'^NEEDED_PARAMS="([^"]+)"$', setup, re.M).group(1).split()
        self.assertEqual(list(check.BOOT_PARAMETERS), parameters)
        pulled = re.findall(r'^\s*ollama pull ([^\s]+)', setup, re.M)
        self.assertEqual(pulled, [check.MODEL])
        self.assertEqual(check.PAYLOAD["model"], check.MODEL)
        self.assertFalse(check.PAYLOAD["stream"])
        self.assertFalse(check.PAYLOAD["think"])


if __name__ == "__main__":
    unittest.main()
