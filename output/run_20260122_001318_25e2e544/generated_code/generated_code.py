```python
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
from enum import Enum as PyEnum
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable is not set.")
    raise RuntimeError("DATABASE_URL environment variable is required.")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Enum definitions
class StatusEnum(PyEnum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class PriorityEnum(PyEnum):
    low = "low"
    medium = "medium"
    high = "high"

# Database model
class TodoItem(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    priority = Column(Enum(PriorityEnum))
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic models
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: PriorityEnum
    due_date: Optional[datetime] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[datetime] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: StatusEnum
    priority: PriorityEnum
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# FastAPI app setup
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://yourdomain.com"],  # Restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations
@app.post("/todos", response_model=TodoResponse)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)) -> TodoResponse:
    """Create a new todo item."""
    try:
        db_todo = TodoItem(**todo.dict())
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        logger.info("Created new todo item with ID %d", db_todo.id)
        return db_todo
    except SQLAlchemyError as e:
        logger.error("Error creating todo item: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/todos", response_model=List[TodoResponse])
async def read_todos(
    status: Optional[StatusEnum] = Query(None),
    priority: Optional[PriorityEnum] = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> List[TodoResponse]:
    """Retrieve a list of all todo items with optional filtering and pagination."""
    try:
        query = db.query(TodoItem)
        if status:
            query = query.filter(TodoItem.status == status)
        if priority:
            query = query.filter(TodoItem.priority == priority)
        todos = query.offset(skip).limit(limit).all()
        logger.info("Retrieved %d todo items", len(todos))
        return todos
    except SQLAlchemyError as e:
        logger.error("Error retrieving todo items: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/todos/{id}", response_model=TodoResponse)
async def read_todo(id: int, db: Session = Depends(get_db)) -> TodoResponse:
    """Retrieve a specific todo item by its ID."""
    try:
        todo = db.query(TodoItem).filter(TodoItem.id == id).first()
        if not todo:
            logger.warning("Todo item with ID %d not found", id)
            raise HTTPException(status_code=404, detail="Todo item not found")
        return todo
    except SQLAlchemyError as e:
        logger.error("Error retrieving todo item: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put("/todos/{id}", response_model=TodoResponse)
async def update_todo(id: int, todo: TodoUpdate, db: Session = Depends(get_db)) -> TodoResponse:
    """Update a specific todo item by its ID."""
    try:
        db_todo = db.query(TodoItem).filter(TodoItem.id == id).first()
        if not db_todo:
            logger.warning("Todo item with ID %d not found", id)
            raise HTTPException(status_code=404, detail="Todo item not found")
        for key, value in todo.dict(exclude_unset=True).items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
        logger.info("Updated todo item with ID %d", id)
        return db_todo
    except SQLAlchemyError as e:
        logger.error("Error updating todo item: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete("/todos/{id}", response_model=TodoResponse)
async def delete_todo(id: int, db: Session = Depends(get_db)) -> TodoResponse:
    """Delete a specific todo item by its ID."""
    try:
        db_todo = db.query(TodoItem).filter(TodoItem.id == id).first()
        if not db_todo:
            logger.warning("Todo item with ID %d not found", id)
            raise HTTPException(status_code=404, detail="Todo item not found")
        if db_todo.status != StatusEnum.completed:
            logger.warning("Todo item with ID %d is not completed and cannot be deleted", id)
            raise HTTPException(status_code=400, detail="Only completed todo items can be deleted")
        db.delete(db_todo)
        db.commit()
        logger.info("Deleted todo item with ID %d", id)
        return db_todo
    except SQLAlchemyError as e:
        logger.error("Error deleting todo item: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/todos/stats")
async def get_todo_stats(db: Session = Depends(get_db)) -> dict:
    """Retrieve statistics on todos, including total count, completed count, and pending count."""
    try:
        total = db.query(TodoItem).count()
        completed = db.query(TodoItem).filter(TodoItem.status == StatusEnum.completed).count()
        pending = db.query(TodoItem).filter(TodoItem.status == StatusEnum.pending).count()
        logger.info("Retrieved todo statistics")
        return {"total": total, "completed": completed, "pending": pending}
    except SQLAlchemyError as e:
        logger.error("Error retrieving todo statistics: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Initialize database
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

This code addresses the feedback by implementing a more secure CORS policy, adding pagination to the `read_todos` endpoint, validating environment variables, and ensuring consistent logging. It also includes error handling for database operations and uses Pydantic models for input validation. The code is structured to be maintainable and efficient, following best practices for a production-ready FastAPI application.