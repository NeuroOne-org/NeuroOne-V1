"""
Generic repository providing reusable CRUD operations.

This base repository implements common database operations shared across
all application models. Feature-specific repositories should inherit from
this class and extend it with custom query methods.
"""
from typing import Generic, TypeVar, Type
from uuid import UUID

from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from app.models.base import BaseModel


ModelType = TypeVar("ModelType", bound=BaseModel)


class EntityNotFoundError(Exception):
    pass


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model


    def create(self, db:Session, obj:ModelType) -> ModelType:
        """Create a new database record and persist it.

        Adds the model instance to the session, commits the transaction,
        refreshes the object from the database, and returns the persisted entity.
        """
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj


    def get_by_id(self, db:Session, obj_id:UUID) -> ModelType | None:
        """Retrieve a single record by its unique identifier.

        Returns the entity if it exists and is not soft-deleted;
        otherwise returns None.
        """
        return db.query(self.model).filter(self.model.id == obj_id).first()

    def get_or_404(self, db: Session, obj_id: UUID) -> ModelType:
        obj = self.get_by_id(db, obj_id)
        if obj is None:
            raise EntityNotFoundError(...)
        return obj

    def get_all(self, db:Session, skip:int = 0, limit:int = 100) -> list[ModelType]:
        """Retrieve all active records.

        Returns a list of all entities that have not been soft-deleted.
        Supports pagination through skip and limit parameters.
        """
        return db.query(self.model).all()

    def update(self,db:Session, obj: ModelType) -> ModelType:
        """Persist changes made to an existing entity.

        Commits the current transaction, refreshes the entity from the database,
        and returns the updated instance.
        """
        db.commit()
        db.refresh(obj)
        return obj


    def soft_delete(self, db:Session, obj: ModelType):
        """Soft-delete an entity.

        Marks the entity as deleted by setting the `is_deleted` flag to True
        instead of permanently removing it from the database.
        """
        obj.soft_delete()
        db.commit()

    def exists(
            self,
            db: Session,
            obj_id: UUID,
    ) -> bool:
        """Check whether a record exists.

                Returns True if an active record with the given identifier exists;
                otherwise returns False.
                """
        return db.query(
            exists().where(self.model.id == obj_id)
        ).scalar()

