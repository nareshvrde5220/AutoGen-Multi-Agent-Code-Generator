## Todo List Manager REST API

### Functional Requirements
- Implement CRUD operations for todo items:
  - Create new todo items with fields: title, description, priority (low/medium/high), and due date.
  - Read all todo items with optional filtering by status and priority.
  - Update existing todo items.
  - Delete completed todo items.
- Develop a data model for todo items with attributes: id, title, description, status (pending/in_progress/completed), priority, due_date, created_at, updated_at.
- Provide API endpoints:
  - `POST /todos` to create a new todo item.
  - `GET /todos` to list all todo items with optional query parameters for filtering.
  - `GET /todos/{id}` to retrieve a specific todo item.
  - `PUT /todos/{id}` to update a specific todo item.
  - `DELETE /todos/{id}` to delete a specific todo item.
  - `GET /todos/stats` to retrieve statistics on total, completed, and pending todos.
- Implement input validation using Pydantic models.
- Ensure proper error handling with appropriate HTTP status codes.
- Implement rate limiting to allow a maximum of 100 requests per minute.
- Provide API documentation using Swagger UI.
- Enable logging for all operations.
- Enable CORS for frontend integration.

### Technical Specifications
- Programming Language: Python 3.10+
- Dependencies: FastAPI, SQLAlchemy, SQLite, Pydantic, pytest, Docker, Swagger UI, CORS middleware
- Input Format: JSON for request bodies
- Output Format: JSON for responses

### Acceptance Criteria
- CRUD operations should be functional and adhere to the specified data model.
- API endpoints should return correct HTTP status codes and messages.
- Input validation should prevent invalid data from being processed.
- Rate limiting should restrict requests to 100 per minute.
- Swagger UI should be accessible for API documentation.
- Logs should capture all operations with relevant details.
- CORS should allow requests from the specified frontend origin.
- Test coverage should be greater than 80% using pytest.
- The application should be deployable using Docker.

### Constraints & Assumptions
- SQLite is used as the database for simplicity and local development.
- It is assumed that the frontend will handle user authentication and authorization.
- The system will be deployed in a containerized environment using Docker.
- Environment variables will be used to configure the database path.

### Data Structures & Models
- Todo Model:
  ```python
  class Todo(Base):
      __tablename__ = 'todos'
      id = Column(Integer, primary_key=True, index=True)
      title = Column(String, index=True)
      description = Column(String)
      status = Column(Enum('pending', 'in_progress', 'completed', name='status_enum'), default='pending')
      priority = Column(Enum('low', 'medium', 'high', name='priority_enum'), default='medium')
      due_date = Column(DateTime)
      created_at = Column(DateTime, default=datetime.utcnow)
      updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  ```