"""
Kavach - AI-Assisted Application Security Testing Platform
FastAPI Application Entry Point
"""

from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings

# Tag metadata for documentation grouping
tags_metadata = [
    {
        "name": "General",
        "description": "General platform information and discovery endpoints.",
    },
    {
        "name": "Health",
        "description": "Liveness and readiness health check probe endpoints.",
    },
]

# FastAPI application initialization consuming centralized settings
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    openapi_tags=tags_metadata,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
    contact={
        "name": "Kavach Security Team",
    },
    license_info={
        "name": "Proprietary / Authorized Security Testing Only",
    },
)

# Register modular API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", summary="Platform Metadata", tags=["General"])
def read_root() -> dict[str, str | bool]:
    """Root endpoint returning basic platform identification and documentation URLs."""
    return {
        "title": settings.APP_NAME,
        "description": settings.APP_DESCRIPTION,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "debug": settings.DEBUG,
        "docs": settings.DOCS_URL,
        "redoc": settings.REDOC_URL,
        "openapi": settings.OPENAPI_URL,
        "health": f"{settings.API_V1_PREFIX}/health",
        "ready": f"{settings.API_V1_PREFIX}/ready",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=(settings.DEBUG or settings.is_development),
        log_level=settings.LOG_LEVEL.lower(),
    )
