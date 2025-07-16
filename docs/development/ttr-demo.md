# TTR System Demo Guide

This guide shows how to test and demo the TTR (Task, Todo, Review) system features that have been implemented.

## Quick Start

```bash
# 1. Start the database
just db-up

# 2. Run migrations to create TTR tables
just db-migrate

# 3. Run the TTR demo (two options)

# Option A: Using main Justfile
just demo-ttr

# Option B: Using demo Justfile directly
just -f justfile.demos.standalone demo-ttr

# 4. Optional: Start API server for interactive testing
just run
```

## Implemented Features

### ✅ User Management
- Create, read, update, delete users
- Username and email validation
- Unique constraints on username and email
- Full test coverage with integration tests

### ✅ Repository Management  
- Create, read, update, delete repositories
- Support for local and remote repositories
- Branch tracking and validation
- GitHub repository detection
- Full test coverage with integration tests

### 🚧 In Progress
- Commit tracking (implementation started)
- Comment system (planned)
- Review workflow (planned)
- Frontend interface (planned)

## Running Demo Commands Independently

You can run demo commands directly from the standalone demo justfile:

```bash
# View all available demo commands
just -f justfile.demos.standalone demo

# Run specific demos
just -f justfile.demos.standalone demo-ttr           # TTR system demo
just -f justfile.demos.standalone demo-health        # Health check endpoints
just -f justfile.demos.standalone demo-api           # REST API operations
just -f justfile.demos.standalone demo-graphql       # GraphQL operations
just -f justfile.demos.standalone demo-all           # All demos in sequence
```

This is useful when you want to:
- Run demos without importing the full justfile
- Test specific features quickly
- Integrate demos into CI/CD pipelines
- Debug demo-specific issues

## Testing the Implementation

### Unit Tests
```bash
# Test all TTR domain entities
just test tests/unit/domain/test_user.py tests/unit/domain/test_repository.py

# Test all TTR services  
just test tests/unit/application/test_user_service.py tests/unit/application/test_repository_service.py

# Test all TTR repositories
just test tests/unit/infrastructure/test_user_repository.py tests/unit/infrastructure/test_repository_repository.py
```

### Integration Tests
```bash
# Test with real database
just test tests/unit/infrastructure/test_user_repository.py -v
just test tests/unit/infrastructure/test_repository_repository.py -v
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Repositories Table
```sql
CREATE TABLE repositories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    url TEXT NOT NULL,
    branch VARCHAR(255) NOT NULL DEFAULT 'main',
    description TEXT,
    is_local BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Manual Testing Examples

### User Operations
```python
# Create a user
from haven.domain.entities.user import User
from haven.application.services.user_service import UserService

user = User(
    username="plva",
    email="paul@example.com", 
    display_name="Paul"
)

# The service will handle validation and persistence
```

### Repository Operations
```python
# Create a repository
from haven.domain.entities.repository import Repository
from haven.application.services.repository_service import RepositoryService

# Local repository
local_repo = Repository(
    name="haven",
    full_name="jazzydog-labs/haven",
    url="/Users/paul/dev/jazzydog-labs/haven",
    branch="main",
    description="Haven repository",
    is_local=True
)

# Remote repository
remote_repo = Repository(
    name="test-repo",
    full_name="user/test-repo", 
    url="https://github.com/user/test-repo.git",
    branch="main",
    is_local=False
)
```

## Database Console Access

```bash
# Connect to database to inspect data
just db-console

# Example queries
\dt  -- List all tables
SELECT * FROM users;
SELECT * FROM repositories;
SELECT * FROM alembic_version;
```

## Architecture Overview

The TTR system follows Clean Architecture:

```
Domain Layer (Entities)
├── User entity with validation
├── Repository entity with validation
└── Future: Commit, Comment entities

Application Layer (Services)
├── UserService (business logic)
├── RepositoryService (business logic)
└── Future: CommitService, CommentService

Infrastructure Layer (Database)
├── UserRepositoryImpl (data access)
├── RepositoryRepositoryImpl (data access)
└── SQLAlchemy models and migrations

Interface Layer (APIs)
└── Future: REST and GraphQL endpoints
```

## Test Coverage

Current test coverage for TTR features:
- User domain entity: 100% (all validations)
- User repository: 94% (all CRUD operations)
- User service: 88% (all business logic)
- Repository domain entity: 100% (all validations)
- Repository repository: 96% (all CRUD operations)
- Repository service: 88% (all business logic)

## Development Workflow

1. **Add Feature**: Implement domain entity first
2. **Add Repository**: Create repository interface and implementation
3. **Add Service**: Create service with business logic
4. **Add Tests**: Unit and integration tests
5. **Add Migration**: Database schema changes
6. **Add Demo**: Update this document with examples

## Next Steps

1. Implement Commit domain entity
2. Add Comment system
3. Create REST API endpoints
4. Add GraphQL schema
5. Build React frontend
6. Add real-time features

## Troubleshooting

### Database Issues
```bash
# Reset database if needed
just db-reset

# Check migration status
just db-current

# View migration history
just db-history
```

### Test Issues
```bash
# Run specific test file
just test tests/unit/domain/test_user.py -v

# Run with coverage
just test-cov

# Debug test failures
just test tests/unit/infrastructure/test_user_repository.py -v -s
```

### Environment Issues
```bash
# Check Python environment
just info

# Restart services
just down && just db-up && just run
```