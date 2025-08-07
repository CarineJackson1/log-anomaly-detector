import argparse
import json
import os
import sys
from datetime import datetime
from bs4 import BeautifulSoup

REPORT_PATHS = {
    "bandit": "Bandit Backend",
    "semgrep_frontend": "Semgrep Frontend",
    "semgrep_backend": "Semgrep Backend",
    "gitleaks": "Gitleaks",
    "retire": "Retire.js",
    "trivy": "Trivy",
    "zap": "OWASP ZAP",
}

def load_json(path):
    if not path or not os.path.isfile(path):
        print(f"⚠️ Warning: File not found or not provided: {path}")
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error loading JSON from {path}: {e}")
        return None

def load_html(path):
    if not path or not os.path.isfile(path):
        print(f"⚠️ Warning: File not found or not provided: {path}")
        return ""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_zap_critical_issues(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    issues = []
    for alertitem in soup.select('alertitem'):
        riskcode = alertitem.find('riskcode')
        if riskcode and int(riskcode.text) >= 2:  # 2=Medium, 3=High severity
            alertname = alertitem.find('alert').text if alertitem.find('alert') else "Unknown"
            desc = alertitem.find('desc').text if alertitem.find('desc') else ""
            issues.append(f"{alertname}: {desc}")
    return issues

# Add your summarize functions here (summarize_semgrep, summarize_bandit, etc.)
# ...

def main():
    parser = argparse.ArgumentParser(description="Generate combined security report")
    parser.add_argument("--bandit", help="Path to bandit JSON report")
    parser.add_argument("--semgrep-frontend-react", help="Path to semgrep React frontend JSON report")
    parser.add_argument("--semgrep-frontend-ts", help="Path to semgrep TypeScript frontend JSON report")
    parser.add_argument("--semgrep-backend", help="Path to semgrep backend JSON report")
    parser.add_argument("--gitleaks", help="Path to gitleaks JSON report")
    parser.add_argument("--retire", help="Path to retire.js JSON report")
    parser.add_argument("--trivy", help="Path to trivy JSON report")
    parser.add_argument("--zap", help="Path to OWASP ZAP HTML report")
    parser.add_argument("--output", required=True, help="Output markdown report path")
    args = parser.parse_args()

    # Load frontend React and TS results, merge them
    semgrep_front_react = load_json(args.semgrep_frontend_react) or {"results": []}
    semgrep_front_ts = load_json(args.semgrep_frontend_ts) or {"results": []}
    combined_frontend = {"results": semgrep_front_react.get("results", []) + semgrep_front_ts.get("results", [])}

    tool_data = {
        "bandit": load_json(args.bandit),
        "semgrep_frontend": combined_frontend,
        "semgrep_backend": load_json(args.semgrep_backend),
        "gitleaks": load_json(args.gitleaks),
        "retire": load_json(args.retire),
        "trivy": load_json(args.trivy),
        "zap": args.zap  # HTML filepath
    }

    # Compose report
    report_lines = [f"# 🔒 Security Scan Summary\n\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"]
    critical_found = False

    # For each tool, call the corresponding summarize function and add to report
    for tool, display_name in REPORT_PATHS.items():
        data = tool_data.get(tool)
        if tool in ["semgrep_frontend", "semgrep_backend"]:
            lines = summarize_semgrep(data)
        elif tool == "bandit":
            lines = summarize_bandit(data)
        elif tool == "gitleaks":
            lines = summarize_gitleaks(data)
        elif tool == "retire":
            lines = summarize_retire(data)
        elif tool == "trivy":
            lines = summarize_trivy(data)
        elif tool == "zap":
            lines = summarize_zap(data)
        else:
            lines = ["No summary function defined."]

        report_lines.append(f"## {display_name}")
        report_lines.extend(lines)
        report_lines.append("")

        # Check if critical/high severity issues found
        if contains_critical(data, tool):
            critical_found = True

    # Write markdown output
    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"✅ Report written to {args.output}")

    if critical_found:
        print("❌ Critical or high severity issues found, failing CI.")
        sys.exit(1)
    else:
        print("✅ No critical or high severity issues found.")
        sys.exit(0)

if __name__ == "__main__":
    main()
