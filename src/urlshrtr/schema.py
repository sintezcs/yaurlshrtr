"""DTO and request/response entity classes."""

from pydantic import AnyHttpUrl
from pydantic.dataclasses import dataclass


@dataclass
class ShortUrlRequest:
    """A request object for creating a new ShortUrl."""

    url: AnyHttpUrl


@dataclass
class ShortUrlResponse:
    """A response object handling ShortUrl data."""

    url: str
    url_id: str


@dataclass
class ShortUrlStatsResponse:
    """A response object handling ShortUrl stats data."""

    url_id: str
    last_24h: int  # Number of clicks in the last 24h period.


@dataclass
class DeleteShortUrlResponse:
    """A response object containing a deleted ShortUrl url_id."""

    url_id: str


@dataclass
class HealthCheckResponse:
    """A response object for the health check."""

    status: str = 'ok'
