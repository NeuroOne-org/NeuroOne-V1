"""
Generic repository providing reusable CRUD operations.

This base repository implements common database operations shared across
all application models. Feature-specific repositories should inherit from
this class and extend it with custom query methods.
"""
from typing import Generic, TypeVar, Type
from uuid import UUID

from sqlalchemy import exists, func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.base import BaseModel
from app.utils.exceptions import ConflictError, DatabaseError, EntityNotFoundError


ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model


    def create(self, db:Session, obj:ModelType) -> ModelType:
        """Create a new database record and persist it.

        Adds the model instance to the session, commits the transaction,
        refreshes the object from the database, and returns the persisted entity.
        """
        try:
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj
        except IntegrityError as exc:
            db.rollback()
            raise ConflictError("Record conflicts with existing data.") from exc
        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseError("Unable to create record.") from exc


    def get_by_id(
        self,
        db: Session,
        obj_id: UUID,
        *,
        include_deleted: bool = False,
    ) -> ModelType | None:
        """Retrieve a single record by its unique identifier.

        Returns the entity if it exists and is not soft-deleted;
        otherwise returns None.
        """
        statement = select(self.model).where(self.model.id == obj_id)
        if not include_deleted:
            statement = statement.where(self.model.is_deleted.is_(False))
        return db.scalar(statement)

    def get_or_404(self, db: Session, obj_id: UUID) -> ModelType:
        obj = self.get_by_id(db, obj_id)
        if obj is None:
            raise EntityNotFoundError(self.model.__name__, obj_id)
        return obj

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        *,
        include_deleted: bool = False,
    ) -> list[ModelType]:
        """Retrieve all active records.

        Returns a list of all entities that have not been soft-deleted.
        Supports pagination through skip and limit parameters.
        """
        statement = select(self.model)
        if not include_deleted:
            statement = statement.where(self.model.is_deleted.is_(False))
        statement = statement.offset(skip).limit(limit)
        return list(db.scalars(statement).all())

    def count(self, db: Session, *, include_deleted: bool = False) -> int:
        """Count records, excluding soft-deleted rows by default."""
        statement = select(func.count()).select_from(self.model)
        if not include_deleted:
            statement = statement.where(self.model.is_deleted.is_(False))
        return db.scalar(statement) or 0

    def update(self,db:Session, obj: ModelType) -> ModelType:
        """Persist changes made to an existing entity.

        Commits the current transaction, refreshes the entity from the database,
        and returns the updated instance.
        """
        try:
            db.commit()
            db.refresh(obj)
            return obj
        except IntegrityError as exc:
            db.rollback()
            raise ConflictError("Record conflicts with existing data.") from exc
        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseError("Unable to update record.") from exc


    def soft_delete(self, db:Session, obj: ModelType):
        """Soft-delete an entity.

        Marks the entity as deleted by setting the `is_deleted` flag to True
        instead of permanently removing it from the database.
        """
        obj.soft_delete()
        try:
            db.commit()
            db.refresh(obj)
            return obj
        except SQLAlchemyError as exc:
            db.rollback()
            raise DatabaseError("Unable to delete record.") from exc

    def exists(
            self,
            db: Session,
            obj_id: UUID,
            *,
            include_deleted: bool = False,
    ) -> bool:
        """Check whether a record exists.

                Returns True if an active record with the given identifier exists;
                otherwise returns False.
                """
        criteria = [self.model.id == obj_id]
        if not include_deleted:
            criteria.append(self.model.is_deleted.is_(False))
        return bool(db.scalar(select(exists().where(*criteria))))
