# Cursor Demo API Architecture

This document describes the architecture of the Cursor Demo API.

## Application Structure

The application follows a layered architecture with the following components:

- **API Layer**: FastAPI application with REST endpoints
- **Service Layer**: Business logic and data access
- **Data Layer**: SQLModel models and database access

### Directory Structure

```
project/
├── db/                 # Database files
├── src/                # Source code
│   ├── endpoints/      # API endpoints
│   ├── models.py       # Data models
│   ├── database.py     # Database access
│   └── main.py         # FastAPI application
├── main.py             # Entry point
└── ...
```

## Component Diagram

```mermaid
graph TD
    A[Client] -->|HTTP Request| B[FastAPI App]
    B -->|Route| C[Endpoints]
    C -->|CRUD Operations| D[Database Module]
    D -->|SQL Queries| E[SQLite Database]

    subgraph API Layer
        B
        C
    end

    subgraph Service Layer
        D
    end

    subgraph Data Layer
        E
    end
```

## Database Schema

```mermaid
erDiagram
    USERS {
        int id PK
        string first_name
        string last_name
        int age
    }
```

## API Endpoints

### User Endpoints

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Database

    Client->>API: GET /api/users
    API->>Database: Query all users
    Database-->>API: Return users list
    API-->>Client: JSON users array

    Client->>API: GET /api/users/{id}
    API->>Database: Query user by ID
    Database-->>API: Return user or None
    alt User Found
        API-->>Client: JSON user object
    else User Not Found
        API-->>Client: 404 Not Found
    end

    Client->>API: POST /api/users
    Note right of Client: {first_name, last_name, age}
    API->>Database: Create new user
    Database-->>API: Return created user
    API-->>Client: JSON user object

    Client->>API: PATCH /api/users/{id}
    Note right of Client: {updated fields}
    API->>Database: Update user
    Database-->>API: Return updated user or None
    alt User Found
        API-->>Client: JSON updated user object
    else User Not Found
        API-->>Client: 404 Not Found
    end

    Client->>API: DELETE /api/users/{id}
    API->>Database: Delete user
    Database-->>API: Return success/failure
    alt User Found
        API-->>Client: 200 Success message
    else User Not Found
        API-->>Client: 404 Not Found
    end
```

## Async Implementation

The application uses async/await pattern throughout the codebase:

- Async SQLModel for database operations using aiosqlite
- FastAPI async endpoints for non-blocking request handling
- Dependency injection for database session management

```mermaid
sequenceDiagram
    participant A as API Endpoint
    participant D as Database Module
    participant S as SQLite (aiosqlite)

    A->>D: async request
    D->>S: async query
    Note right of S: Non-blocking I/O
    S-->>D: async result
    D-->>A: return data

    Note over A,S: All operations are non-blocking
```

The async implementation allows for efficient handling of concurrent requests, making the application more scalable.

## Testing Strategy

Tests are implemented using pytest and pytest-asyncio:

- Unit tests for database CRUD operations
- Async fixtures for database session management
- In-memory SQLite database for testing