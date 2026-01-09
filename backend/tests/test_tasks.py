import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import patch
from uuid import uuid4
import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from main import app
from database import get_session
from models import User, Task
from auth import auth_router

# Create a test database engine
engine = create_engine(
    "sqlite:///:memory:",
    echo=True,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

def get_test_session():
    """Get a test database session"""
    with Session(engine) as session:
        yield session

# Override the dependency to use the test session
app.dependency_overrides[get_session] = get_test_session

# Create a test client
client = TestClient(app)

@pytest.fixture
def setup_test_db():
    """Set up the test database with tables"""
    SQLModel.metadata.create_all(engine)
    yield
    # Cleanup after tests if needed
    SQLModel.metadata.drop_all(engine)

def test_create_user_and_task(setup_test_db):
    """Test creating a user and adding a task"""
    # Create a test user
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User"
    }

    response = client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

    user_id = data["id"]

    # Create a task for the user
    task_data = {
        "title": "Test Task",
        "description": "This is a test task"
    }

    response = client.post(f"/api/users/{user_id}/tasks", json=task_data)
    assert response.status_code == 200
    task = response.json()
    assert task["title"] == "Test Task"
    assert task["description"] == "This is a test task"
    assert task["user_id"] == user_id

def test_get_user_tasks(setup_test_db):
    """Test retrieving tasks for a user"""
    # Create a test user
    user_data = {
        "email": "test2@example.com",
        "password": "testpassword",
        "first_name": "Test2",
        "last_name": "User2"
    }

    response = client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 200
    data = response.json()
    user_id = data["id"]
    assert data["email"] == "test2@example.com"

    # Create a task for the user
    task_data = {
        "title": "Another Test Task",
        "description": "This is another test task"
    }

    response = client.post(f"/api/users/{user_id}/tasks", json=task_data)
    assert response.status_code == 200

    # Get the user's tasks
    response = client.get(f"/api/users/{user_id}/tasks")
    assert response.status_code == 200
    tasks_data = response.json()
    assert "tasks" in tasks_data
    assert len(tasks_data["tasks"]) == 1
    assert tasks_data["tasks"][0]["title"] == "Another Test Task"

