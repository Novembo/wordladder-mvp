---
name: fastapi-development
description: "Build or modify FastAPI applications, routers, dependencies, schemas, middleware, and OpenAPI behavior. Use when working on FastAPI: routers, dependencies, Pydantic schemas, middleware, async endpoints, OpenAPI."
---

# FastAPI Development

## Workflow
1. Inspect app creation, router registration, dependency patterns, settings, lifespan, and test setup.
2. Place endpoints in focused routers; keep HTTP concerns separate from domain/business logic.
3. Define Pydantic request/response schemas explicitly. Do not expose ORM objects or internal fields accidentally.
4. Use dependency injection for authentication, database sessions, and shared services.
5. Choose correct HTTP methods, status codes, response models, and error semantics.
6. Add async only when the full call path uses non-blocking I/O; do not call blocking libraries directly from async endpoints.
7. Add tests for success, validation errors, authorization failures, and relevant edge cases.
8. Check generated OpenAPI behavior and document non-obvious contracts.

## Rules
- Use lifespan context managers for startup/shutdown resources when appropriate.
- Keep configuration in validated settings; do not hardcode credentials.
- Scope database sessions to requests/tasks and close them reliably.
- Avoid putting business logic in route handlers.
- Use explicit response models and avoid leaking stack traces.
- Apply pagination and bounded limits to collection endpoints.
- Set timeouts for outbound HTTP calls and define safe retry/idempotency behavior.
- Do not claim an endpoint is secure merely because it requires a logged-in user.

## Verification
Run the project's tests and configured lint/type checks. If unavailable, state the missing tool or dependency and provide exact commands.
