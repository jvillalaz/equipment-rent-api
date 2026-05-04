from typing import Type

from app.core.exceptions import ConflictException, UnauthorizedException
from app.interfaces.auth_interface import IAuthService
from app.schemas.user_auth_schemas import UserRequestSchema, UserResponseSchema, TokenSchema, LoginSchema
from tools.application import Service


class AuthService(Service):
    """
    Service class responsible for authentication-related operations.
    """
    auth_repository: Type[IAuthService]

    def __new__(
        cls,
        auth_repository:Type[IAuthService],
    ):
        # Assign the auth repository implementation to the class.
        cls.auth_repository = auth_repository
        return cls

    @classmethod
    async def post_user(
            cls,
            user_info: UserRequestSchema
    ) -> UserResponseSchema:
        """
        Registers a new user with the given credentials.
        """
        user = await cls.auth_repository.post_user(user_info)

        if not user:
            raise ConflictException(detail=f"Username '{user_info.username}' already registered")

        return user

    @classmethod
    async def login_user(
            cls,
            credentials: LoginSchema,
    ) -> TokenSchema:
        """
        Authenticates the user and returns a JWT access token.
        """
        token = await cls.auth_repository.login_user(credentials)

        if not token:
            raise UnauthorizedException(detail="Incorrect username or password")

        return TokenSchema(access_token=token, token_type="bearer")

    @classmethod
    async def get_current_active_user(
            cls,
            token: str
    ) -> UserResponseSchema:
        """
        Extracts the user from the JWT token and ensures they are active.
        """
        asd = await cls.auth_repository.get_current_active_user(token)

        if not asd:
            raise UnauthorizedException(detail="Authentication credentials were missing or invalid")

        return asd
