"""User request and response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import UserRole


class UserBase(BaseModel):
    """Fields shared by user create and response schemas."""

    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=255)


class UserCreate(UserBase):
    """Payload used to register a user."""

    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """Payload used to partially update a user."""

    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    role: UserRole | None = None
    is_active: bool | None = None
    is_verified: bool | None = None



class UserResponse(UserBase):
    """Public user data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


__all__ = [
    "UserBase",
    "UserCreate",
    "UserResponse",
    "UserUpdate",
]