def test_update_task(setup_test_db):
    """Test updating a task"""
    # Create a test user
    user_data = {
        "email": "test3@example.com",
        "password": "testpassword",
        "first_name": "Test3",
        "last_name": "User3"
    }

    response = client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 200
    data = response.json()
    user_id = data["id"]
    assert data["email"] == "test3@example.com"

    # Create a task for the user
    task_data = {
        "title": "Original Task",
        "description": "Original description"
    }

    response = client.post(f"/api/users/{user_id}/tasks", json=task_data)
    assert response.status_code == 200
    original_task = response.json()
    task_id = original_task["id"]
    assert original_task["title"] == "Original Task"

    # Update the task
    update_data = {
        "title": "Updated Task",
        "description": "Updated description",
        "is_completed": True
    }

    response = client.put(f"/api/users/{user_id}/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == "Updated Task"
    assert updated_task["description"] == "Updated description"
    assert updated_task["is_completed"] is True

def test_delete_task(setup_test_db):
    """Test deleting a task"""
    # Create a test user
    user_data = {
        "email": "test4@example.com",
        "password": "testpassword",
        "first_name": "Test4",
        "last_name": "User4"
    }

    response = client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 200
    data = response.json()
    user_id = data["id"]
    assert data["email"] == "test4@example.com"

    # Create a task for the user
    task_data = {
        "title": "Task to Delete",
        "description": "This task will be deleted"
    }

    response = client.post(f"/api/users/{user_id}/tasks", json=task_data)
    assert response.status_code == 200
    task = response.json()
    task_id = task["id"]
    assert task["title"] == "Task to Delete"

    # Delete the task
    response = client.delete(f"/api/users/{user_id}/tasks/{task_id}")
    assert response.status_code == 200

    # Verify the task is deleted by trying to get it
    response = client.get(f"/api/users/{user_id}/tasks/{task_id}")
    assert response.status_code == 404

def test_toggle_task_completion(setup_test_db):
    """Test toggling task completion status"""
    # Create a test user
    user_data = {
        "email": "test5@example.com",
        "password": "testpassword",
        "first_name": "Test5",
        "last_name": "User5"
    }

    response = client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 200
    data = response.json()
    user_id = data["id"]
    assert data["email"] == "test5@example.com"

    # Create a task for the user
    task_data = {
        "title": "Task to Toggle",
        "description": "This task will be toggled"
    }

    response = client.post(f"/api/users/{user_id}/tasks", json=task_data)
    assert response.status_code == 200
    task = response.json()
    task_id = task["id"]
    assert task["is_completed"] is False  # Should be false by default

    # Toggle the task completion
    completion_data = {
        "is_completed": True
    }

    response = client.patch(f"/api/users/{user_id}/tasks/{task_id}/complete", json=completion_data)
    assert response.status_code == 200
    toggled_task = response.json()
    assert toggled_task["is_completed"] is True

def test_user_cannot_access_other_user_task(setup_test_db):
    """Test that a user cannot access another user's task"""
    # Create first user
    user1_data = {
        "email": "user1@example.com",
        "password": "password1",
        "first_name": "User",
        "last_name": "One"
    }

    response = client.post("/api/auth/signup", json=user1_data)
    assert response.status_code == 200
    user1_data_response = response.json()
    user1_id = user1_data_response["id"]
    assert user1_data_response["email"] == "user1@example.com"

    # Create second user
    user2_data = {
        "email": "user2@example.com",
        "password": "password2",
        "first_name": "User",
        "last_name": "Two"
    }

    response = client.post("/api/auth/signup", json=user2_data)
    assert response.status_code == 200
    user2_data_response = response.json()
    user2_id = user2_data_response["id"]
    assert user2_data_response["email"] == "user2@example.com"

    # Create a task for user1
    task_data = {
        "title": "User1's Task",
        "description": "This is user1's task"
    }

    response = client.post(f"/api/users/{user1_id}/tasks", json=task_data)
    assert response.status_code == 200
    task = response.json()
    task_id = task["id"]
    assert task["title"] == "User1's Task"

    # Try to access user1's task as user2 (should fail with 403)
    response = client.get(f"/api/users/{user2_id}/tasks/{task_id}")
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]

    # Try to update user1's task as user2 (should fail with 403)
    update_data = {
        "title": "Attempted Update",
        "description": "Should not work"
    }

    response = client.put(f"/api/users/{user2_id}/tasks/{task_id}", json=update_data)
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]

    # Try to delete user1's task as user2 (should fail with 403)
    response = client.delete(f"/api/users/{user2_id}/tasks/{task_id}")
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]

    # Try to toggle user1's task completion as user2 (should fail with 403)
    completion_data = {
        "is_completed": True
    }

    response = client.patch(f"/api/users/{user2_id}/tasks/{task_id}/complete", json=completion_data)
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]

def test_invalid_user_id_format(setup_test_db):
    """Test that invalid user ID formats return appropriate errors"""
    # Try with an invalid UUID format
    invalid_user_id = "invalid-uuid"
    task_data = {
        "title": "Test Task",
        "description": "Test description"
    }

    response = client.post(f"/api/users/{invalid_user_id}/tasks", json=task_data)
    assert response.status_code == 400
    assert "Invalid user ID format" in response.json()["detail"]

    # Try getting tasks with invalid UUID
    response = client.get(f"/api/users/{invalid_user_id}/tasks")
    assert response.status_code == 400
    assert "Invalid user ID format" in response.json()["detail"]

def test_health_check(setup_test_db):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "API is running" in data["message"]

def test_signup_duplicate_email(setup_test_db):
    """Test that signing up with a duplicate email fails"""
    user_data = {
        "email": "duplicate@example.com",
        "password": "password",
        "first_name": "Duplicate",
        "last_name": "User"
    }

    # First signup should succeed
    response = client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 200

    # Second signup with same email should fail
    response = client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 409
    assert "Email already registered" in response.json()["detail"]