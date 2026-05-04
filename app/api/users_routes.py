from typing import List
from uuid import UUID

from fastapi import APIRouter, Path, Body
from starlette import status

from app.schemas.user_auth_schemas import UserResponseSchema, UserUpdateSchema
from app.services.user_service import UserService

users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@users_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[UserResponseSchema],
    summary="List all users",
    description="Returns a list of all registered users."
)
async def get_users() -> List[UserResponseSchema]:
    """
    Returns a list of all registered users.
    """
    return await UserService.get_users()


@users_router.get(
    "/{userId}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchema,
    summary="Get user details",
    description="Returns details of a specific user by userId."
)
async def get_specific_user(
        user_id: UUID = Path(..., description="Unique identifier of the user.", alias="userId"),
) -> UserResponseSchema:
    """
    Retrieves details for a specific user.
    \f
    :param user_id: Unique identifier of the user.
    """
    return await UserService.get_specific_user(user_id)


@users_router.patch(
    "/{userId}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchema,
    summary="Update user information",
    description="Updates user information such as name or email."
)
async def patch_user(
        user_id: UUID = Path(..., description="Unique identifier of the user.", alias="userId"),
        user_data: UserUpdateSchema = Body(..., description="Data information of the user", alias="userData"),
) -> UserResponseSchema:
    """
    Updates user information such as name or email.
    \f
    :param user_id: Unique identifier of the user.
    :param user_data: Data information of the user.
    """
    return await UserService.patch_user(user_id, user_data)


@users_router.delete(
    "/{userId}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Delete a user",
    description="Removes a user from the system."
)
async def delete_user(
        user_id: UUID = Path(..., description="Unique identifier of the user.", alias="userId"),
) -> None:
    """
    Removes a user from the system.
    \f
    :param user_id: Unique identifier of the user.
    """
    return await UserService.delete_user(user_id)
