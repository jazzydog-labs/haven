from typing import List, Optional
from haven.domain.entities.repository import Repository
from haven.domain.repositories.repository_repository import RepositoryRepository

class RepositoryService:
    def __init__(self, repository_repository: RepositoryRepository):
        self.repository_repository = repository_repository
    
    async def create_repository(
        self, 
        name: str, 
        full_name: str, 
        url: str, 
        branch: str = "main", 
        description: Optional[str] = None,
        is_local: bool = True
    ) -> Repository:
        """Create a new repository"""
        repository = Repository(
            name=name,
            full_name=full_name,
            url=url,
            branch=branch,
            description=description,
            is_local=is_local
        )
        
        return await self.repository_repository.create(repository)
    
    async def get_repository_by_id(self, repo_id: int) -> Optional[Repository]:
        """Get repository by ID"""
        return await self.repository_repository.get_by_id(repo_id)
    
    async def get_repository_by_name(self, name: str) -> Optional[Repository]:
        """Get repository by name"""
        return await self.repository_repository.get_by_name(name)
    
    async def get_repository_by_url(self, url: str) -> Optional[Repository]:
        """Get repository by URL"""
        return await self.repository_repository.get_by_url(url)
    
    async def get_all_repositories(self) -> List[Repository]:
        """Get all repositories"""
        return await self.repository_repository.get_all()
    
    async def update_repository(
        self, 
        repo_id: int, 
        name: Optional[str] = None,
        full_name: Optional[str] = None,
        branch: Optional[str] = None,
        description: Optional[str] = None
    ) -> Repository:
        """Update repository (only certain fields can be updated)"""
        repository = await self.repository_repository.get_by_id(repo_id)
        if not repository:
            raise ValueError(f"Repository with id {repo_id} not found")
        
        if name is not None:
            repository.name = name
        if full_name is not None:
            repository.full_name = full_name
        if branch is not None:
            repository.branch = branch
        if description is not None:
            repository.description = description
        
        return await self.repository_repository.update(repository)
    
    async def delete_repository(self, repo_id: int) -> bool:
        """Delete repository"""
        return await self.repository_repository.delete(repo_id)
    
    def validate_repository_path(self, repository: Repository) -> bool:
        """Validate that repository path exists (for local repositories)"""
        if repository.is_local:
            from pathlib import Path
            return Path(repository.url).exists()
        return True