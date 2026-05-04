from typing import List, Optional
from uuid import UUID

from app.database import UserAuth
from app.interfaces.user_interface import IUserService
from app.schemas.user_auth_schemas import UserUpdateSchema, UserResponseSchema


class UserPersistence(IUserService):
    """
    Persistence class for user-related operations.
    """
    @classmethod
    async def get_users(cls) -> List[UserResponseSchema]:
        """
        Retrieves a list of all registered users along with their authentication details.
        """

        # Fetch authentication records and prefetch related user profile data
        auth_records = await UserAuth.all().prefetch_related("user")
        user_list: List[UserResponseSchema] = []

        # Convert each record into a unified UserResponseSchema
        for auth in auth_records:
            user = auth.user
            user_response = UserResponseSchema(
                id=auth.id,
                username=auth.username,
                name=user.name,
                email=user.email,
                is_active=user.is_active
            )

            user_list.append(user_response)

        return user_list

    @classmethod
    async def get_specific_user(
            cls,
            user_id: UUID
    ) -> Optional[UserResponseSchema]:
        """
        Retrieves a specific user by their ID, including authentication and profile details.
        """

        # Fetch the UserAuth record and load its linked user profile
        user_auth = await UserAuth.get_or_none(id=user_id).prefetch_related("user")

        if not user_auth:
            return None

        user_response = UserResponseSchema(
            id=user_auth.id,
            username=user_auth.username,
            name=user_auth.user.name,
            email=user_auth.user.email,
            is_active=user_auth.user.is_active
        )

        return user_response

    @classmethod
    async def patch_user(
            cls,
            user_id: UUID,
            user_data: UserUpdateSchema
    ) -> Optional[UserResponseSchema]:
        """
        Updates user information such as name, username and email.
        """

        # Fetch the user and their linked profile
        user_auth = await UserAuth.get_or_none(id=user_id).prefetch_related("user")

        # Update profile fields only if new values were provided
        if user_data.name is not None:
            user_auth.user.name = user_data.name
        if user_data.email is not None:
            user_auth.user.email = user_data.email

        # Check if the new username is already taken by another user
        if user_data.username is not None:
            existing = await UserAuth.get_or_none(username=user_data.username)
            if existing and existing.id != user_id:
                return None
            user_auth.username = user_data.username

        # Save changes to both user and auth records
        await user_auth.user.save()
        await user_auth.save()

        return UserResponseSchema(
            id=user_auth.id,
            username=user_auth.username,
            name=user_auth.user.name,
            email=user_auth.user.email,
            is_active=user_auth.user.is_active
        )

    @classmethod
    async def delete_user(
            cls,
            user_id: UUID
    ) -> None:
        """
        Deactivates a user by setting is_active to False.
        """
        # Load the user’s authentication and profile info
        user_auth = await UserAuth.get_or_none(id=user_id).prefetch_related("user")

        # Mark user as inactive
        user_auth.user.is_active = False
        await user_auth.user.save()
