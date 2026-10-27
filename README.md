# Log Scanner — Python and Bash

A beginner-friendly Python command-line tool that recursively inventories files and summarizes matching error lines in `.log` files. It reports file paths, sizes, modification timestamps, and the number of lines matching a chosen text pattern.

## Skills Demonstrated

- Python functions, loops, dictionaries, and lists
- Filesystem traversal with `os.walk()`
- File metadata with `os.stat()`
- Log parsing and text matching
- Command-line arguments with `sys.argv`
- Basic error handling and exit codes
- Bash scripting and Linux command-line workflows

## How It Works

1. Recursively scans the selected directory and records each file's path, size, and modification time.
2. Identifies files ending in `.log`.
3. Searches each log for a selected text pattern.
4. Prints a summary of the matching lines per log file.

The default search pattern is `ERROR`.

## Requirements

- Python 3
- No third-party Python packages are required; the script uses Python's standard library.

## How to Run

From the project directory, run:

```bash
python scanner.py
```

Scan a particular directory:

```bash
python scanner.py logs
```

Search for a different pattern:

```bash
python scanner.py logs WARNING
```

The command-line arguments are:

```text
python scanner.py [directory] [pattern]
```

The directory defaults to the current directory, and the pattern defaults to `ERROR`.

## Example Output

Captured from a real run of `python scanner.py logs ERROR` on Windows:

```text
Found 2 files in logs:
  logs\app.log — 200 bytes — modified 2026-08-16 21:55
  logs\system.log — 83 bytes — modified 2026-08-16 22:01

'ERROR' summary:
  logs\app.log: 2 'ERROR' line(s)
  logs\system.log: 1 'ERROR' line(s)
```

This run found three matching lines across the two log files.

## Error Handling

- Checks whether the target directory exists before scanning.
- Exits with status code `1` if the target directory is invalid.
- Skips files that raise `PermissionError` or `FileNotFoundError` during metadata inspection.
- Returns an empty list of matches when a requested log file does not exist.

## Current Limitations

- Pattern matching is case-sensitive and uses substring matching, not regular expressions.
- Only files ending in `.log` are included in the error summary.
- The tool counts matching lines; it does not classify error severity or automatically repair problems.

## Project Structure

```text
log_scanner-08-16-2026/
├── scanner.py
├── script.sh
├── logs/
├── journal/
├── .gitignore
└── README.md
```

This describes the project structure observed during development; check the actual folder contents if the files change.

## What I Learned

This project helped me practice combining filesystem operations, file metadata, text parsing, command-line arguments, and basic exception handling into a single tool. It also demonstrates how simple log summaries can help identify problems without manually reading every log file.
