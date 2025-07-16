from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from pathlib import Path

@dataclass
class Repository:
    name: str
    full_name: str
    url: str
    branch: str
    description: Optional[str] = None
    is_local: bool = True
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("Repository name cannot be empty")
        if not self.url:
            raise ValueError("Repository URL cannot be empty")
        if not self.branch:
            raise ValueError("Branch cannot be empty")
        
        # Validate URL format for local repositories
        if self.is_local:
            if not Path(self.url).exists():
                raise ValueError(f"Local repository path does not exist: {self.url}")
    
    @property
    def display_name(self) -> str:
        """Get display name for UI"""
        return self.full_name or self.name
    
    @property
    def is_github(self) -> bool:
        """Check if this is a GitHub repository"""
        return "github.com" in self.url.lower()