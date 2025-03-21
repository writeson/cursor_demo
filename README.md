# Cursor Demo FastAPI Project

A modern FastAPI application with async SQLite database access using SQLModel and aiosqlite.

## Features

- Modern Python 3.12.7
- FastAPI with async endpoints
- SQLModel ORM with async SQLite database
- Clean architecture with separation of concerns
- Type hints and comprehensive documentation
- Pytest-based testing framework
- Docker containerization
- Pre-commit hooks

## Project Structure

```
/
├── project/                  # Project package
│   ├── db/                   # Database directory
│   ├── src/                  # Source code
│   │   ├── endpoints/        # API endpoints
│   │   └── main.py           # FastAPI application
│   └── database.py           # Database models and operations
├── tests/                    # Test cases
├── docs/                     # Documentation
│   └── architecture/         # Architecture documentation
├── .python-version           # Python version specification
├── .gitignore                # Git ignore file
├── pyproject.toml            # Project dependencies and config
├── Dockerfile                # Container definition
└── docker-compose.yml        # Container orchestration
```

## Installation

### Prerequisites

- Python 3.12.7
- uv (Python package manager)

### Local Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd cursor-demo
   ```

2. Install dependencies with uv:
   ```bash
   uv venv .venv
   source .venv/bin/activate
   uv sync
   ```

3. Run the application:
   ```bash
   uvicorn project.src.main:app --reload
   ```

4. The API will be available at http://localhost:8000

### Docker Setup

1. Build and start the Docker container:
   ```bash
   docker compose up --build
   ```

2. The API will be available at http://localhost:8000

## API Endpoints

- `GET /api/users/` - List all users
- `POST /api/users/` - Create a new user
- `GET /api/users/{user_id}` - Retrieve a specific user
- `PATCH /api/users/{user_id}` - Update a user
- `DELETE /api/users/{user_id}` - Delete a user
- `GET /health` - Health check endpoint

## Development

### Testing

Run the tests:
```bash
pytest
```

### Linting

Run linting with ruff:
```bash
ruff check .
```

Format code with ruff:
```bash
ruff format .
```

## Documentation

See the [architecture documentation](docs/architecture/README.md) for more details on the project structure and design.

## License

This project is licensed under the MIT License.