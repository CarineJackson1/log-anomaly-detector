## 🚀 Description

<!--
Explain the purpose of this PR and what it changes. 
If this is a security/DevSecOps change (e.g., dependency updates, vuln disclosures, CI/CD hardening), call that out explicitly.
-->

## 🛡️ Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Dependency update / security patch
- [ ] Security policy / disclosure workflow
- [ ] CI/CD or deployment improvement
- [ ] Documentation
- [ ] Other: ___________________

## 🧪 Checklist (especially for security-related changes)

- [ ] Does this change introduce or modify dependency updates? If yes:  
  - [ ] Dependabot config reviewed (`.github/dependabot.yml`)
  - [ ] Updated dependencies have been tested via CI
- [ ] Is there any new external input (forms, data submission)?  
  - [ ] Input validation implemented  
  - [ ] Spam/abuse mitigation considered  
- [ ] Were security/privacy implications assessed?  
  - [ ] Data handling follows the project's privacy/security guidelines  
  - [ ] Any new secrets or credentials are **not** committed
- [ ] For deployment changes:  
  - [ ] Secure deployment checklist completed  
  - [ ] IaC/container changes reviewed (e.g., Docker hardening, IAM least privilege)
- [ ] For vulnerability reporting or policy updates:  
  - [ ] `SECURITY.md` reflects intended process  
  - [ ] Contact mechanism (email/PGP) is valid or noted for update
- [ ] Codeowners/reviewers assigned appropriately (`.github/CODEOWNERS`)

## ✅ Implementation Notes

<!--
Detail what was done, why, and any decisions made.
If this is a security fix or policy addition, include impact, mitigation, and testing steps.
-->

## 📦 How to Test

<!--
Instructions for verifying the change, e.g., running tests, simulating scenario, reviewing config.
-->

## 🗂 Related Issues / References

- Closes: #[issue-number]
- Related: #[other-issue]
- Security advisory: [if applicable]

## 📝 Additional Notes

<!--
Anything else reviewers should know (e.g., required post-merge steps like enabling Dependabot alerts or private vuln reporting).
-->
