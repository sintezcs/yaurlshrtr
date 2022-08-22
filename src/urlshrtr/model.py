"""Model layer."""

import time
from typing import Optional

import nanoid
from nanoid.resources import alphabet

from urlshrtr import error
from urlshrtr.config import settings
from urlshrtr.redis_connector import redis_client


@error.handle_redis_errors
async def update_view_count(url_id: str):
    """Update (increase) the URL view count stats.

    Args:
        url_id (str): The short url ID.

    Raises:
        HTTPException: if some error happened during the Redis update.
    """
    await redis_client.ts().add(_stats_key(url_id), '*', 1)


@error.handle_redis_errors
async def get_view_count(
    url_id: str, interval: int = settings.stats_period
) -> Optional[int]:
    """Get the URL view count stats.

    Args:
        url_id (str): The short url ID.
        interval (int): The stats period in ms. (defaults to one day)

    Returns:
        int: The number of views for the last interval or None.

    Raises:
        HTTPException: if some error happened during the Redis request.
    """
    url_exists = await redis_client.get(url_id)
    if not url_exists:
        return None
    result = await redis_client.ts().range(
        _stats_key(url_id),
        _ts_24h_ago(),
        '+',
        aggregation_type='sum',
        bucket_size_msec=interval,
    )
    return int(result[0][1]) if result else 0


@error.handle_redis_errors
async def get_short_url(url_id: str) -> str:
    """Get the ShortURL record from Redis.

    Args:
        url_id (str): The short url ID.

    Returns:
        str: The original URL.

    Raises:
        HTTPException: if some error happened during the Redis request.
    """
    result = await redis_client.get(url_id)
    if not result:
        return None
    await update_view_count(url_id)
    return result.decode()


@error.handle_redis_errors
async def create_short_url(url: str) -> str:
    """Create the ShortURL record in Redis.

    Also creates a TimeSeries record for the stats.

    Args:
        url (str): The original URL.

    Returns:
        str: The newly created short URL ID.
    """
    url_id = nanoid.generate(alphabet, settings.url_key_length)
    await redis_client.ts().create(
        _stats_key(url_id),
        retention_msec=settings.stats_retention,
        duplicate_policy='first',
    )
    await redis_client.set(url_id, url)
    return url_id


@error.handle_redis_errors
async def update_short_url(url: str, url_id: str) -> Optional[str]:
    """Update the ShortURL record in Redis.

    Args:
        url (str): The new updated URL.
        url_id (str): The short url ID.

    Returns:
        str: The updated short URL ID.

    Raises:
        HTTPException: if the ShortURL with url_id is not found in Redis
    """
    url_exists = await redis_client.get(url_id)
    if not url_exists:
        return None
    await redis_client.set(url_id, url)
    return url_id


@error.handle_redis_errors
async def delete_short_url(url_id: str) -> Optional[str]:
    """Delete the ShortURL record from Redis.

    Args:
        url_id (str): The short url ID.

    Returns:
        str: The deleted short URL ID.

    Raises:
        HTTPException: if the ShortURL with url_id is not found in Redis
    """
    success = await redis_client.delete(url_id)
    if success:
        return url_id
    return None


def _stats_key(url_id: str) -> str:
    """Make a key for stats redis record.

    Args:
        url_id (str): The short url ID.

    Returns:
        str: The Redis TimeSeries key for the stats record.
    """
    return f'{url_id}:stats'


def _ts_24h_ago() -> int:
    """Get timestamp for 24 hours ago in ms.

    Returns:
        int: The timestamp in ms.
    """
    return int(time.time()) * 1000 - settings.stats_period
