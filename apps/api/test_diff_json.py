#!/usr/bin/env python3
"""Test script to generate JSON diff output"""

import asyncio
import json
import subprocess
import tempfile
from pathlib import Path


async def test_diff_json():
    # Get a sample diff from the repository
    repo_path = "/repo"
    
    # Get the latest commit hash
    result = subprocess.run(
        ["git", "log", "-1", "--format=%H"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    commit_hash = result.stdout.strip()
    
    print(f"Testing with commit: {commit_hash}")
    
    # Get the diff
    result = subprocess.run(
        ["git", "show", "--format=", commit_hash],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    diff_content = result.stdout
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.diff', delete=False) as tmp:
        tmp.write(diff_content)
        tmp_path = tmp.name
    
    # Generate JSON using diff2html
    cmd = [
        "/usr/local/bin/diff2html",
        "-f", "json",
        "-i", "file",
        "--",
        tmp_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(f"Return code: {result.returncode}")
    print(f"Stdout length: {len(result.stdout)}")
    print(f"Stderr: {result.stderr}")
    
    if result.returncode == 0 and result.stdout:
        # Parse and pretty print the JSON
        diff_json = json.loads(result.stdout)
        print(json.dumps(diff_json, indent=2))
        
        # Save to file for inspection
        with open('/app/sample_diff.json', 'w') as f:
            json.dump(diff_json, f, indent=2)
        print("\nJSON saved to /app/sample_diff.json")
    else:
        print(f"Error: {result.stderr}")
    
    # Cleanup
    Path(tmp_path).unlink()


if __name__ == "__main__":
    asyncio.run(test_diff_json())