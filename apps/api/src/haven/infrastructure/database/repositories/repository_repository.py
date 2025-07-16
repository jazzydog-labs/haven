from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from haven.domain.entities.repository import Repository
from haven.domain.repositories.repository_repository import RepositoryRepository
from haven.infrastructure.database.models import RepositoryModel

class RepositoryRepositoryImpl(RepositoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, repository: Repository) -> Repository:
        """Create a new repository"""
        db_repository = RepositoryModel(
            name=repository.name,
            full_name=repository.full_name,
            url=repository.url,
            branch=repository.branch,
            description=repository.description,
            is_local=repository.is_local
        )
        
        try:
            self.session.add(db_repository)
            await self.session.commit()
            await self.session.refresh(db_repository)
            return self._to_entity(db_repository)
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Repository with this name or URL already exists")
    
    async def get_by_id(self, repo_id: int) -> Optional[Repository]:
        """Get repository by ID"""
        stmt = select(RepositoryModel).where(RepositoryModel.id == repo_id)
        result = await self.session.execute(stmt)
        db_repository = result.scalar_one_or_none()
        return self._to_entity(db_repository) if db_repository else None
    
    async def get_by_name(self, name: str) -> Optional[Repository]:
        """Get repository by name"""
        stmt = select(RepositoryModel).where(RepositoryModel.name == name)
        result = await self.session.execute(stmt)
        db_repository = result.scalar_one_or_none()
        return self._to_entity(db_repository) if db_repository else None
    
    async def get_by_url(self, url: str) -> Optional[Repository]:
        """Get repository by URL"""
        stmt = select(RepositoryModel).where(RepositoryModel.url == url)
        result = await self.session.execute(stmt)
        db_repository = result.scalar_one_or_none()
        return self._to_entity(db_repository) if db_repository else None
    
    async def get_all(self) -> List[Repository]:
        """Get all repositories"""
        stmt = select(RepositoryModel)
        result = await self.session.execute(stmt)
        db_repositories = result.scalars().all()
        return [self._to_entity(db_repo) for db_repo in db_repositories]
    
    async def update(self, repository: Repository) -> Repository:
        """Update existing repository"""
        stmt = select(RepositoryModel).where(RepositoryModel.id == repository.id)
        result = await self.session.execute(stmt)
        db_repository = result.scalar_one_or_none()
        
        if not db_repository:
            raise ValueError(f"Repository with id {repository.id} not found")
        
        db_repository.name = repository.name
        db_repository.full_name = repository.full_name
        db_repository.url = repository.url
        db_repository.branch = repository.branch
        db_repository.description = repository.description
        db_repository.is_local = repository.is_local
        
        await self.session.commit()
        await self.session.refresh(db_repository)
        return self._to_entity(db_repository)
    
    async def delete(self, repo_id: int) -> bool:
        """Delete repository"""
        stmt = select(RepositoryModel).where(RepositoryModel.id == repo_id)
        result = await self.session.execute(stmt)
        db_repository = result.scalar_one_or_none()
        
        if not db_repository:
            return False
        
        await self.session.delete(db_repository)
        await self.session.commit()
        return True
    
    def _to_entity(self, db_repository: RepositoryModel) -> Repository:
        """Convert database model to domain entity"""
        return Repository(
            id=db_repository.id,
            name=db_repository.name,
            full_name=db_repository.full_name,
            url=db_repository.url,
            branch=db_repository.branch,
            description=db_repository.description,
            is_local=db_repository.is_local,
            created_at=db_repository.created_at,
            updated_at=db_repository.updated_at
        )