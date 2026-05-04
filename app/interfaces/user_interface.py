from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.schemas.user_auth_schemas import UserResponseSchema, UserUpdateSchema


class IUserService(ABC):
    """
    Interface class for user-related operations.
    """
    @classmethod
    @abstractmethod
    async def get_users(
            cls
    ) -> List[UserResponseSchema]:
        """
        Retrieves a list of all registered users along with their authentication details.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_specific_user(
            cls,
            user_id: UUID
    ) -> Optional[UserResponseSchema]:
        """
        Retrieves a specific user by their ID, including authentication and profile details.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def patch_user(
            cls,
            user_id: UUID,
            user_data: UserUpdateSchema
    ) -> Optional[UserResponseSchema]:
        """
        Updates user information such as name, username and email.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def delete_user(
            cls,
            user_id: UUID
    ) -> None:
        """
        Deactivates a user by setting is_active to False.
        """
        raise NotImplementedError()
