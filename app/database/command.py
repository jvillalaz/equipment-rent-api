from datetime import datetime
from typing import Optional

from tortoise import fields, models
import uuid

from tools.application import naive_utcnow


class Command(models.Model):
    """
    Records commands sent to equipment.

    Attributes:
        id (UUID): Unique identifier of the command.
        command_type (CommandType): Name of the command type.
        equipment (Equipment): Equipment that will receive the command.
        payload (str): Command data.
        created_at (datetime): Record creation timestamp.
    """
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    command_type = fields.ForeignKeyField(
        "models.CommandType",
        related_name="commands",
        null=False
    )
    equipment = fields.ForeignKeyField(
        "models.Equipment",
        related_name="commands",
        null=False
    )
    payload = fields.CharField(max_length=200, null=True)
    created_at = fields.DatetimeField(null=False, default=naive_utcnow)

    # This field is not part of the actual model definition.
    # It's only added to help the IDE recognize the FK ID attribute.
    command_type_id: Optional[uuid.UUID]
    equipment_id: Optional[uuid.UUID]

    class Meta:
        table = "Commands"
        ordering = ["-created_at"]
