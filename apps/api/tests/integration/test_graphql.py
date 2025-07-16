"""Integration tests for GraphQL API."""

import pytest
from fastapi.testclient import TestClient

from haven.interface.api.app import create_app


class TestGraphQLAPI:
    """Test cases for GraphQL API."""

    def graphql_request(self, test_test_client: TestClient, query: str, variables: dict | None = None):
        """Helper to make GraphQL requests."""
        response = test_client.post(
            "/graphql",
            json={"query": query, "variables": variables or {}},
        )
        return response

    def test_create_record_mutation(self, test_client: TestClient) -> None:
        """Test creating a record via GraphQL."""
        mutation = """
        mutation CreateRecord($input: RecordInput!) {
            createRecord(input: $input) {
                id
                data
                createdAt
                updatedAt
            }
        }
        """
        variables = {"input": {"data": {"name": "GraphQL Record", "value": 123}}}

        response = self.graphql_request(test_client, mutation, variables)
        assert response.status_code == 200

        data = response.json()
        assert "data" in data
        assert "createRecord" in data["data"]

        record = data["data"]["createRecord"]
        assert "id" in record
        assert record["data"] == {"name": "GraphQL Record", "value": 123}

    def test_get_record_query(self, test_client: TestClient) -> None:
        """Test getting a record via GraphQL."""
        # First create a record
        create_mutation = """
        mutation CreateRecord($input: RecordInput!) {
            createRecord(input: $input) {
                id
            }
        }
        """
        create_response = self.graphql_request(
            test_client, create_mutation, {"input": {"data": {"test": "data"}}}
        )
        record_id = create_response.json()["data"]["createRecord"]["id"]

        # Then query it
        query = """
        query GetRecord($id: UUID!) {
            record(id: $id) {
                id
                data
                createdAt
                updatedAt
            }
        }
        """
        response = self.graphql_request(test_client, query, {"id": record_id})
        assert response.status_code == 200

        data = response.json()
        record = data["data"]["record"]
        assert record["id"] == record_id
        assert record["data"] == {"test": "data"}

    def test_list_records_query(self, test_client: TestClient) -> None:
        """Test listing records with pagination via GraphQL."""
        # Create some records
        create_mutation = """
        mutation CreateRecord($input: RecordInput!) {
            createRecord(input: $input) {
                id
            }
        }
        """
        for i in range(5):
            self.graphql_request(test_client, create_mutation, {"input": {"data": {"index": i}}})

        # Query with pagination
        query = """
        query ListRecords($first: Int!, $after: String) {
            records(first: $first, after: $after) {
                edges {
                    cursor
                    node {
                        id
                        data
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
        """
        response = self.graphql_request(test_client, query, {"first": 3})
        assert response.status_code == 200

        data = response.json()
        connection = data["data"]["records"]
        assert len(connection["edges"]) <= 3
        assert "pageInfo" in connection
        assert isinstance(connection["pageInfo"]["hasNextPage"], bool)

    def test_update_record_mutation(self, test_client: TestClient) -> None:
        """Test updating a record via GraphQL."""
        # Create a record
        create_mutation = """
        mutation CreateRecord($input: RecordInput!) {
            createRecord(input: $input) {
                id
            }
        }
        """
        create_response = self.graphql_request(
            test_client, create_mutation, {"input": {"data": {"old": "data"}}}
        )
        record_id = create_response.json()["data"]["createRecord"]["id"]

        # Update it
        update_mutation = """
        mutation UpdateRecord($id: UUID!, $input: RecordInput!) {
            updateRecord(id: $id, input: $input) {
                id
                data
            }
        }
        """
        variables = {
            "id": record_id,
            "input": {"data": {"new": "data"}},
        }
        response = self.graphql_request(test_client, update_mutation, variables)
        assert response.status_code == 200

        data = response.json()
        record = data["data"]["updateRecord"]
        assert record["id"] == record_id
        assert record["data"] == {"new": "data"}

    def test_delete_record_mutation(self, test_client: TestClient) -> None:
        """Test deleting a record via GraphQL."""
        # Create a record
        create_mutation = """
        mutation CreateRecord($input: RecordInput!) {
            createRecord(input: $input) {
                id
            }
        }
        """
        create_response = self.graphql_request(test_client, create_mutation, {"input": {"data": {}}})
        record_id = create_response.json()["data"]["createRecord"]["id"]

        # Delete it
        delete_mutation = """
        mutation DeleteRecord($id: UUID!) {
            deleteRecord(id: $id)
        }
        """
        response = self.graphql_request(test_client, delete_mutation, {"id": record_id})
        assert response.status_code == 200

        data = response.json()
        assert data["data"]["deleteRecord"] is True

        # Verify it's gone
        query = """
        query GetRecord($id: UUID!) {
            record(id: $id) {
                id
            }
        }
        """
        verify_response = self.graphql_request(test_client, query, {"id": record_id})
        assert verify_response.json()["data"]["record"] is None

    def test_graphql_introspection(self, test_client: TestClient) -> None:
        """Test GraphQL introspection query."""
        query = """
        {
            __schema {
                types {
                    name
                }
            }
        }
        """
        response = self.graphql_request(test_client, query)
        assert response.status_code == 200

        data = response.json()
        type_names = [t["name"] for t in data["data"]["__schema"]["types"]]
        assert "RecordType" in type_names
        assert "Query" in type_names
        assert "Mutation" in type_names
