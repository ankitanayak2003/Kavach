from fastapi.testclient import TestClient


def test_health_endpoint_returns_ok(client: TestClient) -> None:
    """Verify the versioned health endpoint returns 200 and healthy status."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "kavach-api"
    assert data["version"] == "0.1.0"


def test_root_endpoint_metadata(client: TestClient) -> None:
    """Verify root endpoint returns basic service metadata and docs pointers."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "Kavach"
    assert data["health"] == "/api/v1/health"
