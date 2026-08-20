from ast import pattern
import datetime
import os
import sys 


def scan_directory(path="."):
    results = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            full_path = os.path.join(root, filename)
            try:
                info = os.stat(full_path)
            except (PermissionError, FileNotFoundError) as e:
                print(f"  Skipping {full_path}: {e}")
                continue
            results.append({
                "path": full_path,
                "size": info.st_size,
                "modified": datetime.datetime.fromtimestamp(info.st_mtime).strftime("%Y-%m-%d %H:%M")
            })
    return results  

def parse_log_errors(filepath, pattern="ERROR"):
    matches = []
    if not os.path.exists(filepath):
        return matches
    with open(filepath, "r") as f:
        for line in f:
            if pattern in line:
                matches.append(line.strip())
    return matches

def summarize_errors(log_files, pattern="ERROR"):
    summary = {}
    for filepath in log_files:              
        summary[filepath] = len(parse_log_errors(filepath, pattern))
    return summary

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    pattern = sys.argv[2] if len(sys.argv) > 2 else "ERROR"

    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory")
        sys.exit(1)


    files = scan_directory(target_dir)
    print(f"Found {len(files)} files in {target_dir}:")
    for f in files:
        print(f"  {f['path']} — {f['size']} bytes — modified {f['modified']}")

    log_files = [f["path"] for f in files if f["path"].endswith(".log")]
    summary = summarize_errors(log_files, pattern)
    print(f"\n'{pattern}' summary:")
    for filepath, count in summary.items():
        print(f"  {filepath}: {count} '{pattern}' line(s)")