import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PATH = Path(__file__).resolve().parents[1] / 'scripts/fetch_uk_grid_intensity.py'
spec = importlib.util.spec_from_file_location('fetch_grid', PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class GridFetchTests(unittest.TestCase):
    def test_bad_payload_does_not_replace_existing_evidence(self):
        for rows in ([{}], [{'from':'2026-09-15T00:00Z','intensity':{'forecast':float('nan')}}],
                     [{'from':'2026-09-15T00:00','intensity':{'forecast':5}}]):
            with tempfile.TemporaryDirectory() as directory:
                old = Path.cwd()
                try:
                    os.chdir(directory)
                    Path('data').mkdir()
                    path = Path('data/grid_intensity_uk_summary.json')
                    path.write_text('preserve')
                    with patch.object(module, 'fetch_json', return_value={'data':rows}):
                        with self.assertRaises(ValueError):
                            module.main()
                    self.assertEqual(path.read_text(), 'preserve')
                finally:
                    os.chdir(old)
