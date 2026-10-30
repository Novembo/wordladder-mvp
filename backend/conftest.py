import os
import pytest
from httpx import ASGITransport, AsyncClient

# Set testing environment flags
os.environ["WL_REDIS_ENABLED"] = "false"
os.environ["WL_DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from app.database import init_db
from app.main import app
from app.services.graph_service import get_or_load_pack


@pytest.fixture
async def setup_test_db():
    await init_db()
    await get_or_load_pack("en")


@pytest.fixture
async def client(setup_test_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
