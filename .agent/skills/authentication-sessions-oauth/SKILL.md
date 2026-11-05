---
name: authentication-sessions-oauth
description: "Implement authentication correctly: password hashing, sessions vs tokens, OAuth2/OIDC with PKCE, MFA, reset flows, and account-enumeration defenses. Use when building login, signup, SSO, password reset, or reviewing auth security."
---

# Authentication, Sessions, and OAuth

## Passwords
- Hash with Argon2id (or bcrypt/scrypt/PBKDF2 where required) using parameters from the current OWASP Password Storage Cheat Sheet. Never encrypt or store plain passwords; never log them.
- Enforce length (support long passphrases), check against breached-password lists, no arbitrary composition rules, allow password managers (no paste blocking).
- Rate limit and progressively delay login attempts per account and per IP; alert on credential-stuffing patterns.

## Sessions vs tokens
- Browser apps: server-side sessions in `HttpOnly`, `Secure`, `SameSite=Lax/Strict` cookies, plus CSRF protection for state-changing requests.
- APIs/mobile: short-lived access tokens + rotating refresh tokens with reuse detection; store on mobile in Keychain/Keystore, never in plain storage or URLs.
- Regenerate the session ID on login and privilege change; support logout and server-side revocation.

## OAuth2 / OIDC
- Use Authorization Code flow with PKCE for public clients and web apps. Do not use implicit or password grants.
- Validate `state`, `nonce`, `iss`, `aud`, expiry, and signature (via JWKS); exact-match redirect URIs.
- Prefer a vetted library or identity provider over custom protocol code.

## Account flows
- Password reset and email verification: single-use, high-entropy, expiring tokens stored hashed; identical responses whether or not the account exists.
- Offer MFA (TOTP/WebAuthn passkeys); require re-authentication for sensitive actions (email, password, payout changes).
- Notify users of new-device logins and credential changes.

## Verify
Test brute-force limits, token expiry/reuse, session fixation, logout invalidation, and that authorization is enforced separately from authentication.
