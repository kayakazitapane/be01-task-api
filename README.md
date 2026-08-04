# Task API

A simple CRUD Task API built with FastAPI and PostgreSQL running in Docker.

## Features

- Create tasks
- Read all tasks
- Read a single task
- Update tasks
- Delete tasks
- Data persists after application and container restarts
- PostgreSQL database running in Docker

## Technologies

- Python
- FastAPI
- PostgreSQL
- Docker
- Docker Compose
- psycopg2
- python-dotenv

## Why PostgreSQL?

PostgreSQL was chosen because it is a powerful relational database commonly used in production applications. Running it inside Docker provides a consistent development environment and makes the application easy to set up on any machine.

## Project Structure

```
CodeBE01/
│── main.py
│── docker-compose.yml
│── .env.example
│── README.md
│── docs/
│   ├── docker-container.png
│   ├── swagger-ui.png
```

## Environment Variables

Create a `.env` file using `.env.example`.

Example:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=tasksdb
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tasksdb
```

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/kayakazitapane/be01-task-api.git
```

### 2. Navigate into the project

```bash
cd CodeBE01
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install fastapi uvicorn psycopg2-binary python-dotenv
```

### 6. Start PostgreSQL

```bash
docker compose up -d
```

### 7. Start the API

```bash
uvicorn main:app --reload
```

### 8. Open Swagger UI

```
http://127.0.0.1:8000/docs
```

## Database

- PostgreSQL 17
- Running inside Docker
- Data stored in a Docker volume
- Database and table are created automatically if they do not exist
- Three sample tasks are inserted only on the first run

## Persistence Test

The application was tested by:

1. Creating a new task.
2. Stopping the FastAPI application.
3. Stopping the PostgreSQL Docker container.
4. Restarting both the container and the application.
5. Confirming that the created task still existed.

This demonstrates that the data is permanently stored in PostgreSQL.

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get one task |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

## Screenshots

### Swagger UI

![Swagger UI](docs/docsswagger.png)

### Docker Container Running

![Docker Container](docs/docker-container.png)

### Tasks in PostgreSQL

![PostgreSQL Tasks](docs/sqlite-database.png)