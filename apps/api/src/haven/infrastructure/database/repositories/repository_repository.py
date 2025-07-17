from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from haven.domain.entities.repository import Repository
from haven.domain.repositories.repository_repository import RepositoryRepository
from haven.infrastructure.database.models import RepositoryModel


class RepositoryRepositoryImpl(RepositoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, repository: Repository) -> Repository:
        """Create a new repository"""
        import hashlib
        
        # Generate repository hash from URL
        if not repository.repository_hash:
            repository.repository_hash = hashlib.sha256(repository.url.encode()).hexdigest()
        
        # Generate slug - try using the name first
        slug = repository.slug
        if not slug:
            # Check if name is unique
            existing = await self.get_by_name(repository.name)
            if not existing:
                slug = repository.name.lower()
            else:
                # Use short hash if name is not unique
                slug = repository.repository_hash[:8] if repository.repository_hash else None
        
        db_repository = RepositoryModel(
            name=repository.name,
            full_name=repository.full_name,
            url=repository.url,
            remote_url=repository.remote_url,
            repository_hash=repository.repository_hash,
            slug=slug,
            branch=repository.branch,
            description=repository.description,
            is_local=repository.is_local,
        )

        try:
            self.session.add(db_repository)
            await self.session.commit()
            await self.session.refresh(db_repository)
            return self._to_entity(db_repository)
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Repository with this name or URL already exists") from e

    async def get_by_id(self, repo_id: int) -> Repository | None:
        """Get repository by ID"""
        stmt = select(RepositoryModel).where(RepositoryModel.id == repo_id)
        result = await self.session.execute(stmt)
        db_repository = result.scalar_one_or_none()
        return self._to_entity(db_repository) if db_repository else None

    async def get_by_name(self, name: str) -> Repository | None:
        """Get repository by name"""
        stmt = select(RepositoryModel).where(RepositoryModel.name == name)
        result = await self.session.execute(stmt)
        db_repository = result.scalar_one_or_none()
        return self._to_entity(db_repository) if db_repository else None

    async def get_by_url(self, url: str) -> Repository | None:
        """Get repository by URL"""
        stmt = select(RepositoryModel).where(RepositoryModel.url == url)
        result = await self.session.execute(stmt)
        db_repository = result.scalar_one_or_none()
        return self._to_entity(db_repository) if db_repository else None

    async def get_by_hash(self, repository_hash: str) -> Repository | None:
        """Get repository by hash"""
        stmt = select(RepositoryModel).where(RepositoryModel.repository_hash == repository_hash)
        result = await self.session.execute(stmt)
        db_repository = result.scalar_one_or_none()
        return self._to_entity(db_repository) if db_repository else None

    async def get_by_slug(self, slug: str) -> Repository | None:
        """Get repository by slug"""
        stmt = select(RepositoryModel).where(RepositoryModel.slug == slug)
        result = await self.session.execute(stmt)
        db_repository = result.scalar_one_or_none()
        return self._to_entity(db_repository) if db_repository else None

    async def get_all(self) -> list[Repository]:
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
        db_repository.remote_url = repository.remote_url
        db_repository.repository_hash = repository.repository_hash
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
            remote_url=db_repository.remote_url,
            repository_hash=db_repository.repository_hash,
            slug=db_repository.slug,
            branch=db_repository.branch,
            description=db_repository.description,
            is_local=db_repository.is_local,
            created_at=db_repository.created_at,
            updated_at=db_repository.updated_at,
        )
