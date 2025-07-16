# Haven

[![CI](https://github.com/jazzydog-labs/haven/actions/workflows/ci.yml/badge.svg)](https://github.com/jazzydog-labs/haven/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A self-contained microservice exposing REST and GraphQL APIs over PostgreSQL, built with modern Python and Clean Architecture principles.

## Features

- 🚀 **Dual APIs**: REST (FastAPI) and GraphQL (Strawberry) interfaces
- 🏗️ **Clean Architecture**: Clear separation of concerns with domain-driven design
- 🔄 **Async Throughout**: Built on async/await for high performance
- 📊 **Type Safe**: Full type hints with strict Pyright checking
- 🧪 **Well Tested**: Comprehensive test suite with 70%+ coverage
- 🐳 **Production Ready**: Optimized Docker images with security best practices
- 📚 **Fully Documented**: API docs, architecture guides, and development workflows

## Quick Start

```bash
# Clone the repository
git clone https://github.com/jazzydog-labs/haven.git
cd haven

# Install dependencies
just bootstrap

# Start PostgreSQL
just db-up

# Run database migrations
just db-migrate

# Start the application
just run
```

The application will be available at:
- REST API: http://localhost:8080/docs
- GraphQL: http://localhost:8080/graphql
- Health: http://localhost:8080/health

## Project Structure

```
haven/
├── src/haven/          # Application source code
│   ├── domain/         # Business logic and entities
│   ├── application/    # Use cases and services
│   ├── infrastructure/ # Database and external services
│   └── interface/      # API routes and GraphQL schema
├── tests/              # Test suite (unit, integration, e2e)
├── docs/               # MkDocs documentation
├── conf/               # Hydra configuration files
├── alembic/            # Database migrations
└── scripts/            # Development and deployment scripts
```

## Development

### Prerequisites

- Python 3.12 or higher
- Docker and Docker Compose
- [Just](https://github.com/casey/just) command runner

### Key Commands

```bash
just --list      # Show all available commands
just check       # Run all quality checks (lint, type, test)
just test        # Run test suite with coverage
just docs-serve  # Preview documentation locally
just docker-build # Build Docker image
```

### Testing

```bash
# Run all tests
just test

# Run specific test file
just test-file tests/unit/domain/test_record.py

# Run with coverage report
just test-cov
```

### Code Quality

```bash
# Format code
just format

# Run linting
just lint

# Type checking
just type
```

## API Examples

### REST API

```bash
# Create a record
curl -X POST http://localhost:8080/api/v1/records \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "Example", "value": 42}}'

# Get all records
curl http://localhost:8080/api/v1/records
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

query GetRecords {
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

## Documentation

Full documentation is available at [https://jazzydog-labs.github.io/haven](https://jazzydog-labs.github.io/haven)

Key documentation:
- [Architecture Overview](docs/architecture.md)
- [Local Setup Guide](docs/local-setup.md)
- [API Reference](docs/api/)
- [Testing Guide](docs/testing.md)
- [Deployment Guide](docs/deployment.md)

## Contributing

We welcome contributions! Please see our [Contributing Guide](docs/contributing.md) for details.

## Security

For security issues, please email security@jazzydog-labs.com instead of using the issue tracker. See our [Security Policy](SECURITY.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Strawberry GraphQL](https://strawberry.rocks/) - Python GraphQL library
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [Hydra](https://hydra.cc/) - Configuration management

---

Made with ❤️ by the Haven team