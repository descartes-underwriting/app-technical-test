import pytest
from httpx import AsyncClient
from server.api import app

@pytest.mark.asyncio
async def test_create_contact():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "job": "Developer",
            "email_address": "john.doe@mail.com",
            "comment": "Test contact"
        }
        response = await ac.post("/contact/", json=payload)
        assert response.status_code == 200
        assert response.json()["first_name"] == "John"

@pytest.mark.asyncio
async def test_list_contacts():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/contacts/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_list_contacts_with_pagination():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/contacts/?limit=2&offset=0")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) <= 2

@pytest.mark.asyncio
async def test_get_contact():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "job": "Designer",
            "email_address": "jane.smith@mail.com",
            "comment": "Another test contact"
        }
        create_response = await ac.post("/contact/", json=payload)
        contact_id = create_response.json()["id"]
        
        response = await ac.get(f"/contact/{contact_id}")
        assert response.status_code == 200
        assert response.json()["first_name"] == "Jane"
