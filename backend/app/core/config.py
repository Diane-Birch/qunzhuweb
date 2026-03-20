from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import BaseSettings, Field, validator


ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    """Centralized runtime configuration loaded from environment variables."""

    app_name: str = Field("哈尼梯田红米文化展示网站", env="APP_NAME")
    api_v1_prefix: str = Field("/api/v1", env="API_V1_PREFIX")
    database_url: str = Field(..., env="DATABASE_URL")
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(720, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    admin_username: str = Field("admin", env="ADMIN_USERNAME")
    admin_password: str = Field("admin123456", env="ADMIN_PASSWORD")
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    @validator("cors_origins", pre=True)
    def split_cors_origins(cls, value):
        """Allow JSON arrays or comma-separated CORS origins in `.env`."""
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    class Config:
        env_file = str(ENV_FILE)
        env_file_encoding = "utf-8"
        case_sensitive = False

        @classmethod
        def parse_env_var(cls, field_name, raw_value):
            if field_name == "cors_origins":
                value = raw_value.strip()
                if value.startswith("["):
                    import json

                    return json.loads(value)
                return [item.strip() for item in value.split(",") if item.strip()]
            return cls.json_loads(raw_value)


@lru_cache()
def get_settings() -> Settings:
    """Cache settings so the application reuses one validated config object."""
    return Settings()