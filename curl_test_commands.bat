@echo off
REM Project Management API - cURL Test Commands (Windows)
REM Make sure the API server is running on http://localhost:8000

set BASE_URL=http://localhost:8000

echo 🚀 Project Management API - cURL Test Commands
echo ================================================

REM 1. User Signup
echo 1️⃣ Testing User Signup...
curl -X POST "%BASE_URL%/auth/signup" ^
  -H "Content-Type: application/json" ^
  -d "{\"username\": \"john_doe\", \"email\": \"john@example.com\", \"password\": \"securepassword123\"}"

echo.

REM 2. User Login
echo 2️⃣ Testing User Login...
curl -X POST "%BASE_URL%/auth/login" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\": \"john@example.com\", \"password\": \"securepassword123\"}" > login_response.json

echo Login completed. Check login_response.json for token.
echo.

REM Note: For Windows batch, you'll need to manually extract the token from login_response.json
REM and replace YOUR_TOKEN_HERE in the following commands

set ACCESS_TOKEN=YOUR_TOKEN_HERE

REM 3. Create Project
echo 3️⃣ Testing Create Project...
curl -X POST "%BASE_URL%/projects/" ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer %ACCESS_TOKEN%" ^
  -d "{\"title\": \"My Awesome Project\", \"description\": \"A collaborative project for our team\"}"

echo.

REM 4. Get User Projects
echo 4️⃣ Testing Get User Projects...
curl -X GET "%BASE_URL%/projects/" ^
  -H "Authorization: Bearer %ACCESS_TOKEN%"

echo.

REM 5. Get Project Details (replace 1 with actual project ID)
echo 5️⃣ Testing Get Project Details...
curl -X GET "%BASE_URL%/projects/1" ^
  -H "Authorization: Bearer %ACCESS_TOKEN%"

echo.

REM 6. Create Task (replace 1 with actual project ID)
echo 6️⃣ Testing Create Task...
curl -X POST "%BASE_URL%/tasks/" ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer %ACCESS_TOKEN%" ^
  -d "{\"title\": \"Implement user authentication\", \"description\": \"Add JWT-based authentication system\", \"project_id\": 1}"

echo.

REM 7. Get Project Tasks (replace 1 with actual project ID)
echo 7️⃣ Testing Get Project Tasks...
curl -X GET "%BASE_URL%/tasks/project/1" ^
  -H "Authorization: Bearer %ACCESS_TOKEN%"

echo.

REM 8. Update Task (replace 1 with actual task ID)
echo 8️⃣ Testing Update Task...
curl -X PUT "%BASE_URL%/tasks/1" ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer %ACCESS_TOKEN%" ^
  -d "{\"title\": \"Updated task title\", \"description\": \"Updated task description\", \"status\": \"in_progress\"}"

echo.

REM 9. Create Comment (replace 1 with actual task ID)
echo 9️⃣ Testing Create Comment...
curl -X POST "%BASE_URL%/comments/" ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer %ACCESS_TOKEN%" ^
  -d "{\"text\": \"This task is progressing well. Need to add unit tests.\", \"task_id\": 1}"

echo.

REM 10. Get Task Comments (replace 1 with actual task ID)
echo 🔟 Testing Get Task Comments...
curl -X GET "%BASE_URL%/comments/task/1" ^
  -H "Authorization: Bearer %ACCESS_TOKEN%"

echo.

echo ✅ All cURL tests completed!
echo ================================================
echo.
echo Note: Replace YOUR_TOKEN_HERE with the actual token from login_response.json
echo and update the IDs (1) with actual project/task IDs from the responses.

pause