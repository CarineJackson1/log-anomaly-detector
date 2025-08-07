# ✅ Secure Deployment Checklist

Use this checklist before releasing or deploying the project.

---

## 🔐 Application Security

- [ ] HTTPS enforced on all routes
- [ ] All API endpoints protected (auth where required)
- [ ] No use of `eval()` or insecure patterns
- [ ] Semgrep/Bandit scans clean
- [ ] No hardcoded secrets or tokens

---

## 🧾 Configuration & Secrets

- [ ] All secrets stored in environment variables
- [ ] `.env` file added to `.gitignore`
- [ ] Docker secrets / GitHub Secrets in use
- [ ] GitHub Actions workflows don't echo secrets

---

## 🐳 Docker & Infrastructure

- [ ] Docker images scanned with Trivy
- [ ] Dockerfiles follow best practices
- [ ] No `latest` tags used
- [ ] Exposed ports minimized (only 80/443/5000 if needed)

---

## 📡 CI/CD

- [ ] GitHub Actions include Semgrep, Bandit, Checkov, etc.
- [ ] Deployment secrets managed in GitHub
- [ ] Auto PRs for vulnerable deps via Dependabot

---

## 🌍 CORS / Headers

- [ ] CORS restricted to known frontend URLs
- [ ] Secure headers (`helmet` or Flask equivalent) set
- [ ] Rate limiting enabled (Flask-Limiter / nginx / middleware)

---

## 🧪 Final Tests

- [ ] OWASP ZAP scan passed
- [ ] Manual auth & access testing complete
- [ ] No open S3 buckets or cloud misconfigs
