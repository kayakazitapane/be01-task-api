# Task API

A simple CRUD (Create, Read, Update, Delete) REST API built with **Python** and **FastAPI** for the FlyRank Backend AI Engineering Week 2 assignment.

## Features

- Create a task
- View all tasks
- View a task by ID
- Update a task
- Delete a task
- Health check endpoint
- Interactive Swagger API documentation

## Technologies Used

- Python 3.14
- FastAPI
- Uvicorn
- Pydantic

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/kayakazitapane/be01-task-api.git
```

### 2. Navigate into the project

```bash
cd be01-task-api
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install fastapi uvicorn
```

## Running the API

Start the server using:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | API information |
| GET | /health | Health check |
| GET | /tasks | Get all tasks |
| GET | /tasks/{task_id} | Get a task by ID |
| POST | /tasks | Create a new task |
| PUT | /tasks/{task_id} | Update a task |
| DELETE | /tasks/{task_id} | Delete a task |

## Example cURL Request

```bash
curl -i http://127.0.0.1:8000/tasks
```

Example Response

```http
HTTP/1.1 200 OK
content-type: application/json

[
  {
    "id": 1,
    "title": "Study Python",
    "done": false
  },
  {
    "id": 2,
    "title": "Complete Assignment",
    "done": false
  }
]
```

## Swagger Screenshot

Add a screenshot of your Swagger UI here.

Example:

```
docs/swagger.png
```

You can create a folder called **docs**, save your screenshot as **swagger.png**, and update this section like this:

![Swagger UI](docs/swagger.png)

## Project Structure

```
be01-task-api/
│── main.py
│── README.md
│── .gitignore
```

## Author

**Kayakazi Tapane**

GitHub: https://github.com/kayakazitapane