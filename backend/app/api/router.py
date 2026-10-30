"""API router aggregating modular routes."""

from fastapi import APIRouter
from app.api.routes import health

api_router = APIRouter()

# Include health and readiness probe routes
api_router.include_router(health.router)
