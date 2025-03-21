# Cursor Demo Application Architecture

This document describes the architecture of the Cursor Demo application, a FastAPI-based API with async SQLite database access.

## Overview

The application follows a layered architecture with the following components:
- **API Layer**: FastAPI application with endpoints for CRUD operations
- **Service Layer**: Business logic (when needed)
- **Data Access Layer**: Database operations using SQLModel and aiosqlite

## Component Diagram

```mermaid
flowchart LR
    A[FastAPI Application] <--> B[SQLModel Models/CRUD]
    B <--> C[SQLite DB\n(aiosqlite)]
```

## Project Structure

```mermaid
graph TD
    project[/project]
    db[/db]
    src[/src]
    endpoints[/endpoints]
    init[__init__.py]
    users[users.py]
    main[main.py]
    database[database.py]

    project --> db
    project --> src
    project --> database
    src --> endpoints
    src --> main
    endpoints --> init
    endpoints --> users
    db --> cursor_demo[cursor_demo.db]
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

## API Endpoints Sequence Diagram

```mermaid
sequenceDiagram
    participant Client
    participant FastAPI
    participant CRUDOperations
    participant Database

    %% Create User
    Client->>FastAPI: POST /api/users/
    FastAPI->>CRUDOperations: create(user_data)
    CRUDOperations->>Database: Insert user
    Database-->>CRUDOperations: Return created user
    CRUDOperations-->>FastAPI: Return user object
    FastAPI-->>Client: 201 Created (user data)

    %% Get User
    Client->>FastAPI: GET /api/users/{id}
    FastAPI->>CRUDOperations: get(id)
    CRUDOperations->>Database: Select user by id
    Database-->>CRUDOperations: Return user data
    CRUDOperations-->>FastAPI: Return user object
    FastAPI-->>Client: 200 OK (user data)

    %% Update User
    Client->>FastAPI: PATCH /api/users/{id}
    FastAPI->>CRUDOperations: update(id, user_data)
    CRUDOperations->>Database: Update user
    Database-->>CRUDOperations: Return updated user
    CRUDOperations-->>FastAPI: Return updated user object
    FastAPI-->>Client: 200 OK (updated user data)

    %% Delete User
    Client->>FastAPI: DELETE /api/users/{id}
    FastAPI->>CRUDOperations: delete(id)
    CRUDOperations->>Database: Delete user
    Database-->>CRUDOperations: Confirm deletion
    CRUDOperations-->>FastAPI: Return success
    FastAPI-->>Client: 204 No Content
```

## Async Implementation

The application uses async/await throughout the stack:
- FastAPI endpoints are defined as async functions
- SQLModel operations use the async SQLAlchemy engine
- The database connection uses aiosqlite for async operations

This allows for efficient handling of concurrent requests and improved performance.