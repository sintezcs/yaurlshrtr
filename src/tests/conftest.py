"""Shared pytest fixtures."""

from unittest.mock import patch

import pytest


@pytest.fixture()
def mock_redis_client():
    """Redis client mock."""
    with patch('urlshrtr.model.redis_client') as redis_mock:
        yield redis_mock
