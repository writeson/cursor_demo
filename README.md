# Cursor Demo API

A RESTful API built with FastAPI, SQLModel, and async SQLite.

## Features

- **Async API**: Built with FastAPI and async SQLModel
- **Database**: SQLite with async access via aiosqlite
- **CRUD Operations**: Complete set of operations for user management
- **API Documentation**: Auto-generated with Swagger UI
- **Type Annotations**: Full type hinting for better developer experience
- **Containerization**: Docker and docker-compose setup

## Requirements

- Python 3.12.7 or higher
- [Astral UV](https://docs.astral.sh/uv/) for dependency management

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/cursor-demo.git
cd cursor-demo
```

2. Set up the Python environment:

```bash
uv sync
```

3. Run the API:

```bash
python project/main.py
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Health Check

- `GET /health`: Check the health status of the API

### User Endpoints

- `GET /api/users`: Get all users
- `GET /api/users/{user_id}`: Get a specific user
- `POST /api/users`: Create a new user
- `PATCH /api/users/{user_id}`: Update a user
- `DELETE /api/users/{user_id}`: Delete a user

## Docker

You can also run the application using Docker:

```bash
docker compose up -d
```

This will build and start the application in a container.

## Development

### Running Tests

Run the tests with pytest:

```bash
python -m pytest
```

### API Documentation

When the API is running, you can view the API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

See [Architecture Documentation](docs/architecture/README.md) for details on the project's architecture and design.

## License

This project is licensed under the MIT License.