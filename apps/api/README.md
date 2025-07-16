# Haven API

A self-contained microservice exposing REST and GraphQL APIs over PostgreSQL, built with modern Python and Clean Architecture principles.

## Features

- 🚀 **Dual APIs**: REST (FastAPI) and GraphQL (Strawberry) interfaces
- 🏗️ **Clean Architecture**: Clear separation of concerns with domain-driven design
- 🔄 **Async Throughout**: Built on async/await for high performance
- 📊 **Type Safe**: Full type hints with strict Pyright checking
- 🧪 **Well Tested**: Comprehensive test suite with 70%+ coverage
- 🐳 **Production Ready**: Optimized Docker images with security best practices

## Quick Start

```bash
# From the repository root:
just bootstrap-python
just database::up
just database::migrate
just run
```

The application will be available at:
- REST API: http://api.haven.local/docs
- GraphQL: http://api.haven.local/graphql
- Health: http://api.haven.local/health

## Project Structure

```
apps/api/
├── src/haven/          # Application source code
│   ├── domain/         # Business logic and entities
│   ├── application/    # Use cases and services
│   ├── infrastructure/ # Database and external services
│   └── interface/      # API routes and GraphQL schema
├── tests/              # Test suite (unit, integration, e2e)
├── conf/               # Hydra configuration files
├── alembic/            # Database migrations
└── scripts/            # Development scripts
```

## Development

### Key Commands

```bash
just testing::python      # Run test suite
just lint-python      # Run linting
just type-python      # Type checking
just format-python    # Format code
```

## API Examples

### REST API

```bash
# Create a record
curl -X POST http://api.haven.local/api/v1/records \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "Example", "value": 42}}'

# Get all records
curl http://api.haven.local/api/v1/records
```

### GraphQL API

```graphql
mutation CreateRecord {
  createRecord(input: { data: { name: "Example", value: 42 } }) {
    id
    data
    createdAt
  }
}
```

## License

This project is licensed under the MIT License.