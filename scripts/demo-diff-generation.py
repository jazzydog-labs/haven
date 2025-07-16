#!/usr/bin/env python3
"""Demo script for the diff generation API."""

import asyncio
import json
import sys
import time
from pathlib import Path

import httpx


async def demo_diff_generation():
    """Demonstrate the diff generation API."""
    base_url = "http://localhost:8080/api/v1/diffs"
    
    print("🚀 Diff Generation API Demo")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        # 1. Start diff generation
        print("\n1. Starting diff generation...")
        
        # Check if we're on main branch
        import subprocess
        
        # Get the first commit in the repo
        first_commit = subprocess.check_output(
            ["git", "rev-list", "--max-parents=0", "HEAD"],
            text=True
        ).strip()
        
        # Count total commits
        total_commits = int(subprocess.check_output(
            ["git", "rev-list", "--count", "HEAD"],
            text=True
        ).strip())
        
        print(f"   Generating diffs for all {total_commits} commits in the repository")
        print(f"   Base: {first_commit[:7]} (first commit)")
        
        response = await client.post(
            f"{base_url}/generate",
            json={
                "branch": "HEAD",
                "base_branch": first_commit,
                "max_commits": total_commits
            }
        )
        
        if response.status_code != 200:
            print(f"❌ Error: {response.text}")
            return
            
        result = response.json()
        task_id = result["task_id"]
        print(f"✅ Task created: {task_id}")
        
        # 2. Poll for status
        print("\n2. Checking generation status...")
        max_attempts = 30
        for i in range(max_attempts):
            response = await client.get(f"{base_url}/status/{task_id}")
            status_data = response.json()
            
            status = status_data["status"]
            print(f"   Status: {status}", end="")
            
            if status == "completed":
                print(f"\n✅ Completed! Generated {status_data['commit_count']} diff files")
                break
            elif status == "failed":
                print(f"\n❌ Failed: {status_data['message']}")
                return
            else:
                print(" (waiting...)", end="\r")
                await asyncio.sleep(1)
        else:
            print("\n⏱️  Timeout waiting for completion")
            return
        
        # 3. Fetch the index
        print("\n3. Fetching generated index...")
        response = await client.get(f"{base_url}/{task_id}/index.html")
        
        if response.status_code == 200:
            # Save the index file
            output_dir = Path(f"diff-demo-{task_id}")
            output_dir.mkdir(exist_ok=True)
            
            index_path = output_dir / "index.html"
            index_path.write_text(response.text)
            print(f"✅ Saved index to: {index_path}")
            
            # Download individual diff files
            print("\n4. Downloading diff files...")
            
            # Parse the JavaScript data to find the diff files
            import re
            # Look for file: 'filename.html' in the JavaScript
            file_pattern = r"file:\s*'([^']+\.html)'"
            files = re.findall(file_pattern, response.text)
            
            downloaded = 0
            for filename in files:
                if filename != "index.html":
                    print(f"   Downloading: {filename}")
                    file_response = await client.get(f"{base_url}/{task_id}/files/{filename}")
                    if file_response.status_code == 200:
                        file_path = output_dir / filename
                        file_path.write_text(file_response.text)
                        downloaded += 1
                    else:
                        print(f"   ⚠️  Failed to download: {filename}")
            
            print(f"   ✅ Downloaded {downloaded} diff files")
            
            # 5. Cleanup option
            print("\n5. Cleanup (optional)")
            print(f"   To clean up: DELETE {base_url}/{task_id}")
            
            print(f"\n✨ Demo complete! Open {index_path} in your browser")
            print(f"   Or run: python -m http.server 8000 --directory {output_dir}")
            
        else:
            print(f"❌ Error fetching index: {response.status_code}")


async def check_server():
    """Check if the server is running."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8080/health")
            return response.status_code == 200
    except:
        return False


async def main():
    """Main demo function."""
    # Check if server is running
    if not await check_server():
        print("❌ Server is not running!")
        print("   Please start the server first: just run")
        sys.exit(1)
    
    try:
        await demo_diff_generation()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())