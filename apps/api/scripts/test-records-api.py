#!/usr/bin/env python3
"""Test Records API endpoints"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8080/api/v1"

def test_records_api():
    """Test all CRUD operations for records"""
    print("Testing Records API...")
    
    # 1. Create a record
    print("\n1. Creating a record...")
    create_data = {
        "data": {
            "name": "Test Record",
            "type": "example",
            "value": 42,
            "active": True,
            "tags": ["test", "example"],
            "metadata": {
                "created_by": "test_script",
                "purpose": "API testing"
            }
        }
    }
    
    response = requests.post(f"{BASE_URL}/records", json=create_data)
    print(f"Status: {response.status_code}")
    if response.status_code in (200, 201):
        record = response.json()
        print(f"Created record: {json.dumps(record, indent=2)}")
        record_id = record["id"]
    else:
        print(f"Error: {response.text}")
        return
    
    # 2. List records
    print("\n2. Listing records...")
    response = requests.get(f"{BASE_URL}/records?limit=10&offset=0")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total records: {data['total']}")
        print(f"Records returned: {len(data['items'])}")
    else:
        print(f"Error: {response.text}")
    
    # 3. Get specific record
    print(f"\n3. Getting record {record_id}...")
    response = requests.get(f"{BASE_URL}/records/{record_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Record: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    
    # 4. Update record
    print(f"\n4. Updating record {record_id}...")
    update_data = {
        "data": {
            "name": "Updated Test Record",
            "type": "example",
            "value": 100,
            "active": False,
            "tags": ["test", "example", "updated"],
            "metadata": {
                "created_by": "test_script",
                "purpose": "API testing",
                "updated_at": datetime.now().isoformat()
            }
        }
    }
    
    response = requests.put(f"{BASE_URL}/records/{record_id}", json=update_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Updated record: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    
    # 5. Delete record
    print(f"\n5. Deleting record {record_id}...")
    response = requests.delete(f"{BASE_URL}/records/{record_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Record deleted successfully")
    else:
        print(f"Error: {response.text}")
    
    # 6. Verify deletion
    print(f"\n6. Verifying deletion...")
    response = requests.get(f"{BASE_URL}/records/{record_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 404:
        print("Record not found (as expected)")
    else:
        print(f"Unexpected response: {response.text}")

if __name__ == "__main__":
    test_records_api()