from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Food Ordering CRUD App is running"


def test_create_food_item():
    response = client.post(
        "/items/",
        json={
            "name": "Burger",
            "description": "Cheese Burger",
            "price": 120,
            "category": "Fast Food",
            "available": True
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Burger"
    assert response.json()["price"] == 120


def test_view_menu():
    response = client.get("/items/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)