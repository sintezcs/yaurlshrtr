from fastapi import APIRouter
from starlette.responses import RedirectResponse

from urlshrtr import logic
from urlshrtr.entity import (
    ShortUrlRequest,
    ShortUrlResponse,
    ShortUrlStatsResponse,
    DeleteShortUrlResponse,
)

router = APIRouter(prefix='/urls')


@router.get('/{url_id}')
async def redirect_to_url(url_id: str) -> RedirectResponse:
    """Redirect to the original URL."""
    url = await logic.get_full_url(url_id)
    return RedirectResponse(url)


@router.post('/', response_model=ShortUrlResponse)
async def create_url(url_data: ShortUrlRequest) -> ShortUrlResponse:
    """Create a new short URL."""
    response = await logic.create_short_url(url_data.url)
    return response


@router.put('/{url_id}', response_model=ShortUrlResponse)
async def update_url(url_id: str, url_data: ShortUrlRequest) -> ShortUrlResponse:
    """Update the existing short URL."""
    result = await logic.update_short_url(url_data.url, url_id)
    return result


@router.delete('/{url_id}', response_model=DeleteShortUrlResponse)
async def delete_url(url_id: str) -> DeleteShortUrlResponse:
    """Delete the existing short URL."""
    result = await logic.delete_short_url(url_id)
    return result


@router.get('/{url_id}/stats', response_model=ShortUrlStatsResponse)
async def get_url_stats(url_id: str) -> ShortUrlStatsResponse:
    """Get the URL view count stats."""
    result = await logic.get_short_url_stats(url_id)
    return result
