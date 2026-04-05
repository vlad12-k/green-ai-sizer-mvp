import csv
import json
import unittest
from pathlib import Path


class DashboardEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[1]
        self.docs_evidence = self.repo_root / "docs" / "evidence"

    def test_dashboard_evidence_files_load_and_parse(self) -> None:
        grid_path = self.docs_evidence / "grid_intensity_uk_summary.json"
        probe_path = self.docs_evidence / "probe_run_summary.json"
        csv_path = self.docs_evidence / "scenario-baseline-improved.csv"

        self.assertTrue(grid_path.exists(), f"Missing file: {grid_path}")
        self.assertTrue(probe_path.exists(), f"Missing file: {probe_path}")
        self.assertTrue(csv_path.exists(), f"Missing file: {csv_path}")

        grid = json.loads(grid_path.read_text(encoding="utf-8"))
        probe = json.loads(probe_path.read_text(encoding="utf-8"))

        with csv_path.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))

        for key in ["min_g_per_kwh", "avg_g_per_kwh", "max_g_per_kwh", "generated_utc"]:
            self.assertIn(key, grid)

        for key in ["cache_hit_rate_observed", "small_route_rate_observed"]:
            self.assertIn(key, probe)

        self.assertGreater(len(rows), 0)
        required_headers = {
            "scenario",
            "requests_per_day",
            "cache_hit_rate",
            "small_route_rate",
            "wh_small",
            "wh_large",
            "grid_intensity_g_per_kwh",
        }
        self.assertTrue(required_headers.issubset(set(rows[0].keys())))

        scenarios = {(r.get("scenario") or "").strip().lower() for r in rows}
        self.assertIn("baseline", scenarios)
        self.assertIn("improved", scenarios)

    def test_dashboard_paths_match_docs_evidence(self) -> None:
        app_js = (self.repo_root / "docs" / "app.js").read_text(encoding="utf-8")
        self.assertIn("evidence/grid_intensity_uk_summary.json", app_js)
        self.assertIn("evidence/probe_run_summary.json", app_js)
        self.assertIn("evidence/scenario-baseline-improved.csv", app_js)


if __name__ == "__main__":
    unittest.main()
