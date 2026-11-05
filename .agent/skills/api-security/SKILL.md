---
name: api-security
description: "Audit or implement API security controls including validation, authorization, rate limiting, and secure error handling. Use when securing an API: input validation, authorization checks, rate limiting, CORS, error leakage, or a security audit."
---

# API Security Audit

## Threat review
- Identify assets, trust boundaries, actors, entry points, and sensitive data.
- Check authentication separately from authorization.
- Verify object-level and function-level authorization on every sensitive operation.
- Validate input with allowlists, length/range limits, and safe parsing.
- Review injection, SSRF, path traversal, mass assignment, insecure file uploads, CORS, CSRF, and unsafe redirects as applicable.
- Check rate limiting, brute-force protection, abuse controls, and resource limits.
- Review secrets, logs, error responses, TLS assumptions, and dependency exposure.

## Implementation rules
- Deny by default; grant least privilege.
- Enforce permissions server-side, not in the frontend.
- Avoid leaking stack traces, tokens, passwords, or personal data.
- Use parameterized database access and safe outbound URL validation.
- Store passwords with a modern password-hashing algorithm via a maintained library.
- Rotate/revoke credentials safely; use short-lived access tokens where appropriate.
- Do not invent compliance claims or guarantee security.

## Output
List verified findings, severity, exploit preconditions, impact, remediation, and tests needed. Clearly label unverified assumptions.
