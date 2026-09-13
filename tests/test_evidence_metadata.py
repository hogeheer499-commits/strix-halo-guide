import csv
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EvidenceMetadataTests(unittest.TestCase):
    def test_model_bytes_have_source_and_consistent_units(self):
        with (ROOT / 'data/benchmarks.csv').open() as handle:
            for row in csv.DictReader(handle):
                if not row['model_size_bytes']:
                    self.assertFalse(row['model_size_gb'])
                    self.assertFalse(row['model_size_gib'])
                    continue
                value = int(row['model_size_bytes'])
                self.assertAlmostEqual(float(row['model_size_gb']), value / 1e9, places=5)
                self.assertAlmostEqual(float(row['model_size_gib']), value / 2**30, places=5)
                path = ROOT / row['model_size_source']
                with path.open() as source:
                    if path.suffix == '.jsonl':
                        source_rows = [json.loads(line) for line in source if line.strip()]
                    else:
                        source_rows = list(csv.DictReader(source))
                self.assertIn(value, [int(item['model_size']) for item in source_rows if item.get('model_size')])

    def test_minimax_delta_names_successful_two_node_baseline(self):
        with (ROOT / 'data/community_rpc.csv').open() as handle:
            rows = [row for row in csv.DictReader(handle) if row['model'] == 'MiniMax-M2.7 230B' and row['tg128_tps']]
        baseline = next(float(row['tg128_tps']) for row in rows if row['nodes'] == '2')
        for row in rows:
            self.assertEqual(row['baseline_nodes'], '2')
            self.assertAlmostEqual(float(row['tg_delta_vs_baseline_pct']), (float(row['tg128_tps']) / baseline - 1) * 100, places=2)


if __name__ == '__main__':
    unittest.main()
