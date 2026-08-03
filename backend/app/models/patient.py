from datetime import date
from typing import TYPE_CHECKING
import uuid

from sqlalchemy import UUID, String, Date, ForeignKey, Index
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, Base

if TYPE_CHECKING:
    from .user import User

"""
+----------------------+
|      PATIENT         |
+----------------------+
| PK id (UUID)         |
| FK doctor_id         |
| first_name           |
| last_name            |
| gender               |
| dob                  |
| phone                |
| email                |
| address              |
| blood_group          |
| allergies            |
| emergency_contact    |
| created_at           |
| updated_at           |
+----------------------+
"""
class Patient(BaseModel):
    """Patient model definitions."""
    __tablename__ = "patients"

    __table_args__ = (
        Index(
            "ix_patients_doctor_name",
            "doctor_id",
            "first_name",
            "last_name",
        ),
    )

    doctor: Mapped["User"] = relationship(
        "User",back_populates="patients", )

    # ForeignKey
    doctor_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable= False,
        index=True
    )



    # Table Specific columns
    first_name : Mapped[str] = mapped_column(
        String(20),
        nullable= False,

    )
    last_name : Mapped[ str | None] = mapped_column(String(20), nullable= True)



    gender : Mapped[str] = mapped_column(String(1), nullable= False)
    dob : Mapped[date] = mapped_column(Date, nullable= False)

    # phone |
    phone :Mapped[list["PhoneNumber"]] = relationship(
        back_populates="patient",
        cascade="all, delete-orphan" )

    # | email |
    email : Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable= False,
        index=True
    )
    # | address |
    address : Mapped[str] = mapped_column(String(100), nullable= False)
    # | blood_group |
    blood_group : Mapped[str] = mapped_column(String(4), nullable= False)
    # | allergies |
    allergies : Mapped[list[str]] = mapped_column(ARRAY(String), nullable= False)
    # | emergency_contact |
    emergency_contact : Mapped[str] = mapped_column(String(15), nullable= False)

"""
    Missing relationships
    -> appointments
    -> medical_records
    -> diagnoses
    -> symptoms
    -> reports
    -> prescriptions
"""


class PhoneNumber(Base):
    __tablename__ = "patient_phones"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str] = mapped_column(String(15))
    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patients.id"),
        nullable=False,
    )
    patient: Mapped["Patient"] = relationship(back_populates="phone")
