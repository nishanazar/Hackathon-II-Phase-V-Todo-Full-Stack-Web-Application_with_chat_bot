import pytest
from fastapi.testclient import TestClient
from main import app
from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool
from db import get_db, engine
from datetime import datetime
from uuid import uuid4
from models import Task, PriorityEnum, RecurringIntervalEnum

# Create a test database
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(bind=engine)
    with sessionmaker(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture():
    def get_test_db():
        yield session

    app.dependency_overrides[get_db] = get_test_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_task_with_advanced_features(client: TestClient):
    """Test creating a task with due date, priority, tags, and recurring interval."""
    user_id = str(uuid4())
    
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "completed": False,
        "due_date": "2026-12-31T23:59:59",
        "priority": "high",
        "tags": ["test", "important"],
        "recurring_interval": "weekly"
    }
    
    response = client.post(f"/api/{user_id}/tasks/", json=task_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False
    assert data["due_date"] == "2026-12-31T23:59:59"
    assert data["priority"] == "high"
    assert data["tags"] == ["test", "important"]
    assert data["recurring_interval"] == "weekly"

def test_get_tasks_with_filters(client: TestClient):
    """Test getting tasks with various filters."""
    user_id = str(uuid4())
    
    # Create a few tasks with different attributes
    task_data_1 = {
        "title": "High Priority Task",
        "description": "Test Description",
        "completed": False,
        "due_date": "2026-12-31T23:59:59",
        "priority": "high",
        "tags": ["work", "urgent"],
        "recurring_interval": "daily"
    }
    
    task_data_2 = {
        "title": "Low Priority Task",
        "description": "Test Description",
        "completed": False,
        "due_date": "2026-11-30T23:59:59",
        "priority": "low",
        "tags": ["personal"],
        "recurring_interval": None
    }
    
    client.post(f"/api/{user_id}/tasks/", json=task_data_1)
    client.post(f"/api/{user_id}/tasks/", json=task_data_2)
    
    # Test filtering by priority
    response = client.get(f"/api/{user_id}/tasks/?priority_filter=high")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["priority"] == "high"
    
    # Test filtering by due date range
    response = client.get(f"/api/{user_id}/tasks/?due_date_from=2026-11-01T00:00:00&due_date_to=2026-12-01T23:59:59")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Low Priority Task"

def test_update_task_with_advanced_fields(client: TestClient):
    """Test updating a task with advanced fields."""
    user_id = str(uuid4())
    
    # Create a task first
    task_data = {
        "title": "Original Task",
        "description": "Original Description",
        "completed": False,
        "due_date": "2026-12-31T23:59:59",
        "priority": "medium",
        "tags": ["original"],
        "recurring_interval": None
    }
    
    response = client.post(f"/api/{user_id}/tasks/", json=task_data)
    assert response.status_code == 201
    task_id = response.json()["id"]
    
    # Update the task
    update_data = {
        "title": "Updated Task",
        "description": "Updated Description",
        "completed": True,
        "due_date": "2027-01-31T23:59:59",
        "priority": "high",
        "tags": ["updated", "important"],
        "recurring_interval": "monthly"
    }
    
    response = client.put(f"/api/{user_id}/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["completed"] is True
    assert data["priority"] == "high"
    assert "updated" in data["tags"]
    assert data["recurring_interval"] == "monthly"

def test_search_tasks(client: TestClient):
    """Test searching tasks by title or description."""
    user_id = str(uuid4())
    
    # Create tasks
    task_data_1 = {
        "title": "Marketing Report",
        "description": "Prepare quarterly marketing report",
        "completed": False,
        "due_date": "2026-12-31T23:59:59",
        "priority": "high",
        "tags": ["work", "report"],
        "recurring_interval": None
    }
    
    task_data_2 = {
        "title": "Grocery Shopping",
        "description": "Buy groceries for the week",
        "completed": False,
        "due_date": "2026-11-30T23:59:59",
        "priority": "medium",
        "tags": ["personal", "shopping"],
        "recurring_interval": "weekly"
    }
    
    client.post(f"/api/{user_id}/tasks/", json=task_data_1)
    client.post(f"/api/{user_id}/tasks/", json=task_data_2)
    
    # Search for "marketing" in title or description
    response = client.get(f"/api/{user_id}/tasks/search/?search_query=marketing")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "Marketing" in data[0]["title"]
    
    # Search for "groceries" in title or description
    response = client.get(f"/api/{user_id}/tasks/search/?search_query=groceries")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "Grocery" in data[0]["title"]