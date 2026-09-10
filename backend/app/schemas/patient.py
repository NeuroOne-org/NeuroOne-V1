"""Patient request and response schemas."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.common import PaginatedResponse
from app.schemas.user import UserResponse


class PhoneNumber(BaseModel):
    """A patient phone number."""

    model_config = ConfigDict(from_attributes=True)

    phone_number: str = Field(min_length=1, max_length=15)


class PatientBase(BaseModel):
    """Fields shared by patient request and response schemas."""

    first_name: str = Field(min_length=1, max_length=20)
    last_name: str | None = Field(default=None, min_length=1, max_length=20)
    gender: str = Field(min_length=1, max_length=1)
    dob: date
    phone: list[PhoneNumber] = Field(min_length=1)
    email: EmailStr = Field(max_length=255)
    address: str = Field(min_length=1, max_length=100)
    blood_group: str = Field(min_length=1, max_length=4)
    allergies: list[str]
    emergency_contact: str = Field(min_length=1, max_length=15)


class PatientCreate(PatientBase):
    """Payload used to create a patient."""

    doctor_id: UUID | None = None


class PatientUpdate(BaseModel):
    """Payload used to partially update a patient."""

    first_name: str | None = Field(default=None, min_length=1, max_length=20)
    last_name: str | None = Field(default=None, min_length=1, max_length=20)
    gender: str | None = Field(default=None, min_length=1, max_length=1)
    dob: date | None = None
    phone: list[PhoneNumber] | None = Field(default=None, min_length=1)
    email: EmailStr | None = Field(default=None, max_length=255)
    address: str | None = Field(default=None, min_length=1, max_length=100)
    blood_group: str | None = Field(default=None, min_length=1, max_length=4)
    allergies: list[str] | None = None
    emergency_contact: str | None = Field(
        default=None,
        min_length=1,
        max_length=15,
    )
    doctor_id: UUID | None = None


class PatientResponse(PatientBase):
    """Public patient data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    doctor_id: UUID
    doctor: UserResponse
    created_at: datetime
    updated_at: datetime


class PatientListResponse(PaginatedResponse[PatientResponse]):
    """Paginated patient collection returned by list endpoints."""


__all__ = [
    "PatientBase",
    "PatientCreate",
    "PatientListResponse",
    "PatientResponse",
    "PatientUpdate",
    "PhoneNumber",
]
