import pytest
from fastapi.testclient import TestClient

def get_auth_headers(client: TestClient, username: str = "testuser", password: str = "testpass123"):
    # Create user and login
    client.post("/auth/signup", json={
        "username": username,
        "email": f"{username}@example.com",
        "password": password
    })
    
    response = client.post("/auth/login", json={
        "email": f"{username}@example.com",
        "password": password
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_project(client: TestClient):
    headers = get_auth_headers(client)
    
    response = client.post("/projects/", json={
        "title": "Test Project",
        "description": "A test project"
    }, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Project"
    assert data["description"] == "A test project"

def test_get_user_projects(client: TestClient):
    headers = get_auth_headers(client)
    
    # Create a project
    client.post("/projects/", json={
        "title": "Test Project",
        "description": "A test project"
    }, headers=headers)
    
    response = client.get("/projects/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Project"

def test_unauthorized_access(client: TestClient):
    response = client.get("/projects/")
    assert response.status_code == 403