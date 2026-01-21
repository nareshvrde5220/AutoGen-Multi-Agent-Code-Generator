# Todo List Manager API

## Overview
The Todo List Manager API is a FastAPI-based application designed to manage todo items with CRUD operations. It allows users to create, read, update, and delete todo items, with additional features such as filtering, pagination, and statistics retrieval. The API is built with a focus on maintainability, security, and performance, making it suitable for production environments.

## Installation
```bash
pip install -r requirements.txt
```

## Architecture
The application is structured around the FastAPI framework, using SQLAlchemy for database interactions and Pydantic for data validation. The main components are:

- **FastAPI Application**: Handles HTTP requests and responses.
- **SQLAlchemy ORM**: Manages database operations and models.
- **Pydantic Models**: Validates and serializes input and output data.
- **Logging**: Provides detailed logs for operations and errors.
- **CORS Middleware**: Configures cross-origin resource sharing.

## API Reference

### Class: TodoItem
**Purpose:** Represents a todo item in the database.

#### Attributes:
- `id` (Integer): Primary key.
- `title` (String): Title of the todo item.
- `description` (String, optional): Description of the todo item.
- `status` (Enum): Status of the todo item (pending, in_progress, completed).
- `priority` (Enum): Priority level (low, medium, high).
- `due_date` (DateTime, optional): Due date for the todo item.
- `created_at` (DateTime): Timestamp of creation.
- `updated_at` (DateTime): Timestamp of last update.

### Class: TodoCreate
**Purpose:** Pydantic model for creating a new todo item.

#### Attributes:
- `title` (str): Title of the todo item.
- `description` (Optional[str]): Description of the todo item.
- `priority` (PriorityEnum): Priority level.
- `due_date` (Optional[datetime]): Due date for the todo item.

### Class: TodoUpdate
**Purpose:** Pydantic model for updating an existing todo item.

#### Attributes:
- `title` (Optional[str]): Title of the todo item.
- `description` (Optional[str]): Description of the todo item.
- `status` (Optional[StatusEnum]): Status of the todo item.
- `priority` (Optional[PriorityEnum]): Priority level.
- `due_date` (Optional[datetime]): Due date for the todo item.

### Class: TodoResponse
**Purpose:** Pydantic model for todo item responses.

#### Attributes:
- `id` (int): ID of the todo item.
- `title` (str): Title of the todo item.
- `description` (Optional[str]): Description of the todo item.
- `status` (StatusEnum): Status of the todo item.
- `priority` (PriorityEnum): Priority level.
- `due_date` (Optional[datetime]): Due date for the todo item.
- `created_at` (datetime): Timestamp of creation.
- `updated_at` (datetime): Timestamp of last update.

### Endpoints

#### POST /todos
**Purpose:** Create a new todo item.

**Parameters:**
- `todo` (TodoCreate): Todo item data.

**Returns:** TodoResponse - The created todo item.

**Raises:**
- HTTPException: If there is a database error.

**Example:**
```python
response = await create_todo(todo=TodoCreate(title="New Task", priority=PriorityEnum.low))
```

#### GET /todos
**Purpose:** Retrieve a list of all todo items with optional filtering and pagination.

**Parameters:**
- `status` (Optional[StatusEnum]): Filter by status.
- `priority` (Optional[PriorityEnum]): Filter by priority.
- `skip` (int): Number of items to skip.
- `limit` (int): Maximum number of items to return.

**Returns:** List[TodoResponse] - List of todo items.

**Raises:**
- HTTPException: If there is a database error.

**Example:**
```python
response = await read_todos(status=StatusEnum.pending, limit=5)
```

#### GET /todos/{id}
**Purpose:** Retrieve a specific todo item by its ID.

**Parameters:**
- `id` (int): ID of the todo item.

**Returns:** TodoResponse - The requested todo item.

**Raises:**
- HTTPException: If the todo item is not found or there is a database error.

**Example:**
```python
response = await read_todo(id=1)
```

#### PUT /todos/{id}
**Purpose:** Update a specific todo item by its ID.

**Parameters:**
- `id` (int): ID of the todo item.
- `todo` (TodoUpdate): Updated todo item data.

**Returns:** TodoResponse - The updated todo item.

**Raises:**
- HTTPException: If the todo item is not found or there is a database error.

**Example:**
```python
response = await update_todo(id=1, todo=TodoUpdate(title="Updated Task"))
```

#### DELETE /todos/{id}
**Purpose:** Delete a specific todo item by its ID.

**Parameters:**
- `id` (int): ID of the todo item.

**Returns:** TodoResponse - The deleted todo item.

**Raises:**
- HTTPException: If the todo item is not found, not completed, or there is a database error.

**Example:**
```python
response = await delete_todo(id=1)
```

#### GET /todos/stats
**Purpose:** Retrieve statistics on todos, including total count, completed count, and pending count.

**Returns:** dict - Statistics on todo items.

**Raises:**
- HTTPException: If there is a database error.

**Example:**
```python
stats = await get_todo_stats()
```

## Usage Examples
```python
# Create a new todo item
new_todo = TodoCreate(title="Finish project", priority=PriorityEnum.high)
response = await create_todo(todo=new_todo)

# Retrieve all pending todo items
todos = await read_todos(status=StatusEnum.pending)

# Update a todo item
update_data = TodoUpdate(status=StatusEnum.completed)
updated_todo = await update_todo(id=1, todo=update_data)

# Delete a completed todo item
deleted_todo = await delete_todo(id=1)

# Get todo statistics
stats = await get_todo_stats()
```

## Configuration
- **Environment Variables:**
  - `DATABASE_URL`: URL for the database connection. Default is `sqlite:///./test.db`.
- **CORS Configuration:**
  - Allowed origins are specified in the middleware setup.

## Error Handling
- **HTTPException**: Raised for client and server errors with appropriate status codes.
- **SQLAlchemyError**: Caught and logged for database operation failures.

## Best Practices
- Use environment variables for sensitive configurations.
- Restrict CORS to specific domains.
- Handle exceptions gracefully and log errors.
- Use pagination for large datasets to improve performance.

## Troubleshooting
- **Database Connection Issues**: Ensure `DATABASE_URL` is correctly set.
- **CORS Errors**: Verify allowed origins in CORS middleware.
- **Invalid Data**: Check request payloads against Pydantic models for validation errors.
- **Server Errors**: Review logs for detailed error messages and stack traces.