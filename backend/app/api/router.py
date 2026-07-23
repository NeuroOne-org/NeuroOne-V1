"""Top-level API router."""

from fastapi import APIRouter

from app.api.v1 import auth, diagnosis, patients, rag, reports, visits

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(visits.router, prefix="/visits", tags=["visits"])
api_router.include_router(diagnosis.router, prefix="/diagnosis", tags=["diagnosis"])
api_router.include_router(rag.router, prefix="/rag", tags=["rag"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
