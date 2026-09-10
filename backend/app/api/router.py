"""Top-level API router."""

from fastapi import APIRouter

from app.api.v1 import (
    admin,
    analysis,
    auth,
    patient_visits,
    patients,
    reports,
    visits,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(patient_visits.router, prefix="/patients", tags=["visits"])
api_router.include_router(visits.router, prefix="/visits", tags=["visits"])
api_router.include_router(analysis.router, prefix="/analyses", tags=["analysis"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
