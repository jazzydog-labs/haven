# Contributing to Haven

Thank you for your interest in contributing to Haven! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Respect differing viewpoints and experiences

## How to Contribute

### Reporting Issues

1. Check if the issue already exists
2. Provide a clear description
3. Include steps to reproduce
4. Add relevant logs or screenshots
5. Mention your environment (OS, Python version, etc.)

### Suggesting Features

1. Check the [roadmap](roadmap.md) for planned features
2. Open a discussion first for major features
3. Clearly describe the use case
4. Provide examples if possible

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.12+
- Docker and Docker Compose
- Just command runner
- Git

### Setting Up

```bash
# Clone your fork
git clone https://github.com/your-username/haven.git
cd haven

# Add upstream remote
git remote add upstream https://github.com/jazzydog-labs/haven.git

# Install dependencies
just bootstrap

# Start services
just database::up

# Run tests
just test
```

## Development Workflow

### 1. Create a Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow our coding standards:

- Write clean, readable code
- Add type hints
- Include docstrings
- Follow existing patterns

### 3. Test Your Changes

```bash
# Run all quality checks
just check

# Run specific tests
just test tests/path/to/test.py

# Check coverage
just testing::coverage
```

### 4. Commit Your Changes

We follow conventional commits:

```bash
# Format: <type>(<scope>): <subject>

feat(api): add pagination to records endpoint
fix(auth): correct token validation
docs(readme): update installation instructions
test(api): add tests for new endpoint
refactor(domain): simplify record entity
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `chore`: Maintenance tasks

### 5. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name
```

Then create a pull request with:
- Clear title and description
- Link to related issues
- Screenshots for UI changes
- Test results

## Code Standards

### Python Style

We use Ruff for linting and formatting:

```bash
# Format code
just format

# Check style
just lint
```

Key guidelines:
- 100 character line length
- Double quotes for strings
- Type hints for all functions
- Meaningful variable names

### Type Checking

We use Pyright in strict mode:

```bash
just type
```

### Testing

- Write tests for all new code
- Maintain 70%+ coverage
- Use descriptive test names
- Include unit and integration tests

Example test:

```python
@pytest.mark.unit
class TestRecord:
    def test_create_record_with_data(self) -> None:
        """Test creating a record with specific data."""
        data = {"key": "value"}
        record = Record(data=data)
        
        assert record.data == data
        assert isinstance(record.id, UUID)
```

### Documentation

- Update docs for new features
- Include docstrings in code
- Add examples where helpful
- Keep README current

## Review Process

### What We Look For

1. **Code Quality**
   - Clean, readable code
   - Proper error handling
   - Performance considerations

2. **Tests**
   - Adequate test coverage
   - Edge cases covered
   - Tests pass in CI

3. **Documentation**
   - Code is documented
   - Docs are updated
   - Changelog entry added

4. **Architecture**
   - Follows project patterns
   - Maintains clean architecture
   - No breaking changes

### Review Timeline

- Initial review within 2-3 days
- Follow-up reviews within 1-2 days
- Feel free to ping if waiting longer

## Release Process

1. Features merged to `main`
2. Version bumped following semver
3. Changelog updated
4. Tagged and released
5. Docker images published

## Getting Help

- Check existing documentation
- Search closed issues
- Ask in discussions
- Join our community chat

## Recognition

Contributors are recognized in:
- [CHANGELOG.md](changelog.md)
- GitHub contributors page
- Release notes

Thank you for contributing to Haven!