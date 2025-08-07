import json
import os

REPORT_PATHS = {
    "Semgrep Frontend": "semgrep-frontend.json",
    "Semgrep Backend": "semgrep-backend.json",
    "Bandit Backend": "bandit-report.json",
    "Retire.js": "retire-frontend.json",
    "Gitleaks": "gitleaks-report.json",
    "Trivy": "trivy-report.json",
    # OWASP ZAP report is HTML and can be viewed separately as artifact
}

OUTPUT_PATH = "security-reports/summary_report.md"

def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)

def summarize_semgrep(data):
    if not data or "results" not in data:
        return "No data available."
    return "\n".join(
        f"- [{r['extra'].get('severity', 'N/A').upper()}] `{r['check_id']}` in `{r['path']}`: {r['extra'].get('message', '')}"
        for r in data["results"]
    )

def summarize_bandit(data):
    if not data or "results" not in data:
        return "No data available."
    return "\n".join(
        f"- [{r['issue_severity'].upper()}] `{r.get('test_id', 'bandit')}` in `{r['filename']}`: {r['issue_text']}"
        for r in data["results"]
    )

def summarize_retire(data):
    if not data or "data" not in data:
        return "No data available."
    return "\n".join(
        f"- [HIGH] `{r['component']}` ({r.get('vulnerabilities', [{}])[0].get('identifiers', {}).get('summary', 'vuln')}) in `{r['file']}`"
        for r in data["data"]
    )

def summarize_gitleaks(data):
    if not data or "findings" not in data:
        return "No data available."
    return "\n".join(
        f"- [SECRET] `{f['description']}` in `{f['file']}`"
        for f in data["findings"]
    )

def summarize_trivy(data):
    if not data or "Results" not in data:
        return "No data available."
    vulns = []
    for res in data["Results"]:
        if "Vulnerabilities" in res:
            for v in res["Vulnerabilities"]:
                vulns.append(f"- [{v['Severity'].upper()}] `{v['VulnerabilityID']}` in `{res['Target']}`: {v['Title']}")
    return "\n".join(vulns) if vulns else "No vulnerabilities found."

def main():
    os.makedirs("security-reports", exist_ok=True)
    report = "# 🔒 Security Scan Summary\n\n"

    for name, path in REPORT_PATHS.items():
        data = load_json(path)
        if name.startswith("Semgrep"):
            summary = summarize_semgrep(data)
        elif name == "Bandit Backend":
            summary = summarize_bandit(data)
        elif name == "Retire.js":
            summary = summarize_retire(data)
        elif name == "Gitleaks":
            summary = summarize_gitleaks(data)
        elif name == "Trivy":
            summary = summarize_trivy(data)
        else:
            summary = "No summary function available."
        
        report += f"### {name}\n{summary}\n\n"

    with open(OUTPUT_PATH, "w") as f:
        f.write(report)
    print(f"Summary report generated at {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
