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
