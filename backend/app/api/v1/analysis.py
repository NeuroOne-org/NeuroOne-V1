"""Analysis item endpoints.

Flat rather than nested under the visit: an analysis id is globally unique, so
carrying the visit id would be redundant. Collection and trigger endpoints live
in visits.py, where the case is the natural parent.

An analysis reached by its own id gets a 404 labelled "Analysis" even when the
real cause is that its parent visit belongs to another clinician -- otherwise
the visit's UUID would leak (ADR-002, applied one level deeper).
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_analysis_service,
    get_current_active_user,
    get_db,
)
from app.models.analysis import Analysis
from app.models.user import User
from app.schemas.analysis import AnalysisResponse
from app.services.analysis_service import AnalysisService

router = APIRouter()


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    analysis_service: Annotated[AnalysisService, Depends(get_analysis_service)],
) -> Analysis:
    """Retrieve one analysis. Ownership violations read as 404."""

    return analysis_service.get_analysis(db, analysis_id, current_user)
