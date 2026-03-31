---
name: omx-security-review
description: >-
  Comprehensive security audit checking for OWASP Top 10 vulnerabilities, hardcoded secrets, and unsafe patterns, adapted for Cursor agent use
---
# Security Review (ported from OmX $security-review)

## Purpose
Conduct a thorough security audit checking for OWASP Top 10 vulnerabilities, hardcoded secrets, and unsafe patterns across the codebase.

## When to Use
- User requests "security review" or "security audit"
- After writing code that handles user input
- After adding new API endpoints
- After modifying authentication/authorization logic
- Before deploying to production
- After adding external dependencies

## When Not to Use
- Low-risk utility code with no user input handling
- Well-audited patterns that have existing security tests
- Code with no external surface area

## Workflow

### 1. OWASP Top 10 Scan
- A01: Broken Access Control
- A02: Cryptographic Failures
- A03: Injection (SQL, NoSQL, Command, XSS)
- A04: Insecure Design
- A05: Security Misconfiguration
- A06: Vulnerable and Outdated Components
- A07: Identification and Authentication Failures
- A08: Software and Data Integrity Failures
- A09: Security Logging and Monitoring Failures
- A10: Server-Side Request Forgery (SSRF)

### 2. Secrets Detection
- Hardcoded API keys
- Passwords in source code
- Private keys in repo
- Tokens and credentials
- Connection strings with secrets

### 3. Input Validation
- All user inputs sanitized
- SQL/NoSQL injection prevention
- Command injection prevention
- XSS prevention (output escaping)
- Path traversal prevention

### 4. Authentication/Authorization
- Proper password hashing (bcrypt, argon2)
- Session management security
- Access control enforcement
- JWT implementation security

### 5. Dependency Security
- Run `npm audit` (or equivalent) for known vulnerabilities
- Check for outdated dependencies
- Identify high-severity CVEs

## Tools

- **Grep tool**: Search for hardcoded secrets, unsafe patterns, and vulnerability indicators across the codebase
- **Read tool**: Read source files for detailed security analysis
- **Shell tool**: Run `npm audit`, dependency checks, and other security scanning commands
- **ReadLints tool**: Check for linter-detected security issues
- **Task tool (subagent)**: Delegate specialized security analysis to focused subagents for parallel review of different vulnerability categories

## Rules

- Default to concise, evidence-dense progress and completion reporting unless the user or risk level requires more detail.
- If correctness depends on additional inspection, retrieval, execution, or verification, keep using the relevant tools until the security review is grounded.
- Continue through clear, low-risk, reversible next steps automatically; ask only when the next step is materially branching, destructive, or preference-dependent.
- Form your OWN security analysis FIRST before any cross-validation.
- Never block the review if any single tool is unavailable — gracefully fall back.
- Consider consulting additional resources for CRITICAL/HIGH findings.

## Output Format

```
SECURITY REVIEW REPORT
======================

Scope: [files/modules scanned]
Scan Date: [timestamp]

CRITICAL (N)
------------
1. file:line - Finding Title
   Finding: [description]
   Impact: [severity explanation]
   Remediation: [fix guidance]
   Reference: OWASP [category]

HIGH (N)
--------
...

MEDIUM (N)
----------
...

LOW (N)
-------
...

DEPENDENCY VULNERABILITIES
--------------------------
[npm audit / pip audit results]

OVERALL ASSESSMENT
------------------
Security Posture: [GOOD/FAIR/POOR]

Immediate Actions Required:
1. [action]
2. [action]

Recommendation: [deploy/do not deploy guidance]
```

## Checklist

### Authentication & Authorization
- [ ] Passwords hashed with strong algorithm (bcrypt/argon2)
- [ ] Session tokens cryptographically random
- [ ] JWT tokens properly signed and validated
- [ ] Access control enforced on all protected resources
- [ ] No authentication bypass vulnerabilities

### Input Validation
- [ ] All user inputs validated and sanitized
- [ ] SQL queries use parameterization (no string concatenation)
- [ ] NoSQL queries prevent injection
- [ ] File uploads validated (type, size, content)
- [ ] URLs validated to prevent SSRF

### Output Encoding
- [ ] HTML output escaped to prevent XSS
- [ ] JSON responses properly encoded
- [ ] No user data in error messages
- [ ] Content-Security-Policy headers set

### Secrets Management
- [ ] No hardcoded API keys
- [ ] No passwords in source code
- [ ] No private keys in repo
- [ ] Environment variables used for secrets
- [ ] Secrets not logged or exposed in errors

### Cryptography
- [ ] Strong algorithms used (AES-256, RSA-2048+)
- [ ] Proper key management
- [ ] Random number generation cryptographically secure
- [ ] TLS/HTTPS enforced for sensitive data

### Dependencies
- [ ] No known vulnerabilities in dependencies
- [ ] Dependencies up to date
- [ ] No CRITICAL or HIGH CVEs
- [ ] Dependency sources verified

## Appendix

### Severity Definitions
- **CRITICAL** — Exploitable vulnerability with severe impact (data breach, RCE, credential theft)
- **HIGH** — Vulnerability requiring specific conditions but serious impact
- **MEDIUM** — Security weakness with limited impact or difficult exploitation
- **LOW** — Best practice violation or minor security concern

### Remediation Priority
1. **Rotate exposed secrets** — Immediate (within 1 hour)
2. **Fix CRITICAL** — Urgent (within 24 hours)
3. **Fix HIGH** — Important (within 1 week)
4. **Fix MEDIUM** — Planned (within 1 month)
5. **Fix LOW** — Backlog (when convenient)

### Best Practices
- **Review early** — Security by design, not afterthought
- **Review often** — Every major feature or API change
- **Automate** — Run security scans in CI/CD pipeline
- **Fix immediately** — Don't accumulate security debt
- **Educate** — Learn from findings to prevent future issues
- **Verify fixes** — Re-run security review after remediation
