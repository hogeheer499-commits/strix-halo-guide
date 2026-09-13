import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


benchmark = load('benchmark_openai_server')
features = load('check_openai_server_features')


class Response(io.BytesIO):
    status = 200


def stream(tokens=3, done=True, finish='stop', usage=True, content='three words here'):
    events = [{'choices': [{'text': content, 'finish_reason': None}]}]
    events.append({'choices': [{'text': '', 'finish_reason': finish}]})
    if usage:
        events.append({'choices': [], 'usage': {'prompt_tokens': 5, 'completion_tokens': tokens}})
    data = ''.join('data: ' + json.dumps(event) + '\n\n' for event in events)
    if done:
        data += 'data: [DONE]\n\n'
    return data.encode()


class AccountingTests(unittest.TestCase):
    def run_one(self, data, mode='fixed'):
        with patch.object(benchmark.urllib.request, 'urlopen', return_value=Response(data)):
            return benchmark.run_one('http://fixture.invalid', 'fixture', 1, 0, 0, 'measure', 3, 1, 'prompt', mode)

    def test_multi_token_chunk_uses_usage(self):
        result = self.run_one(stream())
        self.assertEqual(result.tokens, 3)
        self.assertEqual(result.chunks, 1)
        self.assertFalse(result.error)

    def test_missing_usage_never_counts_chunks(self):
        result = self.run_one(stream(usage=False))
        self.assertIsNone(result.tokens)
        self.assertIsNone(result.request_wall_tps)
        self.assertTrue(result.error)

    def test_invalid_and_truncated_responses(self):
        for data in (stream(done=False), stream(finish=None), stream(content=''),
                     b'data: invalid\n', b'data: []\n', stream(tokens=True),
                     stream(tokens=-1), stream(tokens=float('nan')), stream(tokens='3')):
            with self.subTest(data=data):
                result = self.run_one(data)
                self.assertTrue(result.error)
                self.assertIsNone(result.request_wall_tps)

    def test_natural_completion_is_distinct(self):
        self.assertTrue(self.run_one(stream(tokens=2)).error)
        self.assertFalse(self.run_one(stream(tokens=2), 'natural').error)

    def test_invalid_batch_has_no_success_metrics(self):
        invalid = self.run_one(stream(usage=False))
        with patch.object(benchmark, 'run_one', return_value=invalid):
            _, summary = benchmark.run_batch('fixture', 'fixture', 1, 0, 'measure', 3, 1, 'prompt')
        self.assertEqual(summary['errors'], 1)
        self.assertEqual(summary['valid_requests'], 0)
        self.assertIsNone(summary['aggregate_tps'])
        self.assertIsNone(summary['p95_request_mean_decode_interval_s'])


class FeatureTests(unittest.TestCase):
    def test_empty_and_invalid_not_semantic_success(self):
        for payload in ('bad json', [], {}, {'choices': []}, {'choices': [{'message': {'content': ''}}]}):
            for kind in ('models', 'chat', 'completion', 'tools'):
                self.assertFalse(features.semantic_success(kind, payload, 'fixture'))

    def test_content_and_tools_are_separate(self):
        payload = {'choices': [{'finish_reason': 'tool_calls', 'message': {'tool_calls': [
            {'id': 'call_1', 'type': 'function', 'function': {'name': 'get_weather', 'arguments': '{"city":"Paris"}'}}
        ]}}]}
        self.assertTrue(features.semantic_success('tools', payload, 'fixture'))
        self.assertFalse(features.semantic_success('chat', payload, 'fixture'))
        payload['choices'][0]['message']['tool_calls'][0]['function']['arguments'] = 'not json'
        self.assertFalse(features.semantic_success('tools', payload, 'fixture'))

    def test_role_only_stream_is_not_content(self):
        data = b'data: {"choices":[{"delta":{"role":"assistant"},"finish_reason":"stop"}]}\n\ndata: [DONE]\n'
        with patch.object(features.urllib.request, 'urlopen', return_value=Response(data)):
            ok, status, _, _ = features.request_streaming_chat('http://fixture.invalid', 'fixture', 1, None)
        self.assertFalse(ok)
        self.assertEqual(status, 200)


if __name__ == '__main__':
    unittest.main()
