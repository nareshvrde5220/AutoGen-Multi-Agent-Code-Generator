# Todo List Manager REST API

## Overview
The Todo List Manager REST API is a web service built using FastAPI that provides CRUD operations for managing todo items. It allows users to create, read, update, and delete todo items, with features such as input validation, rate limiting, and logging. The API supports filtering and pagination, and provides statistics on todo items. It is designed to be easily integrated with frontend applications through CORS support.

## Installation
To install the necessary dependencies, run the following command:
```bash
pip install -r requirements.txt
```

## Architecture
The application is structured as follows:
- **FastAPI**: The web framework used to build the API.
- **SQLAlchemy**: ORM used for database interactions with an SQLite database.
- **Pydantic**: Used for data validation and serialization.
- **FastAPI-Limiter**: Implements rate limiting to control API request rates.
- **Logging**: Configured to log all operations for monitoring and debugging.

## API Reference

### Class: Todo
**Purpose:** Represents a todo item in the database with fields for title, description, status, priority, due date, and timestamps.

### Method: create_todo
**Parameters:**
- `todo` (TodoCreate): The todo item data to create.
- `db` (Session): Database session dependency.

**Returns:** TodoResponse - The created todo item.

**Raises:**
- HTTPException: If an error occurs during creation.

**Example:**
```python
response = await create_todo(todo=TodoCreate(title="Buy groceries", description="Milk, Bread, Eggs", priority="medium", due_date="2023-12-31T23:59:59"), db=db_session)
```

### Method: read_todos
**Parameters:**
- `status` (Optional[str]): Filter by status.
- `priority` (Optional[str]): Filter by priority.
- `skip` (int): Number of items to skip for pagination.
- `limit` (int): Maximum number of items to return.
- `db` (Session): Database session dependency.

**Returns:** List[TodoResponse] - List of todo items.

**Raises:**
- HTTPException: If an error occurs during retrieval.

**Example:**
```python
todos = await read_todos(status="pending", priority="medium", skip=0, limit=10, db=db_session)
```

### Method: read_todo
**Parameters:**
- `id` (int): ID of the todo item to retrieve.
- `db` (Session): Database session dependency.

**Returns:** TodoResponse - The requested todo item.

**Raises:**
- HTTPException: If the todo item is not found.

**Example:**
```python
todo = await read_todo(id=1, db=db_session)
```

### Method: update_todo
**Parameters:**
- `id` (int): ID of the todo item to update.
- `todo` (TodoCreate): Updated todo item data.
- `db` (Session): Database session dependency.

**Returns:** TodoResponse - The updated todo item.

**Raises:**
- HTTPException: If the todo item is not found.

**Example:**
```python
updated_todo = await update_todo(id=1, todo=TodoCreate(title="Buy groceries", description="Milk, Bread, Eggs", priority="high", due_date="2023-12-31T23:59:59"), db=db_session)
```

### Method: delete_todo
**Parameters:**
- `id` (int): ID of the todo item to delete.
- `db` (Session): Database session dependency.

**Returns:** None

**Raises:**
- HTTPException: If the todo item is not found or not completed.

**Example:**
```python
await delete_todo(id=1, db=db_session)
```

### Method: get_todo_stats
**Parameters:**
- `db` (Session): Database session dependency.

**Returns:** dict - Statistics on total, completed, and pending todos.

**Example:**
```python
stats = await get_todo_stats(db=db_session)
```

## Usage Examples
- **Creating a Todo Item:**
  ```python
  response = await create_todo(todo=TodoCreate(title="Buy groceries", description="Milk, Bread, Eggs", priority="medium", due_date="2023-12-31T23:59:59"), db=db_session)
  ```

- **Retrieving Todo Items:**
  ```python
  todos = await read_todos(status="pending", priority="medium", skip=0, limit=10, db=db_session)
  ```

- **Updating a Todo Item:**
  ```python
  updated_todo = await update_todo(id=1, todo=TodoCreate(title="Buy groceries", description="Milk, Bread, Eggs", priority="high", due_date="2023-12-31T23:59:59"), db=db_session)
  ```

- **Deleting a Todo Item:**
  ```python
  await delete_todo(id=1, db=db_session)
  ```

## Configuration
- **Environment Variables:**
  - `DATABASE_URL`: URL for the database connection (default: `sqlite:///./todo.db`).
  - `FRONTEND_ORIGIN`: Allowed origin for CORS (default: `http://localhost:3000`).
  - `REDIS_URL`: URL for Redis used in rate limiting (default: `redis://localhost`).

## Error Handling
- **HTTP 404 Not Found:** Raised when a todo item is not found.
- **HTTP 400 Bad Request:** Raised when attempting to delete a non-completed todo item.

## Best Practices
- Use environment variables to configure database and CORS settings.
- Ensure Redis is running for rate limiting to function.
- Log all operations for monitoring and debugging purposes.

## Troubleshooting
- **Database Connection Issues:** Ensure the `DATABASE_URL` is correctly set and the database is accessible.
- **Rate Limiting Not Working:** Verify that Redis is running and accessible at the specified `REDIS_URL`.
- **CORS Errors:** Check that `FRONTEND_ORIGIN` matches the origin of your frontend application.