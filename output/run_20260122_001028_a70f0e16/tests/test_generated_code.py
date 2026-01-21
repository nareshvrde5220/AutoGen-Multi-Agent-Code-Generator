Below is a comprehensive set of pytest test cases for the provided FastAPI application. These tests cover the CRUD operations, edge cases, error handling, and integration scenarios. External dependencies such as the database are mocked to ensure isolated unit testing.

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import patch, MagicMock
from datetime import datetime
from main import app, get_db, Base, TodoItem, StatusEnum, PriorityEnum

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test client
client = TestClient(app)

# Override the get_db dependency
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

app.dependency_overrides[get_db] = db_session

# Fixtures for test data
@pytest.fixture
def sample_todo():
    return {
        "title": "Test Todo",
        "description": "Description for test todo",
        "priority": "medium",
        "due_date": datetime.utcnow().isoformat()
    }

@pytest.fixture
def sample_todo_item(db_session):
    todo_item = TodoItem(
        title="Existing Todo",
        description="Existing description",
        status=StatusEnum.pending,
        priority=PriorityEnum.medium,
        due_date=datetime.utcnow()
    )
    db_session.add(todo_item)
    db_session.commit()
    db_session.refresh(todo_item)
    return todo_item

# Test cases for create_todo
def test_create_todo_success(sample_todo):
    response = client.post("/todos", json=sample_todo)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == sample_todo["title"]
    assert data["priority"] == sample_todo["priority"]

def test_create_todo_invalid_priority(sample_todo):
    sample_todo["priority"] = "invalid_priority"
    response = client.post("/todos", json=sample_todo)
    assert response.status_code == 422

def test_create_todo_missing_title(sample_todo):
    del sample_todo["title"]
    response = client.post("/todos", json=sample_todo)
    assert response.status_code == 422

# Test cases for read_todos
def test_read_todos_success(sample_todo_item):
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_read_todos_filter_by_status(sample_todo_item):
    response = client.get("/todos", params={"status": "pending"})
    assert response.status_code == 200
    data = response.json()
    assert all(todo["status"] == "pending" for todo in data)

def test_read_todos_pagination(sample_todo_item):
    response = client.get("/todos", params={"skip": 0, "limit": 1})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

# Test cases for read_todo
def test_read_todo_success(sample_todo_item):
    response = client.get(f"/todos/{sample_todo_item.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_todo_item.id

def test_read_todo_not_found():
    response = client.get("/todos/9999")
    assert response.status_code == 404

# Test cases for update_todo
def test_update_todo_success(sample_todo_item):
    update_data = {"title": "Updated Title"}
    response = client.put(f"/todos/{sample_todo_item.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]

def test_update_todo_not_found():
    update_data = {"title": "Updated Title"}
    response = client.put("/todos/9999", json=update_data)
    assert response.status_code == 404

# Test cases for delete_todo
def test_delete_todo_success(db_session, sample_todo_item):
    sample_todo_item.status = StatusEnum.completed
    db_session.commit()
    response = client.delete(f"/todos/{sample_todo_item.id}")
    assert response.status_code == 200

def test_delete_todo_not_completed(sample_todo_item):
    response = client.delete(f"/todos/{sample_todo_item.id}")
    assert response.status_code == 400

def test_delete_todo_not_found():
    response = client.delete("/todos/9999")
    assert response.status_code == 404

# Test cases for get_todo_stats
def test_get_todo_stats(db_session):
    response = client.get("/todos/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "completed" in data
    assert "pending" in data

# Mocking external dependencies
@patch('main.SessionLocal', return_value=MagicMock())
def test_create_todo_db_error(mock_db, sample_todo):
    mock_db.side_effect = SQLAlchemyError
    response = client.post("/todos", json=sample_todo)
    assert response.status_code == 500

@patch('main.SessionLocal', return_value=MagicMock())
def test_read_todos_db_error(mock_db):
    mock_db.side_effect = SQLAlchemyError
    response = client.get("/todos")
    assert response.status_code == 500

# Integration tests
def test_integration_create_and_read_todo():
    todo_data = {
        "title": "Integration Test Todo",
        "description": "Integration test description",
        "priority": "low",
        "due_date": datetime.utcnow().isoformat()
    }
    create_response = client.post("/todos", json=todo_data)
    assert create_response.status_code == 200
    created_todo = create_response.json()

    read_response = client.get(f"/todos/{created_todo['id']}")
    assert read_response.status_code == 200
    read_todo = read_response.json()
    assert read_todo["title"] == todo_data["title"]

```

### Explanation:
- **Fixtures**: Used to set up a test database and provide sample data for tests.
- **TestClient**: Utilized to simulate HTTP requests to the FastAPI application.
- **Mocking**: SQLAlchemy session is mocked to simulate database errors.
- **CRUD Tests**: Each CRUD operation is tested for success, failure, and edge cases.
- **Integration Tests**: Ensure that creating and reading a todo item works seamlessly.
- **Error Handling**: Tests ensure appropriate HTTP status codes are returned for errors.

These tests aim to cover over 80% of the code, focusing on both positive and negative scenarios, ensuring the API meets the specified requirements.