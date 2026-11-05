---
name: alembic-migrations
description: "Create safe, reviewable Alembic migrations with autogeneration checks, data migrations, and production rollout strategy. Use when changing SQLAlchemy schemas or deploying database changes."
---

# Alembic Migrations

## Workflow
1. Inspect `env.py`, metadata imports, naming conventions, version table, and deployment migration command.
2. Generate a candidate revision, then manually review every operation; autogenerate is not authoritative.
3. Separate schema changes from large data backfills when lock duration or deploy safety matters.
4. Use expand-and-contract for changes that must coexist with old and new application versions.
5. Add indexes concurrently where supported and account for database-specific transaction restrictions.
6. Make data migrations bounded, resumable, observable, and safe to rerun where possible.
7. Define rollback or forward-fix strategy before production execution.

## Rules
- Never edit an already-applied migration in shared environments.
- Never drop/rename a production column in the same release that first stops using it.
- Avoid loading entire tables into Python for large backfills.
- Do not run migrations from every application worker at startup.
- Test upgrade from the previous schema and downgrade only when downgrade is genuinely supported.

## Verification
Run migrations against an empty database and a representative prior revision; inspect locks, execution time, and resulting schema.
