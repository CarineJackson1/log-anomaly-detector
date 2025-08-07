import json
import sys
from pathlib import Path
from datetime import datetime

def load_semgrep_json(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_markdown_report(results, output_path, title="Semgrep Report"):
    error_issues = [r for r in results if r.get("extra", {}).get("severity") == "ERROR"]
    count_errors = len(error_issues)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        f"# {title}",
        "",
        f"**Scan Time:** {timestamp}",
        f"**Error-level Issues Found:** {count_errors}",
        "",
        "---",
        ""
    ]

    if count_errors == 0:
        lines.append("✅ No ERROR-level issues found!")
    else:
        for i, result in enumerate(error_issues, 1):
            extra = result.get("extra", {})
            lines.extend([
                f"## {i}. {extra.get('message', 'No message')}",
                f"- **Rule:** `{result.get('check_id', 'N/A')}`",
                f"- **File:** `{result.get('path', 'N/A')}`",
                f"- **Line:** {result['start']['line']}",
                f"- **Severity:** {extra.get('severity', 'UNKNOWN')}",
                f"- **CWE:** {extra.get('metadata', {}).get('cwe', 'N/A')}",
                f"- **Category:** {extra.get('metadata', {}).get('category', 'N/A')}",
                "",
                "---",
                ""
            ])

    with open(output_path, 'w', encoding='utf-8') as md_file:
        md_file.write('\n'.join(lines))

    if count_errors > 0:
        print(f"❌ Found {count_errors} ERROR-level issues, failing CI.")
        sys.exit(1)
    else:
        print("✅ No ERROR-level issues found.")

def generate_report(raw_json_paths, output_md_path):
    combined_results = []
    for path in raw_json_paths:
        data = load_semgrep_json(path)
        combined_results.extend(data.get("results", []))

    write_markdown_report(combined_results, output_md_path, "Combined Semgrep Frontend Report")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_semgrep_report.py <output_md_path> <raw_json_path_1> [<raw_json_path_2> ...]")
        sys.exit(2)
    output_path = sys.argv[1]
    raw_paths = sys.argv[2:]
    generate_report(raw_paths, output_path)
