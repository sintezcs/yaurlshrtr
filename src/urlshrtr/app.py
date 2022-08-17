"""URL Shortener Application."""

from fastapi import FastAPI

from urlshrtr.config import settings
from urlshrtr.entity import HealthCheckResponse
from urlshrtr.handlers import router

app = FastAPI(debug=settings.debug)
app.include_router(router)


@app.get('/health', response_model=HealthCheckResponse)
async def health():
    """Health check endpoint."""
    return HealthCheckResponse()
