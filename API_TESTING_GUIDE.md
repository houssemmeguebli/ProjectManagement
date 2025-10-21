# API Testing Guide

This guide provides multiple ways to test all the endpoints of the Project Management API.

## 🚀 Quick Start

1. **Start the API server:**
   ```bash
   uvicorn main:app --reload
   ```

2. **Access Swagger UI:**
   - Open http://localhost:8000/docs in your browser
   - Interactive API documentation with "Try it out" functionality

3. **Access ReDoc:**
   - Open http://localhost:8000/redoc in your browser
   - Alternative API documentation

## 📋 Testing Methods

### 1. Swagger UI (Recommended for Beginners)

**URL:** http://localhost:8000/docs

**Steps:**
1. Open the Swagger UI in your browser
2. Click on any endpoint to expand it
3. Click "Try it out" button
4. Fill in the required parameters
5. Click "Execute" to test the endpoint

**Authentication:**
1. First, use `/auth/signup` to create a user
2. Then use `/auth/login` to get an access token
3. Click the "Authorize" button at the top
4. Enter: `Bearer <your_access_token>`
5. Now you can test protected endpoints

### 2. Python Test Script

**File:** `test_api_endpoints.py`

```bash
# Install requests if not already installed
pip install requests

# Run the test script
python test_api_endpoints.py
```

This script will:
- Test all endpoints automatically
- Create test data (user, project, task, comment)
- Show success/failure for each endpoint
- Provide detailed output

### 3. cURL Commands

**Linux/Mac:** Use `curl_test_commands.sh`
```bash
chmod +x curl_test_commands.sh
./curl_test_commands.sh
```

**Windows:** Use `curl_test_commands.bat`
```cmd
curl_test_commands.bat
```

### 4. Postman Collection

**File:** `api_test_collection.json`

**Steps:**
1. Open Postman
2. Click "Import" 
3. Select `api_test_collection.json`
4. Set the `base_url` variable to `http://localhost:8000`
5. Run the "Authentication" folder first to get a token
6. Copy the access token to the `access_token` variable
7. Test other endpoints

### 5. Import OpenAPI Specification

**File:** `swagger.json`

You can import this file into:
- **Swagger Editor:** https://editor.swagger.io/
- **Postman:** Import > Upload Files
- **Insomnia:** Import/Export > Import Data
- **Any OpenAPI 3.0 compatible tool**

## 🔐 Authentication Flow

### Step 1: Create User Account
```bash
POST /auth/signup
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com", 
  "password": "securepassword123"
}
```

### Step 2: Login to Get Token
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Step 3: Use Token in Headers
```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 📝 Complete Testing Workflow

### 1. Authentication
- ✅ POST `/auth/signup` - Create user account
- ✅ POST `/auth/login` - Get access token

### 2. Project Management
- ✅ POST `/projects/` - Create a new project
- ✅ GET `/projects/` - Get user's projects
- ✅ GET `/projects/{id}` - Get project details
- ✅ PUT `/projects/{id}` - Update project (owner only)
- ✅ POST `/projects/{id}/contributors/{user_id}` - Add contributor

### 3. Task Management
- ✅ POST `/tasks/` - Create a new task
- ✅ GET `/tasks/project/{project_id}` - Get project tasks
- ✅ GET `/tasks/{id}` - Get task details
- ✅ PUT `/tasks/{id}` - Update task
- ✅ DELETE `/tasks/{id}` - Delete task

### 4. Comments
- ✅ POST `/comments/` - Create a comment
- ✅ GET `/comments/task/{task_id}` - Get task comments

## 🧪 Sample Test Data

### User Data
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpass123"
}
```

### Project Data
```json
{
  "title": "My Test Project",
  "description": "A project for testing the API"
}
```

### Task Data
```json
{
  "title": "Implement feature X",
  "description": "Add the new feature to the system",
  "project_id": 1,
  "assigned_user_id": 1
}
```

### Comment Data
```json
{
  "text": "This task is progressing well",
  "task_id": 1
}
```

## 🔍 Testing Checklist

### Authentication
- [ ] User can sign up with valid data
- [ ] User cannot sign up with duplicate username
- [ ] User can login with correct credentials
- [ ] User cannot login with wrong credentials
- [ ] Protected endpoints require valid token

### Projects
- [ ] User can create a project
- [ ] User can view their projects
- [ ] User can view project details
- [ ] Only project owner can update project
- [ ] Only project owner can add contributors

### Tasks
- [ ] User can create tasks in their projects
- [ ] User can view project tasks
- [ ] User can update task details and status
- [ ] User can delete tasks
- [ ] Task status changes correctly (todo → in_progress → done)

### Comments
- [ ] User can add comments to tasks
- [ ] User can view all comments on a task
- [ ] Comments show correct author and timestamp

### Security
- [ ] Endpoints require authentication
- [ ] Users can only access their own projects
- [ ] Contributors can access shared projects
- [ ] Proper error messages for unauthorized access

## 🐛 Troubleshooting

### Common Issues

**1. Server not running**
```
Error: Connection refused
Solution: Start the server with `uvicorn main:app --reload`
```

**2. Authentication errors**
```
Error: 401 Unauthorized
Solution: Make sure you're using a valid access token in the Authorization header
```

**3. Validation errors**
```
Error: 422 Unprocessable Entity
Solution: Check that your request body matches the expected schema
```

**4. Not found errors**
```
Error: 404 Not Found
Solution: Make sure you're using valid IDs that exist in the database
```

### Debug Tips

1. **Check server logs** for detailed error messages
2. **Use Swagger UI** to see expected request/response formats
3. **Verify token expiration** - tokens expire after 30 minutes by default
4. **Check database** - SQLite database file: `project_management.db`

## 📊 Performance Testing

For load testing, you can use tools like:
- **Apache Bench (ab)**
- **wrk**
- **Artillery**
- **Locust**

Example with Apache Bench:
```bash
# Test login endpoint with 100 requests, 10 concurrent
ab -n 100 -c 10 -p login_data.json -T application/json http://localhost:8000/auth/login
```

## 🔧 Advanced Testing

### Database Testing
```bash
# View database contents
sqlite3 project_management.db
.tables
SELECT * FROM users;
SELECT * FROM projects;
SELECT * FROM tasks;
SELECT * FROM comments;
```

### API Response Time Testing
```bash
# Test response times with curl
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/projects/
```

Create `curl-format.txt`:
```
     time_namelookup:  %{time_namelookup}\n
        time_connect:  %{time_connect}\n
     time_appconnect:  %{time_appconnect}\n
    time_pretransfer:  %{time_pretransfer}\n
       time_redirect:  %{time_redirect}\n
  time_starttransfer:  %{time_starttransfer}\n
                     ----------\n
          time_total:  %{time_total}\n
```

---

**Happy Testing! 🎉**

For questions or issues, check the API documentation at http://localhost:8000/docs