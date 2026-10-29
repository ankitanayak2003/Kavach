from fastapi import FastAPI
from app.api.v1.router import api_v1_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-assisted application security testing platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)


@app.get("/", summary="Root Index", tags=["General"])
def read_root() -> dict[str, str]:
    """Root endpoint providing service metadata."""
    return {
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "description": "AI-assisted application security testing platform",
        "docs": "/docs",
        "health": f"{settings.API_V1_PREFIX}/health",
        "version": "0.1.0",
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
