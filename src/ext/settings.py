"""
Application settings loaded from environment and .env file.

Uses pydantic-settings: env vars override .env; .env is loaded from current
working directory or from env_file path. Use get_settings() for FastAPI
Depends() or to obtain a consistent entry point; tests can override by
replacing or wrapping the factory.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Parsed settings from .env and environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    database_url: str = "sqlite+aiosqlite:///./finadv.db"
    sql_echo: bool = False


def get_settings() -> Settings:
    """Return application settings. Use in Depends(get_settings) or as entry point."""
    return _settings


# Singleton; created once at import. Tests can set os.environ or patch get_settings.
_settings = Settings()
settings = _settings

__all__ = ["Settings", "get_settings", "settings"]
