import json
from pathlib import Path
from datetime import datetime

def load_semgrep_json(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_markdown_report(results, output_path, title="Semgrep Report"):
    count = len(results)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# {title}",
        "",
        f"**Scan Time:** {timestamp}",
        f"**Issues Found:** {count}",
        "",
        "---",
        ""
    ]

    if not results:
        lines.append("✅ No issues found!")
    else:
        for i, result in enumerate(results, 1):
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

def generate_report(raw_json_path):
    folder = Path(raw_json_path).parent
    markdown_path = folder / "report.md"
    data = load_semgrep_json(raw_json_path)
    results = data.get("results", [])
    title = f"Semgrep Report – {folder.name.capitalize()}"
    write_markdown_report(results, markdown_path, title)
    print(f"✅ Generated: {markdown_path}")

# Example usage:
# generate_report("security-reports/semgrep/backend/raw.json")
