import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from server.api import app

@pytest.mark.asyncio
async def test_create_contact():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "job": "Developer",
            "email_address": "john.doe@example.com",
            "comment": "Test contact"
        }
        response = await ac.post("/contact/", json=payload)
        assert response.status_code == 200
        assert response.json()["first_name"] == "John"

@pytest.mark.asyncio
async def test_create_contact_missing_first_name():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "last_name": "Doe",
            "job": "Developer",
            "email_address": "john.doe@example.com",
            "comment": "Test contact"
        }
        response = await ac.post("/contact/", json=payload)
        assert response.status_code == 422  # Pydantic will raise a validation error

@pytest.mark.asyncio
async def test_create_contact_missing_last_name():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "first_name": "John",
            "job": "Developer",
            "email_address": "john.doe@example.com",
            "comment": "Test contact"
        }
        response = await ac.post("/contact/", json=payload)
        assert response.status_code == 422  # Pydantic will raise a validation error

@pytest.mark.asyncio
async def test_create_duplicate_contact():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "job": "Developer",
            "email_address": "john.doe@example.com",
            "comment": "Test contact"
        }
        response = await ac.post("/contact/", json=payload)
        assert response.status_code == 200

        response = await ac.post("/contact/", json=payload)
        assert response.status_code == 400
        assert response.json()["detail"] == "Contact with this firstname and lastname already exists"

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
async def test_get_contact_by_id():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create a contact to ensure there is one to retrieve
        payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "job": "Designer",
            "email_address": "jane.smith@example.com",
            "comment": "Another test contact"
        }
        create_response = await ac.post("/contact/", json=payload)
        assert create_response.status_code == 200
        contact_id = create_response.json()["id"]

        response = await ac.get(f"/contact/id/{contact_id}")
        assert response.status_code == 200
        assert response.json()["first_name"] == "Jane"
        assert response.json()["last_name"] == "Smith"

@pytest.mark.asyncio
async def test_get_contact_by_details_case_insensitive():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create contacts to ensure there are some to retrieve
        payload1 = {
            "first_name": "Jane",
            "last_name": "Smith",
            "job": "Designer",
            "email_address": "jane.smith@example.com",
            "comment": "Another test contact"
        }
        payload2 = {
            "first_name": "john",
            "last_name": "doe",
            "job": "Developer",
            "email_address": "john.doe@example.com",
            "comment": "Test contact"
        }
        await ac.post("/contact/", json=payload1)
        await ac.post("/contact/", json=payload2)

        # Test case-insensitive search by first name
        response = await ac.get("/contact/?first_name=jane")
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert response.json()[0]["first_name"].lower() == "jane"

        # Test case-insensitive search by last name
        response = await ac.get("/contact/?last_name=smith")
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert response.json()[0]["last_name"].lower() == "smith"

        # Test case-insensitive search by both first name and last name
        response = await ac.get("/contact/?first_name=jane&last_name=smith")
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert response.json()[0]["first_name"].lower() == "jane"
        assert response.json()[0]["last_name"].lower() == "smith"
