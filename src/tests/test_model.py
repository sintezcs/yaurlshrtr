"""Test the model layer."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException
from freezegun import freeze_time
from nanoid.resources import alphabet
from redis.exceptions import RedisError

from tests.constants import FROZEN_TIME, FULL_URL, FULL_URL_BYTES, URL_ID
from urlshrtr import model
from urlshrtr.config import settings


@pytest.mark.asyncio
@patch('urlshrtr.model.update_view_count')
@pytest.mark.parametrize(
    'full_url,expected_result',
    [
        (FULL_URL_BYTES, FULL_URL),
        (None, None),
    ],
)
async def test_get_short_url(
    update_view_count_mock, mock_redis_client, full_url, expected_result
):
    """Test get_short_url success."""
    mock_redis_client.get.return_value = full_url
    result = await model.get_short_url(URL_ID)
    assert result == expected_result
    mock_redis_client.get.assert_awaited_with(URL_ID)
    if expected_result:
        update_view_count_mock.assert_awaited_with(URL_ID)
    else:
        update_view_count_mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_short_url_redis_error(mock_redis_client):
    """Test get_short_url raises HTTPException in case of RedisError raised."""
    mock_redis_client.get.side_effect = RedisError('Redis error')
    with pytest.raises(HTTPException):
        await model.get_short_url(URL_ID)


@pytest.mark.asyncio
async def test_update_view_count(mock_redis_client):
    """Test update_view_count success."""
    ts_mock = AsyncMock()
    mock_redis_client.ts = MagicMock(return_value=ts_mock)
    await model.update_view_count(URL_ID)
    expected_key = model._stats_key(URL_ID)
    ts_mock.add.assert_awaited_with(expected_key, '*', 1)


@pytest.mark.asyncio
async def test_update_view_count_redis_error(mock_redis_client):
    """Test update_view_count raises HTTPException in case of RedisError raised."""
    ts_mock = AsyncMock()
    mock_redis_client.ts = MagicMock(return_value=ts_mock)
    ts_mock.add.side_effect = RedisError('Redis error')
    with pytest.raises(HTTPException):
        await model.update_view_count(URL_ID)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'get_result,ts_result,expected_count',
    [
        (None, [], None),
        (FULL_URL_BYTES, [(1, 1)], 1),
        (FULL_URL_BYTES, [], 0),
    ],
)
async def test_get_view_count(mock_redis_client, get_result, ts_result, expected_count):
    """Test get_view_count success."""
    ts_mock = AsyncMock()
    mock_redis_client.ts = MagicMock(return_value=ts_mock)
    ts_mock.range.return_value = ts_result
    mock_redis_client.get.return_value = get_result
    result = await model.get_view_count(URL_ID)
    assert result == expected_count
    mock_redis_client.get.assert_awaited_with(URL_ID)
    if get_result:
        ts_mock.range.assert_awaited_with(
            model._stats_key(URL_ID),
            model._ts_24h_ago(),
            '+',
            aggregation_type='sum',
            bucket_size_msec=model.settings.stats_period,
        )


@pytest.mark.asyncio
@pytest.mark.parametrize('get_failed', [True, False])
async def test_get_view_count_redis_error(mock_redis_client, get_failed):
    """Test get_view_count raises HTTPException in case of RedisError raised."""
    ts_mock = AsyncMock()
    mock_redis_client.ts = MagicMock(return_value=ts_mock)
    ts_mock.range.side_effect = RedisError('Redis error')
    if get_failed:
        mock_redis_client.get.side_effect = RedisError('Redis error')
    with pytest.raises(HTTPException):
        await model.get_view_count(URL_ID)


@pytest.mark.asyncio
@patch('urlshrtr.model.nanoid.generate')
async def test_create_short_url(nanoid_mock, mock_redis_client):
    """Test create_short_url success."""
    ts_mock = AsyncMock()
    mock_redis_client.ts = MagicMock(return_value=ts_mock)
    nanoid_mock.return_value = URL_ID
    result = await model.create_short_url(FULL_URL)
    assert result == URL_ID
    nanoid_mock.assert_called_with(alphabet, settings.url_key_length)
    mock_redis_client.set.assert_awaited_with(URL_ID, FULL_URL)
    ts_mock.create.assert_awaited_with(
        model._stats_key(URL_ID),
        retention_msec=settings.stats_retention,
        duplicate_policy='first',
    )


@pytest.mark.asyncio
@pytest.mark.parametrize('ts_create_failed', [True, False])
async def test_create_short_url_redis_error(mock_redis_client, ts_create_failed):
    """Test create_short_url raises HTTPException in case of RedisError raised."""
    ts_mock = AsyncMock()
    mock_redis_client.ts = MagicMock(return_value=ts_mock)
    mock_redis_client.set.side_effect = RedisError('Redis error')
    if ts_create_failed:
        ts_mock.create.side_effect = RedisError('Redis error')
    with pytest.raises(HTTPException):
        await model.create_short_url(FULL_URL)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'get_result,expected_url_id', [(FULL_URL_BYTES, URL_ID), (None, None)]
)
async def test_update_short_url(mock_redis_client, get_result, expected_url_id):
    """Test update_short_url success."""
    mock_redis_client.get.return_value = get_result
    result = await model.update_short_url(FULL_URL, URL_ID)
    assert result == expected_url_id
    mock_redis_client.get.assert_awaited_with(URL_ID)
    if get_result:
        mock_redis_client.set.assert_awaited_with(URL_ID, FULL_URL)
    else:
        mock_redis_client.set.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize('get_failed', [True, False])
async def test_update_short_url_redis_error(mock_redis_client, get_failed):
    """Test update_short_url raises HTTPException in case of RedisError raised."""
    if get_failed:
        mock_redis_client.get.side_effect = RedisError('Redis error')
    mock_redis_client.set.side_effect = RedisError('Redis error')
    with pytest.raises(HTTPException):
        await model.update_short_url(FULL_URL, URL_ID)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'delete_result,expected_url_id', [(True, URL_ID), (False, None)]
)
async def test_delete_short_url(mock_redis_client, delete_result, expected_url_id):
    """Test delete_short_url success."""
    mock_redis_client.delete.return_value = delete_result
    result = await model.delete_short_url(URL_ID)
    assert result == expected_url_id
    mock_redis_client.delete.assert_awaited_with(URL_ID)


@pytest.mark.asyncio
async def test_delete_short_url_redis_error(mock_redis_client):
    """Test delete_short_url raises HTTPException in case of RedisError raised."""
    mock_redis_client.delete.side_effect = RedisError('Redis error')
    with pytest.raises(HTTPException):
        await model.delete_short_url(URL_ID)


def test_stats_key():
    """Test stats_key success."""
    result = model._stats_key(URL_ID)
    assert result == f'{URL_ID}:stats'


@freeze_time(FROZEN_TIME)
def test_ts_24h_ago():
    """Test ts_24h_ago success."""
    expected_ts = 1577750400000  # FROZEN_TIME - 24h in msec
    result = model._ts_24h_ago()
    assert result == expected_ts
