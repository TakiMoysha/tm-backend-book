import logging.config
import pathlib
from functools import lru_cache

from pydantic import AnyHttpUrl, BaseSettings

from .logs import LOGGING_CONFIG

_BASE_DIR = pathlib.Path(__file__).resolve().parent
_DEFAULT_BACKEND_URL = AnyHttpUrl.build(
    scheme="http", host="localhost.taki", port=8000
)
_DEFAULT_STATIC_URL = AnyHttpUrl.build(
    scheme="http", host="localhost.taki", port=8000, path="/static/"
)


class Settings(BaseSettings):
    DEBUG: bool = False

    BACKEND_URL: AnyHttpUrl = _DEFAULT_BACKEND_URL

    STATIC_URL: AnyHttpUrl = _DEFAULT_STATIC_URL


@lru_cache()
def get_settings() -> Settings:
    return Settings()


logging.config.dictConfig(LOGGING_CONFIG)
settings: Settings = get_settings()
