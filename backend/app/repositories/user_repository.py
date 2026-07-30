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
        return (
            db.query(User).filter(

                User.email == email,
                User.is_deleted == False,
            ).first()
        )

    def get_by_username(self, db: Session, username: str) -> User | None:
        return (
            db.query(User).filter(
                User.username == username,
                User.is_deleted == False,
            ).first()
        )

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

    def get_active_users(self, db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        return (
            db.query(User).filter(
                User.is_deleted == False,
                User.is_active == True,
            ).all()
        )
