"""Tests for soft-delete semantics and transactional failure handling."""

from unittest.mock import Mock
from uuid import uuid4

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import String, create_engine, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, Session, mapped_column
from sqlalchemy.pool import StaticPool

from app.models.base import BaseModel
from app.repositories.base_repository import BaseRepository
from app.utils.handlers import register_exception_handlers
from app.utils.exceptions import DatabaseError


class RepositoryRecord(BaseModel):
    __tablename__ = "test_repository_records"

    name: Mapped[str] = mapped_column(String(50), nullable=False)


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    RepositoryRecord.__table__.create(engine)
    return Session(engine)


def test_soft_deleted_records_are_hidden_unless_explicitly_requested() -> None:
    repository = BaseRepository(RepositoryRecord)
    with _session() as db:
        record = repository.create(db, RepositoryRecord(name="visible"))
        repository.soft_delete(db, record)

        assert record.deleted_at is not None
        assert repository.get_by_id(db, record.id) is None
        assert repository.get_all(db) == []
        assert not repository.exists(db, record.id)
        assert repository.get_by_id(db, record.id, include_deleted=True) is record
        assert repository.get_all(db, include_deleted=True) == [record]
        assert repository.exists(db, record.id, include_deleted=True)


def test_create_rolls_back_and_raises_controlled_database_error() -> None:
    repository = BaseRepository(RepositoryRecord)
    db = Mock()
    db.commit.side_effect = SQLAlchemyError("private database details")

    try:
        repository.create(db, RepositoryRecord(id=uuid4(), name="failure"))
    except DatabaseError as exc:
        assert str(exc) == "Unable to create record."
    else:
        raise AssertionError("DatabaseError was not raised")

    db.rollback.assert_called_once_with()


def test_mid_write_failure_persists_nothing_and_translates_database_error() -> None:
    secret = "private database exception detail"
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    RepositoryRecord.__table__.create(engine)
    repository = BaseRepository(RepositoryRecord)
    test_app = FastAPI()
    register_exception_handlers(test_app)

    @test_app.post("/write")
    def write_record():
        with Session(engine) as db:
            def fail_after_flush() -> None:
                db.flush()
                raise SQLAlchemyError(secret)

            db.commit = fail_after_flush
            return repository.create(db, RepositoryRecord(name="must-rollback"))

    response = TestClient(test_app, raise_server_exceptions=False).post("/write")

    assert response.status_code == 503
    assert response.json() == {
        "message": "Unable to create record.",
        "error_code": "database_error",
        "details": None,
    }
    assert secret not in response.text
    with Session(engine) as verification_db:
        persisted = verification_db.scalar(
            select(func.count()).select_from(RepositoryRecord)
        )
    assert persisted == 0
