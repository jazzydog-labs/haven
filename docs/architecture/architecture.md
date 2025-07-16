# Haven - Architecture Guide

*Last updated: 2025-07-16*

This document describes Haven's architecture following Clean Architecture principles, with clear separation of concerns across layers.

---

## 1. Architecture Overview

Haven follows a layered architecture pattern with strict dependency rules:

```
┌─────────────────────────────────────────────┐
│           Interface Layer                    │
│  (FastAPI routes, GraphQL schema, CLI)      │
├─────────────────────────────────────────────┤
│         Application Layer                    │
│    (Use cases, Application services)        │
├─────────────────────────────────────────────┤
│          Domain Layer                        │
│   (Entities, Value objects, Domain logic)   │
├─────────────────────────────────────────────┤
│       Infrastructure Layer                   │
│ (Database, External services, File system)  │
└─────────────────────────────────────────────┘
```

### Dependency Rule
- Dependencies only point inward
- Inner layers know nothing about outer layers
- Domain layer has zero external dependencies

---

## 2. Layer Responsibilities

### 2.1 Domain Layer (`src/domain/`)
- **Purpose**: Core business logic and rules
- **Components**: 
  - Entities (e.g., `Record`)
  - Value Objects
  - Domain Events
  - Repository Interfaces (abstract)
- **Example**:
  ```python
  # src/domain/entities/record.py
  @dataclass
  class Record:
      id: UUID
      data: dict[str, Any]
      created_at: datetime
      updated_at: datetime
  ```

### 2.2 Application Layer (`src/application/`)
- **Purpose**: Orchestrates domain objects to fulfill use cases
- **Components**:
  - Use Cases (e.g., `CreateRecordUseCase`)
  - Application Services
  - DTOs (Data Transfer Objects)
- **Example**:
  ```python
  # src/application/use_cases/create_record.py
  class CreateRecordUseCase:
      async def execute(self, data: dict) -> Record:
          # Business logic orchestration
  ```

### 2.3 Infrastructure Layer (`src/infrastructure/`)
- **Purpose**: External concerns and implementations
- **Components**:
  - Database implementations
  - Repository implementations
  - External service adapters
  - Configuration loaders
- **Example**:
  ```python
  # src/infrastructure/database/repositories/record_repository.py
  class SQLAlchemyRecordRepository(RecordRepository):
      # Concrete implementation using SQLAlchemy
  ```

### 2.4 Interface Layer (`src/interface/`)
- **Purpose**: Entry points for external actors
- **Components**:
  - REST API routes
  - GraphQL resolvers
  - CLI commands
  - WebSocket handlers
- **Example**:
  ```python
  # src/interface/api/routes/records.py
  @router.post("/records")
  async def create_record(data: RecordCreate) -> RecordResponse:
      # Calls application layer use case
  ```

---

## 3. Data Flow Example

Creating a new record:

1. **Interface**: HTTP POST to `/records` endpoint
2. **Interface**: FastAPI route validates input using Pydantic
3. **Application**: `CreateRecordUseCase` receives DTO
4. **Domain**: Creates `Record` entity with business rules
5. **Application**: Calls repository interface to persist
6. **Infrastructure**: SQLAlchemy repository saves to PostgreSQL
7. **Interface**: Returns response DTO to client

---

## 4. Key Patterns

### 4.1 Repository Pattern
- Abstract interfaces in domain layer
- Concrete implementations in infrastructure
- Enables database technology swapping

### 4.2 Unit of Work
- Manages database transactions
- Ensures consistency across aggregates
- Implemented in infrastructure layer

### 4.3 Dependency Injection
- FastAPI's `Depends()` for automatic injection
- Configuration via Hydra
- Repository instances injected into use cases

### 4.4 CQRS (Light)
- Separate read/write models where beneficial
- Optimized queries for GraphQL resolvers
- Command handlers for mutations

---

## 5. Testing Strategy by Layer

- **Domain**: Pure unit tests, no dependencies
- **Application**: Unit tests with mocked repositories
- **Infrastructure**: Integration tests with real database
- **Interface**: E2E tests with test client

---

## 6. Common Pitfalls to Avoid

1. **Leaking infrastructure into domain** - No SQLAlchemy imports in domain layer
2. **Anemic domain models** - Keep business logic in entities, not services
3. **Bypassing layers** - Always go through proper channels
4. **Tight coupling** - Use interfaces and dependency injection

---

## 7. Evolution Guidelines

When adding new features:

1. Start with domain entities and logic
2. Define repository interfaces if needed
3. Create use cases in application layer
4. Implement infrastructure components
5. Wire up interface endpoints
6. Test each layer independently

---

For implementation examples, see the existing code in `src/` following these patterns.