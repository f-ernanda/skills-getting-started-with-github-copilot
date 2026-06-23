import copy

import pytest
import httpx

from src.app import activities, app


@pytest.fixture
async def client() -> httpx.AsyncClient:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Keep tests isolated by restoring in-memory data around each test."""
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)
