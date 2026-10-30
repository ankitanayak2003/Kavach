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

# FastAPI application initialization with comprehensive metadata
app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Kavach is an AI-assisted application security testing platform designed "
        "to orchestrate dynamic vulnerability scanners (OWASP ZAP, Nuclei), "
        "headless browser crawling (Playwright), and AI-driven vulnerability triage."
    ),
    version=settings.APP_VERSION,
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
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
def read_root() -> dict[str, str]:
    """Root endpoint returning basic platform identification and documentation URLs."""
    return {
        "title": settings.APP_NAME,
        "description": "AI-assisted application security testing platform",
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
        "health": f"{settings.API_V1_PREFIX}/health",
        "ready": f"{settings.API_V1_PREFIX}/ready",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=(settings.APP_ENV == "development"),
        log_level=settings.LOG_LEVEL.lower(),
    )
