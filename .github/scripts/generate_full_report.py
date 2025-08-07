import json
import sys
import argparse
from pathlib import Path

def load_json(path):
    if not Path(path).is_file():
        print(f"Warning: File not found: {path}")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def summarize_semgrep(data):
    if not data or "results" not in data:
        return ["No issues found."], False
    lines = []
    critical_found = False
    for issue in data["results"]:
        sev = issue.get("extra", {}).get("severity", "N/A").upper()
        if sev == "CRITICAL":
            critical_found = True
        lines.append(
            f"- `{issue.get('path', 'unknown')}:{issue.get('start', {}).get('line', '?')}` — "
            f"{issue.get('extra', {}).get('message', 'No message')} (Severity: {sev})"
        )
    return lines, critical_found

def summarize_bandit(data):
    if not data or "results" not in data:
        return ["No issues found."], False
    lines = []
    critical_found = False
    for issue in data["results"]:
        sev = issue.get("issue_severity", "").upper()
        if sev in ["HIGH", "CRITICAL"]:
            critical_found = True
        lines.append(
            f"- `{issue.get('filename', 'unknown')}:{issue.get('line_number', '?')}` — "
            f"{issue.get('issue_text', 'No description')} (Severity: {sev}, Confidence: {issue.get('issue_confidence', 'N/A')})"
        )
    return lines, critical_found

def summarize_gitleaks(data):
    if not data or "findings" not in data:
        return ["No issues found."], False
    lines = [f"- [SECRET] `{f.get('description', 'Secret')}` in `{f.get('file', 'unknown')}`" for f in data["findings"]]
    return lines, bool(lines)

def summarize_retire(data):
    if not data or "data" not in data:
        return ["No issues found."], False
    lines = []
    for i in data["data"]:
        vuln_summary = i.get("vulnerabilities", [{}])[0].get("identifiers", {}).get("summary", "vuln")
        lines.append(f"- `{i.get('component', 'unknown')}` ({vuln_summary}) in `{i.get('file', 'unknown')}`")
    return lines, False  # Adjust if you want critical detection here

def summarize_trivy(data):
    if not data or "Results" not in data:
        return ["No issues found."], False
    lines = []
    critical_found = False
    for r in data["Results"]:
        for v in r.get("Vulnerabilities", []):
            sev = v.get("Severity", "").upper()
            if sev in ["CRITICAL", "HIGH"]:
                critical_found = True
            lines.append(
                f"- [{sev}] `{v.get('VulnerabilityID', 'unknown')}` in `{r.get('Target', 'unknown')}`: {v.get('Title', 'No title')}"
            )
    return lines, critical_found

def summarize_zap(path):
    # Simple placeholder: Just include a link to the HTML report in the markdown
    if Path(path).is_file():
        return [f"- See [ZAP Report]({path}) (HTML report)"], False
    else:
        return ["No ZAP report found."], False

def main():
    parser = argparse.ArgumentParser(description="Generate combined security report")
    parser.add_argument("--bandit", type=str, help="Bandit JSON report path")
    parser.add_argument("--semgrep-frontend", type=str, help="Semgrep frontend JSON report path")
    parser.add_argument("--semgrep-backend", type=str, help="Semgrep backend JSON report path")
    parser.add_argument("--retire", type=str, help="Retire.js JSON report path")
    parser.add_argument("--gitleaks", type=str, help="Gitleaks JSON report path")
    parser.add_argument("--trivy", type=str, help="Trivy JSON report path")
    parser.add_argument("--zap", type=str, help="OWASP ZAP HTML report path")
    parser.add_argument("--output", required=True, type=str, help="Output markdown report path")

    args = parser.parse_args()

    report_md = "# 🔒 Security Scan Summary\n\n"
    critical_found = False

    tools = [
        ("Bandit Backend", args.bandit, summarize_bandit),
        ("Semgrep Frontend", args.semgrep_frontend, summarize_semgrep),
        ("Semgrep Backend", args.semgrep_backend, summarize_semgrep),
        ("Retire.js", args.retire, summarize_retire),
        ("Gitleaks", args.gitleaks, summarize_gitleaks),
        ("Trivy", args.trivy, summarize_trivy),
        ("OWASP ZAP", args.zap, summarize_zap),
    ]

    for title, path, summarizer in tools:
        if path:
            if "zap" == title.lower().replace(" ", ""):
                lines, found = summarizer(path)
            else:
                data = load_json(path)
                lines, found = summarizer(data)
            critical_found = critical_found or found
        else:
            lines, found = (["No report provided."], False)
        report_md += f"## {title}\n" + "\n".join(lines) + "\n\n"

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report_md)

    print(f"✅ Combined security report written to {args.output}")

    if critical_found:
        print("❌ Critical issues found! Failing job.")
        sys.exit(1)
    else:
        print("✅ No critical issues found.")
        sys.exit(0)

if __name__ == "__main__":
    main()
