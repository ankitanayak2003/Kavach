"""
Unit tests for Kavach centralized configuration module (backend/app/core/config.py).

Validates default development values, environment variable overrides,
cached singleton behavior, and independence from external services.
"""

import pytest
from app.core.config import Settings, get_settings


def test_default_settings_values() -> None:
    """Verify that default settings provide safe development defaults."""
    settings = Settings()

    # Application metadata
    assert settings.APP_NAME == "Kavach"
    assert settings.APP_ENV == "development"
    assert settings.APP_VERSION == "0.1.0"
    assert "AI-assisted" in settings.APP_DESCRIPTION

    # Debug and networking
    assert settings.DEBUG is False
    assert settings.APP_HOST == "127.0.0.1"
    assert settings.APP_PORT == 8000

    # Routing and logging
    assert settings.API_V1_PREFIX == "/api/v1"
    assert settings.LOG_LEVEL == "INFO"

    # Documentation paths
    assert settings.DOCS_URL == "/docs"
    assert settings.REDOC_URL == "/redoc"
    assert settings.OPENAPI_URL == "/openapi.json"

    # Environment helper properties
    assert settings.is_development is True
    assert settings.is_testing is False
    assert settings.is_production is False


def test_environment_variable_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that environment variables take precedence over defaults."""
    monkeypatch.setenv("APP_NAME", "Kavach-Enterprise")
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("APP_VERSION", "1.0.0")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("APP_HOST", "0.0.0.0")
    monkeypatch.setenv("APP_PORT", "9000")
    monkeypatch.setenv("API_V1_PREFIX", "/api/v2")
    monkeypatch.setenv("LOG_LEVEL", "debug")

    custom_settings = Settings()
    assert custom_settings.APP_NAME == "Kavach-Enterprise"
    assert custom_settings.APP_ENV == "production"
    assert custom_settings.APP_VERSION == "1.0.0"
    assert custom_settings.DEBUG is True
    assert custom_settings.APP_HOST == "0.0.0.0"
    assert custom_settings.APP_PORT == 9000
    assert custom_settings.API_V1_PREFIX == "/api/v2"
    assert custom_settings.LOG_LEVEL == "DEBUG"

    # Verify environment helper properties updated
    assert custom_settings.is_development is False
    assert custom_settings.is_testing is False
    assert custom_settings.is_production is True


def test_cached_settings_accessor() -> None:
    """Verify that get_settings() returns a cached singleton instance."""
    instance_one = get_settings()
    instance_two = get_settings()
    assert instance_one is instance_two


def test_starts_without_cloud_credentials() -> None:
    """Verify configuration loads without requiring Firestore, Redis, or API credentials."""
    settings = Settings()
    assert settings is not None
    assert settings.APP_NAME == "Kavach"
