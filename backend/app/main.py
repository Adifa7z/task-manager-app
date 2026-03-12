from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from . import models
from .database import engine, get_db

# Create all tables in the database on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

# CORS — allows React (running on port 3000) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:3000",
    "https://compassionate-light-production.up.railway.app",
    "https://compassionate-light-production-8336.up.railway.app",
],
)

# --- Pydantic Schemas (what data looks like coming IN) ---
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    completed: bool

# --- API Routes ---

@app.get("/")
def root():
    return {"message": "Task Manager API is running!"}

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    """Get all tasks from the database"""
    tasks = db.query(models.Task).all()
    return tasks

@app.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    new_task = models.Task(
        title=task.title,
        description=task.description
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.patch("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate, db: Session = Depends(get_db)):
    """Mark a task complete or incomplete"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = update.completed
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": f"Task {task_id} deleted"}