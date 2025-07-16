# API Overview

Haven provides two complementary API interfaces:

## REST API

A RESTful API built with FastAPI that provides:

- Standard HTTP methods (GET, POST, PUT, PATCH, DELETE)
- JSON request/response format
- OpenAPI 3.0 specification
- Automatic interactive documentation (Swagger UI)
- Predictable resource-based URLs

[View REST API Reference →](rest.md)

### Base URL
```
http://localhost:8080/api/v1
```

### Example
```bash
curl http://localhost:8080/api/v1/records
```

## GraphQL API

A flexible GraphQL API built with Strawberry that offers:

- Single endpoint for all queries
- Precise data fetching (request exactly what you need)
- Strong type system
- Real-time schema introspection
- Interactive GraphiQL explorer

[View GraphQL API Reference →](graphql.md)

### Endpoint
```
http://localhost:8080/graphql
```

### Example
```graphql
query {
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

## Choosing Between REST and GraphQL

### Use REST when you:
- Need simple CRUD operations
- Want predictable caching
- Prefer conventional HTTP semantics
- Are building traditional web applications

### Use GraphQL when you:
- Need flexible data queries
- Want to minimize over-fetching
- Have complex nested data requirements
- Are building modern single-page applications

## Common Features

Both APIs share:

- Same underlying data models
- Consistent authentication (when enabled)
- Unified error handling
- Comprehensive test coverage
- Performance monitoring

## Authentication

Currently, the APIs are open for local development. Production deployments will support:

- Bearer token authentication
- API key authentication
- OAuth2 flows (planned)

## Rate Limiting

Local development has no rate limits. Production will enforce:

- 1000 requests/hour per IP (REST)
- 100 queries/hour per IP (GraphQL)
- Higher limits with API keys

## Error Handling

Both APIs return consistent error responses:

```json
{
  "detail": "Record not found",
  "type": "not_found",
  "status": 404
}
```

## Versioning

- REST API uses URL versioning: `/api/v1/`, `/api/v2/`
- GraphQL API uses field deprecation for backwards compatibility

## Next Steps

- Explore the [REST API Reference](rest.md)
- Learn about the [GraphQL Schema](graphql.md)
- View the [OpenAPI Specification](openapi.md)
- Try the interactive demos at `/docs` and `/graphql`