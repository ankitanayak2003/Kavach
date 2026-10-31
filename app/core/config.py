"""
Kavach - Centralized Application Settings Module.

Provides type-safe configuration management using Pydantic Settings.
Loads values from environment variables and an optional .env file with
sensible development defaults.
"""

from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized application settings for the Kavach FastAPI backend."""

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Core Application Metadata
    APP_NAME: str = Field(
        default="Kavach",
        description="Name of the security platform",
    )
    APP_VERSION: str = Field(
        default="0.1.0",
        description="Semantic version of the application",
    )
    APP_DESCRIPTION: str = Field(
        default=(
            "Kavach is an AI-assisted application security testing platform designed "
            "to orchestrate dynamic vulnerability scanners (OWASP ZAP, Nuclei), "
            "headless browser crawling (Playwright), and AI-driven vulnerability triage."
        ),
        description="Detailed description of the application platform",
    )

    # Runtime Environment (development, testing, production)
    APP_ENV: str = Field(
        default="development",
        description="Runtime environment: development, testing, or production",
    )

    # Debug Mode
    DEBUG: bool = Field(
        default=False,
        description="Enable debug mode and verbose tracebacks",
    )

    # Server Network Configuration
    APP_HOST: str = Field(
        default="127.0.0.1",
        description="Host interface for the Uvicorn server",
    )
    APP_PORT: int = Field(
        default=8000,
        description="Port for the Uvicorn server",
    )

    # API Routing
    API_V1_PREFIX: str = Field(
        default="/api/v1",
        description="URL prefix for version 1 API endpoints",
    )

    # Logging Configuration
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Application logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    # Documentation URLs
    DOCS_URL: str = Field(
        default="/docs",
        description="Interactive Swagger UI endpoint path",
    )
    REDOC_URL: str = Field(
        default="/redoc",
        description="Alternative ReDoc documentation endpoint path",
    )
    OPENAPI_URL: str = Field(
        default="/openapi.json",
        description="OpenAPI specification JSON endpoint path",
    )

    @field_validator("APP_ENV")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        """Normalize and validate application environment."""
        normalized = value.strip().lower()
        allowed = {"development", "testing", "production", "staging"}
        if normalized not in allowed:
            return normalized
        return normalized

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        """Normalize log level to uppercase."""
        return value.strip().upper()

    @property
    def is_development(self) -> bool:
        """Return True if running in development mode."""
        return self.APP_ENV == "development"

    @property
    def is_testing(self) -> bool:
        """Return True if running in testing mode."""
        return self.APP_ENV == "testing"

    @property
    def is_production(self) -> bool:
        """Return True if running in production mode."""
        return self.APP_ENV == "production"


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings singleton instance.

    Uses functools.lru_cache so settings are parsed once from the environment
    and reused across the application lifecycle without repeated construction.
    """
    return Settings()


# Global reusable settings instance
settings: Settings = get_settings()
