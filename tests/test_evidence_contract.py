import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'workbook'))
from evidence import load_grid, sync_evidence
from calc_co2e import calc_row


class EvidenceContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for directory in ('data', 'docs/evidence', 'scripts'):
            shutil.copytree(ROOT / directory, self.root / directory)

    def test_summary_must_match_snapshot(self):
        path = self.root / 'data/grid_intensity_uk_summary.json'
        data = json.loads(path.read_text())
        data['avg_g_per_kwh'] = 79.85
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'does not match'):
            load_grid(self.root)

    def test_stale_and_future_evidence_fail(self):
        grid = load_grid(self.root)
        generated = datetime.fromisoformat(grid['generated_utc'])
        for now in (generated + timedelta(hours=49), generated - timedelta(hours=1)):
            with self.assertRaises(ValueError):
                load_grid(self.root, now=now)
        load_grid(self.root, now=generated)

    def test_mirror_drift_fails_and_sync_repairs(self):
        (self.root / 'docs/evidence/probe_run_summary.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'mirror differs'):
            sync_evidence(self.root, check=True)
        sync_evidence(self.root)
        sync_evidence(self.root, check=True)

    def test_python_javascript_agree_using_canonical_grid(self):
        grid = load_grid()
        with (ROOT / 'data/scenario-baseline-improved.csv').open() as f:
            rows = list(csv.DictReader(f))
        source = (ROOT / 'docs/app.js').read_text()
        source = "const document = {addEventListener() {}};\n" + source
        source += '\nconsole.log(JSON.stringify(' + json.dumps(rows) + '.map(r => calcRow(r, ' + json.dumps(grid) + '))));'
        result = subprocess.run(['node', '-e', source], check=True, capture_output=True, text=True)
        actual = json.loads(result.stdout)
        for row, value in zip(rows, actual):
            row['grid_intensity_g_per_kwh'] = grid['avg_g_per_kwh']
            self.assertAlmostEqual(calc_row(row)[0], value)
            for invalid in ('NaN', 'Infinity', '-1'):
                bad = dict(row, wh_small=invalid)
                with self.assertRaises(ValueError):
                    calc_row(bad)

    def test_budget_failure_and_nonfinite_budget(self):
        for budget in ('1', 'NaN', 'Infinity', '-1'):
            result = subprocess.run([sys.executable, 'workbook/calc_co2e.py', budget], cwd=ROOT,
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
