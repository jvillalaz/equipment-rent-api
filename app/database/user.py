from datetime import datetime

from tortoise.models import Model
from tortoise import fields
import uuid

from tools.application import naive_utcnow


class User(Model):
    """
    Stores information about the system's users.

    Attributes:
        id (UUID): Unique identifier of the user.
        name (str): Name of the user.
        email (str): User's email address.
        is_active (bool): Indicates whether the user is active.
        created_at (datetime): Record creation timestamp.
    """
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=60, null=False)
    email = fields.CharField(max_length=60, unique=True, null=False)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(null=False, default=naive_utcnow)

    class Meta:
        table = "Users"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"
