import json
import os

# Config: paths to raw scan JSON reports
REPORT_PATHS = {
    "Semgrep Frontend": "security-reports/raw/semgrep-frontend.json",
    "Semgrep Backend": "security-reports/raw/semgrep-backend.json",
    "Bandit Backend": "security-reports/raw/bandit-backend.json",
    "Gitleaks": "security-reports/raw/gitleaks-report.json",
    "Retire.js": "security-reports/raw/retire-frontend.json",
    "Trivy": "security-reports/raw/trivy-report.json",
}

OUTPUT_PATH = "security-reports/summary_report.md"


def load_json(path):
    if not os.path.isfile(path):
        return None
    with open(path, "r") as f:
        return json.load(f)


def summarize_semgrep(data):
    if not data or "results" not in data:
        return "No issues found."
    lines = []
    for issue in data["results"]:
        path = issue.get("path", "unknown file")
        line = issue.get("start", {}).get("line", "?")
        message = issue.get("extra", {}).get("message", issue.get("message", "No message"))
        severity = issue.get("extra", {}).get("severity", "N/A")
        lines.append(f"- `{path}:{line}` — {message} (Severity: {severity})")
    return "\n".join(lines) if lines else "No issues found."


def summarize_bandit(data):
    if not data or "results" not in data:
        return "No issues found."
    lines = []
    for issue in data["results"]:
        filename = issue.get("filename", "unknown file")
        line = issue.get("line_number", "?")
        text = issue.get("issue_text", "No description")
        severity = issue.get("issue_severity", "N/A")
        confidence = issue.get("issue_confidence", "N/A")
        lines.append(f"- `{filename}:{line}` — {text} (Severity: {severity}, Confidence: {confidence})")
    return "\n".join(lines) if lines else "No issues found."


def summarize_gitleaks(data):
    if not data or "findings" not in data:
        return "No issues found."
    lines = []
    for finding in data["findings"]:
        desc = finding.get("description", "Secret found")
        file = finding.get("file", "unknown file")
        lines.append(f"- [SECRET] `{desc}` in `{file}`")
    return "\n".join(lines) if lines else "No issues found."


def summarize_retire(data):
    if not data or "data" not in data:
        return "No issues found."
    lines = []
    for item in data["data"]:
        component = item.get("component", "unknown component")
        file = item.get("file", "unknown file")
        vuln = item.get("vulnerabilities", [{}])[0].get("identifiers", {}).get("summary", "vulnerability")
        lines.append(f"- `{component}` ({vuln}) in `{file}`")
    return "\n".join(lines) if lines else "No issues found."


def summarize_trivy(data):
    if not data or "Results" not in data:
        return "No issues found."
    lines = []
    for result in data["Results"]:
        vulns = result.get("Vulnerabilities", [])
        for vuln in vulns:
            severity = vuln.get("Severity", "N/A")
            vuln_id = vuln.get("VulnerabilityID", "unknown")
            target = result.get("Target", "unknown target")
            title = vuln.get("Title", "No title")
            lines.append(f"- [{severity}] `{vuln_id}` in `{target}`: {title}")
    return "\n".join(lines) if lines else "No issues found."


def generate_report():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    report = "# 🔒 Security Scan Summary\n\n"

    for title, path in REPORT_PATHS.items():
        data = load_json(path)
        if "Semgrep" in title:
            summary = summarize_semgrep(data)
        elif "Bandit" in title:
            summary = summarize_bandit(data)
        elif "Gitleaks" in title:
            summary = summarize_gitleaks(data)
        elif "Retire" in title:
            summary = summarize_retire(data)
        elif "Trivy" in title:
            summary = summarize_trivy(data)
        else:
            summary = "No summary function defined."

        report += f"## {title}\n{summary}\n\n"

    with open(OUTPUT_PATH, "w") as f:
        f.write(report)
    print(f"Summary report generated at {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_report()
