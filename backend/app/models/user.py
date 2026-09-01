from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum
from app.models.base import BaseModel

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Boolean,
    String,
    Index,
)

if TYPE_CHECKING:
    from app.models.patient import Patient


class UserRole(str, Enum):
    DOCTOR = "doctor"
    ADMIN = "admin"
    RECEPTIONIST = "receptionist"
    RESEARCHER = "researcher"

class User(BaseModel):
    """User model definitions."""

    __tablename__ = "users"
    __table_args__ = (
        Index(
            "ix_users_name",
            "last_name",
            "first_name",
        ),
    )
    patients: Mapped[list["Patient"]] = relationship("Patient", back_populates="doctor")
    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)

    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole),
        default=UserRole.DOCTOR,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )