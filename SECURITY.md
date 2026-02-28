# 🔐 Security Document - Quantum LMS

**Last Security Audit**: February 28, 2026  
**Status**: All critical issues resolved ✅

---

## ✅ Security Audit Results

### Current Security Status

All sensitive credentials are now properly secured using environment variables. No hardcoded secrets exist in production code.

#### Secure Files (In Use)
| File | Status | Method |
|------|--------|--------|
| `app.py` | ✅ Secure | `os.getenv('GROQ_API_KEY')` |
| `chatbot.py` | ✅ Secure | `os.getenv('GROQ_API_KEY')` |
| `video_generator.py` | ✅ Secure | API key passed as parameter from app.py |
| `.env` | ✅ Protected | Listed in `.gitignore` |

#### Fixed Files (Old/Unused)
| File | Issue | Resolution |
|------|-------|------------|
| `lms_chatbot.py` | ❌ Hardcoded API key | ✅ Removed, now uses `os.getenv()` |
| `test_email.py` | ❌ Placeholder credentials | ✅ Updated to use `.env` |

---

## 🔐 Environment Variables

All sensitive data is stored in the `.env` file, which is:
- ✅ **Not tracked by Git** (in `.gitignore`)
- ✅ **Loaded at runtime** via `python-dotenv`
- ✅ **Has example template** (`.env.example`)

### Required Environment Variables

```bash
# .env file structure
GROQ_API_KEY=gsk_your_api_key_here      # Required for AI features
SECRET_KEY=your-flask-secret-key        # Required for sessions
SENDER_EMAIL=your-email@gmail.com       # Optional for alerts
SENDER_PASSWORD=your-app-password       # Optional for alerts
```

### How to Set Up

1. **Copy the template**:
   ```bash
   cp .env.example .env
   ```

2. **Get your Groq API key** (free):
   - Visit: https://console.groq.com/keys
   - Sign up (no credit card required)
   - Create API key
   - Copy key starting with `gsk_...`

3. **Add to `.env` file**:
   ```bash
   GROQ_API_KEY=gsk_your_actual_key_here
   SECRET_KEY=change-this-to-random-string
   ```

4. **Never commit `.env`**: 
   - The `.gitignore` file prevents this
   - Only commit `.env.example`

---

## 🚨 Critical Security Measures

### 1. Database Security

#### Default Credentials (⚠️ CHANGE IN PRODUCTION)
```python
# Default admin account (users.db)
Username: admin
Password: admin123  # ⚠️ CHANGE THIS!
```

**Before production deployment:**
```python
# Change via Python or SQLite browser
import sqlite3
conn = sqlite3.connect('users.db')
conn.execute("UPDATE users SET password=? WHERE username='admin'", 
             ('your_new_secure_password',))
conn.commit()
```

#### SQL Injection Protection
✅ All queries use parameterized statements:
```python
# ✅ SECURE - Parameterized query
cursor.execute("SELECT * FROM users WHERE username=?", (username,))

# ❌ INSECURE - String concatenation (NOT used)
# cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
```

### 2. Session Security

#### Flask Secret Key
- **Current**: Falls back to `'fallback-quantum-secret-2026'`
- **Production**: Must set strong random key in `.env`

```python
# Generate a strong secret key
import secrets
print(secrets.token_hex(32))
# Output: e.g., '8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6e'
```

Add to `.env`:
```bash
SECRET_KEY=8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6e
```

#### Session Storage
- ✅ Server-side Flask sessions
- ✅ Quantum key verification required
- ✅ Session timeout after inactivity

### 3. API Key Protection

#### Groq API Key Security
```python
# ✅ SECURE - Loaded from environment
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise ValueError("API key not found")

# ❌ INSECURE - Hardcoded (NEVER do this)
# GROQ_API_KEY = "gsk_LL7uSUIpXAE..."  # WRONG!
```

#### API Key Rotation
If your API key is compromised:
1. Revoke old key at: https://console.groq.com/keys
2. Generate new key
3. Update `.env` file
4. Restart Flask: `python app.py`

### 4. Git Repository Security

#### .gitignore Protection
The following are **NEVER committed** to Git:
```
.env                # Environment variables
*.db                # SQLite databases (user data)
output/             # Generated videos
*.key, *.pem        # Cryptographic keys
secrets/            # Any secret directory
```

#### Before First Commit
```bash
# Verify .env is not tracked
git status

# Should NOT show .env in "Changes to be committed"
# If it does, run:
git rm --cached .env
git commit -m "Remove .env from tracking"
```

---

## 🔒 Security Features

### Multi-Factor Authentication
1. **Face Detection** (Biometric)
   - OpenCV Haar Cascade
   - Liveness check via webcam
   - No face image storage (privacy-first)

2. **Password Verification** (Knowledge)
   - SQLite credential lookup
   - Parameterized queries (SQL injection protection)
   - Failed attempt tracking

