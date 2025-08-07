# 🛡️ Data Privacy & Protection Measures

**Project:** AstroSkill LMS  
**Last Updated:** [Date]

---

## 🔐 Data Types Collected

- Email addresses
- Names
- Learning progress
- Admin credentials

---

## 🔒 Storage & Encryption

| Data Type       | Method of Protection                  |
|------------------|----------------------------------------|
| Passwords        | Hashed using bcrypt (salted)           |
| Session Tokens   | Stored securely in HTTP-only cookies   |
| Personal Data    | Stored in encrypted PostgreSQL DB      |

---

## 🌐 Network Security

- HTTPS enforced on all environments
- CORS configured to allow only trusted domains
- CSRF protection via [Flask-WTF / FastAPI dependency]
- Backend not exposed publicly in development

---

## 👥 Access Control

- Role-based access implemented
- Admin dashboard protected
- User registration & login required

---

## ⚠️ No PII exposed in logs or console

- Logging is sanitized
- No `console.log()` in frontend in production
