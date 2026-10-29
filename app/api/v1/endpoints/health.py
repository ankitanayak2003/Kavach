from fastapi import APIRouter

router = APIRouter()


@router.get("", summary="Service Health Check")
def get_health() -> dict[str, str]:
    """Return the health status of the Kavach API service."""
    return {
        "status": "healthy",
        "service": "kavach-api",
        "version": "0.1.0",
    }
