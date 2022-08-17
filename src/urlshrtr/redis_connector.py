"""Redis connector for URL Shortener"""

from redis.asyncio.client import Redis

from urlshrtr.config import settings

redis_client = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    password=settings.redis_password,
)
