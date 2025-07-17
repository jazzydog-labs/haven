"""Service for generating JSON diffs using diff2html."""

import asyncio
import json
import os
import tempfile
from datetime import datetime
from pathlib import Path

from haven.domain.entities.commit import Commit
from haven.domain.repositories.commit_repository import CommitRepository
from haven.infrastructure.git.git_client import GitClient


class DiffHtmlService:
    """Service for generating diff data for commits using diff2html."""

    def __init__(
        self,
        git_client: GitClient,
        commit_repository: CommitRepository,
        output_dir: str = "/app/diff-output",
    ):
        """Initialize the diff service."""
        self.git_client = git_client
        self.commit_repository = commit_repository
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_diff_html(self, commit: Commit, repo_path: str = "/repo") -> str:
        """
        Generate JSON diff data for a commit using diff2html-cli.

        Args:
            commit: The commit to generate diff for
            repo_path: Path to the repository (default: "/repo")

        Returns:
            Path to the generated JSON file
        """
        # Create output directory for this repository
        repo_dir = self.output_dir / f"repo_{commit.repository_id}"
        repo_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename based on commit hash
        json_filename = f"{commit.commit_hash}.json"
        json_path = repo_dir / json_filename

        # Get the git diff for this commit
        diff_content = await self._get_commit_diff(commit, repo_path)

        if not diff_content:
            # No diff content (might be initial commit)
            empty_diff_data = {
                "commit": {
                    "hash": commit.commit_hash,
                    "short_hash": commit.short_hash,
                    "summary": commit.summary,
                    "message": commit.message,
                    "author_name": commit.author_name,
                    "author_email": commit.author_email,
                    "committed_at": commit.committed_at.isoformat()
                },
                "files": []
            }
            json_path.write_text(json.dumps(empty_diff_data, indent=2))
        else:
            # Use diff2html-cli to generate JSON
            await self._run_diff2html_json(diff_content, json_path, commit)

        # Note: Commit update is handled by the caller to ensure proper transaction management

        # Return relative path from project root
        relative_path = json_path.relative_to(Path.cwd())
        return str(relative_path)

    async def _get_commit_diff(self, commit: Commit, repo_path: str) -> str:
        """Get the diff content for a commit."""
        try:
            # Get diff between commit and its parent
            return await self.git_client.get_commit_diff(repo_path, commit.commit_hash)
        except Exception as e:
            print(f"Error getting diff for commit {commit.commit_hash}: {e}")
            return ""

    async def _run_diff2html_json(self, diff_content: str, output_path: Path, commit: Commit) -> None:
        """Run diff2html-cli to generate JSON from diff content."""
        # Create temporary file with diff content
        with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as tmp:
            tmp.write(diff_content)
            tmp_path = tmp.name

        try:
            # Run diff2html-cli command to generate JSON
            cmd = [
                "/usr/local/bin/diff2html",
                "--input",
                "file",
                "--format",
                "json",
                "--output",
                "stdout",
                "--",
                tmp_path,
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise Exception(f"diff2html-cli failed: {stderr.decode()}")

            # Parse the JSON output
            diff_data = json.loads(stdout.decode())
            
            # Enhance with commit metadata
            enhanced_data = {
                "commit": {
                    "hash": commit.commit_hash,
                    "short_hash": commit.short_hash,
                    "summary": commit.summary,
                    "message": commit.message,
                    "author_name": commit.author_name,
                    "author_email": commit.author_email,
                    "committed_at": commit.committed_at.isoformat()
                },
                "files": diff_data
            }
            
            # Write enhanced JSON to file
            output_path.write_text(json.dumps(enhanced_data, indent=2))

        finally:
            # Clean up temporary file
            os.unlink(tmp_path)

    def _generate_empty_diff_html(self, commit: Commit) -> str:
        """Generate HTML for commits with no diff (e.g., initial commit)."""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Commit {commit.short_hash}: {commit.summary}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .commit-info {{
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 20px;
            margin-bottom: 20px;
        }}
        .commit-hash {{
            font-family: monospace;
            background-color: #f0f0f0;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        .no-changes {{
            text-align: center;
            color: #666;
            padding: 40px;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="commit-info">
            <h1>Commit <span class="commit-hash">{commit.short_hash}</span></h1>
            <h2>{commit.summary}</h2>
            <p><strong>Author:</strong> {commit.author_name} &lt;{commit.author_email}&gt;</p>
            <p><strong>Date:</strong> {commit.committed_at.strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        <div class="no-changes">
            No changes in this commit (might be an initial commit or merge commit with no conflicts)
        </div>
    </div>
</body>
</html>
"""

    async def process_commits_batch(
        self, commits: list[Commit], repo_path: str = "/repo", max_concurrent: int = 5
    ) -> dict[int, str]:
        """
        Process multiple commits in parallel to generate HTML diffs.

        Args:
            commits: List of commits to process
            repo_path: Path to the repository
            max_concurrent: Maximum number of concurrent diff generations

        Returns:
            Dictionary mapping commit IDs to HTML file paths
        """
        results = {}
        semaphore = asyncio.Semaphore(max_concurrent)

        async def process_with_semaphore(commit: Commit) -> tuple[int, str | None]:
            async with semaphore:
                try:
                    html_path = await self.generate_diff_html(commit, repo_path)
                    return (commit.id, html_path)
                except Exception as e:
                    print(f"Error processing commit {commit.id}: {e}")
                    return (commit.id, None)

        # Process all commits concurrently
        tasks = [process_with_semaphore(commit) for commit in commits]
        completed = await asyncio.gather(*tasks)

        # Build results dictionary
        for commit_id, html_path in completed:
            if html_path:
                results[commit_id] = html_path

        return results
