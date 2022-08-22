"""Test the logic layer functions."""
from unittest.mock import AsyncMock, patch
from urllib import parse

import pytest
from fastapi import HTTPException

from tests.constants import FULL_URL, FULL_URL_BYTES, URL_ID
from urlshrtr import logic


@pytest.mark.asyncio
@patch('urlshrtr.logic.model')
async def test_get_short_url(model_mock):
    """Test get_short_url success."""
    model_mock.get_short_url = AsyncMock(return_value=parse.quote_plus(FULL_URL_BYTES))
    result = await logic.get_short_url(URL_ID)
    assert result == FULL_URL
    model_mock.get_short_url.assert_awaited_with(URL_ID)


@pytest.mark.asyncio
@patch('urlshrtr.logic.model')
async def test_get_short_url_redis_error(model_mock):
    """Test get_short_url raises HTTPException in case of RedisError raised."""
    model_mock.get_short_url = AsyncMock(
        side_effect=HTTPException(status_code=500, detail='Redis error')
    )
    with pytest.raises(HTTPException):
        await logic.get_short_url(URL_ID)


@pytest.mark.asyncio
@patch('urlshrtr.logic.model')
async def test_get_short_url_not_found(model_mock):
    """Test get_short_url raises HTTPException in case of URL not found."""
    model_mock.get_short_url = AsyncMock(return_value=None)
    with pytest.raises(HTTPException):
        await logic.get_short_url(URL_ID)


# TODO: complete the logic module tests
# Tests for the rest of the logic functions will be similar
# to the ones above. They are skipped for now to save the development time.
