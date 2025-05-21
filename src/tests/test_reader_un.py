import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_post_reader_without_auth(client: AsyncClient):
    response = await client.get("/api/v1/reader")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

async def test_get_readers_without_auth(client: AsyncClient):
    response = await client.get("/api/v1/reader")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

async def test_delete_reader_without_auth(client: AsyncClient):
    response = await client.delete("/api/v1/reader/1")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

async def test_get_reader_without_auth(client: AsyncClient):
    response = await client.get("/api/v1/reader/1")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

async def test_put_reader_without_auth(client: AsyncClient):
    response = await client.put("/api/v1/reader/1")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}