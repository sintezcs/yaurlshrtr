"""Error handlers and utilities."""

from functools import wraps
from typing import Any

from fastapi import HTTPException
from redis.exceptions import RedisError

from urlshrtr.config import logger


def handle_redis_errors(func):
    """A decorator to handle Redis exception and log it.

    Args:
        func: Function to decorate.

    Returns:
        Decorated function.

    Raises:
        HTTPException: If Redis exception is raised.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        """Wrapper function.

        Args:
            args: Function arguments.
            kwargs: Function keyword arguments.
        """
        try:
            return await func(*args, **kwargs)
        except RedisError as e:
            logger.exception('Redis error')
            raise HTTPException(status_code=500, detail=f'Redis error: {e}')

    return wrapper


def raise_if_url_not_found(url_id: str, result: Any):
    """Raise HTTPException if ShortURL item with url_id was not found in Redis.

    Args:
        url_id: ShortURL ID.
        result: Redis result received from the model layer.

    Raises:
        HTTPException: If ShortURL item with url_id was not found in Redis.
    """
    if result is None:
        error_message = f'ShortUrl with id {url_id} not found'
        logger.error(error_message)
        raise HTTPException(status_code=404, detail=error_message)
