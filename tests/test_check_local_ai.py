"""Offline setup-check fixtures; no host change, socket or model invocation."""
from contextlib import ExitStack, redirect_stdout
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


def loaded_model(name=check.MODEL, size=1024, vram=1024):
    return {"name": name, "model": name, "size": size, "size_vram": vram}


def system_fixture(memory=128 * 2**30):
    return {"memory_bytes": memory, "kernel": "6.19.4",
            "boot": {p.split("=")[0]: "match" for p in check.BOOT_PARAMETERS},
            "groups": {"render": "active", "video": "active"}}


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
        for args in ([], ["unknown"], ["answer", "--host", "example.invalid"],
                     ["report", "--host", "PRIVATE_CLI_99"], ["report", "--model", "PRIVATE_CLI_99"]):
            with self.subTest(args=args), patch.object(check, "check_boot") as boot, \
                 patch.object(check, "check_answer") as answer, patch.object(check, "check_report") as report, \
                 redirect_stdout(io.StringIO()) as output:
                self.assertEqual(check.main(args), 1)
                self.assertTrue(output.getvalue().startswith("STOP:"))
                boot.assert_not_called()
                answer.assert_not_called()
                report.assert_not_called()
                self.assertNotIn("PRIVATE_CLI_99", output.getvalue())

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


class ReportAllocationTests(unittest.TestCase):
    def test_gpu_cpu_and_mixed_use_runtime_bytes(self):
        for vram, expected in ((1024, "GPU"), (0, "CPU"), (512, "mixed"), (1023, "mixed")):
            with self.subTest(vram=vram):
                state, reason, sizes = check.allocation_metadata({"models": [loaded_model(vram=vram)]})
                self.assertEqual(state, expected)
                self.assertEqual(sizes, (1024, vram))

    def test_exact_selection_among_multiple_models_ignores_order_and_prefixes(self):
        other = loaded_model("private-client-model", vram=0)
        prefix = loaded_model(check.MODEL + "-private", vram=0)
        for rows in ([other, loaded_model(), prefix], [loaded_model(), prefix, other]):
            self.assertEqual(check.allocation_metadata({"models": rows})[0], "GPU")

    def test_missing_empty_unrelated_and_duplicate_models_are_unknown(self):
        for rows in ([], [loaded_model("other")], [loaded_model(check.MODEL + "x")],
                     [loaded_model(), loaded_model()], [loaded_model(), loaded_model(vram=0)]):
            with self.subTest(rows=rows):
                self.assertEqual(check.allocation_metadata({"models": rows})[0], "unknown")

    def test_invalid_schema_error_and_conflicting_identity_are_unknown(self):
        for value in (None, [], {}, {"models": None}, {"models": {}},
                      {"error": "private-error", "models": [loaded_model()]},
                      {"models": [None]}, {"models": [loaded_model(), None]},
                      {"models": [{**loaded_model(), "model": "different"}]},
                      {"models": [{"name": check.MODEL, "size": 1024, "size_vram": 1024}]},
                      {"models": [{**loaded_model(), "name": None}]}):
            with self.subTest(value=value):
                self.assertEqual(check.allocation_metadata(value)[0], "unknown")

    def test_invalid_missing_boolean_float_negative_and_overflow_sizes_are_unknown(self):
        for key in ("size", "size_vram"):
            for invalid in (None, True, False, "1024", 1024.0, -1, [], {}, 2**63, float("nan")):
                row = {**loaded_model(), key: invalid}
                with self.subTest(key=key, value=invalid):
                    self.assertEqual(check.allocation_metadata({"models": [row]})[0], "unknown")
            row = loaded_model()
            del row[key]
            self.assertEqual(check.allocation_metadata({"models": [row]})[0], "unknown")
        for size, vram in ((0, 0), (0, 1), (1024, 1025)):
            self.assertEqual(check.allocation_metadata({"models": [loaded_model(size=size, vram=vram)]})[0], "unknown")


