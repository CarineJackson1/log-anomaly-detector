# Security Policy

## Reporting a Vulnerability

We take the security of AstroSkill Connector seriously. If you discover a security vulnerability, please report it responsibly by opening a private issue or contacting us via email at security@astroskill.com (replace with your real contact).

Please include:

- Description of the vulnerability
- Steps to reproduce
- Impact assessment (if known)
- Any suggested remediation

## Security Practices

Our project maintains a proactive security posture including:

- Automated Continuous Integration (CI) security scans on all pull requests and critical branches (`main`, `develop`).
- Static Application Security Testing (SAST) via Semgrep and Bandit.
- Secrets detection using Gitleaks.
- Dependency vulnerability monitoring via Dependabot and Retire.js.
- Dynamic Application Security Testing (DAST) using OWASP ZAP.
- Container and filesystem vulnerability scanning with Trivy.
- Strict pull request protection rules.
- Automated labeling and triage workflows.

## Supported Branches

| Branch    | Security Coverage          |
|-----------|----------------------------|
| `main`    | Full security scan + PR protection |
| `develop` | Full security scan + PR protection |

## Automated Scanning & PR Comments

Security scans are run automatically on pull requests, including those from Dependabot. Results are summarized in PR comments for quick review and action.

Critical and high severity findings cause the CI to fail and label PRs for immediate security review.

## Dependencies & Updates

- Dependencies are monitored and updated via Dependabot with daily and weekly schedules depending on ecosystem.
- Automated pull requests are created for security patches and updates.

---

Thank you for helping keep AstroSkill Connector secure!
