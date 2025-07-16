# Haven

A self-contained microservice exposing REST and GraphQL APIs over PostgreSQL.

## Quick Start

```bash
# Install dependencies
just bootstrap

# Start PostgreSQL
just db-up

# Run the application
just run
```

## Project Structure

```
haven/
├── src/haven/          # Application source code
│   ├── domain/         # Business logic and entities
│   ├── application/    # Use cases and services
│   ├── infrastructure/ # Database and external services
│   └── interface/      # API routes and GraphQL schema
├── tests/              # Test suite
├── docs/               # Documentation
├── conf/               # Configuration files
└── alembic/            # Database migrations
```

## Development

See `CLAUDE.md` for fast development workflow and `docs/` for comprehensive documentation.

### Key Commands

```bash
just --list      # Show all available commands
just check       # Run quality checks (lint, type, test)
just test        # Run test suite
just docs-serve  # Preview documentation
```

## Documentation

- [Architecture](docs/architecture.md) - System design and patterns
- [Local Setup](docs/local-setup.md) - Development environment setup
- [API Reference](docs/api/) - REST and GraphQL endpoints
- [Testing](docs/testing.md) - Test strategy and examples

## License

MIT