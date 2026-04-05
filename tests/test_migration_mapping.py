import re
import unittest
from pathlib import Path


class MigrationMappingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[1]
        self.migration_file = self.repo_root / "MIGRATION.md"

    def _load_mapping(self):
        text = self.migration_file.read_text(encoding="utf-8")
        mapping = {}
        pattern = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*$")
        for line in text.splitlines():
            m = pattern.match(line)
            if m:
                old_path, new_path = m.group(1), m.group(2)
                mapping[old_path] = new_path
        return mapping

    def test_migration_mapping_targets_exist(self) -> None:
        mapping = self._load_mapping()
        self.assertGreater(len(mapping), 0, "No MIGRATION mappings found")

        missing_targets = []
        for new_path in mapping.values():
            if not (self.repo_root / new_path).exists():
                missing_targets.append(new_path)

        self.assertEqual([], missing_targets, f"Missing mapped targets: {missing_targets}")

    def test_known_legacy_paths_resolve(self) -> None:
        mapping = self._load_mapping()
        legacy_paths = [
            "workbook/appendix-d-baseline-improved.csv",
            "docs/appendix-a-architecture.md",
            "docs/controls.md",
        ]

        for old_path in legacy_paths:
            self.assertIn(old_path, mapping)
            resolved = self.repo_root / mapping[old_path]
            self.assertTrue(resolved.exists(), f"Resolved path does not exist: {resolved}")


if __name__ == "__main__":
    unittest.main()
