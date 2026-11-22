
import argparse
import re
import sys
from pathlib import Path
from datetime import datetime


def scan_directory(directory):
    """Recursively inventory files in a directory."""
    results = []

    for path in Path(directory).rglob("*"):
        if not path.is_file():
            continue

        try:
            info = path.stat()

        except (PermissionError, FileNotFoundError, OSError) as exc:
            print(f"Warning: Skipping {path}: {exc}", file=sys.stderr)
            continue

        results.append({
            "path": str(path),
            "size": info.st_size,
            "modified": datetime.fromtimestamp(
                info.st_mtime
            ).strftime("%Y-%m-%d %H:%M"),
        })

    return sorted(results, key=lambda item: item["path"].lower())


def parse_log_errors(filepath, pattern="ERROR", regex=False,
                     ignore_case=True):
    """Return lines that match the search pattern."""
    matches = []
    path = Path(filepath)

    if not path.is_file():
        return matches

    flags = re.IGNORECASE if ignore_case else 0

    try:
        with path.open("r", encoding="utf-8", errors="replace") as file:
            for line in file:
                if regex:
                    if re.search(pattern, line, flags):
                        matches.append(line.rstrip("\r\n"))
                else:
                    search_line = line.lower() if ignore_case else line
                    search_pattern = pattern.lower() if ignore_case else pattern

                    if search_pattern in search_line:
                        matches.append(line.rstrip("\r\n"))

    except (PermissionError, OSError) as exc:
        print(f"Warning: Cannot read {filepath}: {exc}", file=sys.stderr)

    return matches



def summarize_errors(log_files, pattern="ERROR", regex=False,
                     ignore_case=True):
    """Count matching lines per log file."""
    summary = {}

    for filepath in log_files:
        filepath = str(filepath)

        matches = parse_log_errors(
            filepath,
            pattern,
            regex=regex,
            ignore_case=ignore_case,
        )

        summary[filepath] = len(matches)

    return summary




def format_size(size):
    """Convert bytes to human-readable units."""
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size)

    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.2f} {unit}" if unit != "B" else f"{int(value)} B"

        value /= 1024

    return f"{value:.2f} TB"


def build_parser():
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Recursively scan files and summarize matching log lines."
    )

    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to scan (default: current directory)",
    )

    parser.add_argument(
        "-p",
        "--pattern",
        default="ERROR",
        help="Text or regex pattern to search (default: ERROR)",
    )

    parser.add_argument(
        "--regex",
        action="store_true",
        help="Treat pattern as a regular expression",
    )

    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Use case-sensitive matching",
    )

    return parser


def run_scan(directory, pattern="ERROR", regex=False,
              ignore_case=True):
    """Run inventory and log summary."""
    directory = Path(directory)

    if not directory.exists() or not directory.is_dir():
        print(f"Error: '{directory}' is not a valid directory.", file=sys.stderr)
        return 1

    files = scan_directory(directory)

    print(f"\nFile inventory: {directory}")
    print(f"Files found: {len(files)}\n")

    for file_info in files:
        print(
            f"{file_info['path']} | "
            f"{format_size(file_info['size'])} | "
            f"modified {file_info['modified']}"
        )

    log_files = [
        file_info["path"]
        for file_info in files
        if file_info["path"].lower().endswith(".log")
    ]

    summary = summarize_errors(
        log_files,
        pattern,
        regex=regex,
        ignore_case=ignore_case,
    )

    print(f"\nLog summary: '{pattern}'")
    print("-" * 40)

    for filepath, count in summary.items():
        print(f"{filepath}: {count} matching line(s)")

    total = sum(summary.values())
    print("-" * 40)
    print(f"Total matches: {total}")

    return 0


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    return run_scan(
        args.directory,
        pattern=args.pattern,
        regex=args.regex,
        ignore_case=not args.case_sensitive,
    )


if __name__ == "__main__":
    raise SystemExit(main())
