import os
import subprocess
import tempfile
import unittest
from pathlib import Path


class CarbonBudgetGateOutputTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[1]

    def test_calc_co2e_outputs_expected_console_and_summary_fields(self) -> None:
        with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
            summary_path = tmp.name

        env = os.environ.copy()
        env["GITHUB_STEP_SUMMARY"] = summary_path

        proc = subprocess.run(
            ["python", "workbook/calc_co2e.py", "999999"],
            cwd=self.repo_root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(proc.returncode, 0, msg=proc.stdout + "\n" + proc.stderr)

        stdout = proc.stdout
        self.assertIn("Budget (gCO2e/1k):", stdout)
        self.assertIn("Improved gCO2e per 1k requests:", stdout)
        self.assertIn("Improved total gCO2e/day:", stdout)

        summary = Path(summary_path).read_text(encoding="utf-8")
        self.assertIn("## Carbon Budget Gate — Results", summary)
        self.assertIn("**Budget:**", summary)
        self.assertIn("**Improved:**", summary)


if __name__ == "__main__":
    unittest.main()
