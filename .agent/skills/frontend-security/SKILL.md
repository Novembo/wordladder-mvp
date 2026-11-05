---
name: frontend-security
description: "Prevent browser-side security issues and integrate safely with backend authentication and APIs. Use for XSS, CSRF, token storage, CSP, unsafe HTML rendering, or browser-side auth issues."
---

# Frontend Security

## Threat areas
Review XSS, CSRF, clickjacking, unsafe redirects, token storage, dependency risks, source maps, CORS assumptions, and sensitive data exposure.

## Rules
- Treat all API responses, URL parameters, and user content as untrusted.
- Avoid `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, and equivalent sinks for untrusted content.
- Prefer secure, HttpOnly, SameSite cookies for browser sessions when architecture supports them; evaluate CSRF protections.
- Do not store long-lived secrets or privileged API keys in localStorage or frontend bundles.
- Do not put authorization decisions only in the UI.
- Use a restrictive Content Security Policy where feasible.
- Validate redirect destinations against allowlists.
- Keep dependencies patched and review supply-chain changes.
