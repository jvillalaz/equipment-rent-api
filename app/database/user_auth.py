from datetime import datetime
from typing import Optional

from tortoise import fields, models
import uuid

from tools.application import naive_utcnow


class UserAuth(models.Model):
    """
    Stores user credential information.

    Attributes:
        id (UUID): Unique identifier of the record.
        username (str): Username used for login.
        password_hash (datetime): Hashed password of the user.
        user (User): Reference to the corresponding user.
        created_at (datetime): Record creation timestamp.
    """
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    username = fields.CharField(max_length=60, unique=True, null=False)
    password_hash = fields.CharField(max_length=100, null=False)
    user = fields.ForeignKeyField(
        "models.User",
        related_name="auths",
        null=False
    )
    created_at = fields.DatetimeField(null=False, default=naive_utcnow)

    # This field is not part of the actual model definition.
    # It's only added to help the IDE recognize the FK ID attribute.
    user_id: Optional[uuid.UUID]

    class Meta:
        table = "UserAuth"
        ordering = ["-created_at"]

    def __str__(self):
        return self.username
