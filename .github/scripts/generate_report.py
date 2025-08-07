import json
import os
import sys
from collections import defaultdict
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Customize what counts as a critical issue
CRITICAL_LEVELS = {"CRITICAL", "HIGH"}

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

def summarize_issues(issues, get_severity, formatter):
    if not issues:
        return ["No issues found."], 0, defaultdict(int)

    # Count and sort
    counts = defaultdict(int)
    for issue in issues:
        level = get_severity(issue).upper()
        counts[level] += 1
    issues.sort(key=lambda i: get_severity(i).upper(), reverse=True)

    lines = [formatter(issue) for issue in issues]
    critical_count = sum(counts[sev] for sev in CRITICAL_LEVELS)
    return lines or ["No issues found."], critical_count, counts

def summarize_semgrep(data):
    if not data or "results" not in data:
        return ["No issues found."], 0, defaultdict(int)
    return summarize_issues(
        data["results"],
        lambda i: i.get("extra", {}).get("severity", ""),
        lambda i: f"- `{i.get('path', 'unknown')}:{i.get('start', {}).get('line', '?')}` — {i.get('extra', {}).get('message', 'No message')} (Severity: {i.get('extra', {}).get('severity', 'N/A')})"
    )

def summarize_bandit(data):
    if not data or "results" not in data:
        return ["No issues found."], 0, defaultdict(int)
    return summarize_issues(
        data["results"],
        lambda i: i.get("issue_severity", ""),
        lambda i: f"- `{i.get('filename', 'unknown')}:{i.get('line_number', '?')}` — {i.get('issue_text', 'No description')} (Severity: {i.get('issue_severity', 'N/A')}, Confidence: {i.get('issue_confidence', 'N/A')})"
    )

def summarize_gitleaks(data):
    if not data or "findings" not in data:
        return ["No issues found."], 0, defaultdict(int)
    issues = data["findings"]
    return summarize_issues(
        issues,
        lambda _: "CRITICAL",  # All secrets are critical
        lambda i: f"- [SECRET] `{i.get('description', 'Secret')}` in `{i.get('file', 'unknown')}`"
    )

def summarize_retire(data):
    if not data or "data" not in data:
        return ["No issues found."], 0, defaultdict(int)
    return summarize_issues(
        data["data"],
        lambda _: "MEDIUM",  # Retire.js doesn't classify well
        lambda i: f"- `{i.get('component', 'unknown')}` ({i.get('vulnerabilities', [{}])[0].get('identifiers', {}).get('summary', 'vuln')}) in `{i.get('file', 'unknown')}`"
    )

def summarize_trivy(data):
    if not data or "Results" not in data:
        return ["No issues found."], 0, defaultdict(int)
    issues = []
    for r in data["Results"]:
        for v in r.get("Vulnerabilities", []):
            issues.append({
                "target": r.get("Target", "unknown"),
                "severity": v.get("Severity", ""),
                "vuln_id": v.get("VulnerabilityID", ""),
                "title": v.get("Title", "")
            })
    return summarize_issues(
        issues,
        lambda i: i["severity"],
        lambda i: f"- [{i['severity']}] `{i['vuln_id']}` in `{i['target']}`: {i['title']}"
    )

def generate_report():
    os.makedirs("security-reports", exist_ok=True)
    report_md = "# 🔒 Security Scan Summary\n\n"
    styles = getSampleStyleSheet()
    story = [Paragraph("🔒 Security Scan Summary", styles["Title"]), Spacer(1, 12)]

    critical_found = False

    for title, path in REPORT_PATHS.items():
        data = load_json(path)
        if "Semgrep" in title:
            lines, crit_count, counts = summarize_semgrep(data)
        elif "Bandit" in title:
            lines, crit_count, counts = summarize_bandit(data)
        elif "Gitleaks" in title:
            lines, crit_count, counts = summarize_gitleaks(data)
        elif "Retire" in title:
            lines, crit_count, counts = summarize_retire(data)
        elif "Trivy" in title:
            lines, crit_count, counts = summarize_trivy(data)
        else:
            lines, crit_count, counts = ["No summary function defined."], 0, defaultdict(int)

        if crit_count > 0:
            critical_found = True

        section_header = f"## {title}\n"
        section_header += f"**Total Issues:** {sum(counts.values())} | "
        section_header += " | ".join([f"{k}: {v}" for k, v in counts.items()]) + "\n\n"

        report_md += section_header + "\n".join(lines) + "\n\n"

        story.append(Paragraph(title, styles["Heading2"]))
        story.append(Paragraph(section_header.strip(), styles["Normal"]))
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
