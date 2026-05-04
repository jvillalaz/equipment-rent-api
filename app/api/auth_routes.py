from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.core.config import oauth2_scheme
from app.schemas.user_auth_schemas import UserRequestSchema, UserResponseSchema, TokenSchema, LoginSchema
from app.services.auth_service import AuthService

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@auth_router.post(
    "/register",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a new user account with login credentials."
)
async def register_user(
        user_info: UserRequestSchema = Body(..., description="Data information of the user", alias="userInfo"),
) -> UserResponseSchema:
    """
    Handles user registration by creating a new user and associated login credentials.
    \f
    :param user_info: UserRequestSchema object containing user registration data.
    :return: UserResponseSchema object representing the newly created user.
    """
    return await AuthService.post_user(user_info)


@auth_router.post(
    "/login",
    response_model=TokenSchema,
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    description="Logs a user in."
)
async def login_user(
        credentials: OAuth2PasswordRequestForm = Depends()
) -> TokenSchema:
    """
    Authenticates a user and returns a JWT token upon successful login.
    \f
    :param credentials: OAuth2PasswordRequestForm containing username and password.
    :return: TokenSchema object with access token and token type.
    """
    credentials = LoginSchema(username=credentials.username, password=credentials.password)
    return await AuthService.login_user(credentials)


@auth_router.get(
    "/me",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get current user info",
    description="Returns the authenticated user's information.",
    dependencies=[Depends(oauth2_scheme)],
)
async def get_specific_user(
        current: UserResponseSchema = Depends(AuthService.get_current_active_user)
) -> UserResponseSchema:
    """
    Retrieves the currently authenticated user's details.
    \f
    :param current: UserResponseSchema of the current authenticated user (injected by dependency).
    :return: UserResponseSchema object with user information.
    """
    return current
