import argparse
import json
import os
import sys
from datetime import datetime

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
    parser = argparse.ArgumentParser(description="Generate combined security report from multiple tool JSON outputs.")
    parser.add_argument("--bandit", help="Path to bandit JSON report")
    parser.add_argument("--semgrep-frontend", help="Path to semgrep frontend JSON report")
    parser.add_argument("--semgrep-backend", help="Path to semgrep backend JSON report")
    parser.add_argument("--gitleaks", help="Path to gitleaks JSON report")
   
