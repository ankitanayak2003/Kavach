"""
Pytest configuration and test fixtures for Kavach backend tests.
"""

from typing import Generator
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    """
    Session-scoped FastAPI TestClient fixture.

    Provides a clean HTTP client for testing API routes without starting a live server.
    Does not require external databases (Firestore) or caching layers (Redis).
    """
    with TestClient(app) as test_client:
        yield test_client
