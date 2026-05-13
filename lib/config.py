from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


def _get_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _get_list(name: str, default: list[str] | None = None) -> list[str]:
    value = os.getenv(name)
    if not value:
        return default or []
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Le Tre Gemme API")
    app_env: str = os.getenv("APP_ENV", "local")
    api_host: str = os.getenv("API_HOST", "127.0.0.1")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    api_reload: bool = _get_bool("API_RELOAD", True)
    cors_origins: list[str] = None

    mysql_host: str = os.getenv("MYSQL_HOST", "127.0.0.1")
    mysql_port: int = int(os.getenv("MYSQL_PORT", "3306"))
    mysql_database: str = os.getenv("MYSQL_DATABASE", "my_bb")
    mysql_user: str = os.getenv("MYSQL_USER", "my_bb_user")
    mysql_password: str = os.getenv("MYSQL_PASSWORD", "my_bb_password")
    mysql_url: str | None = os.getenv("MYSQL_PUBLIC_URL") or os.getenv("DATABASE_URL") or os.getenv("MYSQL_URL")

    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file_path: str = os.getenv("LOG_FILE_PATH", "backend/logs/app.log")
    log_backup_count: int = int(os.getenv("LOG_BACKUP_COUNT", "14"))

    admin_username: str = os.getenv("ADMIN_USERNAME", "admin")
    admin_password: str = os.getenv("ADMIN_PASSWORD", "admin")
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "change-me-in-production")
    jwt_expires_minutes: int = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))

    @property
    def database_url(self) -> str:
        if self.mysql_url:
            return self.mysql_url.replace("mysql://", "mysql+pymysql://", 1)

        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        )


settings = Settings(cors_origins=_get_list("CORS_ORIGINS", ["http://localhost:5173"]))
