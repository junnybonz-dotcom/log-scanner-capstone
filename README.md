
# Log Scanner — Python CLI Tool

[![Log Scanner CI](https://github.com/junnybonz-dotcom/log-scanner-capstone/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/junnybonz-dotcom/log-scanner-capstone/actions/workflows/tests.yml)

A Python command-line tool that recursively inventories files and summarizes matching lines in `.log` files.

It supports text and regular-expression searches, configurable matching behavior, file metadata, and automated tests.

## Features

- Recursively scans directories using pathlib.
- Records file paths, sizes, and modification timestamps.
- Finds `.log` files.
- Searches for custom text patterns.
- Supports regular-expression searches.
- Uses case-insensitive matching by default.
- Supports case-sensitive searches.
- Displays human-readable file sizes.
- Reports per-file matches and total matches.
- Handles invalid directories and filesystem errors.

## Requirements

- Python 3.12 or newer
- No third-party packages required.

The application uses Python's standard library.

## Usage

Scan a directory:

```bash
python scanner.py logs
```

Search for a custom pattern:

```bash
python scanner.py logs --pattern WARNING
```

Search using regular expressions:

```bash
python scanner.py logs --pattern "ERROR|WARNING" --regex
```

Use case-sensitive matching:

```bash
python scanner.py logs --pattern ERROR --case-sensitive
```

Display available arguments:

```bash
python scanner.py --help
```

## How It Works

1. Validates the selected directory.
2. Recursively discovers files.
3. Records file metadata.
4. Identifies `.log` files.
5. Searches each log for the requested pattern.
6. Summarizes matches per file and across the directory.

## Automated Tests

Run the test suite:

```bash
python -m unittest discover -s tests -v
```

The suite contains 14 tests covering:

- Recursive file discovery
- File metadata
- Case-insensitive matching
- Case-sensitive matching
- Regular-expression searches
- Missing files
- Per-file match summaries
- Human-readable file sizes
- CLI arguments
- Invalid directory handling

Tests use temporary directories and sample log files. They do not modify the repository's original sample logs.

## Continuous Integration

GitHub Actions runs the test suite on:

- Python 3.12
- Python 3.13
- Python 3.14

The workflow also checks Python syntax.

## Project Structure

```text
log-scanner-capstone/
├── .github/
│   └── workflows/
│       └── tests.yml
├── logs/
│   ├── app.log
│   └── system.log
├── tests/
│   ├── test_scanner.py
│   └── test_cli.py
├── .gitignore
├── README.md
└── scanner.py
```

## Limitations

- Scans local directories rather than remote systems.
- Searches text-based `.log` files.
- Reports matching lines but does not diagnose or repair the underlying issue.
- Does not continuously monitor new log entries.

## What I Learned

This project helped me combine filesystem traversal, file metadata, text processing, regular expressions, command-line arguments, and exception handling into a reusable Python tool.

It also introduced automated testing and continuous integration, making the application easier to validate across multiple Python versions.
