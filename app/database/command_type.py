from tortoise import fields, models
import uuid

from tools.application import naive_utcnow


class CommandType(models.Model):
    """
    Defines the different types of commands that can be sent to equipment.

    Attributes:
        id (UUID): Unique identifier of the command type.
        name (str): Name of the command type.
        created_at (datetime): Record creation timestamp.
    """
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=60, unique=True, null=False)
    created_at = fields.DatetimeField(null=False, default=naive_utcnow)

    class Meta:
        table = "CommandTypes"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
