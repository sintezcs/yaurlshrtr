"""Test the API handlers module."""
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException
from fastapi.testclient import TestClient

from tests.constants import FULL_URL, URL_ID
from urlshrtr.app import app

client = TestClient(app)


@patch('urlshrtr.handlers.logic')
def test_get_short_url(logic_mock):
    """Test get_short_url success."""
    logic_mock.get_short_url = AsyncMock(return_value=FULL_URL)
    response = client.get(f'/urls/{URL_ID}', allow_redirects=False)
    assert response.status_code == 307
    assert response.headers['Location'] == FULL_URL


@patch('urlshrtr.handlers.logic')
def test_get_short_url_redis_error(logic_mock):
    """Test get_short_url raises HTTPException in case of RedisError raised."""
    logic_mock.get_short_url = AsyncMock(
        side_effect=HTTPException(status_code=500, detail='Redis error')
    )
    response = client.get(f'/urls/{URL_ID}')
    assert response.status_code == 500
    assert response.json() == {'detail': 'Redis error'}


@patch('urlshrtr.handlers.logic')
def test_get_short_url_not_found(logic_mock):
    """Test get_short_url raises HTTPException in case of URL not found."""
    error_detail = 'ShortUrl with id {} not found'.format(URL_ID)
    logic_mock.get_short_url = AsyncMock(
        side_effect=HTTPException(status_code=404, detail=error_detail)
    )
    response = client.get(f'/urls/{URL_ID}', allow_redirects=False)
    assert response.status_code == 404
    assert response.json() == {'detail': error_detail}


# TODO: complete the handler module tests
# Tests for the rest of the API handler functions will be similar
# to the ones above. They are skipped for now to save the development time.
