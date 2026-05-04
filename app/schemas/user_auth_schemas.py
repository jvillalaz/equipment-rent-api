from typing import Optional
from uuid import UUID
from pydantic import EmailStr, Field
from tools.application import DTO


class UserRequestSchema(DTO):
    """
    Request schema for creating a new user with credentials.
    """
    name: str = Field(..., description="Name of the user")
    username: str = Field(..., description="Username used for login")
    email: EmailStr  = Field(..., description="User's email address")
    password: str  = Field(..., description="Hashed password of the user")

class UserResponseSchema(DTO):
    """
    Response schema returning basic information about a registered user.
    """
    id: UUID = Field(..., description="Unique identifier of the user")
    name: str = Field(..., description="Name of the user")
    username: str = Field(..., description="Username used for login")
    email: EmailStr = Field(..., description="User's email address")
    is_active: bool = Field(..., description="Indicates whether the user is active")

class UserUpdateSchema(DTO):
    """
    Schema for updating user profile information.
    """
    name: Optional[str] = Field(None, description="Name of the user")
    username: Optional[str] = Field(None, description="Username used for login")
    email: Optional[EmailStr] = Field(None, description="User's email address")
    is_active: Optional[bool] = Field(None, description="Indicates whether the user is active")

class TokenSchema(DTO):
    """
    Response schema returned after successful authentication.
    """
    access_token: str = Field(..., description="JWT access token for authenticated requests")
    token_type: str = Field(..., description="Type of the token (e.g., 'bearer')")

class TokenDataSchema(DTO):
    """
    Schema representing the decoded information from the JWT token payload.
    """
    username: Optional[str] = Field(None, description="Username extracted from the token payload")

class LoginSchema(DTO):
    """
    Schema for user login credentials.
    Used to authenticate and obtain a JWT token.
    """
    username: str = Field(..., description="Username used for authentication")
    password: str = Field(..., description="User's password")
