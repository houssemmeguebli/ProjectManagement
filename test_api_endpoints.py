#!/usr/bin/env python3
"""
API Endpoint Testing Script
Tests all endpoints of the Project Management API
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

class APITester:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.access_token = None
        self.user_id = None
        self.project_id = None
        self.task_id = None
        
    def test_user_signup(self):
        """Test user registration"""
        print("🔹 Testing User Signup...")
        url = f"{self.base_url}/auth/signup"
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            self.user_id = result["id"]
            print(f"✅ User created successfully: {result['username']}")
            return True
        else:
            print(f"❌ Signup failed: {response.text}")
            return False
    
    def test_user_login(self):
        """Test user authentication"""
        print("🔹 Testing User Login...")
        url = f"{self.base_url}/auth/login"
        data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            self.access_token = result["access_token"]
            print(f"✅ Login successful, token received")
            return True
        else:
            print(f"❌ Login failed: {response.text}")
            return False
    
    def get_headers(self):
        """Get authorization headers"""
        return {"Authorization": f"Bearer {self.access_token}"}
    
    def test_create_project(self):
        """Test project creation"""
        print("🔹 Testing Create Project...")
        url = f"{self.base_url}/projects/"
        data = {
            "title": "Test Project",
            "description": "A test project for API testing"
        }
        
        response = requests.post(url, json=data, headers=self.get_headers())
        if response.status_code == 200:
            result = response.json()
            self.project_id = result["id"]
            print(f"✅ Project created: {result['title']}")
            return True
        else:
            print(f"❌ Project creation failed: {response.text}")
            return False
    
    def test_get_projects(self):
        """Test getting user projects"""
        print("🔹 Testing Get User Projects...")
        url = f"{self.base_url}/projects/"
        
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Retrieved {len(result)} projects")
            return True
        else:
            print(f"❌ Get projects failed: {response.text}")
            return False
    
    def test_create_task(self):
        """Test task creation"""
        print("🔹 Testing Create Task...")
        url = f"{self.base_url}/tasks/"
        data = {
            "title": "Test Task",
            "description": "A test task for API testing",
            "project_id": self.project_id
        }
        
        response = requests.post(url, json=data, headers=self.get_headers())
        if response.status_code == 200:
            result = response.json()
            self.task_id = result["id"]
            print(f"✅ Task created: {result['title']}")
            return True
        else:
            print(f"❌ Task creation failed: {response.text}")
            return False
    
    def test_get_project_tasks(self):
        """Test getting project tasks"""
        print("🔹 Testing Get Project Tasks...")
        url = f"{self.base_url}/tasks/project/{self.project_id}"
        
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Retrieved {len(result)} tasks")
            return True
        else:
            print(f"❌ Get tasks failed: {response.text}")
            return False
    
    def test_update_task(self):
        """Test task update"""
        print("🔹 Testing Update Task...")
        url = f"{self.base_url}/tasks/{self.task_id}"
        data = {
            "title": "Updated Test Task",
            "status": "in_progress"
        }
        
        response = requests.put(url, json=data, headers=self.get_headers())
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Task updated: {result['title']} - {result['status']}")
            return True
        else:
            print(f"❌ Task update failed: {response.text}")
            return False
    
    def test_create_comment(self):
        """Test comment creation"""
        print("🔹 Testing Create Comment...")
        url = f"{self.base_url}/comments/"
        data = {
            "text": "This is a test comment for API testing",
            "task_id": self.task_id
        }
        
        response = requests.post(url, json=data, headers=self.get_headers())
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Comment created: {result['text'][:50]}...")
            return True
        else:
            print(f"❌ Comment creation failed: {response.text}")
            return False
    
    def test_get_task_comments(self):
        """Test getting task comments"""
        print("🔹 Testing Get Task Comments...")
        url = f"{self.base_url}/comments/task/{self.task_id}"
        
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Retrieved {len(result)} comments")
            return True
        else:
            print(f"❌ Get comments failed: {response.text}")
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting API Endpoint Tests...")
        print("=" * 50)
        
        tests = [
            self.test_user_signup,
            self.test_user_login,
            self.test_create_project,
            self.test_get_projects,
            self.test_create_task,
            self.test_get_project_tasks,
            self.test_update_task,
            self.test_create_comment,
            self.test_get_task_comments
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
                time.sleep(0.5)  # Small delay between tests
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
        
        print("=" * 50)
        print(f"🏁 Tests completed: {passed}/{total} passed")
        
        if passed == total:
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed. Check the API server and try again.")

def main():
    """Main function to run API tests"""
    print("Project Management API - Endpoint Tester")
    print("Make sure the API server is running on http://localhost:8000")
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ API server is running")
        else:
            print("❌ API server responded with error")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Make sure it's running on http://localhost:8000")
        return
    
    # Run tests
    tester = APITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()