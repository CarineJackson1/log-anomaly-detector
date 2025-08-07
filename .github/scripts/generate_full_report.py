<<<<<<< HEAD
=======
# scripts/generate_full_report.py

>>>>>>> 49e83b0e3e85c607539e8a07d81365e21d875f75
import json
import sys
from pathlib import Path
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

def load_semgrep_json(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_markdown_report(results, output_path, title="Semgrep Report"):
    error_issues = [r for r in results if r.get("extra", {}).get("severity") == "ERROR"]
    count_errors = len(error_issues)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        f"# {title}",
        "",
        f"**Scan Time:** {timestamp}",
        f"**Error-level Issues Found:** {count_errors}",
        "",
        "---",
        ""
    ]

    if count_errors == 0:
        lines.append("✅ No ERROR-level issues found!")
    else:
        for i, result in enumerate(error_issues, 1):
            extra = result.get("extra", {})
            lines.extend([
                f"## {i}. {extra.get('message', 'No message')}",
                f"- **Rule:** `{result.get('check_id', 'N/A')}`",
                f"- **File:** `{result.get('path', 'N/A')}`",
                f"- **Line:** {result['start']['line']}",
                f"- **Severity:** {extra.get('severity', 'UNKNOWN')}",
                f"- **CWE:** {extra.get('metadata', {}).get('cwe', 'N/A')}",
                f"- **Category:** {extra.get('metadata', {}).get('category', 'N/A')}",
                "",
                "---",
                ""
            ])

    with open(output_path, 'w', encoding='utf-8') as md_file:
        md_file.write('\n'.join(lines))

    if count_errors > 0:
        print(f"❌ Found {count_errors} ERROR-level issues.")
        sys.exit(1)
    else:
        print("✅ No ERROR-level issues found.")

def generate_combined_report(frontend_path, backend_path, output_md_path):
    combined_results = []

    for path in [frontend_path, backend_path]:
        if Path(path).exists():
            data = load_semgrep_json(path)
            combined_results.extend(data.get("results", []))

    write_markdown_report(combined_results, output_md_path, title="Combined Semgrep Report")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python generate_full_report.py <frontend_json> <backend_json> <output_md_path>")
        sys.exit(2)

    frontend_path, backend_path, output_md_path = sys.argv[1], sys.argv[2], sys.argv[3]
    generate_combined_report(frontend_path, backend_path, output_md_path)
>>>>>>> 49e83b0e3e85c607539e8a07d81365e21d875f75
