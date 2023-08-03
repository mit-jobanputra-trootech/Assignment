from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, Field, PostgresDsn


class GlobalConfig(BaseSettings):
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: PostgresDsn = Field(env="DATABASE_URL")
    SECRET_KEY: str = Field(env="SECRET_KEY")
    ALGORITHM: str = Field(env="ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = 180
    ENVIRONMENT: str = Field(env="ENVIRONMENT", default="DEV")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class DevConfig(GlobalConfig):
    DEBUG = True


class TestingConfig(GlobalConfig):
    DEBUG = True
    TESTING = True
    TEST_DB_URL: PostgresDsn = Field(env="TEST_DB_URL")
    ALEMBIC_INI: str = "alembic.ini"


class FactoryConfig:
    """Returns a config instance depends on the ENV_STATE variable."""

    def __init__(self, environment: Optional[str] = "DEV"):
        self.environment = environment

    def __call__(self):
        if self.environment == "TEST":
            return TestingConfig()
        return DevConfig()


@lru_cache()
def get_configuration():
    return FactoryConfig(GlobalConfig().ENVIRONMENT)()


config = get_configuration()
