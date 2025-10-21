"""
Swagger/OpenAPI examples and documentation enhancements
"""

# Example request bodies for Swagger documentation
swagger_examples = {
    "user_signup": {
        "summary": "User Signup Example",
        "description": "Create a new user account",
        "value": {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "securepassword123"
        }
    },
    "user_login": {
        "summary": "User Login Example", 
        "description": "Login with email and password",
        "value": {
            "email": "john@example.com",
            "password": "securepassword123"
        }
    },
    "project_create": {
        "summary": "Create Project Example",
        "description": "Create a new project",
        "value": {
            "title": "My Awesome Project",
            "description": "A collaborative project for our team"
        }
    },
    "project_update": {
        "summary": "Update Project Example",
        "description": "Update project details",
        "value": {
            "title": "Updated Project Title",
            "description": "Updated project description"
        }
    },
    "task_create": {
        "summary": "Create Task Example",
        "description": "Create a new task in a project",
        "value": {
            "title": "Implement user authentication",
            "description": "Add JWT-based authentication system",
            "project_id": 1,
            "assigned_user_id": 2
        }
    },
    "task_update": {
        "summary": "Update Task Example",
        "description": "Update task details and status",
        "value": {
            "title": "Updated task title",
            "description": "Updated task description",
            "status": "in_progress",
            "assigned_user_id": 3
        }
    },
    "comment_create": {
        "summary": "Create Comment Example",
        "description": "Add a comment to a task",
        "value": {
            "text": "This task is progressing well. Need to add unit tests.",
            "task_id": 1
        }
    }
}