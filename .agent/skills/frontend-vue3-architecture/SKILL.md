---
name: frontend-vue3-architecture
description: "Structure scalable Vue 3 applications using Composition API, composables, Pinia, routing, and component boundaries. Use when building or refactoring Vue 3 applications."
---

# Vue 3 Application Architecture

## Workflow
1. Inspect Vue version, build tool, router, state library, TypeScript mode, and existing conventions.
2. Organize by feature/domain where useful; keep route pages, reusable UI, composables, API clients, and domain types distinct.
3. Use `<script setup>` and Composition API consistently; extract composables around reusable behavior, not every few lines.
4. Keep server state, URL state, and local UI state separate; use Pinia only for genuinely shared client state.
5. Define typed API boundaries and normalize errors in one integration layer.
6. Use route-level code splitting, accessible forms, and explicit loading/empty/error states.
7. Test components, composables, routing, and critical user journeys.

## Rules
- Avoid giant components and global stores for page-local state.
- Do not duplicate backend business rules in the UI as an authorization mechanism.
- Avoid watchers when derived computed state or direct event handling is clearer.
- Keep secrets out of client bundles.
- Preserve keyboard and screen-reader behavior.

## Verification
Run type checks, lint, unit/component tests, E2E tests, and production build.
