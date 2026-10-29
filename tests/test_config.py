import pytest
from app.core.config import Settings, get_settings


def test_default_settings_values() -> None:
    """Verify default settings provide safe development configuration."""
    settings = Settings()
    assert settings.APP_NAME == "Kavach"
    assert settings.APP_ENV == "development"
    assert settings.APP_HOST == "127.0.0.1"
    assert settings.APP_PORT == 8000
    assert settings.API_V1_PREFIX == "/api/v1"
    assert settings.LOG_LEVEL == "INFO"


def test_environment_variable_override(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify environment variables take precedence over default settings."""
    monkeypatch.setenv("APP_NAME", "Kavach-Override")
    monkeypatch.setenv("APP_PORT", "9090")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    custom_settings = Settings()
    assert custom_settings.APP_NAME == "Kavach-Override"
    assert custom_settings.APP_PORT == 9090
    assert custom_settings.LOG_LEVEL == "DEBUG"


def test_starts_without_cloud_credentials() -> None:
    """Verify application configuration loads cleanly without any cloud or API credentials."""
    # Ensure no Firestore, Redis, or LLM credentials are required for initialization
    settings = get_settings()
    assert settings is not None
    assert settings.APP_NAME == "Kavach"
