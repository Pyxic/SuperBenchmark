# -*- coding: utf-8 -*-
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured with environment variables.

    """

    debug: bool = False

    model_config = SettingsConfigDict(
        env_prefix="SUPERBENCHMARK_", env_file=".env", env_file_encoding="utf-8"
    )


settings = Settings()
