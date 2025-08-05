# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly by emailing us with the following details:

- Description of the vulnerability  
- Steps to reproduce the issue  
- Impact assessment (if known)  
- Any suggested fixes or mitigations  

We commit to acknowledging all reports within 48 hours and will work to resolve critical issues as quickly as possible.

---

## Supported Versions

We support security fixes for the latest stable release of this project. Please keep your dependencies and software up to date.

---

## Security Best Practices

- Always keep your dependencies updated  
- Regularly review dependency alerts in GitHub  
- Use automated tools such as Dependabot and Snyk for vulnerability scanning  
- Follow secure coding standards and practices  

---

## 📊 Security Workflow Overview
<img width="2461" height="2000" alt="security_workflow_diagram" src="https://github.com/user-attachments/assets/1155320e-6235-47ff-8297-76e8d5d918c6" />

---

## Disclosures

Once a vulnerability is resolved, we may publicly disclose the issue to inform users and the community, unless a request for confidentiality is made.

---

## Contact

### Lead Security Reviewer
- **Name:** Carine Jackson  
- **GitHub:** [@CarineJackson1](https://github.com/CarineJackson1)  
- **Email:** carinejackson48@gmail.com 
- **Role:** Lead Security Reviewer

### Security Reviewer
- **Name:** Sajana MHR  
- **GitHub:** [@sajanamhr21](https://github.com/sajanamhr21)  
- **Email:** security@yourdomain.com  
- **Role:** Secondary Security Reviewer

## 🔒 Security & Dependency Management

This repository uses an automated **SecDevOps workflow** to keep dependencies updated and secure.

### 1. Dependency Updates (Dependabot)
- **Frequency:** Weekly for Python (`pip`), JavaScript (`npm`), Docker, and GitHub Actions workflows.
- **Labels:** Each update PR gets:
  - `dependencies` (marks as a dependency update)
  - `auto-merge` (optional – triggers automatic merging)
- **Reviewers:** Security leads (`@CarineJackson1`, `@sajanamhr21`) are auto-assigned for review.

### 2. Auto-Merge Rules
- Only **Dependabot PRs** with the `auto-merge` label will be merged automatically.
- Auto-merge happens **after** all required checks pass (build, tests, security scans).
- Major version updates **must be reviewed manually** before merging.

### 3. Security Scans
- **CodeQL Analysis** (`.github/workflows/codeql.yml`)
  - Runs on every PR and weekly.
  - Detects vulnerabilities in JavaScript and Python code.
- **Snyk Scan** (`.github/workflows/snyk.yml`)
  - Runs on every PR and weekly.
  - Detects insecure dependencies in both JavaScript and Python.
  - Requires `SNYK_TOKEN` in repo secrets.

### 4. Branch Protection
- **`develop` branch:**
  - Requires passing build/tests, CodeQL, and Snyk before merging.
  - Requires PR reviews from code owners.
- **`main` branch:**
  - Changes can only come from `develop`.
  - Requires passing all security scans and build/tests before merging.

---

