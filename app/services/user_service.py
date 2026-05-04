from typing import List, Type
from uuid import UUID

from app.core.exceptions import NotFoundException, ConflictException
from app.interfaces.user_interface import IUserService
from app.schemas.user_auth_schemas import UserResponseSchema, UserUpdateSchema
from tools.application import Service


class UserService(Service):
    """
    Service class for user-related operations.
    """
    user_repository: Type[IUserService]

    def __new__(
        cls,
        user_repository:Type[IUserService],
    ):
        # Assign the user repository implementation to the class.
        cls.user_repository = user_repository
        return cls

    @classmethod
    async def get_users(cls) -> List[UserResponseSchema]:
        """
        Retrieves a list of all registered users along with their authentication details.
        """

        # Retrieve the user from the repository
        user_list = await cls.user_repository.get_users()
        return user_list

    @classmethod
    async def get_specific_user(cls, user_id: UUID) -> UserResponseSchema:
        """
        Retrieves a specific user by their ID, including authentication and profile details.
        """

        # Retrieve the user from the repository
        user = await cls.user_repository.get_specific_user(user_id)

        # Validate user existence
        if user is None:
            raise NotFoundException(detail=f"User {user_id} not found in database")

        return user

    @classmethod
    async def patch_user(cls, user_id: UUID, user_data: UserUpdateSchema) -> UserResponseSchema:
        """
        Updates user information such as name, username and email.
        """

        # Ensure the user exists before attempting to update
        await cls.get_specific_user(user_id)

        # Perform the update in the repository
        update_user = await cls.user_repository.patch_user(user_id, user_data)

        # Handle case where username is already in use
        if not update_user:
            raise ConflictException(detail=f"The '{user_data.username} is already taken'")

        return update_user


    @classmethod
    async def delete_user(cls, user_id: UUID) -> None:
        """
        Deactivates a user by setting is_active to False.
        """

        # Ensure the user exists
        await cls.get_specific_user(user_id)

        # Deactivate user
        delete_user = await cls.user_repository.delete_user(user_id)

        return delete_user
