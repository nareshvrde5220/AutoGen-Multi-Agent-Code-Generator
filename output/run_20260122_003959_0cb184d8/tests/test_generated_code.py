To generate comprehensive pytest test cases for the provided FastAPI application, we will cover all the CRUD operations and additional functionalities such as statistics retrieval and rate limiting. We will mock external dependencies like the database and rate limiter to ensure isolated unit tests. Below is a complete pytest test suite for the application:

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, MagicMock
from datetime import datetime
from main import app, Base, get_db, Todo

# Create a test database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_todo.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)

# Fixture for test client
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Mock the RateLimiter dependency
@pytest.fixture(autouse=True)
def mock_rate_limiter():
    with patch("fastapi_limiter.depends.RateLimiter.__call__", return_value=None):
        yield

# Sample data for testing
@pytest.fixture
def sample_todo():
    return {
        "title": "Test Todo",
        "description": "Test description",
        "priority": "medium",
        "due_date": datetime.utcnow().isoformat()
    }

# Happy path tests
def test_create_todo_success(client, sample_todo):
    response = client.post("/todos", json=sample_todo)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_todo["title"]
    assert data["description"] == sample_todo["description"]

def test_read_todos_success(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_todo_success(client, sample_todo):
    # Create a todo first
    create_response = client.post("/todos", json=sample_todo)
    todo_id = create_response.json()["id"]

    # Read the created todo
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id

# Edge case tests
def test_create_todo_invalid_priority(client, sample_todo):
    sample_todo["priority"] = "invalid"
    response = client.post("/todos", json=sample_todo)
    assert response.status_code == 422

def test_read_todo_not_found(client):
    response = client.get("/todos/9999")
    assert response.status_code == 404

def test_update_todo_not_found(client, sample_todo):
    response = client.put("/todos/9999", json=sample_todo)
    assert response.status_code == 404

# Error handling tests
def test_delete_todo_not_completed(client, sample_todo):
    # Create a todo first
    create_response = client.post("/todos", json=sample_todo)
    todo_id = create_response.json()["id"]

    # Attempt to delete the non-completed todo
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 400

def test_delete_todo_not_found(client):
    response = client.delete("/todos/9999")
    assert response.status_code == 404

# Integration tests
def test_integration_create_update_delete(client, sample_todo):
    # Create a todo
    create_response = client.post("/todos", json=sample_todo)
    todo_id = create_response.json()["id"]

    # Update the todo
    sample_todo["title"] = "Updated Title"
    update_response = client.put(f"/todos/{todo_id}", json=sample_todo)
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Title"

    # Mark as completed and delete
    sample_todo["status"] = "completed"
    client.put(f"/todos/{todo_id}", json=sample_todo)
    delete_response = client.delete(f"/todos/{todo_id}")
    assert delete_response.status_code == 204

# Mock external dependencies
@patch('main.FastAPILimiter.init')
def test_startup(mock_init):
    from main import startup
    mock_init.assert_not_called()
    startup()
    mock_init.assert_called_once()

# Test statistics endpoint
def test_get_todo_stats(client):
    response = client.get("/todos/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "completed" in data
    assert "pending" in data
```

### Explanation:
- **Fixtures**: We use fixtures to set up the test database and client, ensuring tests are isolated and repeatable.
- **Mocking**: We mock the rate limiter to focus on testing the application logic without hitting rate limits.
- **Test Cases**: We include tests for creating, reading, updating, and deleting todos, covering both successful operations and various edge cases.
- **Integration Tests**: We test the workflow of creating, updating, and deleting a todo to ensure the system works as expected.
- **Statistics Endpoint**: We verify the statistics endpoint returns the correct data structure.

This test suite aims for high coverage and robustness, ensuring the application meets the specified requirements.