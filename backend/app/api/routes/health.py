"""
Health and readiness probe endpoints for Kavach.
"""

from typing import Dict
from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.core.config import settings

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Schema for basic application liveness health check."""

    status: str = Field(default="healthy", description="Application operational status")
    app: str = Field(default=settings.APP_NAME, description="Application name")
    app_name: str = Field(default=settings.APP_NAME, description="Application name alias")
    version: str = Field(default=settings.APP_VERSION, description="Application API version")
    environment: str = Field(default=settings.APP_ENV, description="Active runtime environment")


class DependencyStatus(BaseModel):
    """Schema for individual external dependency status."""

    status: str = Field(description="Dependency status (e.g., connected, unconfigured, unavailable)")
    required: bool = Field(description="Whether this dependency is strictly required for basic operation")
    details: str = Field(description="Descriptive explanation or connection details")


class ReadinessResponse(BaseModel):
    """Schema for application readiness probe."""

    status: str = Field(default="ready", description="Overall readiness status")
    ready: bool = Field(default=True, description="Boolean flag indicating if API is ready to accept traffic")
    app: str = Field(default=settings.APP_NAME, description="Application name")
    version: str = Field(default=settings.APP_VERSION, description="Application API version")
    dependencies: Dict[str, DependencyStatus] = Field(
        description="Status breakdown of external downstream dependencies"
    )


def check_firestore_readiness() -> DependencyStatus:
    """
    Check Firestore connection readiness.

    Note: Firestore persistence is planned for Phase 2. Currently marked as unconfigured
    so readiness checks accurately reflect external dependency status without false claims.
    """
    return DependencyStatus(
        status="unconfigured",
        required=False,
        details="Firestore integration planned for Phase 2; not initialized.",
    )


def check_redis_readiness() -> DependencyStatus:
    """
    Check Redis connection readiness.

    Note: Redis task broker/cache is planned for Phase 3. Currently marked as unconfigured
    so readiness checks accurately reflect external dependency status without false claims.
    """
    return DependencyStatus(
        status="unconfigured",
        required=False,
        details="Redis task broker/cache planned for Phase 3; not initialized.",
    )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Application Health Check",
    description="Basic liveness check verifying the FastAPI application process is up and running.",
)
def get_health() -> HealthResponse:
    """Return process liveness status without dependency on external services."""
    return HealthResponse(
        status="healthy",
        app=settings.APP_NAME,
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.APP_ENV,
    )


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    summary="Application Readiness Check",
    description="Readiness probe verifying the application is ready to accept incoming HTTP requests.",
)
def get_readiness() -> ReadinessResponse:
    """
    Return application readiness status.

    Clearly distinguishes core application readiness from external service dependencies.
    """
    dependencies = {
        "firestore": check_firestore_readiness(),
        "redis": check_redis_readiness(),
    }

    # Core API is ready to accept incoming requests. External services will be evaluated
    # in subsequent phases as their connections are implemented and configured.
    return ReadinessResponse(
        status="ready",
        ready=True,
        app=settings.APP_NAME,
        version=settings.APP_VERSION,
        dependencies=dependencies,
    )
