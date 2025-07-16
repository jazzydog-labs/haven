"""Application settings using Pydantic and Hydra."""

from functools import lru_cache
from typing import Any, Optional

from hydra import compose, initialize_config_dir
from hydra.core.global_hydra import GlobalHydra
from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings


class ServerSettings(BaseModel):
    """Server configuration."""

    host: str = "0.0.0.0"
    port: int = 8080
    reload: bool = False


class DatabaseSettings(BaseModel):
    """Database configuration."""

    driver: str
    host: str
    port: int
    name: str
    user: str
    password: str
    dsn: str

    class PoolSettings(BaseModel):
        """Connection pool settings."""

        size: int = 20
        max_overflow: int = 10
        timeout: int = 30
        recycle: int = 3600

    pool: PoolSettings = Field(default_factory=PoolSettings)


class LoggingSettings(BaseModel):
    """Logging configuration."""

    level: str = "INFO"
    format: str = "json"

    class StructuredSettings(BaseModel):
        """Structured logging settings."""

        enabled: bool = True
        include_timestamp: bool = True
        include_level: bool = True
        include_logger: bool = True
        include_hostname: bool = False
        include_process: bool = False

    class ConsoleSettings(BaseModel):
        """Console logging settings."""

        enabled: bool = True
        colorize: bool = True

    class FileSettings(BaseModel):
        """File logging settings."""

        enabled: bool = False
        path: str = "logs/haven.log"
        rotation: str = "100 MB"
        retention: str = "10 days"

    structured: StructuredSettings = Field(default_factory=StructuredSettings)
    console: ConsoleSettings = Field(default_factory=ConsoleSettings)
    file: FileSettings = Field(default_factory=FileSettings)
    loggers: dict[str, str] = Field(default_factory=dict)


class CorsSettings(BaseModel):
    """CORS configuration."""

    allow_origins: list[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]


class AppInfo(BaseModel):
    """Application information."""

    name: str = "haven"
    version: str = "0.1.0"
    debug: bool = False
    env: str = "local"


class AppSettings(BaseSettings):
    """Main application settings."""

    app: AppInfo
    server: ServerSettings
    database: DatabaseSettings
    logging: LoggingSettings
    cors: CorsSettings

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @validator("database", pre=True)
    def validate_database(cls, v: Any) -> Any:
        """Ensure database settings are properly structured."""
        if isinstance(v, dict) and "pool" in v and isinstance(v["pool"], dict):
            v["pool"] = DatabaseSettings.PoolSettings(**v["pool"])
        return v


@lru_cache()
def get_settings() -> AppSettings:
    """Get cached application settings from Hydra configuration."""
    # Clear any existing Hydra instance
    if GlobalHydra.instance().is_initialized():
        GlobalHydra.instance().clear()

    # Initialize Hydra with config directory
    initialize_config_dir(config_dir="/Users/paul/dev/jazzydog-labs/haven/conf", version_base="1.3")

    # Compose configuration
    cfg = compose(config_name="defaults")

    # Convert to dictionary and create settings
    settings_dict = {
        "app": cfg.get("app", {}),
        "server": cfg.get("server", {}),
        "database": cfg.get("database", {}),
        "logging": cfg.get("logging", {}),
        "cors": cfg.get("cors", {}),
    }

    return AppSettings(**settings_dict)