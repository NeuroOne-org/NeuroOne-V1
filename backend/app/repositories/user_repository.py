from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base_repository import BaseRepository

"""Repository for user-related database operations.

Provides user-specific queries in addition to the generic CRUD
operations inherited from BaseRepository.
"""
class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(
        self,
        db: Session,
        email: str,
    ) -> User | None:
        statement = select(User).where(
            User.email == email,
            User.is_deleted.is_(False),
        )
        return db.scalar(statement)

    def get_by_username(self, db: Session, username: str) -> User | None:
        statement = select(User).where(
            User.username == username,
            User.is_deleted.is_(False),
        )
        return db.scalar(statement)

    def exists_email(self, db:Session, email:str) -> bool:
        return (
            db.query(User).filter(
                User.email == email,
                User.is_deleted == False,
            ).first() is not None
        )

    def exists_username(self, db:Session, username:str) -> bool:
        return (
        db.query(User).filter(
            User.username == username,
            User.is_deleted == False,
        ).first() is not None
        )

    def get_active_users(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[User]:
        statement = (
            select(User)
            .where(
                User.is_deleted.is_(False),
                User.is_active.is_(True),
            )
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(statement).all())
