from typing import Any, cast
from typing_extensions import override
from datetime import timedelta, datetime, timezone

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError, decode

from app.core.config import pwd_context, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.database import UserAuth, User
from app.interfaces.auth_interface import IAuthService
from app.schemas.user_auth_schemas import UserRequestSchema, UserResponseSchema, LoginSchema


class AuthPersistence(IAuthService):
    """
    Persistence class responsible for authentication-related operations.
    """
    @override
    @classmethod
    async def get_password_hash(cls, password: str) -> str:
        """
        Hashes a plaintext password.
        """
        return pwd_context.hash(password)

    @override
    @classmethod
    async def post_user(
            cls,
            user_info: UserRequestSchema
    ) -> UserResponseSchema | None:
        """
        Registers a new user with the given credentials.
        """
        existing_auth = await UserAuth.filter(username=user_info.username).first()

        if existing_auth:
            return None

        create_user = await User.create(
            name=user_info.name,
            email=user_info.email
        )

        hashed_password = await cls.get_password_hash(user_info.password)

        create_user_auth = await UserAuth.create(
            username=user_info.username,
            password_hash=hashed_password,
            user=create_user
        )

        user_response = UserResponseSchema(
            id=create_user.id,
            name=create_user.name,
            username=create_user_auth.username,
            email=create_user.email,
            is_active=create_user.is_active
        )

        return user_response

    @override
    @classmethod
    async def login_user(
            cls,
            credentials: LoginSchema
    ) -> str | None:
        """
        Authenticates the user and returns a JWT access token.
        """
        user_auth = await UserAuth.get_or_none(username=credentials.username).prefetch_related("user")

        if not user_auth or not pwd_context.verify(credentials.password, user_auth.password_hash):
            return None

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.now(timezone.utc) + access_token_expires
        to_encode = {
            "sub": user_auth.username,
            "exp": expire
        }
        access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return access_token

    @override
    @classmethod
    async def get_current_active_user(
            cls,
            token: str
    ) -> UserResponseSchema | None:
        """
        Extracts the user from the JWT token and ensures they are active.
        """
        try:
            payload = cast(dict[str, Any], decode(token, SECRET_KEY, algorithms=[ALGORITHM]))
            username: str | None = payload.get("sub")
            if username is None:
                return None
        except (ExpiredSignatureError, InvalidTokenError):
            return None

        user_auth = await UserAuth.get_or_none(username=username).prefetch_related("user")
        if not user_auth or not user_auth.user.is_active:
            return None

        user_response = UserResponseSchema(
            id=user_auth.user.id,
            name=user_auth.user.name,
            username=user_auth.username,
            email=user_auth.user.email,
            is_active=user_auth.user.is_active
        )

        return user_response
