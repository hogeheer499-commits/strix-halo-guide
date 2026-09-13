import csv
from pathlib import Path
import tempfile
import unittest
from test_measurement_contracts import load, ROOT

density = load('parse_density_gate_campaign')


class DensityTests(unittest.TestCase):
    def test_shared_summary_retains_every_campaign_and_value(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'summary.csv'
            detail = Path(temporary) / 'detail.csv'
            rows = density.collect()
            density.write_detail(rows, detail)
            density.write_summary(rows, target)
            with target.open() as handle:
                actual = list(csv.DictReader(handle))
            with density.SUMMARY.open() as handle:
                expected = list(csv.DictReader(handle))
            key = lambda row: tuple(row[field] for field in ('date', 'system', 'model', 'tool_route', 'concurrency', 'source'))
            self.assertEqual({key(row): row for row in actual}, {key(row): row for row in expected})
            self.assertEqual(len(actual), 92)
            self.assertEqual(len([row for row in actual if row['date'] == '2026-07-16']), 4)
            self.assertEqual(detail.read_bytes(), density.DETAIL.read_bytes())


if __name__ == '__main__':
    unittest.main()
