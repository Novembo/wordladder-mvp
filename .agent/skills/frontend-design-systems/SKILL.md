---
name: frontend-design-systems
description: "Create reusable accessible design systems with tokens, component contracts, theming, and documentation. Use when standardizing UI components across pages or applications."
---

# Frontend Design Systems

## Workflow
1. Audit existing UI patterns and identify repeated components and inconsistent tokens.
2. Define semantic design tokens for color, spacing, typography, radii, elevation, and motion.
3. Specify component API, states, variants, keyboard behavior, responsive behavior, and accessibility requirements.
4. Build primitives before complex composed components; avoid one-off props without a clear use case.
5. Document usage, anti-patterns, and examples in a living component catalog.
6. Version breaking changes and provide migration guidance.

## Rules
- Prefer semantic tokens over hard-coded values scattered through components.
- Do not encode product-specific business logic in generic UI primitives.
- Ensure focus, hover, disabled, error, loading, and reduced-motion states are designed.
- Avoid inaccessible color-only status indicators.
- Test components in real consuming contexts.

## Verification
Use visual regression, accessibility checks, responsive testing, and consumer feedback.
