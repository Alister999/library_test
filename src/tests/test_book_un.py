import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_post_book_without_auth(client: AsyncClient):
    response = await client.get("/api/v1/book")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

async def test_get_books_without_auth(client: AsyncClient):
    response = await client.get("/api/v1/book")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

async def test_delete_book_without_auth(client: AsyncClient):
    response = await client.delete("/api/v1/book/1")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

async def test_get_book_without_auth(client: AsyncClient):
    response = await client.get("/api/v1/book/1")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

async def test_put_book_without_auth(client: AsyncClient):
    response = await client.put("/api/v1/book/1")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}