# Demo Commands Guide

This guide documents all available demo commands in the Haven project. These commands showcase implemented features and help verify functionality.

## Overview

Demo commands follow the pattern `just demo-<feature>` and are designed to:
- Quickly verify feature functionality
- Provide examples of API usage
- Help onboard new developers
- Support testing and debugging

## Available Demo Commands

### `just demo`
Shows a list of all available demo commands with descriptions.

### `just demos::health`
Tests both REST and GraphQL health endpoints.
- Verifies API is running
- Shows health status response format
- Tests both REST and GraphQL endpoints

### `just demos::api`
Demonstrates REST API CRUD operations.
- Creates a new record
- Lists all records
- Shows proper JSON formatting
- Includes link to Swagger documentation

### `just demos::graphql`
Shows GraphQL query and mutation examples.
- Queries all records
- Creates a record via mutation
- Demonstrates GraphQL request format
- Includes link to GraphQL playground

### `just demos::docker`
Verifies Docker containerization setup.
- Shows container status
- Tests containerized API health
- Verifies database connectivity
- Useful for debugging container issues

### `just demos::migrations`
Demonstrates all migration strategies.
- Shows current migration status
- Lists all available migration methods
- Helps choose appropriate migration approach

### `just demo-commits`
Launches a web server to view all repository commits with diffs.
- Single command to see entire repository history
- HTML-formatted diff output
- Useful for code reviews

### `just demo-diff-generation`
Shows the diff generation API in action.
- Generates diffs between commits
- Demonstrates background task processing
- Shows HTML diff output generation

### `just demos::all`
Runs all demos in sequence.
- Comprehensive feature verification
- Good for testing after major changes
- Shows all features working together

## Docker-Specific Demos

These commands run demos inside Docker containers:

- `just demo-commits-docker`
- `just demo-diff-generation-docker`

Use these when testing containerized deployments.

## Usage Examples

### Quick Feature Verification
```bash
# Start the API
just run

# Test it's working
just demos::health

# Try CRUD operations
just demos::api
```

### Full System Test
```bash
# Start everything in Docker
just docker::up

# Run all demos
just demos::all
```

### Debugging Issues
```bash
# Check Docker setup
just demos::docker

# Test specific features
just demos::graphql
just demos::migrations
```

## Adding New Demo Commands

To add a new demo command:

1. Edit `justfile.demos`
2. Follow the naming pattern: `demo-<feature>`
3. Include clear output and error handling
4. Update this documentation
5. Reference in relevant work log entries

Example template:
```just
# Demo: Your feature description
demo-your-feature:
    @echo "🎯 Testing your feature..."
    # Your demo commands here
    @echo "✅ Demo complete!"
```

## Best Practices

1. **Keep demos simple** - Focus on one feature at a time
2. **Include error handling** - Show helpful messages when services aren't running
3. **Provide clear output** - Use emojis and formatting for readability
4. **Make them idempotent** - Demos should work repeatedly without cleanup
5. **Document dependencies** - Note if a demo requires services to be running

## Troubleshooting

If a demo fails:

1. Ensure services are running: `just run` or `just docker::up`
2. Check database is up: `just database::up`
3. Verify migrations: `just database::migrate`
4. See logs: `just logs`

For more help, see the [Container Troubleshooting Guide](../operations/container-troubleshooting.md).