from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Repository:
    name: str
    full_name: str
    url: str  # Local path
    branch: str
    repository_hash: str | None = None
    remote_url: str | None = None  # Git remote URL
    description: str | None = None
    is_local: bool = True
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self):
        if not self.name:
            raise ValueError("Repository name cannot be empty")
        if not self.url:
            raise ValueError("Repository URL cannot be empty")
        if not self.branch:
            raise ValueError("Branch cannot be empty")

        # Validate URL format for local repositories
        if self.is_local and not Path(self.url).exists():
            raise ValueError(f"Local repository path does not exist: {self.url}")

    @property
    def display_name(self) -> str:
        """Get display name for UI"""
        return self.full_name or self.name

    @property
    def is_github(self) -> bool:
        """Check if this is a GitHub repository"""
        return "github.com" in self.url.lower()
