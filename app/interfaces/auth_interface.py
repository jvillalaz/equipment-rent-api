from abc import ABC, abstractmethod
from typing import Optional

from app.core.config import oauth2_scheme
from app.schemas.user_auth_schemas import UserResponseSchema, UserRequestSchema, TokenSchema, LoginSchema


class IAuthService(ABC):
    """
    Interface class responsible for authentication-related operations.
    """
    @classmethod
    @abstractmethod
    async def get_password_hash(cls, password: str) -> str:
        """
        Hashes a plaintext password.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def post_user(
            cls,
            user_info: UserRequestSchema
    ) -> Optional[UserResponseSchema]:
        """
        Registers a new user with the given credentials.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def login_user(
            cls,
            credentials: Optional[LoginSchema],
    ) -> str:
        """
        Authenticates the user and returns a JWT access token.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_current_active_user(
            cls,
            token: str
    ) -> UserResponseSchema:
        """
        Extracts the user from the JWT token and ensures they are active.
        """
        raise NotImplementedError()

