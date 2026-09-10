"""Regression tests for the deleted_at timezone migration."""

from importlib import util
from pathlib import Path
from types import ModuleType

import sqlalchemy as sa


MIGRATION_PATH = (
    Path(__file__).resolve().parents[1]
    / "alembic"
    / "versions"
    / "b8d41e2f7c53_make_deleted_at_timezone_aware.py"
)
TARGET_TABLES = ("users", "patients", "patient_phones")


def _load_migration() -> ModuleType:
    spec = util.spec_from_file_location("deleted_at_timezone_migration", MIGRATION_PATH)
    assert spec is not None and spec.loader is not None
    migration = util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    return migration


def test_migration_chains_from_case_01() -> None:
    migration = _load_migration()

    assert migration.revision == "b8d41e2f7c53"
    assert migration.down_revision == "a3c7be51d904"


def test_upgrade_uses_implicit_timezone_cast(monkeypatch) -> None:
    migration = _load_migration()
    calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
    monkeypatch.setattr(
        migration.op,
        "alter_column",
        lambda *args, **kwargs: calls.append((args, kwargs)),
    )

    migration.upgrade()

    assert [args[0] for args, _ in calls] == list(TARGET_TABLES)
    for args, kwargs in calls:
        assert args[1] == "deleted_at"
        assert isinstance(kwargs["existing_type"], sa.DateTime)
        assert kwargs["existing_type"].timezone is False
        assert isinstance(kwargs["type_"], sa.DateTime)
        assert kwargs["type_"].timezone is True
        assert kwargs["existing_nullable"] is True
        assert "postgresql_using" not in kwargs


def test_downgrade_restores_naive_timestamps(monkeypatch) -> None:
    migration = _load_migration()
    calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
    monkeypatch.setattr(
        migration.op,
        "alter_column",
        lambda *args, **kwargs: calls.append((args, kwargs)),
    )

    migration.downgrade()

    assert [args[0] for args, _ in calls] == list(TARGET_TABLES)
    for args, kwargs in calls:
        assert args[1] == "deleted_at"
        assert isinstance(kwargs["existing_type"], sa.DateTime)
        assert kwargs["existing_type"].timezone is True
        assert isinstance(kwargs["type_"], sa.DateTime)
        assert kwargs["type_"].timezone is False
        assert kwargs["existing_nullable"] is True
        assert "postgresql_using" not in kwargs
