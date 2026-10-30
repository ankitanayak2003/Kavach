"""
Automated tests for FastAPI application initialization, metadata, and documentation.
"""

from fastapi.testclient import TestClient
from app.main import app


def test_app_initialization() -> None:
    """Verify that the FastAPI application initializes with correct configuration metadata."""
    assert app.title == "Kavach"
    assert "AI-assisted application security testing platform" in app.description
    assert app.version == "0.1.0"
    assert app.docs_url == "/docs"
    assert app.redoc_url == "/redoc"
    assert app.openapi_url == "/openapi.json"


def test_root_endpoint_metadata(client: TestClient) -> None:
    """Verify root endpoint returns HTTP 200 and expected metadata pointers."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Kavach"
    assert "AI-assisted" in data["description"]
    assert data["version"] == "0.1.0"
    assert data["docs"] == "/docs"
    assert data["redoc"] == "/redoc"
    assert data["openapi"] == "/openapi.json"
    assert data["health"] == "/api/v1/health"
    assert data["ready"] == "/api/v1/ready"


def test_swagger_docs_accessible(client: TestClient) -> None:
    """Verify that the Swagger UI interactive documentation is accessible at /docs."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger-ui" in response.text.lower() or "html" in response.text.lower()


def test_redoc_docs_accessible(client: TestClient) -> None:
    """Verify that ReDoc alternative API documentation is accessible at /redoc."""
    response = client.get("/redoc")
    assert response.status_code == 200
    assert "redoc" in response.text.lower() or "html" in response.text.lower()


def test_openapi_json_schema(client: TestClient) -> None:
    """Verify OpenAPI JSON schema returns correct metadata and routes."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()

    assert schema["info"]["title"] == "Kavach"
    assert schema["info"]["version"] == "0.1.0"
    assert "/api/v1/health" in schema["paths"]
    assert "/api/v1/ready" in schema["paths"]
    assert "/" in schema["paths"]


def test_no_duplicate_route_registration() -> None:
    """Verify each route path and method combination is registered uniquely."""
    route_signatures = set()
    for route in app.routes:
        methods = getattr(route, "methods", None)
        path = getattr(route, "path", None)
        if methods and path:
            for method in methods:
                sig = (method, path)
                assert sig not in route_signatures, f"Duplicate route signature detected: {sig}"
                route_signatures.add(sig)
