#!/usr/bin/env python
"""Script to bootstrap Haven repository commits."""

import asyncio
import requests

async def bootstrap_haven_commits():
    """Load all commits for Haven repository."""
    
    # First, get the repository info
    response = requests.get("http://localhost:8080/api/v1/repositories/haven")
    if response.status_code == 404:
        response = requests.get("http://localhost:8080/api/v1/repositories/5b40a07c")
    
    if response.status_code != 200:
        print(f"Error: Could not find Haven repository. Status: {response.status_code}")
        return
    
    repo_data = response.json()
    identifier = repo_data.get("slug") or repo_data.get("repository_hash")
    
    print(f"Found Haven repository: {repo_data['name']} (identifier: {identifier})")
    print(f"Current stats:")
    
    # Get current stats
    stats_response = requests.get(f"http://localhost:8080/api/v1/repository-management/{identifier}/stats")
    if stats_response.status_code == 200:
        stats = stats_response.json()
        print(f"  Total commits: {stats['total_commits']}")
        print(f"  Total branches: {stats['total_branches']}")
        print(f"  Latest commit: {stats['latest_commit_date']}")
        print(f"  Oldest commit: {stats['oldest_commit_date']}")
    
    # Load commits
    print("\nLoading all commits from main branch...")
    load_response = requests.post(
        f"http://localhost:8080/api/v1/repository-management/{identifier}/load-commits",
        json={
            "branch": "main",
            "limit": None  # Load all commits
        }
    )
    
    if load_response.status_code == 200:
        result = load_response.json()
        print(f"Success: {result['message']}")
        print(f"Task ID: {result.get('task_id', 'N/A')}")
        
        # Wait a bit and check stats again
        print("\nWaiting for commits to load...")
        await asyncio.sleep(5)
        
        stats_response = requests.get(f"http://localhost:8080/api/v1/repository-management/{identifier}/stats")
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"\nUpdated stats:")
            print(f"  Total commits: {stats['total_commits']}")
            print(f"  Total branches: {stats['total_branches']}")
            print(f"  Latest commit: {stats['latest_commit_date']}")
            print(f"  Oldest commit: {stats['oldest_commit_date']}")
    else:
        print(f"Error loading commits: {load_response.status_code}")
        print(load_response.text)


if __name__ == "__main__":
    asyncio.run(bootstrap_haven_commits())