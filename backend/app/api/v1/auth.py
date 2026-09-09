"""Authentication endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_auth_service, get_current_active_user, get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    credentials: LoginRequest,
    db: Annotated[Session, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> Token:
    """Verify username/email and password and return a signed JWT."""

    return auth_service.login(db, credentials.username, credentials.password)


@router.get("/me", response_model=UserResponse)
def read_current_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserResponse:
    """Return the identity associated with the bearer token."""

    return current_user
