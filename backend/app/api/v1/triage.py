"""Triage queue endpoint (ADR-006).

Deliberately not called "dashboard": this replaces the dashboard's stat
tiles with a ranked queue, and the route name should not smuggle the old
framing back in.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user, get_db, get_triage_service
from app.models.user import User
from app.schemas.triage import TriageListResponse
from app.services.triage_service import TriageService
from app.utils.responses import build_pagination

router = APIRouter()


@router.get("", response_model=TriageListResponse)
def get_triage_queue(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    triage_service: Annotated[TriageService, Depends(get_triage_service)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> TriageListResponse:
    """Return the caller's patient panel, ranked by what needs attention."""

    skip = (page - 1) * page_size
    items, total = triage_service.list_queue(db, current_user, skip, page_size)
    return TriageListResponse(
        items=items,
        pagination=build_pagination(total, page, page_size),
    )
