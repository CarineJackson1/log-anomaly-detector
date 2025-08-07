<<<<<<< HEAD
<<<<<<< HEAD
=======
# scripts/generate_full_report.py

>>>>>>> 49e83b0e3e85c607539e8a07d81365e21d875f75
=======
import argparse
>>>>>>> 549e78b1c9c21502fbe2c5b2001515ae06f982ce
import json
import os
import sys
from datetime import datetime
<<<<<<< HEAD
from bs4 import BeautifulSoup

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_html(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_zap_critical_issues(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    issues = []
    for alertitem in soup.select('alertitem'):
        riskcode = alertitem.find('riskcode')
        if riskcode and int(riskcode.text) >= 2:  # RiskCode 2=Medium, 3=High
            alertname = alertitem.find('alert').text if alertitem.find('alert') else "Unknown"
            desc = alertitem.find('desc').text if alertitem.find('desc') else ""
            issues.append(f"{alertname}: {desc}")
    return issues

def summarize_semgrep(results):
    error_issues = [r for r in results if r.get("extra", {}).get("severity") == "ERROR"]
    warning_issues = [r for r in results if r.get("extra", {}).get("severity") == "WARNING"]
    lines = []
    if error_issues:
        lines.append(f"### Semgrep Errors ({len(error_issues)})")
        for i, issue in enumerate(error_issues, 1):
            lines.append(f"{i}. `{issue.get('check_id', 'N/A')}` in `{issue.get('path', 'N/A')}` line {issue['start']['line']}: {issue.get('extra', {}).get('message', '')}")
    if warning_issues:
        lines.append(f"### Semgrep Warnings ({len(warning_issues)})")
        for i, issue in enumerate(warning_issues, 1):
            lines.append(f"{i}. `{issue.get('check_id', 'N/A')}` in `{issue.get('path', 'N/A')}` line {issue['start']['line']}: {issue.get('extra', {}).get('message', '')}")
    if not error_issues and not warning_issues:
        lines.append("✅ No Semgrep issues found.")
    return "\n".join(lines), len(error_issues) > 0

def summarize_bandit(data):
    issues = data.get('results', [])
    errors = [i for i in issues if i.get('issue_severity') == 'HIGH']
    warnings = [i for i in issues if i.get('issue_severity') == 'MEDIUM']
    lines = []
    if errors:
        lines.append(f"### Bandit High Severity Issues ({len(errors)})")
        for i, issue in enumerate(errors, 1):
            lines.append(f"{i}. {issue.get('test_name')} in `{issue.get('filename')}` line {issue.get('line_number')}: {issue.get('issue_text')}")
    if warnings:
        lines.append(f"### Bandit Medium Severity Issues ({len(warnings)})")
        for i, issue in enumerate(warnings, 1):
            lines.append(f"{i}. {issue.get('test_name')} in `{issue.get('filename')}` line {issue.get('line_number')}: {issue.get('issue_text')}")
    if not errors and not warnings:
        lines.append("✅ No Bandit issues found.")
    return "\n".join(lines), len(errors) > 0

def summarize_retire(data):
    vulns = data.get('data', {}).get('vulnerabilities', [])
    criticals = [v for v in vulns if v.get('severity') == 'high']
    lines = []
    if criticals:
        lines.append(f"### Retire.js Critical Vulnerabilities ({len(criticals)})")
        for i, vuln in enumerate(criticals, 1):
            lines.append(f"{i}. {vuln.get('component')} - {vuln.get('identifiers', {}).get('summary', 'No description')}")
    if not criticals:
        lines.append("✅ No Retire.js critical vulnerabilities found.")
    return "\n".join(lines), len(criticals) > 0

def summarize_gitleaks(data):
    leaks = data.get('results', [])
    lines = []
    if leaks:
        lines.append(f"### Gitleaks Secrets Found ({len(leaks)})")
        for i, leak in enumerate(leaks, 1):
            lines.append(f"{i}. {leak.get('Description')} in {leak.get('File')} (Commit {leak.get('Commit')})")
    else:
        lines.append("✅ No Gitleaks issues found.")
    return "\n".join(lines), len(leaks) > 0

def summarize_trivy(data):
    vulns = []
    for result in data.get('Results', []):
        vulns.extend(result.get('Vulnerabilities', []))
    criticals = [v for v in vulns if v.get('Severity', '').lower() == 'critical']
    lines = []
    if criticals:
        lines.append(f"### Trivy Critical Vulnerabilities ({len(criticals)})")
        for i, vuln in enumerate(criticals, 1):
            lines.append(f"{i}. {vuln.get('PkgName')} - {vuln.get('Title')} ({vuln.get('Severity')})")
    if not criticals:
        lines.append("✅ No Trivy critical vulnerabilities found.")
    return "\n".join(lines), len(criticals) > 0

def main(args):
    # Expected args: --bandit <file> --semgrep-frontend <file> --semgrep-backend <file> --retire <file> --gitleaks <file> --trivy <file> --zap <file> --output <file>
    import argparse
    parser = argparse.ArgumentParser(description="Generate unified security report")
    parser.add_argument("--bandit", required=True)
    parser.add_argument("--semgrep-frontend", required=True)
    parser.add_argument("--semgrep-backend", required=True)
    parser.add_argument("--retire", required=True)
    parser.add_argument("--gitleaks", required=True)
    parser.add_argument("--trivy", required=True)
    parser.add_argument("--zap", required=True)
    parser.add_argument("--output", required=True)
    opts = parser.parse_args(args)

    print("Loading reports...")
    bandit_data = load_json(opts.bandit)
    semgrep_front = load_json(opts.semgrep_frontend)
    semgrep_back = load_json(opts.semgrep_backend)
    retire_data = load_json(opts.retire)
    gitleaks_data = load_json(opts.gitleaks)
    trivy_data = load_json(opts.trivy)
    zap_html = load_html(opts.zap)

    # Combine semgrep results
    combined_semgrep_results = semgrep_front.get("results", []) + semgrep_back.get("results", [])

    # Summarize each tool
    semgrep_summary, semgrep_has_errors = summarize_semgrep(combined_semgrep_results)
    bandit_summary, bandit_has_errors = summarize_bandit(bandit_data)
    retire_summary, retire_has_errors = summarize_retire(retire_data)
    gitleaks_summary, gitleaks_has_errors = summarize_gitleaks(gitleaks_data)
    trivy_summary, trivy_has_errors = summarize_trivy(trivy_data)
    # For ZAP, just check if there are any critical alerts
    zap_critical_issues = extract_zap_critical_issues(zap_html)
    zap_has_errors = len(zap_critical_issues) > 0
    zap_summary = "### OWASP ZAP Critical Alerts ({})\n".format(len(zap_critical_issues))
    if zap_critical_issues:
        for i, issue in enumerate(zap_critical_issues, 1):
            zap_summary += f"{i}. {issue}\n"
    else:
        zap_summary += "✅ No OWASP ZAP critical alerts found.\n"

    # Compose full report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_lines = [
        f"# Security Scan Summary Report",
        f"**Generated on:** {timestamp}",
        "",
        semgrep_summary,
        "",
        bandit_summary,
        "",
        retire_summary,
        "",
        gitleaks_summary,
        "",
        trivy_summary,
        "",
        zap_summary,
        "",
    ]

    # Mark report if any errors found
    if any([semgrep_has_errors, bandit_has_errors, retire_has_errors, gitleaks_has_errors, trivy_has_errors, zap_has_errors]):
        report_lines.append("\n**CRITICAL ISSUE FOUND**\n")
    else:
        report_lines.append("\nAll scans passed without critical issues.\n")

    # Write report
    output_path = Path(opts.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(report_lines), encoding='utf-8')

    print(f"Report generated at {output_path}")
    if any([semgrep_has_errors, bandit_has_errors, retire_has_errors, gitleaks_has_errors, trivy_has_errors, zap_has_errors]):
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
=======

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
    if not os.path.isfile(path):
        print(f"⚠️ Warning: File not found: {path}")
        return None
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading JSON from {path}: {e}")
            return None

def summarize_semgrep(data):
    if not data or "results" not in data:
        return ["No issues found."]
    lines = []
    for issue in data["results"]:
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
    if not os.path.isfile(path):
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
        # No JSON parsing; assume exists means a report
        return os.path.isfile(path)
    return False

def main(args):
    report_md = f"# 🔒 Security Scan Summary\n\nScan time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    critical_found = False

    tool_data = {}

    # Load all JSON inputs where provided
    for tool, display_name in REPORT_PATHS.items():
        input_path = getattr(args, tool, None)
        if input_path:
            if tool == "zap":
                # For zap, input_path is a file path (html)
                tool_data[tool] = input_path
            else:
                tool_data[tool] = load_json(input_path)
        else:
            tool_data[tool] = None

    # Generate summaries per tool
    for tool, display_name in REPORT_PATHS.items():
        data = tool_data.get(tool)
        if tool == "semgrep_frontend" or tool == "semgrep_backend":
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

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report_md)

    print(f"✅ Report written to {args.output}")

    if critical_found:
        print("❌ Critical or high severity issues found, failing CI.")
        sys.exit(1)
    else:
        print("✅ No critical or high severity issues found.")
        sys.exit(0)

if __name__ == "__main__":
<<<<<<< HEAD
    if len(sys.argv) != 4:
        print("Usage: python generate_full_report.py <frontend_json> <backend_json> <output_md_path>")
        sys.exit(2)

    frontend_path, backend_path, output_md_path = sys.argv[1], sys.argv[2], sys.argv[3]
    generate_combined_report(frontend_path, backend_path, output_md_path)
>>>>>>> 49e83b0e3e85c607539e8a07d81365e21d875f75
=======
    parser = argparse.ArgumentParser(description="Generate combined security report from multiple tool JSON outputs.")
    parser.add_argument("--bandit", help="Path to bandit JSON report")
    parser.add_argument("--semgrep-frontend", help="Path to semgrep frontend JSON report")
    parser.add_argument("--semgrep-backend", help="Path to semgrep backend JSON report")
    parser.add_argument("--gitleaks", help="Path to gitleaks JSON report")
   
>>>>>>> 549e78b1c9c21502fbe2c5b2001515ae06f982ce
