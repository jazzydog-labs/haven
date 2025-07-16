# Haven – GraphQL Reference

*Last updated: 2025‑07‑15*

Haven exposes a code‑first GraphQL API built with **Strawberry**.  The interactive IDE lives at **`/graphql`** (GraphiQL) and hot‑reloads alongside the FastAPI REST routes.

---

## 1  Schema Definition Language (SDL)

Below is the canonical SDL as rendered by Strawberry.  Copy‑pasted here for quick reference; the live endpoint is always source‑of‑truth.

```graphql
"""Root query type"""
type Query {
  """Return a single Record by its UUID"""
  record(id: UUID!): Record

  """List records with optional pagination cursor"""
  records(first: Int = 25, after: String): RecordConnection!
}

"""Root mutation type"""
type Mutation {
  """Create a new Record"""
  createRecord(input: RecordInput!): Record!
  
  """Update an existing Record"""
  updateRecord(id: UUID!, input: RecordInput!): Record!
  
  """Delete by UUID; returns true if removed"""
  deleteRecord(id: UUID!): Boolean!
}

"""Aggregate representing arbitrary JSON payload"""
type Record {
  id: UUID!
  createdAt: DateTime!
  updatedAt: DateTime!
  data: JSON!
}

"""Input type reused for create & update"""
input RecordInput {
  data: JSON!
}

"""Relay‑style cursor connection for Record lists"""
type RecordConnection {
  edges: [RecordEdge!]!
  pageInfo: PageInfo!
}

type RecordEdge {
  cursor: String!
  node: Record!
}

type PageInfo {
  hasNextPage: Boolean!
  endCursor: String
}
```

> **Note** Strawberry auto‑generates scalars for `UUID`, `DateTime`, and `JSON` via Pydantic.

---

## 2  Sample Queries and Mutations

### 2.1  Create a Record

```graphql
mutation CreateRecord {
  createRecord(input: { data: { "hello": "world" } }) {
    id
    createdAt
    data
  }
}
```

### 2.2  Fetch a Single Record

```graphql
query GetOne {
  record(id: "c0235b50‑7034‑4a2e‑9990‑c4b2e268e5a1") {
    id
    data
  }
}
```

### 2.3  Cursor‑based Pagination

```graphql
query Paginated($first: Int = 10, $after: String) {
  records(first: $first, after: $after) {
    edges {
      cursor
      node { id data }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

Sample client loop (pseudo‑Python):

```python
cursor = None
while True:
    resp = gql("""{ records(first: 50, after: $after) { ... }}""", variables={"after": cursor})
    for rec in resp["edges"]:
        process(rec["node"])
    if not resp["pageInfo"]["hasNextPage"]:
        break
    cursor = resp["pageInfo"]["endCursor"]
```

### 2.4  Update a Record

```graphql
mutation Update {
  updateRecord(id: "c0235b50‑7034‑4a2e‑9990‑c4b2e268e5a1", input: { data: { "foo": 42 } }) {
    id
    data
    updatedAt
  }
}
```

### 2.5  Delete a Record

```graphql
mutation Delete {
  deleteRecord(id: "c0235b50‑7034‑4a2e‑9990‑c4b2e268e5a1")
}
```

`true` indicates the row was removed; if `false`, the UUID didn’t exist.

---

## 3  Pagination Strategy

* **Cursor style** – uses opaque Base64 cursors; no offset‑based pagination, which avoids skipped rows on concurrent inserts.
* **Arguments** – `first` (limit) and `after` (cursor).
* **PageInfo** – Relay spec fields; clients stop when `hasNextPage = false`.

> Limit defaults to **25**; max is **250**—configurable via `conf/.../graphql.yaml`.

---

## 4  Error Handling

All errors conform to GraphQL spec: HTTP 200 with `errors` array.  We surface domain violations (e.g., “duplicate key”) as `BAD_USER_INPUT`, while unexpected exceptions map to `INTERNAL_SERVER_ERROR`.

```json
{
  "errors": [
    {
      "message": "Record not found",
      "extensions": { "code": "NOT_FOUND" }
    }
  ]
}
```

---

## 5  Testing the GraphQL Layer

Integration tests use **httpx.AsyncClient** against the ASGI app:

```python
async def test_create_record(client):
    q = """mutation($input: RecordInput!) { createRecord(input: $input) { id } }"""
    variables = {"input": {"data": {"hello": "world"}}}
    resp = await client.post("/graphql", json={"query": q, "variables": variables})
    assert resp.json()["data"]["createRecord"]["id"]
```

Tests live in `tests/integration/api/` alongside REST equivalents.

---

## 6  Future Enhancements

* **Filtering / sorting** – GraphQL‑compatible “where” DSL or Dataloader approach.
* **Subscriptions** – real‑time record updates via WebSocket transport.
* **Batch mutations** – bulk create/update for high‑volume ingest.

---

Questions? Open an issue or ping #haven‑dev.
