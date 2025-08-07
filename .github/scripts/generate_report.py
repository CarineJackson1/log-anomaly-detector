import json
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

REPORT_PATHS = {
    "Semgrep Frontend": "security-reports/raw/semgrep-frontend.json",
    "Semgrep Backend": "security-reports/raw/semgrep-backend.json",
    "Bandit Backend": "security-reports/raw/bandit-report.json",
    "Gitleaks": "security-reports/raw/gitleaks-report.json",
    "Retire.js": "security-reports/raw/retire-frontend.json",
    "Trivy": "security-reports/raw/trivy-report.json",
}

OUTPUT_MD = "security-reports/summary_report.md"
OUTPUT_PDF = "security-reports/summary_report.pdf"

def load_json(path):
    if not os.path.isfile(path):
        return None
    with open(path, "r") as f:
        return json.load(f)

def summarize_semgrep(data):
    if not data or "results" not in data:
        return ["No issues found."]
    return [
        f"- `{issue.get('path', 'unknown')}:{issue.get('start', {}).get('line', '?')}` — {issue.get('extra', {}).get('message', 'No message')} (Severity: {issue.get('extra', {}).get('severity', 'N/A')})"
        for issue in data["results"]
    ]

def summarize_bandit(data):
    if not data or "results" not in data:
        return ["No issues found."]
    return [
        f"- `{i.get('filename', 'unknown')}:{i.get('line_number', '?')}` — {i.get('issue_text', 'No description')} (Severity: {i.get('issue_severity', 'N/A')}, Confidence: {i.get('issue_confidence', 'N/A')})"
        for i in data["results"]
    ]

def summarize_gitleaks(data):
    if not data or "findings" not in data:
        return ["No issues found."]
    return [f"- [SECRET] `{f.get('description', 'Secret')}` in `{f.get('file', 'unknown')}`" for f in data["findings"]]

def summarize_retire(data):
    if not data or "data" not in data:
        return ["No issues found."]
    return [
        f"- `{i.get('component', 'unknown')}` ({i.get('vulnerabilities', [{}])[0].get('identifiers', {}).get('summary', 'vuln')}) in `{i.get('file', 'unknown')}`"
        for i in data["data"]
    ]

def summarize_trivy(data):
    if not data or "Results" not in data:
        return ["No issues found."]
    lines = []
    for r in data["Results"]:
        for v in r.get("Vulnerabilities", []):
            lines.append(f"- [{v.get('Severity', 'N/A')}] `{v.get('VulnerabilityID', 'unknown')}` in `{r.get('Target', 'unknown')}`: {v.get('Title', 'No title')}")
    return lines or ["No issues found."]

def generate_report():
    os.makedirs("security-reports", exist_ok=True)
    report_md = "# 🔒 Security Scan Summary\n\n"
    styles = getSampleStyleSheet()
    story = [Paragraph("🔒 Security Scan Summary", styles["Title"]), Spacer(1, 12)]

    critical_found = False

    for title, path in REPORT_PATHS.items():
        data = load_json(path)
        if "Semgrep" in title:
            lines = summarize_semgrep(data)
            # Check for critical Semgrep issues
            if data and "results" in data:
                for issue in data["results"]:
                    severity = issue.get("extra", {}).get("severity", "").upper()
                    if severity == "CRITICAL":
                        critical_found = True
        elif "Bandit" in title:
            lines = summarize_bandit(data)
            # Check Bandit critical severity (example)
            if data and "results" in data:
                for issue in data["results"]:
                    if issue.get("issue_severity", "").upper() == "HIGH":  # or CRITICAL if Bandit supports
                        critical_found = True
        elif "Gitleaks" in title:
            lines = summarize_gitleaks(data)
            if data and "findings" in data and len(data["findings"]) > 0:
                critical_found = True  # any secret is critical
        elif "Retire" in title:
            lines = summarize_retire(data)
        elif "Trivy" in title:
            lines = summarize_trivy(data)
            if data and "Results" in data:
                for r in data["Results"]:
                    for v in r.get("Vulnerabilities", []):
                        if v.get("Severity", "").upper() in ["CRITICAL", "HIGH"]:
                            critical_found = True
        else:
            lines = ["No summary function defined."]

        section = f"## {title}\n" + "\n".join(lines) + "\n\n"
        report_md += section
        story.append(Paragraph(title, styles["Heading2"]))
        for line in lines:
            story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 12))

    with open(OUTPUT_MD, "w") as f:
        f.write(report_md)

    doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=letter)
    doc.build(story)
    print(f"✅ Reports generated: {OUTPUT_MD}, {OUTPUT_PDF}")

    if critical_found:
        print("❌ Critical issues found! Failing build.")
        sys.exit(1)
    else:
        print("✅ No critical issues found.")
        sys.exit(0)

if __name__ == "__main__":
    generate_report()
