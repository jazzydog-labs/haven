# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure with Clean Architecture
- REST API with FastAPI and full CRUD operations
- GraphQL API with Strawberry and Relay-style pagination
- PostgreSQL database with async SQLAlchemy 2.0
- Comprehensive test suite with 70%+ coverage requirement
- Docker support with multi-stage builds
- CI/CD pipeline with GitHub Actions
- MkDocs documentation site
- Hydra configuration management
- Alembic database migrations
- Repository pattern with Unit of Work
- Structured logging with JSON output
- Health check endpoints
- CORS middleware support
- Pre-commit hooks for code quality

### Security
- Non-root Docker container
- Secure defaults for production

## [0.1.0] - TBD

Initial release of Haven microservice.

### Features
- RESTful API with OpenAPI documentation
- GraphQL API with schema introspection
- PostgreSQL database with connection pooling
- Clean Architecture design
- Comprehensive testing infrastructure
- Production-ready Docker images
- Complete documentation

[Unreleased]: https://github.com/jazzydog-labs/haven/compare/main...HEAD