#!/bin/bash
# Project Management API - cURL Test Commands
# Make sure the API server is running on http://localhost:8000

BASE_URL="http://localhost:8000"

echo "🚀 Project Management API - cURL Test Commands"
echo "================================================"

# 1. User Signup
echo "1️⃣ Testing User Signup..."
curl -X POST "$BASE_URL/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com", 
    "password": "securepassword123"
  }' | jq '.'

echo -e "\n"

# 2. User Login (save token for later use)
echo "2️⃣ Testing User Login..."
TOKEN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "securepassword123"}'

ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access_token')
echo "Login Response: $TOKEN_RESPONSE" | jq '.'
echo "Access Token: $ACCESS_TOKEN"

echo -e "\n"

# 3. Create Project
echo "3️⃣ Testing Create Project..."
PROJECT_RESPONSE=$(curl -s -X POST "$BASE_URL/projects/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "title": "My Awesome Project",
    "description": "A collaborative project for our team"
  }')

PROJECT_ID=$(echo $PROJECT_RESPONSE | jq -r '.id')
echo "Project Response: $PROJECT_RESPONSE" | jq '.'
echo "Project ID: $PROJECT_ID"

echo -e "\n"

# 4. Get User Projects
echo "4️⃣ Testing Get User Projects..."
curl -X GET "$BASE_URL/projects/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

echo -e "\n"

# 5. Get Project Details
echo "5️⃣ Testing Get Project Details..."
curl -X GET "$BASE_URL/projects/$PROJECT_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

echo -e "\n"

# 6. Create Task
echo "6️⃣ Testing Create Task..."
TASK_RESPONSE=$(curl -s -X POST "$BASE_URL/tasks/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d "{
    \"title\": \"Implement user authentication\",
    \"description\": \"Add JWT-based authentication system\",
    \"project_id\": $PROJECT_ID
  }")

TASK_ID=$(echo $TASK_RESPONSE | jq -r '.id')
echo "Task Response: $TASK_RESPONSE" | jq '.'
echo "Task ID: $TASK_ID"

echo -e "\n"

# 7. Get Project Tasks
echo "7️⃣ Testing Get Project Tasks..."
curl -X GET "$BASE_URL/tasks/project/$PROJECT_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

echo -e "\n"

# 8. Update Task
echo "8️⃣ Testing Update Task..."
curl -X PUT "$BASE_URL/tasks/$TASK_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "title": "Updated task title",
    "description": "Updated task description", 
    "status": "in_progress"
  }' | jq '.'

echo -e "\n"

# 9. Create Comment
echo "9️⃣ Testing Create Comment..."
curl -X POST "$BASE_URL/comments/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d "{
    \"text\": \"This task is progressing well. Need to add unit tests.\",
    \"task_id\": $TASK_ID
  }" | jq '.'

echo -e "\n"

# 10. Get Task Comments
echo "🔟 Testing Get Task Comments..."
curl -X GET "$BASE_URL/comments/task/$TASK_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

echo -e "\n"

# 11. Update Project
echo "1️⃣1️⃣ Testing Update Project..."
curl -X PUT "$BASE_URL/projects/$PROJECT_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "title": "Updated Project Title",
    "description": "Updated project description"
  }' | jq '.'

echo -e "\n"

# 12. Delete Task
echo "1️⃣2️⃣ Testing Delete Task..."
curl -X DELETE "$BASE_URL/tasks/$TASK_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'

echo -e "\n"
echo "✅ All cURL tests completed!"
echo "================================================"