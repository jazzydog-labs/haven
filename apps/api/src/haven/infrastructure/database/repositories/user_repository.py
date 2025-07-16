
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from haven.domain.entities.user import User
from haven.domain.repositories.user_repository import UserRepository
from haven.infrastructure.database.models import UserModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        """Create a new user"""
        db_user = UserModel(
            username=user.username,
            email=user.email,
            display_name=user.display_name,
            avatar_url=user.avatar_url
        )

        try:
            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)
            return self._to_entity(db_user)
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Username or email already exists") from e

    async def get_by_id(self, user_id: int) -> User | None:
        """Get user by ID"""
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None

    async def get_by_username(self, username: str) -> User | None:
        """Get user by username"""
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email"""
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None

    async def get_all(self) -> list[User]:
        """Get all users"""
        stmt = select(UserModel)
        result = await self.session.execute(stmt)
        db_users = result.scalars().all()
        return [self._to_entity(db_user) for db_user in db_users]

    async def update(self, user: User) -> User:
        """Update existing user"""
        stmt = select(UserModel).where(UserModel.id == user.id)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()

        if not db_user:
            raise ValueError(f"User with id {user.id} not found")

        db_user.username = user.username
        db_user.email = user.email
        db_user.display_name = user.display_name
        db_user.avatar_url = user.avatar_url

        await self.session.commit()
        await self.session.refresh(db_user)
        return self._to_entity(db_user)

    async def delete(self, user_id: int) -> bool:
        """Delete user"""
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()

        if not db_user:
            return False

        await self.session.delete(db_user)
        await self.session.commit()
        return True

    def _to_entity(self, db_user: UserModel) -> User:
        """Convert database model to domain entity"""
        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            display_name=db_user.display_name,
            avatar_url=db_user.avatar_url,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
