from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_users(client):
    response = client.get("/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_missing_user(client):
    response = client.get("/users/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_create_user(client):
    user_data = {
        "username": "user tester",
        "email": "xyz@example.com",
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] is not None
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]