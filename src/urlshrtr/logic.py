"""Application business logic layer."""

from urllib import parse

from urlshrtr import error, model
from urlshrtr.schema import (DeleteShortUrlResponse, ShortUrlResponse,
                             ShortUrlStatsResponse)


async def get_short_url(url_id: str) -> str:
    """Get the original URL for a short url ID.

    Args:
        url_id (str): The short url ID.

    Returns:
        str: The original URL.

    Raises:
        HTTPException: if the ShortURL with url_id is not found in Redis.
    """
    result = await model.get_short_url(url_id)
    error.raise_if_url_not_found(url_id, result)
    return parse.unquote_plus(result)


async def create_short_url(url: str) -> ShortUrlResponse:
    """Create a new short URL.

    Url is normalized and stored in Redis.

    Args:
        url (str): The original URL.

    Returns:
        ShortUrlResponse: The created short URL response item.
    """
    safe_url = parse.quote_plus(url)
    url_id = await model.create_short_url(safe_url)
    return ShortUrlResponse(url=url, url_id=url_id)


async def update_short_url(url: str, url_id: str) -> ShortUrlResponse:
    """Update an existing short URL.

    Args:
        url (str): The new updated URL.
        url_id (str): The short url ID.

    Returns:
        ShortUrlResponse: The updated short URL response item.

    Raises:
        HTTPException: if the ShortURL with url_id is not found in Redis.
    """
    safe_url = parse.quote_plus(url)
    result = await model.update_short_url(safe_url, url_id)
    error.raise_if_url_not_found(url_id, result)
    return ShortUrlResponse(url=url, url_id=url_id)


async def delete_short_url(url_id: str) -> DeleteShortUrlResponse:
    """Delete an existing short URL.

    Args:
        url_id (str): The short url ID.

    Returns:
        DeleteShortUrlResponse: The deleted short URL response item.

    Raises:
        HTTPException: if the ShortURL with url_id is not found in Redis.
    """
    result = await model.delete_short_url(url_id)
    error.raise_if_url_not_found(url_id, result)
    return DeleteShortUrlResponse(url_id=url_id)


async def get_short_url_stats(url_id: str) -> ShortUrlStatsResponse:
    """Get the short URL stats - number of clicks for the last 24h period.

    Args:
        url_id (str): The short url ID.

    Returns:
        ShortUrlStatsResponse: The short URL stats response item.

    Raises:
        HTTPException: if the ShortURL with url_id is not found in Redis.
    """
    result = await model.get_view_count(url_id)
    error.raise_if_url_not_found(url_id, result)
    return ShortUrlStatsResponse(last_24h=result, url_id=url_id)
