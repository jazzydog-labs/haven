from abc import ABC, abstractmethod

from haven.domain.entities.repository import Repository


class RepositoryRepository(ABC):
    @abstractmethod
    async def create(self, repository: Repository) -> Repository:
        """Create a new repository"""
        pass

    @abstractmethod
    async def get_by_id(self, repo_id: int) -> Repository | None:
        """Get repository by ID"""
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Repository | None:
        """Get repository by name"""
        pass

    @abstractmethod
    async def get_by_url(self, url: str) -> Repository | None:
        """Get repository by URL"""
        pass

    @abstractmethod
    async def get_all(self) -> list[Repository]:
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
