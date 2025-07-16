from typing import List, Optional
from haven.domain.entities.user import User
from haven.domain.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def create_user(
        self, 
        username: str, 
        email: str, 
        display_name: str, 
        avatar_url: Optional[str] = None
    ) -> User:
        """Create a new user"""
        user = User(
            username=username,
            email=email,
            display_name=display_name,
            avatar_url=avatar_url
        )
        
        return await self.user_repository.create(user)
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return await self.user_repository.get_by_id(user_id)
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return await self.user_repository.get_by_username(username)
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return await self.user_repository.get_by_email(email)
    
    async def get_all_users(self) -> List[User]:
        """Get all users"""
        return await self.user_repository.get_all()
    
    async def update_user(
        self, 
        user_id: int, 
        display_name: Optional[str] = None,
        avatar_url: Optional[str] = None
    ) -> User:
        """Update user (only display_name and avatar_url can be updated)"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        
        if display_name is not None:
            user.display_name = display_name
        if avatar_url is not None:
            user.avatar_url = avatar_url
        
        return await self.user_repository.update(user)
    
    async def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        return await self.user_repository.delete(user_id)