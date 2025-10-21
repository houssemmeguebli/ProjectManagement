import pytest
from fastapi.testclient import TestClient

def setup_task_and_auth(client: TestClient):
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
    
    # Create task
    task_response = client.post(f"/projects/{project_id}/tasks", json={
        "title": "Test Task",
        "description": "A test task",
        "project_id": project_id
    }, headers=headers)
    print(f"Task response: {task_response.status_code}, {task_response.json()}")
    task_id = task_response.json()["id"]
    
    return headers, task_id

def test_create_comment(client: TestClient):
    headers, task_id = setup_task_and_auth(client)
    
    response = client.post(f"/tasks/{task_id}/comments", json={
        "text": "This is a test comment"
    }, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "This is a test comment"
    assert "task_id" in data or "id" in data

def test_get_task_comments(client: TestClient):
    headers, task_id = setup_task_and_auth(client)
    
    # Create a comment
    client.post(f"/tasks/{task_id}/comments", json={
        "text": "This is a test comment"
    }, headers=headers)
    
    response = client.get(f"/tasks/{task_id}/comments", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["text"] == "This is a test comment"