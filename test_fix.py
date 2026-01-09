
#!/usr/bin/env python3
"""
Test script to verify that the task creation works properly with the fixes.
This script simulates the frontend behavior to test the API connection.
"""

import requests
import json
import uuid

# Backend API URL
BASE_URL = "http://localhost:8000"

def test_api_connection():
    """Test basic API connection"""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("[OK] Backend API is accessible")
            return True
        else:
            print(f"[ERROR] Backend API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Could not connect to backend: {e}")
        return False

def test_health_check():
    """Test health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200 and response.json().get("status") == "healthy":
            print("[OK] Health check passed")
            return True
        else:
            print(f"[ERROR] Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Health check error: {e}")
        return False

def test_user_exists(user_id):
    """Test if a specific user exists by trying to get their tasks"""
    # Clean the user ID by removing hyphens to match backend format
    clean_user_id = user_id.replace('-', '')

    try:
        response = requests.get(f"{BASE_URL}/api/users/{clean_user_id}/tasks")
        if response.status_code == 200:
            print(f"[OK] User {clean_user_id} exists and is accessible")
            return True
        elif response.status_code == 404:
            print(f"[ERROR] User {clean_user_id} does not exist or is not found")
            return False
        else:
            print(f"[ERROR] Unexpected response for user {clean_user_id}: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Error checking user {clean_user_id}: {e}")
        return False

def test_create_task(user_id, token=None):
    """Test creating a task for a specific user"""
    # Clean the user ID by removing hyphens to match backend format
    clean_user_id = user_id.replace('-', '')

    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    task_data = {
        "title": "Test task from verification script",
        "description": "This is a test task to verify the fix works properly"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/users/{clean_user_id}/tasks",
            headers=headers,
            json=task_data
        )

        if response.status_code == 200:
            print(f"[OK] Successfully created task for user {clean_user_id}")
            return response.json()
        else:
            print(f"[ERROR] Failed to create task for user {clean_user_id}: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Error creating task for user {clean_user_id}: {e}")
        return None

def main():
    print("Testing task creation fix...")
    print("=" * 50)

    # Test basic connectivity
    if not test_api_connection():
        return

    if not test_health_check():
        return

    # Test with a known user ID from the database
    # From our earlier check, we know this user exists:
    # ('shahzadarham266@gmail.com', 'shahzad', 'hameed', '4398b2de2fa5413f93c44117d3c685da', ...)
    user_id = "4398b2de-2fa5-413f-93c4-4117d3c685da"  # With hyphens (as might be stored in frontend)

    print(f"\nTesting with user ID: {user_id}")
    print(f"Cleaned user ID (for API): {user_id.replace('-', '')}")

    # Test if the user exists with the cleaned ID
    if test_user_exists(user_id):
        # Try to create a test task
        result = test_create_task(user_id)
        if result:
            print(f"✓ Task creation test completed successfully!")
            print(f"  - Task ID: {result.get('id')}")
            print(f"  - Title: {result.get('title')}")
        else:
            print("✗ Task creation test failed")
    else:
        print("Cannot test task creation - user doesn't exist with cleaned ID")

    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    main()