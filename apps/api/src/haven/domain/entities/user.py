from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    username: str
    email: str
    display_name: str
    avatar_url: str | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self):
        # Validation logic
        if not self.username:
            raise ValueError("Username cannot be empty")
        if not self.email:
            raise ValueError("Email cannot be empty")
        if "@" not in self.email:
            raise ValueError("Invalid email format")
        if not self.display_name:
            self.display_name = self.username
