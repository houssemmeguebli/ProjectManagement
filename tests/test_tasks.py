import pytest
from fastapi.testclient import TestClient

def setup_project_and_auth(client: TestClient):
    # Create user and login
    client.post("/auth/signup", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create project
    project_response = client.post("/projects/", json={
        "title": "Test Project",
        "description": "A test project"
    }, headers=headers)
    project_id = project_response.json()["id"]
    
    return headers, project_id

def test_create_task(client: TestClient):
    headers, project_id = setup_project_and_auth(client)
    
    response = client.post(f"/projects/{project_id}/tasks", json={
        "title": "Test Task",
        "description": "A test task",
        "project_id": project_id
    }, headers=headers)
    print(f"Task creation response: {response.status_code}, {response.json()}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert "project_id" in data or "id" in data
    assert data["status"] == "todo"

def test_get_project_tasks(client: TestClient):
    headers, project_id = setup_project_and_auth(client)
    
    # Create a task
    client.post(f"/projects/{project_id}/tasks", json={
        "title": "Test Task",
        "description": "A test task",
        "project_id": project_id
    }, headers=headers)
    
    response = client.get(f"/projects/{project_id}/tasks", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Task"