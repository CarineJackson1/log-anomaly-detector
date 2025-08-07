# 🔐 Security Overview

## 🚀 About

AstroSkill Connector bridges the gap between Moodle course completion and employer recruitment, helping learners showcase verified credentials to hiring platforms.

This project maintains a proactive security posture through:
- Automated CI-based scanning
- PR protection rules
- Secret scanning and DAST
- Dependency update monitoring

---

## 🛡 Supported Branches

| Branch    | Security Coverage          |
|-----------|----------------------------|
| `main`    | ✅ Full scan + PR protection |
| `develop` | ✅ Full scan + PR protection |

---

## 🧪 CI-Based Scanning Tools

| Tool         | Target Scope         | Purpose                                           |
|--------------|----------------------|---------------------------------------------------|
| Semgrep      | Frontend + Backend   | Static code analysis                              |
| Bandit       | Python backend       | Python SAST rules                                 |
| Retire.js    | JavaScript frontend  | Vulnerable JS libraries                           |
| Trivy        | Codebase & container | OS and package vulnerabilities                    |
| Gitleaks     | Whole repo           | Secrets detection                                 |
| OWASP ZAP    | Staging frontend     | Dynamic app security testing                      |
| Dependabot   | PR dependencies      | Auto PRs for security patches                     |

# 🔐 Security Scan Summary Reports

Our CI pipeline runs a comprehensive set of automated security scans on every pull request and push to critical branches (`main` and `develop`). These scans detect vulnerabilities, secrets, and insecure code patterns.

## Tools and Coverage

| Tool        | Scope                          | Purpose                                   |
|-------------|--------------------------------|-------------------------------------------|
| Semgrep     | Frontend & Backend code        | Static code analysis with custom rules   |
| Bandit      | Python backend                 | Detects Python security issues           |
| Retire.js   | JavaScript dependencies        | Finds vulnerable JS libraries             |
| Gitleaks    | Entire repository             | Detects hardcoded secrets                 |
| Trivy       | Codebase & containers          | Finds OS/package vulnerabilities         |
| OWASP ZAP   | Live frontend (staging)        | Dynamic Application Security Testing (DAST) |

## Reading the Report

Reports are generated in Markdown and PDF formats and saved in the `security-reports/` directory. The report contains sections per tool listing detected issues.

Each issue entry includes:

- **File and line number** where the issue was detected
- **Description** of the vulnerability or issue
- **Severity level** (CRITICAL, HIGH, MEDIUM, LOW, INFO)
- **Additional details** like CWE or rule IDs where available

### Example Markdown Section:

```md
## Semgrep Backend
- `backend/api/views.py:45` — Use of `eval()` detected (Severity: CRITICAL)
- `backend/app.py:23` — Hardcoded credentials (Severity: HIGH)

## Bandit Backend
- `backend/models/user.py:87` — Use of insecure function `pickle.loads` (Severity: HIGH)
```


- 🛠️ Scans run on every PR
- 🟥 CI fails on critical/high severity findings
- 💬 PR comments summarize results
- 📁 Reports saved to `security-reports/`

---

## 🧠 Reading Reports

Reports contain:
- File and line number of the issue
- Description and severity
- CWE, rule ID, or category

---

## 📦 Dependency Updates

| Ecosystem       | Frequency | Auto-Merge | Target Branch |
|-----------------|-----------|------------|----------------|
| Python (pip)    | Daily     | ✅          | `develop`      |
| Node.js (npm)   | Weekly    | ✅          | `develop`      |
| GitHub Actions  | Weekly    | ✅          | `develop`      |
| Docker          | Weekly    | ✅          | `develop`      |
