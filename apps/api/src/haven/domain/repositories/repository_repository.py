from abc import ABC, abstractmethod
from typing import List, Optional
from haven.domain.entities.repository import Repository

class RepositoryRepository(ABC):
    @abstractmethod
    async def create(self, repository: Repository) -> Repository:
        """Create a new repository"""
        pass
    
    @abstractmethod
    async def get_by_id(self, repo_id: int) -> Optional[Repository]:
        """Get repository by ID"""
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Repository]:
        """Get repository by name"""
        pass
    
    @abstractmethod
    async def get_by_url(self, url: str) -> Optional[Repository]:
        """Get repository by URL"""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Repository]:
        """Get all repositories"""
        pass
    
    @abstractmethod
    async def update(self, repository: Repository) -> Repository:
        """Update existing repository"""
        pass
    
    @abstractmethod
    async def delete(self, repo_id: int) -> bool:
        """Delete repository"""
        pass