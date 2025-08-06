# 🔐 Security Assessment Report

**Project:** AstroSkill LMS  
**Date:** [Insert Date]  
**Conducted by:** [Your Name]

---

## 🔎 Tools Used

| Tool         | Purpose                                 |
|--------------|-----------------------------------------|
| Semgrep      | Static code analysis (SAST)             |
| Bandit       | Python-specific security scanning       |
| ESLint Plugin (Security) | JS/React linting for security      |
| Trivy        | Container vulnerability scanning        |
| Checkov      | Terraform / IaC scanning                |
| Gitleaks     | Secrets detection in repo history       |
| OWASP ZAP    | Dynamic app security testing (DAST)     |

---

## 🚨 Findings Summary

| Severity   | # of Issues | Tools |
|------------|-------------|-------|
| High       | [X]         | [List tools] |
| Medium     | [X]         | [List tools] |
| Low        | [X]         | [List tools] |
| Info       | [X]         | [List tools] |

---

## 🛠️ Sample Issues

### 🧨 High: Hardcoded Secret Found
**Tool:** Gitleaks  
**Location:** `frontend/src/config.js`  
**Fix:** Use environment variables and `.env` files

---

### 🕵️ Medium: Insecure Use of `eval()`
**Tool:** Bandit  
**File:** `backend/utils/exec.py`  
**Fix:** Replace `eval()` with safe alternatives

---

## ✅ Recommendations

- Remove or rotate any exposed secrets
- Enforce HTTPS everywhere (frontend & backend)
- Enable rate limiting
- Use helmet/secure headers
- Enable Docker image scanning in CI
