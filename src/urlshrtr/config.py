"""Application configuration."""

import sys

from loguru import logger
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    environment = 'development'
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0
    redis_password: str = None
    stats_period = 86400 * 1000  # 1 day in msec
    stats_retention = 86400 * 1000 * 7  # 7 days in msec
    url_key_length = 6
    debug = False
    app_port = 8000
    app_host = 'localhost'
    app_protocol = 'http'
    log_level = 'INFO'
    log_format = '{time} {level} {message}'


settings = Settings()


logger.configure(
    handlers=[
        dict(
            sink=sys.stderr,
            format=settings.log_format,
            level=settings.log_level,
            enqueue=True,
            serialize=True,
        )
    ]
)
