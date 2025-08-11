# AstroSkill Connector — Security Overview

## About

AstroSkill Connector securely links Moodle course completion to employer recruitment, enabling verified credential sharing with hiring platforms.

We maintain strong security practices through automated CI scans, PR protection, secret scanning, and dependency monitoring.

## Branches & Security

| Branch    | Security Measures                    |
|-----------|------------------------------------|
| `main`    | Full security scan + PR protection |
| `develop` | Full security scan + PR protection |

## Security Scanning Tools

| Tool         | Scope                        | Purpose                               |
|--------------|------------------------------|-------------------------------------|
| Semgrep      | Frontend & Backend code      | Static code analysis with custom rules |
| Bandit       | Python backend               | Python security static analysis     |
| Retire.js    | JavaScript dependencies      | Finds vulnerable JS libraries       |
| Trivy        | Codebase & container images  | OS/package vulnerability scanning   |
| Gitleaks     | Entire repository            | Hardcoded secrets detection         |
| OWASP ZAP    | Live frontend (staging)      | Dynamic application security testing|

## Workflow Summary

- Automated security scans run on every PR and branch update.
- Dependabot PRs trigger full scans and auto-labeling.
- CI fails if critical/high severity issues are found.
- Security summaries are posted as PR comments.
- Reports saved in `security-reports/` for audit and review.

## Dependency Updates

We leverage Dependabot for:

| Ecosystem       | Schedule | Auto-Merge | Target Branch |
|-----------------|----------|------------|---------------|
| Python (pip)    | Daily    | Yes        | `develop`     |
| Node.js (npm)   | Weekly   | Yes        | `develop`     |
| GitHub Actions  | Weekly   | Yes        | `develop`     |
| Docker          | Weekly   | Yes        | `develop`     |

---

*Keeping AstroSkill Connector safe and trustworthy for our users and partners.*
