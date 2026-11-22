
import tempfile
import unittest
from pathlib import Path

from scanner import (
    scan_directory,
    parse_log_errors,
    summarize_errors,
    format_size,
)


class ScannerTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        self.logs = self.root / "logs"
        self.logs.mkdir()

        self.app_log = self.logs / "app.log"
        self.app_log.write_text(
            "INFO Server started\n"
            "ERROR Database failed\n"
            "error Connection lost\n"
            "WARNING Low memory\n",
            encoding="utf-8",
        )

        self.system_log = self.logs / "system.log"
        self.system_log.write_text(
            "INFO System ready\n"
            "ERROR Disk issue\n",
            encoding="utf-8",
        )

        self.notes = self.root / "notes.txt"
        self.notes.write_text("Normal text file\n", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_scan_finds_files_recursively(self):
        results = scan_directory(self.root)

        paths = [item["path"] for item in results]

        self.assertEqual(len(results), 3)
        self.assertTrue(any("app.log" in path for path in paths))
        self.assertTrue(any("system.log" in path for path in paths))
        self.assertTrue(any("notes.txt" in path for path in paths))

    def test_inventory_contains_size_and_modified(self):
        results = scan_directory(self.root)

        item = next(
            item for item in results
            if item["path"].endswith("notes.txt")
        )

        self.assertIn("size", item)
        self.assertIn("modified", item)
        self.assertGreaterEqual(item["size"], 0)

    def test_case_insensitive_search(self):
        matches = parse_log_errors(
            self.app_log,
            pattern="error",
        )

        self.assertEqual(len(matches), 2)

    def test_case_sensitive_search(self):
        matches = parse_log_errors(
            self.app_log,
            pattern="ERROR",
            ignore_case=False,
        )

        self.assertEqual(len(matches), 1)

    def test_regex_search(self):
        matches = parse_log_errors(
            self.app_log,
            pattern=r"ERROR|WARNING",
            regex=True,
        )

        self.assertEqual(len(matches), 3)

    def test_missing_file_returns_empty_list(self):
        missing = self.root / "missing.log"

        matches = parse_log_errors(missing)

        self.assertEqual(matches, [])

    def test_summary_counts_per_file(self):
        summary = summarize_errors(
            [self.app_log, self.system_log],
            pattern="ERROR",
        )

        self.assertEqual(summary[str(self.app_log)], 2)
        self.assertEqual(summary[str(self.system_log)], 1)

    def test_format_size_bytes(self):
        self.assertEqual(format_size(512), "512 B")

    def test_format_size_kilobytes(self):
        self.assertEqual(format_size(1024), "1.00 KB")

    def test_format_size_megabytes(self):
        self.assertEqual(format_size(1024 * 1024), "1.00 MB")


if __name__ == "__main__":
    unittest.main()
