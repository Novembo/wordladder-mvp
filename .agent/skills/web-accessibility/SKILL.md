---
name: web-accessibility
description: "Audit and implement accessible web experiences aligned with WCAG principles. Use for WCAG audits, keyboard navigation, ARIA, screen reader support, contrast, or accessible components."
---

# Web Accessibility

## Audit workflow
1. Identify user journeys and test keyboard-only operation.
2. Verify semantic landmarks, heading order, labels, names, roles, and states.
3. Check focus order, visible focus, dialogs, menus, and keyboard escape behavior.
4. Check contrast, zoom/reflow, text alternatives, captions, and reduced motion.
5. Test screen-reader announcements for validation, async updates, and errors.
6. Use automated tools as assistance, not as proof of conformance.
7. Record issues with impact, reproduction, and remediation.

## Rules
- Prefer native HTML semantics.
- Every control needs an accessible name and clear purpose.
- Do not use positive tabindex to force focus order.
- Manage focus when opening/closing dialogs and route transitions.
- Ensure errors are associated with fields and announced.
- Do not claim WCAG compliance based only on automated scans.
