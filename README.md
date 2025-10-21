# Project Management API

A collaborative project management platform built with FastAPI, SQLAlchemy, and SQLite.

## Features

- **User Management**: Signup and login with JWT authentication
- **Project Management**: Create and manage projects with owners and contributors
- **Task Management**: Create, update, and track tasks within projects
- **Comment System**: Add comments to tasks for collaboration
- **Role-based Access Control**: Owner, contributor, and visitor permissions
- **Automatic API Documentation**: Swagger UI and ReDoc

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database
- **JWT**: JSON Web Tokens for authentication
- **Bcrypt**: Password hashing
- **Pytest**: Testing framework

## Project Structure

```
FastAPIProject/
├── app/
│   ├── core/           # Configuration and security
│   ├── db/             # Database setup
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── crud/           # Database operations
│   └── routers/        # API endpoints
├── tests/              # Test files
├── main.py             # Application entry point
└── requirements.txt    # Dependencies
```

## Setup Instructions

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd FastAPIProject
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API**:
   - API: http://localhost:8000
   - Interactive API docs (Swagger UI): http://localhost:8000/docs
   - Alternative API docs (ReDoc): http://localhost:8000/redoc

## Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app
```

Run specific test file:
```bash
pytest tests/test_auth.py
```

## API Endpoints

### Authentication
- `POST /auth/signup` - Register a new user
- `POST /auth/login` - Login and get access token

### Projects
- `POST /projects/` - Create a new project
- `GET /projects/` - Get user's projects
- `GET /projects/{project_id}` - Get project details
- `PUT /projects/{project_id}` - Update project (owner only)
- `POST /projects/{project_id}/contributors/{user_id}` - Add contributor (owner only)

### Tasks
- `POST /tasks/` - Create a new task
- `GET /tasks/project/{project_id}` - Get project tasks
- `GET /tasks/{task_id}` - Get task details
- `PUT /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task

### Comments
- `POST /comments/` - Create a comment
- `GET /comments/task/{task_id}` - Get task comments

## Usage Examples

### 1. Register a new user
```bash
curl -X POST "http://localhost:8000/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "email": "john@example.com",
       "password": "securepassword123"
     }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john_doe&password=securepassword123"
```

### 3. Create a project (with token)
```bash
curl -X POST "http://localhost:8000/projects/" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "My Awesome Project",
       "description": "A collaborative project for our team"
     }'
```

## Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Authentication**: Stateless authentication with configurable expiration
- **Role-based Access Control**: Different permissions for owners, contributors, and visitors
- **Input Validation**: Pydantic schemas ensure data integrity

## Configuration

Update `app/core/config.py` to modify:
- Secret key for JWT signing
- Token expiration time
- Database URL
- Other application settings

## Development

The application uses:
- **Hot reload**: Enabled with `--reload` flag
- **Automatic validation**: Pydantic schemas
- **Type hints**: Full type annotation support
- **Interactive docs**: Automatic OpenAPI documentation

## Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation as needed
4. Ensure all tests pass before submitting

## License

This project is open source and available under the MIT License.