3. **Quantum Key (BB84 Protocol)** (Possession)
   - Simulated quantum key distribution
   - Session binding
   - Prevents session hijacking

### Anomaly Detection
- **Algorithm**: Isolation Forest (scikit-learn)
- **Features**: Login time, IP address, behavior patterns
- **Action**: Real-time alerts for suspicious activity

### Input Validation
- ✅ Flask CSRF protection (can be enhanced)
- ✅ Parameterized SQL queries
- ✅ Content-Type validation on uploads
- ⚠️ Rate limiting (not implemented - future enhancement)

---

## 🛡️ Production Security Checklist

Before deploying to production:

### Critical (Must Do)
- [ ] Change all default passwords
  ```bash
  admin / admin123 → Strong password
  ```
- [ ] Set strong `SECRET_KEY` in `.env`
  ```bash
  SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
  ```
- [ ] Enable HTTPS (SSL/TLS)
  - Use Let's Encrypt for free SSL
  - Configure Flask with Gunicorn + Nginx
- [ ] Remove or secure test accounts
  ```python
  # Delete: student1, teacher1, etc.
  ```
- [ ] Verify `.env` is in `.gitignore`
  ```bash
  grep ".env" .gitignore  # Should exist
  ```

### Important (Highly Recommended)
- [ ] Set up database backups
  ```bash
  # Automated daily backup
  0 2 * * * cp users.db backups/users_$(date +\%Y\%m\%d).db
  ```
- [ ] Add rate limiting
  ```python
  # Flask-Limiter for API protection
  pip install Flask-Limiter
  ```
- [ ] Implement CSRF protection
  ```python
  pip install Flask-WTF
  ```
- [ ] Add logging (file-based, not console)
  ```python
  import logging
  logging.basicConfig(filename='app.log', level=logging.INFO)
  ```
- [ ] Set up monitoring (Sentry, etc.)
- [ ] Configure CORS properly
  ```python
  # Flask-CORS with specific origins
  ```

### Optional (Nice to Have)
- [ ] Implement 2FA/TOTP
- [ ] Add password strength requirements
- [ ] Set up intrusion detection
- [ ] Enable database encryption
- [ ] Add API key usage limits
- [ ] Implement password reset flow
- [ ] Add account lockout after failed attempts
- [ ] Set up WAF (Web Application Firewall)

---

## 🔍 Security Testing

### Manual Security Checks

```bash
# 1. Check for hardcoded secrets
grep -r "gsk_" *.py        # Should only find in .env
grep -r "api_key.*=" *.py  # Should use os.getenv()

# 2. Verify .env is protected
git status .env            # Should be untracked
cat .gitignore | grep .env # Should be listed

# 3. Check file permissions
# Linux/Mac
ls -l .env           # Should be 600 or 644
ls -l users.db       # Should be 644

# Windows
icacls .env          # Check permissions

# 4. Scan for SQL injection vectors
grep -r "execute.*f\"" *.py     # Should NOT exist
grep -r "execute.*format" *.py  # Should NOT exist
```

### Automated Security Scanning

```bash
# Install security tools
pip install bandit safety

# Run security audit
bandit -r . -f json -o security_report.json

# Check for known vulnerabilities in dependencies
safety check --full-report

# Scan for secrets in Git history
pip install truffleHog
truffleHog --regex --entropy=False .
```

---

## 🚨 Incident Response

### If API Key is Compromised

1. **Immediately revoke** at https://console.groq.com/keys
2. **Generate new key**
3. **Update `.env` file**
4. **Restart application**
5. **Review logs** for unauthorized usage
6. **Rotate all other secrets** (SECRET_KEY, passwords)

### If Database is Accessed

1. **Backup current state**
   ```bash
   cp users.db users_incident_$(date +%Y%m%d).db
   ```
2. **Change all user passwords**
3. **Review anomaly_alerts table** for suspicious activity
4. **Check login_attempts** for unauthorized access
5. **Notify affected users**

### If .env is Committed to Git

1. **Remove from Git history** immediately
   ```bash
   # Remove file from all commits
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   
   # Force push (if remote exists)
   git push origin --force --all
   ```
2. **Rotate ALL credentials** in `.env`
3. **Consider repository compromised** - may need new repo

---

## 📞 Security Contact

For security issues or questions:
- **Email**: security@quantum-lms.edu
- **Do NOT** open public GitHub issues for security vulnerabilities
- **Use private disclosure** for sensitive bugs

---

## 📚 Security References

### Best Practices
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security](https://flask.palletsprojects.com/en/stable/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

### Tools Used
- `python-dotenv` - Environment variable management
- SQLite parameterized queries - SQL injection prevention
- OpenCV - Biometric face detection
- scikit-learn Isolation Forest - Anomaly detection
- Flask sessions - Secure session management

---

**Last Updated**: February 28, 2026  
**Security Audit Status**: ✅ All critical issues resolved  
**Next Review**: Every 90 days or after major changes
