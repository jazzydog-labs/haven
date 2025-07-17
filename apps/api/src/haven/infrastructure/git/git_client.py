"""Git client for interacting with git repositories."""

import asyncio
from pathlib import Path


class GitClient:
    """Client for interacting with git repositories."""

    def __init__(self, repos_base_path: str = "/tmp/haven-repos"):
        """Initialize git client with base path for repositories."""
        self.repos_base_path = Path(repos_base_path)
        self.repos_base_path.mkdir(parents=True, exist_ok=True)

    async def get_commit_diff(self, repository_id: int, commit_hash: str) -> str:
        """
        Get the diff for a specific commit.

        Args:
            repository_id: ID of the repository
            commit_hash: Hash of the commit

        Returns:
            Unified diff content as string
        """
        # For now, we'll use a mock implementation
        # In a real system, this would clone/fetch the repo and get the actual diff
        repo_path = self._get_repo_path(repository_id)

        if not repo_path.exists():
            # Mock some diff content for demonstration
            return self._generate_mock_diff(commit_hash)

        # Run git show to get the diff
        cmd = ["git", "show", "--format=", commit_hash]

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=str(repo_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise Exception(f"Git command failed: {stderr.decode()}")

            return stdout.decode()

        except Exception as e:
            print(f"Error getting diff: {e}")
            # Return mock diff on error
            return self._generate_mock_diff(commit_hash)

    def _get_repo_path(self, repository_id: int) -> Path:
        """Get the local path for a repository."""
        return self.repos_base_path / f"repo_{repository_id}"

    def _generate_mock_diff(self, commit_hash: str) -> str:
        """Generate a mock diff for testing."""
        return f"""diff --git a/src/example.py b/src/example.py
index 1234567..abcdefg 100644
--- a/src/example.py
+++ b/src/example.py
@@ -1,10 +1,15 @@
 def hello_world():
-    print("Hello, World!")
+    print("Hello, Haven!")
+    print("This is commit {commit_hash[:7]}")

 def main():
     hello_world()
+    # New feature added
+    process_data()
+
+def process_data():
+    data = [1, 2, 3, 4, 5]
+    return sum(data)

 if __name__ == "__main__":
     main()
"""

    async def clone_repository(self, repository_id: int, clone_url: str) -> Path:
        """
        Clone a repository to local storage.

        Args:
            repository_id: ID of the repository
            clone_url: Git URL to clone from

        Returns:
            Path to the cloned repository
        """
        repo_path = self._get_repo_path(repository_id)

        if repo_path.exists():
            # Repository already exists, pull latest
            await self._git_pull(repo_path)
        else:
            # Clone the repository
            await self._git_clone(clone_url, repo_path)

        return repo_path

    async def _git_clone(self, url: str, target_path: Path) -> None:
        """Clone a git repository."""
        cmd = ["git", "clone", url, str(target_path)]

        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise Exception(f"Git clone failed: {stderr.decode()}")

    async def _git_pull(self, repo_path: Path) -> None:
        """Pull latest changes in a repository."""
        cmd = ["git", "pull"]

        process = await asyncio.create_subprocess_exec(
            *cmd, cwd=str(repo_path), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise Exception(f"Git pull failed: {stderr.decode()}")

    async def _run_command(self, cmd: list[str], cwd: str | None = None) -> str:
        """Run a git command and return output."""
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise Exception(f"Command failed: {stderr.decode()}")
        return stdout.decode()

    async def list_files(self, repo_path: str, ref: str = "HEAD") -> list[str]:
        """List all files in repository at given ref."""
        result = await self._run_command(
            ["git", "ls-tree", "-r", "--name-only", ref], cwd=repo_path
        )
        return result.strip().split("\n") if result.strip() else []

    async def get_remote_url(self, repo_path: str, remote: str = "origin") -> str | None:
        """Get the remote URL for a repository."""
        try:
            result = await self._run_command(
                ["git", "config", "--get", f"remote.{remote}.url"], cwd=repo_path
            )
            return result.strip() if result.strip() else None
        except Exception:
            return None

    async def get_current_branch(self, repo_path: str) -> str | None:
        """Get the current branch name."""
        try:
            result = await self._run_command(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_path
            )
            return result.strip() if result.strip() else None
        except Exception:
            return None

    async def get_branches(self, repo_path: str) -> list[str]:
        """Get all branch names."""
        try:
            result = await self._run_command(
                ["git", "branch", "-a", "--format=%(refname:short)"], cwd=repo_path
            )
            branches = result.strip().split("\n") if result.strip() else []
            # Remove duplicates and sort
            return sorted(list(set(branches)))
        except Exception:
            return []

    async def get_commit_count(self, repo_path: str, branch: str = "HEAD") -> int:
        """Get the total number of commits in a branch."""
        try:
            result = await self._run_command(
                ["git", "rev-list", "--count", branch], cwd=repo_path
            )
            return int(result.strip()) if result.strip() else 0
        except Exception:
            return 0
