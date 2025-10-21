#!/usr/bin/env python3
"""
Test script for signup endpoint
"""

import requests
import json

def test_signup():
    url = "http://localhost:8000/auth/signup"
    data = {
        "username": "testuser",
        "email": "test@example.com", 
        "password": "testpass123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to server. Make sure it's running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing signup endpoint...")
    success = test_signup()
    if success:
        print("✅ Signup test passed!")
    else:
        print("❌ Signup test failed!")