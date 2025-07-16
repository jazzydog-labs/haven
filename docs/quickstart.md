# Quick Start Guide

Get Haven up and running in under 5 minutes!

## Prerequisites

- Python 3.12 or higher
- Docker and Docker Compose
- [Just](https://github.com/casey/just) command runner (optional but recommended)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jazzydog-labs/haven.git
cd haven
```

### 2. Set Up Environment

=== "With Just"

    ```bash
    # Install dependencies and create virtual environment
    just bootstrap
    
    # Start PostgreSQL
    just database::up
    
    # Run database migrations
    just database::migrate
    
    # Start the application
    just run
    ```

=== "Without Just"

    ```bash
    # Create virtual environment
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    
    # Install dependencies
    pip install -e ".[dev]"
    
    # Start PostgreSQL
    docker-compose up -d postgres
    
    # Run database migrations
    alembic upgrade head
    
    # Start the application
    python -m haven.main
    ```

### 3. Verify Installation

The application should now be running at `http://api.haven.local`

Check the health endpoint:
```bash
curl http://api.haven.local/health
```

## Explore the APIs

### REST API (Swagger UI)

Open [http://api.haven.local/docs](http://api.haven.local/docs) in your browser to explore the REST API using Swagger UI.

### GraphQL (GraphiQL)

Open [http://api.haven.local/graphql](http://api.haven.local/graphql) to interact with the GraphQL API using GraphiQL.

## Create Your First Record

### Using REST API

```bash
# Create a record
curl -X POST http://api.haven.local/api/v1/records \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "My First Record", "value": 42}}'

# Response:
# {
#   "id": "550e8400-e29b-41d4-a716-446655440000",
#   "data": {"name": "My First Record", "value": 42},
#   "created_at": "2025-01-15T12:00:00Z",
#   "updated_at": "2025-01-15T12:00:00Z"
# }
```

### Using GraphQL

```graphql
mutation CreateRecord {
  createRecord(input: {
    data: {
      name: "My First Record"
      value: 42
    }
  }) {
    id
    data
    createdAt
    updatedAt
  }
}
```

## Common Operations

### List All Records

**REST:**
```bash
curl http://api.haven.local/api/v1/records
```

**GraphQL:**
```graphql
query ListRecords {
  records(first: 10) {
    edges {
      node {
        id
        data
      }
    }
  }
}
```

### Update a Record

**REST:**
```bash
curl -X PUT http://api.haven.local/api/v1/records/{id} \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "Updated Record", "value": 100}}'
```

**GraphQL:**
```graphql
mutation UpdateRecord {
  updateRecord(
    id: "550e8400-e29b-41d4-a716-446655440000"
    input: { data: { name: "Updated Record", value: 100 } }
  ) {
    id
    data
  }
}
```

## Development Commands

```bash
# Run tests
just test

# Run linting and type checks
just check

# Format code
just format

# View all available commands
just --list
```

## Next Steps

- Read the [Architecture Overview](architecture.md) to understand the design
- Explore the full [API Reference](api/index.md)
- Set up your [Development Environment](local-setup.md)
- Learn about [Testing](testing.md) and [Code Quality](quality.md)

## Troubleshooting

### Database Connection Error

If you see database connection errors:

1. Ensure PostgreSQL is running: `docker ps`
2. Check the connection string in `.env` file
3. Verify PostgreSQL logs: `just logs`

### Port Already in Use

If port 8080 is already in use:

1. Change the port in `.env`: `APP_PORT=8081`
2. Or stop the conflicting service

### Import Errors

If you see import errors:

1. Ensure you're in the virtual environment
2. Reinstall dependencies: `pip install -e ".[dev]"`

For more help, see the [full documentation](index.md) or [open an issue](https://github.com/jazzydog-labs/haven/issues).