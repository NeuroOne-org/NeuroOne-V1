"""Fixtures for the Postgres-marked suite (ADR-007 Testing Impact, AI-02b-8).

Every test under `tests/postgres/` exercises real SQL -- `ts_rank_cd`, the
generated `search_vector` column, the tier `CHECK` constraint -- that
SQLite cannot represent, so the fast suite never runs it. Each test module
sets its own `pytestmark = pytest.mark.postgres` (a module-level
`pytestmark` in `conftest.py` does not propagate to sibling test modules),
and the `pg_session` fixture below skips every test unless
`TEST_POSTGRES_URL` is set; CI always sets it (see
`.github/workflows/backend-tests.yml`).

Each test gets its own Postgres *schema* -- not a whole database, which
would need superuser-level `CREATE DATABASE` privileges CI's Postgres
service user may not have -- migrated to head with the project's own
Alembic config, so this suite tests the real migration rather than a
hand-rolled equivalent, and drops it afterward.
"""

import os
import uuid
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker


TEST_POSTGRES_URL = os.environ.get("TEST_POSTGRES_URL")

BACKEND_DIR = Path(__file__).resolve().parents[2]


@pytest.fixture()
def pg_session() -> Session:
    if not TEST_POSTGRES_URL:
        pytest.skip("TEST_POSTGRES_URL is not set; skipping the Postgres suite")

    schema = f"test_{uuid.uuid4().hex[:12]}"

    admin_engine = create_engine(TEST_POSTGRES_URL)
    with admin_engine.begin() as conn:
        conn.execute(text(f'CREATE SCHEMA "{schema}"'))

    # psycopg2 accepts libpq connection options via the `options` query
    # parameter; this sets search_path for every connection this engine
    # opens, so the migration and the test both land in the fresh schema
    # without any test code needing to know the schema name.
    schema_url = f"{TEST_POSTGRES_URL}?options=-csearch_path%3D{schema}"

    config = Config(str(BACKEND_DIR / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", schema_url)
    command.upgrade(config, "head")

    engine = create_engine(schema_url)
    session = sessionmaker(bind=engine)()

    try:
        yield session
    finally:
        session.close()
        engine.dispose()
        with admin_engine.begin() as conn:
            conn.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        admin_engine.dispose()
