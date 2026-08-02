from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI(
    title="Task API",
    description="A simple CRUD API",
    version="1.0"
)

# Show the full database path
print("Database path:", os.path.abspath("tasks.db"))

# Connect to SQLite database
connection = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = connection.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done INTEGER NOT NULL
)
""")

connection.commit()

# Insert sample data only if the table is empty
cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    cursor.executemany("""
    INSERT INTO tasks (title, done)
    VALUES (?, ?)
    """, [
        ("Study Python", 0),
        ("Complete Assignment", 0),
        ("Buy Milk", 1)
    ])
    connection.commit()


# Model for creating/updating a task
class TaskCreate(BaseModel):
    title: str
    done: bool = False


# Root endpoint
@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


# Health endpoint
@app.get("/health")
def health():
    return {"status": "ok"}


# Get all tasks
@app.get("/tasks")
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])
        }
        for row in rows
    ]


# Get one task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2])
    }


# Create task
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title, int(task.done))
    )

    connection.commit()

    return {
        "id": cursor.lastrowid,
        "title": task.title,
        "done": task.done
    }


# Update task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskCreate):

    if updated_task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (
            updated_task.title,
            int(updated_task.done),
            task_id
        )
    )

    connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return {
        "id": task_id,
        "title": updated_task.title,
        "done": updated_task.done
    }


# Delete task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return