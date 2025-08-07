import json
import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from bs4 import BeautifulSoup

RAW_DIR = "security-reports/raw"
OUTPUT_MD = "security-reports/summary_report.md"
OUTPUT_PDF = "security-reports/summary_report.pdf"

REPORT_PATHS = {
    "Semgrep Frontend": os.path.join(RAW_DIR, "semgrep-frontend.json"),
    "Semgrep Backend": os.path.join(RAW_DIR, "semgrep-backend.json"),
    "Bandit": os.path.join(RAW_DIR, "bandit-report.json"),
    "Gitleaks": os.path.join(RAW_DIR, "gitleaks-report.json"),
    "Retire.js": os.path.join(RAW_DIR, "retire-frontend.json"),
    "Trivy": os.path.join(RAW_DIR, "trivy-report.json"),
    "OWASP ZAP": os.path.join(RAW_DIR, "zap-report.html"),
}

def load_json(path):
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return None

def load_html(path):
    if not os.path.isfile(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_zap_critical_issues(html):
    soup = BeautifulSoup(html, "html.parser")
    issues = []
    for alertitem in soup.select("alertitem"):
        riskcode = alertitem.find("riskcode")
        if riskcode and int(riskcode.text) >= 2:  # Medium or High risk
            alert = alertitem.find("alert").text if alertitem.find("alert") else "Unknown"
            desc = alertitem.find("desc").text if alertitem.find("desc") else ""
            issues.append(f"{alert}: {desc}")
    return issues

def summarize_semgrep(data):
    if not data or "results" not in data:
        return ["No issues found."], False
    lines = []
    critical_found = False
    for issue in data["results"]:
        severity = issue.get("extra", {}).get("severity", "").upper()
        if severity in ["CRITICAL", "ERROR", "HIGH"]:
            critical_found = True
        path = issue.get("path", "unknown")
        line = issue.get("start", {}).get("line", "?")
        msg = issue.get("extra", {}).get("message", "No message")
        lines.append(f"- `{path}:{line}` — {msg} (Severity: {severity or 'N/A'})")
    if not lines:
        lines.append("No issues found.")
    return lines, critical_found

def summarize_bandit(data):
    if not data or "results" not in data:
        return ["No issues found."], False
    lines = []
    critical_found = False
    for issue in data["results"]:
        severity = issue.get("issue_severity", "").upper()
        if severity in ["HIGH", "CRITICAL"]:
            critical_found = True
        file = issue.get("filename", "unknown")
        line = issue.get("line_number", "?")
        desc = issue.get("issue_text", "No description")
        lines.append(f"- `{file}:{line}` — {desc} (Severity: {severity or 'N/A'})")
    if not lines:
        lines.append("No issues found.")
    return lines, critical_found

def summarize_gitleaks(data):
    if not data or "findings" not in data or not data["findings"]:
        return ["No issues found."], False
    lines = [f"- [SECRET] `{f.get('description', 'Secret')}` in `{f.get('file', 'unknown')}`" for f in data["findings"]]
    return lines, True  # Any secret leak is critical

def summarize_retire(data):
    if not data or "data" not in data:
        return ["No issues found."], False
    critical_found = False
    lines = []
    for component in data["data"]:
        vulns = component.get("vulnerabilities", [])
        for vuln in vulns:
            severity = vuln.get("severity", "").upper()
            if severity == "HIGH" or severity == "CRITICAL":
                critical_found = True
            summary = vuln.get("identifiers", {}).get("summary", "Vulnerability")
            file = component.get("file", "unknown")
            lines.append(f"- `{component.get('component', 'unknown')}` ({summary}) in `{file}` (Severity: {severity or 'N/A'})")
    if not lines:
        lines.append("No issues found.")
    return lines, critical_found

def summarize_trivy(data):
    if not data or "Results" not in data:
        return ["No issues found."], False
    lines = []
    critical_found = False
    for result in data["Results"]:
        for vuln in result.get("Vulnerabilities", []):
            severity = vuln.get("Severity", "").upper()
            if severity in ["CRITICAL", "HIGH"]:
                critical_found = True
            pkg = vuln.get("PkgName", "unknown")
            title = vuln.get("Title", "No title")
            target = result.get("Target", "unknown")
            lines.append(f"- [{severity}] `{vuln.get('VulnerabilityID','unknown')}` in `{target}`: {title}")
    if not lines:
        lines.append("No issues found.")
    return lines, critical_found

def summarize_zap(path):
    if not os.path.isfile(path):
        return ["No issues found."], False
    html = load_html(path)
    issues = extract_zap_critical_issues(html)
    if issues:
        return [f"- {i}" for i in issues], True
    return ["No critical alerts found."], False

def generate_report():
    os.makedirs("security-reports", exist_ok=True)
    report_md = f"# 🔒 Security Scan Summary\n\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    styles = getSampleStyleSheet()
    story = [Paragraph("🔒 Security Scan Summary", styles["Title"]), Spacer(1, 12)]

    critical_found = False

    for tool, path in REPORT_PATHS.items():
        if tool == "OWASP ZAP":
            lines, has_critical = summarize_zap(path)
        else:
            data = load_json(path)
            if tool == "Semgrep Frontend" or tool == "Semgrep Backend":
                lines, has_critical = summarize_semgrep(data)
            elif tool == "Bandit":
                lines, has_critical = summarize_bandit(data)
            elif tool == "Gitleaks":
                lines, has_critical = summarize_gitleaks(data)
            elif tool == "Retire.js":
                lines, has_critical = summarize_retire(data)
            elif tool == "Trivy":
                lines, has_critical = summarize_trivy(data)
            else:
                lines, has_critical = ["No summary function defined."], False

        report_md += f"## {tool}\n" + "\n".join(lines) + "\n\n"

        story.append(Paragraph(tool, styles["Heading2"]))
        for line in lines:
            story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 12))

        if has_critical:
            critical_found = True

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(report_md)

    doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=letter)
    doc.build(story)

    print(f"✅ Reports generated: {OUTPUT_MD}, {OUTPUT_PDF}")

    if critical_found:
        print("❌ Critical or high severity issues found, failing CI.")
        sys.exit(1)
    else:
        print("✅ No critical or high severity issues found.")
        sys.exit(0)

if __name__ == "__main__":
    generate_report()
