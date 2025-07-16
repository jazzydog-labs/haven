"""Integration tests for REST API."""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from haven.interface.api.app import create_app


class TestRecordsAPI:
    """Test cases for Records REST API."""

    @pytest.fixture
    def client(self) -> TestClient:
        """Create test client."""
        app = create_app()
        return TestClient(app)

    def test_health_check(self, client: TestClient) -> None:
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    def test_create_record(self, client: TestClient) -> None:
        """Test creating a new record."""
        test_data = {"name": "Test Record", "value": 42}
        response = client.post("/api/v1/records", json={"data": test_data})

        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["data"] == test_data
        assert "created_at" in data
        assert "updated_at" in data

    def test_get_record(self, client: TestClient) -> None:
        """Test getting a record by ID."""
        # First create a record
        test_data = {"name": "Test Record"}
        create_response = client.post("/api/v1/records", json={"data": test_data})
        record_id = create_response.json()["id"]

        # Then get it
        response = client.get(f"/api/v1/records/{record_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == record_id
        assert data["data"] == test_data

    def test_get_nonexistent_record(self, client: TestClient) -> None:
        """Test getting a nonexistent record returns 404."""
        fake_id = uuid4()
        response = client.get(f"/api/v1/records/{fake_id}")
        assert response.status_code == 404

    def test_list_records(self, client: TestClient) -> None:
        """Test listing records with pagination."""
        # Create a few records
        for i in range(5):
            client.post("/api/v1/records", json={"data": {"index": i}})

        # List with pagination
        response = client.get("/api/v1/records?limit=3&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) <= 3
        assert data["total"] >= 5
        assert data["limit"] == 3
        assert data["offset"] == 0

    def test_update_record(self, client: TestClient) -> None:
        """Test updating a record."""
        # Create a record
        create_response = client.post("/api/v1/records", json={"data": {"old": "data"}})
        record_id = create_response.json()["id"]

        # Update it
        new_data = {"new": "data"}
        response = client.put(f"/api/v1/records/{record_id}", json={"data": new_data})
        assert response.status_code == 200
        data = response.json()
        assert data["data"] == new_data

    def test_partial_update_record(self, client: TestClient) -> None:
        """Test partially updating a record."""
        # Create a record
        original_data = {"field1": "value1", "field2": "value2"}
        create_response = client.post("/api/v1/records", json={"data": original_data})
        record_id = create_response.json()["id"]

        # Partially update it
        partial_data = {"field2": "updated"}
        response = client.patch(f"/api/v1/records/{record_id}", json=partial_data)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["field1"] == "value1"
        assert data["data"]["field2"] == "updated"

    def test_delete_record(self, client: TestClient) -> None:
        """Test deleting a record."""
        # Create a record
        create_response = client.post("/api/v1/records", json={"data": {}})
        record_id = create_response.json()["id"]

        # Delete it
        response = client.delete(f"/api/v1/records/{record_id}")
        assert response.status_code == 204

        # Verify it's gone
        get_response = client.get(f"/api/v1/records/{record_id}")
        assert get_response.status_code == 404

    def test_check_record_exists(self, client: TestClient) -> None:
        """Test HEAD request to check record existence."""
        # Create a record
        create_response = client.post("/api/v1/records", json={"data": {}})
        record_id = create_response.json()["id"]

        # Check it exists
        response = client.head(f"/api/v1/records/{record_id}")
        assert response.status_code == 200

        # Check nonexistent
        fake_id = uuid4()
        response = client.head(f"/api/v1/records/{fake_id}")
        assert response.status_code == 404
