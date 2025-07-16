"""End-to-end tests for complete user flows."""

import pytest
from fastapi.testclient import TestClient

from haven.interface.api.app import create_app


@pytest.mark.e2e
class TestFullFlow:
    """Test complete user flows through the application."""

    def test_complete_crud_flow_rest(self, test_test_client: TestClient) -> None:
        """Test complete CRUD flow via REST API."""
        # 1. Create a record
        create_data = {
            "name": "E2E Test Record",
            "description": "Testing full flow",
            "metadata": {"tags": ["e2e", "test"]},
        }
        create_response = test_client.post("/api/v1/records", json={"data": create_data})
        assert create_response.status_code == 201
        record_id = create_response.json()["id"]

        # 2. Read the record
        get_response = test_client.get(f"/api/v1/records/{record_id}")
        assert get_response.status_code == 200
        assert get_response.json()["data"] == create_data

        # 3. Update the record
        update_data = {
            "name": "Updated E2E Record",
            "description": "Updated description",
            "metadata": {"tags": ["e2e", "updated"]},
        }
        update_response = test_client.put(f"/api/v1/records/{record_id}", json={"data": update_data})
        assert update_response.status_code == 200
        assert update_response.json()["data"] == update_data

        # 4. List records
        list_response = test_client.get("/api/v1/records")
        assert list_response.status_code == 200
        records = list_response.json()["items"]
        assert any(r["id"] == record_id for r in records)

        # 5. Delete the record
        delete_response = test_client.delete(f"/api/v1/records/{record_id}")
        assert delete_response.status_code == 204

        # 6. Verify deletion
        verify_response = test_client.get(f"/api/v1/records/{record_id}")
        assert verify_response.status_code == 404

    def test_complete_crud_flow_graphql(self, test_client: TestClient) -> None:
        """Test complete CRUD flow via GraphQL API."""
        # 1. Create a record
        create_mutation = """
        mutation CreateRecord($input: RecordInput!) {
            createRecord(input: $input) {
                id
                data
                createdAt
            }
        }
        """
        create_variables = {
            "input": {
                "data": {
                    "name": "GraphQL E2E Record",
                    "type": "test",
                }
            }
        }
        create_response = test_client.post(
            "/graphql",
            json={"query": create_mutation, "variables": create_variables},
        )
        assert create_response.status_code == 200
        record_id = create_response.json()["data"]["createRecord"]["id"]

        # 2. Query the record
        get_query = """
        query GetRecord($id: UUID!) {
            record(id: $id) {
                id
                data
                createdAt
                updatedAt
            }
        }
        """
        get_response = test_client.post(
            "/graphql",
            json={"query": get_query, "variables": {"id": record_id}},
        )
        assert get_response.status_code == 200
        record = get_response.json()["data"]["record"]
        assert record["id"] == record_id

        # 3. Update the record
        update_mutation = """
        mutation UpdateRecord($id: UUID!, $input: RecordInput!) {
            updateRecord(id: $id, input: $input) {
                id
                data
                updatedAt
            }
        }
        """
        update_variables = {
            "id": record_id,
            "input": {"data": {"name": "Updated GraphQL Record", "type": "updated"}},
        }
        update_response = test_client.post(
            "/graphql",
            json={"query": update_mutation, "variables": update_variables},
        )
        assert update_response.status_code == 200

        # 4. List records
        list_query = """
        query ListRecords {
            records(first: 10) {
                edges {
                    node {
                        id
                        data
                    }
                }
                pageInfo {
                    hasNextPage
                }
            }
        }
        """
        list_response = test_client.post("/graphql", json={"query": list_query})
        assert list_response.status_code == 200

        # 5. Delete the record
        delete_mutation = """
        mutation DeleteRecord($id: UUID!) {
            deleteRecord(id: $id)
        }
        """
        delete_response = test_client.post(
            "/graphql",
            json={"query": delete_mutation, "variables": {"id": record_id}},
        )
        assert delete_response.status_code == 200
        assert delete_response.json()["data"]["deleteRecord"] is True

    @pytest.mark.slow
    def test_concurrent_operations(self, test_client: TestClient) -> None:
        """Test concurrent operations don't interfere."""
        import concurrent.futures

        def create_record(index: int) -> str:
            response = test_client.post(
                "/api/v1/records",
                json={"data": {"index": index, "type": "concurrent"}},
            )
            return response.json()["id"]

        # Create multiple records concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(create_record, i) for i in range(10)]
            record_ids = [f.result() for f in futures]

        # Verify all records were created
        assert len(record_ids) == 10
        assert len(set(record_ids)) == 10  # All unique

        # Clean up
        for record_id in record_ids:
            test_client.delete(f"/api/v1/records/{record_id}")
