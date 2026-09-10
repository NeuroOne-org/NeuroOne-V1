---
type: "query"
date: "2026-09-10T13:07:46.702176+00:00"
question: "How are Alembic migrations and backend tests configured, and where should PR CI run pytest?"
contributor: "graphify"
outcome: "useful"
source_nodes: ["b8d41e2f7c53_make_deleted_at_timezone_aware.py", "backend/requirements-dev.txt — Test Dependencies (pytest, pytest-asyncio, httpx)", "Alembic Migration Policy"]
---

# Q: How are Alembic migrations and backend tests configured, and where should PR CI run pytest?

## Answer

Expanded from original query via graph vocabulary: [alembic, migration, migrations, deleted, timezone, timestamptz, backend, pytest, tests, requirements]. The repository graph identified b8d41e2f7c53 as the deleted_at timezone migration, a3c7be51d904 as its required predecessor, backend/requirements-dev.txt as the test dependency manifest, and TRD section 12 as the automated-test contract. Source inspection confirmed CI should install from backend/requirements-dev.txt, validate the single Alembic head, and run pytest from backend.

## Outcome

- Signal: useful

## Source Nodes

- b8d41e2f7c53_make_deleted_at_timezone_aware.py
- backend/requirements-dev.txt — Test Dependencies (pytest, pytest-asyncio, httpx)
- Alembic Migration Policy