import json
import os

# Paths to your raw JSON reports
REPORT_PATHS = {
    "Semgrep Frontend": "security-reports/raw/semgrep-frontend.json",
    "Semgrep Backend": "security-reports/raw/semgrep-backend.json",
    "Bandit Backend": "security-reports/raw/bandit-backend.json",
    "Retire.js Frontend": "security-reports/raw/retire-frontend.json"
}

SUMMARY_MD_PATH = "security-reports/summary_report.md"
BADGE_JSON_PATH = "security-reports/security_badge.json"

def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)

def summarize_semgrep(data, title):
    if not data or "results" not in data:
        return f"### {title}\nNo data available.\n\n", 0
    issues = data["results"]
    summary = f"### {title}\nFound {len(issues)} issue(s):\n"
    high_severity_count = 0
    for i, issue in enumerate(issues, 1):
        path = issue.get("path", "unknown file")
        start_line = issue.get("start", {}).get("line", "?")
        message = issue.get("extra", {}).get("message", issue.get("message", "No message"))
        severity = issue.get("extra", {}).get("severity", "N/A")
        if severity.upper() == "HIGH":
            high_severity_count += 1
        summary += f"{i}. `{path}:{start_line}` - {message} (Severity: {severity})\n"
    summary += "\n"
    return summary, high_severity_count

def summarize_bandit(data, title):
    if not data or "results" not in data:
        return f"### {title}\nNo data available.\n\n", 0
    issues = data["results"]
    summary = f"### {title}\nFound {len(issues)} issue(s):\n"
    high_severity_count = 0
    for i, issue in enumerate(issues, 1):
        filename = issue.get("filename", "unknown file")
        line = issue.get("line_number", "?")
        issue_text = issue.get("issue_text", "No description")
        severity = issue.get("issue_severity", "N/A")
        confidence = issue.get("issue_confidence", "N/A")
        if severity.upper() == "HIGH":
            high_severity_count += 1
        summary += f"{i}. `{filename}:{line}` - {issue_text} (Severity: {severity}, Confidence: {confidence})\n"
    summary += "\n"
    return summary, high_severity_count

def summarize_retire(data, title):
    if not data or "data" not in data:
        return f"### {title}\nNo data available.\n\n", 0
    vulns = data["data"]
    summary = f"### {title}\nFound {len(vulns)} vulnerability(ies):\n"
    high_severity_count = 0
    for i, vuln in enumerate(vulns, 1):
        component = vuln.get("component", "unknown")
        summary_vuln = vuln.get("vulnerabilities", [{}])[0].get("identifiers", {}).get("summary", "N/A")
        severity = vuln.get("vulnerabilities", [{}])[0].get("severity", "N/A")
        if severity.upper() == "HIGH":
            high_severity_count += 1
        summary += f"{i}. {component} - {summary_vuln} (Severity: {severity})\n"
    summary += "\n"
    return summary, high_severity_count

def main():
    os.makedirs("security-reports", exist_ok=True)

    total_high_severity = 0
    md_report = "# 🔒 Security Scan Summary\n\n"

    # Load and summarize Semgrep frontend
    semgrep_fe = load_json(REPORT_PATHS["Semgrep Frontend"])
    summary, high = summarize_semgrep(semgrep_fe, "Semgrep Frontend Scan")
    md_report += summary
    total_high_severity += high

    # Load and summarize Semgrep backend
    semgrep_be = load_json(REPORT_PATHS["Semgrep Backend"])
    summary, high = summarize_semgrep(semgrep_be, "Semgrep Backend Scan")
    md_report += summary
    total_high_severity += high

    # Load and summarize Bandit backend
    bandit_be = load_json(REPORT_PATHS["Bandit Backend"])
    summary, high = summarize_bandit(bandit_be, "Bandit Backend Scan")
    md_report += summary
    total_high_severity += high

    # Load and summarize Retire.js frontend
    retire_fe = load_json(REPORT_PATHS["Retire.js Frontend"])
    summary, high = summarize_retire(retire_fe, "Retire.js Frontend Scan")
    md_report += summary
    total_high_severity += high

    # Write Markdown summary report
    with open(SUMMARY_MD_PATH, "w") as f:
        f.write(md_report)
    print(f"Summary report generated at {SUMMARY_MD_PATH}")

    # Generate Shields.io badge JSON
    badge = {
        "schemaVersion": 1,
        "label": "security",
        "message": f"{total_high_severity} High Issues",
        "color": "red" if total_high_severity > 0 else "brightgreen"
    }
    with open(BADGE_JSON_PATH, "w") as f:
        json.dump(badge, f)
    print(f"Badge JSON generated at {BADGE_JSON_PATH}")

if __name__ == "__main__":
    main()
