from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("=" * 50)
print("DATABASE_URL:", DATABASE_URL)
print("=" * 50)

app = FastAPI(
    title="Task API",
    description="A simple CRUD API",
    version="1.0"
)

# Connect to PostgreSQL
connection = psycopg2.connect(DATABASE_URL)
connection.autocommit = True
cursor = connection.cursor(cursor_factory=RealDictCursor)

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
)
""")

# Insert sample data only if table is empty
cursor.execute("SELECT COUNT(*) AS count FROM tasks")
count = cursor.fetchone()["count"]

if count == 0:
    cursor.executemany(
        """
        INSERT INTO tasks (title, done)
        VALUES (%s, %s)
        """,
        [
            ("Study Python", False),
            ("Complete Assignment", False),
            ("Buy Milk", True)
        ]
    )


# Model
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

    cursor.execute("SELECT * FROM tasks ORDER BY id")

    return cursor.fetchall()


# Get one task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    task = cursor.fetchone()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return task


# Create task
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    cursor.execute(
        """
        INSERT INTO tasks (title, done)
        VALUES (%s, %s)
        RETURNING id
        """,
        (task.title, task.done)
    )

    new_id = cursor.fetchone()["id"]

    return {
        "id": new_id,
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
        SET title = %s,
            done = %s
        WHERE id = %s
        RETURNING id
        """,
        (
            updated_task.title,
            updated_task.done,
            task_id
        )
    )

    result = cursor.fetchone()

    if result is None:
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
        """
        DELETE FROM tasks
        WHERE id = %s
        RETURNING id
        """,
        (task_id,)
    )

    result = cursor.fetchone()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return