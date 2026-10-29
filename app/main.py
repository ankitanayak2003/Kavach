from fastapi import FastAPI
from app.api.v1.router import api_v1_router

app = FastAPI(
    title="Kavach",
    description="AI-assisted application security testing platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/", summary="Root Index", tags=["General"])
def read_root() -> dict[str, str]:
    """Root endpoint providing service metadata."""
    return {
        "app": "Kavach",
        "description": "AI-assisted application security testing platform",
        "docs": "/docs",
        "health": "/api/v1/health",
        "version": "0.1.0",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
