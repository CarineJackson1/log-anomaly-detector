🔐 Security Overview

🚀 About

AstroSkill Connector bridges the gap between Moodle course completion and employer recruitment—enabling learners to showcase verified credentials to hiring platforms.

This project maintains a proactive security posture through:
	•	✅ Automated CI-based scanning (SAST, DAST, secrets, deps)
	•	✅ Pull Request (PR) protection with branch rules
	•	✅ Secret scanning and dynamic security testing
	•	✅ Continuous dependency update monitoring

⸻

🛡️ Branch Security Coverage

Branch	Scanning Level	PR Protection
main	✅ Full scan (SAST + DAST)	✅ Enabled
develop	✅ Full scan (SAST only)	✅ Enabled
All PRs	✅ Fast scan (Semgrep only)	❌ N/A
Dependabot	✅ Full scan + labeling	✅ Conditional


⸻

🧪 CI-Based Security Tooling

Tool	Scope	Purpose
Semgrep	Frontend + Backend	Custom static code analysis (SAST)
Bandit	Python backend	Python-specific SAST
Retire.js	JavaScript frontend	Detects vulnerable JS libraries
Trivy	App files & containers	OS/package vulnerability scanning
Gitleaks	Entire repository	Secrets/hardcoded credential detection
OWASP ZAP	Staging frontend	Dynamic app security testing (DAST)
Dependabot	Dependencies	Automatic PRs for vulnerable packages


⸻

📄 Security Scan Reports

The CI pipeline produces detailed security reports on every PR and push to critical branches (main, develop), and on all Dependabot PRs.

✅ Highlights
	•	🔍 Scans run automatically
	•	🟥 CI fails if critical/high issues are found
	•	📁 Reports saved to security-reports/
	•	💬 PR comments summarize detected issues

⸻

🧠 How to Read the Reports

Reports are generated in Markdown and PDF formats and saved to:

security-reports/
├── summary_report.md
├── summary_report.pdf
└── raw/           # Raw JSON outputs from tools

Each report section includes:
	•	📂 File & line number of the issue
	•	📝 Description and rule/message
	•	⚠️ Severity (CRITICAL, HIGH, MEDIUM, LOW, INFO)
	•	🆔 Rule ID, CWE, or category where applicable

📌 Example (Markdown Snippet):

## Semgrep Backend
- `backend/api/views.py:45` — Use of `eval()` detected (Severity: CRITICAL)
- `backend/app.py:23` — Hardcoded credentials (Severity: HIGH)

## Bandit Backend
- `backend/models/user.py:87` — Use of insecure function `pickle.loads` (Severity: HIGH)

⸻

### 🔎 Vulnerability Triage Checklist

- [ ] Review Semgrep findings
- [ ] Review Bandit (Python backend) issues
- [ ] Review Trivy (OS/package scan)
- [ ] Review Gitleaks (secrets)
- [ ] Review Retire.js (JS libraries)
- [ ] Review OWASP ZAP (DAST results)
- [ ] Mark resolved vulnerabilities as mitigated or fixed

⸻

📦 Dependency Update Strategy

Ecosystem	Frequency	Auto-Merge	Target Branch
Python (pip)	Daily	✅	develop
Node.js (npm)	Weekly	✅	develop
GitHub Actions	Weekly	✅	develop
Docker	Weekly	✅	develop
