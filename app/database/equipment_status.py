from datetime import datetime

from tortoise import fields, models
import uuid

from tools.application import naive_utcnow


class EquipmentStatus(models.Model):
    """
    Stores information about the system's users.

    Attributes:
        id (UUID): Unique identifier of the status equipment.
        name (str): Name of the status equipment.
        created_at (datetime): Record creation timestamp.
    """
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=60, unique=True, null=False)
    created_at = fields.DatetimeField(null=False, default=naive_utcnow)

    class Meta:
        table = "EquipmentStatuses"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
