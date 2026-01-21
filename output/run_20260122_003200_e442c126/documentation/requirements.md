## Todo List Manager API

### Functional Requirements
- Implement CRUD operations for todo items:
  - Create new todo items with fields: title, description, priority (low/medium/high), and due date.
  - Read all todo items with optional filtering by status (pending/in_progress/completed) and priority.
  - Update existing todo items by their ID.
  - Delete todo items that are marked as completed.
- Provide an API endpoint for each CRUD operation:
  - `POST /todos`: Create a new todo item.
  - `GET /todos`: Retrieve a list of all todo items, with optional query parameters for filtering by status and priority.
  - `GET /todos/{id}`: Retrieve a specific todo item by its ID.
  - `PUT /todos/{id}`: Update a specific todo item by its ID.
  - `DELETE /todos/{id}`: Delete a specific todo item by its ID.
  - `GET /todos/stats`: Retrieve statistics on todos, including total count, completed count, and pending count.
- Validate input data using Pydantic models.
- Implement proper error handling with appropriate HTTP status codes.
- Implement rate limiting to allow a maximum of 100 requests per minute.
- Provide API documentation using Swagger UI.
- Enable logging for all API operations.
- Enable CORS to allow integration with frontend applications.

### Technical Specifications
- Programming Language: Python 3.10+
- Dependencies:
  - FastAPI
  - SQLAlchemy
  - SQLite
  - Pydantic
  - Swagger UI
  - Pytest
  - Docker
- Input Format:
  - JSON for request bodies in POST and PUT operations.
  - Query parameters for filtering in GET operations.
- Output Format:
  - JSON for all responses, including error messages.

### Acceptance Criteria
- The API must correctly perform CRUD operations as specified.
- The API must validate input data and return a 400 status code for invalid inputs.
- The API must handle errors gracefully and return appropriate HTTP status codes.
- The API must enforce a rate limit of 100 requests per minute and return a 429 status code if exceeded.
- The API must provide accurate Swagger UI documentation accessible at `/docs`.
- The API must log all operations with relevant details.
- The API must allow cross-origin requests from specified frontend domains.
- The API must pass all pytest test cases with a coverage of over 80%.
- The API must be deployable using Docker with a configurable database path via environment variables.

### Constraints & Assumptions
- The system will use an SQLite database for storage.
- SQLAlchemy ORM will be used for database interactions.
- The API will be deployed in a Docker container.
- Environment variables will be used for configuration, such as the database path.
- The system assumes a single user context for managing todos.

### Data Structures & Models
- Todo Item Model:
  - `id`: Integer, primary key
  - `title`: String, required
  - `description`: String, optional
  - `status`: Enum (pending, in_progress, completed), default to pending
  - `priority`: Enum (low, medium, high), required
  - `due_date`: DateTime, optional
  - `created_at`: DateTime, auto-generated
  - `updated_at`: DateTime, auto-generated