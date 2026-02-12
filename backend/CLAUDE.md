# Backend Development Guidelines

## Project Overview
This is a FastAPI-based backend for a multi-user Todo application using SQLModel ORM and Neon PostgreSQL. The API provides full CRUD operations for tasks with proper user isolation and authentication middleware.

## Tech Stack
- **Framework**: FastAPI (latest stable)
- **ORM**: SQLModel
- **Database**: PostgreSQL (Neon)
- **Validation**: Pydantic
- **Authentication**: JWT tokens

## Architecture
- **Models**: SQLModel classes in `src/models/`
- **Schemas**: Pydantic classes for validation in `src/schemas/`
- **Routes**: API endpoints in `src/routes/`
- **Services**: Business logic in `src/services/`
- **Middleware**: Custom middleware in `src/middleware/`
- **Utils**: Helper functions in `src/utils/`

## Key Patterns
1. **Dependency Injection**: Use FastAPI's dependency system
2. **Separation of Concerns**: Keep business logic in services, not route handlers
3. **Async Operations**: Use async/await for I/O operations
4. **Error Handling**: Use consistent error response format
5. **Authentication**: All endpoints require JWT validation

## File Structure
```
backend/
├── pyproject.toml          # Dependencies and configuration
├── src/
│   ├── main.py             # FastAPI app entry point
│   ├── database.py         # Database connection and session management
│   ├── models/             # SQLModel database models
│   ├── schemas/            # Pydantic schemas for validation
│   ├── routes/             # API route handlers
│   ├── services/           # Business logic layer
│   ├── middleware/         # Custom middleware
│   └── utils/              # Utility functions
├── tests/                  # Test files
├── alembic/                # Database migrations
├── docker/                 # Docker configuration
├── .env.example           # Environment variables template
└── .gitignore
```

## Important Implementation Notes
- All database operations should be async
- Use UUID primary keys for User and Task models
- Implement proper user isolation (users can only access their own tasks)
- Follow REST conventions for endpoint design
- Use consistent error response format: `{success: boolean, data: any, error: object}`
- Implement proper validation with Pydantic schemas
- Character limits: Title (255 chars), Description (5000 chars)

## Security Considerations
- Validate JWT tokens on every request
- Verify user_id in URL path matches JWT claims
- Return 401 for missing/invalid tokens
- Return 403 for authorization failures
- Sanitize all user inputs to prevent injection attacks
- Use bcrypt for password hashing