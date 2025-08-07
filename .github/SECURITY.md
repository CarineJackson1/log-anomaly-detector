# 🔐 Security

---

## 🚀 Overview

AstroSkill Connector bridges the gap between Moodle course completion and employer recruitment, helping learners showcase verified credentials to hiring platforms.

This project maintains a proactive security posture by integrating automated CI-based scanning, PR protection rules, and clear reporting processes.

---

## 🛡 Supported Branches

| Branch   | Security Coverage                  |
|----------|------------------------------------|
| `main`   | ✅ Full scan + PR protection        |
| `develop`| ✅ Full scan + PR protection        |

---

## 🧪 CI-Based Security Scanning

AstroSkill LMS uses **GitHub Actions** to automatically scan for vulnerabilities on every pull request.

| Tool         | Target Scope         | Purpose                                         |
|--------------|----------------------|-------------------------------------------------|
| **Semgrep**  | Frontend + Backend   | Static code analysis using custom and open rules |
| **Bandit**   | Python backend       | Detects insecure code patterns in Python         |
| **Retire.js**| JavaScript frontend  | Finds vulnerable JS libraries in use             |
| **Trivy**    | Codebase & container | Finds OS/package-level vulnerabilities           |
| **Gitleaks** | Entire repo          | Detects hardcoded secrets                        |
| **OWASP ZAP**| Live staging URL     | Dynamic app security testing (DAST)              |
| **Dependabot** | PRs for dependencies | Ensures secure versions for packages            |

- ✅ **CI auto-fails** for **CRITICAL or HIGH** severity issues  
- 📄 Security summary is **posted automatically as a PR comment**  
- 🧾 Reports saved to `security-reports/` as **Markdown, PDF, and raw JSON**

---

## 🧠 How to Read Reports

Reports include:
- Vulnerability file/line location
- Description and severity
- CWE or rule ID (if available)

### Example (Markdown):

```md
### Semgrep Backend
- `backend/api/views.py:45` — Insecure use of `eval` (Severity: CRITICAL)
- `backend/app.py:23` — Hardcoded credentials (Severity: HIGH)
