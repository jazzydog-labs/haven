# Haven - REST API Reference

*Last updated: 2025-07-16*

Haven exposes a RESTful API built with FastAPI. The interactive documentation is available at **`/docs`** (Swagger UI) and **`/redoc`** (ReDoc).

---

## 1. Base URL

```
http://api.haven.local/api/v1
```

All endpoints are prefixed with `/api/v1` for versioning.

---

## 2. Authentication

Currently, the API is unauthenticated for local development. Production deployment will use:
- Bearer token authentication
- API key headers
- OAuth2 flows (future)

---

## 3. Common Headers

### Request Headers
```http
Content-Type: application/json
Accept: application/json
X-Request-ID: <uuid>  # Optional, for tracing
```

### Response Headers
```http
Content-Type: application/json
X-Request-ID: <uuid>  # Echoed from request
X-Response-Time: <ms>
```

---

## 4. Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid request data |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

---

## 5. Endpoints

### 5.1 Health Check

Check service status and dependencies.

```http
GET /health
```

#### Response
```json
{
  "status": "healthy",
  "timestamp": "2025-07-16T12:00:00Z",
  "version": "0.1.0",
  "dependencies": {
    "database": "healthy",
    "redis": "healthy"
  }
}
```

---

### 5.2 Records

#### List Records
```http
GET /api/v1/records?limit=20&offset=0
```

##### Query Parameters
- `limit` (int, optional): Number of records to return (default: 20, max: 100)
- `offset` (int, optional): Number of records to skip (default: 0)
- `sort` (string, optional): Sort field (default: "created_at")
- `order` (string, optional): Sort order "asc" or "desc" (default: "desc")

##### Response
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "data": {"key": "value"},
      "created_at": "2025-07-16T12:00:00Z",
      "updated_at": "2025-07-16T12:00:00Z"
    }
  ],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

#### Get Record
```http
GET /api/v1/records/{id}
```

##### Path Parameters
- `id` (uuid): Record identifier

##### Response
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": {"key": "value"},
  "created_at": "2025-07-16T12:00:00Z",
  "updated_at": "2025-07-16T12:00:00Z"
}
```

#### Create Record
```http
POST /api/v1/records
```

##### Request Body
```json
{
  "data": {
    "key": "value",
    "nested": {
      "field": "data"
    }
  }
}
```

##### Response (201 Created)
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": {"key": "value", "nested": {"field": "data"}},
  "created_at": "2025-07-16T12:00:00Z",
  "updated_at": "2025-07-16T12:00:00Z"
}
```

#### Update Record
```http
PUT /api/v1/records/{id}
```

##### Path Parameters
- `id` (uuid): Record identifier

##### Request Body
```json
{
  "data": {
    "key": "new_value",
    "additional": "field"
  }
}
```

##### Response
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": {"key": "new_value", "additional": "field"},
  "created_at": "2025-07-16T12:00:00Z",
  "updated_at": "2025-07-16T12:15:00Z"
}
```

#### Partial Update Record
```http
PATCH /api/v1/records/{id}
```

##### Request Body (JSON Patch)
```json
[
  {"op": "replace", "path": "/data/key", "value": "new_value"},
  {"op": "add", "path": "/data/new_field", "value": "new_data"}
]
```

#### Delete Record
```http
DELETE /api/v1/records/{id}
```

##### Response (204 No Content)
Empty response body

---

## 6. Error Responses

### Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "data"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Not Found (404)
```json
{
  "detail": "Record not found"
}
```

### Server Error (500)
```json
{
  "detail": "Internal server error",
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## 7. Pagination

Haven uses offset-based pagination for REST endpoints:

```http
GET /api/v1/records?limit=20&offset=40
```

To iterate through all records:
```python
offset = 0
limit = 20
while True:
    response = requests.get(f"/api/v1/records?limit={limit}&offset={offset}")
    data = response.json()
    
    for record in data["items"]:
        process(record)
    
    if offset + limit >= data["total"]:
        break
        
    offset += limit
```

---

## 8. Rate Limiting

Local development has no rate limits. Production will enforce:
- 1000 requests per hour per IP
- 10000 requests per hour per API key
- Burst allowance of 100 requests

Rate limit headers:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1625097600
```

---

## 9. Webhooks (Future)

Haven will support webhooks for real-time notifications:

```json
{
  "event": "record.created",
  "timestamp": "2025-07-16T12:00:00Z",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "data": {"key": "value"}
  }
}
```

---

## 10. Client Examples

### cURL
```bash
# Create record
curl -X POST http://api.haven.local/api/v1/records \
  -H "Content-Type: application/json" \
  -d '{"data": {"key": "value"}}'

# Get record
curl http://api.haven.local/api/v1/records/550e8400-e29b-41d4-a716-446655440000
```

### Python (httpx)
```python
import httpx

async with httpx.AsyncClient(base_url="http://api.haven.local") as client:
    # Create
    response = await client.post("/api/v1/records", json={"data": {"key": "value"}})
    record = response.json()
    
    # Get
    response = await client.get(f"/api/v1/records/{record['id']}")
```

### JavaScript (fetch)
```javascript
// Create record
const response = await fetch('http://api.haven.local/api/v1/records', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({data: {key: 'value'}})
});
const record = await response.json();
```

---

*Note: This documentation is auto-generated from the OpenAPI schema. Run `just docs` to regenerate after API changes.*