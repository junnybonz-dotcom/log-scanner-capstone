
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO
from contextlib import redirect_stderr
from scanner import main


class CLITests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        (self.root / "app.log").write_text(
            "ERROR first issue\n"
            "INFO working normally\n"
            "WARNING second issue\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_cli_default_pattern(self):
        output = StringIO()

        with redirect_stdout(output):
            result = main([str(self.root)])

        self.assertEqual(result, 0)
        self.assertIn("ERROR", output.getvalue())
        self.assertIn("Total matches: 1", output.getvalue())

    def test_cli_custom_pattern(self):
        output = StringIO()

        with redirect_stdout(output):
            result = main([
                str(self.root),
                "--pattern",
                "WARNING",
            ])

        self.assertEqual(result, 0)
        self.assertIn("Total matches: 1", output.getvalue())

    def test_cli_regex(self):
        output = StringIO()

        with redirect_stdout(output):
            result = main([
                str(self.root),
                "--pattern",
                "ERROR|WARNING",
                "--regex",
            ])

        self.assertEqual(result, 0)
        self.assertIn("Total matches: 2", output.getvalue())

    
    def test_invalid_directory_returns_nonzero(self):
        output = StringIO()

        with redirect_stdout(output), redirect_stderr(output):
            result = main([
                str(self.root / "missing")
            ])

        self.assertEqual(result, 1)
        self.assertIn("not a valid directory", output.getvalue())


if __name__ == "__main__":
    unittest.main()

