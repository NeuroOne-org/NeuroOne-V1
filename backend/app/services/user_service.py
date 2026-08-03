"""Business logic for user management."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.base_service import BaseService


class UserService(BaseService[UserRepository]):
    """Business logic for user management."""

    def __init__(self, repository: UserRepository):
        super().__init__(repository)

    def create_user(
        self,
        db: Session,
        user_data: UserCreate,
        *,
        hashed_password: str,
    ) -> User:
        """Create a new user."""

        user_values = user_data.model_dump(exclude={"password"})
        user = User(
            **user_values,
            hashed_password=hashed_password,
        )

        return self.repository.create(db, user)

    def get_user(
        self,
        db: Session,
        user_id: UUID,
    ) -> User | None:
        """Retrieve a user by ID."""

        return self.repository.get_by_id(db, user_id)

    def list_users(self, db: Session) -> list[User]:
        """Retrieve all users."""

        return self.repository.get_all(db)

    def update_user(
        self,
        db: Session,
        user_id: UUID,
        user_data: UserUpdate,
    ) -> User | None:
        """Update an existing user."""

        user = self.repository.get_by_id(db, user_id)

        if user is None:
            return None

        update_data = user_data.model_dump(
            exclude_unset=True,
            exclude={"password"},
        )

        for field, value in update_data.items():
            setattr(user, field, value)

        return self.repository.update(db, user)

    def delete_user(self, db: Session, user_id: UUID) -> bool:
        """Soft-delete a user."""

        user = self.repository.get_by_id(db, user_id)

        if user is None:
            return False

        self.repository.soft_delete(db, user)

        return True

    def get_user_by_email(
        self,
        db: Session,
        email: str,
    ) -> User | None:
        """Retrieve a user by email."""

        return self.repository.get_by_email(db, email)

    def get_user_by_username(
        self,
        db: Session,
        username: str,
    ) -> User | None:
        """Retrieve a user by username."""

        return self.repository.get_by_username(db, username)
