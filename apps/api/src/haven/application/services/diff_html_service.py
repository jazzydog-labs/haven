"""Service for generating HTML diffs using diff2html."""

import asyncio
import os
import tempfile
from datetime import datetime
from pathlib import Path

from haven.domain.entities.commit import Commit
from haven.domain.repositories.commit_repository import CommitRepository
from haven.infrastructure.git.git_client import GitClient


class DiffHtmlService:
    """Service for generating HTML diffs for commits using diff2html."""

    def __init__(
        self,
        git_client: GitClient,
        commit_repository: CommitRepository,
        output_dir: str = "apps/api/diff-output",
    ):
        """Initialize the diff HTML service."""
        self.git_client = git_client
        self.commit_repository = commit_repository
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_diff_html(self, commit: Commit) -> str:
        """
        Generate HTML diff for a commit using diff2html-cli.

        Args:
            commit: The commit to generate diff for

        Returns:
            Path to the generated HTML file
        """
        # Create output directory for this repository
        repo_dir = self.output_dir / f"repo_{commit.repository_id}"
        repo_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename based on commit hash
        html_filename = f"{commit.commit_hash}.html"
        html_path = repo_dir / html_filename

        # Get the git diff for this commit
        diff_content = await self._get_commit_diff(commit)

        if not diff_content:
            # No diff content (might be initial commit)
            html_content = self._generate_empty_diff_html(commit)
            html_path.write_text(html_content)
        else:
            # Use diff2html-cli to generate HTML
            await self._run_diff2html(diff_content, html_path, commit)

        # Return relative path from project root
        relative_path = html_path.relative_to(Path.cwd())
        return str(relative_path)

    async def _get_commit_diff(self, commit: Commit) -> str:
        """Get the diff content for a commit."""
        # This assumes git_client has a method to get diff
        # You might need to implement this in GitClient
        try:
            # Get diff between commit and its parent
            return await self.git_client.get_commit_diff(commit.repository_id, commit.commit_hash)
        except Exception as e:
            print(f"Error getting diff for commit {commit.commit_hash}: {e}")
            return ""

    async def _run_diff2html(self, diff_content: str, output_path: Path, commit: Commit) -> None:
        """Run diff2html-cli to generate HTML from diff content."""
        # Create temporary file with diff content
        with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as tmp:
            tmp.write(diff_content)
            tmp_path = tmp.name

        try:
            # Run diff2html-cli command
            cmd = [
                "npx",
                "diff2html-cli",
                "--input",
                "file",
                "--output",
                "file",
                "--file",
                str(output_path),
                "--style",
                "side",  # Side-by-side view
                "--title",
                f"Commit {commit.short_hash}: {commit.summary}",
                "--highlightCode",  # Enable syntax highlighting
                tmp_path,
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=str(Path.cwd() / "apps/api"),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise Exception(f"diff2html-cli failed: {stderr.decode()}")

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
        self, commits: list[Commit], max_concurrent: int = 5
    ) -> dict[int, str]:
        """
        Process multiple commits in parallel to generate HTML diffs.

        Args:
            commits: List of commits to process
            max_concurrent: Maximum number of concurrent diff generations

        Returns:
            Dictionary mapping commit IDs to HTML file paths
        """
        results = {}
        semaphore = asyncio.Semaphore(max_concurrent)

        async def process_with_semaphore(commit: Commit) -> tuple[int, str | None]:
            async with semaphore:
                try:
                    html_path = await self.generate_diff_html(commit)
                    # Update commit in database with HTML path
                    commit.diff_html_path = html_path
                    commit.diff_generated_at = datetime.utcnow()
                    await self.commit_repository.update(commit)
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
