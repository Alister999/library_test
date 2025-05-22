import logging
import pytest
from httpx import AsyncClient

logger = logging.getLogger("ReaderTests")

@pytest.mark.asyncio
async def test_post_reader(client: AsyncClient):
    data = {"name": "Nikola", "email": "user@example.com", "password": "123"}
    login_data = {"email": "user@example.com", "password": "123"}
    reader_data = {"name": "Alex", "email": "user1@example.com"}
    await client.post("/api/v1/register", json=data)
    response = await client.post("/api/v1/login", json=login_data)
    my_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {my_token}"}
    post_response = await client.post("/api/v1/reader", json=reader_data, headers=headers)

    assert post_response.status_code == 200
    expected_keys = {"id", "name", "email"}
    assert set(post_response.json().keys()) == expected_keys
    assert post_response.json()["name"] == "Alex"
    assert post_response.json()["email"] == "user1@example.com"


@pytest.mark.asyncio
async def test_get_readers(client: AsyncClient):
    data = {"name": "Nikola", "email": "user@example.com", "password": "123"}
    login_data = {"email": "user@example.com", "password": "123"}
    reader_data = {"name": "Alex", "email": "user1@example.com"}
    await client.post("/api/v1/register", json=data)
    response = await client.post("/api/v1/login", json=login_data)
    my_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {my_token}"}
    await client.post("/api/v1/reader", json=reader_data, headers=headers)
    get_response = await client.get("/api/v1/reader", headers=headers)

    assert get_response.status_code == 200
    assert len(get_response.json()) == 1
    expected_keys = {"id", "name", "email"}
    assert set(get_response.json()[0].keys()) == expected_keys
    assert get_response.json()[0]["name"] == "Alex"
    assert get_response.json()[0]["email"] == "user1@example.com"


@pytest.mark.asyncio
async def test_get_reader(client: AsyncClient):
    data = {"name": "Nikola", "email": "user@example.com", "password": "123"}
    login_data = {"email": "user@example.com", "password": "123"}
    reader_data = {"name": "Alex", "email": "user1@example.com"}
    await client.post("/api/v1/register", json=data)
    response = await client.post("/api/v1/login", json=login_data)
    my_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {my_token}"}
    post_response = await client.post("/api/v1/reader", json=reader_data, headers=headers)
    reader_id = post_response.json()["id"]
    get_response = await client.get(f"/api/v1/reader/{reader_id}", headers=headers)

    assert get_response.status_code == 200
    expected_keys = {"id", "name", "email"}
    assert set(get_response.json().keys()) == expected_keys
    assert get_response.json()["name"] == "Alex"
    assert get_response.json()["email"] == "user1@example.com"


@pytest.mark.asyncio
async def test_delete_reader(client: AsyncClient):
    data = {"name": "Nikola", "email": "user@example.com", "password": "123"}
    login_data = {"email": "user@example.com", "password": "123"}
    reader_data = {"name": "Alex", "email": "user1@example.com"}
    await client.post("/api/v1/register", json=data)
    response = await client.post("/api/v1/login", json=login_data)
    my_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {my_token}"}
    post_response = await client.post("/api/v1/reader", json=reader_data, headers=headers)
    reader_id = post_response.json()["id"]

    get_response = await client.get(f"/api/v1/reader/{reader_id}", headers=headers)
    assert get_response.status_code == 200

    del_response = await client.delete(f"/api/v1/reader/{reader_id}", headers=headers)
    assert del_response.status_code == 200
    assert del_response.json() == {"message": f"Reader with id {reader_id} was deleted successful"}

    second_get_response = await client.get(f"/api/v1/reader/{reader_id}", headers=headers)
    assert second_get_response.status_code == 404


@pytest.mark.asyncio
async def test_put_reader(client: AsyncClient):
    data = {"name": "Nikola", "email": "user@example.com", "password": "123"}
    login_data = {"email": "user@example.com", "password": "123"}
    reader_data = {"name": "Alex", "email": "user1@example.com"}
    reader_data_2 = {"name": "Alexy", "email": "user2@example.com"}
    await client.post("/api/v1/register", json=data)
    response = await client.post("/api/v1/login", json=login_data)
    my_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {my_token}"}
    post_response = await client.post("/api/v1/reader", json=reader_data, headers=headers)
    reader_id = post_response.json()["id"]
    put_response = await client.put(f"/api/v1/reader/{reader_id}", json=reader_data_2, headers=headers)

    assert put_response.status_code == 200
    expected_keys = {"id", "name", "email"}
    assert set(put_response.json().keys()) == expected_keys
    assert put_response.json()["name"] == "Alexy"
    assert put_response.json()["email"] == "user2@example.com"

    get_response = await client.get("/api/v1/reader", headers=headers)

    assert get_response.status_code == 200
    assert len(get_response.json()) == 1
    expected_keys = {"id", "name", "email"}
    assert set(get_response.json()[0].keys()) == expected_keys
    assert get_response.json()[0]["name"] == "Alexy"
    assert get_response.json()[0]["email"] == "user2@example.com"