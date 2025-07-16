# OpenAPI Specification

Haven automatically generates an OpenAPI 3.0 specification from the FastAPI routes.

## Accessing the OpenAPI Schema

### Interactive Documentation (Swagger UI)
Visit [http://localhost:8080/docs](http://localhost:8080/docs)

### Alternative Documentation (ReDoc)
Visit [http://localhost:8080/redoc](http://localhost:8080/redoc)

### Raw OpenAPI JSON
```bash
curl http://localhost:8080/openapi.json
```

## Schema Overview

The OpenAPI schema includes:

- All REST endpoints with parameters
- Request/response models with examples
- Authentication requirements (when enabled)
- Error response formats
- API metadata and descriptions

## Integration

### Generate Client Code

You can use the OpenAPI schema to generate client libraries:

```bash
# Install OpenAPI Generator
npm install -g @openapitools/openapi-generator-cli

# Generate Python client
openapi-generator-cli generate \
  -i http://localhost:8080/openapi.json \
  -g python \
  -o ./haven-client-python

# Generate TypeScript client  
openapi-generator-cli generate \
  -i http://localhost:8080/openapi.json \
  -g typescript-axios \
  -o ./haven-client-typescript
```

### Import to Postman

1. Open Postman
2. Click "Import" 
3. Enter URL: `http://localhost:8080/openapi.json`
4. Postman will create a collection with all endpoints

### Use with Insomnia

1. In Insomnia, create new Request Collection
2. Click "Import/Export" 
3. Import from URL: `http://localhost:8080/openapi.json`

## Schema Customization

The OpenAPI schema can be customized in `src/haven/interface/api/app.py`:

```python
app = FastAPI(
    title="Haven API",
    description="Your custom description",
    version="1.0.0",
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "API Support",
        "email": "api@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)
```

## Example Schema Section

```json
{
  "openapi": "3.0.2",
  "info": {
    "title": "Haven API",
    "description": "Self-contained microservice with REST and GraphQL APIs",
    "version": "0.1.0"
  },
  "paths": {
    "/api/v1/records": {
      "get": {
        "summary": "List Records",
        "operationId": "list_records",
        "parameters": [
          {
            "name": "limit",
            "in": "query",
            "required": false,
            "schema": {
              "type": "integer",
              "default": 20,
              "minimum": 1,
              "maximum": 100
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/RecordListResponseDTO"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## Downloading the Schema

To save the schema locally:

```bash
# Save as JSON
curl http://localhost:8080/openapi.json > openapi.json

# Convert to YAML (requires yq)
curl http://localhost:8080/openapi.json | yq -P > openapi.yaml
```

## Validation

Validate your API implementation against the schema:

```bash
# Install spectral
npm install -g @stoplight/spectral-cli

# Validate
spectral lint openapi.json
```

## See Also

- [REST API Reference](rest.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAPI Specification](https://swagger.io/specification/)