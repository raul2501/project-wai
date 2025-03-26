"""
API module for Wai project.
"""
from fastapi import APIRouter

from backend.api.documents import router as document_router

# Create main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(document_router, prefix="/documents", tags=["documents"])