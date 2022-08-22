"""Test the error handling helpers."""
from contextlib import nullcontext as does_not_raise

import pytest
from fastapi import HTTPException
from redis.exceptions import RedisError

from urlshrtr import error


@pytest.mark.asyncio
async def test_handle_redis_errors_decorator():
    """Test the handle_redis_errors decorator."""

    @error.handle_redis_errors
    async def func():
        """Test function."""
        return 'test'

    assert await func() == 'test'


@pytest.mark.asyncio
async def test_handle_redis_errors_decorator_raises_http_exception():
    """Test the handle_redis_errors decorator raises HTTPException."""

    @error.handle_redis_errors
    async def func():
        """Test function."""
        raise RedisError('Redis error')

    with pytest.raises(HTTPException):
        await func()


@pytest.mark.parametrize(
    'result,should_raise',
    [(None, pytest.raises(HTTPException)), ('result', does_not_raise())],
)
def test_raise_if_url_not_found(result, should_raise):
    """Test raise_if_url_not_found helper."""
    with pytest.raises(HTTPException):
        error.raise_if_url_not_found('url_id', None)
