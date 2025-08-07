#Security

![🔐 Security Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/AstroSkill/astroskill-lms-connector/develop/.github/badges/security-badge.json)
⸻

🚀 Overview

AstroSkill Connector bridges the gap between Moodle course completion and employer recruitment…

⸻

🔐 Security Policy

🛡 Supported Branches

Branch	Security Coverage
main	✅ Full Scan & PR Protection
develop	✅ Full Scan & PR Protection


⸻

🐞 Reporting a Vulnerability

If you discover a security issue, please do not open a public GitHub issue.
Instead, report privately to the project maintainers:
	•	Lead Security Reviewer: @CarineJackson1
	•	Security Reviewer: @sajanamhr21

Expected response time: within 48 hours

⸻

🧪 CI-Based Security Scanning

AstroSkill LMS integrates automated security testing via GitHub Actions:

Tool	Scan Target	Output
Semgrep	Frontend + Backend	SAST, custom rule checks
Bandit	Python backend	Common Python security issues
Retire.js	JS dependencies	Known vulnerable libraries
OWASP ZAP	Live frontend (staging)	Dynamic Application Security Testing (DAST)
Dependabot PR CI	Any PR from Dependabot	Runs tests + security checks

✅ PRs auto-fail on critical security violations
📄 Results summarized and posted as PR comments
📂 Artifacts stored for audit in security-reports/

⸻

📦 Dependency Updates (via Dependabot)

All package ecosystems are monitored for security updates:

Ecosystem	Frequency	Auto-Merge	Branch
Python (pip)	Daily	✅	develop
Node.js (npm)	Weekly	✅	develop
GitHub Actions	Weekly	✅	develop
Docker	Weekly	✅	develop

PRs are:
	•	Auto-assigned to @CarineJackson1, @sajanamhr21
	•	Auto-labeled with dependencies, auto-merge
	•	Merged if tests + scans pass

⸻

🛡 Security Enforcement & Best Practices
	•	✅ Security Scans are run on every PR via GitHub Actions
	•	✅ Credentials and API keys are managed via GitHub Secrets
	•	✅ Branch protection is enabled on main and develop
	•	✅ Security reports are uploaded for audit trails
	•	✅ Auto-summary comments are generated on PRs for transparency
