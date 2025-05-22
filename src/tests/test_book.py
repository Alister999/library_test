import logging
import pytest
from httpx import AsyncClient

logger = logging.getLogger("BookTests")

@pytest.mark.asyncio
async def test_post_book(client: AsyncClient):
    data = {"name": "Nikola", "email": "user@example.com", "password": "123"}
    login_data = {"email": "user@example.com", "password": "123"}
    book_data = {
      "name": "Война и мир",
      "author": "Толстой",
      "year": 1992,
      "ISBN": "isbn",
      "count": 1
    }
    await client.post("/api/v1/register", json=data)
    response = await client.post("/api/v1/login", json=login_data)
    my_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {my_token}"}
    post_response = await client.post("/api/v1/book", json=book_data, headers=headers)

    assert post_response.status_code == 200
    expected_keys = {"id", "name", "author", "year", "ISBN", "count"}
    assert set(post_response.json().keys()) == expected_keys
    assert post_response.json()["name"] == "Война и мир"
    assert post_response.json()["author"] == "Толстой"
    assert post_response.json()["year"] == 1992
    assert post_response.json()["ISBN"] == "isbn"
    assert post_response.json()["count"] == 1


@pytest.mark.asyncio
async def test_get_books(client: AsyncClient):
    data = {"name": "Nikola", "email": "user@example.com", "password": "123"}
    login_data = {"email": "user@example.com", "password": "123"}
    book_data = {
      "name": "Война и мир",
      "author": "Толстой",
      "year": 1992,
      "ISBN": "isbn",
      "count": 1
    }
    await client.post("/api/v1/register", json=data)
    response = await client.post("/api/v1/login", json=login_data)
    my_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {my_token}"}
    await client.post("/api/v1/book", json=book_data, headers=headers)
    get_response = await client.get("/api/v1/book", headers=headers)
    print(f'response - {get_response.json()}')

    assert get_response.status_code == 200
    assert len(get_response.json()) == 1
    expected_keys = {"id", "name", "author", "year", "ISBN", "count"}
    assert set(get_response.json()[0].keys()) == expected_keys
    assert get_response.json()[0]["name"] == "Война и мир"
    assert get_response.json()[0]["author"] == "Толстой"
    assert get_response.json()[0]["year"] == 1992
    assert get_response.json()[0]["ISBN"] == "isbn"
    assert get_response.json()[0]["count"] == 1


@pytest.mark.asyncio
async def test_get_book(client: AsyncClient):
    data = {"name": "Nikola", "email": "user@example.com", "password": "123"}
    login_data = {"email": "user@example.com", "password": "123"}
    book_data = {
      "name": "Война и мир",
      "author": "Толстой",
      "year": 1992,
      "ISBN": "isbn",
      "count": 1
    }
    await client.post("/api/v1/register", json=data)
    response = await client.post("/api/v1/login", json=login_data)
    my_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {my_token}"}
    post_response = await client.post("/api/v1/book", json=book_data, headers=headers)
    book_id = post_response.json()["id"]
    get_response = await client.get(f"/api/v1/book/{book_id}", headers=headers)

    assert get_response.status_code == 200
    expected_keys = {"id", "name", "author", "year", "ISBN", "count"}
    assert set(get_response.json().keys()) == expected_keys
    assert get_response.json()["name"] == "Война и мир"
    assert get_response.json()["author"] == "Толстой"
    assert get_response.json()["year"] == 1992
    assert get_response.json()["ISBN"] == "isbn"
    assert get_response.json()["count"] == 1


@pytest.mark.asyncio
async def test_delete_reader(client: AsyncClient):
    data = {"name": "Nikola", "email": "user@example.com", "password": "123"}
    login_data = {"email": "user@example.com", "password": "123"}
    book_data = {
      "name": "Война и мир",
      "author": "Толстой",
      "year": 1992,
      "ISBN": "isbn",
      "count": 1
    }
    await client.post("/api/v1/register", json=data)
    response = await client.post("/api/v1/login", json=login_data)
    my_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {my_token}"}
    post_response = await client.post("/api/v1/book", json=book_data, headers=headers)
    book_id = post_response.json()["id"]

    get_response = await client.get(f"/api/v1/book/{book_id}", headers=headers)
    assert get_response.status_code == 200

    del_response = await client.delete(f"/api/v1/book/{book_id}", headers=headers)
    assert del_response.status_code == 200
    assert del_response.json() == {"message": f"Book with id {book_id} was deleted successful"}

    second_get_response = await client.get(f"/api/v1/book/{book_id}", headers=headers)
    assert second_get_response.status_code == 404


@pytest.mark.asyncio
async def test_put_reader(client: AsyncClient):
    data = {"name": "Nikola", "email": "user@example.com", "password": "123"}
    login_data = {"email": "user@example.com", "password": "123"}
    book_data = {
      "name": "Война и мир",
      "author": "Толстой",
      "year": 1992,
      "ISBN": "isbn",
      "count": 1
    }
    book_data_2 = {
      "name": "Война миров",
      "author": "Герберт Уэлс",
      "year": 1990,
      "ISBN": "isbn2",
      "count": 1
    }
    await client.post("/api/v1/register", json=data)
    response = await client.post("/api/v1/login", json=login_data)
    my_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {my_token}"}
    post_response = await client.post("/api/v1/book", json=book_data, headers=headers)
    book_id = post_response.json()["id"]
    put_response = await client.put(f"/api/v1/book/{book_id}", json=book_data_2, headers=headers)

    assert put_response.status_code == 200
    expected_keys = {"id", "name", "author", "year", "ISBN", "count"}
    assert set(put_response.json().keys()) == expected_keys
    assert put_response.json()["name"] == "Война миров"
    assert put_response.json()["author"] == "Герберт Уэлс"
    assert put_response.json()["year"] == 1990
    assert put_response.json()["ISBN"] == "isbn2"
    assert put_response.json()["count"] == 1

    get_response = await client.get("/api/v1/book", headers=headers)

    assert get_response.status_code == 200
    assert len(get_response.json()) == 1
    expected_keys = {"id", "name", "author", "year", "ISBN", "count"}
    assert set(get_response.json()[0].keys()) == expected_keys
    assert get_response.json()[0]["name"] == "Война миров"
    assert get_response.json()[0]["author"] == "Герберт Уэлс"
    assert get_response.json()[0]["year"] == 1990
    assert get_response.json()[0]["ISBN"] == "isbn2"
    assert get_response.json()[0]["count"] == 1