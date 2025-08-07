import json
import os

# Paths to the raw JSON reports
SEMgrep_FRONTEND_PATH = "security-reports/raw/semgrep-frontend.json"
SEMgrep_BACKEND_PATH = "security-reports/raw/semgrep-backend.json"
BANDIT_BACKEND_PATH = "security-reports/raw/bandit-backend.json"

OUTPUT_PATH = "security-reports/summary_report.md"

def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)

def summarize_semgrep(data, title):
    if not data or "results" not in data:
        return f"### {title}\nNo data available.\n\n"
    issues = data["results"]
    summary = f"### {title}\nFound {len(issues)} issue(s):\n"
    for i, issue in enumerate(issues, 1):
        path = issue.get("path", "unknown file")
        start_line = issue.get("start", {}).get("line", "?")
        message = issue.get("extra", {}).get("message", issue.get("message", "No message"))
        severity = issue.get("extra", {}).get("severity", "N/A")
        summary += f"{i}. `{path}:{start_line}` - {message} (Severity: {severity})\n"
    summary += "\n"
    return summary

def summarize_bandit(data, title):
    if not data or "results" not in data:
        return f"### {title}\nNo data available.\n\n"
    issues = data["results"]
    summary = f"### {title}\nFound {len(issues)} issue(s):\n"
    for i, issue in enumerate(issues, 1):
        filename = issue.get("filename", "unknown file")
        line = issue.get("line_number", "?")
        issue_text = issue.get("issue_text", "No description")
        severity = issue.get("issue_severity", "N/A")
        confidence = issue.get("issue_confidence", "N/A")
        summary += f"{i}. `{filename}:{line}` - {issue_text} (Severity: {severity}, Confidence: {confidence})\n"
    summary += "\n"
    return summary

def main():
    os.makedirs("security-reports", exist_ok=True)

    semgrep_frontend = load_json(SEMgrep_FRONTEND_PATH)
    semgrep_backend = load_json(SEMgrep_BACKEND_PATH)
    bandit_backend = load_json(BANDIT_BACKEND_PATH)

    report = "# 🔒 Security Scan Summary\n\n"

    report += summarize_semgrep(semgrep_frontend, "Semgrep Frontend Scan")
    report += summarize_semgrep(semgrep_backend, "Semgrep Backend Scan")
    report += summarize_bandit(bandit_backend, "Bandit Backend Scan")

    with open(OUTPUT_PATH, "w") as f:
        f.write(report)

    print(f"Summary report generated at {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
