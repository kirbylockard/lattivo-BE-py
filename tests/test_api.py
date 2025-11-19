import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

# Reset in-memory DB between tests
from api.schemas.habits import store


# Reset in-memory DB before each test
@pytest.fixture(autouse=True)
def reset_db():
    """Reset HabitStore before each test."""
    store.reset()


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}


@pytest.mark.anyio
async def test_list_habits_empty():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/habits/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_create_habit():
    habit_data = {"name": "Drink Water", "description": "Stay hydrated"}
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/habits/", json=habit_data)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == habit_data["name"]
    assert data["description"] == habit_data["description"]


@pytest.mark.anyio
async def test_list_habits_after_creation():
    habit_data = {"name": "Drink Water", "description": "Stay hydrated"}
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        await ac.post("/habits/", json=habit_data)
        response = await ac.get("/habits/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["name"] == habit_data["name"]
    assert data[0]["description"] == habit_data["description"]
