from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="A simple CRUD API",
    version="1.0"
)

# Model for creating/updating a task
class TaskCreate(BaseModel):
    title: str
    done: bool = False

# In-memory list of tasks
tasks = [
    {"id": 1, "title": "Study Python", "done": False},
    {"id": 2, "title": "Complete Assignment", "done": False},
    {"id": 3, "title": "Buy Milk", "done": True}
]

# Root endpoint
@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# Get all tasks
@app.get("/tasks")
def get_tasks():
    return tasks

# Get one task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )

# Create task
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task

# Update task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskCreate):

    if updated_task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["done"] = updated_task.done
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )

# Delete task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )