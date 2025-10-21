import pytest
from fastapi.testclient import TestClient

def test_signup(client: TestClient):
    response = client.post("/auth/signup", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_login(client: TestClient):
    # First create a user
    client.post("/auth/signup", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    
    # Then login
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient):
    response = client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401