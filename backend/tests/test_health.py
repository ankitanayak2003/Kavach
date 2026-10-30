"""
Automated API tests for Kavach health and readiness probe endpoints.

These tests verify process liveness and application readiness without
requiring external services such as Firestore or Redis.
"""

from fastapi.testclient import TestClient


def test_health_check_status_code(client: TestClient) -> None:
    """Verify that GET /api/v1/health returns HTTP 200 OK."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200


def test_health_check_response_fields(client: TestClient) -> None:
    """Verify that GET /api/v1/health response contains expected fields and values."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()

    # Core health payload assertions
    assert data["status"] == "healthy"
    assert data["app"] == "Kavach"
    assert data["app_name"] == "Kavach"
    assert data["version"] == "0.1.0"
    assert "environment" in data


def test_health_check_does_not_depend_on_external_services(client: TestClient) -> None:
    """Verify health endpoint succeeds in complete isolation without external dependencies."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")


def test_readiness_check_status_code(client: TestClient) -> None:
    """Verify that GET /api/v1/ready returns HTTP 200 OK."""
    response = client.get("/api/v1/ready")
    assert response.status_code == 200


def test_readiness_check_response_fields(client: TestClient) -> None:
    """Verify that GET /api/v1/ready response contains readiness status and dependencies."""
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    data = response.json()

    # Core readiness payload assertions
    assert data["status"] == "ready"
    assert data["ready"] is True
    assert data["app"] == "Kavach"
    assert data["version"] == "0.1.0"
    assert "dependencies" in data


def test_readiness_dependency_firestore_unconfigured(client: TestClient) -> None:
    """
    Verify Firestore is reported as unconfigured and not falsely claimed as connected.
    
    Firestore persistence is scheduled for Phase 2.
    """
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    data = response.json()

    firestore_status = data["dependencies"]["firestore"]
    assert firestore_status["status"] == "unconfigured"
    assert firestore_status["required"] is False
    assert "details" in firestore_status


def test_readiness_dependency_redis_unconfigured(client: TestClient) -> None:
    """
    Verify Redis is reported as unconfigured and not falsely claimed as connected.
    
    Redis task broker is scheduled for Phase 3.
    """
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    data = response.json()

    redis_status = data["dependencies"]["redis"]
    assert redis_status["status"] == "unconfigured"
    assert redis_status["required"] is False
    assert "details" in redis_status


def test_health_endpoints_reject_invalid_methods(client: TestClient) -> None:
    """Verify non-GET HTTP methods return HTTP 405 Method Not Allowed."""
    post_health = client.post("/api/v1/health")
    assert post_health.status_code == 405

    post_ready = client.post("/api/v1/ready")
    assert post_ready.status_code == 405
