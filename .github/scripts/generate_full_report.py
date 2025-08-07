import argparse
import json
import os
import sys
from datetime import datetime
from bs4 import BeautifulSoup

def load_json(path):
    if not path or not os.path.isfile(path):
        print(f"⚠️ Warning: File not found or path not provided: {path}")
        return None
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading JSON from {path}: {e}")
            return None

def load_html(path):
    if not path or not os.path.isfile(path):
        print(f"⚠️ Warning: File not found or path not provided: {path}")
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_zap_critical_issues(html_content):
    if not html_content:
        return []
    soup = BeautifulSoup(html_content, 'html.parser')
    issues = []
    for alertitem in soup.select('alertitem'):
        riskcode = alertitem.find('riskcode')
        if riskcode and int(riskcode.text) >= 2:  # 2=Medium, 3=High risk
            alertname = alertitem.find('alert').text if alertitem.find('alert') else "Unknown"
            desc = alertitem.find('desc').text if alertitem.find('desc') else ""
            issues.append(f"{alertname}: {desc}")
    return issues

def summarize_semgrep(results):
    if not results or "results" not in results:
        return ["No issues found."]
    lines = []
    for issue in results["results"]:
        lines.append(
            f"- `{issue.get('path','unknown')}:{issue.get('start',{}).get('line','?')}` — "
            f"{issue.get('extra', {}).get('message', 'No message')} "
            f"(Severity: {issue.get('extra', {}).get('severity', 'N/A')})"
        )
    return lines

def summarize_bandit(data):
    if not data or "results" not in data:
        return ["No issues found."]
    lines = []
    for i in data["results"]:
        lines.append(
            f"- `{i.get('filename','unknown')}:{i.get('line_number','?')}` — "
            f"{i.get('issue_text','No description')} "
            f"(Severity: {i.get('issue_severity','N/A')}, Confidence: {i.get('issue_confidence','N/A')})"
        )
    return lines

def summarize_gitleaks(data):
    if not data or "findings" not in data:
        return ["No issues found."]
    return [f"- [SECRET] `{f.get('description','Secret')}` in `{f.get('file','unknown')}`" for f in data["findings"]]

def summarize_retire(data):
    if not data or "data" not in data:
        return ["No issues found."]
    lines = []
    for i in data["data"]:
        vuln = i.get('vulnerabilities', [{}])[0]
        summary = vuln.get('identifiers', {}).get('summary', 'vuln')
        lines.append(f"- `{i.get('component','unknown')}` ({summary}) in `{i.get('file','unknown')}`")
    return lines

def summarize_trivy(data):
    if not data or "Results" not in data:
        return ["No issues found."]
    lines = []
    for r in data["Results"]:
        for v in r.get("Vulnerabilities", []):
            lines.append(f"- [{v.get('Severity','N/A')}] `{v.get('VulnerabilityID','unknown')}` in `{r.get('Target','unknown')}`: {v.get('Title','No title')}")
    return lines or ["No issues found."]

def summarize_zap(path):
    if not path or not os.path.isfile(path):
        return ["No issues found."]
    # For simplicity, just link to the HTML report
    return [f"ZAP report available: `{path}`"]

def contains_critical(data, tool):
    if not data:
        return False
    if tool in ["semgrep_frontend", "semgrep_backend"]:
        for issue in data.get("results", []):
            if issue.get("extra", {}).get("severity", "").upper() in ["CRITICAL", "ERROR", "HIGH"]:
                return True
    elif tool == "bandit":
        for issue in data.get("results", []):
            if issue.get("issue_severity", "").upper() in ["HIGH", "CRITICAL"]:
                return True
    elif tool == "gitleaks":
        return bool(data.get("findings"))
    elif tool == "retire":
        return bool(data.get("data"))
    elif tool == "trivy":
        for r in data.get("Results", []):
            for v in r.get("Vulnerabilities", []):
                if v.get("Severity", "").upper() in ["CRITICAL", "HIGH"]:
                    return True
    elif tool == "zap":
        return os.path.isfile(data)
    return False

def main():
    parser = argparse.ArgumentParser(description="Generate combined security report from multiple tool JSON outputs.")
    parser.add_argument("--bandit", help="Path to bandit JSON report")
    parser.add_argument("--semgrep-frontend", help="Path to semgrep frontend JSON report")
    parser.add_argument("--semgrep-backend", help="Path to semgrep backend JSON report")
    parser.add_argument("--gitleaks", help="Path to gitleaks JSON report")
    parser.add_argument("--retire", help="Path to retire JSON report")
    parser.add_argument("--trivy", help="Path to trivy JSON report")
    parser.add_argument("--zap", help="Path to ZAP HTML report")
    parser.add_argument("--output", required=True, help="Output markdown report path")
    args = parser.parse_args()

    report_md = f"# 🔒 Security Scan Summary\n\nScan time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    critical_found = False

    tool_data = {}

    # Load all JSON inputs where provided
    tools = {
        "bandit": args.bandit,
        "semgrep_frontend": args.semgrep_frontend,
        "semgrep_backend": args.semgrep_backend,
        "gitleaks": args.gitleaks,
        "retire": args.retire,
        "trivy": args.trivy,
        "zap": args.zap,
    }

    for tool, path in tools.items():
        if tool == "zap":
            tool_data[tool] = path if path and os.path.isfile(path) else None
        else:
            tool_data[tool] = load_json(path)

    # Generate summaries per tool
    for tool, display_name in {
        "semgrep_frontend": "Semgrep Frontend",
        "semgrep_backend": "Semgrep Backend",
        "bandit": "Bandit Backend",
        "gitleaks": "Gitleaks",
        "retire": "Retire.js",
        "trivy": "Trivy",
        "zap": "OWASP ZAP",
    }.items():
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

        report_md += f"## {display_name}\n"
        report_md += "\n".join(lines) + "\n\n"

        if contains_critical(data, tool):
            critical_found = True

    # Write the combined markdown report
    output_path = args.output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_md)

    print(f"✅ Report written to {output_path}")

    if critical_found:
        print("❌ Critical or high severity issues found, failing CI.")
        sys.exit(1)
    else:
        print("✅ No critical or high severity issues found.")
        sys.exit(0)

if __name__ == "__main__":
    main()
