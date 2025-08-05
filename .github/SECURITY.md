# 🔐 Security Policy

## 🛡 Supported Branches
| Branch  | Supported |
|---------|-----------|
| main    | ✅        |
| develop | ✅        |

---

## 🐞 Reporting a Vulnerability
If you find a security issue, please **do not open a public GitHub Issue**.  
Instead, contact the security team directly:

- **Lead Security Reviewer:** [@CarineJackson1](https://github.com/CarineJackson1)
- **Security Reviewer:** [@sajanamhr21](https://github.com/sajanamhr21)

We aim to respond within **48 hours**.

---

## 📊 Security Scans
- **CodeQL**: [View Results](https://github.com/CarineJackson1/astroskill-lms-connector-carine/security/code-scanning)
- **Snyk (via GitHub Actions)**: [View Results](https://github.com/CarineJackson1/astroskill-lms-connector-carine/actions/workflows/snyk.yml)

---

## 🔄 Automated Dependency Updates
We use [Dependabot](https://docs.github.com/en/code-security/dependabot) to keep dependencies secure and up-to-date.  
Security PRs are:
- Reviewed by: `@CarineJackson1`, `@sajanamhr21`
- Auto-merged if tests pass

---

## 🛠 Security Best Practices
- All PRs must pass **CodeQL** and **Snyk** scans before merging
- Sensitive credentials are stored in **GitHub Actions Secrets**
- Branch protection is enabled on `main` and `develop`