class ReportSystemTests(unittest.TestCase):
    def collect(self, meminfo="MemTotal: 134217728 kB\n", cmdline=None, release="6.19.4", groups=(100, 101)):
        if cmdline is None:
            cmdline = " ".join(check.BOOT_PARAMETERS)
        with patch.object(check, "read_metadata_file", side_effect=[meminfo, cmdline]), \
             patch.object(check.os, "uname", return_value=SimpleNamespace(release=release)), \
             patch.object(check.os, "getgroups", return_value=list(groups)), \
             patch.object(check.os, "getegid", return_value=1000), \
             patch.object(check.grp, "getgrnam", side_effect=lambda name: SimpleNamespace(gr_gid={"render": 100, "video": 101}[name])):
            return check.system_metadata()

    def test_linux_kibibytes_convert_to_gib_and_primary_group_is_counted(self):
        value = self.collect()
        self.assertEqual(value["memory_bytes"] / 2**30, 128)
        self.assertEqual(value["groups"], {"render": "active", "video": "active"})
        self.assertEqual(self.collect(groups=(100,))["groups"]["video"], "inactive")
        with patch.object(check, "read_metadata_file", return_value=""), \
             patch.object(check.os, "getgroups", return_value=[]), \
             patch.object(check.os, "getegid", return_value=101), \
             patch.object(check.grp, "getgrnam", return_value=SimpleNamespace(gr_gid=101)):
            self.assertEqual(check.system_metadata()["groups"]["video"], "active")

    def test_malformed_missing_duplicate_or_oversized_memory_is_unknown(self):
        for text in (None, "", "MemTotal: 2 GB", "MemTotal: -1 kB", "MemTotal: 0 kB",
                     "MemTotal: 134217728 kB\nMemTotal: 1 kB", "MemTotal: " + "9" * 80 + " kB"):
            with self.subTest(text=text):
                self.assertIsNone(self.collect(meminfo=text)["memory_bytes"])

    def test_kernel_suffix_and_unrelated_cmdline_never_reach_metadata(self):
        secret = "PRIVATE_FIXTURE_92"
        value = self.collect(release="6.19.4-" + secret,
                             cmdline=f"root=/private/{secret} console={secret} amdgpu.gttsize={secret}")
        self.assertEqual(value["kernel"], "6.19.4")
        self.assertNotIn(secret, json.dumps(value))
        self.assertEqual(value["boot"]["amdgpu.gttsize"], "different")
        self.assertEqual(value["boot"]["ttm.pages_limit"], "absent")
        self.assertEqual(self.collect(release=secret)["kernel"], "unknown")

    def test_duplicate_boot_parameters_and_unreadable_metadata_are_distinct(self):
        value = self.collect(cmdline=" ".join((*check.BOOT_PARAMETERS, check.BOOT_PARAMETERS[0])))
        self.assertEqual(value["boot"]["amdgpu.gttsize"], "conflicting")
        with patch.object(check, "read_metadata_file", return_value=None), \
             patch.object(check.os, "uname", side_effect=OSError("private")), \
             patch.object(check.os, "getgroups", side_effect=OSError("private")):
            value = check.system_metadata()
        self.assertEqual(value["kernel"], "unknown")
        self.assertEqual(set(value["boot"].values()), {"unknown"})
        self.assertEqual(set(value["groups"].values()), {"unknown"})

    def test_group_database_errors_are_unknown_and_absence_is_reported(self):
        for error, expected in ((OSError("private"), "unknown"), (KeyError("private"), "absent")):
            with patch.object(check, "read_metadata_file", return_value=""), \
                 patch.object(check.grp, "getgrnam", side_effect=error):
                self.assertEqual(set(check.system_metadata()["groups"].values()), {expected})

    def test_proc_read_is_bounded_and_nonascii_or_io_failure_is_hidden(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture"
            for body in (b"x" * (check.MAX_RESPONSE_BYTES + 1), b"\xff"):
                path.write_bytes(body)
                self.assertIsNone(check.read_metadata_file(path))
            path.write_text("test")
            self.assertEqual(check.read_metadata_file(path), "test")
            with patch.object(check.Path, "open", side_effect=PermissionError("secret")):
                self.assertIsNone(check.read_metadata_file(path))


class ReportTests(unittest.TestCase):
    def run_report(self, models=None, version=None, listener_error=None, error=None, system=None):
        with patch.object(check, "system_metadata", return_value=system_fixture() if system is None else system), \
             patch.object(check, "check_listeners", side_effect=listener_error) as listener, \
             patch.object(check, "fetch_metadata", side_effect=error or [
                 {"version": "0.31.2"} if version is None else version,
                 {"models": [loaded_model()]} if models is None else models]) as fetch, \
             patch.object(check, "check_boot") as boot, patch.object(check, "check_answer") as answer, \
             redirect_stdout(io.StringIO()) as output:
            code = check.main(["report"])
            boot.assert_not_called()
            answer.assert_not_called()
            listener.assert_called_once_with(quiet=True)
            return code, output.getvalue(), fetch

    def test_known_allocations_return_zero_without_claiming_setup_pass(self):
        for vram, state in ((1024, "GPU"), (0, "CPU"), (512, "mixed")):
            with self.subTest(state=state):
                code, output, fetch = self.run_report(models={"models": [loaded_model(vram=vram)]})
                self.assertEqual(code, 0)
                self.assertIn(f"Allocation: {state}", output)
                self.assertIn("REPORT: complete (allocation only)", output)
                self.assertNotIn("PASS", output)
                self.assertIn(check.REPORT_NEXT[state], output)
                self.assertEqual([c.args for c in fetch.call_args_list], [("/api/version",), ("/api/ps",)])
                self.assertIn("not proof of GPU execution", output)

    def test_unknown_allocation_or_metadata_returns_two_without_pass(self):
        for kwargs in ({"models": {"models": []}}, {"models": {}}, {"version": {}},
                       {"version": {"version": "0.31.2-secret-build"}},
                       {"system": {**system_fixture(), "memory_bytes": None}},
                       {"system": {**system_fixture(), "kernel": "unknown"}},
                       {"system": {**system_fixture(), "groups": {"render": "unknown", "video": "active"}}}):
            with self.subTest(kwargs=kwargs):
                code, output, _ = self.run_report(**kwargs)
                self.assertEqual(code, 2)
                self.assertIn("REPORT: incomplete/unknown", output)
                self.assertNotIn("PASS", output)

    def test_listener_failure_makes_no_request_and_hides_exception(self):
        code, output, fetch = self.run_report(listener_error=check.CheckFailed("PRIVATE_LISTENER_93"))
        self.assertEqual(code, 1)
        fetch.assert_not_called()
        self.assertIn("no HTTP request was sent", output)
        self.assertIn("Allocation: unknown", output)
        self.assertNotIn("PRIVATE_LISTENER_93", output)

    def test_real_listener_parser_blocks_unsafe_missing_or_invalid_tables(self):
        for ipv4, ipv6 in ((HEADER + tcp("00000000"), HEADER),
                           (HEADER + tcp(), HEADER + tcp("0" * 32)),
                           (HEADER, HEADER), ("invalid", HEADER)):
            with patch.object(check, "system_metadata", return_value=system_fixture()), \
                 patch.object(check.Path, "read_text", side_effect=[ipv4, ipv6]), \
                 patch.object(check.http.client, "HTTPConnection") as connection, \
                 redirect_stdout(io.StringIO()) as output:
                self.assertEqual(check.main(["report"]), 1)
                connection.assert_not_called()
                self.assertIn("Allocation: unknown", output.getvalue())

    def test_timeout_transport_api_and_cancel_failures_stop_without_retry_or_details(self):
        secret = "PRIVATE_ERROR_94"
        for error in (TimeoutError(secret), ConnectionRefusedError(secret),
                      check.http.client.BadStatusLine(secret), check.CheckFailed(secret), KeyboardInterrupt()):
            with self.subTest(error=type(error)):
                code, output, fetch = self.run_report(error=error)
                self.assertEqual(code, 1)
                self.assertEqual(fetch.call_count, 1)
                self.assertNotIn(secret, output)
                self.assertNotIn("Traceback", output)
                self.assertIn("STOP:", output)

    def test_failure_of_second_get_keeps_safe_version_but_allocation_unknown(self):
        code, output, fetch = self.run_report(error=[{"version": "0.31.2"}, TimeoutError("private")])
        self.assertEqual(code, 1)
        self.assertEqual(fetch.call_count, 2)
        self.assertIn("Ollama version: 0.31.2", output)
        self.assertIn("Allocation: unknown", output)

    def test_private_model_fields_error_text_and_versions_are_not_printed(self):
        secret = "PRIVATE_API_95"
        rows = [loaded_model(secret), {**loaded_model(), "digest": secret,
                                      "details": {"family": secret}, "expires_at": secret}]
        code, output, _ = self.run_report(models={"models": rows, "private": secret},
                                         version={"version": secret})
        self.assertEqual(code, 2)
        self.assertIn("Allocation: GPU", output)
        self.assertNotIn(secret, output)
        _, output, _ = self.run_report(models={"error": secret, "models": rows})
        self.assertNotIn(secret, output)
        self.assertIn("Allocation: unknown", output)

    def test_all_memory_classes_keep_128gb_reference_nonprescriptive(self):
        for gib in (32, 64, 96, 128, 192, 48):
            with self.subTest(gib=gib):
                code, output, _ = self.run_report(system=system_fixture(gib * 2**30))
                self.assertEqual(code, 0)
                self.assertIn(f"{gib:.2f} GiB MemTotal", output)
                self.assertIn("not installed RAM/SKU", output)
                self.assertIn("never copy the 128GB boot values to another size", output)
                self.assertNotIn("131072", output)
                self.assertNotIn("31457280", output)

    def test_runtime_version_allows_numeric_release_or_rc_only(self):
        for value, expected in (("0.31.2", "0.31.2"), ("0.31.2-rc1", "0.31.2-rc1"),
                                ("0.31.2\n", "unknown"), ("0.31.2-private", "unknown"),
                                (17, "unknown"), ([], "unknown"), (None, "unknown")):
            self.assertEqual(check.runtime_version({"version": value}), expected)
        self.assertEqual(check.runtime_version({"version": "0.31.2", "error": "secret"}), "unknown")


class ReportHttpTests(unittest.TestCase):
    """Isolated synthetic HTTP boundary, not a running Ollama or host qualification."""

    def run_http_report(self, responses):
        connections = []
        for response in responses:
            connection = Mock()
            connection.getresponse.return_value = response
            connections.append(connection)
        with ExitStack() as stack:
            stack.enter_context(patch.object(check, "system_metadata", return_value=system_fixture()))
            stack.enter_context(patch.object(check.Path, "read_text", side_effect=[HEADER + tcp(), HEADER]))
            factory = stack.enter_context(patch.object(check.http.client, "HTTPConnection", side_effect=connections))
            output = stack.enter_context(redirect_stdout(io.StringIO()))
            code = check.main(["report"])
        for connection in connections[:factory.call_count]:
            connection.close.assert_called_once()
        return code, output.getvalue(), factory, connections

    def response(self, value=None, body=None, status=200, length=None):
        response = Mock(status=status)
        response.getheader.return_value = length
        response.read.return_value = json.dumps(value).encode() if body is None else body
        return response

    def test_synthetic_cpu_fixture_uses_only_two_fixed_gets_despite_host_and_proxy_env(self):
        responses = [self.response({"version": "0.31.2"}),
                     self.response({"models": [loaded_model(vram=0)]})]
        with patch.dict(check.os.environ, {"OLLAMA_HOST": "https://PRIVATE_PROXY_96.invalid",
                                          "HTTP_PROXY": "http://PRIVATE_PROXY_96.invalid",
                                          "HTTPS_PROXY": "http://PRIVATE_PROXY_96.invalid",
                                          "ALL_PROXY": "socks5://PRIVATE_PROXY_96.invalid"}):
            code, output, factory, connections = self.run_http_report(responses)
        self.assertEqual(code, 0)
        self.assertIn("Allocation: CPU", output)
        self.assertNotIn("PRIVATE_PROXY_96", output)
        self.assertEqual(factory.call_count, 2)
        for call, conn, response, path in zip(factory.call_args_list, connections, responses, ("/api/version", "/api/ps")):
            self.assertEqual(call.args, ("127.0.0.1", 11434))
            self.assertEqual(call.kwargs, {"timeout": 5})
            conn.request.assert_called_once_with("GET", path)
            conn.connect.assert_called_once()
            self.assertEqual(conn.auto_open, 0)
            conn.sock.settimeout.assert_called_once_with(10)
            response.read.assert_called_once_with(check.MAX_RESPONSE_BYTES + 1)

    def test_redirect_http_error_and_oversize_length_stop_without_body_or_second_request(self):
        for response in (self.response(status=302), self.response(status=500),
                         self.response(length=str(check.MAX_RESPONSE_BYTES + 1)),
                         self.response(length="PRIVATE_LENGTH_97")):
            code, output, factory, _ = self.run_http_report([response])
            self.assertEqual(code, 1)
            self.assertEqual(factory.call_count, 1)
            response.read.assert_not_called()
            self.assertNotIn("PRIVATE_LENGTH_97", output)

    def test_malformed_json_duplicate_keys_and_large_body_stop_privately(self):
        for body in (b"PRIVATE_JSON_98", b"\xff", b"", b"x" * (check.MAX_RESPONSE_BYTES + 1),
                     b'{"version":"0.31.2","version":"PRIVATE_JSON_98"}',
                     b'{"version":NaN}', b'{"version":Infinity}'):
            with self.subTest(body_length=len(body)):
                code, output, factory, _ = self.run_http_report([self.response(body=body)])
                self.assertEqual(code, 1)
                self.assertEqual(factory.call_count, 1)
                self.assertNotIn("PRIVATE_JSON_98", output)

    def test_json_recursion_failure_stops_without_runtime_depth_assumptions(self):
        with patch.object(check.json, "loads", side_effect=RecursionError):
            code, output, factory, _ = self.run_http_report([self.response(body=b"[]")])
        self.assertEqual(code, 1)
        self.assertEqual(factory.call_count, 1)
        self.assertIn("Allocation: unknown", output)

    def test_duplicate_allocation_fields_are_not_silently_accepted(self):
        body = ('{"models":[{"name":"%s","model":"%s","size":1024,"size_vram":0,"size_vram":1024}]}'
                % (check.MODEL, check.MODEL)).encode()
        code, output, _, _ = self.run_http_report([self.response({"version": "0.31.2"}), self.response(body=body)])
        self.assertEqual(code, 1)
        self.assertIn("Allocation: unknown", output)

    def test_actual_report_deadline_interrupts_response_and_restores_signal(self):
        handlers = []
        response = self.response()
        response.read.side_effect = lambda _count: handlers[0](check.signal.SIGALRM, None)
        with patch.object(check.signal, "signal", side_effect=lambda _sig, handler: handlers.append(handler) or "previous"), \
             patch.object(check.signal, "setitimer") as timer:
            code, output, factory, _ = self.run_http_report([response])
        self.assertEqual(code, 1)
        self.assertEqual(factory.call_count, 1)
        self.assertIn("10s total per GET", output)
        self.assertEqual(timer.call_args_list[0].args, (check.signal.ITIMER_REAL, 10))
        self.assertEqual(timer.call_args_list[-1].args, (check.signal.ITIMER_REAL, 0))
        self.assertEqual(handlers[-1], "previous")

    def test_nonmetadata_endpoint_is_rejected_before_connection(self):
        with patch.object(check.http.client, "HTTPConnection") as connection:
            for path in ("/api/generate", "/api/chat", "/api/pull", "https://example.invalid/api/ps"):
                with self.assertRaises(check.CheckFailed):
                    check.fetch_metadata(path)
            connection.assert_not_called()


if __name__ == "__main__":
    unittest.main()
