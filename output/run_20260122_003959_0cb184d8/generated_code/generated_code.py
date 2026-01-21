```python
import os
import logging
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, Field
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Todo model
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

# Pydantic models
class TodoCreate(BaseModel):
    title: str = Field(..., example="Buy groceries")
    description: str = Field(..., example="Milk, Bread, Eggs")
    priority: str = Field(..., regex="^(low|medium|high)$", example="medium")
    due_date: datetime = Field(..., example="2023-12-31T23:59:59")

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    due_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# FastAPI app setup
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")],
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

@app.on_event("startup")
async def startup():
    redis_url = os.getenv("REDIS_URL", "redis://localhost")
    await FastAPILimiter.init(redis_url=redis_url)

@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo item."""
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    logger.info(f"Created todo item with ID: {db_todo.id}")
    return db_todo

@app.get("/todos", response_model=List[TodoResponse], dependencies=[Depends(RateLimiter(times=100, seconds=60))])
async def read_todos(status: Optional[str] = Query(None, regex="^(pending|in_progress|completed)$"), 
                     priority: Optional[str] = Query(None, regex="^(low|medium|high)$"), 
                     skip: int = 0, 
                     limit: int = 10, 
                     db: Session = Depends(get_db)):
    """Retrieve all todo items with optional filtering and pagination."""
    query = db.query(Todo)
    if status:
        query = query.filter(Todo.status == status)
    if priority:
        query = query.filter(Todo.priority == priority)
    todos = query.offset(skip).limit(limit).all()
    logger.info(f"Retrieved {len(todos)} todo items")
    return todos

@app.get("/todos/{id}", response_model=TodoResponse)
async def read_todo(id: int, db: Session = Depends(get_db)):
    """Retrieve a specific todo item by ID."""
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        logger.error(f"Todo item with ID {id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found")
    return todo

@app.put("/todos/{id}", response_model=TodoResponse)
async def update_todo(id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    """Update a specific todo item."""
    db_todo = db.query(Todo).filter(Todo.id == id).first()
    if not db_todo:
        logger.error(f"Todo item with ID {id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found")
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    logger.info(f"Updated todo item with ID: {id}")
    return db_todo

@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(RateLimiter(times=100, seconds=60))])
async def delete_todo(id: int, db: Session = Depends(get_db)):
    """Delete a specific completed todo item."""
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        logger.error(f"Todo item with ID {id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found")
    if todo.status != 'completed':
        logger.error(f"Todo item with ID {id} is not completed and cannot be deleted")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only completed todo items can be deleted")
    db.delete(todo)
    db.commit()
    logger.info(f"Deleted todo item with ID: {id}")

@app.get("/todos/stats")
async def get_todo_stats(db: Session = Depends(get_db)):
    """Retrieve statistics on total, completed, and pending todos."""
    total = db.query(Todo).count()
    completed = db.query(Todo).filter(Todo.status == 'completed').count()
    pending = db.query(Todo).filter(Todo.status == 'pending').count()
    logger.info(f"Todo stats - Total: {total}, Completed: {completed}, Pending: {pending}")
    return {"total": total, "completed": completed, "pending": pending}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

This code addresses the issues identified in the review by implementing the necessary changes for correctness, security, performance, and readability. It includes proper error handling, input validation, and logging, making it production-ready and maintainable.